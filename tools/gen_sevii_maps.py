#!/usr/bin/env python3
"""Génère les cartes JSON des Îles Sevii pour le projet Pokémon."""
import json
import os

OUT_DIR = "data/maps"

def tile_grid(w, h, default=0):
    return [[default]*w for _ in range(h)]

def flat_grid(w, h, default=0):
    return [default]*(w*h)

def set_rect(grid, x1, y1, x2, y2, val):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                grid[y][x] = val

def set_rect_flat(data, w, x1, y1, x2, y2, val):
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            idx = y*w + x
            if 0 <= idx < len(data):
                data[idx] = val

def set_border(grid, w, h, val):
    for x in range(w):
        grid[0][x] = val
        grid[h-1][x] = val
    for y in range(h):
        grid[y][0] = val
        grid[y][w-1] = val

def write_map(filename, data):
    path = os.path.join(OUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Créé: {path}")

# ===========================================================================
# ÎLE 1 — Île des Braises (ville portuaire principale)
# ===========================================================================
def gen_ile1():
    W, H = 18, 16
    sol = tile_grid(W, H, 0)  # herbe
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    
    # Eau en bas (port)
    set_rect(sol, 0, 13, 17, 15, 5)
    set_rect_flat(col, W, 0, 13, 17, 15, 2)  # surfable
    # Quai
    set_rect(sol, 7, 12, 10, 13, 2)
    set_rect_flat(col, W, 7, 12, 10, 13, 0)
    # Chemin principal
    set_rect(sol, 7, 3, 10, 12, 2)
    set_rect(sol, 3, 6, 14, 7, 2)
    # Sable autour du port
    set_rect(sol, 0, 11, 17, 12, 6)
    set_rect_flat(col, W, 0, 11, 6, 12, 0)
    set_rect_flat(col, W, 11, 11, 17, 12, 0)
    # Arbres bordure
    set_border(obj, W, H, 10)
    set_rect_flat(col, W, 0, 0, 17, 0, 3)
    set_rect_flat(col, W, 0, 0, 0, 15, 3)
    set_rect_flat(col, W, 17, 0, 17, 15, 3)
    # Bâtiments
    # Centre Pokémon (en haut à gauche)
    set_rect(obj, 3, 3, 5, 4, 8)
    set_rect_flat(col, W, 3, 3, 5, 4, 3)
    # Boutique (en haut à droite)
    set_rect(obj, 12, 3, 14, 4, 8)
    set_rect_flat(col, W, 12, 3, 14, 4, 3)
    # Maison PNJ
    set_rect(obj, 3, 8, 5, 9, 8)
    set_rect_flat(col, W, 3, 8, 5, 9, 3)

    return {
        "id": "sevii_ile1",
        "nom": "Île 1 — Port des Braises",
        "largeur": W, "hauteur": H,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/sevii_ile1.ogg",
        "connexions": [
            {"direction": "nord", "vers": "sevii_grotte_braise_ext", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 4, "y": 5, "vers_map": "sevii_ile1_centre_pokemon", "vers_warp": "sortie", "type": "porte"},
            {"id": "boutique_entree", "x": 13, "y": 5, "vers_map": "sevii_ile1_boutique", "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_entree", "x": 4, "y": 10, "vers_map": "sevii_ile1_maison", "vers_warp": "sortie", "type": "porte"},
            {"id": "port_ferry", "x": 8, "y": 13, "vers_map": "carmin_sur_mer", "vers_warp": "sevii_ferry_arrivee", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_marin_ile1", "x": 9, "y": 12, "sprite": "pnj_marin", "direction": "gauche",
             "dialogue": ["Le ferry fait la navette entre\nCarmin-sur-Mer et les Îles Sevii.", "Monte à bord quand tu veux !"],
             "mobile": False},
            {"id": "pnj_femme_ile1", "x": 6, "y": 7, "sprite": "pnj_femme", "direction": "droite",
             "dialogue": ["Bienvenue sur l'Île des Braises !", "C'est un endroit paisible,\nmais la grotte au nord\ncache des Pokémon rares."],
             "mobile": False},
            {"id": "pnj_vieil_homme_ile1", "x": 13, "y": 7, "sprite": "pnj_vieil_homme", "direction": "bas",
             "dialogue": ["On dit qu'un oiseau légendaire\nvit au sommet du volcan…", "Mais personne n'a pu le vérifier."],
             "dialogue_conditions": [
                 {"flag": "sevii_volcan_termine", "valeur": True, "dialogue": ["Tu as exploré le volcan ?!\nQuel courage !"]}
             ],
             "mobile": False}
        ],
        "objets_sol": [],
        "panneaux": [
            {"x": 8, "y": 6, "texte": "ÎLE 1 — PORT DES BRAISES\n— Porte d'entrée des Îles Sevii —"},
            {"x": 4, "y": 5, "texte": "CENTRE POKÉMON"},
            {"x": 13, "y": 5, "texte": "BOUTIQUE POKÉMON"}
        ],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# ÎLE 1 — Centre Pokémon
# ===========================================================================
def gen_ile1_centre():
    W, H = 10, 8
    sol = tile_grid(W, H, 24)
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    # Murs extérieurs
    set_rect(obj, 0, 0, 9, 0, 25)
    set_rect(obj, 0, 0, 0, 7, 25)
    set_rect(obj, 9, 0, 9, 7, 25)
    set_rect_flat(col, W, 0, 0, 9, 0, 3)
    set_rect_flat(col, W, 0, 0, 0, 7, 3)
    set_rect_flat(col, W, 9, 0, 9, 7, 3)
    # Comptoir
    set_rect(obj, 3, 1, 6, 1, 26)
    set_rect_flat(col, W, 3, 1, 6, 1, 3)
    # PC
    obj[1][1] = 27
    col[1*W+1] = 3

    return {
        "id": "sevii_ile1_centre_pokemon",
        "nom": "Centre Pokémon",
        "largeur": W, "hauteur": H,
        "tileset": "indoor",
        "musique": "res://assets/audio/music/centre_pokemon.ogg",
        "connexions": [],
        "warps": [
            {"id": "sortie", "x": 5, "y": 7, "vers_map": "sevii_ile1", "vers_warp": "centre_pokemon_entree", "type": "porte"}
        ],
        "pnj": [
            {"id": "infirmiere_sevii1", "x": 5, "y": 1, "sprite": "pnj_infirmiere", "direction": "bas",
             "dialogue": ["Bienvenue au Centre Pokémon\ndes Îles Sevii !", "Je vais soigner vos Pokémon.",
                          "...Vos Pokémon sont maintenant\nen pleine forme !", "Revenez quand vous voulez !"],
             "mobile": False, "type": "infirmiere"},
            {"id": "pc_sevii1", "x": 1, "y": 1, "sprite": "pnj_pc", "direction": "bas",
             "dialogue": ["Il y a un PC ici.", "Voulez-vous l'utiliser ?"],
             "mobile": False, "type": "pc"},
            {"id": "pnj_centre_sevii1", "x": 8, "y": 4, "sprite": "pnj_homme", "direction": "gauche",
             "dialogue": ["Les Îles Sevii sont un archipel\nde 3 îles au sud de Kanto.", "Chacune a ses propres\nPokémon sauvages !"],
             "mobile": False}
        ],
        "objets_sol": [],
        "panneaux": [],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# ÎLE 1 — Boutique
# ===========================================================================
def gen_ile1_boutique():
    W, H = 8, 6
    sol = tile_grid(W, H, 24)
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    set_rect(obj, 0, 0, 7, 0, 25)
    set_rect(obj, 0, 0, 0, 5, 25)
    set_rect(obj, 7, 0, 7, 5, 25)
    set_rect_flat(col, W, 0, 0, 7, 0, 3)
    set_rect_flat(col, W, 0, 0, 0, 5, 3)
    set_rect_flat(col, W, 7, 0, 7, 5, 3)
    set_rect(obj, 2, 1, 5, 1, 26)
    set_rect_flat(col, W, 2, 1, 5, 1, 3)

    return {
        "id": "sevii_ile1_boutique",
        "nom": "Boutique Pokémon",
        "largeur": W, "hauteur": H,
        "tileset": "indoor",
        "musique": "res://assets/audio/music/boutique.ogg",
        "connexions": [],
        "warps": [
            {"id": "sortie", "x": 4, "y": 5, "vers_map": "sevii_ile1", "vers_warp": "boutique_entree", "type": "porte"}
        ],
        "pnj": [
            {"id": "vendeur_sevii1", "x": 3, "y": 1, "sprite": "pnj_vendeur", "direction": "bas",
             "dialogue": ["Bienvenue ! Nous avons\ndes articles spéciaux\ndes Îles Sevii."],
             "mobile": False, "type": "vendeur",
             "boutique": ["hyper_ball", "super_potion", "hyper_potion", "total_soin", "rappel", "super_repousse", "corde_sortie"]}
        ],
        "objets_sol": [],
        "panneaux": [],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# ÎLE 1 — Maison PNJ
# ===========================================================================
def gen_ile1_maison():
    W, H = 8, 6
    sol = tile_grid(W, H, 24)
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    set_rect(obj, 0, 0, 7, 0, 25)
    set_rect(obj, 0, 0, 0, 5, 25)
    set_rect(obj, 7, 0, 7, 5, 25)
    set_rect_flat(col, W, 0, 0, 7, 0, 3)
    set_rect_flat(col, W, 0, 0, 0, 5, 3)
    set_rect_flat(col, W, 7, 0, 7, 5, 3)

    return {
        "id": "sevii_ile1_maison",
        "nom": "Maison",
        "largeur": W, "hauteur": H,
        "tileset": "indoor",
        "musique": "res://assets/audio/music/maison.ogg",
        "connexions": [],
        "warps": [
            {"id": "sortie", "x": 4, "y": 5, "vers_map": "sevii_ile1", "vers_warp": "maison_entree", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_chercheur_sevii", "x": 3, "y": 2, "sprite": "pnj_scientifique", "direction": "bas",
             "dialogue": ["Je suis un chercheur qui étudie\nles Pokémon des Îles Sevii.", "Ces îles ont des espèces\nqu'on ne trouve nulle part\nailleurs à Kanto !",
                          "Les eaux entre les îles\nregorgent de Pokémon Eau rares."],
             "dialogue_conditions": [
                 {"flag": "sevii_quete_chercheur_terminee", "valeur": True, "dialogue": ["Merci pour ton aide !\nGrâce à toi, mes recherches\navancent bien."]}
             ],
             "mobile": False}
        ],
        "objets_sol": [
            {"id": "obj_pp_plus_sevii", "x": 6, "y": 1, "item_id": "pp_plus", "ramasse": False}
        ],
        "panneaux": [],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# ÎLE 2 — Île du Paradis (résidentielle)
# ===========================================================================
def gen_ile2():
    W, H = 16, 14
    sol = tile_grid(W, H, 0)
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    
    # Eau autour
    set_rect(sol, 0, 0, 15, 1, 5)
    set_rect(sol, 0, 12, 15, 13, 5)
    set_rect(sol, 0, 0, 1, 13, 5)
    set_rect(sol, 14, 0, 15, 13, 5)
    set_rect_flat(col, W, 0, 0, 15, 1, 2)
    set_rect_flat(col, W, 0, 12, 15, 13, 2)
    set_rect_flat(col, W, 0, 0, 1, 13, 2)
    set_rect_flat(col, W, 14, 0, 15, 13, 2)
    # Sol intérieur île
    set_rect(sol, 2, 2, 13, 11, 0)
    # Chemin
    set_rect(sol, 6, 4, 9, 10, 2)
    set_rect(sol, 4, 6, 11, 7, 2)
    # Sable plage
    set_rect(sol, 2, 10, 13, 11, 6)
    set_rect_flat(col, W, 2, 10, 13, 11, 0)
    # Arbres
    for x in [2, 3, 12, 13]:
        for y in [2, 3, 4]:
            obj[y][x] = 10
            col[y*W+x] = 3
    # Maisons
    set_rect(obj, 4, 3, 5, 4, 8)
    set_rect_flat(col, W, 4, 3, 5, 4, 3)
    set_rect(obj, 10, 3, 11, 4, 8)
    set_rect_flat(col, W, 10, 3, 11, 4, 3)
    # Zones herbe
    set_rect(sol, 2, 5, 4, 9, 1)
    set_rect(sol, 11, 5, 13, 9, 1)

    return {
        "id": "sevii_ile2",
        "nom": "Île 2 — Cap du Paradis",
        "largeur": W, "hauteur": H,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/sevii_ile2.ogg",
        "connexions": [],
        "warps": [
            {"id": "maison1_entree", "x": 5, "y": 5, "vers_map": "sevii_ile2_maison1", "vers_warp": "sortie", "type": "porte"},
            {"id": "maison2_entree", "x": 10, "y": 5, "vers_map": "sevii_ile2_maison2", "vers_warp": "sortie", "type": "porte"}
        ],
        "zones_herbes": [
            {"x1": 2, "y1": 5, "x2": 4, "y2": 9, "table": "sevii_ile2"},
            {"x1": 11, "y1": 5, "x2": 13, "y2": 9, "table": "sevii_ile2"}
        ],
        "pnj": [
            {"id": "pnj_ile2_peche", "x": 7, "y": 10, "sprite": "pnj_pecheur", "direction": "bas",
             "dialogue": ["La pêche est excellente\npar ici !", "J'ai même vu un Léviator\nune fois !"],
             "mobile": False},
            {"id": "pnj_ile2_fille", "x": 8, "y": 6, "sprite": "pnj_fillette", "direction": "droite",
             "dialogue": ["Il paraît qu'on peut surfer\njusqu'à l'Île 3 en allant au sud.", "Mais il y a beaucoup de\nPokémon dans l'eau !"],
             "mobile": False}
        ],
        "objets_sol": [
            {"id": "obj_perle_ile2", "x": 3, "y": 11, "item_id": "perle", "ramasse": False},
            {"id": "obj_super_potion_ile2", "x": 12, "y": 6, "item_id": "super_potion", "ramasse": False}
        ],
        "panneaux": [
            {"x": 7, "y": 4, "texte": "ÎLE 2 — CAP DU PARADIS\n— L'île la plus paisible —"}
        ],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# ÎLE 2 — Maisons
# ===========================================================================
def gen_ile2_maison(num):
    W, H = 8, 6
    sol = tile_grid(W, H, 24)
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    set_rect(obj, 0, 0, 7, 0, 25)
    set_rect(obj, 0, 0, 0, 5, 25)
    set_rect(obj, 7, 0, 7, 5, 25)
    set_rect_flat(col, W, 0, 0, 7, 0, 3)
    set_rect_flat(col, W, 0, 0, 0, 5, 3)
    set_rect_flat(col, W, 7, 0, 7, 5, 3)
    
    warp_vers = "maison1_entree" if num == 1 else "maison2_entree"
    pnj_data = []
    if num == 1:
        pnj_data = [{"id": "pnj_ile2_m1", "x": 3, "y": 2, "sprite": "pnj_femme", "direction": "bas",
                      "dialogue": ["Les Îles Sevii sont un paradis\npour les dresseurs.", "Certains Pokémon ne vivent\nqu'ici !"],
                      "mobile": False}]
    else:
        pnj_data = [{"id": "pnj_ile2_m2", "x": 5, "y": 3, "sprite": "pnj_vieil_homme", "direction": "gauche",
                      "dialogue": ["La Forêt Baie sur l'Île 3\nest très dense.", "Beaucoup de dresseurs s'y perdent…"],
                      "mobile": False}]

    return {
        "id": f"sevii_ile2_maison{num}",
        "nom": "Maison",
        "largeur": W, "hauteur": H,
        "tileset": "indoor",
        "musique": "res://assets/audio/music/maison.ogg",
        "connexions": [],
        "warps": [
            {"id": "sortie", "x": 4, "y": 5, "vers_map": "sevii_ile2", "vers_warp": warp_vers, "type": "porte"}
        ],
        "pnj": pnj_data,
        "objets_sol": [],
        "panneaux": [],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# ÎLE 3 — Forêt Baie (zone sauvage principale)
# ===========================================================================
def gen_ile3_foret():
    W, H = 18, 20
    sol = tile_grid(W, H, 0)
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    
    # Bordure arbres denses
    set_border(obj, W, H, 10)
    set_rect_flat(col, W, 0, 0, 17, 0, 3)
    set_rect_flat(col, W, 0, 0, 0, 19, 3)
    set_rect_flat(col, W, 17, 0, 17, 19, 3)
    set_rect_flat(col, W, 0, 19, 17, 19, 3)
    # Arbres épars
    for pos in [(3,3),(5,5),(7,2),(12,4),(14,3),(4,8),(13,8),(6,12),(11,12),(3,15),(14,15),(8,16)]:
        obj[pos[1]][pos[0]] = 10
        col[pos[1]*W+pos[0]] = 3
    # Chemin sinueux
    set_rect(sol, 8, 1, 9, 5, 2)
    set_rect(sol, 5, 5, 8, 6, 2)
    set_rect(sol, 5, 6, 6, 10, 2)
    set_rect(sol, 6, 10, 11, 11, 2)  
    set_rect(sol, 11, 11, 12, 15, 2)
    set_rect(sol, 8, 15, 11, 16, 2)
    set_rect(sol, 8, 16, 9, 18, 2)
    # Hautes herbes (zones d'encounter)
    set_rect(sol, 2, 4, 4, 7, 1)
    set_rect(sol, 10, 2, 13, 5, 1)
    set_rect(sol, 2, 10, 5, 14, 1)
    set_rect(sol, 13, 10, 15, 14, 1)
    set_rect(sol, 7, 13, 10, 15, 1)
    # Point d'eau (petit lac)
    set_rect(sol, 14, 16, 16, 18, 5)
    set_rect_flat(col, W, 14, 16, 16, 18, 2)

    return {
        "id": "sevii_ile3_foret",
        "nom": "Île 3 — Forêt Baie",
        "largeur": W, "hauteur": H,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/sevii_foret.ogg",
        "connexions": [],
        "warps": [
            {"id": "entree_sud", "x": 8, "y": 19, "vers_map": "sevii_ile3", "vers_warp": "foret_sortie", "type": "chemin"}
        ],
        "zones_herbes": [
            {"x1": 2, "y1": 4, "x2": 4, "y2": 7, "table": "sevii_foret"},
            {"x1": 10, "y1": 2, "x2": 13, "y2": 5, "table": "sevii_foret"},
            {"x1": 2, "y1": 10, "x2": 5, "y2": 14, "table": "sevii_foret"},
            {"x1": 13, "y1": 10, "x2": 15, "y2": 14, "table": "sevii_foret"},
            {"x1": 7, "y1": 13, "x2": 10, "y2": 15, "table": "sevii_foret"}
        ],
        "pnj": [
            {"id": "dresseur_foret_01", "x": 3, "y": 6, "sprite": "pnj_insectomane", "direction": "droite",
             "dialogue_avant": "Les Pokémon Insecte de cette\nforêt sont uniques !",
             "dialogue_defaite": "Impressionnant !",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_insectomane_01"},
            {"id": "dresseur_foret_02", "x": 12, "y": 12, "sprite": "pnj_campeur", "direction": "gauche",
             "dialogue_avant": "Je m'entraîne ici tous les jours !",
             "dialogue_defaite": "Tu es trop fort pour moi…",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_campeur_01"},
            {"id": "dresseur_foret_03", "x": 8, "y": 14, "sprite": "pnj_randonneuse", "direction": "bas",
             "dialogue_avant": "Tu es perdu ? Moi aussi !\nCombattons pour passer le temps !",
             "dialogue_defaite": "Au moins j'ai plus\nde patience maintenant !",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_randonneuse_01"}
        ],
        "objets_sol": [
            {"id": "obj_baie_sitrus_ile3", "x": 15, "y": 5, "item_id": "baie_sitrus", "ramasse": False},
            {"id": "obj_hyper_potion_ile3", "x": 3, "y": 12, "item_id": "hyper_potion", "ramasse": False},
            {"id": "obj_ct_mega_sangsue", "x": 9, "y": 8, "item_id": "ct_mega_sangsue", "ramasse": False}
        ],
        "panneaux": [
            {"x": 8, "y": 18, "texte": "FORÊT BAIE\n— Attention Pokémon sauvages ! —"}
        ],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# ÎLE 3 — Village (petite zone d'accès à la forêt)
# ===========================================================================
def gen_ile3():
    W, H = 16, 12
    sol = tile_grid(W, H, 0)
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    
    # Eau en bas
    set_rect(sol, 0, 10, 15, 11, 5)
    set_rect_flat(col, W, 0, 10, 15, 11, 2)
    # Sable
    set_rect(sol, 0, 9, 15, 9, 6)
    # Chemin
    set_rect(sol, 7, 0, 8, 9, 2)
    set_rect(sol, 4, 5, 11, 6, 2)
    # Arbres bordure
    for x in range(W):
        obj[0][x] = 10
        col[0*W+x] = 3
    for y in range(H):
        obj[y][0] = 10 
        obj[y][15] = 10
        col[y*W+0] = 3
        col[y*W+15] = 3
    # Sortie vers forêt en haut
    obj[0][7] = -1
    obj[0][8] = -1
    col[0*W+7] = 0
    col[0*W+8] = 0
    # Bâtiment
    set_rect(obj, 3, 3, 5, 4, 8)
    set_rect_flat(col, W, 3, 3, 5, 4, 3)
    # Herbes
    set_rect(sol, 10, 2, 13, 4, 1)
    set_rect(sol, 10, 7, 13, 8, 1)

    return {
        "id": "sevii_ile3",
        "nom": "Île 3 — Île du Bond",
        "largeur": W, "hauteur": H,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/sevii_ile3.ogg",
        "connexions": [],
        "warps": [
            {"id": "foret_sortie", "x": 7, "y": 0, "vers_map": "sevii_ile3_foret", "vers_warp": "entree_sud", "type": "chemin"},
            {"id": "maison_entree", "x": 4, "y": 5, "vers_map": "sevii_ile3_maison", "vers_warp": "sortie", "type": "porte"}
        ],
        "zones_herbes": [
            {"x1": 10, "y1": 2, "x2": 13, "y2": 4, "table": "sevii_ile3"},
            {"x1": 10, "y1": 7, "x2": 13, "y2": 8, "table": "sevii_ile3"}
        ],
        "pnj": [
            {"id": "pnj_ile3_guide", "x": 6, "y": 5, "sprite": "pnj_homme", "direction": "droite",
             "dialogue": ["La Forêt Baie est au nord.", "Elle est pleine de Pokémon Plante\net Insecte rares !"],
             "mobile": False},
            {"id": "dresseur_ile3_01", "x": 12, "y": 3, "sprite": "pnj_dresseur_m", "direction": "gauche",
             "dialogue_avant": "Hey ! Tu es un dresseur\nde Kanto ?",
             "dialogue_defaite": "Tu es costaud !",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_dresseur_ile3_01"}
        ],
        "objets_sol": [
            {"id": "obj_rappel_ile3", "x": 13, "y": 8, "item_id": "rappel", "ramasse": False}
        ],
        "panneaux": [
            {"x": 7, "y": 4, "texte": "ÎLE 3 — ÎLE DU BOND\n— Vers la Forêt Baie au nord —"}
        ],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# ÎLE 3 — Maison PNJ
# ===========================================================================
def gen_ile3_maison():
    W, H = 8, 6
    sol = tile_grid(W, H, 24)
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    set_rect(obj, 0, 0, 7, 0, 25)
    set_rect(obj, 0, 0, 0, 5, 25)
    set_rect(obj, 7, 0, 7, 5, 25)
    set_rect_flat(col, W, 0, 0, 7, 0, 3)
    set_rect_flat(col, W, 0, 0, 0, 5, 3)
    set_rect_flat(col, W, 7, 0, 7, 5, 3)

    return {
        "id": "sevii_ile3_maison",
        "nom": "Maison",
        "largeur": W, "hauteur": H,
        "tileset": "indoor",
        "musique": "res://assets/audio/music/maison.ogg",
        "connexions": [],
        "warps": [
            {"id": "sortie", "x": 4, "y": 5, "vers_map": "sevii_ile3", "vers_warp": "maison_entree", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_ile3_m1", "x": 3, "y": 2, "sprite": "pnj_homme", "direction": "bas",
             "dialogue": ["Je cherche des Baies rares\ndans la Forêt Baie.", "Si tu en trouves, ça vaut\nle coup de les garder !"],
             "mobile": False}
        ],
        "objets_sol": [
            {"id": "obj_super_repousse_ile3m", "x": 6, "y": 1, "item_id": "super_repousse", "ramasse": False}
        ],
        "panneaux": [],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# Grotte des Braises (extérieur volcan, accès depuis Île 1 nord)
# ===========================================================================
def gen_grotte_braise_ext():
    W, H = 16, 14
    sol = tile_grid(W, H, 4)  # rocheux
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    
    # Bordure rochers
    set_border(obj, W, H, 11)
    set_rect_flat(col, W, 0, 0, 15, 0, 3)
    set_rect_flat(col, W, 0, 0, 0, 13, 3)
    set_rect_flat(col, W, 15, 0, 15, 13, 3)
    set_rect_flat(col, W, 0, 13, 15, 13, 3)
    # Sortie sud vers Île 1
    obj[13][7] = -1
    obj[13][8] = -1
    col[13*W+7] = 0
    col[13*W+8] = 0
    # Chemin
    set_rect(sol, 7, 2, 8, 12, 3)
    set_rect(sol, 4, 6, 11, 7, 3)
    # Herbe volcanique (herbes rares)
    set_rect(sol, 2, 3, 5, 5, 1)
    set_rect(sol, 10, 3, 13, 5, 1)
    set_rect(sol, 2, 9, 5, 11, 1)
    set_rect(sol, 10, 9, 13, 11, 1)
    # Entrée grotte (trou noir)
    obj[2][7] = 12
    obj[2][8] = 12

    return {
        "id": "sevii_grotte_braise_ext",
        "nom": "Sentier des Braises",
        "largeur": W, "hauteur": H,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/sevii_grotte.ogg",
        "connexions": [
            {"direction": "sud", "vers": "sevii_ile1", "decalage": 0}
        ],
        "warps": [
            {"id": "grotte_entree", "x": 7, "y": 2, "vers_map": "sevii_grotte_braise", "vers_warp": "sortie", "type": "grotte"}
        ],
        "zones_herbes": [
            {"x1": 2, "y1": 3, "x2": 5, "y2": 5, "table": "sevii_volcan"},
            {"x1": 10, "y1": 3, "x2": 13, "y2": 5, "table": "sevii_volcan"},
            {"x1": 2, "y1": 9, "x2": 5, "y2": 11, "table": "sevii_volcan"},
            {"x1": 10, "y1": 9, "x2": 13, "y2": 11, "table": "sevii_volcan"}
        ],
        "pnj": [
            {"id": "dresseur_volcan_01", "x": 5, "y": 6, "sprite": "pnj_karateka", "direction": "droite",
             "dialogue_avant": "Le volcan me rend plus fort !",
             "dialogue_defaite": "Aargh ! Trop chaud pour moi !",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_karateka_01"},
            {"id": "dresseur_volcan_02", "x": 10, "y": 10, "sprite": "pnj_montagnard", "direction": "gauche",
             "dialogue_avant": "Seuls les meilleurs arrivent\njusqu'ici !",
             "dialogue_defaite": "Tu mérites d'entrer\ndans la grotte !",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_montagnard_01"}
        ],
        "objets_sol": [
            {"id": "obj_pierre_feu_volcan", "x": 13, "y": 4, "item_id": "pierre_feu", "ramasse": False},
            {"id": "obj_rappel_max_volcan", "x": 3, "y": 10, "item_id": "rappel_max", "ramasse": False}
        ],
        "panneaux": [
            {"x": 7, "y": 5, "texte": "SENTIER DES BRAISES\n— La grotte se trouve au sommet —"}
        ],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# Grotte des Braises (intérieur)
# ===========================================================================
def gen_grotte_braise():
    W, H = 14, 16
    sol = tile_grid(W, H, 4)  # sol rocheux
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 0)
    
    # Murs
    set_border(obj, W, H, 11)
    set_rect_flat(col, W, 0, 0, 13, 0, 3)
    set_rect_flat(col, W, 0, 0, 0, 15, 3)
    set_rect_flat(col, W, 13, 0, 13, 15, 3)
    set_rect_flat(col, W, 0, 15, 13, 15, 3)
    # Sortie en bas
    obj[15][6] = -1
    obj[15][7] = -1
    col[15*W+6] = 0
    col[15*W+7] = 0
    # Chemin principal
    set_rect(sol, 6, 2, 7, 14, 3)
    set_rect(sol, 3, 5, 10, 6, 3)
    set_rect(sol, 3, 10, 10, 11, 3)
    # Rochers obstacles
    for pos in [(4,3),(9,3),(3,8),(10,8),(5,13),(8,13)]:
        obj[pos[1]][pos[0]] = 11
        col[pos[1]*W+pos[0]] = 3
    # Lave (eau chaude → réutilise le type eau pour les graphiques, sera orange)
    set_rect(sol, 1, 1, 3, 3, 5)
    set_rect_flat(col, W, 1, 1, 3, 3, 3)  # pas surfable, juste décoratif et bloqué
    set_rect(sol, 10, 1, 12, 3, 5)
    set_rect_flat(col, W, 10, 1, 12, 3, 3)

    return {
        "id": "sevii_grotte_braise",
        "nom": "Grotte des Braises",
        "largeur": W, "hauteur": H,
        "tileset": "indoor",
        "musique": "res://assets/audio/music/sevii_grotte.ogg",
        "sombre": True,
        "connexions": [],
        "warps": [
            {"id": "sortie", "x": 6, "y": 15, "vers_map": "sevii_grotte_braise_ext", "vers_warp": "grotte_entree", "type": "grotte"}
        ],
        "zones_herbes": [
            {"x1": 3, "y1": 5, "x2": 5, "y2": 6, "table": "sevii_grotte_braise"},
            {"x1": 8, "y1": 5, "x2": 10, "y2": 6, "table": "sevii_grotte_braise"},
            {"x1": 3, "y1": 10, "x2": 5, "y2": 11, "table": "sevii_grotte_braise"},
            {"x1": 8, "y1": 10, "x2": 10, "y2": 11, "table": "sevii_grotte_braise"}
        ],
        "pnj": [
            {"id": "dresseur_grotte_01", "x": 4, "y": 5, "sprite": "pnj_scientifique", "direction": "droite",
             "dialogue_avant": "J'étudie les Pokémon Feu\nde cette grotte.",
             "dialogue_defaite": "Revenez avec des Pokémon Eau\nla prochaine fois !",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_scientifique_01"},
            {"id": "dresseur_grotte_02", "x": 9, "y": 10, "sprite": "pnj_montagnard", "direction": "gauche",
             "dialogue_avant": "La chaleur ne me fait pas peur !",
             "dialogue_defaite": "Bon, peut-être un peu quand même…",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_montagnard_02"}
        ],
        "objets_sol": [
            {"id": "obj_ct_lance_flamme_grotte", "x": 6, "y": 2, "item_id": "ct_lance_flamme", "ramasse": False},
            {"id": "obj_pepite_grotte", "x": 11, "y": 7, "item_id": "pepite", "ramasse": False},
            {"id": "obj_elixir_grotte", "x": 3, "y": 12, "item_id": "elixir", "ramasse": False}
        ],
        "panneaux": [],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }

# ===========================================================================
# Route Marine Sevii (mer entre les îles, surf)
# ===========================================================================
def gen_route_marine():
    W, H = 20, 24
    sol = tile_grid(W, H, 5)  # tout eau
    obj = tile_grid(W, H, -1)
    col = flat_grid(W, H, 2)  # tout surfable
    
    # Petits îlots rocheux
    for iy, ix in [(5,4),(5,5),(12,14),(12,15),(18,8),(18,9)]:
        sol[iy][ix] = 6  # sable
        col[iy*W+ix] = 0
    # Rochers bloquants
    for iy, ix in [(3,9),(8,2),(8,17),(15,6),(15,13),(20,10)]:
        if 0 <= iy < H and 0 <= ix < W:
            obj[iy][ix] = 11
            col[iy*W+ix] = 3

    return {
        "id": "sevii_route_marine",
        "nom": "Route Marine Sevii",
        "largeur": W, "hauteur": H,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/sevii_mer.ogg",
        "connexions": [],
        "warps": [
            {"id": "vers_ile1", "x": 10, "y": 0, "vers_map": "sevii_ile1", "vers_warp": "port_marine", "type": "chemin"},
            {"id": "vers_ile2", "x": 4, "y": 5, "vers_map": "sevii_ile2", "vers_warp": "arrivee_marine", "type": "chemin"},
            {"id": "vers_ile3", "x": 10, "y": 23, "vers_map": "sevii_ile3", "vers_warp": "arrivee_marine", "type": "chemin"}
        ],
        "zones_herbes": [],
        "zones_eau": [
            {"x1": 0, "y1": 0, "x2": 19, "y2": 23, "table": "sevii_mer"}
        ],
        "pnj": [
            {"id": "nageur_sevii_01", "x": 6, "y": 8, "sprite": "pnj_nageur", "direction": "droite",
             "dialogue_avant": "L'eau est bonne !",
             "dialogue_defaite": "Tu nages bien et tu\ncombats bien !",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_nageur_01"},
            {"id": "nageur_sevii_02", "x": 14, "y": 16, "sprite": "pnj_nageuse", "direction": "gauche",
             "dialogue_avant": "Mes Pokémon Eau sont\nimbattables !",
             "dialogue_defaite": "Ah… peut-être pas.",
             "mobile": False, "type": "dresseur", "dresseur_id": "sevii_nageuse_01"}
        ],
        "objets_sol": [
            {"id": "obj_perle_mer", "x": 5, "y": 5, "item_id": "perle", "ramasse": False},
            {"id": "obj_big_perle_mer", "x": 15, "y": 12, "item_id": "grosse_perle", "ramasse": False}
        ],
        "panneaux": [],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": col
    }


# ===========================================================================
# MAIN — Générer toutes les cartes
# ===========================================================================
if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Génération des cartes Îles Sevii...")
    
    maps = [
        ("sevii_ile1.json", gen_ile1()),
        ("sevii_ile1_centre_pokemon.json", gen_ile1_centre()),
        ("sevii_ile1_boutique.json", gen_ile1_boutique()),
        ("sevii_ile1_maison.json", gen_ile1_maison()),
        ("sevii_ile2.json", gen_ile2()),
        ("sevii_ile2_maison1.json", gen_ile2_maison(1)),
        ("sevii_ile2_maison2.json", gen_ile2_maison(2)),
        ("sevii_ile3.json", gen_ile3()),
        ("sevii_ile3_foret.json", gen_ile3_foret()),
        ("sevii_ile3_maison.json", gen_ile3_maison()),
        ("sevii_grotte_braise_ext.json", gen_grotte_braise_ext()),
        ("sevii_grotte_braise.json", gen_grotte_braise()),
        ("sevii_route_marine.json", gen_route_marine()),
    ]
    
    for filename, data in maps:
        write_map(filename, data)
    
    print(f"\n✓ {len(maps)} cartes Sevii générées !")
