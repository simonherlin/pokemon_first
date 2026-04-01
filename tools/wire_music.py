#!/usr/bin/env python3
"""
Met à jour le champ 'musique' de toutes les cartes JSON pour pointer vers
les vrais fichiers OGG téléchargés depuis FRLG.
"""
import json
import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS_DIR = os.path.join(BASE_DIR, "data", "maps")
MUSIC_DIR = os.path.join(BASE_DIR, "assets", "audio", "music")

# Mapping: carte_id → nom_fichier_ogg (sans chemin ni extension)
MAP_MUSIC = {
    # === Villes ===
    "bourg_palette": "bourg_palette",
    "jadielle_ville": "jadielle",
    "argenta_ville": "argenta",
    "azuria_ville": "azuria",
    "carmin_sur_mer": "carmin",
    "lavanville": "lavanville",
    "celadopole": "celadopole",
    "safrania": "safrania",
    "parmanie": "parmanie",
    "cramoisile": "cramoisile",
    "plateau_indigo": "plateau_indigo",
    
    # === Routes ===
    "route_1": "route_1",
    "route_2": "route_2",
    "route_3": "route_3",
    "route_4": "route_4",
    "route_5": "route_5",
    "route_6": "route_6",
    "route_7": "route_7",
    "route_8": "route_8",
    "route_9": "route_9",
    "route_10": "route_10",
    "route_10_surf": "route_10",
    "route_11": "route_11",
    "route_12": "route_12",
    "route_13": "route_13",
    "route_14": "route_14",
    "route_15": "route_15",
    "route_16": "route_16",
    "route_17": "route_17",
    "route_18": "route_18",
    "route_19": "route_19",
    "route_20": "route_20",
    "route_21": "route_21",
    "route_22": "route_22",
    "route_23": "route_23",
    "route_24": "route_24",
    "route_25": "route_25",
    
    # === Centres Pokémon ===
    "centre_pokemon_argenta": "centre_pokemon",
    "centre_pokemon_azuria": "centre_pokemon",
    "centre_pokemon_carmin": "centre_pokemon",
    "centre_pokemon_celadopole": "centre_pokemon",
    "centre_pokemon_cramoisile": "centre_pokemon",
    "centre_pokemon_jadielle": "centre_pokemon",
    "centre_pokemon_lavanville": "centre_pokemon",
    "centre_pokemon_parmanie": "centre_pokemon",
    "centre_pokemon_plateau": "centre_pokemon",
    "centre_pokemon_safrania": "centre_pokemon",
    
    # === Boutiques ===
    "boutique_azuria": "boutique_pokemon",
    "boutique_carmin": "boutique_pokemon",
    "boutique_cramoisile": "boutique_pokemon",
    "boutique_jadielle": "boutique_pokemon",
    "boutique_lavanville": "boutique_pokemon",
    "boutique_parmanie": "boutique_pokemon",
    "boutique_safrania": "boutique_pokemon",
    "grand_magasin_1f": "boutique_pokemon",
    "grand_magasin_2f": "boutique_pokemon",
    
    # === Arènes ===
    "arene_argenta": "arene",
    "arene_azuria": "arene",
    "arene_carmin": "arene",
    "arene_celadopole": "arene",
    "arene_cramoisile": "arene",
    "arene_jadielle": "arene",
    "arene_parmanie": "arene",
    "arene_safrania": "arene",
    
    # === Laboratoire ===
    "laboratoire_chen": "laboratoire_chen",
    
    # === Grottes / Donjons ===
    "mont_selenite_1f": "mont_selenite",
    "mont_selenite_b1f": "mont_selenite",
    "mont_selenite_b2f": "mont_selenite",
    "foret_de_jade": "foret_jade",
    "grotte_taupiqueur": "grotte_taupiqueur",
    "grotte_inconnue_1f": "grotte_inconnue",
    "grotte_inconnue_b1f": "grotte_inconnue",
    "tunnel_roche_1f": "tunnel",
    "tunnel_roche_b1f": "tunnel",
    "tunnel_souterrain": "tunnel",
    "tunnel_souterrain_2": "tunnel",
    "iles_ecume_1f": "iles_ecume",
    "iles_ecume_b1f": "iles_ecume",
    "iles_ecume_b2f": "iles_ecume",
    "route_victoire_1f": "route_victoire",
    "route_victoire_2f": "route_victoire",
    "route_victoire_3f": "route_victoire",
    
    # === Tour Pokémon (Lavanville) ===
    "tour_pokemon_1f": "tour_pokemon",
    "tour_pokemon_2f": "tour_pokemon",
    "tour_pokemon_3f": "tour_pokemon",
    "tour_pokemon_4f": "tour_pokemon",
    "tour_pokemon_5f": "tour_pokemon",
    "tour_pokemon_6f": "tour_pokemon",
    
    # === Tour Sylphe ===
    "tour_sylphe_1f": "tour_sylphe",
    "tour_sylphe_5f": "tour_sylphe",
    "tour_sylphe_11f": "tour_sylphe",
    
    # === Repaire Rocket ===
    "repaire_rocket_b1f": "repaire_rocket",
    "repaire_rocket_b2f": "repaire_rocket",
    "repaire_rocket_b3f": "repaire_rocket",
    "repaire_rocket_b4f": "repaire_rocket",
    
    # === SS Anne ===
    "ss_anne_pont": "ss_anne",
    "ss_anne_cabines": "ss_anne",
    "ss_anne_cuisine": "ss_anne",
    "ss_anne_capitaine": "ss_anne",
    
    # === Manoir Pokémon ===
    "manoir_pokemon_1f": "manoir_pokemon",
    "manoir_pokemon_2f": "manoir_pokemon",
    
    # === Parc Safari ===
    "parc_safari_entree": "parc_safari",
    "parc_safari_zone1": "parc_safari",
    "parc_safari_zone2": "parc_safari",
    "cabane_safari_surf": "parc_safari",
    
    # === Casino ===
    "casino_celadopole": "casino",
    
    # === Ligue Pokémon ===
    "ligue_olga": "arene",        # Salle Olga = ambiance arène/combat
    "ligue_aldo": "arene",        # Salle Aldo
    "ligue_agatha": "arene",      # Salle Agatha
    "ligue_peter": "arene",       # Salle Peter
    "ligue_champion": "arene",    # Salle Champion/Rival
    
    # === Dojo Combat ===
    "dojo_combat": "dojo_combat",
    
    # === Maisons / Bâtiments divers ===
    "maison_joueur": "bourg_palette",      # Maison du joueur = thème village
    "maison_joueur_2f": "bourg_palette",
    "maison_rival": "bourg_palette",
    "maison_bill": "azuria",               # Maison de Bill = thème Azuria
    "maison_m_fuji": "lavanville",         # Maison M. Fuji = thème Lavanville
    "maison_gardien_safari": "parmanie",
    "maison_cs05_vol": "parmanie",
    "maison_evoli_celadopole": "celadopole",
    "labo_fossiles": "labo_fossiles",
    "centrale": "repaire_rocket",           # Centrale = ambiance industrielle
    "musee_argenta": "musee",
}


def main():
    updated = 0
    already_ok = 0
    no_mapping = 0
    
    for json_path in sorted(glob.glob(os.path.join(MAPS_DIR, "*.json"))):
        map_id = os.path.basename(json_path).replace(".json", "")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if map_id in MAP_MUSIC:
            track = MAP_MUSIC[map_id]
            expected_path = f"res://assets/audio/music/{track}.ogg"
            ogg_file = os.path.join(MUSIC_DIR, f"{track}.ogg")
            
            if not os.path.exists(ogg_file):
                print(f"  [WARN] OGG manquant: {track}.ogg pour {map_id}")
                continue
            
            current = data.get("musique", "")
            if current == expected_path:
                already_ok += 1
                continue
            
            data["musique"] = expected_path
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"  {map_id}: {current or '(vide)'} → {expected_path}")
            updated += 1
        else:
            no_mapping += 1
            current = data.get("musique", "")
            if not current:
                print(f"  [NO MAP] {map_id}")
    
    print(f"\nRésultat: {updated} mis à jour, {already_ok} déjà OK, {no_mapping} sans mapping")


if __name__ == "__main__":
    main()
