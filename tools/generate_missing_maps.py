#!/usr/bin/env python3
"""Génère les cartes JSON manquantes pour Sprint D."""

import json
import os

MAPS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "maps")

def tile_grid(w, h, fill=24, wall=25):
    """Crée une grille rectangulaire avec des murs sur les bords."""
    grid = []
    for y in range(h):
        for x in range(w):
            if x == 0 or x == w-1 or y == 0 or y == h-1:
                grid.append(wall)
            else:
                grid.append(fill)
    return grid

def tile_grid_cave(w, h, water_rects=None):
    """Grille de grotte avec eau optionnelle."""
    grid = tile_grid(w, h, fill=24, wall=25)
    if water_rects:
        for (rx1, ry1, rx2, ry2) in water_rects:
            for y in range(ry1, ry2+1):
                for x in range(rx1, rx2+1):
                    grid[y * w + x] = 4
    return grid

def tile_grid_outdoor(w, h, grass_rects=None, water_rects=None, path_cols=None):
    """Grille extérieure avec herbes, eau et chemin."""
    grid = []
    for y in range(h):
        for x in range(w):
            if x == 0 or x == w-1 or y == 0 or y == h-1:
                grid.append(3)  # arbres bordure
            else:
                grid.append(0)  # sol normal
    if grass_rects:
        for (rx1, ry1, rx2, ry2) in grass_rects:
            for y in range(ry1, ry2+1):
                for x in range(rx1, rx2+1):
                    if 0 <= y < h and 0 <= x < w:
                        grid[y * w + x] = 1
    if water_rects:
        for (rx1, ry1, rx2, ry2) in water_rects:
            for y in range(ry1, ry2+1):
                for x in range(rx1, rx2+1):
                    if 0 <= y < h and 0 <= x < w:
                        grid[y * w + x] = 4
    if path_cols:
        for (col, y1, y2) in path_cols:
            for y in range(y1, y2+1):
                if 0 <= y < h and 0 <= col < w:
                    grid[y * w + col] = 2
    return grid

def save_map(filename, data):
    path = os.path.join(MAPS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {filename}")

# =====================================================
# ROUTE 11 — entre Carmin-sur-Mer et Lavanville
# =====================================================
def gen_route_11():
    w, h = 30, 15
    grass = [(2,3,8,8), (15,2,22,6), (24,8,28,12)]
    path = [(10, 1, h-2), (11, 1, h-2)]
    data = {
        "id": "route_11",
        "nom": "Route 11",
        "largeur": w,
        "hauteur": h,
        "tileset": "exterieur",
        "musique": "res://assets/audio/music/route_11.ogg",
        "tile_data": tile_grid_outdoor(w, h, grass_rects=grass, path_cols=path),
        "connexions": [
            {"direction": "ouest", "vers": "carmin_sur_mer", "decalage": 0},
            {"direction": "est", "vers": "route_12", "decalage": 0}
        ],
        "warps": [
            {"id": "entree_tunnel_souterrain", "x": 14, "y": 1, "vers_map": "tunnel_souterrain_2", "vers_warp": "sortie_sud", "type": "grotte"}
        ],
        "zones_herbes": [
            {"x1": 2, "y1": 3, "x2": 8, "y2": 8, "table": "route_11"},
            {"x1": 15, "y1": 2, "x2": 22, "y2": 6, "table": "route_11"},
            {"x1": 24, "y1": 8, "x2": 28, "y2": 12, "table": "route_11"}
        ],
        "pnj": [
            {"id": "dresseur_route11_1", "x": 5, "y": 6, "sprite": "pnj_gamin", "direction": "droite", "dresseur": True, "trainer_id": "route11_gamin1", "portee_vue": 3},
            {"id": "dresseur_route11_2", "x": 18, "y": 4, "sprite": "pnj_fillette", "direction": "bas", "dresseur": True, "trainer_id": "route11_fillette1", "portee_vue": 3},
            {"id": "dresseur_route11_3", "x": 26, "y": 10, "sprite": "pnj_gamin", "direction": "gauche", "dresseur": True, "trainer_id": "route11_gamin2", "portee_vue": 4},
            {"id": "pnj_route11_1", "x": 12, "y": 7, "sprite": "pnj_homme", "direction": "bas", "dialogue": ["Le Diglett's Cave est juste au nord !", "Tu peux y accéder par l'entrée."], "mobile": False}
        ],
        "panneaux": [
            {"x": 1, "y": 7, "texte": "ROUTE 11\nCARMIN-SUR-MER — LAVANVILLE"}
        ],
        "objets_sol": [
            {"id": "obj_potion_r11", "x": 20, "y": 9, "item": "super_potion", "quantite": 1}
        ]
    }
    save_map("route_11.json", data)

# =====================================================
# TOUR SYLPHE — étages manquants (2F-4F, 6F-10F)
# =====================================================
def gen_tour_sylphe_floors():
    w, h = 15, 12
    # Chaque étage a un accès escalier haut et bas + des rockets
    floors = {
        "2f": {"down": "1f", "up": "3f"},
        "3f": {"down": "2f", "up": "4f"},
        "4f": {"down": "3f", "up": "5f"},
        "6f": {"down": "5f", "up": "7f"},
        "7f": {"down": "6f", "up": "8f"},
        "8f": {"down": "7f", "up": "9f"},
        "9f": {"down": "8f", "up": "10f"},
        "10f": {"down": "9f", "up": "11f"},
    }
    
    rocket_sprites = ["pnj_rocket_homme", "pnj_rocket_femme"]
    
    for floor_name, links in floors.items():
        fname = f"tour_sylphe_{floor_name}"
        # Créer le tile_data avec quelques murs intérieurs variés
        td = tile_grid(w, h, fill=24, wall=25)
        # Ajouter un mur intérieur pour la variété
        floor_num = int(floor_name.replace("f", ""))
        if floor_num % 2 == 0:
            # Mur horizontal au milieu
            for x in range(3, 10):
                td[6 * w + x] = 25
        else:
            # Mur vertical
            for y in range(3, 9):
                td[y * w + 7] = 25
        
        pnjs = []
        # 1-3 Rockets par étage
        n_rockets = min(3, floor_num - 1)
        positions_rockets = [(3, 3), (10, 5), (5, 9)]
        for i in range(n_rockets):
            px, py = positions_rockets[i]
            pnjs.append({
                "id": f"rocket_{fname}_{i+1}",
                "x": px, "y": py,
                "sprite": rocket_sprites[i % 2],
                "direction": "bas",
                "dresseur": True,
                "trainer_id": f"sylphe_{floor_name}_rocket{i+1}"
            })
        
        # Otage/PNJ dialogue
        pnjs.append({
            "id": f"pnj_{fname}_employe",
            "x": 8, "y": 8,
            "sprite": "pnj_scientifique",
            "direction": "bas",
            "dialogue": [f"Bienvenue au {floor_num}e étage de la Tour Sylphe.", "La Team Rocket a envahi les lieux !"],
            "mobile": False
        })
        
        warps = [
            {"id": f"escalier_{links['down']}", "x": 1, "y": 1, "vers_map": f"tour_sylphe_{links['down']}", "vers_warp": f"escalier_{floor_name}", "type": "escalier"},
            {"id": f"escalier_{links['up']}", "x": 13, "y": 1, "vers_map": f"tour_sylphe_{links['up']}", "vers_warp": f"escalier_{floor_name}", "type": "escalier"}
        ]
        
        # Objet sol sur certains étages
        objets = []
        items_par_etage = {
            "2f": ("cle_carte", "Carte Magnétique"),
            "4f": ("elixir", "Élixir"),
            "6f": ("super_potion", "Super Potion"),
            "7f": ("corde_sortie", "Corde Sortie"),
            "9f": ("ct_psycho", "CT Psycho"),
        }
        if floor_name in items_par_etage:
            item_id, _ = items_par_etage[floor_name]
            objets.append({"id": f"obj_{fname}", "x": 12, "y": 10, "item": item_id, "quantite": 1})
        
        data = {
            "id": fname,
            "nom": f"Tour Sylphe {floor_name.upper()}",
            "largeur": w,
            "hauteur": h,
            "tileset": "interieur",
            "musique": "res://assets/audio/music/tour_sylphe.ogg",
            "tile_data": td,
            "connexions": [],
            "warps": warps,
            "pnj": pnjs,
            "panneaux": [],
            "objets_sol": objets
        }
        save_map(f"{fname}.json", data)

# =====================================================
# MANOIR POKÉMON — 3F et B1F
# =====================================================
def gen_manoir_pokemon_floors():
    w, h = 15, 12
    
    # 3F
    td_3f = tile_grid(w, h, fill=24, wall=25)
    # Murs intérieurs en L
    for x in range(3, 8):
        td_3f[4 * w + x] = 25
    for y in range(4, 9):
        td_3f[y * w + 7] = 25
    
    save_map("manoir_pokemon_3f.json", {
        "id": "manoir_pokemon_3f",
        "nom": "Manoir Pokémon 3F",
        "largeur": w,
        "hauteur": h,
        "tileset": "interieur",
        "musique": "res://assets/audio/music/manoir_pokemon.ogg",
        "tile_data": td_3f,
        "connexions": [],
        "warps": [
            {"id": "escalier_2f", "x": 13, "y": 10, "vers_map": "manoir_pokemon_2f", "vers_warp": "escalier_3f", "type": "escalier"},
            {"id": "escalier_b1f", "x": 1, "y": 1, "vers_map": "manoir_pokemon_b1f", "vers_warp": "escalier_3f", "type": "escalier"}
        ],
        "pnj": [
            {"id": "scientifique_manoir3f", "x": 5, "y": 7, "sprite": "pnj_scientifique", "direction": "droite", "dresseur": True, "trainer_id": "manoir_scientifique3"},
            {"id": "pnj_journal_3f", "x": 10, "y": 3, "sprite": "pnj_panneau", "direction": "bas", "dialogue": ["Journal du Dr X : 'Nous avons découvert une espèce rare...Mew.'", "'Le 6 février, Mew a donné naissance...'", "'Nous l'avons nommé Mewtwo.'"], "mobile": False}
        ],
        "panneaux": [],
        "objets_sol": [
            {"id": "obj_manoir3f_ct", "x": 2, "y": 9, "item": "ct_lance_flamme", "quantite": 1}
        ]
    })
    
    # B1F
    td_b1f = tile_grid(w, h, fill=24, wall=25)
    # Plusieurs murs internes formant un mini-labyrinthe
    for x in range(2, 6):
        td_b1f[3 * w + x] = 25
    for x in range(8, 13):
        td_b1f[5 * w + x] = 25
    for y in range(7, 11):
        td_b1f[y * w + 5] = 25
    for y in range(2, 6):
        td_b1f[y * w + 10] = 25
    
    save_map("manoir_pokemon_b1f.json", {
        "id": "manoir_pokemon_b1f",
        "nom": "Manoir Pokémon B1F",
        "largeur": w,
        "hauteur": h,
        "tileset": "interieur",
        "musique": "res://assets/audio/music/manoir_pokemon.ogg",
        "tile_data": td_b1f,
        "sombre": True,
        "connexions": [],
        "warps": [
            {"id": "escalier_3f", "x": 1, "y": 1, "vers_map": "manoir_pokemon_3f", "vers_warp": "escalier_b1f", "type": "escalier"}
        ],
        "pnj": [
            {"id": "scientifique_manoir_b1f", "x": 8, "y": 8, "sprite": "pnj_scientifique", "direction": "haut", "dresseur": True, "trainer_id": "manoir_scientifique_b1f"},
            {"id": "pnj_journal_b1f", "x": 12, "y": 3, "sprite": "pnj_panneau", "direction": "bas", "dialogue": ["Journal du Dr X : 'Mewtwo est devenu trop puissant.'", "'Nous ne pouvons plus le contrôler...'"], "mobile": False}
        ],
        "panneaux": [],
        "objets_sol": [
            {"id": "obj_manoir_b1f_cle", "x": 3, "y": 10, "item": "cle_arene_cramoisile", "quantite": 1}
        ]
    })

# =====================================================
# ÎLES ÉCUME — B3F et B4F
# =====================================================
def gen_iles_ecume_floors():
    w, h = 15, 15
    
    # B3F — grotte avec passages d'eau
    water_b3 = [(3, 5, 6, 9), (9, 3, 12, 7)]
    td_b3f = tile_grid_cave(w, h, water_rects=water_b3)
    
    save_map("iles_ecume_b3f.json", {
        "id": "iles_ecume_b3f",
        "nom": "Îles Écume B3F",
        "largeur": w,
        "hauteur": h,
        "tileset": "grotte",
        "musique": "res://assets/audio/music/iles_ecume.ogg",
        "sombre": True,
        "tile_data": td_b3f,
        "connexions": [],
        "warps": [
            {"id": "escalier_b2f", "x": 12, "y": 13, "vers_map": "iles_ecume_b2f", "vers_warp": "escalier_b3f", "type": "escalier"},
            {"id": "escalier_b4f", "x": 2, "y": 2, "vers_map": "iles_ecume_b4f", "vers_warp": "escalier_b3f", "type": "escalier"}
        ],
        "pnj": [],
        "panneaux": [],
        "objets_sol": [
            {"id": "obj_ecume_b3f", "x": 7, "y": 12, "item": "perle", "quantite": 1}
        ]
    })
    
    # B4F — Artikodin se trouve ici (on le déplace du B2F qui l'avait par erreur)
    water_b4 = [(2, 4, 12, 8)]
    td_b4f = tile_grid_cave(w, h, water_rects=water_b4)
    # Créer un îlot au centre de l'eau pour Artikodin
    for x in range(6, 9):
        for y in range(5, 8):
            td_b4f[y * w + x] = 24  # îlot
    
    save_map("iles_ecume_b4f.json", {
        "id": "iles_ecume_b4f",
        "nom": "Îles Écume B4F",
        "largeur": w,
        "hauteur": h,
        "tileset": "grotte",
        "musique": "res://assets/audio/music/iles_ecume.ogg",
        "sombre": True,
        "tile_data": td_b4f,
        "connexions": [],
        "warps": [
            {"id": "escalier_b3f", "x": 12, "y": 13, "vers_map": "iles_ecume_b3f", "vers_warp": "escalier_b4f", "type": "escalier"}
        ],
        "pnj": [
            {"id": "artikodin", "x": 7, "y": 6, "sprite": "pnj_legendaire", "direction": "bas", "type": "legendaire", "pokemon_id": "144", "niveau": 50, "dialogue": ["Artikodin te fixe d'un regard glacial !"], "mobile": False}
        ],
        "panneaux": [],
        "objets_sol": []
    })

# =====================================================
# PARC SAFARI — Zone 3 et Zone 4
# =====================================================
def gen_safari_zones():
    w, h = 25, 25
    
    # Zone 3 — Dent d'Or ici
    grass_z3 = [(2,2,10,10), (14,3,22,8), (3,15,12,22), (16,14,23,21)]
    water_z3 = [(11,12,14,16)]
    td_z3 = tile_grid_outdoor(w, h, grass_rects=grass_z3, water_rects=water_z3)
    
    save_map("parc_safari_zone3.json", {
        "id": "parc_safari_zone3",
        "nom": "Parc Safari Zone 3",
        "largeur": w,
        "hauteur": h,
        "tileset": "exterieur",
        "musique": "res://assets/audio/music/parc_safari.ogg",
        "tile_data": td_z3,
        "connexions": [],
        "warps": [
            {"id": "depuis_zone2", "x": 12, "y": 24, "vers_map": "parc_safari_zone2", "vers_warp": "vers_zone3", "type": "porte"},
            {"id": "vers_zone4", "x": 12, "y": 0, "vers_map": "parc_safari_zone4", "vers_warp": "depuis_zone3", "type": "porte"}
        ],
        "zones_herbes": [
            {"x1": 2, "y1": 2, "x2": 10, "y2": 10, "table": "parc_safari"},
            {"x1": 14, "y1": 3, "x2": 22, "y2": 8, "table": "parc_safari"},
            {"x1": 3, "y1": 15, "x2": 12, "y2": 22, "table": "parc_safari"},
            {"x1": 16, "y1": 14, "x2": 23, "y2": 21, "table": "parc_safari"}
        ],
        "pnj": [
            {"id": "pnj_safari_z3_1", "x": 6, "y": 12, "sprite": "pnj_homme", "direction": "droite", "dialogue": ["Le Gardien du Safari a perdu sa Dent d'Or quelque part par ici..."], "mobile": False}
        ],
        "panneaux": [],
        "objets_sol": [
            {"id": "obj_dent_or_safari", "x": 18, "y": 18, "item": "dent_or", "quantite": 1}
        ]
    })
    
    # Zone 4 — Cabane CS Surf + zone secrète
    grass_z4 = [(2,5,11,12), (14,2,23,10), (3,16,22,22)]
    water_z4 = [(2,13,11,15)]
    td_z4 = tile_grid_outdoor(w, h, grass_rects=grass_z4, water_rects=water_z4)
    
    save_map("parc_safari_zone4.json", {
        "id": "parc_safari_zone4",
        "nom": "Parc Safari Zone 4",
        "largeur": w,
        "hauteur": h,
        "tileset": "exterieur",
        "musique": "res://assets/audio/music/parc_safari.ogg",
        "tile_data": td_z4,
        "connexions": [],
        "warps": [
            {"id": "depuis_zone3", "x": 12, "y": 24, "vers_map": "parc_safari_zone3", "vers_warp": "vers_zone4", "type": "porte"},
            {"id": "entree_cabane_cs", "x": 20, "y": 5, "vers_map": "cabane_safari_surf", "vers_warp": "sortie", "type": "porte"}
        ],
        "zones_herbes": [
            {"x1": 2, "y1": 5, "x2": 11, "y2": 12, "table": "parc_safari"},
            {"x1": 14, "y1": 2, "x2": 23, "y2": 10, "table": "parc_safari"},
            {"x1": 3, "y1": 16, "x2": 22, "y2": 22, "table": "parc_safari"}
        ],
        "pnj": [
            {"id": "pnj_safari_z4_1", "x": 15, "y": 7, "sprite": "pnj_femme", "direction": "bas", "dialogue": ["Les Pokémon les plus rares se cachent dans cette zone !"], "mobile": False}
        ],
        "panneaux": [
            {"x": 19, "y": 4, "texte": "CABANE DU GARDIEN\nCS03 SURF À L'INTÉRIEUR"}
        ],
        "objets_sol": [
            {"id": "obj_safari_z4_pepite", "x": 5, "y": 20, "item": "pepite", "quantite": 1},
            {"id": "obj_safari_z4_ct", "x": 21, "y": 15, "item": "ct_toxic", "quantite": 1}
        ]
    })

# =====================================================
# Ajouter les warps manquants aux étages existants
# =====================================================
def patch_existing_maps():
    """Ajouter les warps manquants pour connecter aux nouveaux étages."""
    patches = {
        "tour_sylphe_1f.json": {
            "add_warps": [
                {"id": "escalier_2f", "x": 1, "y": 1, "vers_map": "tour_sylphe_2f", "vers_warp": "escalier_1f", "type": "escalier"}
            ]
        },
        "tour_sylphe_5f.json": {
            "add_warps": [
                {"id": "escalier_4f", "x": 1, "y": 1, "vers_map": "tour_sylphe_4f", "vers_warp": "escalier_5f", "type": "escalier"},
                {"id": "escalier_6f", "x": 13, "y": 1, "vers_map": "tour_sylphe_6f", "vers_warp": "escalier_5f", "type": "escalier"}
            ]
        },
        "tour_sylphe_11f.json": {
            "add_warps": [
                {"id": "escalier_10f", "x": 1, "y": 1, "vers_map": "tour_sylphe_10f", "vers_warp": "escalier_11f", "type": "escalier"}
            ]
        },
        "manoir_pokemon_2f.json": {
            "add_warps": [
                {"id": "escalier_3f", "x": 1, "y": 1, "vers_map": "manoir_pokemon_3f", "vers_warp": "escalier_2f", "type": "escalier"}
            ]
        },
        "iles_ecume_b2f.json": {
            "add_warps": [
                {"id": "escalier_b3f", "x": 2, "y": 2, "vers_map": "iles_ecume_b3f", "vers_warp": "escalier_b2f", "type": "escalier"}
            ]
        },
        "parc_safari_zone2.json": {
            "add_warps": [
                {"id": "vers_zone3", "x": 12, "y": 0, "vers_map": "parc_safari_zone3", "vers_warp": "depuis_zone2", "type": "porte"}
            ]
        }
    }
    
    for filename, patch in patches.items():
        path = os.path.join(MAPS_DIR, filename)
        if not os.path.exists(path):
            print(f"  ⚠ {filename} introuvable, skip")
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if "add_warps" in patch:
            existing_ids = {w.get("id", "") for w in data.get("warps", [])}
            for warp in patch["add_warps"]:
                if warp["id"] not in existing_ids:
                    data.setdefault("warps", []).append(warp)
                    print(f"  + warp '{warp['id']}' ajouté à {filename}")
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    print("=== Génération des cartes manquantes ===")
    print("\n--- Route 11 ---")
    gen_route_11()
    print("\n--- Tour Sylphe (8 étages) ---")
    gen_tour_sylphe_floors()
    print("\n--- Manoir Pokémon (3F + B1F) ---")
    gen_manoir_pokemon_floors()
    print("\n--- Îles Écume (B3F + B4F) ---")
    gen_iles_ecume_floors()
    print("\n--- Parc Safari (Zone 3 + Zone 4) ---")
    gen_safari_zones()
    print("\n--- Patch des cartes existantes ---")
    patch_existing_maps()
    print("\n=== Terminé ! 15 cartes générées/modifiées ===")
