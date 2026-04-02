#!/usr/bin/env python3
"""Audit complet du projet Pokémon Rouge/Bleu HD.
Vérifie : autoloads, sprites, maps JSON, warps, tiles, scènes, scripts."""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS = []
WARNINGS = []

def err(cat, msg):
    ERRORS.append(f"[{cat}] {msg}")

def warn(cat, msg):
    WARNINGS.append(f"[{cat}] {msg}")

# ─── 1. Autoloads ───
def audit_autoloads():
    print("=== 1. Vérification des autoloads ===")
    godot_file = ROOT / "project.godot"
    if not godot_file.exists():
        err("AUTOLOAD", "project.godot introuvable!")
        return
    
    in_autoload = False
    autoloads = {}
    for line in godot_file.read_text().splitlines():
        if line.strip() == "[autoload]":
            in_autoload = True
            continue
        if in_autoload and line.startswith("["):
            break
        if in_autoload and "=" in line:
            name, path = line.split("=", 1)
            path = path.strip().strip('"').lstrip("*")
            autoloads[name.strip()] = path
    
    for name, res_path in autoloads.items():
        real_path = ROOT / res_path.replace("res://", "")
        if not real_path.exists():
            err("AUTOLOAD", f"{name} → {res_path} — FICHIER MANQUANT!")
        else:
            print(f"  ✓ {name} → {res_path}")

# ─── 2. Map JSON integrity ───
def audit_maps():
    print("\n=== 2. Vérification des maps JSON ===")
    maps_dir = ROOT / "data" / "maps"
    if not maps_dir.exists():
        err("MAPS", "data/maps/ introuvable!")
        return
    
    map_ids = set()
    all_map_data = {}
    
    for f in sorted(maps_dir.glob("*.json")):
        map_id = f.stem
        map_ids.add(map_id)
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            all_map_data[map_id] = data
        except json.JSONDecodeError as e:
            err("JSON", f"{f.name} — JSON invalide: {e}")
    
    print(f"  {len(map_ids)} fichiers JSON trouvés")
    
    # Check each map's content
    sprite_dir = ROOT / "assets" / "sprites" / "characters"
    all_sprites = set()
    if sprite_dir.exists():
        for sf in sprite_dir.iterdir():
            if sf.suffix == ".png" and not sf.name.endswith(".import"):
                all_sprites.add(sf.name)
    
    missing_sprites = set()
    missing_warps = set()
    tile_errors = 0
    
    for map_id, data in sorted(all_map_data.items()):
        # Check required keys
        if "largeur" not in data:
            warn("MAP", f"{map_id}.json — clé 'largeur' manquante")
        if "hauteur" not in data:
            warn("MAP", f"{map_id}.json — clé 'hauteur' manquante")
        
        largeur = data.get("largeur", 20)
        hauteur = data.get("hauteur", 18)
        
        # Check tiles_sol dimensions
        tiles_sol = data.get("tiles_sol", [])
        if tiles_sol:
            if len(tiles_sol) != hauteur:
                err("TILES", f"{map_id}.json — tiles_sol: {len(tiles_sol)} lignes ≠ hauteur {hauteur}")
            for i, row in enumerate(tiles_sol):
                if len(row) != largeur:
                    err("TILES", f"{map_id}.json — tiles_sol[{i}]: {len(row)} cols ≠ largeur {largeur}")
                for j, tile_idx in enumerate(row):
                    if tile_idx < -1 or tile_idx > 47:
                        tile_errors += 1
                        if tile_errors <= 10:
                            err("TILES", f"{map_id}.json — tiles_sol[{i}][{j}] = {tile_idx} (hors plage 0-47)")
        else:
            warn("MAP", f"{map_id}.json — tiles_sol manquant ou vide")
        
        # Check tiles_objets dimensions
        tiles_objets = data.get("tiles_objets", [])
        if tiles_objets:
            if len(tiles_objets) != hauteur:
                err("TILES", f"{map_id}.json — tiles_objets: {len(tiles_objets)} lignes ≠ hauteur {hauteur}")
            for i, row in enumerate(tiles_objets):
                if len(row) != largeur:
                    err("TILES", f"{map_id}.json — tiles_objets[{i}]: {len(row)} cols ≠ largeur {largeur}")
                for j, tile_idx in enumerate(row):
                    if tile_idx < -1 or tile_idx > 47:
                        tile_errors += 1
                        if tile_errors <= 10:
                            err("TILES", f"{map_id}.json — tiles_objets[{i}][{j}] = {tile_idx} (hors plage 0-47)")
        
        # Check NPC sprites
        pnjs = data.get("pnj", [])
        for pnj in pnjs:
            sprite_id = pnj.get("sprite", "pnj_homme")
            # Check that at least bas_0 exists
            test_file = f"{sprite_id}_bas_0.png"
            if test_file not in all_sprites:
                if sprite_id not in missing_sprites:
                    missing_sprites.add(sprite_id)
                    err("SPRITE", f"{map_id}.json — PNJ '{pnj.get('id', '?')}' sprite '{sprite_id}' → {test_file} MANQUANT")
        
        # Check warps
        warps = data.get("warps", [])
        for warp in warps:
            target_map = warp.get("vers_map", "")
            target_warp = warp.get("vers_warp", "")
            if target_map and target_map not in map_ids:
                key = f"{target_map}"
                if key not in missing_warps:
                    missing_warps.add(key)
                    err("WARP", f"{map_id}.json — warp '{warp.get('id', '?')}' → vers_map '{target_map}' INEXISTANT")
            
            # Check warp has required keys
            if "x" not in warp or "y" not in warp:
                err("WARP", f"{map_id}.json — warp '{warp.get('id', '?')}' manque x/y")
        
        # Check connexions
        connexions = data.get("connexions", [])
        for conn in connexions:
            target = conn.get("vers", "")
            if target and target not in map_ids:
                err("CONNEXION", f"{map_id}.json — connexion vers '{target}' INEXISTANT")
    
    if tile_errors > 10:
        err("TILES", f"... et {tile_errors - 10} autres erreurs de tiles")
    
    print(f"  Sprites PNJ manquants: {len(missing_sprites)}")
    print(f"  Warps cassés: {len(missing_warps)}")
    print(f"  Erreurs de tiles: {tile_errors}")
    
    return all_map_data, map_ids

# ─── 3. Scene files check ───
def audit_scenes(map_ids):
    print("\n=== 3. Vérification des scènes .tscn ===")
    maps_scene_dir = ROOT / "scenes" / "maps"
    if not maps_scene_dir.exists():
        err("SCENES", "scenes/maps/ introuvable!")
        return
    
    scene_files = set()
    for f in maps_scene_dir.glob("*.tscn"):
        scene_files.add(f.stem)
    
    print(f"  {len(scene_files)} fichiers .tscn dans scenes/maps/")
    
    # Check for maps without scenes
    maps_without_scenes = map_ids - scene_files
    scenes_without_maps = scene_files - map_ids
    
    if maps_without_scenes:
        print(f"  Maps JSON sans scène .tscn ({len(maps_without_scenes)}):")
        for m in sorted(maps_without_scenes):
            err("SCENE", f"  data/maps/{m}.json existe mais scenes/maps/{m}.tscn MANQUANT")
    
    if scenes_without_maps:
        print(f"  Scènes .tscn sans JSON ({len(scenes_without_maps)}):")
        for s in sorted(scenes_without_maps):
            warn("SCENE", f"  scenes/maps/{s}.tscn existe mais pas de data/maps/{s}.json")

# ─── 4. Scene references in code ───
def audit_scene_refs():
    print("\n=== 4. Vérification des références de scènes dans le code ===")
    scene_patterns = re.compile(r'(?:load|preload|change_scene_to_file|charger_scene)\s*\(\s*["\']([^"\']+\.tscn)["\']')
    
    missing_refs = set()
    for gd_file in sorted(ROOT.rglob("*.gd")):
        if ".godot" in str(gd_file) or "tools" in str(gd_file):
            continue
        content = gd_file.read_text(encoding="utf-8", errors="replace")
        for match in scene_patterns.finditer(content):
            ref = match.group(1)
            if ref.startswith("res://"):
                # Ignorer les format strings (%s, {0}, etc.)
                if "%" in ref or "{" in ref:
                    continue
                real = ROOT / ref.replace("res://", "")
                if not real.exists():
                    if ref not in missing_refs:
                        missing_refs.add(ref)
                        rel = gd_file.relative_to(ROOT)
                        err("REF", f"{rel} — référence '{ref}' FICHIER MANQUANT")
    
    # Also check .tscn files for resource references
    for tscn_file in sorted(ROOT.rglob("*.tscn")):
        if ".godot" in str(tscn_file):
            continue
        content = tscn_file.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r'path="(res://[^"]+)"', content):
            ref = match.group(1)
            real = ROOT / ref.replace("res://", "")
            if not real.exists():
                if ref not in missing_refs:
                    missing_refs.add(ref)
                    rel = tscn_file.relative_to(ROOT)
                    err("REF", f"{rel} — référence '{ref}' FICHIER MANQUANT")
    
    print(f"  Références manquantes trouvées: {len(missing_refs)}")

# ─── 5. Pokémon sprites ───
def audit_pokemon_sprites():
    print("\n=== 5. Vérification des sprites Pokémon ===")
    front_dir = ROOT / "assets" / "sprites" / "pokemon" / "front"
    back_dir = ROOT / "assets" / "sprites" / "pokemon" / "back"
    
    fronts = set()
    backs = set()
    
    if front_dir.exists():
        for f in front_dir.iterdir():
            if f.suffix == ".png" and not f.name.endswith(".import"):
                fronts.add(f.stem)
    
    if back_dir.exists():
        for f in back_dir.iterdir():
            if f.suffix == ".png" and not f.name.endswith(".import"):
                backs.add(f.stem)
    
    print(f"  Front sprites: {len(fronts)}")
    print(f"  Back sprites: {len(backs)}")
    
    # Check species.json references
    species_file = ROOT / "data" / "pokemon" / "species.json"
    if species_file.exists():
        species = json.loads(species_file.read_text(encoding="utf-8"))
        for pokeid, data in species.items():
            # Check if front/back sprites exist for this ID
            if pokeid not in fronts and f"{int(pokeid)}" not in fronts:
                warn("PKM_SPRITE", f"Pokémon #{pokeid} ({data.get('nom', '?')}) — front sprite manquant")
            if pokeid not in backs and f"{int(pokeid)}" not in backs:
                warn("PKM_SPRITE", f"Pokémon #{pokeid} ({data.get('nom', '?')}) — back sprite manquant")

# ─── 6. Trainer sprites ───
def audit_trainer_sprites():
    print("\n=== 6. Vérification des sprites de dresseurs ===")
    trainer_dir = ROOT / "assets" / "sprites" / "trainers"
    
    trainer_sprites = set()
    if trainer_dir.exists():
        for f in trainer_dir.iterdir():
            if f.suffix == ".png" and not f.name.endswith(".import"):
                trainer_sprites.add(f.stem)
    
    print(f"  Trainer sprites: {len(trainer_sprites)}")
    
    # Check trainer_sprites.json mapping
    ts_file = ROOT / "data" / "trainer_sprites.json"
    if ts_file.exists():
        ts_data = json.loads(ts_file.read_text(encoding="utf-8"))
        for key, sprite_file in ts_data.items():
            if isinstance(sprite_file, str):
                # Remove res:// and path prefix to check
                fname = sprite_file.replace("res://assets/sprites/trainers/", "")
                fname_stem = fname.replace(".png", "")
                if fname_stem not in trainer_sprites:
                    err("TRAINER", f"trainer_sprites.json['{key}'] → '{sprite_file}' MANQUANT")

# ─── 7. Data files integrity ───
def audit_data_files():
    print("\n=== 7. Vérification des fichiers de données ===")
    data_files = [
        "data/pokemon/species.json",
        "data/pokemon/moves.json",
        "data/items.json",
        "data/type_chart.json",
        "data/encounter_tables.json",
        "data/trainers.json",
        "data/trainer_sprites.json",
        "data/quetes.json",
    ]
    
    for rel_path in data_files:
        full_path = ROOT / rel_path
        if not full_path.exists():
            err("DATA", f"{rel_path} — FICHIER MANQUANT!")
            continue
        try:
            data = json.loads(full_path.read_text(encoding="utf-8"))
            size = len(data) if isinstance(data, (dict, list)) else "N/A"
            print(f"  ✓ {rel_path} — {size} entrées")
        except json.JSONDecodeError as e:
            err("DATA", f"{rel_path} — JSON invalide: {e}")
    
    # Cross-validate encounters with species
    species_file = ROOT / "data" / "pokemon" / "species.json"
    encounters_file = ROOT / "data" / "encounter_tables.json"
    if species_file.exists() and encounters_file.exists():
        species = json.loads(species_file.read_text(encoding="utf-8"))
        encounters = json.loads(encounters_file.read_text(encoding="utf-8"))
        species_ids = set(species.keys())
        
        for zone, enc_data in encounters.items():
            if isinstance(enc_data, dict):
                for enc_type, entries in enc_data.items():
                    if isinstance(entries, list):
                        for entry in entries:
                            if isinstance(entry, dict):
                                pid = str(entry.get("pokemon_id", entry.get("id", "")))
                                if pid and pid not in species_ids:
                                    err("ENCOUNTER", f"encounter_tables['{zone}']['{enc_type}'] — pokemon_id '{pid}' pas dans species.json")
    
    # Cross-validate moves referenced in species learnsets
    moves_file = ROOT / "data" / "pokemon" / "moves.json"
    if species_file.exists() and moves_file.exists():
        species = json.loads(species_file.read_text(encoding="utf-8"))
        moves = json.loads(moves_file.read_text(encoding="utf-8"))
        move_ids = set(moves.keys())
        
        missing_moves = set()
        for pokeid, data in species.items():
            learnset = data.get("learnset", {})
            if isinstance(learnset, dict):
                for level, move_list in learnset.items():
                    if isinstance(move_list, list):
                        for move_id in move_list:
                            if move_id not in move_ids and move_id not in missing_moves:
                                missing_moves.add(move_id)
                                err("LEARNSET", f"Pokémon #{pokeid} — attaque '{move_id}' pas dans moves.json")
    
    # Cross-validate trainers
    trainers_file = ROOT / "data" / "trainers.json"
    if trainers_file.exists() and species_file.exists():
        species = json.loads(species_file.read_text(encoding="utf-8"))
        trainers = json.loads(trainers_file.read_text(encoding="utf-8"))
        species_ids = set(species.keys())
        
        if isinstance(trainers, dict):
            for tid, tdata in trainers.items():
                team = tdata.get("equipe", [])
                if isinstance(team, list):
                    for poke in team:
                        if isinstance(poke, dict):
                            pid = str(poke.get("espece_id", ""))
                            if pid and pid not in species_ids:
                                err("TRAINER", f"trainers['{tid}'] — espece_id '{pid}' pas dans species.json")

# ─── 8. Tileset validation ───
def audit_tileset():
    print("\n=== 8. Vérification du tileset ===")
    tileset_path = ROOT / "assets" / "sprites" / "tilesets" / "tileset_outdoor.png"
    if not tileset_path.exists():
        err("TILESET", "tileset_outdoor.png MANQUANT!")
        return
    
    # Check dimensions with PIL if available
    try:
        from PIL import Image
        img = Image.open(tileset_path)
        w, h = img.size
        cols = w // 32
        rows = h // 32
        total = cols * rows
        print(f"  Tileset: {w}×{h}px = {cols}×{rows} tiles = {total} total")
        
        # TileSetBuilder expects 8 columns and uses indices 0-47 (6 rows)
        if cols != 8:
            err("TILESET", f"Tileset a {cols} colonnes, TileSetBuilder attend 8!")
        if total < 48:
            err("TILESET", f"Tileset a {total} tiles, TileSetBuilder utilise indices 0-47 (48 requis)!")
        elif total < 48:
            warn("TILESET", f"Tileset a seulement {total} tiles, indices 0-47 utilisés")
        else:
            print(f"  ✓ Tileset suffisant ({total} >= 48 tiles requis)")
    except ImportError:
        # Check file size as proxy
        size = tileset_path.stat().st_size
        print(f"  Tileset présent ({size} bytes) — PIL non disponible pour vérifier dimensions")

# ─── 9. Player sprite frames ───
def audit_player_frames():
    print("\n=== 9. Vérification des sprites joueur ===")
    # player_frames.tres references red_normal_{dir}_{frame}.png
    tres_path = ROOT / "assets" / "sprites" / "characters" / "player_frames.tres"
    if not tres_path.exists():
        err("PLAYER", "player_frames.tres MANQUANT!")
        return
    
    content = tres_path.read_text(encoding="utf-8")
    sprite_refs = re.findall(r'path="(res://[^"]+\.png)"', content)
    
    for ref in sprite_refs:
        real = ROOT / ref.replace("res://", "")
        if not real.exists():
            err("PLAYER", f"player_frames.tres — '{ref}' MANQUANT!")
        else:
            print(f"  ✓ {ref}")

# ─── 10. Check .tscn files for script references ───
def audit_tscn_scripts():
    print("\n=== 10. Vérification des scripts dans les .tscn ===")
    missing = set()
    for tscn_file in sorted(ROOT.rglob("*.tscn")):
        if ".godot" in str(tscn_file):
            continue
        content = tscn_file.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r'script\s*=\s*ExtResource\("([^"]+)"\)', content):
            # The ext resource ID is referenced, we need to find the path
            pass
        # Check ext_resource lines
        for match in re.finditer(r'\[ext_resource\s+[^]]*path="(res://[^"]+)"[^]]*\]', content):
            ref = match.group(1)
            real = ROOT / ref.replace("res://", "")
            if not real.exists() and ref not in missing:
                missing.add(ref)
                rel = tscn_file.relative_to(ROOT)
                err("TSCN_REF", f"{rel} — ext_resource '{ref}' MANQUANT")
    
    print(f"  Références manquantes: {len(missing)}")

# ─── 11. Check warp cross-references (bidirectional) ───
def audit_warp_bidirectional(all_map_data):
    print("\n=== 11. Vérification des warps bidirectionnels ===")
    broken_pairs = 0
    
    for map_id, data in all_map_data.items():
        warps = data.get("warps", [])
        for warp in warps:
            target_map = warp.get("vers_map", "")
            target_warp = warp.get("vers_warp", "")
            warp_id = warp.get("id", "")
            
            if not target_map or not target_warp:
                continue
            
            if target_map not in all_map_data:
                continue  # Already reported as missing
            
            # Check if target map has a warp back
            target_data = all_map_data[target_map]
            target_warps = target_data.get("warps", [])
            found = False
            for tw in target_warps:
                if tw.get("id") == target_warp or tw.get("vers_warp") == warp_id:
                    found = True
                    break
            
            if not found:
                broken_pairs += 1
                if broken_pairs <= 20:
                    warn("WARP_BI", f"{map_id} warp '{warp_id}' → {target_map}:'{target_warp}' — warp retour introuvable")
    
    print(f"  Warps sans retour: {broken_pairs}")
    if broken_pairs > 20:
        print(f"  (affichage limité à 20)")

# ─── 12. Check for code-referenced scene patterns ───
def audit_dynamic_scene_refs():
    print("\n=== 12. Vérification des références dynamiques ===")
    # Look for patterns like: "res://scenes/maps/%s.tscn" % some_var
    maps_scene_dir = ROOT / "scenes" / "maps"
    existing_scenes = set()
    if maps_scene_dir.exists():
        for f in maps_scene_dir.glob("*.tscn"):
            existing_scenes.add(f.stem)
    
    # Check charger_scene calls in map JSON warps → do target scenes exist?
    maps_dir = ROOT / "data" / "maps"
    if maps_dir.exists():
        for f in sorted(maps_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except:
                continue
            
            warps = data.get("warps", [])
            for warp in warps:
                target_map = warp.get("vers_map", "")
                if target_map and target_map not in existing_scenes:
                    err("DYN_SCENE", f"{f.stem} warp → '{target_map}' n'a pas de scène .tscn correspondante")

# ─── 13. Check .import files ───
def audit_import_files():
    print("\n=== 13. Vérification des fichiers .import ===")
    missing_imports = 0
    dirs_to_check = [
        ROOT / "assets" / "sprites" / "characters",
        ROOT / "assets" / "sprites" / "pokemon" / "front",
        ROOT / "assets" / "sprites" / "pokemon" / "back",
        ROOT / "assets" / "sprites" / "tilesets",
        ROOT / "assets" / "sprites" / "trainers",
        ROOT / "assets" / "sprites" / "ui",
    ]
    
    for dir_path in dirs_to_check:
        if not dir_path.exists():
            warn("IMPORT", f"{dir_path.relative_to(ROOT)} — dossier inexistant")
            continue
        
        dir_missing = 0
        for f in dir_path.iterdir():
            if f.suffix == ".png" and not f.name.endswith(".import"):
                import_file = f.with_suffix(f.suffix + ".import")
                if not import_file.exists():
                    dir_missing += 1
                    missing_imports += 1
        
        if dir_missing > 0:
            err("IMPORT", f"{dir_path.relative_to(ROOT)} — {dir_missing} fichiers .import manquants")
    
    print(f"  Fichiers .import manquants total: {missing_imports}")

# ─── MAIN ───
def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║  AUDIT COMPLET — Pokémon Rouge/Bleu HD          ║")
    print(f"║  Racine: {str(ROOT)[:40]:<40} ║")
    print("╚══════════════════════════════════════════════════╝\n")
    
    audit_autoloads()
    result = audit_maps()
    all_map_data = result[0] if result else ({}, set())
    map_ids = result[1] if result else set()
    audit_scenes(map_ids)
    audit_scene_refs()
    audit_pokemon_sprites()
    audit_trainer_sprites()
    audit_data_files()
    audit_tileset()
    audit_player_frames()
    audit_tscn_scripts()
    audit_warp_bidirectional(all_map_data)
    audit_dynamic_scene_refs()
    audit_import_files()
    
    print("\n" + "=" * 60)
    print(f"RÉSUMÉ: {len(ERRORS)} ERREURS, {len(WARNINGS)} AVERTISSEMENTS")
    print("=" * 60)
    
    if ERRORS:
        print("\n── ERREURS ──")
        for e in ERRORS:
            print(f"  ❌ {e}")
    
    if WARNINGS:
        print(f"\n── AVERTISSEMENTS ({len(WARNINGS)}) ──")
        for w in WARNINGS[:50]:
            print(f"  ⚠️  {w}")
        if len(WARNINGS) > 50:
            print(f"  ... et {len(WARNINGS) - 50} autres avertissements")
    
    if not ERRORS:
        print("\n🎉 Aucune erreur critique trouvée!")
    
    return len(ERRORS)

if __name__ == "__main__":
    sys.exit(main())
