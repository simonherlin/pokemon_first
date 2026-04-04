#!/usr/bin/env python3
"""
Extraction FIABLE des sprites PNJ depuis le decomp pokefirered (pret/pokefirered).
Télécharge les PNGs individuels nommés par personnage, convertit en RGBA,
extrait les frames d'animation, scale 2× et sauvegarde au format du jeu.
"""

from PIL import Image
import io
import os
import urllib.request

OUTPUT_DIR = "assets/sprites/characters"
BASE_URL = "https://raw.githubusercontent.com/pret/pokefirered/master/graphics/object_events/pics/people"

# Mapping : fichier decomp → liste de sprite_ids du jeu
# Chaque sprite du decomp génère un ou plusieurs sprite_ids
SPRITE_MAP = {
    # === Personnages principaux ===
    "red_normal": ["player", "red_normal"],
    "prof_oak": ["pnj_chen", "prof_chen", "prof_oak"],
    "blue": ["pnj_rival", "green_normal"],
    "mom": ["maman"],
    "daisy": ["pnj_daisy", "soeur_rival"],

    # === PNJ génériques ===
    "man": ["pnj_homme"],
    "woman_1": ["pnj_femme"],
    "woman_2": ["pnj_femme2"],
    "woman_3": ["pnj_femme3"],
    "boy": ["pnj_garcon", "boy"],
    "old_man_1": ["pnj_vieil_homme", "pnj_vieux"],
    "old_man_2": ["pnj_vieux2"],
    "old_woman": ["old_woman", "pnj_vieille"],
    "gentleman": ["gentleman"],
    "fat_man": ["fat_man", "pnj_gros"],
    "little_boy": ["pnj_petit_garcon"],
    "little_girl": ["pnj_fillette", "pnj_petite_fille"],
    "balding_man": ["pnj_chauve"],

    # === Dresseurs classiques ===
    "youngster": ["youngster", "pnj_gamin"],
    "lass": ["lass", "pnj_gamine"],
    "bug_catcher": ["bug_catcher", "pnj_insectomane"],
    "fisher": ["fisher", "pnj_pecheur"],
    "hiker": ["hiker", "pnj_montagnard", "pnj_randonneur", "dresseur_randonneur"],
    "beauty": ["beauty", "pnj_randonneuse"],
    "sailor": ["sailor", "pnj_marin"],
    "camper": ["pnj_campeur"],
    "picnicker": ["pnj_pique_niqueuse"],
    "biker": ["biker", "pnj_motard"],
    "scientist": ["scientist", "pnj_scientifique"],
    "rocker": ["rocker", "pnj_rocker"],
    "poke_maniac": ["pnj_poke_maniaque"],
    "cooltrainer_m": ["dresseur", "dresseur_m", "pnj_dresseur", "pnj_dresseur_m"],
    "cooltrainer_f": ["dresseur_f", "pnj_dresseur_f"],
    "black_belt": ["pnj_karateka"],
    "channeler": ["channeler", "pnj_medium"],
    "swimmer_m_land": ["pnj_nageur"],
    "swimmer_f_land": ["pnj_nageuse"],
    "policeman": ["pnj_garde"],
    "worker_m": ["pnj_ouvrier"],

    # === Team Rocket ===
    "rocket_m": ["rocket_m", "pnj_rocket", "pnj_rocket_homme"],
    "rocket_f": ["rocket_f", "pnj_rocket_femme"],

    # === Personnel ===
    "nurse": ["nurse", "pnj_infirmiere", "infirmiere"],
    "clerk": ["clerk", "vendeur", "pnj_vendeur"],
    "gym_guy": ["pnj_guide_arene"],
    "captain": ["pnj_capitaine"],

    # === Champions d'arène ===
    "brock": ["brock"],
    "misty": ["misty"],
    "lt_surge": ["lt_surge"],
    "erika": ["erika", "champion_erika"],
    "koga": ["koga"],
    "sabrina": ["sabrina"],
    "blaine": ["blaine"],
    "giovanni": ["giovanni", "pnj_giovanni", "champion"],

    # === Conseil des 4 ===
    "lorelei": ["lorelei"],
    "bruno": ["bruno"],
    "agatha": ["agatha"],
    "lance": ["lance"],

    # === PNJ spéciaux ===
    "mr_fuji": ["mr_fuji"],
    "bill": ["bill"],
}

# Dimensions de cellule par défaut (la plupart sont 16×32)
# Les exceptions sont dans ce dict
SPECIAL_SIZES = {
    "biker": (32, 32),
    "little_boy": (16, 16),
    "little_girl": (16, 16),
}

DIRECTIONS_MAP = {
    # Pour un sprite 9-10 frames (standard) :
    # frames 0-2 = bas, 3-5 = haut, 6-8 = gauche, droite = gauche miroir
    9: {"bas": [0, 1, 2], "haut": [3, 4, 5], "gauche": [6, 7, 8], "droite": "mirror_gauche"},
    10: {"bas": [0, 1, 2], "haut": [3, 4, 5], "gauche": [6, 7, 8], "droite": "mirror_gauche"},
    # Pour un sprite 3 frames (comme mom) : que le bas
    3: {"bas": [0, 1, 2], "haut": [0, 1, 2], "gauche": [0, 1, 2], "droite": "mirror_gauche"},
    # Pour un sprite 1 frame (statique)
    1: {"bas": [0, 0, 0], "haut": [0, 0, 0], "gauche": [0, 0, 0], "droite": "mirror_gauche"},
}


def download_sprite(filename):
    """Télécharge un sprite PNG depuis le decomp."""
    url = f"{BASE_URL}/{filename}.png"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = urllib.request.urlopen(req).read()
        return Image.open(io.BytesIO(data))
    except Exception as e:
        print(f"  ERREUR téléchargement {filename}: {e}")
        return None


def extract_frames(img, cell_w, cell_h):
    """Extrait toutes les frames d'un sprite sheet horizontal."""
    # Convertir indexed → RGBA
    if img.mode == 'P':
        # L'index 0 du palette GBA = transparent
        img_rgba = img.convert("RGBA")
        # Rendre l'index 0 (vert/magenta de fond) transparent
        pixels = img_rgba.load()
        # Récupérer la couleur de l'index 0 dans la palette originale
        palette = img.getpalette()
        if palette:
            bg_r, bg_g, bg_b = palette[0], palette[1], palette[2]
            for y in range(img_rgba.height):
                for x in range(img_rgba.width):
                    r, g, b, a = pixels[x, y]
                    if r == bg_r and g == bg_g and b == bg_b:
                        pixels[x, y] = (0, 0, 0, 0)
    else:
        img_rgba = img.convert("RGBA")

    num_frames = img_rgba.width // cell_w
    frames = []
    for i in range(num_frames):
        frame = img_rgba.crop((i * cell_w, 0, (i + 1) * cell_w, cell_h))
        frames.append(frame)
    return frames


def pad_and_scale(frame, cell_w, cell_h):
    """Pad à 16×32 si nécessaire, puis scale 2× (NEAREST)."""
    target_native_w = 16
    target_native_h = 32

    if cell_h < target_native_h:
        # Pad en haut (le sprite est aligné en bas)
        padded = Image.new("RGBA", (target_native_w, target_native_h), (0, 0, 0, 0))
        padded.paste(frame, (0, target_native_h - cell_h))
        frame = padded
    elif cell_w > target_native_w:
        # Sprite plus large (biker 32×32): garder tel quel
        target_native_w = cell_w
        if cell_h < target_native_h:
            padded = Image.new("RGBA", (target_native_w, target_native_h), (0, 0, 0, 0))
            padded.paste(frame, (0, target_native_h - cell_h))
            frame = padded

    # Scale 2×
    final_w = frame.width * 2
    final_h = frame.height * 2
    return frame.resize((final_w, final_h), Image.NEAREST)


def save_sprite_set(frames, sprite_id, cell_w, cell_h, output_dir):
    """Sauvegarde un jeu complet de sprites pour un sprite_id."""
    num_frames = len(frames)

    # Trouver le mapping de directions approprié
    if num_frames >= 10:
        dir_map = DIRECTIONS_MAP[10]
    elif num_frames >= 9:
        dir_map = DIRECTIONS_MAP[9]
    elif num_frames >= 3:
        dir_map = DIRECTIONS_MAP[3]
    else:
        dir_map = DIRECTIONS_MAP[1]

    saved = 0
    for direction, frame_indices in dir_map.items():
        if frame_indices == "mirror_gauche":
            # Créer droite en miroir horizontal de gauche
            gauche_indices = dir_map["gauche"]
            for frame_idx, src_idx in enumerate(gauche_indices):
                if src_idx < len(frames):
                    frame = frames[src_idx]
                    frame = pad_and_scale(frame, cell_w, cell_h)
                    frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
                    fname = f"{sprite_id}_droite_{frame_idx}.png"
                    frame.save(os.path.join(output_dir, fname))
                    saved += 1
        else:
            for frame_idx, src_idx in enumerate(frame_indices):
                if src_idx < len(frames):
                    frame = frames[src_idx]
                    frame = pad_and_scale(frame, cell_w, cell_h)
                    fname = f"{sprite_id}_{direction}_{frame_idx}.png"
                    frame.save(os.path.join(output_dir, fname))
                    saved += 1

    return saved


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total_saved = 0
    total_sprites = 0
    errors = []

    for decomp_name, game_ids in sorted(SPRITE_MAP.items()):
        print(f"\n--- {decomp_name} → {game_ids}")
        img = download_sprite(decomp_name)
        if img is None:
            errors.append(decomp_name)
            continue

        cell_w, cell_h = SPECIAL_SIZES.get(decomp_name, (16, 32))
        print(f"  Taille: {img.size}, mode={img.mode}, cell={cell_w}×{cell_h}")

        frames = extract_frames(img, cell_w, cell_h)
        print(f"  Frames extraites: {len(frames)}")

        for sprite_id in game_ids:
            saved = save_sprite_set(frames, sprite_id, cell_w, cell_h, OUTPUT_DIR)
            total_saved += saved
            total_sprites += 1
            print(f"  → {sprite_id}: {saved} fichiers")

    print(f"\n{'='*60}")
    print(f"Total sprites générés: {total_sprites}")
    print(f"Total fichiers sauvegardés: {total_saved}")
    if errors:
        print(f"Erreurs ({len(errors)}): {errors}")


if __name__ == "__main__":
    main()
