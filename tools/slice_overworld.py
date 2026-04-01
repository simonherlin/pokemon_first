#!/usr/bin/env python3
"""Découpe les spritesheets overworld (pret/pokefirered) en frames individuelles.
Chaque spritesheet est découpé en frames de 16×32, mis à l'échelle ×2 (32×64),
et sauvegardé avec le nommage attendu par le système NPC : {nom}_{dir}_{frame}.png

Layout des spritesheets FRLG :
- 9 frames (144×32) : bas_0, bas_1, bas_2, haut_0, haut_1, haut_2, gauche_0, gauche_1, gauche_2
- 10 frames (160×32) : pareil + 1 frame extra
- 3 frames (48×32) : bas_0, haut_0 (ou gauche_0), droite_0 (ou flip gauche)
- 4 frames (64×32) : bas_0, haut_0, gauche_0, droite_0

Mapping sprite_id (JSON cartes) → nom du fichier pret :
"""

from PIL import Image
import os
import json

CHARS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sprites", "characters")
FRAME_W = 16
FRAME_H = 32
SCALE = 2

# Mapping des sprite_ids utilisés dans les maps vers les noms de fichiers pret
# Format : sprite_id → pret_filename (sans .png)
SPRITE_MAP = {
    # PNJ génériques
    "pnj_garcon": "boy",
    "pnj_gamin": "youngster",
    "pnj_fille": "lass",
    "pnj_gamine": "lass",
    "pnj_marin": "sailor",
    "pnj_rocket": "rocket_m",
    "rocket_m": "rocket_m",
    "pnj_scientifique": "scientist",
    "pnj_motard": "biker",
    "pnj_medium": "channeler",
    "pnj_karateka": "boy",  # Pas de spritesheet karateka overworld
    "pnj_pecheur": "fisher",
    "pnj_randonneur": "hiker",
    "pnj_vieux": "old_woman",
    "pnj_infirmiere": "nurse",
    "pnj_vendeur": "clerk",
    "pnj_pc": "clerk",
    "pnj_garde": "gentleman",
    "pnj_jongleur": "gentleman",
    "pnj_nageur": "sailor",
    "pnj_nageuse": "beauty",
    # Champions / personnages spéciaux
    "pnj_chen": "prof_oak",
    "pnj_rival": "green_normal",
    "pnj_giovanni": "giovanni",
    "pnj_champion": "brock",
    "pnj_champion_bob": "brock",
    "pnj_champion_ondine": "misty",
    "champion_erika": "erika",
    "pnj_capitaine": "sailor",
    # Dresseurs génériques
    "dresseur": "boy",
    "dresseur_m": "boy",
    "dresseur_f": "beauty",
    "dresseur_randonneur": "hiker",
    "pnj_dresseur": "boy",
}

# Noms des directions selon le nombre de frames
DIR_MAP_9 = {
    0: "bas_0",    1: "bas_1",    2: "bas_2",
    3: "haut_0",   4: "haut_1",   5: "haut_2",
    6: "gauche_0", 7: "gauche_1", 8: "gauche_2",
}

DIR_MAP_3 = {
    0: "bas_0",
    1: "gauche_0",
    2: "haut_0",
}

DIR_MAP_4 = {
    0: "bas_0",
    1: "haut_0",
    2: "gauche_0",
    3: "droite_0",
}


def slice_spritesheet(filepath: str) -> dict:
    """Découpe un spritesheet en frames individuelles. Retourne {frame_name: Image}."""
    img = Image.open(filepath)
    w, h = img.size
    
    if h != FRAME_H:
        return {}
    
    num_frames = w // FRAME_W
    frames = {}
    
    if num_frames >= 9:
        # 9+ frames : layout standard FRLG
        for i in range(min(num_frames, 9)):
            frame = img.crop((i * FRAME_W, 0, (i + 1) * FRAME_W, FRAME_H))
            frames[DIR_MAP_9[i]] = frame
        # Générer droite par miroir horizontal de gauche
        if "gauche_0" in frames:
            frames["droite_0"] = frames["gauche_0"].transpose(Image.FLIP_LEFT_RIGHT)
        if "gauche_1" in frames:
            frames["droite_1"] = frames["gauche_1"].transpose(Image.FLIP_LEFT_RIGHT)
        if "gauche_2" in frames:
            frames["droite_2"] = frames["gauche_2"].transpose(Image.FLIP_LEFT_RIGHT)
    elif num_frames == 4:
        for i in range(4):
            frame = img.crop((i * FRAME_W, 0, (i + 1) * FRAME_W, FRAME_H))
            frames[DIR_MAP_4[i]] = frame
    elif num_frames == 3:
        for i in range(3):
            frame = img.crop((i * FRAME_W, 0, (i + 1) * FRAME_W, FRAME_H))
            frames[DIR_MAP_3[i]] = frame
        # Miroir de gauche pour droite
        if "gauche_0" in frames:
            frames["droite_0"] = frames["gauche_0"].transpose(Image.FLIP_LEFT_RIGHT)
    elif num_frames == 1:
        frame = img.crop((0, 0, FRAME_W, FRAME_H))
        frames["bas_0"] = frame
    
    return frames


def process_all_spritesheets():
    """Traite tous les spritesheets pret et crée les frames individuelles."""
    # Lister les fichiers pret (ceux qui sont des spritesheets 16×32)
    pret_files = set()
    for name in os.listdir(CHARS_DIR):
        if not name.endswith(".png"):
            continue
        filepath = os.path.join(CHARS_DIR, name)
        try:
            img = Image.open(filepath)
            w, h = img.size
            if h == FRAME_H and w > FRAME_W:
                pret_files.add(name.replace(".png", ""))
        except:
            continue
    
    print(f"Spritesheets pret trouvés : {len(pret_files)}")
    
    # Traiter chaque spritesheet pret
    created = 0
    for base_name in sorted(pret_files):
        filepath = os.path.join(CHARS_DIR, f"{base_name}.png")
        frames = slice_spritesheet(filepath)
        if not frames:
            print(f"  ⚠ {base_name}: aucune frame extraite")
            continue
        
        for frame_name, frame_img in frames.items():
            # Upscale ×2
            new_w = frame_img.width * SCALE
            new_h = frame_img.height * SCALE
            frame_scaled = frame_img.resize((new_w, new_h), Image.NEAREST)
            
            # Convertir en RGBA
            if frame_scaled.mode != "RGBA":
                frame_scaled = frame_scaled.convert("RGBA")
            
            out_name = f"{base_name}_{frame_name}.png"
            out_path = os.path.join(CHARS_DIR, out_name)
            frame_scaled.save(out_path)
            created += 1
        
        print(f"  ✓ {base_name}: {len(frames)} frames extraites")
    
    # Maintenant créer les alias pour les sprite_ids des maps
    print(f"\nCréation des alias sprite_id → pret...")
    aliases_created = 0
    for sprite_id, pret_name in SPRITE_MAP.items():
        # Vérifier si le pret_name a des frames
        sample = os.path.join(CHARS_DIR, f"{pret_name}_bas_0.png")
        if not os.path.exists(sample):
            print(f"  ⚠ {sprite_id} → {pret_name}: pas de frames disponibles")
            continue
        
        # Vérifier si l'alias existe déjà (déjà un fichier custom)
        alias_check = os.path.join(CHARS_DIR, f"{sprite_id}_bas_0.png")
        if os.path.exists(alias_check):
            # Ne pas écraser les sprites custom existants
            continue
        
        # Copier les frames avec le nom alias
        for frame_file in os.listdir(CHARS_DIR):
            if frame_file.startswith(f"{pret_name}_") and frame_file.endswith(".png"):
                suffix = frame_file[len(pret_name):]  # ex: _bas_0.png
                alias_name = f"{sprite_id}{suffix}"
                src = os.path.join(CHARS_DIR, frame_file)
                dst = os.path.join(CHARS_DIR, alias_name)
                if not os.path.exists(dst):
                    img = Image.open(src)
                    img.save(dst)
                    aliases_created += 1
        
    print(f"\nTerminé: {created} frames extraites, {aliases_created} alias créés")


if __name__ == "__main__":
    process_all_spritesheets()
