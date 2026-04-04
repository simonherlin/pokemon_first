#!/usr/bin/env python3
"""
Correction de TOUS les sprites PNJ dans les cartes du jeu.
Basé sur les données authentiques du decomp pokefirered (pret/pokefirered).
"""

import json
import os
import glob

MAPS_DIR = "data/maps"

# ============================================================
# CORRECTIONS DE SPRITES PAR CARTE
# Basé sur les object_events du decomp pokefirered
# ============================================================

# Format: { "map_name": { "npc_id": {"sprite": "new_sprite", ...other_fixes} } }
# On peut aussi ajouter/supprimer des PNJs

SPRITE_CORRECTIONS = {
    # === BOURG PALETTE ===
    # Decomp: WOMAN_1 (wander), FAT_MAN (wander), PROF_OAK
    "bourg_palette": {
        "pnj_homme_01": {"sprite": "pnj_femme", "notes": "C'est une femme dans l'original (WOMAN_1)"},
        "pnj_femme_01": {"sprite": "pnj_gros", "notes": "C'est le gros homme (FAT_MAN) dans l'original"},
    },

    # === MAISON DU JOUEUR ===
    # Decomp: MOM
    "maison_joueur": {
        "maman": {"sprite": "maman", "notes": "Sprite dédié de la mère (MOM)"},
    },

    # === MAISON DU RIVAL ===
    # Decomp: DAISY
    "maison_rival": {
        "soeur_rival": {"sprite": "soeur_rival", "notes": "Sprite Daisy (sœur du rival)"},
    },

    # === ROUTE 1 ===
    # Decomp: CLERK (vendeur), BOY
    "route_1": {
        "pnj_vendeur": {"sprite": "pnj_vendeur", "notes": "Correct: CLERK"},
    },

    # === JADIELLE VILLE ===
    # Decomp: FAT_MAN, OLD_MAN_1, WOMAN_3, YOUNGSTER, BOY
    "jadielle_ville": {
        "pnj_vieux_01": {"sprite": "pnj_vieux", "notes": "Correct: OLD_MAN_1"},
        "pnj_femme_02": {"sprite": "pnj_femme3", "notes": "WOMAN_3 dans l'original"},
        "pnj_homme_02": {"sprite": "pnj_garcon", "notes": "C'est un BOY dans l'original"},
    },

    # === ARGENTA VILLE ===
    # Decomp: LASS, MAN, FAT_MAN, BUG_CATCHER, BOY, SCIENTIST
    "argenta_ville": {
        "pnj_homme_01": {"sprite": "pnj_gamine", "notes": "LASS dans l'original"},
        "pnj_femme_02": {"sprite": "pnj_homme", "notes": "MAN dans l'original"},
        "pnj_homme_03": {"sprite": "pnj_gros", "notes": "FAT_MAN dans l'original"},
    },

    # === ROUTE 2 ===
    "route_2": {
        "gamin_route2_01": {"sprite": "pnj_gamin", "notes": "Correct"},
    },

    # === AZURIA VILLE ===
    # Decomp: POLICEMAN, ROCKET_M, LITTLE_BOY, BALDING_MAN, LASS, YOUNGSTER, WOMAN_1, COOLTRAINER_M
    "azuria_ville": {
        "pnj_azuria_01": {"sprite": "pnj_garde", "notes": "POLICEMAN dans l'original"},
        "pnj_azuria_02": {"sprite": "pnj_chauve", "notes": "BALDING_MAN dans l'original"},
        "pnj_azuria_03": {"sprite": "pnj_gamin", "notes": "YOUNGSTER dans l'original"},
        "pnj_azuria_04": {"sprite": "pnj_femme", "notes": "WOMAN_1 dans l'original"},
    },

    # === ROUTE 5 ===
    "route_5": {
        "pnj_route5_01": {"sprite": "pnj_femme", "notes": "Correct"},
    },

    # === ROUTE 6 ===
    "route_6": {
        "pnj_route6_01": {"sprite": "pnj_homme", "notes": "Correct"},
    },

    # === CARMIN SUR MER ===
    # Decomp: WOMAN_1, OLD_MAN_1, OLD_MAN_2, SAILOR×2, SCIENTIST
    "carmin_sur_mer": {
        "pnj_carmin_01": {"sprite": "pnj_femme", "notes": "WOMAN_1 dans l'original"},
        "pnj_carmin_02": {"sprite": "pnj_vieux", "notes": "OLD_MAN_1 dans l'original"},
        "pnj_carmin_03": {"sprite": "pnj_marin", "notes": "Correct: SAILOR"},
        "pnj_carmin_04": {"sprite": "pnj_vieux2", "notes": "OLD_MAN_2 dans l'original"},
        "pnj_ferry_sevii": {"sprite": "pnj_marin", "notes": "Correct: SAILOR"},
    },

    # === CELADOPOLE ===
    # Decomp: ROCKET_M×3, FAT_MAN, LITTLE_GIRL, WOMAN_2, OLD_MAN_1×2, OLD_MAN_2, BOY, SCIENTIST
    "celadopole": {
        "pnj_celadopole_01": {"sprite": "pnj_rocket", "notes": "ROCKET_M dans l'original"},
        "pnj_celadopole_02": {"sprite": "pnj_gros", "notes": "FAT_MAN dans l'original"},
        "pnj_celadopole_03": {"sprite": "pnj_vieux", "notes": "OLD_MAN_1 dans l'original"},
        "pnj_celadopole_04": {"sprite": "pnj_femme2", "notes": "WOMAN_2 dans l'original"},
        "pnj_celadopole_05": {"sprite": "pnj_fillette", "notes": "LITTLE_GIRL dans l'original"},
    },

    # === LAVANVILLE ===
    # Decomp: LITTLE_GIRL, WORKER_M, BOY
    "lavanville": {
        "pnj_lavanville_01": {"sprite": "pnj_fillette", "notes": "LITTLE_GIRL dans l'original"},
        "pnj_lavanville_02": {"sprite": "pnj_ouvrier", "notes": "WORKER_M dans l'original"},
        "pnj_lavanville_03": {"sprite": "pnj_garcon", "notes": "BOY dans l'original"},
    },

    # === SAFRANIA ===
    # Decomp: ROCKET_M×8, YOUNGSTER, WORKER_M, MAN, BOY, LASS, CRUSH_GIRL
    "safrania": {
        "pnj_safrania_01": {"sprite": "pnj_gamin", "notes": "YOUNGSTER dans l'original"},
        "pnj_safrania_02": {"sprite": "pnj_gamine", "notes": "LASS dans l'original"},
        "pnj_safrania_03": {"sprite": "pnj_homme", "notes": "MAN dans l'original"},
    },

    # === PARMANIE ===
    # Decomp: FAT_MAN, YOUNGSTER, LITTLE_BOY, OLD_MAN_1, BUG_CATCHER, LASS
    "parmanie": {
        "pnj_parmanie_01": {"sprite": "pnj_gamin", "notes": "YOUNGSTER dans l'original"},
        "pnj_parmanie_02": {"sprite": "pnj_gamine", "notes": "LASS dans l'original"},
    },

    # === CRAMOISILE ===
    # Decomp: WOMAN_2, OLD_MAN_1, BILL
    "cramoisile": {
        "pnj_cramoisile_01": {"sprite": "pnj_femme2", "notes": "WOMAN_2 dans l'original"},
        "pnj_cramoisile_02": {"sprite": "pnj_vieux", "notes": "OLD_MAN_1 dans l'original"},
    },

    # === ROUTE 8 ===
    "route_8": {
        "dresseur_route8_01": {"sprite": "dresseur_m", "notes": "COOLTRAINER_M"},
        "dresseur_route8_02": {"sprite": "dresseur_f", "notes": "COOLTRAINER_F"},
    },

    # === ROUTE 9 ===
    "route_9": {
        "randonneur_route9_01": {"sprite": "pnj_montagnard", "notes": "HIKER"},
        "randonneur_route9_02": {"sprite": "pnj_montagnard", "notes": "HIKER"},
    },

    # === ROUTE 10 ===
    "route_10": {
        "randonneur_route10_01": {"sprite": "pnj_montagnard", "notes": "HIKER"},
        "scout_route10_01": {"sprite": "pnj_gamin", "notes": "Correct"},
    },

    # === ROUTE 17 ===
    "route_17": {
        "motard_r17_01_pnj": {"sprite": "pnj_motard", "notes": "Correct: BIKER"},
        "motard_r17_02_pnj": {"sprite": "pnj_motard", "notes": "Correct: BIKER"},
        "motard_r17_03_pnj": {"sprite": "pnj_motard", "notes": "Correct: BIKER"},
    },

    # === ROUTE 24 ===
    "route_24": {
        "rival_route24_001": {"sprite": "pnj_rival", "notes": "Correct"},
        "rocket_pont_pepite": {"sprite": "pnj_rocket", "notes": "Correct"},
    },

    # === ROUTE 25 ===
    "route_25": {
        "dresseur_route25_01": {"sprite": "pnj_montagnard", "notes": "HIKER dans l'original"},
        "pnj_route25_guide": {"sprite": "pnj_homme", "notes": "MAN correct"},
    },

    # ============================================================
    # ARÈNES — CORRECTIONS CRITIQUES
    # ============================================================

    # Arène d'Argenta — Decomp: BROCK, CAMPER, GYM_GUY
    "arene_argenta": {
        "champion_pierre": {"sprite": "brock", "notes": "Sprite dédié de Pierre/Brock"},
        "apprenti_arene_01": {"sprite": "pnj_campeur", "notes": "CAMPER dans l'original"},
        "guide_arene": {"sprite": "pnj_guide_arene", "notes": "GYM_GUY dans l'original"},
    },

    # Arène d'Azuria — Decomp: MISTY, SWIMMER_M_WATER, PICNICKER, GYM_GUY
    "arene_azuria": {
        "champion_ondine": {"sprite": "misty", "notes": "Sprite dédié d'Ondine/Misty"},
        "dresseur_arene_azuria_01": {"sprite": "pnj_nageuse", "notes": "Correct: nageuse"},
        "dresseur_arene_azuria_02": {"sprite": "pnj_pique_niqueuse", "notes": "PICNICKER dans l'original"},
        "pnj_arene_azuria_guide": {"sprite": "pnj_guide_arene", "notes": "GYM_GUY"},
    },

    # Arène de Carmin — Decomp: LT_SURGE, BALDING_MAN, SAILOR, GYM_GUY, GENTLEMAN
    "arene_carmin": {
        "champion_major_bob": {"sprite": "lt_surge", "notes": "Sprite dédié de Major Bob/Lt. Surge"},
        "dresseur_arene_carmin_01": {"sprite": "pnj_marin", "notes": "SAILOR correct"},
        "pnj_arene_carmin_guide": {"sprite": "pnj_guide_arene", "notes": "GYM_GUY"},
    },

    # Arène de Céladopole — Decomp: ERIKA, LASS, BEAUTY, PICNICKER, COOLTRAINER_F
    "arene_celadopole": {
        "champion_erika": {"sprite": "erika", "notes": "Sprite dédié d'Erika"},
        "dresseuse_arene_celadopole_01": {"sprite": "beauty", "notes": "BEAUTY dans l'original"},
        "dresseuse_arene_celadopole_02": {"sprite": "pnj_gamine", "notes": "LASS dans l'original"},
        "pnj_guide_arene_celadopole": {"sprite": "pnj_guide_arene", "notes": "GYM_GUY"},
    },

    # Arène de Parmanie — Decomp: KOGA, ROCKER×4, MAN×2, GYM_GUY
    "arene_parmanie": {
        "champion_koga_pnj": {"sprite": "koga", "notes": "Sprite dédié de Koga"},
        "dresseur_arene_parmanie_01_pnj": {"sprite": "pnj_rocker", "notes": "ROCKER dans l'original (Jongleur)"},
        "dresseur_arene_parmanie_02_pnj": {"sprite": "pnj_rocker", "notes": "ROCKER dans l'original (Jongleur)"},
    },

    # Arène de Safrania — Decomp: SABRINA, COOLTRAINER_M×4, CHANNELER×3, GYM_GUY
    "arene_safrania": {
        "champion_morgane_pnj": {"sprite": "sabrina", "notes": "Sprite dédié de Morgane/Sabrina"},
        "medium_01_pnj": {"sprite": "pnj_medium", "notes": "Correct: CHANNELER"},
        "medium_02_pnj": {"sprite": "pnj_medium", "notes": "Correct: CHANNELER"},
    },

    # Arène de Cramoisîle — Decomp: BLAINE, POKE_MANIAC×3, SCIENTIST×4, GYM_GUY
    "arene_cramoisile": {
        "champion_auguste_pnj": {"sprite": "blaine", "notes": "Sprite dédié d'Auguste/Blaine"},
        "dresseur_arene_auguste_01_pnj": {"sprite": "pnj_scientifique", "notes": "SCIENTIST dans l'original"},
        "dresseur_arene_auguste_02_pnj": {"sprite": "pnj_poke_maniaque", "notes": "POKE_MANIAC dans l'original"},
    },

    # Arène de Jadielle — Decomp: GIOVANNI, BLACK_BELT×3, COOLTRAINER_M×3, MAN×2, GYM_GUY
    "arene_jadielle": {
        "champion_giovanni_arene": {"sprite": "giovanni", "notes": "Sprite dédié de Giovanni"},
        "dresseur_01": {"sprite": "pnj_karateka", "notes": "BLACK_BELT dans l'original"},
        "dresseur_02": {"sprite": "dresseur_m", "notes": "COOLTRAINER_M dans l'original"},
    },

    # ============================================================
    # LIGUE POKÉMON — SPRITES INDIVIDUELS
    # ============================================================
    "ligue_olga": {
        "pnj_ligue_olga": {"sprite": "lorelei", "notes": "Sprite dédié d'Olga/Lorelei"},
    },
    "ligue_aldo": {
        "pnj_ligue_aldo": {"sprite": "bruno", "notes": "Sprite dédié d'Aldo/Bruno"},
    },
    "ligue_agatha": {
        "pnj_ligue_agatha": {"sprite": "agatha", "notes": "Sprite dédié d'Agatha"},
    },
    "ligue_peter": {
        "pnj_ligue_peter": {"sprite": "lance", "notes": "Sprite dédié de Peter/Lance"},
    },
    "ligue_champion": {
        "pnj_ligue_champion": {"sprite": "pnj_rival", "notes": "Le rival est le champoin de la ligue"},
    },

    # ============================================================
    # CENTRES POKÉMON — Uniformiser les sprites
    # ============================================================
    "centre_pokemon_plateau": {
        "infirmiere_plateau": {"sprite": "pnj_infirmiere", "notes": "Uniformiser: infirmiere → pnj_infirmiere"},
        "pc_plateau": {"sprite": "pnj_pc", "notes": "Uniformiser: pc → pnj_pc"},
    },
    "centre_pokemon_celadopole": {
        "pc_celadopole": {"sprite": "pnj_pc", "notes": "Uniformiser: pc → pnj_pc"},
    },

    # ============================================================
    # INTÉRIEURS DIVERS
    # ============================================================

    # Laboratoire Chen
    "laboratoire_chen": {
        "prof_chen": {"sprite": "pnj_chen", "notes": "Correct: PROF_OAK"},
        "rival_labo": {"sprite": "pnj_rival", "notes": "Correct: BLUE"},
    },

    # Maison de Bill
    "maison_bill": {
        "pnj_bill": {"sprite": "bill", "notes": "Sprite dédié de Bill"},
        "pnj_bill_pc": {"sprite": "bill", "notes": "Sprite dédié de Bill"},
    },

    # Tour Pokémon 6F — Mr. Fuji
    "tour_pokemon_6f": {
        "m_fuji": {"sprite": "mr_fuji", "notes": "Sprite dédié de Mr. Fuji (pas pnj_vieux)"},
    },

    # Maison de Mr. Fuji
    "maison_m_fuji": {
        "pnj_fuji_aide_01": {"sprite": "pnj_fillette", "notes": "LITTLE_GIRL dans l'original"},
        "pnj_fuji_aide_02": {"sprite": "pnj_garcon", "notes": "BOY correct"},
    },

    # Mont Sélénite
    "mont_selenite_1f": {
        "montagnard_selenite_01": {"sprite": "pnj_montagnard", "notes": "HIKER dans l'original"},
        "pnj_selenite_guide": {"sprite": "pnj_homme", "notes": "MAN correct"},
    },
    "mont_selenite_b1f": {
        "montagnard_selenite_02": {"sprite": "pnj_montagnard", "notes": "HIKER"},
    },
    "mont_selenite_b2f": {
        "pedro_selenite": {"sprite": "pnj_montagnard", "notes": "HIKER"},
        "pnj_fossile_gauche": {"sprite": "pnj_scientifique", "notes": "SCIENTIST dans l'original"},
        "pnj_fossile_droite": {"sprite": "pnj_scientifique", "notes": "SCIENTIST dans l'original"},
    },

    # Tunnel Roche
    "tunnel_roche_1f": {
        "randonneur_tunnel_roche_01": {"sprite": "pnj_montagnard", "notes": "HIKER"},
    },
    "tunnel_roche_b1f": {
        "randonneur_tunnel_roche_02": {"sprite": "pnj_montagnard", "notes": "HIKER"},
    },

    # Dojo Combat — BLACK_BELT
    "dojo_combat": {
        "maitre_karate_pnj": {"sprite": "pnj_karateka", "notes": "Correct: BLACK_BELT"},
        "karateka_dojo_01_pnj": {"sprite": "pnj_karateka", "notes": "Correct"},
        "karateka_dojo_02_pnj": {"sprite": "pnj_karateka", "notes": "Correct"},
    },

    # Casino — Uniformiser  
    "casino_celadopole": {
        "rocket_casino": {"sprite": "pnj_rocket", "notes": "Correct"},
    },

    # Forêt de Jade — BUG_CATCHER
    "foret_de_jade": {
        "insectomane_foret_01": {"sprite": "pnj_insectomane", "notes": "BUG_CATCHER correct"},
        "insectomane_foret_02": {"sprite": "pnj_insectomane", "notes": "BUG_CATCHER"},
        "insectomane_foret_03": {"sprite": "pnj_insectomane", "notes": "BUG_CATCHER"},
        "insectomane_foret_04": {"sprite": "pnj_insectomane", "notes": "BUG_CATCHER"},
        "pnj_randonneur": {"sprite": "pnj_montagnard", "notes": "HIKER pour le randonneur"},
    },

    # Repaire Rocket B4F — Giovanni
    "repaire_rocket_b4f": {
        "giovanni_repaire": {"sprite": "giovanni", "notes": "Sprite dédié de Giovanni"},
    },

    # Tour Sylphe 5F — Rival  
    "tour_sylphe_5f": {
        "rival_sylphe_pnj": {"sprite": "pnj_rival", "notes": "Correct"},
    },
    # Tour Sylphe 11F — Giovanni
    "tour_sylphe_11f": {
        "giovanni_sylphe_pnj": {"sprite": "giovanni", "notes": "Sprite dédié de Giovanni"},
        "president_sylphe": {"sprite": "pnj_vieux", "notes": "OLD_MAN dans l'original"},
    },

    # SS Anne
    "ss_anne_pont": {
        "pnj_ss_anne_controleur": {"sprite": "pnj_marin", "notes": "SAILOR correct"},
        "rival_ss_anne": {"sprite": "pnj_rival", "notes": "Correct"},
    },
    "ss_anne_capitaine": {
        "capitaine_ss_anne": {"sprite": "pnj_capitaine", "notes": "Correct: CAPTAIN"},
    },
    "ss_anne_cabines": {
        "gentleman_ss_anne_01": {"sprite": "gentleman", "notes": "GENTLEMAN dans l'original"},
    },

    # Manoir Pokémon
    "manoir_pokemon_1f": {
        "scientifique_manoir_01_pnj": {"sprite": "pnj_scientifique", "notes": "Correct"},
    },

    # Cabane Safari (CS03 Surf)
    "cabane_safari_surf": {
        "pnj_cs03_surf": {"sprite": "pnj_vieux", "notes": "OLD_MAN dans l'original"},
    },

    # Maison Gardien Safari
    "maison_gardien_safari": {
        "gardien_safari": {"sprite": "pnj_vieux", "notes": "OLD_MAN dans l'original"},
    },

    # Route Victoire  
    "route_victoire_1f": {
        "dresseur_rv1_01": {"sprite": "dresseur_m", "notes": "COOLTRAINER_M"},
        "dresseur_rv1_02": {"sprite": "dresseur_f", "notes": "COOLTRAINER_F"},
    },
    "route_victoire_2f": {
        "dresseur_rv2_01": {"sprite": "dresseur_m", "notes": "COOLTRAINER_M"},
    },
}


def fix_map(map_path, corrections):
    """Applique les corrections de sprites à un fichier carte JSON."""
    with open(map_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pnjs = data.get("pnj", [])
    changes = 0

    for pnj in pnjs:
        pnj_id = pnj.get("id", "")
        if pnj_id in corrections:
            corr = corrections[pnj_id]
            old_sprite = pnj.get("sprite", "")
            new_sprite = corr["sprite"]
            if old_sprite != new_sprite:
                pnj["sprite"] = new_sprite
                print(f"    {pnj_id}: {old_sprite} → {new_sprite}")
                changes += 1

    if changes > 0:
        with open(map_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return changes


def main():
    total_changes = 0

    for map_name, corrections in sorted(SPRITE_CORRECTIONS.items()):
        map_path = os.path.join(MAPS_DIR, f"{map_name}.json")
        if not os.path.exists(map_path):
            print(f"  ATTENTION: {map_path} n'existe pas!")
            continue

        print(f"\n--- {map_name} ---")
        changes = fix_map(map_path, corrections)
        total_changes += changes
        if changes == 0:
            print("    (aucun changement nécessaire)")

    print(f"\n{'='*60}")
    print(f"Total corrections appliquées: {total_changes}")
    
    # Vérification : lister les sprites utilisés qui n'ont pas de fichier
    print(f"\n--- Vérification des sprites manquants ---")
    used_sprites = set()
    for f in sorted(glob.glob(os.path.join(MAPS_DIR, "*.json"))):
        with open(f, 'r', encoding='utf-8') as fh:
            try:
                d = json.load(fh)
            except:
                continue
        for pnj in d.get("pnj", []):
            s = pnj.get("sprite", "")
            if s:
                used_sprites.add(s)
    
    chars_dir = "assets/sprites/characters"
    missing = []
    for s in sorted(used_sprites):
        test_file = os.path.join(chars_dir, f"{s}_bas_0.png")
        if not os.path.exists(test_file):
            missing.append(s)
    
    if missing:
        print(f"Sprites utilisés SANS fichier ({len(missing)}):")
        for s in missing:
            print(f"  - {s}")
    else:
        print("✓ Tous les sprites utilisés ont leurs fichiers!")


if __name__ == "__main__":
    main()
