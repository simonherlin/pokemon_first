#!/usr/bin/env python3
"""
Reconstruction des cartes de Kanto pour correspondre fidèlement au layout FRLG.
Chaque carte est reconstruite tile par tile avec notre système de tiles.

Système de tiles :
  Sol (ground layer):
    0=HERBE  1=HERBE_VAR  2=HERBE_FLEURS  3=HERBE_HAUTE
    4=CHEMIN  5=CH_BORD_H  6=CH_BORD_B  7=CH_BORD_G  8=CH_BORD_D
    9=CH_COIN_HG  10=CH_COIN_HD  11=CH_COIN_BG  12=CH_COIN_BD
    13=CH_COIN_INT_HG  14=CH_COIN_INT_HD
    15=SABLE
    16=EAU  17=EAU_RIV_H  18=EAU_RIV_B  19=EAU_RIV_G  20=EAU_RIV_D
    21=EAU_COIN_HG  22=EAU_COIN_HD  23=EAU_COIN_BG  24=EAU_COIN_BD
    25=EAU_COIN_INT_HG  26=EAU_COIN_INT_HD  27=EAU_COIN_INT_BG  28=EAU_COIN_INT_BD
    29=CH_COIN_INT_BG  30=CH_COIN_INT_BD

  Objets (object layer, -1 = vide):
    32=ARBRE_HG  33=ARBRE_HD  34=ARBRE_BG  35=ARBRE_BD
    36=BUISSON  37=PETIT_ARBRE  38=ROCHER
    39=CLOTURE_H  40=CLOTURE_V  41=PANNEAU  42=BOITE_LETTRES
    43=REBORD_H  44=REBORD_G  45=REBORD_D
    48-58=MAISON  64-74=LABO  80-85=CENTRE  86-91=BOUTIQUE  92-93=ARENE
"""

import json, os, copy

# ===== Tile constants =====
H = 0   # Herbe
HV = 1  # Herbe variante
HF = 2  # Herbe fleurs
HH = 3  # Herbe haute (encounters)
C = 4   # Chemin
CH = 5  # Chemin bord haut
CB = 6  # Chemin bord bas
CG = 7  # Chemin bord gauche
CD = 8  # Chemin bord droit
CHG = 9  # Coin haut-gauche
CHD = 10  # Coin haut-droit
CBG = 11  # Coin bas-gauche
CBD = 12  # Coin bas-droit
CIH = 13  # Coin interne haut-gauche
CID = 14  # Coin interne haut-droit
S = 15   # Sable
W = 16   # Eau
WRH = 17  # Eau rivage haut
WRB = 18  # Eau rivage bas
WRG = 19  # Eau rivage gauche
WRD = 20  # Eau rivage droit
WCH = 21  # Eau coin haut-gauche
WCD = 22  # Eau coin haut-droit
WCB = 23  # Eau coin bas-gauche
WCR = 24  # Eau coin bas-droit
WCIH = 25  # Eau coin interne HG
WCID = 26  # Eau coin interne HD
WCIB = 27  # Eau coin interne BG
WCIR = 28  # Eau coin interne BD
CIBG = 29  # Chemin coin interne BG
CIBD = 30  # Chemin coin interne BD

# Objets
V = -1  # Vide
AHG = 32  # Arbre haut-gauche
AHD = 33  # Arbre haut-droit
ABG = 34  # Arbre bas-gauche
ABD = 35  # Arbre bas-droit
BUI = 36  # Buisson
PAR = 37  # Petit arbre
ROC = 38  # Rocher
CLH = 39  # Clôture horizontale
CLV = 40  # Clôture verticale
PAN = 41  # Panneau
BOI = 42  # Boîte aux lettres
RBH = 43  # Rebord haut
RBG = 44  # Rebord gauche  
RBD = 45  # Rebord droit

# Maison toit rouge (3 large × 3 haut)
MTH = [48, 49, 50]  # toit haut
MTB = [51, 52, 53]  # toit bas
MMU = [54, 55, 56]  # mur (G, M, D)
MFE = 57  # fenêtre
MPO = 58  # porte

# Labo (4 large × 3 haut)
LTH = [64, 65, 65, 66]  # toit haut (4 wide)
LTB = [67, 68, 68, 69]  # toit bas
LMU = [70, 71, 71, 72]  # mur
LFE = 73  # labo fenêtre
LPO = 74  # labo porte

# Centre Pokémon (3×2)
CTR = [[80, 81, 82], [83, 84, 85]]

# Boutique (3×2) 
BOU = [[86, 87, 88], [89, 90, 91]]

# Arène
ASOL = 92
ASTA = 93

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "maps")


def make_grid(w, h, fill=0):
    return [[fill for _ in range(w)] for _ in range(h)]


def place_tree_border(obj, w, h, gaps=None):
    """Place des arbres 2×2 sur toute la bordure, avec des gaps aux entrées/sorties."""
    if gaps is None:
        gaps = []
    
    # Haut et bas
    for x in range(0, w-1, 2):
        for y_start in [0, h-2]:
            skip = False
            for gx1, gy1, gx2, gy2 in gaps:
                if y_start >= gy1 and y_start <= gy2 and x >= gx1 and x+1 <= gx2:
                    skip = True
                    break
            if not skip:
                obj[y_start][x] = AHG
                obj[y_start][x+1] = AHD
                obj[y_start+1][x] = ABG
                obj[y_start+1][x+1] = ABD
    
    # Gauche et droite
    for y in range(0, h-1, 2):
        for x_start in [0, w-2]:
            skip = False
            for gx1, gy1, gx2, gy2 in gaps:
                if x_start >= gx1 and x_start+1 <= gx2 and y >= gy1 and y+1 <= gy2:
                    skip = True
                    break
            if not skip:
                obj[y][x_start] = AHG
                obj[y][x_start+1] = AHD
                obj[y+1][x_start] = ABG
                obj[y+1][x_start+1] = ABD


def place_tree_col(obj, x, y1, y2):
    """Place une colonne d'arbres 2 wide de y1 à y2."""
    for y in range(y1, y2, 2):
        obj[y][x] = AHG
        obj[y][x+1] = AHD
        if y+1 <= y2:
            obj[y+1][x] = ABG
            obj[y+1][x+1] = ABD

def place_tree_row(obj, y, x1, x2):
    """Place une rangée d'arbres 2 high de x1 à x2."""
    for x in range(x1, x2, 2):
        obj[y][x] = AHG
        obj[y][x+1] = AHD
        obj[y+1][x] = ABG
        obj[y+1][x+1] = ABD


def place_house(obj, x, y, has_window=True):
    """Place une maison 3×3 à la position (x,y) = coin haut-gauche du toit."""
    obj[y][x] = MTH[0]; obj[y][x+1] = MTH[1]; obj[y][x+2] = MTH[2]
    obj[y+1][x] = MTB[0]; obj[y+1][x+1] = MTB[1]; obj[y+1][x+2] = MTB[2]
    if has_window:
        obj[y+2][x] = MFE; obj[y+2][x+1] = MPO; obj[y+2][x+2] = MFE
    else:
        obj[y+2][x] = MMU[0]; obj[y+2][x+1] = MPO; obj[y+2][x+2] = MMU[2]


def place_lab(obj, x, y):
    """Place le labo (4×3) à la position (x,y) = coin haut-gauche."""
    for dx in range(4):
        obj[y][x+dx] = LTH[dx]
        obj[y+1][x+dx] = LTB[dx]
    obj[y+2][x] = LFE; obj[y+2][x+1] = LPO; obj[y+2][x+2] = LPO; obj[y+2][x+3] = LFE


def place_centre(obj, x, y):
    """Place le Centre Pokémon (3×2)."""
    for dy in range(2):
        for dx in range(3):
            obj[y+dy][x+dx] = CTR[dy][dx]


def place_boutique(obj, x, y):
    """Place la Boutique (3×2)."""
    for dy in range(2):
        for dx in range(3):
            obj[y+dy][x+dx] = BOU[dy][dx]


def place_vertical_path(sol, x, y1, y2, width=2):
    """Place un chemin vertical avec bordures."""
    for y in range(y1, y2+1):
        sol[y][x] = CG
        for dx in range(1, width-1):
            sol[y][x+dx] = C
        sol[y][x+width-1] = CD
    # Coins d'entrée haut
    if y1 > 0:
        sol[y1][x] = CHG
        sol[y1][x+width-1] = CHD
    # Coins d'entrée bas  
    if y2 < len(sol)-1:
        sol[y2][x] = CBG
        sol[y2][x+width-1] = CBD


def place_horizontal_path(sol, y, x1, x2, height=2):
    """Place un chemin horizontal avec bordures."""
    for x in range(x1, x2+1):
        sol[y][x] = CH
        for dy in range(1, height-1):
            sol[y+dy][x] = C
        sol[y+height-1][x] = CB
    # Coins
    if x1 > 0:
        sol[y][x1] = CHG
        sol[y+height-1][x1] = CBG
    if x2 < len(sol[0])-1:
        sol[y][x2] = CHD
        sol[y+height-1][x2] = CBD


def fill_grass_area(sol, x1, y1, x2, y2, tile=HH):
    """Remplit une zone avec de l'herbe haute."""
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            sol[y][x] = tile


def fill_water(sol, x1, y1, x2, y2):
    """Remplit une zone d'eau avec rivages."""
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            sol[y][x] = W
    # Rivage haut
    if y1 > 0:
        for x in range(x1, x2+1):
            sol[y1][x] = WRH
    # Rivage bas
    if y2 < len(sol)-1:
        for x in range(x1, x2+1):
            sol[y2][x] = WRB
    # Rivage gauche
    for y in range(y1+1, y2):
        if x1 > 0:
            sol[y][x1] = WRG
    # Rivage droit
    for y in range(y1+1, y2):
        if x2 < len(sol[0])-1:
            sol[y][x2] = WRD
    # Coins
    if y1 > 0 and x1 > 0:
        sol[y1][x1] = WCH
    if y1 > 0 and x2 < len(sol[0])-1:
        sol[y1][x2] = WCD
    if y2 < len(sol)-1 and x1 > 0:
        sol[y2][x1] = WCB
    if y2 < len(sol)-1 and x2 < len(sol[0])-1:
        sol[y2][x2] = WCR


# ===================================================================
# BOURG PALETTE — 20×24 (conforme FRLG)
# ===================================================================
def build_bourg_palette():
    w, h = 20, 24
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # --- Bordure d'arbres ---
    # Haut : arbres sauf ouverture col 9-10 (sortie Route 1)
    for x in range(0, w-1, 2):
        if x < 8 or x > 11:
            for y in range(2):
                if y == 0:
                    obj[y][x] = AHG; obj[y][x+1] = AHD
                else:
                    obj[y][x] = ABG; obj[y][x+1] = ABD
    
    # Gauche : arbres colonnes x=0-1 de y=2 à y=21
    place_tree_col(obj, 0, 2, 20)
    
    # Droite : arbres colonnes x=18-19 de y=2 à y=21
    place_tree_col(obj, 18, 2, 20)
    
    # Arbres intérieurs haut-gauche  
    place_tree_col(obj, 2, 0, 4)
    place_tree_col(obj, 2, 6, 8)
    
    # Arbres intérieurs haut-droit
    place_tree_col(obj, 16, 0, 4)
    place_tree_col(obj, 16, 6, 8)
    
    # --- Chemin central vertical ---
    for y in range(2, 20):
        sol[y][9] = CG
        sol[y][10] = CD
    
    # Entrée nord (vers Route 1)
    sol[0][9] = CHG; sol[0][10] = CHD
    sol[1][9] = CG; sol[1][10] = CD
    
    # --- Maison du joueur (gauche) ---
    place_house(obj, 4, 5)
    obj[8][5] = BOI  # boîte aux lettres
    
    # --- Maison du rival (droite) ---
    place_house(obj, 12, 5)
    obj[8][14] = BOI  # boîte aux lettres
    
    # --- Clôtures le long du chemin ---
    for y in range(9, 13):
        obj[y][8] = CLV  # gauche du chemin
        obj[y][11] = CLV  # droite du chemin
    
    # --- Labo du Prof. Chen ---
    place_lab(obj, 8, 14)
    
    # --- Panneau de ville ---
    obj[10][12] = PAN
    
    # --- Fleurs décoratives ---
    sol[4][4] = HF
    sol[4][15] = HF
    sol[12][4] = HF
    sol[12][15] = HF
    sol[10][6] = HV
    sol[10][13] = HV
    
    # --- Zone eau en bas (Route 21) ---
    for y in range(21, 24):
        for x in range(2, 18):
            sol[y][x] = W
    # Rivage
    for x in range(2, 18):
        sol[20][x] = WRH
    for y in range(21, 24):
        sol[y][2] = WRG
        sol[y][17] = WRD
    sol[20][2] = WCH; sol[20][17] = WCD
    
    # Ouverture dans l'eau pour passage
    sol[20][9] = H; sol[20][10] = H
    sol[21][9] = WRH; sol[21][10] = WRH
    
    # --- Sable/plage ---
    for x in range(3, 9):
        sol[19][x] = S
    for x in range(11, 17):
        sol[19][x] = S
    sol[20][3] = S; sol[20][4] = S
    sol[20][15] = S; sol[20][16] = S
    
    data = {
        "id": "bourg_palette",
        "nom": "Bourg Palette",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/bourg_palette.ogg",
        "connexions": [
            {"direction": "nord", "vers": "route_1", "decalage": 0},
            {"direction": "sud", "vers": "route_21", "decalage": 0}
        ],
        "warps": [
            {"id": "maison_joueur_entree", "x": 5, "y": 7, "vers_map": "maison_joueur",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_rival_entree", "x": 13, "y": 7, "vers_map": "maison_rival",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "laboratoire_entree", "x": 9, "y": 16, "vers_map": "laboratoire_chen",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {
                "id": "pnj_femme_01", "x": 6, "y": 11, "sprite": "pnj_femme",
                "direction": "bas",
                "dialogue": [
                    "Bourg Palette. Une petite ville tranquille.",
                    "D'ici partent de grands aventuriers !"
                ],
                "dialogue_conditions": [
                    {"flag": "champion_ligue_battu", "valeur": True,
                     "dialogue": ["Tu es le nouveau Maître\nPokémon ?!", "Bourg Palette est fière de toi !"]}
                ],
                "mobile": True, "rayon_deplacement": 2
            },
            {
                "id": "pnj_gros_01", "x": 14, "y": 10, "sprite": "pnj_gros",
                "direction": "gauche",
                "dialogue": [
                    "Les Pokémon sauvages vivent dans les hautes herbes.",
                    "Ne t'aventure pas sans les tiens !"
                ],
                "mobile": True, "rayon_deplacement": 2
            }
        ],
        "objets_sol": [],
        "panneaux": [
            {"x": 12, "y": 10, "texte": "BOURG PALETTE\n— Une ville aux bords de l'aventure —"}
        ],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


# ===================================================================
# ROUTE 1 — 20×40 (FRLG = 20×48, compressé fidèlement)
# ===================================================================
def build_route_1():
    w, h = 20, 40
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # --- Bordure d'arbres (gauche/droite) ---
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, 18, 0, h-2)
    
    # Extra bordure intérieure (2 d'épaisseur)
    place_tree_col(obj, 2, 0, 6)
    place_tree_col(obj, 16, 0, 6)
    place_tree_col(obj, 2, 22, 28)
    place_tree_col(obj, 16, 22, 28)
    place_tree_col(obj, 2, 34, 40)
    place_tree_col(obj, 16, 34, 40)
    
    # --- Chemin sinueux ---
    # Segment 1: haut, centré (sortie vers Jadielle)
    for y in range(0, 8):
        sol[y][9] = CG; sol[y][10] = CD
    
    # Bifurcation droite
    for y in range(8, 14):
        sol[y][11] = CG; sol[y][12] = CD
    sol[8][9] = CBG; sol[8][10] = CB; sol[8][11] = CB; sol[8][12] = CBD
    sol[7][9] = CG; sol[7][10] = CIBD; sol[7][11] = CB; sol[7][12] = CBD
    
    # Retour centre
    for y in range(14, 20):
        sol[y][9] = CG; sol[y][10] = CD
    sol[14][9] = CHG; sol[14][10] = CH; sol[14][11] = CH; sol[14][12] = CHD
    sol[13][11] = CG ; sol[13][10] = CH; sol[13][9] = CHG; sol[13][12] = CIBG
    
    # Segment 3: descente avec courbe gauche
    for y in range(20, 26):
        sol[y][7] = CG; sol[y][8] = CD
    sol[20][7] = CHG; sol[20][8] = CH; sol[20][9] = CH; sol[20][10] = CHD
    sol[19][9] = CG; sol[19][10] = CIBG
    
    # Retour centre
    for y in range(26, 32):
        sol[y][9] = CG; sol[y][10] = CD
    sol[26][7] = V; sol[26][8] = V  # clear
    sol[26][9] = CG; sol[26][10] = CD
    sol[25][7] = CBG; sol[25][8] = CB; sol[25][9] = CB; sol[25][10] = CBD
    sol[26][7] = H; sol[26][8] = H  # back to grass
    
    # Segment final vers Bourg Palette
    for y in range(32, 40):
        sol[y][9] = CG; sol[y][10] = CD
    
    # Ouverture nord (vers Jadielle)
    sol[0][9] = CHG; sol[0][10] = CHD
    
    # Ouverture sud (vers Bourg Palette)
    sol[h-1][9] = CBG; sol[h-1][10] = CBD
    
    # --- Zones d'herbe haute ---
    # Patch droite haut
    fill_grass_area(sol, 13, 4, 15, 7)
    # Patch gauche milieu  
    fill_grass_area(sol, 4, 10, 6, 15)
    # Patch droite milieu
    fill_grass_area(sol, 13, 16, 15, 19)
    # Patch gauche bas
    fill_grass_area(sol, 4, 28, 6, 33)
    # Patch droite bas
    fill_grass_area(sol, 13, 32, 15, 37)
    
    # --- Rebords (ledges) ---
    for x in range(4, 8):
        obj[16][x] = RBH
    for x in range(13, 17):
        obj[24][x] = RBH
    
    # --- Fleurs et variantes ---
    sol[3][5] = HF; sol[3][14] = HV
    sol[12][14] = HF; sol[18][5] = HV
    sol[30][5] = HF; sol[30][14] = HV
    sol[27][6] = HF; sol[35][14] = HF
    
    # --- Arbre haut dans le passage
    place_tree_col(obj, 14, 8, 10)
    place_tree_col(obj, 4, 22, 24)
    
    data = {
        "id": "route_1",
        "nom": "Route 1",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/route_1.ogg",
        "connexions": [
            {"direction": "nord", "vers": "jadielle_ville", "decalage": 0},
            {"direction": "sud", "vers": "bourg_palette", "decalage": 0}
        ],
        "warps": [],
        "pnj": [
            {
                "id": "pnj_vendeur_01", "x": 8, "y": 18, "sprite": "pnj_vendeur",
                "direction": "gauche",
                "dialogue": [
                    "Hé ! J'ai trouvé ça par terre !",
                    "Tiens, prends cette Potion.\nÇa te sera utile !"
                ],
                "dialogue_conditions": [
                    {"flag": "vendeur_route1_parle", "valeur": True,
                     "dialogue": ["J'aime me promener ici !\nLes herbes hautes sont\npleines de Pokémon !"]}
                ],
                "mobile": False, "rayon_deplacement": 0
            }
        ],
        "objets_sol": [],
        "panneaux": [],
        "zones_herbes": [
            {"x1": 13, "y1": 4, "x2": 15, "y2": 7, "table": "route_1"},
            {"x1": 4, "y1": 10, "x2": 6, "y2": 15, "table": "route_1"},
            {"x1": 13, "y1": 16, "x2": 15, "y2": 19, "table": "route_1"},
            {"x1": 4, "y1": 28, "x2": 6, "y2": 33, "table": "route_1"},
            {"x1": 13, "y1": 32, "x2": 15, "y2": 37, "table": "route_1"}
        ],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


# ===================================================================
# JADIELLE VILLE — 30×30 (FRLG = 40×48, fidèlement compressé)
# ===================================================================
def build_jadielle_ville():
    w, h = 30, 30
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # --- Bordure d'arbres ---
    # Gauche
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, 2, 0, 4)
    place_tree_col(obj, 2, 10, 18)
    place_tree_col(obj, 2, 24, h-2)
    
    # Droite
    place_tree_col(obj, w-2, 0, h-2)
    place_tree_col(obj, w-4, 0, 4)
    place_tree_col(obj, w-4, 10, 18)
    place_tree_col(obj, w-4, 24, h-2)
    
    # Haut (sortie nord vers Route 2)
    for x in range(0, w-1, 2):
        if x < 13 or x > 16:
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
    
    # Bas (sortie sud vers Route 1)
    for x in range(0, w-1, 2):
        if x < 13 or x > 16:
            obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
            obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
    
    # --- Chemin central nord-sud ---
    for y in range(0, h):
        sol[y][14] = CG
        sol[y][15] = CD
    
    # --- Chemin est-ouest (connexion Route 22 à gauche) ---
    for x in range(0, 14):
        sol[20][x] = CH
        sol[21][x] = CB
    sol[20][14] = CIH; sol[21][14] = CIBG
    
    # Connexion Route 22 à gauche
    for x in range(0, 4):
        sol[20][x] = CH; sol[21][x] = CB
    
    # --- Centre Pokémon (gauche, haut) ---
    place_centre(obj, 5, 4)
    
    # --- Boutique (droite, haut) ---
    place_boutique(obj, 22, 4)
    
    # --- Maisons ---
    # Maison 1 (gauche, milieu)
    place_house(obj, 5, 12)
    
    # Maison 2 (droite, milieu)
    place_house(obj, 22, 12)
    
    # --- Arène de Jadielle (gauche, bas) ---
    # Grande bâtiment arène (4×3)
    place_house(obj, 5, 22)  # structure de base
    obj[22][5] = MTH[0]; obj[22][6] = MTH[1]; obj[22][7] = MTH[2]
    obj[23][5] = MTB[0]; obj[23][6] = MTB[1]; obj[23][7] = MTB[2]
    obj[24][5] = ASTA; obj[24][6] = MPO; obj[24][7] = ASTA
    
    # --- Boutique arbres CS01 (barrière au nord) ---
    # Petit arbre coupable bloquant Route 2 nord gauche
    obj[3][10] = PAR
    
    # --- Panneau de ville ---
    obj[8][16] = PAN
    
    # --- Vieil homme (zone tutoriel capture) ---
    # Chemin vers la zone du vieil homme
    
    # --- Fleurs et détails ---
    sol[6][10] = HF; sol[6][19] = HF
    sol[16][10] = HV; sol[16][19] = HV
    sol[8][8] = HF; sol[8][21] = HF
    sol[26][8] = HV; sol[26][21] = HF
    
    # --- Clôtures ---
    for x in range(8, 14):
        obj[10][x] = CLH
    for x in range(16, 22):
        obj[10][x] = CLH
    
    data = {
        "id": "jadielle_ville",
        "nom": "Jadielle",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/jadielle_ville.ogg",
        "connexions": [
            {"direction": "nord", "vers": "route_2", "decalage": 0},
            {"direction": "sud", "vers": "route_1", "decalage": 0},
            {"direction": "ouest", "vers": "route_22", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 6, "y": 5, "vers_map": "centre_pokemon_jadielle",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "boutique_entree", "x": 23, "y": 5, "vers_map": "boutique_jadielle",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_1_entree", "x": 6, "y": 14, "vers_map": "maison_jadielle_1",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_2_entree", "x": 23, "y": 14, "vers_map": "ecole_jadielle",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "arene_entree", "x": 6, "y": 24, "vers_map": "arene_jadielle",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {
                "id": "pnj_vieux_01", "x": 12, "y": 8, "sprite": "pnj_vieux",
                "direction": "bas",
                "dialogue": [
                    "Ah, la jeunesse...",
                    "Tu as des Poké Balls ?\nJe vais te montrer\ncomment capturer un Pokémon !"
                ],
                "dialogue_conditions": [
                    {"flag": "colis_chen_livre", "valeur": False,
                     "dialogue": ["Je n'ai pas bu mon café ce matin...", "Ne me parle pas !"]}
                ],
                "mobile": False, "rayon_deplacement": 0
            },
            {
                "id": "pnj_femme3_01", "x": 20, "y": 18, "sprite": "pnj_femme3",
                "direction": "gauche",
                "dialogue": [
                    "As-tu vu un Rattatac par ici ?",
                    "Il a mangé toutes mes baies !"
                ],
                "mobile": True, "rayon_deplacement": 2
            },
            {
                "id": "pnj_garcon_01", "x": 8, "y": 18, "sprite": "pnj_garcon",
                "direction": "droite",
                "dialogue": [
                    "Les Champions d'Arène sont\nsuper forts !",
                    "Prépare bien ton équipe\navant de les défier !"
                ],
                "mobile": True, "rayon_deplacement": 2
            }
        ],
        "objets_sol": [],
        "panneaux": [
            {"x": 16, "y": 8, "texte": "JADIELLE\n— Verdoyante et éternelle —"}
        ],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


# ===================================================================
# ARGENTA VILLE — 25×30 (FRLG = 40×48, fidèlement compressé)
# ===================================================================
def build_argenta_ville():
    w, h = 25, 30
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # --- Bordure d'arbres complète ---
    # Gauche
    place_tree_col(obj, 0, 0, h-2)
    
    # Droite 
    place_tree_col(obj, w-2, 0, h-2)
    if w % 2 == 1:
        place_tree_col(obj, w-3, 0, h-2)
    
    # Haut (sortie vers Route 3 est)
    for x in range(0, w-1, 2):
        if x < 11 or x > 13:
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
    
    # Bas (sortie sud vers Route 2)
    for x in range(0, w-1, 2):
        if x < 11 or x > 13:
            obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
            obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
    
    # --- Chemin central nord-sud ---
    for y in range(0, h):
        sol[y][12] = CG
        sol[y][13] = CD
    
    # --- Chemin est-ouest (connexion Route 3) ---
    for x in range(14, w):
        sol[4][x] = CH
        sol[5][x] = CB
    sol[4][13] = CID; sol[5][13] = CIBD
    
    # --- Musée d'Argenta (haut gauche) ---
    # Bâtiment large 4×3
    place_house(obj, 4, 3)
    obj[3][7] = MTH[2]  # extension
    place_house(obj, 7, 3, has_window=False)
    # Simplifié: deux maisons côte à côte pour simuler le musée
    
    # --- Centre Pokémon ---
    place_centre(obj, 4, 8)
    
    # --- Boutique ---
    place_boutique(obj, 16, 8)
    
    # --- Maisons résidentielles ---
    place_house(obj, 4, 14)
    place_house(obj, 16, 14)
    
    # --- Arène de Pierre (droite, milieu-bas) ---
    place_house(obj, 16, 20)
    obj[22][16] = ASTA; obj[22][18] = ASTA
    obj[22][17] = MPO
    
    # --- Panneau de ville ---
    obj[10][14] = PAN
    
    # --- Clôtures ---
    for x in range(8, 12):
        obj[12][x] = CLH
    for x in range(14, 16):
        obj[12][x] = CLH
    
    # --- Fleurs ---
    sol[6][8] = HF; sol[6][20] = HF
    sol[18][8] = HV; sol[18][20] = HV
    sol[26][8] = HF
    
    data = {
        "id": "argenta_ville",
        "nom": "Argenta",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/argenta_ville.ogg",
        "connexions": [
            {"direction": "sud", "vers": "route_2", "decalage": 0},
            {"direction": "est", "vers": "route_3", "decalage": 0}
        ],
        "warps": [
            {"id": "musee_entree", "x": 6, "y": 5, "vers_map": "musee_argenta",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "centre_pokemon_entree", "x": 5, "y": 9, "vers_map": "centre_pokemon_argenta",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "boutique_entree", "x": 17, "y": 9, "vers_map": "boutique_argenta",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_1_entree", "x": 5, "y": 16, "vers_map": "maison_argenta_1",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_2_entree", "x": 17, "y": 16, "vers_map": "maison_argenta_2",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "arene_entree", "x": 17, "y": 22, "vers_map": "arene_argenta",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {
                "id": "pnj_homme_01", "x": 10, "y": 11, "sprite": "pnj_homme",
                "direction": "bas",
                "dialogue": [
                    "Bienvenue à Argenta !",
                    "Notre musée est célèbre\npour ses fossiles."
                ],
                "mobile": True, "rayon_deplacement": 2
            },
            {
                "id": "pnj_femme_01", "x": 8, "y": 18, "sprite": "pnj_femme",
                "direction": "droite",
                "dialogue": [
                    "Le Champion d'Arène Pierre\nutilise des Pokémon Roche.",
                    "Les types Eau et Plante\nsont efficaces !"
                ],
                "mobile": True, "rayon_deplacement": 2
            },
            {
                "id": "pnj_homme_02", "x": 20, "y": 25, "sprite": "pnj_homme",
                "direction": "gauche",
                "dialogue": [
                    "La Route 3 à l'est mène\nau Mont Sélénite.",
                    "Prépare-toi bien avant\nd'y aller !"
                ],
                "mobile": False, "rayon_deplacement": 0
            }
        ],
        "objets_sol": [],
        "panneaux": [
            {"x": 14, "y": 10, "texte": "ARGENTA\n— La ville couleur pierre —"}
        ],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


# ===================================================================
# ROUTE 2 — 20×35 (FRLG = 20×96, compressé)
# ===================================================================
def build_route_2():
    w, h = 20, 35
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # --- Bordure d'arbres ---
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, 18, 0, h-2)
    place_tree_col(obj, 2, 0, 6)
    place_tree_col(obj, 16, 0, 6)
    place_tree_col(obj, 2, 14, 22)
    place_tree_col(obj, 16, 14, 22)
    place_tree_col(obj, 2, 28, h-2)
    place_tree_col(obj, 16, 28, h-2)
    
    # --- Chemin central ---
    for y in range(0, h):
        sol[y][9] = CG
        sol[y][10] = CD
    
    # --- Entrée Forêt de Jade (gauche, milieu) ---
    for x in range(4, 9):
        sol[17][x] = CH
        sol[18][x] = CB
    sol[17][9] = CIH
    sol[18][9] = CIBG
    # Bâtiment d'entrée de la forêt
    place_house(obj, 4, 15, has_window=False)
    
    # --- Maison de la sortie Route 2 (garde) ---
    place_house(obj, 11, 15, has_window=False)
    for x in range(11, 14):
        sol[17][x] = CH; sol[18][x] = CB
    sol[17][10] = CID; sol[18][10] = CIBD
    
    # --- Zones d'herbe haute ---
    fill_grass_area(sol, 4, 4, 7, 9)
    fill_grass_area(sol, 12, 4, 15, 9)
    fill_grass_area(sol, 4, 24, 7, 29)
    fill_grass_area(sol, 12, 24, 15, 29)
    
    # --- Rebords ---
    for x in range(4, 8):
        obj[10][x] = RBH
    for x in range(12, 16):
        obj[22][x] = RBH
    
    # --- Fleurs ---
    sol[12][5] = HF; sol[12][14] = HV
    sol[30][5] = HF; sol[30][14] = HF
    
    data = {
        "id": "route_2",
        "nom": "Route 2",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/route_2.ogg",
        "connexions": [
            {"direction": "nord", "vers": "argenta_ville", "decalage": 0},
            {"direction": "sud", "vers": "jadielle_ville", "decalage": 0}
        ],
        "warps": [
            {"id": "foret_jade_entree", "x": 5, "y": 17, "vers_map": "foret_de_jade",
             "vers_warp": "sortie_sud", "type": "porte"},
            {"id": "garde_route2", "x": 12, "y": 17, "vers_map": "garde_route2",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [],
        "objets_sol": [],
        "panneaux": [],
        "zones_herbes": [
            {"x1": 4, "y1": 4, "x2": 7, "y2": 9, "table": "route_2"},
            {"x1": 12, "y1": 4, "x2": 15, "y2": 9, "table": "route_2"},
            {"x1": 4, "y1": 24, "x2": 7, "y2": 29, "table": "route_2"},
            {"x1": 12, "y1": 24, "x2": 15, "y2": 29, "table": "route_2"}
        ],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


# ===================================================================
# ROUTE 3 — 40×15 (FRLG = 65×26, horizontal! pas vertical)
# ===================================================================
def build_route_3():
    w, h = 40, 15
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # --- Bordure d'arbres haut/bas ---
    for x in range(0, w-1, 2):
        # Haut
        obj[0][x] = AHG; obj[0][x+1] = AHD
        obj[1][x] = ABG; obj[1][x+1] = ABD
        # Bas (sauf ouverture droite)
        if x < w-4:
            obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
            obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
    
    # Bordure gauche (entrée depuis Argenta)
    place_tree_col(obj, 0, 2, 6)
    place_tree_col(obj, 0, 10, h-2)
    
    # Bordure droite (entrée Mont Sélénite)
    place_tree_col(obj, w-2, 2, 6)
    place_tree_col(obj, w-2, 10, h-2)
    
    # --- Chemin principal horizontal (sinueux) ---
    # Segment 1: gauche, hauteur 7-8
    for x in range(0, 12):
        sol[7][x] = CH; sol[8][x] = CB
    
    # Descente
    for y in range(8, 11):
        sol[y][11] = CG; sol[y][12] = CD
    sol[7][11] = CHD; sol[8][11] = CIBD
    sol[8][12] = CBD
    
    # Segment 2: milieu, hauteur 10-11
    for x in range(11, 25):
        sol[10][x] = CH; sol[11][x] = CB
    sol[10][11] = CHG; sol[11][11] = CBG
    
    # Montée
    for y in range(7, 11):
        sol[y][24] = CG; sol[y][25] = CD
    sol[10][24] = CHG; sol[10][25] = CID
    sol[7][24] = CHG; sol[7][25] = CHD
    
    # Segment 3: droite, hauteur 7-8
    for x in range(25, w):
        sol[7][x] = CH; sol[8][x] = CB
    sol[7][25] = CID
    sol[8][25] = CIBD
    
    # --- Zones d'herbe haute ---
    fill_grass_area(sol, 4, 3, 8, 6)
    fill_grass_area(sol, 14, 3, 18, 6)
    fill_grass_area(sol, 14, 12, 20, 13)
    fill_grass_area(sol, 28, 3, 32, 6)
    fill_grass_area(sol, 28, 10, 34, 13)
    
    # --- Fleurs ---
    sol[5][10] = HF; sol[5][22] = HV
    sol[12][8] = HF; sol[9][30] = HV
    
    data = {
        "id": "route_3",
        "nom": "Route 3",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/route_3.ogg",
        "connexions": [
            {"direction": "ouest", "vers": "argenta_ville", "decalage": 0},
            {"direction": "est", "vers": "route_4", "decalage": 0}
        ],
        "warps": [],
        "pnj": [
            {
                "id": "dresseur_gamin_01", "x": 8, "y": 5, "sprite": "pnj_gamin",
                "direction": "droite",
                "dialogue": ["Je t'ai vu dans les herbes !", "Combattons !"],
                "mobile": False, "rayon_deplacement": 0,
                "dresseur": True,
                "equipe": [{"espece": "021", "niveau": 9}],
                "flag": "dresseur_route3_01"
            },
            {
                "id": "dresseur_gamin_02", "x": 16, "y": 9, "sprite": "pnj_gamin",
                "direction": "gauche",
                "dialogue": ["Mes Pokémon sont\nimbattables !"],
                "mobile": False, "rayon_deplacement": 0,
                "dresseur": True,
                "equipe": [{"espece": "019", "niveau": 10}, {"espece": "023", "niveau": 10}],
                "flag": "dresseur_route3_02"
            },
            {
                "id": "dresseur_fillette_01", "x": 22, "y": 5, "sprite": "pnj_fillette",
                "direction": "bas",
                "dialogue": ["Mon Rondoudou est\ntrop mignon !"],
                "mobile": False, "rayon_deplacement": 0,
                "dresseur": True,
                "equipe": [{"espece": "039", "niveau": 10}],
                "flag": "dresseur_route3_03"
            },
            {
                "id": "dresseur_insecto_01", "x": 30, "y": 9, "sprite": "pnj_insectomane",
                "direction": "gauche",
                "dialogue": ["Les Pokémon Insecte\nsont les meilleurs !"],
                "mobile": False, "rayon_deplacement": 0,
                "dresseur": True,
                "equipe": [{"espece": "010", "niveau": 9}, {"espece": "013", "niveau": 9}],
                "flag": "dresseur_route3_04"
            }
        ],
        "objets_sol": [],
        "panneaux": [],
        "zones_herbes": [
            {"x1": 4, "y1": 3, "x2": 8, "y2": 6, "table": "route_3"},
            {"x1": 14, "y1": 3, "x2": 18, "y2": 6, "table": "route_3"},
            {"x1": 14, "y1": 12, "x2": 20, "y2": 13, "table": "route_3"},
            {"x1": 28, "y1": 3, "x2": 32, "y2": 6, "table": "route_3"},
            {"x1": 28, "y1": 10, "x2": 34, "y2": 13, "table": "route_3"}
        ],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


# ===================================================================
# Villes restantes: AZURIA, CARMIN, CELADOPOLE, LAVANVILLE, etc.
# ===================================================================
def build_azuria_ville():
    w, h = 25, 25
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # Bordure
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, w-2, 0, h-2)
    if w % 2 == 1:
        place_tree_col(obj, w-3, 0, h-2)
    
    for x in range(0, w-1, 2):
        if x < 11 or x > 13:
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
            obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
            obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
    
    # Chemin central
    for y in range(0, h):
        sol[y][12] = CG; sol[y][13] = CD
    
    # Chemin est-ouest (connexion Routes 9/10 est + sortie nord Route 24)
    for x in range(4, 12):
        sol[10][x] = CH; sol[11][x] = CB
    for x in range(14, 22):
        sol[10][x] = CH; sol[11][x] = CB
    sol[10][12] = CIH; sol[11][12] = CIBG
    sol[10][13] = CID; sol[11][13] = CIBD
    
    # Bâtiments
    place_centre(obj, 4, 4)     # Centre Pokémon
    place_boutique(obj, 18, 4)  # Boutique
    place_house(obj, 4, 14)     # Maison Bill
    place_house(obj, 18, 14)    # Maison 2
    
    # Arène Ondine (gauche)
    place_house(obj, 4, 20)
    obj[22][4] = ASTA; obj[22][6] = ASTA
    obj[22][5] = MPO
    
    # Eau (rivière au nord)
    for x in range(4, 22):
        sol[2][x] = WRH
        sol[3][x] = W
        sol[4][x] = WRB if obj[4][x] == V else sol[4][x]
    
    # Fleurs
    sol[8][8] = HF; sol[8][19] = HF
    sol[16][8] = HV; sol[16][19] = HV
    
    # Panneau
    obj[8][14] = PAN
    
    data = {
        "id": "azuria_ville",
        "nom": "Azuria",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/azuria_ville.ogg",
        "connexions": [
            {"direction": "nord", "vers": "route_24", "decalage": 0},
            {"direction": "sud", "vers": "route_5", "decalage": 0},
            {"direction": "est", "vers": "route_9", "decalage": 0},
            {"direction": "ouest", "vers": "route_4", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 5, "y": 5, "vers_map": "centre_pokemon_azuria",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "boutique_entree", "x": 19, "y": 5, "vers_map": "boutique_azuria",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_1_entree", "x": 5, "y": 16, "vers_map": "maison_azuria_1",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_2_entree", "x": 19, "y": 16, "vers_map": "maison_azuria_2",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "arene_entree", "x": 5, "y": 22, "vers_map": "arene_azuria",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_homme_01", "x": 10, "y": 8, "sprite": "pnj_homme",
             "direction": "bas",
             "dialogue": ["Bienvenue à Azuria !", "La rivière traverse toute la ville."],
             "mobile": True, "rayon_deplacement": 2},
            {"id": "pnj_femme_01", "x": 16, "y": 16, "sprite": "pnj_femme",
             "direction": "gauche",
             "dialogue": ["Ondine est une dresseuse\ndormidable !", "Elle utilise des Pokémon Eau."],
             "mobile": True, "rayon_deplacement": 2}
        ],
        "objets_sol": [],
        "panneaux": [{"x": 14, "y": 8, "texte": "AZURIA\n— La ville bleue aux eaux pures —"}],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


def build_carmin_sur_mer():
    w, h = 25, 25
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # Bordure
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, w-2, 0, h-2)
    if w % 2 == 1:
        place_tree_col(obj, w-3, 0, h-2)
    
    for x in range(0, w-1, 2):
        if x < 11 or x > 13:
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
    
    # Chemin central
    for y in range(0, h-4):
        sol[y][12] = CG; sol[y][13] = CD
    
    # Chemin est-ouest (vers port)
    for x in range(4, 22):
        sol[14][x] = CH; sol[15][x] = CB
    sol[14][12] = CIH; sol[15][12] = CIBG
    sol[14][13] = CID; sol[15][13] = CIBD
    
    # Bâtiments
    place_centre(obj, 4, 4)
    place_boutique(obj, 18, 4)
    place_house(obj, 4, 8)   # Pokémon Fan Club
    place_house(obj, 18, 8)  # Maison
    
    # Arène du Major Bob
    place_house(obj, 4, 18)
    obj[20][4] = ASTA; obj[20][6] = ASTA
    obj[20][5] = MPO
    
    # Port (bâtiment gauche)
    place_house(obj, 16, 18, has_window=False)
    
    # Eau (port au sud)
    for x in range(2, w-2):
        sol[h-3][x] = WRH
        sol[h-2][x] = W
        sol[h-1][x] = W
    
    # Panneau
    obj[12][14] = PAN
    
    # Fleurs
    sol[6][10] = HF; sol[6][19] = HF
    sol[16][10] = HV
    
    data = {
        "id": "carmin_sur_mer",
        "nom": "Carmin sur Mer",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/carmin_sur_mer.ogg",
        "connexions": [
            {"direction": "nord", "vers": "route_6", "decalage": 0},
            {"direction": "est", "vers": "route_11", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 5, "y": 5, "vers_map": "centre_pokemon_carmin",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "boutique_entree", "x": 19, "y": 5, "vers_map": "boutique_carmin",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "fan_club_entree", "x": 5, "y": 10, "vers_map": "fan_club_pokemon",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_entree", "x": 19, "y": 10, "vers_map": "maison_carmin_1",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "arene_entree", "x": 5, "y": 20, "vers_map": "arene_carmin",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "port_entree", "x": 17, "y": 20, "vers_map": "port_carmin",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_marin_01", "x": 14, "y": 20, "sprite": "pnj_marin",
             "direction": "bas",
             "dialogue": ["Le port de Carmin accueille\nle SS Anne !", "C'est un navire de luxe !"],
             "mobile": False, "rayon_deplacement": 0},
            {"id": "pnj_homme_01", "x": 10, "y": 12, "sprite": "pnj_homme",
             "direction": "droite",
             "dialogue": ["Le Major Bob est un ancien\nmilitaire.", "Ses Pokémon Électrik\nsont redoutables !"],
             "mobile": True, "rayon_deplacement": 2}
        ],
        "objets_sol": [],
        "panneaux": [{"x": 14, "y": 12, "texte": "CARMIN SUR MER\n— Le port aux couchers de soleil —"}],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


def build_lavanville():
    w, h = 20, 20
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # Bordure complète
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, 18, 0, h-2)
    for x in range(0, w-1, 2):
        if x < 8 or x > 11:
            obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
            obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
    for x in range(0, w-1, 2):
        if x < 8 or x > 11:
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
    
    # Chemin central
    for y in range(0, h):
        sol[y][9] = CG; sol[y][10] = CD
    
    # Bâtiments
    place_centre(obj, 3, 4)      # Centre Pokémon
    place_boutique(obj, 13, 4)   # Boutique
    place_house(obj, 3, 8)       # Maison Monsieur Fuji
    place_house(obj, 13, 8)      # Nom Rater
    
    # Tour Pokémon (grand bâtiment à droite)
    place_house(obj, 13, 12)
    obj[14][13] = ASTA; obj[14][15] = ASTA
    
    # Maison volontaires
    place_house(obj, 3, 12)
    
    # Panneau
    obj[3][11] = PAN
    
    # Fleurs/ambiance
    sol[6][7] = HF; sol[6][16] = HV
    sol[10][7] = HV; sol[10][16] = HF
    
    data = {
        "id": "lavanville",
        "nom": "Lavanville",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/lavanville.ogg",
        "connexions": [
            {"direction": "nord", "vers": "route_10", "decalage": 0},
            {"direction": "sud", "vers": "route_12", "decalage": 0},
            {"direction": "ouest", "vers": "route_8", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 4, "y": 5, "vers_map": "centre_pokemon_lavanville",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "boutique_entree", "x": 14, "y": 5, "vers_map": "boutique_lavanville",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_fuji_entree", "x": 4, "y": 10, "vers_map": "maison_m_fuji",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "nom_rater_entree", "x": 14, "y": 10, "vers_map": "maison_nom_rater",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "tour_pokemon_entree", "x": 14, "y": 14, "vers_map": "tour_pokemon_1f",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_volontaires_entree", "x": 4, "y": 14, "vers_map": "maison_volontaires_pokemon",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_ouvrier_01", "x": 7, "y": 7, "sprite": "pnj_ouvrier",
             "direction": "droite",
             "dialogue": ["Cette ville est... étrange.", "On entend des sons\nbizarres la nuit..."],
             "mobile": True, "rayon_deplacement": 2},
            {"id": "pnj_femme_01", "x": 12, "y": 15, "sprite": "pnj_femme",
             "direction": "gauche",
             "dialogue": ["La Tour Pokémon...", "C'est un lieu de repos\npour les Pokémon décédés."],
             "mobile": False, "rayon_deplacement": 0}
        ],
        "objets_sol": [],
        "panneaux": [{"x": 11, "y": 3, "texte": "LAVANVILLE\n— La ville aux esprits reposés —"}],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


def build_celadopole():
    w, h = 30, 25
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # Bordure
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, w-2, 0, h-2)
    for x in range(0, w-1, 2):
        if x < 13 or x > 16:
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
            obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
            obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
    
    # Chemin principal est-ouest
    for x in range(2, w-2):
        sol[12][x] = CH; sol[13][x] = CB
    
    # Chemin nord-sud
    for y in range(0, h):
        sol[y][14] = CG; sol[y][15] = CD
    sol[12][14] = CIH; sol[13][14] = CIBG
    sol[12][15] = CID; sol[13][15] = CIBD
    
    # Bâtiments (rangée haute)
    place_centre(obj, 4, 4)      # Centre Pokémon
    place_boutique(obj, 10, 4)   # Grand Magasin
    place_house(obj, 18, 4)      # Résidence
    place_house(obj, 24, 4)      # Résidence
    
    # Bâtiments (rangée basse)
    place_house(obj, 4, 16)      # Restaurant
    place_house(obj, 10, 16)     # Game Corner
    # Arène Érika
    place_house(obj, 18, 16)
    obj[18][18] = ASTA; obj[18][20] = ASTA
    obj[18][19] = MPO
    
    place_house(obj, 24, 16)     # Repaire Rocket
    
    # Panneau
    obj[10][16] = PAN
    
    # Fleurs (ville fleurie!)
    for x in range(4, 28, 3):
        sol[8][x] = HF
        sol[20][x] = HF
    sol[10][6] = HV; sol[10][22] = HV
    sol[14][6] = HV; sol[14][22] = HV
    
    data = {
        "id": "celadopole",
        "nom": "Céladopole",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/celadopole.ogg",
        "connexions": [
            {"direction": "ouest", "vers": "route_7", "decalage": 0},
            {"direction": "est", "vers": "route_8", "decalage": 0},
            {"direction": "sud", "vers": "route_16", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 5, "y": 5, "vers_map": "centre_pokemon_celadopole",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "grand_magasin_entree", "x": 11, "y": 5, "vers_map": "grand_magasin_1f",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "residence_1_entree", "x": 19, "y": 6, "vers_map": "residence_celadopole",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "residence_2_entree", "x": 25, "y": 6, "vers_map": "residence_celadopole_2",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "restaurant_entree", "x": 5, "y": 18, "vers_map": "restaurant_celadopole",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "casino_entree", "x": 11, "y": 18, "vers_map": "casino_celadopole",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "arene_entree", "x": 19, "y": 18, "vers_map": "arene_celadopole",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "repaire_rocket_entree", "x": 25, "y": 18, "vers_map": "repaire_rocket_entree",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_femme_01", "x": 8, "y": 10, "sprite": "pnj_femme",
             "direction": "droite",
             "dialogue": ["Céladopole est la plus grande\nville de Kanto !", "Il y a tant à faire ici !"],
             "mobile": True, "rayon_deplacement": 2},
            {"id": "pnj_rocket_01", "x": 22, "y": 14, "sprite": "pnj_rocket",
             "direction": "gauche",
             "dialogue": ["..."],
             "dialogue_conditions": [
                 {"flag": "rocket_celadopole_battu", "valeur": False,
                  "dialogue": ["Hé toi ! Ne t'approche pas\ndu Casino !", "Dégage !"]}
             ],
             "mobile": False, "rayon_deplacement": 0}
        ],
        "objets_sol": [],
        "panneaux": [{"x": 16, "y": 10, "texte": "CÉLADOPOLE\n— La ville arc-en-ciel —"}],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


def build_safrania():
    w, h = 30, 30
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # Bordure complète
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, w-2, 0, h-2)
    for x in range(0, w-1, 2):
        if x < 13 or x > 16:
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
            obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
            obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
    
    # Chemins principaux (croix)
    for y in range(0, h):
        sol[y][14] = CG; sol[y][15] = CD
    for x in range(2, w-2):
        sol[14][x] = CH; sol[15][x] = CB
    sol[14][14] = CIH; sol[15][14] = CIBG
    sol[14][15] = CID; sol[15][15] = CIBD
    
    # Bâtiments
    place_centre(obj, 4, 4)      # Centre Pokémon
    place_boutique(obj, 22, 4)   # Boutique
    
    # Silph SARL (grand bâtiment central)
    place_house(obj, 10, 8)
    place_house(obj, 13, 8)      # Extended
    place_house(obj, 16, 8)
    
    # Arène Sabrina (gauche)
    place_house(obj, 4, 18)
    obj[20][4] = ASTA; obj[20][6] = ASTA
    obj[20][5] = MPO
    
    # Dojo de combat (droite)
    place_house(obj, 22, 18)
    
    # Maisons supplémentaires
    place_house(obj, 4, 10)
    place_house(obj, 22, 10)
    
    # Panneau
    obj[12][16] = PAN
    
    data = {
        "id": "safrania",
        "nom": "Safrania",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/safrania.ogg",
        "connexions": [
            {"direction": "nord", "vers": "route_5", "decalage": 0},
            {"direction": "sud", "vers": "route_6", "decalage": 0},
            {"direction": "est", "vers": "route_8", "decalage": 0},
            {"direction": "ouest", "vers": "route_7", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 5, "y": 5, "vers_map": "centre_pokemon_safrania",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "boutique_entree", "x": 23, "y": 5, "vers_map": "boutique_safrania",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "silph_entree", "x": 14, "y": 10, "vers_map": "silph_sarl_1f",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "arene_entree", "x": 5, "y": 20, "vers_map": "arene_safrania",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "dojo_entree", "x": 23, "y": 20, "vers_map": "dojo_combat",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_1_entree", "x": 5, "y": 12, "vers_map": "maison_safrania_1",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_2_entree", "x": 23, "y": 12, "vers_map": "maison_safrania_2",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_homme_01", "x": 10, "y": 12, "sprite": "pnj_homme",
             "direction": "bas",
             "dialogue": ["La Silph SARL est le plus grand\nbâtiment de Kanto !", "Ils fabriquent les Poké Balls !"],
             "mobile": True, "rayon_deplacement": 2},
            {"id": "pnj_femme_01", "x": 18, "y": 22, "sprite": "pnj_femme",
             "direction": "gauche",
             "dialogue": ["Sabrina est terrifiante...", "Ses pouvoirs psychiques\nsont réels !"],
             "mobile": True, "rayon_deplacement": 2}
        ],
        "objets_sol": [],
        "panneaux": [{"x": 16, "y": 12, "texte": "SAFRANIA\n— La ville aux bâtiments dorés —"}],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


def build_parmanie():
    w, h = 25, 25
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # Bordure
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, w-2, 0, h-2)
    if w % 2 == 1:
        place_tree_col(obj, w-3, 0, h-2)
    for x in range(0, w-1, 2):
        if x < 11 or x > 13:
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
            obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
            obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
    
    # Chemin
    for y in range(0, h):
        sol[y][12] = CG; sol[y][13] = CD
    
    # Bâtiments
    place_centre(obj, 4, 4)
    place_boutique(obj, 18, 4)
    place_house(obj, 4, 10)      # Maison
    place_house(obj, 18, 10)     # Zone Safari entrée
    
    # Arène Koga
    place_house(obj, 4, 18)
    obj[20][4] = ASTA; obj[20][6] = ASTA
    obj[20][5] = MPO
    
    # Zone Safari bâtiment
    place_house(obj, 18, 18, has_window=False)
    
    # Panneau + fleurs
    obj[8][14] = PAN
    sol[6][8] = HF; sol[6][20] = HF
    sol[16][8] = HV
    
    data = {
        "id": "parmanie",
        "nom": "Parmanie",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/parmanie.ogg",
        "connexions": [
            {"direction": "est", "vers": "route_15", "decalage": 0},
            {"direction": "sud", "vers": "route_19", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 5, "y": 5, "vers_map": "centre_pokemon_parmanie",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "boutique_entree", "x": 19, "y": 5, "vers_map": "boutique_parmanie",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "maison_entree", "x": 5, "y": 12, "vers_map": "maison_parmanie_1",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "safari_entree", "x": 19, "y": 12, "vers_map": "zone_safari_entree",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "arene_entree", "x": 5, "y": 20, "vers_map": "arene_parmanie",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "safari_bat_entree", "x": 19, "y": 20, "vers_map": "zone_safari_bat",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_homme_01", "x": 10, "y": 8, "sprite": "pnj_homme",
             "direction": "bas",
             "dialogue": ["La Zone Safari est l'endroit\nidéal pour capturer des\nPokémon rares !"],
             "mobile": True, "rayon_deplacement": 2},
            {"id": "pnj_femme_01", "x": 16, "y": 16, "sprite": "pnj_femme",
             "direction": "gauche",
             "dialogue": ["Le Champion Koga utilise\ndes Pokémon Poison.", "Fais attention aux\nstatus altérés !"],
             "mobile": True, "rayon_deplacement": 2}
        ],
        "objets_sol": [],
        "panneaux": [{"x": 14, "y": 8, "texte": "PARMANIE\n— La ville côtière —"}],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


def build_cramoisile():
    w, h = 20, 20
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # Île entourée d'eau — pas de bordure d'arbres
    # Eau tout autour
    for y in range(h):
        for x in range(w):
            sol[y][x] = W
    
    # Terre au centre (île)
    for y in range(3, 17):
        for x in range(3, 17):
            sol[y][x] = H
    
    # Rivages
    for x in range(3, 17):
        sol[2][x] = WRH; sol[17][x] = WRB
    for y in range(3, 17):
        sol[y][2] = WRG; sol[y][17] = WRD
    sol[2][2] = WCH; sol[2][17] = WCD
    sol[17][2] = WCB; sol[17][17] = WCR
    
    # Chemin central
    for y in range(3, 17):
        sol[y][9] = CG; sol[y][10] = CD
    
    # Bâtiments
    place_centre(obj, 4, 5)
    place_boutique(obj, 13, 5)
    
    # Labo fossiles (Cramoisîle)
    place_lab(obj, 7, 9)
    
    # Arène Blaine
    place_house(obj, 4, 12)
    obj[14][4] = ASTA; obj[14][6] = ASTA
    obj[14][5] = MPO
    
    # Panneau + fleurs
    obj[4][11] = PAN
    sol[7][5] = HF; sol[7][15] = HF
    sol[15][5] = S; sol[15][14] = S  # Sable de plage
    
    # Sable en bordure
    for x in range(3, 17):
        sol[16][x] = S
    for x in range(3, 17):
        sol[3][x] = S if sol[3][x] == H else sol[3][x]
    
    data = {
        "id": "cramoisile",
        "nom": "Cramois'Île",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/cramoisile.ogg",
        "connexions": [
            {"direction": "nord", "vers": "route_21", "decalage": 0},
            {"direction": "est", "vers": "route_20", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 5, "y": 6, "vers_map": "centre_pokemon_cramoisile",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "boutique_entree", "x": 14, "y": 6, "vers_map": "boutique_cramoisile",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "labo_entree", "x": 8, "y": 11, "vers_map": "labo_fossiles",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "arene_entree", "x": 5, "y": 14, "vers_map": "arene_cramoisile",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_homme_01", "x": 12, "y": 8, "sprite": "pnj_homme",
             "direction": "gauche",
             "dialogue": ["L'île volcanique est chaude\ntoute l'année !", "Le laboratoire étudie\nles fossiles Pokémon."],
             "mobile": True, "rayon_deplacement": 2}
        ],
        "objets_sol": [],
        "panneaux": [{"x": 11, "y": 4, "texte": "CRAMOIS'ÎLE\n— L'île volcanique —"}],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


def build_plateau_indigo():
    w, h = 20, 20
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # Bordure d'arbres complète
    place_tree_col(obj, 0, 0, h-2)
    place_tree_col(obj, 18, 0, h-2)
    place_tree_col(obj, 2, 0, 6)
    place_tree_col(obj, 16, 0, 6)
    place_tree_col(obj, 2, 12, h-2)
    place_tree_col(obj, 16, 12, h-2)
    
    for x in range(0, w-1, 2):
        if x < 8 or x > 11:
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
    
    # Chemin vers l'entrée
    for y in range(12, h):
        sol[y][9] = CG; sol[y][10] = CD
    
    # Grand bâtiment du Plateau (Centre Pokémon + Ligue)
    place_centre(obj, 7, 6)
    
    # Entrée de la Ligue (grand bâtiment)
    place_house(obj, 7, 9)
    obj[11][7] = ASTA; obj[11][9] = ASTA
    obj[11][8] = MPO
    
    # Chemin décoratif
    for x in range(5, 15):
        sol[12][x] = CH
    
    # Panneau
    obj[14][11] = PAN
    
    # Fleurs
    sol[8][5] = HF; sol[8][14] = HF
    
    data = {
        "id": "plateau_indigo",
        "nom": "Plateau Indigo",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/plateau_indigo.ogg",
        "connexions": [
            {"direction": "sud", "vers": "route_23", "decalage": 0}
        ],
        "warps": [
            {"id": "centre_pokemon_entree", "x": 8, "y": 7, "vers_map": "centre_pokemon_plateau_indigo",
             "vers_warp": "sortie", "type": "porte"},
            {"id": "ligue_entree", "x": 8, "y": 11, "vers_map": "ligue_salle_olga",
             "vers_warp": "sortie", "type": "porte"}
        ],
        "pnj": [
            {"id": "pnj_garde_01", "x": 12, "y": 14, "sprite": "pnj_garde",
             "direction": "gauche",
             "dialogue": ["Bienvenue au Plateau Indigo !", "Seuls les meilleurs dresseurs\npeuvent entrer ici."],
             "mobile": False, "rayon_deplacement": 0}
        ],
        "objets_sol": [],
        "panneaux": [{"x": 11, "y": 14, "texte": "PLATEAU INDIGO\n— La Ligue Pokémon —"}],
        "zones_herbes": [],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


# ===================================================================
# ROUTES complémentaires 
# ===================================================================
def build_route_4():
    """Route 4 — horizontale, entrée Mont Sélénite côté est → Azuria"""
    w, h = 30, 12
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    # Bordure haut/bas
    for x in range(0, w-1, 2):
        obj[0][x] = AHG; obj[0][x+1] = AHD
        obj[1][x] = ABG; obj[1][x+1] = ABD
        obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
        obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
    
    # Chemin horizontal
    for x in range(0, w):
        sol[5][x] = CH; sol[6][x] = CB
    
    # Herbe haute
    fill_grass_area(sol, 4, 3, 10, 4)
    fill_grass_area(sol, 18, 3, 24, 4)
    fill_grass_area(sol, 4, 8, 10, 9)
    fill_grass_area(sol, 18, 8, 24, 9)
    
    # Entrée grotte (Mont Sélénite)
    place_house(obj, 2, 3, has_window=False)
    
    data = {
        "id": "route_4",
        "nom": "Route 4",
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": "res://assets/audio/music/route_3.ogg",
        "connexions": [
            {"direction": "est", "vers": "azuria_ville", "decalage": 0},
            {"direction": "ouest", "vers": "route_3", "decalage": 0}
        ],
        "warps": [
            {"id": "mont_selenite_sortie", "x": 3, "y": 5, "vers_map": "mont_selenite_b2f",
             "vers_warp": "sortie_est", "type": "porte"}
        ],
        "pnj": [],
        "objets_sol": [],
        "panneaux": [],
        "zones_herbes": [
            {"x1": 4, "y1": 3, "x2": 10, "y2": 4, "table": "route_4"},
            {"x1": 18, "y1": 3, "x2": 24, "y2": 4, "table": "route_4"},
            {"x1": 4, "y1": 8, "x2": 10, "y2": 9, "table": "route_4"},
            {"x1": 18, "y1": 8, "x2": 24, "y2": 9, "table": "route_4"}
        ],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


def build_generic_route(route_id, nom, w, h, direction="ns",
                        conn_nord=None, conn_sud=None, conn_est=None, conn_ouest=None,
                        musique=None, grass_areas=None, trainers=None):
    """Crée une route générique avec le bon layout directionnel."""
    sol = make_grid(w, h, H)
    obj = make_grid(w, h, V)
    
    if direction == "ns":  # Nord-Sud
        # Bordure gauche/droite
        place_tree_col(obj, 0, 0, h-2)
        place_tree_col(obj, w-2, 0, h-2)
        # Chemin central
        cx = w // 2 - 1
        for y in range(h):
            sol[y][cx] = CG; sol[y][cx+1] = CD
    elif direction == "ew":  # Est-Ouest
        # Bordure haut/bas
        for x in range(0, w-1, 2):
            obj[0][x] = AHG; obj[0][x+1] = AHD
            obj[1][x] = ABG; obj[1][x+1] = ABD
            obj[h-2][x] = AHG; obj[h-2][x+1] = AHD
            obj[h-1][x] = ABG; obj[h-1][x+1] = ABD
        # Chemin horizontal central
        cy = h // 2 - 1
        for x in range(w):
            sol[cy][x] = CH; sol[cy+1][x] = CB
    
    # Zones d'herbe
    if grass_areas:
        for ga in grass_areas:
            fill_grass_area(sol, ga[0], ga[1], ga[2], ga[3])
    
    connexions = []
    if conn_nord: connexions.append({"direction": "nord", "vers": conn_nord, "decalage": 0})
    if conn_sud: connexions.append({"direction": "sud", "vers": conn_sud, "decalage": 0})
    if conn_est: connexions.append({"direction": "est", "vers": conn_est, "decalage": 0})
    if conn_ouest: connexions.append({"direction": "ouest", "vers": conn_ouest, "decalage": 0})
    
    data = {
        "id": route_id,
        "nom": nom,
        "largeur": w,
        "hauteur": h,
        "tileset": "outdoor",
        "musique": musique or f"res://assets/audio/music/{route_id}.ogg",
        "connexions": connexions,
        "warps": [],
        "pnj": trainers or [],
        "objets_sol": [],
        "panneaux": [],
        "zones_herbes": [{"x1": g[0], "y1": g[1], "x2": g[2], "y2": g[3], "table": route_id} for g in (grass_areas or [])],
        "tiles_sol": sol,
        "tiles_objets": obj
    }
    return data


# ===================================================================
# MAIN — Reconstruction et sauvegarde
# ===================================================================
def save_map(data, backup=True):
    path = os.path.join(DATA_DIR, f"{data['id']}.json")
    if backup and os.path.exists(path):
        bak = path + ".bak"
        if not os.path.exists(bak):
            import shutil
            shutil.copy2(path, bak)
    
    # Générer tile_data (version aplatie de tiles_sol pour compat legacy)
    sol = data.get("tiles_sol", [])
    data["tile_data"] = [sol[y][x] for y in range(len(sol)) for x in range(len(sol[0]) if sol else 0)]
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {data['id']} ({data['largeur']}×{data['hauteur']})")


def merge_existing_data(new_data, map_id):
    """Préserve certaines données de la carte existante (musique, etc.)."""
    path = os.path.join(DATA_DIR, f"{map_id}.json")
    if os.path.exists(path):
        with open(path) as f:
            old = json.load(f)
        # Conserver la musique si elle existe
        if "musique" in old and old["musique"]:
            new_data["musique"] = old["musique"]


def main():
    print("=" * 60)
    print("  RECONSTRUCTION DES CARTES KANTO — Fidèle FRLG")
    print("=" * 60)
    
    # Cartes principales reconstruites
    builders = [
        ("Bourg Palette", build_bourg_palette),
        ("Route 1", build_route_1),
        ("Jadielle", build_jadielle_ville),
        ("Route 2", build_route_2),
        ("Route 3", build_route_3),
        ("Route 4", build_route_4),
        ("Argenta", build_argenta_ville),
        ("Azuria", build_azuria_ville),
        ("Carmin sur Mer", build_carmin_sur_mer),
        ("Lavanville", build_lavanville),
        ("Céladopole", build_celadopole),
        ("Safrania", build_safrania),
        ("Parmanie", build_parmanie),
        ("Cramois'Île", build_cramoisile),
        ("Plateau Indigo", build_plateau_indigo),
    ]
    
    print("\n--- Villes et routes principales ---")
    for name, builder in builders:
        data = builder()
        merge_existing_data(data, data["id"])
        save_map(data)
    
    # Routes génériques
    print("\n--- Routes complémentaires ---")
    routes = [
        build_generic_route("route_5", "Route 5", 15, 25, "ns",
                           conn_nord="azuria_ville", conn_sud="safrania",
                           grass_areas=[(3, 6, 6, 11), (8, 14, 11, 19)]),
        build_generic_route("route_6", "Route 6", 15, 25, "ns",
                           conn_nord="safrania", conn_sud="carmin_sur_mer",
                           grass_areas=[(3, 6, 6, 11), (8, 14, 11, 19)]),
        build_generic_route("route_7", "Route 7", 20, 10, "ew",
                           conn_est="safrania", conn_ouest="celadopole"),
        build_generic_route("route_8", "Route 8", 30, 10, "ew",
                           conn_est="lavanville", conn_ouest="safrania",
                           grass_areas=[(8, 2, 14, 3), (18, 7, 24, 8)]),
        build_generic_route("route_9", "Route 9", 30, 10, "ew",
                           conn_est="route_10", conn_ouest="azuria_ville",
                           grass_areas=[(8, 2, 14, 3), (18, 7, 24, 8)]),
        build_generic_route("route_10", "Route 10", 15, 30, "ns",
                           conn_nord="route_9", conn_sud="lavanville",
                           grass_areas=[(3, 8, 6, 15), (8, 18, 11, 25)]),
        build_generic_route("route_11", "Route 11", 30, 10, "ew",
                           conn_est="route_12", conn_ouest="carmin_sur_mer",
                           grass_areas=[(6, 2, 12, 3), (18, 7, 24, 8)]),
        build_generic_route("route_12", "Route 12", 12, 40, "ns",
                           conn_nord="lavanville", conn_sud="route_13",
                           grass_areas=[(2, 10, 5, 17), (6, 24, 9, 31)]),
        build_generic_route("route_13", "Route 13", 30, 10, "ew",
                           conn_est="route_12", conn_ouest="route_14",
                           grass_areas=[(6, 2, 12, 3), (18, 7, 24, 8)]),
        build_generic_route("route_14", "Route 14", 12, 30, "ns",
                           conn_nord="route_13", conn_sud="route_15",
                           grass_areas=[(2, 8, 5, 15), (6, 18, 9, 25)]),
        build_generic_route("route_15", "Route 15", 30, 10, "ew",
                           conn_est="route_14", conn_ouest="parmanie",
                           grass_areas=[(8, 2, 14, 3), (18, 7, 24, 8)]),
        build_generic_route("route_16", "Route 16", 15, 20, "ns",
                           conn_nord="celadopole", conn_sud="route_17"),
        build_generic_route("route_17", "Route 17", 12, 50, "ns",
                           conn_nord="route_16", conn_sud="route_18"),
        build_generic_route("route_18", "Route 18", 25, 10, "ew",
                           conn_est="parmanie", conn_ouest="route_17"),
        build_generic_route("route_19", "Route 19", 12, 30, "ns",
                           conn_nord="parmanie", conn_sud="route_20",
                           grass_areas=[]),  # Water route, no grass
        build_generic_route("route_20", "Route 20", 40, 10, "ew",
                           conn_est="route_19", conn_ouest="cramoisile"),
        build_generic_route("route_21", "Route 21", 12, 30, "ns",
                           conn_nord="cramoisile", conn_sud="bourg_palette"),
        build_generic_route("route_22", "Route 22", 20, 15, "ew",
                           conn_est="jadielle_ville", conn_ouest="route_23",
                           grass_areas=[(4, 2, 8, 5), (12, 9, 16, 12)]),
        build_generic_route("route_23", "Route 23", 15, 40, "ns",
                           conn_nord="plateau_indigo", conn_sud="route_22"),
        build_generic_route("route_24", "Route 24", 12, 30, "ns",
                           conn_nord="route_25", conn_sud="azuria_ville",
                           grass_areas=[(2, 8, 5, 15), (6, 18, 9, 25)]),
        build_generic_route("route_25", "Route 25", 25, 10, "ew",
                           conn_ouest="route_24",
                           grass_areas=[(6, 2, 12, 3), (14, 7, 20, 8)]),
    ]
    
    for route_data in routes:
        merge_existing_data(route_data, route_data["id"])
        save_map(route_data)
    
    print(f"\n✓ Reconstruction terminée : {len(builders) + len(routes)} cartes")
    print("  Les fichiers .bak contiennent les anciennes versions")


if __name__ == "__main__":
    main()
