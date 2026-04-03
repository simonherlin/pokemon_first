#!/usr/bin/env python3
"""
Générateur de cartes RFVF — Pokémon Rouge/Bleu HD
Crée Bourg Palette, Route 1 et Jadielle avec des layouts fidèles à FRLG.

Utilise les indices du tileset 16 colonnes (tileset_builder.gd RFVF).
"""

import json
import os
import copy

# =============================================================================
#  CONSTANTES TILES (identiques à tileset_builder.gd)
# =============================================================================

# --- Ligne 0 : Sols ---
HERBE     = 0
HERBE_V   = 1   # variante (plus sombre)
FLEURS    = 2
HERBE_H   = 3   # herbe haute (rencontres)
CHEMIN    = 4
CH_H      = 5   # bord haut
CH_B      = 6   # bord bas
CH_G      = 7   # bord gauche
CH_D      = 8   # bord droit
CH_CHG    = 9   # coin haut-gauche (extérieur)
CH_CHD    = 10   # coin haut-droit
CH_CBG    = 11   # coin bas-gauche
CH_CBD    = 12   # coin bas-droit
CH_CIHG   = 13   # coin intérieur haut-gauche
CH_CIHD   = 14
SABLE     = 15

# --- Ligne 1 : Eau ---
EAU       = 16
EAU_RH    = 17   # rivage haut (terre au-dessus)
EAU_RB    = 18
EAU_RG    = 19   # rivage gauche (terre à gauche)
EAU_RD    = 20
EAU_CHG   = 21   # coin extérieur haut-gauche
EAU_CHD   = 22
EAU_CBG   = 23
EAU_CBD   = 24
EAU_CIHG  = 25   # coin intérieur
EAU_CIHD  = 26
EAU_CIBG  = 27
EAU_CIBD  = 28
CH_CIBG   = 29
CH_CIBD   = 30

# --- Ligne 2 : Arbres / obstacles ---
ARB_HG    = 32
ARB_HD    = 33
ARB_BG    = 34
ARB_BD    = 35
BUISSON   = 36
P_ARBRE   = 37   # petit arbre (coupable)
ROCHER    = 38
CLOT_H    = 39   # clôture horizontale
CLOT_V    = 40   # clôture verticale
PANNEAU   = 41
BOITE     = 42   # boîte aux lettres
REBORD_H  = 43
REBORD_G  = 44
REBORD_D  = 45

# --- Ligne 3 : Maisons (toit rouge) ---
M_TG = 48;  M_TM = 49;  M_TD = 50
M_BG = 51;  M_BM = 52;  M_BD = 53
M_WG = 54;  M_WM = 55;  M_WD = 56
M_WF = 57;  M_WP = 58

# --- Ligne 4 : Labo (toit bleu) ---
L_TG = 64;  L_TM = 65;  L_TD = 66
L_BG = 67;  L_BM = 68;  L_BD = 69
L_WG = 70;  L_WM = 71;  L_WD = 72
L_WF = 73;  L_WP = 74

# --- Ligne 5 : Centre Pokémon + Boutique ---
C_TG = 80;  C_TM = 81;  C_TD = 82
C_WG = 83;  C_WP = 84;  C_WD = 85
B_TG = 86;  B_TM = 87;  B_TD = 88
B_WG = 89;  B_WP = 90;  B_WD = 91
A_SOL = 92; A_STATUE = 93

N = -1  # néant (objets layer)

# =============================================================================
#  FONCTIONS UTILITAIRES
# =============================================================================

def grid(w, h, fill=0):
    """Crée une grille 2D [h][w] remplie de fill."""
    return [[fill] * w for _ in range(h)]


def place_tree(obj, x, y):
    """Place un arbre 2×2 (HG/HD sur y, BG/BD sur y+1)."""
    obj[y][x]     = ARB_HG;  obj[y][x+1]   = ARB_HD
    obj[y+1][x]   = ARB_BG;  obj[y+1][x+1] = ARB_BD


def fill_tree_row(obj, y, x_start, x_end):
    """Remplit un bandeau horizontal d'arbres (2 lignes : y et y+1)."""
    for x in range(x_start, x_end, 2):
        if x + 1 < len(obj[0]):
            place_tree(obj, x, y)


def place_house(obj, x, y):
    """Maison toit rouge — 4 large × 4 haut. Porte à (x+2, y+3)."""
    obj[y][x]     = M_TG; obj[y][x+1]   = M_TM; obj[y][x+2]   = M_TM; obj[y][x+3] = M_TD
    obj[y+1][x]   = M_BG; obj[y+1][x+1] = M_BM; obj[y+1][x+2] = M_BM; obj[y+1][x+3] = M_BD
    obj[y+2][x]   = M_WG; obj[y+2][x+1] = M_WF; obj[y+2][x+2] = M_WM; obj[y+2][x+3] = M_WD
    obj[y+3][x]   = M_WG; obj[y+3][x+1] = M_WM; obj[y+3][x+2] = M_WP; obj[y+3][x+3] = M_WD


def place_lab(obj, x, y):
    """Labo Prof. Chen — 4 large × 4 haut. Porte à (x+2, y+3)."""
    obj[y][x]     = L_TG; obj[y][x+1]   = L_TM; obj[y][x+2]   = L_TM; obj[y][x+3] = L_TD
    obj[y+1][x]   = L_BG; obj[y+1][x+1] = L_BM; obj[y+1][x+2] = L_BM; obj[y+1][x+3] = L_BD
    obj[y+2][x]   = L_WG; obj[y+2][x+1] = L_WF; obj[y+2][x+2] = L_WM; obj[y+2][x+3] = L_WD
    obj[y+3][x]   = L_WG; obj[y+3][x+1] = L_WM; obj[y+3][x+2] = L_WP; obj[y+3][x+3] = L_WD


def place_pokecenter(obj, x, y):
    """Centre Pokémon — 3 large × 2 haut. Porte à (x+1, y+1)."""
    obj[y][x]     = C_TG; obj[y][x+1]   = C_TM; obj[y][x+2]   = C_TD
    obj[y+1][x]   = C_WG; obj[y+1][x+1] = C_WP; obj[y+1][x+2] = C_WD


def place_boutique(obj, x, y):
    """Boutique Pokémon — 3 large × 2 haut. Porte à (x+1, y+1)."""
    obj[y][x]     = B_TG; obj[y][x+1]   = B_TM; obj[y][x+2]   = B_TD
    obj[y+1][x]   = B_WG; obj[y+1][x+1] = B_WP; obj[y+1][x+2] = B_WD


def build_path_from_mask(path_mask, w, h, base_sol=None):
    """
    Convertit un masque booléen de chemin en tiles avec bords.
    path_mask[y][x] = True si chemin.
    Retourne une grille sol avec les bons tiles.
    """
    sol = base_sol if base_sol else grid(w, h, HERBE)

    for y in range(h):
        for x in range(w):
            if not path_mask[y][x]:
                continue

            # Voisins directs
            n = path_mask[y-1][x] if y > 0 else False
            s = path_mask[y+1][x] if y < h-1 else False
            west = path_mask[y][x-1] if x > 0 else False
            east = path_mask[y][x+1] if x < w-1 else False

            # Diagonales (pour coins intérieurs)
            nw = path_mask[y-1][x-1] if y > 0 and x > 0 else False
            ne = path_mask[y-1][x+1] if y > 0 and x < w-1 else False
            sw = path_mask[y+1][x-1] if y < h-1 and x > 0 else False
            se = path_mask[y+1][x+1] if y < h-1 and x < w-1 else False

            # Coins extérieurs (deux côtés non-chemin)
            if not n and not west:
                sol[y][x] = CH_CHG
            elif not n and not east:
                sol[y][x] = CH_CHD
            elif not s and not west:
                sol[y][x] = CH_CBG
            elif not s and not east:
                sol[y][x] = CH_CBD
            # Bords simples (un seul côté non-chemin)
            elif not n:
                sol[y][x] = CH_H
            elif not s:
                sol[y][x] = CH_B
            elif not west:
                sol[y][x] = CH_G
            elif not east:
                sol[y][x] = CH_D
            # Centre ou coin intérieur
            elif n and s and west and east:
                if not nw:
                    sol[y][x] = CH_CIHG
                elif not ne:
                    sol[y][x] = CH_CIHD
                elif not sw:
                    sol[y][x] = CH_CIBG
                elif not se:
                    sol[y][x] = CH_CIBD
                else:
                    sol[y][x] = CHEMIN
            else:
                sol[y][x] = CHEMIN

    return sol


def build_water_from_mask(water_mask, w, h, sol):
    """
    Applique les tiles eau avec rivages sur une grille sol existante.
    water_mask[y][x] = True si eau.
    """
    for y in range(h):
        for x in range(w):
            if not water_mask[y][x]:
                continue

            # Voisins
            n = water_mask[y-1][x] if y > 0 else True
            s = water_mask[y+1][x] if y < h-1 else True
            west = water_mask[y][x-1] if x > 0 else True
            east = water_mask[y][x+1] if x < w-1 else True
            nw = water_mask[y-1][x-1] if y > 0 and x > 0 else True
            ne = water_mask[y-1][x+1] if y > 0 and x < w-1 else True
            sw = water_mask[y+1][x-1] if y < h-1 and x > 0 else True
            se = water_mask[y+1][x+1] if y < h-1 and x < w-1 else True

            # Coins extérieurs
            if not n and not west:
                sol[y][x] = EAU_CHG
            elif not n and not east:
                sol[y][x] = EAU_CHD
            elif not s and not west:
                sol[y][x] = EAU_CBG
            elif not s and not east:
                sol[y][x] = EAU_CBD
            elif not n:
                sol[y][x] = EAU_RH
            elif not s:
                sol[y][x] = EAU_RB
            elif not west:
                sol[y][x] = EAU_RG
            elif not east:
                sol[y][x] = EAU_RD
            elif not nw:
                sol[y][x] = EAU_CIHG
            elif not ne:
                sol[y][x] = EAU_CIHD
            elif not sw:
                sol[y][x] = EAU_CIBG
            elif not se:
                sol[y][x] = EAU_CIBD
            else:
                sol[y][x] = EAU

    return sol


def scatter_decoration(sol, positions, tile_id):
    """Place un tile décoratif aux positions données."""
    for (x, y) in positions:
        sol[y][x] = tile_id


def flat_tile_data(w, h, sol, objets):
    """Génère tile_data plat : 0=libre, 2=chemin, 3=bloqué."""
    blocking_objets = {
        ARB_HG, ARB_HD, ARB_BG, ARB_BD, BUISSON, P_ARBRE, ROCHER,
        CLOT_H, CLOT_V, PANNEAU, BOITE, REBORD_H,
        M_TG, M_TM, M_TD, M_BG, M_BM, M_BD,
        M_WG, M_WM, M_WD, M_WF,
        L_TG, L_TM, L_TD, L_BG, L_BM, L_BD,
        L_WG, L_WM, L_WD, L_WF,
        C_TG, C_TM, C_TD, C_WG, C_WD,
        B_TG, B_TM, B_TD, B_WG, B_WD,
        A_STATUE,
    }
    blocking_sol = {EAU, EAU_RH, EAU_RB, EAU_RG, EAU_RD,
                    EAU_CHG, EAU_CHD, EAU_CBG, EAU_CBD,
                    EAU_CIHG, EAU_CIHD, EAU_CIBG, EAU_CIBD}
    path_tiles = {CHEMIN, CH_H, CH_B, CH_G, CH_D,
                  CH_CHG, CH_CHD, CH_CBG, CH_CBD,
                  CH_CIHG, CH_CIHD, CH_CIBG, CH_CIBD}

    data = []
    for y in range(h):
        for x in range(w):
            obj_t = objets[y][x] if y < len(objets) and x < len(objets[0]) else -1
            sol_t = sol[y][x]
            if obj_t in blocking_objets or sol_t in blocking_sol:
                data.append(3)
            elif sol_t in path_tiles:
                data.append(2)
            else:
                data.append(0)
    return data


# =============================================================================
#  BOURG PALETTE  (20×18) — Fidèle à FRLG
# =============================================================================

def create_bourg_palette():
    W, H = 20, 18
    sol = grid(W, H, HERBE)
    obj = grid(W, H, N)

    # --- Chemins ---
    path = [[False]*W for _ in range(H)]

    # Chemin principal vertical (cols 9-10, de y=0 à y=15)
    for y in range(0, 16):
        path[y][9] = True
        path[y][10] = True

    # Branche horizontale vers maison joueur (y=7, cols 5→9)
    for x in range(5, 11):
        path[7][x] = True
        path[8][x] = True

    # Branche horizontale vers maison rival (y=7, cols 10→14)
    for x in range(10, 15):
        path[7][x] = True
        path[8][x] = True

    # Branche horizontale vers labo (y=13, cols 8→11)
    for x in range(8, 12):
        path[13][x] = True

    # Zone devant le labo
    path[14][9] = True
    path[14][10] = True

    # Sortie nord élargie
    for y in range(0, 2):
        for x in range(8, 12):
            path[y][x] = True

    sol = build_path_from_mask(path, W, H, sol)

    # --- Eau (sud) ---
    water = [[False]*W for _ in range(H)]
    for x in range(W):
        water[17][x] = True
        if x < 8 or x > 11:  # Pas de water devant la sortie sud
            water[16][x] = True

    sol = build_water_from_mask(water, W, H, sol)

    # --- Sable devant l'eau ---
    for x in range(W):
        if sol[15][x] == HERBE and (x < 8 or x > 11):
            sol[15][x] = SABLE

    # --- Fleurs décoratives ---
    flower_spots = [(3, 2), (16, 2), (2, 9), (17, 9), (4, 14), (15, 14)]
    for (x, y) in flower_spots:
        if sol[y][x] == HERBE:
            sol[y][x] = FLEURS

    # Variantes d'herbe
    variant_spots = [(5, 2), (14, 2), (3, 10), (16, 10), (6, 15), (13, 15)]
    for (x, y) in variant_spots:
        if sol[y][x] == HERBE:
            sol[y][x] = HERBE_V

    # --- Arbres bordure ---
    # Rangée du haut (rows 0-1), colonnes 0-7 et 12-19
    for x in range(0, 8, 2):
        place_tree(obj, x, 0)
    for x in range(12, 20, 2):
        place_tree(obj, x, 0)

    # Côtés gauche (colonnes 0-1)
    for y in range(2, 16, 2):
        place_tree(obj, 0, y)

    # Côtés droit (colonnes 18-19)
    for y in range(2, 16, 2):
        place_tree(obj, 18, y)

    # Quelques arbres supplémentaires pour encadrer
    place_tree(obj, 2, 2)
    place_tree(obj, 16, 2)
    place_tree(obj, 2, 10)
    place_tree(obj, 16, 10)

    # --- Bâtiments ---
    # Maison du joueur : cols 3-6, rows 3-6 (porte à x=5, y=6)
    place_house(obj, 3, 3)

    # Maison du rival : cols 12-15, rows 3-6 (porte à x=14, y=6)
    place_house(obj, 12, 3)

    # Laboratoire du Prof. Chen : cols 8-11, rows 10-13 (porte à x=10, y=13)
    place_lab(obj, 8, 10)

    # --- Éléments décoratifs ---
    # Boîtes aux lettres devant les maisons
    obj[7][7] = BOITE     # devant maison joueur
    obj[7][16] = BOITE    # devant maison rival

    # Panneau de la ville
    obj[8][12] = PANNEAU

    # Clôtures décoratives entre les maisons et le chemin
    # Petite clôture côté joueur
    obj[9][3] = CLOT_H
    obj[9][4] = CLOT_H

    # Petite clôture côté rival
    obj[9][15] = CLOT_H
    obj[9][16] = CLOT_H

    # --- tile_data ---
    td = flat_tile_data(W, H, sol, obj)

    return {
        "id": "bourg_palette",
        "nom": "Bourg Palette",
        "largeur": W,
        "hauteur": H,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/bourg_palette.ogg",
        "connexions": [
            {"direction": "nord", "vers": "route_1", "decalage": 0},
            {"direction": "sud", "vers": "route_21", "decalage": 0}
        ],
        "warps": [
            {
                "id": "maison_joueur_entree",
                "x": 5, "y": 7,
                "vers_map": "maison_joueur",
                "vers_warp": "sortie",
                "type": "porte"
            },
            {
                "id": "maison_rival_entree",
                "x": 14, "y": 7,
                "vers_map": "maison_rival",
                "vers_warp": "sortie",
                "type": "porte"
            },
            {
                "id": "laboratoire_entree",
                "x": 10, "y": 14,
                "vers_map": "laboratoire_chen",
                "vers_warp": "sortie",
                "type": "porte"
            }
        ],
        "pnj": [
            {
                "id": "pnj_homme_01",
                "x": 6, "y": 9,
                "sprite": "pnj_homme",
                "direction": "bas",
                "dialogue": [
                    "Bourg Palette. Une petite ville tranquille.",
                    "D'ici partent de grands aventuriers !"
                ],
                "dialogue_conditions": [
                    {
                        "flag": "champion_ligue_battu",
                        "valeur": True,
                        "dialogue": [
                            "Tu es le nouveau Maître\nPokémon ?!",
                            "Bourg Palette est fière de toi !"
                        ]
                    }
                ],
                "mobile": False
            },
            {
                "id": "pnj_femme_01",
                "x": 15, "y": 5,
                "sprite": "pnj_femme",
                "direction": "gauche",
                "dialogue": [
                    "Les Pokémon sauvages vivent dans les hautes herbes.",
                    "Ne t'aventure pas sans les tiens !"
                ],
                "mobile": False
            }
        ],
        "objets_sol": [],
        "panneaux": [
            {
                "x": 12, "y": 9,
                "texte": "BOURG PALETTE\n— Une ville aux bords de l'aventure —"
            }
        ],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": td
    }


# =============================================================================
#  ROUTE 1  (20×30) — Fidèle à FRLG
# =============================================================================

def create_route_1():
    W, H = 20, 30
    sol = grid(W, H, HERBE)
    obj = grid(W, H, N)

    # --- Chemin sinueux ---
    path = [[False]*W for _ in range(H)]

    # Partie sud : chemin central (cols 9-10)  y=28-29 (entrée depuis bourg palette)
    for y in range(25, 30):
        path[y][9] = True
        path[y][10] = True

    # Le chemin remonte en biais vers la gauche (y=20-24)
    for y in range(20, 25):
        path[y][7] = True
        path[y][8] = True
    # Transition de 9-10 à 7-8
    path[24][9] = True
    path[24][8] = True
    path[25][8] = True

    # Section milieu : chemin va vers la droite (y=14-19)
    for y in range(14, 20):
        path[y][10] = True
        path[y][11] = True
    # Transition de 7-8 à 10-11
    path[19][9] = True
    path[19][10] = True
    path[20][9] = True
    path[20][10] = True

    # Section haute : chemin revient au centre (y=5-13)
    for y in range(5, 14):
        path[y][9] = True
        path[y][10] = True
    # Transition
    path[13][10] = True
    path[13][11] = True

    # Sortie nord (y=0-4)
    for y in range(0, 5):
        path[y][9] = True
        path[y][10] = True

    # Élargissement à certains endroits pour rendre naturel
    for y in range(0, 2):
        path[y][8] = True
        path[y][11] = True

    sol = build_path_from_mask(path, W, H, sol)

    # --- Herbes hautes (zones de rencontres) ---
    # Zone 1 : côté droit, y=22-27, x=12-16
    for y in range(22, 28):
        for x in range(12, 17):
            if sol[y][x] == HERBE:
                sol[y][x] = HERBE_H

    # Zone 2 : côté gauche, y=8-13, x=3-7
    for y in range(8, 14):
        for x in range(3, 7):
            if sol[y][x] == HERBE:
                sol[y][x] = HERBE_H

    # Zone 3 : côté droit haut, y=3-7, x=13-16
    for y in range(3, 8):
        for x in range(13, 17):
            if sol[y][x] == HERBE:
                sol[y][x] = HERBE_H

    # --- Rebords (ledges) ---
    # Rebord descendant à y=12, x=12-15 (saut vers le bas)
    for x in range(12, 16):
        obj[18][x] = REBORD_H

    # Rebord descendant y=22, x=3-6
    for x in range(3, 7):
        obj[21][x] = REBORD_H

    # --- Arbres bordure ---
    # Côté gauche (cols 0-1)
    for y in range(0, 30, 2):
        place_tree(obj, 0, y)

    # Côté droit (cols 18-19)
    for y in range(0, 30, 2):
        place_tree(obj, 18, y)

    # Arbres supplémentaires pour variété
    # Bloc d'arbres côté gauche haut
    for y in range(0, 8, 2):
        place_tree(obj, 2, y)

    # Bloc d'arbres côté droit bas
    for y in range(14, 22, 2):
        place_tree(obj, 16, y)

    # Quelques arbres isolés pour casser la monotonie
    place_tree(obj, 2, 16)
    place_tree(obj, 2, 20)
    place_tree(obj, 16, 4)
    place_tree(obj, 16, 8)
    place_tree(obj, 4, 16)
    place_tree(obj, 14, 26)

    # Rangée du haut (entrée jadielle)
    for x in range(0, 8, 2):
        place_tree(obj, x, 0)
    for x in range(12, 20, 2):
        place_tree(obj, x, 0)

    # Rangée du bas (entrée bourg palette)
    for x in range(0, 8, 2):
        place_tree(obj, x, 28)
    for x in range(12, 20, 2):
        place_tree(obj, x, 28)

    # --- Fleurs et variantes ---
    flower_spots = [(8, 6), (12, 10), (5, 20), (14, 15), (3, 28), (17, 3)]
    for (x, y) in flower_spots:
        if 0 <= y < H and 0 <= x < W and sol[y][x] == HERBE:
            sol[y][x] = FLEURS

    variant_spots = [(7, 15), (11, 22), (4, 5), (15, 25), (8, 19)]
    for (x, y) in variant_spots:
        if 0 <= y < H and 0 <= x < W and sol[y][x] == HERBE:
            sol[y][x] = HERBE_V

    # --- Panneau ---
    obj[3][8] = PANNEAU  # panneau route 1

    # --- tile_data ---
    td = flat_tile_data(W, H, sol, obj)

    return {
        "id": "route_1",
        "nom": "Route 1",
        "largeur": W,
        "hauteur": H,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/route_1.ogg",
        "connexions": [
            {"direction": "sud", "vers": "bourg_palette", "decalage": 0},
            {"direction": "nord", "vers": "jadielle_ville", "decalage": 0}
        ],
        "warps": [],
        "pnj": [
            {
                "id": "pnj_vendeur",
                "x": 8, "y": 15,
                "sprite": "pnj_homme",
                "direction": "gauche",
                "dialogue": [
                    "Salut ! Tu vas à Jadielle ?",
                    "Les Pokémon sauvages se cachent\ndans les hautes herbes !"
                ],
                "mobile": False
            }
        ],
        "objets_sol": [],
        "panneaux": [
            {
                "x": 8, "y": 4,
                "texte": "ROUTE 1\nBourg Palette — Jadielle"
            }
        ],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": td
    }


# =============================================================================
#  JADIELLE  (20×20) — Fidèle à FRLG
# =============================================================================

def create_jadielle():
    W, H = 20, 20
    sol = grid(W, H, HERBE)
    obj = grid(W, H, N)

    # --- Chemins ---
    path = [[False]*W for _ in range(H)]

    # Axe vertical principal (cols 9-10) de y=0 à y=19
    for y in range(0, 20):
        path[y][9] = True
        path[y][10] = True

    # Branche horizontale haute vers Centre Pokémon (y=5-6, x=3→9)
    for x in range(3, 11):
        path[5][x] = True
        path[6][x] = True

    # Branche horizontale haute vers Boutique (y=5-6, x=10→16)
    for x in range(10, 17):
        path[5][x] = True
        path[6][x] = True

    # Branche horizontale vers arène (y=13-14, x=3→9)
    for x in range(3, 11):
        path[13][x] = True
        path[14][x] = True

    # Branche horizontale vers sortie ouest (y=13-14, x=0→3)
    for x in range(0, 4):
        path[13][x] = True
        path[14][x] = True

    # Chemin sortie nord élargi
    for y in range(0, 2):
        for x in range(8, 12):
            path[y][x] = True

    # Chemin sortie sud élargi
    for y in range(18, 20):
        for x in range(8, 12):
            path[y][x] = True

    sol = build_path_from_mask(path, W, H, sol)

    # --- Arbres bordure ---
    # Haut (rows 0-1) — gap pour sortie nord
    for x in range(0, 8, 2):
        place_tree(obj, x, 0)
    for x in range(12, 20, 2):
        place_tree(obj, x, 0)

    # Bas (rows 18-19) — gap pour sortie sud
    for x in range(0, 8, 2):
        place_tree(obj, x, 18)
    for x in range(12, 20, 2):
        place_tree(obj, x, 18)

    # Côté gauche
    for y in range(2, 12, 2):
        place_tree(obj, 0, y)
    for y in range(16, 18, 2):
        place_tree(obj, 0, y)

    # Côté droit
    for y in range(2, 18, 2):
        place_tree(obj, 18, y)

    # Arbres intérieurs — séparation zones
    place_tree(obj, 2, 2)
    place_tree(obj, 16, 2)
    place_tree(obj, 2, 8)
    place_tree(obj, 16, 8)
    place_tree(obj, 2, 16)
    place_tree(obj, 16, 16)

    # Arbres autour de l'arène
    place_tree(obj, 2, 10)
    place_tree(obj, 6, 10)
    place_tree(obj, 6, 16)

    # --- Bâtiments ---
    # Centre Pokémon : cols 3-5, rows 3-4 (porte à x=4, y=4)
    place_pokecenter(obj, 3, 3)

    # Boutique : cols 13-15, rows 3-4 (porte à x=14, y=4)
    place_boutique(obj, 13, 3)

    # Arène de Jadielle : représentée par un bâtiment spécial
    # On utilise une maison mais avec des statues pour marquer l'arène
    place_house(obj, 3, 10)
    # Statues d'arène de chaque côté de la porte
    obj[14][3] = A_STATUE
    obj[14][7] = A_STATUE

    # --- Éléments décoratifs ---
    # Panneau ville
    obj[7][12] = PANNEAU

    # Panneau arène
    obj[14][8] = PANNEAU

    # Clôtures décoratives
    for x in range(12, 17):
        obj[7][x] = CLOT_H

    # Fleurs
    flower_spots = [(5, 8), (14, 8), (11, 16), (17, 4), (8, 16)]
    for (x, y) in flower_spots:
        if 0 <= y < H and 0 <= x < W and sol[y][x] == HERBE:
            sol[y][x] = FLEURS

    # Variantes d'herbe
    variant_spots = [(7, 2), (12, 2), (5, 16), (14, 16), (17, 12)]
    for (x, y) in variant_spots:
        if 0 <= y < H and 0 <= x < W and sol[y][x] == HERBE:
            sol[y][x] = HERBE_V

    # --- tile_data ---
    td = flat_tile_data(W, H, sol, obj)

    return {
        "id": "jadielle_ville",
        "nom": "Jadielle",
        "largeur": W,
        "hauteur": H,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/jadielle.ogg",
        "connexions": [
            {"direction": "sud", "vers": "route_1", "decalage": 0},
            {"direction": "nord", "vers": "route_2", "decalage": 0},
            {"direction": "ouest", "vers": "route_22", "decalage": 0}
        ],
        "warps": [
            {
                "id": "centre_pokemon_entree",
                "x": 4, "y": 5,
                "vers_map": "centre_pokemon_jadielle",
                "vers_warp": "sortie",
                "type": "porte"
            },
            {
                "id": "boutique_entree",
                "x": 14, "y": 5,
                "vers_map": "boutique_jadielle",
                "vers_warp": "sortie",
                "type": "porte"
            },
            {
                "id": "arene_entree",
                "x": 5, "y": 14,
                "vers_map": "arene_jadielle",
                "vers_warp": "sortie",
                "type": "porte",
                "condition": {
                    "type": "badges",
                    "nombre": 7,
                    "message_refus": "L'arène est fermée.\nTu as besoin de 7 Badges pour entrer."
                }
            }
        ],
        "pnj": [
            {
                "id": "pnj_vieux_01",
                "x": 11, "y": 9,
                "sprite": "pnj_vieux",
                "direction": "bas",
                "dialogue": [
                    "Jadielle est une ville paisible,\nau carrefour de plusieurs routes.",
                    "Le Champion d'Arène ici est\ntrès mystérieux…"
                ],
                "dialogue_conditions": [
                    {
                        "flag": "a_badge_7",
                        "valeur": True,
                        "dialogue": [
                            "L'arène a enfin ouvert !",
                            "Le Champion est incroyablement\npuissant. Bonne chance !"
                        ]
                    }
                ],
                "mobile": False
            },
            {
                "id": "pnj_femme_02",
                "x": 15, "y": 15,
                "sprite": "pnj_femme",
                "direction": "gauche",
                "dialogue": [
                    "La boutique vend toutes sortes\nd'objets utiles aux dresseurs.",
                    "N'oublie pas de t'équiper !"
                ],
                "mobile": False
            },
            {
                "id": "pnj_homme_02",
                "x": 3, "y": 7,
                "sprite": "pnj_homme",
                "direction": "droite",
                "dialogue": [
                    "Le Centre Pokémon soigne tes\nPokémon gratuitement !",
                    "N'hésite pas à y passer souvent."
                ],
                "mobile": False
            }
        ],
        "objets_sol": [],
        "panneaux": [
            {
                "x": 12, "y": 8,
                "texte": "JADIELLE\n— La ville éternellement verte —"
            },
            {
                "x": 8, "y": 15,
                "texte": "ARÈNE DE JADIELLE\nChampion : ???"
            }
        ],
        "tiles_sol": sol,
        "tiles_objets": obj,
        "tile_data": td
    }


# =============================================================================
#  MIGRATION DES CARTES INTÉRIEURES — ancien → nouveau indices
# =============================================================================

# Table de correspondance ancien index → nouveau index
OLD_TO_NEW = {
    0: HERBE,          # herbe → herbe
    1: HERBE_H,        # herbe_haute → herbe_haute
    2: CHEMIN,          # chemin → chemin
    3: SABLE,           # sable → sable
    4: EAU,             # eau → eau
    5: FLEURS,          # fleur → herbe_fleurs
    6: HERBE,           # (inutilisé) → herbe
    7: HERBE,           # (inutilisé)
    8: ARB_HG,          # arbre_haut_L → arbre_hg
    9: ARB_BG,          # arbre_bas_L → arbre_bg
    10: ARB_HD,         # arbre_haut_R → arbre_hd
    11: ARB_BD,         # arbre_bas_R → arbre_bd
    12: CLOT_H,         # fence_h → cloture_h
    13: CLOT_V,         # fence_v → cloture_v
    14: BUISSON,        # buisson → buisson
    15: HERBE_V,        # herbe_detail → herbe_variante
    16: M_TG,           # toit_G → maison_toit_hg
    17: M_TM,           # toit_M → maison_toit_hm
    18: M_TD,           # toit_D → maison_toit_hd
    19: M_WG,           # mur_G → maison_mur_g
    20: M_WM,           # mur_M → maison_mur_m
    21: M_WD,           # mur_D → maison_mur_d
    22: M_WP,           # porte → maison_porte
    23: M_WF,           # fenetre → maison_fenetre
    # Intérieurs (24-47 → 96-119)
    24: 96,   # sol_interieur → sol_int
    25: 97,   # mur_interieur → mur_int
    26: 98,   # comptoir → comptoir
    27: 99,   # machine_soin → machine_soin
    28: 100,  # etagere → etagere
    29: 101,  # tapis → tapis
    30: 102,  # sol_carrelage → sol_carrelage
    31: 103,  # mur_motif → mur_motif
    32: 104,  # lit_tete → lit_tete
    33: 105,  # lit_pied → lit_pied
    34: 106,  # tv → tv
    35: 107,  # pc → pc
    36: 108,  # plante_int → plante
    37: 109,  # escalier_up → escalier_up
    38: 110,  # escalier_down → escalier_down
    39: 111,  # paillasson → paillasson
    40: 112,  # porte_int → porte_int
    41: 113,  # fenetre_int → fenetre_int
    42: 114,  # sol_bois_fonce → sol_bois_fonce
    43: 115,  # mur_ext_fenetre → mur_ext_fenetre
    44: 116,  # table → table
    45: 117,  # chaise → chaise
    46: 118,  # poster → poster
    47: 119,  # poubelle → poubelle
}

def migrate_tile(index):
    """Convertit un ancien index en nouveau."""
    if index < 0:
        return index
    return OLD_TO_NEW.get(index, index)


def migrate_map_file(filepath):
    """Migre les tiles d'un fichier carte vers les nouveaux indices."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changed = False
    for layer in ('tiles_sol', 'tiles_objets'):
        if layer in data:
            for y, row in enumerate(data[layer]):
                for x, val in enumerate(row):
                    new_val = migrate_tile(val)
                    if new_val != val:
                        data[layer][y][x] = new_val
                        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Migré : {os.path.basename(filepath)}")
    else:
        print(f"  · Aucun changement : {os.path.basename(filepath)}")


# =============================================================================
#  MAIN
# =============================================================================

def save_map(map_data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(map_data, f, indent=2, ensure_ascii=False)
    print(f"✓ Sauvegardé : {filepath}")
    print(f"  Taille : {map_data['largeur']}×{map_data['hauteur']}")


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    maps_dir = os.path.join(base, 'data', 'maps')

    print("=" * 60)
    print("  Générateur de cartes RFVF — Pokémon Rouge/Bleu HD")
    print("=" * 60)
    print()

    # --- Générer les 3 cartes principales ---
    print("--- Génération des cartes principales ---")

    bp = create_bourg_palette()
    save_map(bp, os.path.join(maps_dir, 'bourg_palette.json'))

    r1 = create_route_1()
    save_map(r1, os.path.join(maps_dir, 'route_1.json'))

    jv = create_jadielle()
    save_map(jv, os.path.join(maps_dir, 'jadielle_ville.json'))

    print()

    # --- Migrer toutes les autres cartes ---
    print("--- Migration des autres cartes (ancien → nouveau indices) ---")

    skip = {'bourg_palette.json', 'route_1.json', 'jadielle_ville.json'}
    for fname in sorted(os.listdir(maps_dir)):
        if fname.endswith('.json') and fname not in skip:
            migrate_map_file(os.path.join(maps_dir, fname))

    print()
    print("✓ Terminé !")


if __name__ == '__main__':
    main()
