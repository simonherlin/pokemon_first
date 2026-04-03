#!/usr/bin/env python3
"""
Render FRLG metatiles from pokefirered decomp data.

GBA metatile format:
- tiles.png: indexed-color image, 128px wide (16 tiles of 8×8 per row)
- palettes/*.pal: JASC-PAL files, 16 colors each (color 0 = transparent)
- metatiles.bin: 16 bytes per metatile
  - Each metatile has 2 layers (bottom, top) × 4 tiles (2×2)
  - Each tile reference = 2 bytes (little-endian):
    bits 0-9:   tile index in combined tile image
    bit 10:     horizontal flip
    bit 11:     vertical flip
    bits 12-15: palette index

Primary tilesets have tiles 0-639, metatiles 0-639.
Secondary tilesets add tiles starting at index 640.
"""

import os
import struct
import numpy as np
from PIL import Image

BASE_DIR = os.path.join(os.path.dirname(__file__), "source_sprites", "frlg_tilesets")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "source_sprites", "frlg_rendered")

NUM_PRIMARY_TILES = 640


def load_palettes(pal_dir):
    """Charge les 16 palettes JASC depuis un répertoire."""
    palettes = []
    for i in range(16):
        pal_file = os.path.join(pal_dir, f"{i:02d}.pal")
        colors = []
        if os.path.exists(pal_file):
            with open(pal_file, 'r') as f:
                lines = f.readlines()
                # Format: JASC-PAL / 0100 / 16 / R G B × 16
                for line in lines[3:]:  # Skip header (3 lines)
                    parts = line.strip().split()
                    if len(parts) == 3:
                        colors.append(tuple(int(x) for x in parts))
        # Pad to 16 colors if needed
        while len(colors) < 16:
            colors.append((0, 0, 0))
        palettes.append(colors)
    return palettes


def load_tiles(tiles_png_path):
    """Charge les tiles 8×8 depuis une image indexée.
    Retourne un array numpy de shape (num_tiles, 8, 8) avec les palette indices."""
    img = Image.open(tiles_png_path)
    # Convert to numpy keeping palette indices
    data = np.array(img)  # Shape: (height, width), values = palette indices
    
    h, w = data.shape
    tiles_per_row = w // 8
    tiles_per_col = h // 8
    num_tiles = tiles_per_row * tiles_per_col
    
    tiles = np.zeros((num_tiles, 8, 8), dtype=np.uint8)
    for row in range(tiles_per_col):
        for col in range(tiles_per_row):
            idx = row * tiles_per_row + col
            tiles[idx] = data[row*8:(row+1)*8, col*8:(col+1)*8]
    
    return tiles


def load_metatiles_bin(meta_path):
    """Charge les définitions de metatiles depuis metatiles.bin.
    Retourne une liste de metatiles, chaque metatile = 8 tuples (tile_idx, hflip, vflip, pal_idx)."""
    with open(meta_path, 'rb') as f:
        data = f.read()
    
    num_metatiles = len(data) // 16
    metatiles = []
    
    for i in range(num_metatiles):
        refs = []
        for j in range(8):
            offset = i * 16 + j * 2
            val = struct.unpack_from('<H', data, offset)[0]
            tile_idx = val & 0x3FF
            hflip = bool(val & 0x400)
            vflip = bool(val & 0x800)
            pal_idx = (val >> 12) & 0xF
            refs.append((tile_idx, hflip, vflip, pal_idx))
        metatiles.append(refs)
    
    return metatiles


def render_tile_8x8(tile_data, palette, hflip=False, vflip=False):
    """Rend une tile 8×8 en RGBA en utilisant la palette donnée.
    Retourne un array numpy (8, 8, 4)."""
    result = np.zeros((8, 8, 4), dtype=np.uint8)
    
    for y in range(8):
        for x in range(8):
            pal_idx = tile_data[y, x] % 16
            r, g, b = palette[pal_idx]
            # Color 0 is transparent
            alpha = 0 if pal_idx == 0 else 255
            result[y, x] = [r, g, b, alpha]
    
    if hflip:
        result = result[:, ::-1, :]
    if vflip:
        result = result[::-1, :, :]
    
    return result


def render_metatile(meta_refs, all_tiles, palettes):
    """Rend un metatile 16×16 en RGBA.
    meta_refs: 8 tuples (tile_idx, hflip, vflip, pal_idx)
    - refs[0-3] = bottom layer (TL, TR, BL, BR)
    - refs[4-7] = top layer (TL, TR, BL, BR)
    """
    result = np.zeros((16, 16, 4), dtype=np.uint8)
    
    # Positions for 2x2 arrangement: TL, TR, BL, BR
    positions = [(0, 0), (8, 0), (0, 8), (8, 8)]
    
    # Bottom layer first
    for i in range(4):
        tile_idx, hflip, vflip, pal_idx = meta_refs[i]
        if tile_idx < len(all_tiles):
            tile = render_tile_8x8(all_tiles[tile_idx], palettes[pal_idx], hflip, vflip)
            x, y = positions[i]
            result[y:y+8, x:x+8] = tile
    
    # Top layer (alpha-blend over bottom)
    for i in range(4):
        tile_idx, hflip, vflip, pal_idx = meta_refs[4 + i]
        if tile_idx < len(all_tiles):
            tile = render_tile_8x8(all_tiles[tile_idx], palettes[pal_idx], hflip, vflip)
            x, y = positions[i]
            # Alpha blend: top over bottom
            for py in range(8):
                for px in range(8):
                    if tile[py, px, 3] > 0:  # Non-transparent
                        result[y+py, x+px] = tile[py, px]
    
    return result


def render_tileset(primary_name, secondary_name=None, output_name=None):
    """Rend tous les metatiles d'un tileset combiné (primary + secondary).
    Retourne une liste d'images PIL 16×16."""
    
    pri_dir = os.path.join(BASE_DIR, primary_name)
    
    # Charger primary
    pri_tiles = load_tiles(os.path.join(pri_dir, "tiles.png"))
    pri_palettes = load_palettes(os.path.join(pri_dir, "palettes"))
    pri_metatiles = load_metatiles_bin(os.path.join(pri_dir, "metatiles.bin"))
    
    all_tiles = pri_tiles
    all_palettes = pri_palettes  # Start with primary palettes
    
    sec_metatiles = []
    if secondary_name:
        sec_dir = os.path.join(BASE_DIR, secondary_name)
        sec_tiles = load_tiles(os.path.join(sec_dir, "tiles.png"))
        sec_palettes = load_palettes(os.path.join(sec_dir, "palettes"))
        sec_metatiles = load_metatiles_bin(os.path.join(sec_dir, "metatiles.bin"))
        
        # Combine tiles: primary 0-639, secondary starts at 640
        # Pad primary tiles to 640 if needed
        if len(all_tiles) < NUM_PRIMARY_TILES:
            padding = np.zeros((NUM_PRIMARY_TILES - len(all_tiles), 8, 8), dtype=np.uint8)
            all_tiles = np.concatenate([all_tiles, padding])
        all_tiles = np.concatenate([all_tiles, sec_tiles])
        
        # Secondary palettes override slots 7-15 typically
        # But in practice, each tile ref specifies which palette to use
        # Merge: primary uses palettes 0-6, secondary uses 7-12
        # Actually, in FRLG both primary and secondary have 16 palettes
        # The palettes for tiles depend on which tileset they belong to
        # For simplicity: use primary palettes for tiles 0-639, secondary for 640+
        # But tile refs include palette index... they share the same palette space
        # In FRLG: primary palettes occupy slots 0-6, secondary 7-12
        # Let's merge: keep primary as-is, overlay secondary onto slots 7+
        for i in range(7, 16):
            if i < len(sec_palettes):
                all_palettes[i] = sec_palettes[i]
    
    # Render all metatiles
    rendered = []
    
    print(f"  Rendering {len(pri_metatiles)} primary + {len(sec_metatiles)} secondary metatiles...")
    
    for meta in pri_metatiles:
        img_data = render_metatile(meta, all_tiles, all_palettes)
        rendered.append(img_data)
    
    for meta in sec_metatiles:
        img_data = render_metatile(meta, all_tiles, all_palettes)
        rendered.append(img_data)
    
    return rendered


def save_metatile_sheet(rendered_metatiles, output_path, cols=16):
    """Sauvegarde une feuille de tous les metatiles rendus."""
    n = len(rendered_metatiles)
    rows = (n + cols - 1) // cols
    
    sheet = np.zeros((rows * 16, cols * 16, 4), dtype=np.uint8)
    
    for i, meta in enumerate(rendered_metatiles):
        row = i // cols
        col = i % cols
        sheet[row*16:(row+1)*16, col*16:(col+1)*16] = meta
    
    img = Image.fromarray(sheet, 'RGBA')
    img.save(output_path)
    print(f"  Saved: {output_path} ({img.size[0]}×{img.size[1]}, {n} metatiles)")
    return img


def save_metatile_sheet_2x(rendered_metatiles, output_path, cols=16):
    """Sauvegarde une feuille à échelle 2× (32×32 par metatile)."""
    n = len(rendered_metatiles)
    rows = (n + cols - 1) // cols
    
    sheet = np.zeros((rows * 32, cols * 32, 4), dtype=np.uint8)
    
    for i, meta in enumerate(rendered_metatiles):
        row = i // cols
        col = i % cols
        # Scale 2× with nearest neighbor
        scaled = np.repeat(np.repeat(meta, 2, axis=0), 2, axis=1)
        sheet[row*32:(row+1)*32, col*32:(col+1)*32] = scaled
    
    img = Image.fromarray(sheet, 'RGBA')
    img.save(output_path)
    print(f"  Saved 2×: {output_path} ({img.size[0]}×{img.size[1]})")
    return img


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1) Render primary/general alone (outdoor shared tiles)
    print("=== Primary General (outdoor shared) ===")
    general_metas = render_tileset("primary_general")
    save_metatile_sheet(general_metas, os.path.join(OUTPUT_DIR, "primary_general_16.png"))
    save_metatile_sheet_2x(general_metas, os.path.join(OUTPUT_DIR, "primary_general_32.png"))
    
    # 2) Render primary/building alone (indoor shared tiles)
    print("\n=== Primary Building (indoor shared) ===")
    building_metas = render_tileset("primary_building")
    save_metatile_sheet(building_metas, os.path.join(OUTPUT_DIR, "primary_building_16.png"))
    save_metatile_sheet_2x(building_metas, os.path.join(OUTPUT_DIR, "primary_building_32.png"))
    
    # 3) Render combined tilesets for key areas
    areas = [
        ("pallet_town", "Bourg Palette"),
        ("viridian_city", "Jadielle"),
        ("pewter_city", "Argenta"),
        ("cerulean_city", "Azuria"),
        ("vermilion_city", "Carmin-sur-Mer"),
        ("celadon_city", "Céladopole"),
        ("saffron_city", "Safrania"),
        ("fuchsia_city", "Parmanie"),
        ("cinnabar_island", "Cramois'Île"),
        ("lavender_town", "Lavanville"),
        ("viridian_forest", "Forêt de Jade"),
        ("cave", "Grottes"),
        ("pokemon_center", "Centre Pokémon"),
        ("mart", "Boutique"),
        ("rock_tunnel", "Tunnel Taupiqueur"),
        ("seafoam_islands", "Îles Écume"),
        ("pokemon_tower", "Tour Pokémon"),
    ]
    
    for area_name, area_label in areas:
        sec_name = f"secondary_{area_name}"
        if not os.path.isdir(os.path.join(BASE_DIR, sec_name)):
            print(f"\n=== SKIP {area_label} (pas de données) ===")
            continue
        
        print(f"\n=== {area_label} (general + {area_name}) ===")
        metas = render_tileset("primary_general", sec_name, area_name)
        save_metatile_sheet(metas, os.path.join(OUTPUT_DIR, f"{area_name}_16.png"))
        save_metatile_sheet_2x(metas, os.path.join(OUTPUT_DIR, f"{area_name}_32.png"))
    
    print("\n✓ Rendu terminé!")
    print(f"  Fichiers dans: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
