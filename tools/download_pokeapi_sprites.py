#!/usr/bin/env python3
"""
Télécharge les sprites Pokémon Gen V (Black/White) depuis PokeAPI.
Front (96×96) et Back (96×96) pour les 151 premiers Pokémon.
Sauvegarde en PNG RGBA avec transparence, nommés 001.png à 151.png.
"""

import os
import sys
import urllib.request
import time
from PIL import Image
import io

BASE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"
# Gen V Black/White - meilleur pixel art
FRONT_URL = BASE_URL + "/versions/generation-v/black-white/{id}.png"
BACK_URL = BASE_URL + "/versions/generation-v/black-white/back/{id}.png"
# Fallback: sprites par défaut (si Gen V échoue)
FRONT_FALLBACK = BASE_URL + "/{id}.png"
BACK_FALLBACK = BASE_URL + "/back/{id}.png"

FRONT_DIR = "assets/sprites/pokemon/front"
BACK_DIR = "assets/sprites/pokemon/back"
TOTAL = 151

def download_sprite(url: str, timeout: int = 15) -> bytes | None:
    """Télécharge un sprite depuis une URL."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read()
    except Exception:
        return None

def save_sprite(data: bytes, path: str, target_size: tuple = None) -> bool:
    """Sauvegarde un sprite PNG. Convertit en RGBA si nécessaire."""
    try:
        img = Image.open(io.BytesIO(data))
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        if target_size and img.size != target_size:
            img = img.resize(target_size, Image.NEAREST)
        img.save(path, "PNG")
        return True
    except Exception as e:
        print(f"  Erreur sauvegarde {path}: {e}")
        return False

def main():
    os.makedirs(FRONT_DIR, exist_ok=True)
    os.makedirs(BACK_DIR, exist_ok=True)
    
    success_front = 0
    success_back = 0
    errors = []
    
    for i in range(1, TOTAL + 1):
        name = f"{i:03d}.png"
        front_path = os.path.join(FRONT_DIR, name)
        back_path = os.path.join(BACK_DIR, name)
        
        # Front sprite
        data = download_sprite(FRONT_URL.format(id=i))
        if data is None:
            data = download_sprite(FRONT_FALLBACK.format(id=i))
        if data and save_sprite(data, front_path):
            success_front += 1
        else:
            errors.append(f"front/{name}")
            print(f"  ERREUR front {name}")
        
        # Back sprite
        data = download_sprite(BACK_URL.format(id=i))
        if data is None:
            data = download_sprite(BACK_FALLBACK.format(id=i))
        if data and save_sprite(data, back_path):
            success_back += 1
        else:
            errors.append(f"back/{name}")
            print(f"  ERREUR back {name}")
        
        # Progress
        if i % 10 == 0:
            print(f"  {i}/{TOTAL}...")
        
        # Petit délai pour ne pas surcharger le serveur
        time.sleep(0.05)
    
    print(f"\nRésultat:")
    print(f"  Front: {success_front}/{TOTAL}")
    print(f"  Back:  {success_back}/{TOTAL}")
    if errors:
        print(f"  Erreurs ({len(errors)}): {', '.join(errors[:10])}")
    
    # Vérifier les dimensions
    sample = os.path.join(FRONT_DIR, "001.png")
    if os.path.exists(sample):
        img = Image.open(sample)
        print(f"  Taille des sprites: {img.size}")

if __name__ == "__main__":
    main()
