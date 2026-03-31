#!/usr/bin/env python3
"""
Générateur de sprites placeholder pour le MVP Pokémon Rouge/Bleu HD.
Crée des sprites simples mais identifiables pour tester le jeu dans Godot 4.

Sprites générés :
- Joueur : 32×32px, 4 directions × 2 frames (idle + marche)
- Pokémon front : 64×96px avec nom + couleur type
- Pokémon back : 64×96px  
- Pokémon icons : 32×32px
- Tileset outdoor : 32×32px par tile
- UI elements : icônes, cadres
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "sprites")
DATA_DIR = os.path.join(BASE_DIR, "data")

TILE_SIZE = 32
POKEMON_FRONT_SIZE = (64, 96)
POKEMON_BACK_SIZE = (64, 96)
POKEMON_ICON_SIZE = (32, 32)
PLAYER_SIZE = (32, 48)  # Légèrement plus grand que un tile

# Couleurs par type
TYPE_COLORS = {
    "normal":   (168, 168, 120),
    "feu":      (240, 128, 48),
    "eau":      (104, 144, 240),
    "plante":   (120, 200, 80),
    "electrik": (248, 208, 48),
    "glace":    (152, 216, 216),
    "combat":   (192, 48, 40),
    "poison":   (160, 64, 160),
    "sol":      (224, 192, 104),
    "vol":      (168, 144, 240),
    "psy":      (248, 88, 136),
    "insecte":  (168, 184, 32),
    "roche":    (184, 160, 56),
    "spectre":  (112, 88, 152),
    "dragon":   (112, 56, 248),
}

# Couleurs tiles
TILE_COLORS = {
    "herbe":        (88, 168, 72),
    "herbe_haute":  (56, 136, 40),
    "chemin":       (200, 176, 136),
    "eau":          (72, 120, 208),
    "arbre_haut":   (32, 96, 32),
    "arbre_bas":    (40, 112, 40),
    "maison_mur":   (200, 160, 120),
    "maison_toit":  (176, 64, 48),
    "maison_porte": (120, 80, 48),
    "fence":        (160, 128, 96),
    "sable":        (224, 208, 160),
    "fleur":        (88, 168, 72),  # base herbe + points de couleur
    "panneau":      (160, 128, 80),
    "noir":         (16, 16, 16),
    "interieur_sol":(192, 176, 160),
    "interieur_mur":(168, 152, 136),
    "comptoir":     (144, 112, 80),
    "machine_soin": (240, 128, 160),
    "etagere":      (160, 120, 80),
    "tapis_rouge":  (192, 48, 48),
}


def get_font(size=10):
    """Essaie de charger une petite police."""
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        try:
            return ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", size)
        except:
            return ImageFont.load_default()


def draw_text_centered(draw, text, bbox, color=(255, 255, 255), font=None):
    """Dessine du texte centré dans un rectangle."""
    if font is None:
        font = get_font(8)
    # Calculer la taille du texte
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        tw = text_bbox[2] - text_bbox[0]
        th = text_bbox[3] - text_bbox[1]
    except:
        tw, th = len(text) * 6, 10
    x = bbox[0] + (bbox[2] - bbox[0] - tw) // 2
    y = bbox[1] + (bbox[3] - bbox[1] - th) // 2
    draw.text((x, y), text, fill=color, font=font)


# =====================================================================
# JOUEUR — 4 directions × 2 frames (idle, marche)
# =====================================================================
def generate_player_sprites():
    """Génère les sprites du joueur — chapeau rouge, t-shirt bleu, pantalon."""
    out_dir = os.path.join(ASSETS_DIR, "characters")
    os.makedirs(out_dir, exist_ok=True)
    
    directions = {
        "bas":    [(0, 0)],
        "haut":   [(0, 0)],
        "gauche": [(0, 0)],
        "droite": [(0, 0)],
    }
    
    # Couleurs du joueur (style Red)
    HAT_COLOR = (216, 40, 40)
    SKIN_COLOR = (248, 208, 168)
    SHIRT_COLOR = (56, 96, 176)
    PANTS_COLOR = (72, 72, 96)
    SHOE_COLOR = (80, 56, 40)
    HAIR_COLOR = (56, 40, 24)
    
    for direction in ["bas", "haut", "gauche", "droite"]:
        for frame in range(2):
            img = Image.new("RGBA", PLAYER_SIZE, (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            
            w, h = PLAYER_SIZE
            cx = w // 2
            
            # Pieds (y: 40-47) - alternance pour la marche
            if frame == 0:
                d.rectangle([cx-6, 40, cx-2, 47], fill=SHOE_COLOR)
                d.rectangle([cx+1, 40, cx+5, 47], fill=SHOE_COLOR)
            else:
                # Pieds décalés pour animation de marche
                off = 2 if direction in ["bas", "droite"] else -2
                d.rectangle([cx-6+off, 40, cx-2+off, 47], fill=SHOE_COLOR)
                d.rectangle([cx+1-off, 38, cx+5-off, 47], fill=SHOE_COLOR)
            
            # Jambes (y: 32-40)
            d.rectangle([cx-6, 32, cx-2, 40], fill=PANTS_COLOR)
            d.rectangle([cx+1, 32, cx+5, 40], fill=PANTS_COLOR)
            
            # Corps (y: 18-32)
            d.rectangle([cx-8, 18, cx+7, 32], fill=SHIRT_COLOR)
            
            # Bras
            if direction == "gauche":
                d.rectangle([cx-10, 20, cx-8, 30], fill=SHIRT_COLOR)
                d.rectangle([cx+7, 20, cx+9, 28], fill=SHIRT_COLOR)
            elif direction == "droite":
                d.rectangle([cx-10, 20, cx-8, 28], fill=SHIRT_COLOR)
                d.rectangle([cx+7, 20, cx+9, 30], fill=SHIRT_COLOR)
            else:
                d.rectangle([cx-10, 20, cx-8, 30], fill=SHIRT_COLOR)
                d.rectangle([cx+7, 20, cx+9, 30], fill=SHIRT_COLOR)
            
            # Mains
            d.rectangle([cx-10, 28, cx-8, 30], fill=SKIN_COLOR)
            d.rectangle([cx+7, 28, cx+9, 30], fill=SKIN_COLOR)
            
            # Tête (y: 6-18)
            if direction == "bas":
                d.rectangle([cx-7, 6, cx+6, 18], fill=SKIN_COLOR)
                # Yeux
                d.rectangle([cx-5, 11, cx-3, 13], fill=(32, 32, 32))
                d.rectangle([cx+2, 11, cx+4, 13], fill=(32, 32, 32))
                # Bouche
                d.rectangle([cx-2, 15, cx+1, 16], fill=(192, 96, 96))
            elif direction == "haut":
                d.rectangle([cx-7, 6, cx+6, 18], fill=HAIR_COLOR)
            elif direction == "gauche":
                d.rectangle([cx-7, 6, cx+4, 18], fill=SKIN_COLOR)
                d.rectangle([cx+4, 6, cx+6, 18], fill=HAIR_COLOR)
                d.rectangle([cx-5, 11, cx-3, 13], fill=(32, 32, 32))
            elif direction == "droite":
                d.rectangle([cx-7, 6, cx-5, 18], fill=HAIR_COLOR)
                d.rectangle([cx-5, 6, cx+6, 18], fill=SKIN_COLOR)
                d.rectangle([cx+2, 11, cx+4, 13], fill=(32, 32, 32))
            
            # Casquette (y: 2-8)
            d.rectangle([cx-8, 2, cx+7, 7], fill=HAT_COLOR)
            if direction == "bas":
                d.rectangle([cx-9, 6, cx+8, 8], fill=HAT_COLOR)  # visière
            elif direction == "gauche":
                d.rectangle([cx-12, 6, cx-5, 8], fill=HAT_COLOR)
            elif direction == "droite":
                d.rectangle([cx+4, 6, cx+11, 8], fill=HAT_COLOR)
            
            fname = f"player_{direction}_{frame}.png"
            img.save(os.path.join(out_dir, fname))
    
    print(f"  ✓ Joueur : 8 sprites générés dans {out_dir}")


# =====================================================================
# POKÉMON — front / back / icon
# =====================================================================
def generate_pokemon_sprites():
    """Génère les sprites placeholder pour tous les Pokémon du species.json."""
    species_path = os.path.join(DATA_DIR, "pokemon", "species.json")
    with open(species_path, "r", encoding="utf-8") as f:
        species = json.load(f)
    
    front_dir = os.path.join(ASSETS_DIR, "pokemon", "front")
    back_dir = os.path.join(ASSETS_DIR, "pokemon", "back")
    icon_dir = os.path.join(ASSETS_DIR, "pokemon", "icons")
    os.makedirs(front_dir, exist_ok=True)
    os.makedirs(back_dir, exist_ok=True)
    os.makedirs(icon_dir, exist_ok=True)
    
    font_name = get_font(9)
    font_id = get_font(7)
    
    count = 0
    for pid, pdata in species.items():
        nom = pdata.get("nom", f"#{pid}")
        types = pdata.get("types", ["normal"])
        primary_type = types[0]
        color = TYPE_COLORS.get(primary_type, (168, 168, 120))
        
        # Couleur secondaire (plus claire)
        lighter = tuple(min(255, c + 60) for c in color)
        darker = tuple(max(0, c - 40) for c in color)
        
        # --- Front sprite (64×96) ---
        img_front = Image.new("RGBA", POKEMON_FRONT_SIZE, (0, 0, 0, 0))
        df = ImageDraw.Draw(img_front)
        
        # Corps ovale
        df.ellipse([8, 20, 56, 80], fill=color, outline=darker, width=2)
        # Tête
        df.ellipse([14, 8, 50, 44], fill=lighter, outline=darker, width=2)
        # Yeux
        df.ellipse([20, 20, 28, 28], fill=(255, 255, 255), outline=(32, 32, 32))
        df.ellipse([23, 22, 27, 26], fill=(32, 32, 32))
        df.ellipse([36, 20, 44, 28], fill=(255, 255, 255), outline=(32, 32, 32))
        df.ellipse([39, 22, 43, 26], fill=(32, 32, 32))
        # Bouche
        df.arc([26, 28, 38, 36], 0, 180, fill=(64, 32, 32), width=1)
        # Nom en bas
        draw_text_centered(df, nom, (0, 80, 64, 96), color=(255, 255, 255), font=font_name)
        # ID en haut
        draw_text_centered(df, f"#{pid}", (0, 0, 64, 12), color=(200, 200, 200), font=font_id)
        
        img_front.save(os.path.join(front_dir, f"{pid}.png"))
        
        # --- Back sprite (64×96) ---
        img_back = Image.new("RGBA", POKEMON_BACK_SIZE, (0, 0, 0, 0))
        db = ImageDraw.Draw(img_back)
        
        # Corps vu de dos (plus gros, plus bas)
        db.ellipse([6, 24, 58, 88], fill=color, outline=darker, width=2)
        # Tête de dos
        db.ellipse([12, 8, 52, 48], fill=lighter, outline=darker, width=2)
        # Oreilles/cornes simples
        db.polygon([(18, 12), (14, 2), (24, 10)], fill=lighter, outline=darker)
        db.polygon([(46, 12), (50, 2), (40, 10)], fill=lighter, outline=darker)
        # Nom
        draw_text_centered(db, nom, (0, 84, 64, 96), color=(200, 200, 200), font=font_id)
        
        img_back.save(os.path.join(back_dir, f"{pid}.png"))
        
        # --- Icon (32×32) ---
        img_icon = Image.new("RGBA", POKEMON_ICON_SIZE, (0, 0, 0, 0))
        di = ImageDraw.Draw(img_icon)
        di.ellipse([4, 4, 28, 28], fill=color, outline=darker, width=1)
        di.ellipse([10, 6, 22, 16], fill=lighter, outline=darker, width=1)
        # Petits yeux
        di.rectangle([12, 9, 14, 11], fill=(32, 32, 32))
        di.rectangle([18, 9, 20, 11], fill=(32, 32, 32))
        
        img_icon.save(os.path.join(icon_dir, f"{pid}.png"))
        count += 1
    
    print(f"  ✓ Pokémon : {count} espèces × 3 (front/back/icon) = {count*3} sprites")


# =====================================================================
# TILESET — Ensemble de tiles 32×32 pour les cartes
# =====================================================================
def generate_tileset():
    """Génère un tileset outdoor + indoor en une seule image atlas."""
    out_dir = os.path.join(ASSETS_DIR, "tilesets")
    os.makedirs(out_dir, exist_ok=True)
    
    # --- Tileset outdoor : 8 colonnes × 8 lignes = 256×256px ---
    tiles_outdoor = [
        # Ligne 0 : Terrain de base
        ("herbe", "plain"),
        ("herbe_haute", "grass_pattern"),
        ("chemin", "plain"),
        ("sable", "plain"),
        ("eau", "water_pattern"),
        ("fleur", "flower_pattern"),
        ("noir", "plain"),
        ("noir", "plain"),
        # Ligne 1 : Arbres et végétation
        ("arbre_haut", "tree_top"),
        ("arbre_bas", "tree_trunk"),
        ("arbre_haut", "tree_top_r"),
        ("arbre_bas", "tree_trunk_r"),
        ("fence", "fence_h"),
        ("fence", "fence_v"),
        ("herbe", "bush"),
        ("herbe_haute", "tall_grass"),
        # Ligne 2 : Maisons
        ("maison_toit", "roof_l"),
        ("maison_toit", "roof_m"),
        ("maison_toit", "roof_r"),
        ("maison_mur", "wall_l"),
        ("maison_mur", "wall_m"),
        ("maison_mur", "wall_r"),
        ("maison_porte", "door"),
        ("maison_mur", "window"),
        # Ligne 3 : Intérieur
        ("interieur_sol", "plain"),
        ("interieur_mur", "plain"),
        ("comptoir", "plain"),
        ("machine_soin", "machine"),
        ("etagere", "shelf"),
        ("tapis_rouge", "carpet"),
        ("interieur_sol", "tile_pattern"),
        ("interieur_mur", "wall_pattern"),
    ]
    
    cols = 8
    rows = (len(tiles_outdoor) + cols - 1) // cols
    atlas_w = cols * TILE_SIZE
    atlas_h = rows * TILE_SIZE
    
    atlas = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(atlas)
    
    for idx, (tile_name, pattern) in enumerate(tiles_outdoor):
        col = idx % cols
        row = idx // cols
        x0 = col * TILE_SIZE
        y0 = row * TILE_SIZE
        x1 = x0 + TILE_SIZE - 1
        y1 = y0 + TILE_SIZE - 1
        
        base_color = TILE_COLORS.get(tile_name, (128, 128, 128))
        
        # Remplir le fond
        draw.rectangle([x0, y0, x1, y1], fill=base_color)
        
        # Ajouter des patterns selon le type
        if pattern == "grass_pattern":
            # Herbes hautes : petites lignes verticales
            for gx in range(x0 + 2, x1, 6):
                for gy in range(y0 + 2, y1, 8):
                    h_offset = (gx * 7 + gy * 3) % 5
                    draw.line([(gx, gy + h_offset), (gx, gy + h_offset + 4)], 
                             fill=(40, 120, 32), width=1)
                    draw.line([(gx + 2, gy + h_offset + 1), (gx + 3, gy + h_offset - 1)],
                             fill=(48, 140, 36), width=1)
        
        elif pattern == "water_pattern":
            # Eau : petites vagues horizontales
            for wy in range(y0 + 4, y1, 8):
                for wx in range(x0, x1, 12):
                    draw.arc([wx, wy, wx + 10, wy + 4], 0, 180, fill=(88, 144, 232), width=1)
        
        elif pattern == "flower_pattern":
            # Fleurs : points colorés sur herbe
            for fx in range(x0 + 4, x1, 10):
                for fy in range(y0 + 4, y1, 10):
                    colors = [(240, 64, 64), (240, 240, 64), (240, 128, 200)]
                    c = colors[(fx + fy) % 3]
                    draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill=c)
        
        elif pattern == "tree_top":
            # Cime d'arbre : cercle vert foncé
            draw.ellipse([x0+2, y0+4, x1-2, y1], fill=(24, 80, 24), outline=(16, 64, 16))
        
        elif pattern == "tree_top_r":
            draw.ellipse([x0+2, y0+4, x1-2, y1], fill=(28, 88, 28), outline=(16, 64, 16))
        
        elif pattern == "tree_trunk":
            # Tronc d'arbre
            draw.rectangle([x0+10, y0, x0+22, y1], fill=(96, 72, 48))
            draw.ellipse([x0+2, y0-4, x1-2, y0+8], fill=(24, 80, 24))
        
        elif pattern == "tree_trunk_r":
            draw.rectangle([x0+10, y0, x0+22, y1], fill=(104, 76, 52))
            draw.ellipse([x0+2, y0-4, x1-2, y0+8], fill=(28, 88, 28))
        
        elif pattern == "fence_h":
            draw.rectangle([x0, y0+12, x1, y0+20], fill=(144, 112, 80))
            for fx in range(x0+4, x1, 8):
                draw.rectangle([fx, y0+8, fx+3, y0+24], fill=(160, 128, 88))
        
        elif pattern == "fence_v":
            draw.rectangle([x0+12, y0, x0+20, y1], fill=(144, 112, 80))
            for fy in range(y0+4, y1, 8):
                draw.rectangle([x0+8, fy, x0+24, fy+3], fill=(160, 128, 88))
        
        elif pattern == "roof_l":
            draw.polygon([(x0, y1), (x1, y0), (x1, y1)], fill=base_color, outline=(144, 48, 32))
        elif pattern == "roof_m":
            draw.rectangle([x0, y0, x1, y1], fill=base_color)
            draw.line([(x0, y1), (x1, y1)], fill=(144, 48, 32), width=1)
        elif pattern == "roof_r":
            draw.polygon([(x0, y0), (x1, y1), (x0, y1)], fill=base_color, outline=(144, 48, 32))
        
        elif pattern == "wall_l" or pattern == "wall_m" or pattern == "wall_r":
            draw.rectangle([x0, y0, x1, y1], fill=base_color, outline=(176, 144, 104))
        
        elif pattern == "door":
            draw.rectangle([x0+8, y0+4, x1-8, y1], fill=base_color, outline=(96, 64, 32))
            draw.ellipse([x1-14, y0+14, x1-10, y0+18], fill=(200, 176, 48))  # poignée
        
        elif pattern == "window":
            draw.rectangle([x0, y0, x1, y1], fill=base_color, outline=(176, 144, 104))
            draw.rectangle([x0+8, y0+8, x1-8, y1-8], fill=(176, 216, 240), outline=(128, 128, 128))
        
        elif pattern == "machine":
            # Machine de soin Centre Pokémon
            draw.rectangle([x0+4, y0+8, x1-4, y1-2], fill=(200, 200, 200), outline=(128, 128, 128))
            draw.ellipse([x0+10, y0+12, x0+22, y0+24], fill=(240, 80, 80))
            draw.rectangle([x0+14, y0+16, x0+18, y0+20], fill=(255, 255, 255))
        
        elif pattern == "shelf":
            for sy in range(y0+4, y1, 10):
                draw.rectangle([x0+2, sy, x1-2, sy+2], fill=(128, 96, 64))
                for sx in range(x0+4, x1-4, 8):
                    draw.rectangle([sx, sy-6, sx+5, sy], fill=((sx*37)%128+64, (sx*53)%128+64, (sx*71)%128+64))
        
        elif pattern == "carpet":
            draw.rectangle([x0+1, y0+1, x1-1, y1-1], fill=base_color, outline=(160, 32, 32))
        
        elif pattern == "tile_pattern":
            for ty in range(y0, y1+1, 16):
                for tx in range(x0, x1+1, 16):
                    draw.rectangle([tx, ty, tx+15, ty+15], outline=(176, 160, 144))
        
        elif pattern == "wall_pattern":
            draw.rectangle([x0, y0, x1, y1], fill=base_color)
            draw.line([(x0, y1-2), (x1, y1-2)], fill=(144, 128, 112), width=2)
        
        elif pattern == "bush":
            draw.ellipse([x0+2, y0+8, x1-2, y1-2], fill=(48, 128, 40), outline=(32, 96, 24))
    
    atlas.save(os.path.join(out_dir, "tileset_outdoor.png"))
    print(f"  ✓ Tileset outdoor : {atlas_w}×{atlas_h}px ({len(tiles_outdoor)} tiles)")
    
    # Sauvegarder une map de correspondance tile_name → position dans l'atlas
    tile_map_data = {}
    for idx, (tile_name, pattern) in enumerate(tiles_outdoor):
        col = idx % cols
        row = idx // cols
        key = f"{tile_name}_{pattern}" if f"{tile_name}_{pattern}" not in tile_map_data else f"{tile_name}_{pattern}_{idx}"
        tile_map_data[f"tile_{idx}"] = {
            "name": tile_name,
            "pattern": pattern,
            "atlas_x": col * TILE_SIZE,
            "atlas_y": row * TILE_SIZE,
            "col": col,
            "row": row
        }
    
    with open(os.path.join(out_dir, "tileset_map.json"), "w", encoding="utf-8") as f:
        json.dump(tile_map_data, f, indent=2, ensure_ascii=False)
    
    return tiles_outdoor


# =====================================================================
# UI — Éléments d'interface
# =====================================================================
def generate_ui_sprites():
    """Génère les éléments UI basiques."""
    out_dir = os.path.join(ASSETS_DIR, "ui")
    os.makedirs(out_dir, exist_ok=True)
    
    # --- Icône du jeu (64×64) ---
    icon = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(icon)
    # Poké Ball stylisée
    d.ellipse([4, 4, 60, 60], fill=(240, 240, 240), outline=(32, 32, 32), width=2)
    d.pieslice([4, 4, 60, 60], 180, 360, fill=(224, 48, 48), outline=(32, 32, 32), width=2)
    d.line([(4, 32), (60, 32)], fill=(32, 32, 32), width=3)
    d.ellipse([24, 24, 40, 40], fill=(240, 240, 240), outline=(32, 32, 32), width=2)
    d.ellipse([28, 28, 36, 36], fill=(200, 200, 200), outline=(32, 32, 32), width=1)
    icon.save(os.path.join(out_dir, "icon.png"))
    
    # --- Curseur de sélection (16×16) ---
    cursor = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    dc = ImageDraw.Draw(cursor)
    dc.polygon([(2, 2), (14, 8), (2, 14)], fill=(32, 32, 32))
    cursor.save(os.path.join(out_dir, "cursor.png"))
    
    # --- Cadre de dialogue (240×64) ---
    dialog = Image.new("RGBA", (240, 64), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dialog)
    dd.rounded_rectangle([0, 0, 239, 63], radius=8, fill=(248, 248, 240), outline=(32, 32, 32), width=2)
    dialog.save(os.path.join(out_dir, "dialog_frame.png"))
    
    # --- Barre de PV vide (48×6) ---
    hp = Image.new("RGBA", (48, 6), (0, 0, 0, 0))
    dh = ImageDraw.Draw(hp)
    dh.rectangle([0, 0, 47, 5], fill=(40, 40, 40), outline=(80, 80, 80))
    hp.save(os.path.join(out_dir, "hp_bar_bg.png"))
    
    # --- Poké Ball sprite (16×16) pour l'inventaire ---
    ball = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    db = ImageDraw.Draw(ball)
    db.ellipse([1, 1, 15, 15], fill=(240, 240, 240), outline=(32, 32, 32))
    db.pieslice([1, 1, 15, 15], 180, 360, fill=(224, 48, 48), outline=(32, 32, 32))
    db.line([(1, 8), (15, 8)], fill=(32, 32, 32), width=1)
    db.ellipse([6, 6, 10, 10], fill=(240, 240, 240), outline=(32, 32, 32))
    ball.save(os.path.join(out_dir, "pokeball_item.png"))
    
    # --- Cadre de combat (panneau info Pokémon) ---
    for prefix, size in [("panel_joueur", (160, 48)), ("panel_ennemi", (150, 40))]:
        panel = Image.new("RGBA", size, (0, 0, 0, 0))
        dp = ImageDraw.Draw(panel)
        dp.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=6, 
                            fill=(248, 248, 232), outline=(64, 64, 64), width=2)
        panel.save(os.path.join(out_dir, f"{prefix}.png"))
    
    # --- Fond de combat ---
    battle_bg = Image.new("RGBA", (480, 320), (0, 0, 0, 0))
    dbg = ImageDraw.Draw(battle_bg)
    # Ciel gradient
    for y in range(160):
        r = int(136 + (200 - 136) * y / 160)
        g = int(192 + (232 - 192) * y / 160)
        b = int(240 + (255 - 240) * y / 160)
        dbg.line([(0, y), (479, y)], fill=(r, g, b))
    # Sol (herbe)
    for y in range(160, 320):
        g = int(160 - (y - 160) * 0.3)
        dbg.line([(0, y), (479, y)], fill=(72, g, 48))
    # Ligne d'horizon
    dbg.line([(0, 160), (479, 160)], fill=(96, 144, 64), width=2)
    # Plateforme joueur
    dbg.ellipse([40, 220, 200, 280], fill=(104, 168, 72), outline=(72, 128, 48))
    # Plateforme ennemi
    dbg.ellipse([280, 130, 440, 170], fill=(104, 168, 72), outline=(72, 128, 48))
    battle_bg.save(os.path.join(out_dir, "battle_bg.png"))
    
    print(f"  ✓ UI : icon, cursor, dialog_frame, hp_bar, pokeball, panels, battle_bg")


# =====================================================================
# NPC sprites
# =====================================================================
def generate_npc_sprites():
    """Génère quelques sprites PNJ basiques."""
    out_dir = os.path.join(ASSETS_DIR, "characters")
    os.makedirs(out_dir, exist_ok=True)
    
    npcs = {
        "prof_chen": ((240, 240, 240), (176, 144, 104), "Prof"),       # Blouse blanche
        "rival":     ((96, 64, 160), (168, 136, 96), "Rival"),          # Violet
        "infirmiere":((240, 160, 168), (240, 120, 136), "Joëlle"),     # Rose
        "vendeur":   ((64, 112, 192), (168, 136, 96), "Vendeur"),       # Bleu
        "pnj_homme": ((120, 96, 72), (168, 136, 96), "PNJ"),           # Marron
        "pnj_femme": ((192, 80, 96), (168, 136, 96), "PNJ"),           # Rose rouge
        "dresseur_m":((80, 128, 80), (168, 136, 96), "Dres"),          # Vert
        "dresseur_f":((200, 160, 80), (168, 136, 96), "Dres"),         # Jaune
    }
    
    for npc_id, (shirt_color, hair_color, label) in npcs.items():
        for direction in ["bas"]:  # Juste le sprite de face pour le MVP
            img = Image.new("RGBA", PLAYER_SIZE, (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            w, h = PLAYER_SIZE
            cx = w // 2
            
            SKIN = (248, 208, 168)
            
            # Corps
            d.rectangle([cx-8, 18, cx+7, 32], fill=shirt_color)
            d.rectangle([cx-10, 20, cx-8, 30], fill=shirt_color)
            d.rectangle([cx+7, 20, cx+9, 30], fill=shirt_color)
            # Jambes
            d.rectangle([cx-6, 32, cx-2, 42], fill=(72, 72, 96))
            d.rectangle([cx+1, 32, cx+5, 42], fill=(72, 72, 96))
            # Pieds
            d.rectangle([cx-7, 42, cx-1, 47], fill=(80, 56, 40))
            d.rectangle([cx, 42, cx+6, 47], fill=(80, 56, 40))
            # Tête
            d.rectangle([cx-7, 6, cx+6, 18], fill=SKIN)
            d.rectangle([cx-5, 11, cx-3, 13], fill=(32, 32, 32))
            d.rectangle([cx+2, 11, cx+4, 13], fill=(32, 32, 32))
            d.rectangle([cx-2, 15, cx+1, 16], fill=(192, 96, 96))
            # Cheveux
            d.rectangle([cx-8, 2, cx+7, 7], fill=hair_color)
            
            img.save(os.path.join(out_dir, f"{npc_id}_bas_0.png"))
    
    print(f"  ✓ PNJ : {len(npcs)} sprites générés")


# =====================================================================
# Main
# =====================================================================
if __name__ == "__main__":
    print("=== Génération des sprites placeholder ===")
    print()
    
    # Nettoyer les .gitkeep
    for root, dirs, files in os.walk(ASSETS_DIR):
        for f in files:
            if f == ".gitkeep":
                os.remove(os.path.join(root, f))
    
    generate_player_sprites()
    generate_pokemon_sprites()
    generate_tileset()
    generate_npc_sprites()
    generate_ui_sprites()
    
    print()
    print("=== Terminé ! ===")
