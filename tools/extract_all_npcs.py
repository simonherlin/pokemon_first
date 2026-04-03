#!/usr/bin/env python3
"""
Extraction de TOUS les sprites PNJ depuis la feuille FRLG overworld NPC.
Chaque bande est extraite en 12 frames (4 directions × 3 frames),
redimensionnée 2× et sauvegardée au format du jeu:
  {sprite_id}_{direction}_{frame}.png
"""

from PIL import Image
import numpy as np
import os
import json

# --- Configuration ---
SHEET_PATH = "tools/source_sprites/frlg_overworld_npcs.png"
OUTPUT_DIR = "assets/sprites/characters"
TARGET_HEIGHT = 64  # Hauteur finale en pixels (2× depuis 32px GBA, ou adapté)
TARGET_WIDTH = 32   # Largeur finale (2× depuis 16px)

# Couleur orange du fond (à rendre transparent)
ORANGE = np.array([255, 127, 39])

# Positions X des 12 colonnes de sprites
COL_STARTS = [9, 26, 43, 60, 77, 94, 111, 128, 145, 162, 179, 196]
CELL_W = 16

# Mapping directions : cellules 0-2 = bas, 3-5 = haut, 6-8 = gauche, 9-11 = droite
DIRECTIONS = {
    "bas":     [0, 1, 2],
    "haut":    [3, 4, 5],
    "gauche":  [6, 7, 8],
    "droite":  [9, 10, 11],
}

# --- Mapping bande → sprite_id(s) du jeu ---
# Ordre standard de la feuille FRLG NPC overworld (spriters-resource)
# Les bandes < 24px de haut sont souvent des items/objets/petits sprites
BAND_MAPPING = {
    # Personnages principaux
    0: ["red_normal"],        # Red/Joueur debout
    1: ["pnj_chen", "prof_chen", "prof_oak"],  # Prof. Chêne
    2: ["pnj_rival", "green_normal"],  # Rival
    3: ["player"],            # Red variante / Leaf
    # PNJ génériques  
    4: ["boy", "pnj_garcon"],  # Garçon
    5: ["pnj_homme"],         # Homme adulte
    6: ["pnj_femme"],         # Femme adulte
    7: ["pnj_fille"],         # Fille
    8: ["pnj_vieil_homme", "pnj_vieux"],  # Vieil homme
    9: ["old_woman"],          # Vieille femme
    10: ["gentleman"],        # Gentleman
    11: ["fat_man"],          # Homme gros
    12: ["youngster", "pnj_gamin"],   # Gamin
    13: ["lass", "pnj_gamine"],       # Gamine
    14: ["bug_catcher", "pnj_insectomane"],  # Chasseur d'insectes
    15: ["fisher", "pnj_pecheur"],      # Pêcheur
    16: ["hiker", "pnj_montagnard", "pnj_randonneur"],  # Randonneur/Montagnard
    17: ["beauty", "pnj_randonneuse"],  # Belle / Randonneuse
    18: ["sailor", "pnj_marin"],       # Marin
    19: ["pnj_campeur"],              # Campeur
    20: ["biker", "pnj_motard"],       # Motard (32px)
    21: ["scientist", "pnj_scientifique"],  # Scientifique
    22: ["rocket_m", "pnj_rocket", "pnj_rocket_homme"],  # Rocket homme
    23: ["rocket_f", "pnj_rocket_femme"],  # Rocket femme
    24: ["nurse", "pnj_infirmiere", "infirmiere"],  # Infirmière
    25: ["clerk", "vendeur", "pnj_vendeur"],   # Vendeur/Clerk
    # Champions et personnages clés
    26: ["brock", "pnj_champion_bob"],   # Bob (Brock)
    27: ["misty", "pnj_champion_ondine"], # Ondine (Misty)
    28: ["lt_surge"],       # Major Bob
    29: ["erika", "champion_erika"],     # Erika
    30: ["koga"],           # Koga
    31: ["sabrina"],        # Sabrina
    32: ["blaine"],         # Auguste (Blaine)
    33: ["giovanni", "pnj_giovanni"],    # Giovanni
    34: ["lorelei"],        # Olga (Lorelei)
    35: ["bruno"],          # Aldo (Bruno)
    36: ["agatha"],         # Agatha
    37: ["lance"],          # Peter (Lance)
    # Dresseurs spéciaux
    38: ["channeler", "pnj_medium"],    # Médium/Channeler
    39: ["pnj_jongleur"],              # Jongleur
    40: ["pnj_karateka"],             # Karatéka
    41: ["pnj_garde"],               # Garde
    42: ["dresseur", "dresseur_m", "pnj_dresseur", "pnj_dresseur_m"],  # Dresseur M
    43: ["dresseur_f"],               # Dresseur F
    # PNJ spéciaux
    46: ["mr_fuji"],                  # Mr. Fuji
    47: ["bill"],                     # Bill
    48: ["pnj_capitaine"],            # Capitaine (32px)
    51: ["pnj_fillette"],             # Fillette
    52: ["pnj_nageur"],               # Nageur
    54: ["pnj_nageuse"],              # Nageuse
    55: ["dresseur_randonneur"],       # Randonneur dresseur
    # Pokémon/Objets spéciaux
    85: ["pnj_legendaire", "pokemon_legendaire"],  # Grand sprite (28px)
    87: ["pnj_ronflex"],              # Ronflex (32px)
}


def detect_bands(arr):
    """Détecte les bandes de sprites dans la feuille NPC."""
    orange_rows = []
    for y in range(arr.shape[0]):
        matches = np.all(arr[y, :, :3] == ORANGE, axis=1)
        if np.sum(matches) > 10:
            orange_rows.append(y)
    
    bands = []
    if not orange_rows:
        return bands
    
    start = orange_rows[0]
    prev = orange_rows[0]
    for y in orange_rows[1:]:
        if y > prev + 1:
            bands.append((start, prev))
            start = y
        prev = y
    bands.append((start, prev))
    
    # Garder seulement les bandes valides (>= 16px de haut)
    return [(s, e) for s, e in bands if e - s + 1 >= 16]


def extract_cell(img_arr, y_start, y_end, col_idx):
    """Extrait une cellule de sprite de la feuille."""
    x = COL_STARTS[col_idx]
    h = y_end - y_start + 1
    cell = img_arr[y_start:y_end + 1, x:x + CELL_W].copy()
    
    # Remplacer l'orange par la transparence
    mask = np.all(cell[:, :, :3] == ORANGE, axis=2)
    cell[mask, 3] = 0
    
    # Aussi rendre transparent le blanc pur qui est souvent le fond de la feuille
    white_mask = np.all(cell[:, :, :3] == [255, 255, 255], axis=2)
    cell[white_mask, 3] = 0
    
    return Image.fromarray(cell)


def pad_and_scale(cell_img, target_w=TARGET_WIDTH, target_h=TARGET_HEIGHT):
    """Padding pour atteindre les proportions cible, puis mise à l'échelle 2×."""
    w, h = cell_img.size
    
    # D'abord, on padde à 16×32 si nécessaire
    native_w = 16
    native_h = 32
    
    if h < native_h:
        # Ajouter du transparent en haut pour centrer le sprite
        pad_top = native_h - h
        padded = Image.new("RGBA", (native_w, native_h), (0, 0, 0, 0))
        padded.paste(cell_img, (0, pad_top))
        cell_img = padded
    elif h > native_h:
        # Si plus grand, on garde la taille native et on scale
        native_h = h
    
    # Mise à l'échelle 2×
    scale_x = target_w / native_w
    scale_y = target_h / native_h if native_h == 32 else 2.0
    
    final_w = int(cell_img.width * 2)
    final_h = int(cell_img.height * 2)
    
    return cell_img.resize((final_w, final_h), Image.NEAREST)


def main():
    img = Image.open(SHEET_PATH)
    arr = np.array(img)
    bands = detect_bands(arr)
    print(f"Détecté {len(bands)} bandes valides")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    total_saved = 0
    sprites_generated = {}
    
    for band_idx, (y_start, y_end) in enumerate(bands):
        h = y_end - y_start + 1
        sprite_ids = BAND_MAPPING.get(band_idx, [])
        
        if not sprite_ids:
            # Bande non mappée — sauter pour l'instant
            continue
        
        print(f"Bande {band_idx} (h={h}): {sprite_ids}")
        
        for sprite_id in sprite_ids:
            for dir_name, cell_indices in DIRECTIONS.items():
                for frame_idx, col_idx in enumerate(cell_indices):
                    cell = extract_cell(arr, y_start, y_end, col_idx)
                    final = pad_and_scale(cell)
                    
                    fname = f"{sprite_id}_{dir_name}_{frame_idx}.png"
                    fpath = os.path.join(OUTPUT_DIR, fname)
                    final.save(fpath)
                    total_saved += 1
            
            sprites_generated[sprite_id] = band_idx
    
    print(f"\n{'='*50}")
    print(f"Total fichiers sauvegardés : {total_saved}")
    print(f"Sprites uniques générés : {len(sprites_generated)}")
    
    # Lister les sprite_ids du jeu qui n'ont PAS été extraits
    with open("data/maps/bourg_palette.json") as f:
        pass  # Just to check we're in the right dir
    
    # Check game sprite usage
    import glob
    used_sprites = set()
    for f in glob.glob("data/maps/*.json"):
        with open(f) as fh:
            try:
                d = json.load(fh)
            except:
                continue
        for pnj in d.get("pnj", []):
            s = pnj.get("sprite", "")
            if s:
                used_sprites.add(s)
    
    mapped = set(sprites_generated.keys())
    missing = used_sprites - mapped
    print(f"\nSprites utilisés dans le jeu : {len(used_sprites)}")
    print(f"Sprites extraits : {len(mapped)}")
    print(f"Manquants : {len(missing)}")
    if missing:
        for s in sorted(missing):
            print(f"  - {s}")


if __name__ == "__main__":
    main()
