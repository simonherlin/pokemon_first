#!/usr/bin/env python3
"""
Générateur de sprites HD pour Pokémon Rouge/Bleu HD.
Produit des sprites personnages de haute qualité (32×48) style Gen IV/V.
Chaque personnage a 4 directions × 3 frames = 12 fichiers.

Utilise des palettes FRLG/HGSS et du pixel art manuel détaillé.
"""

from PIL import Image
import os, random

random.seed(42)

OUT_DIR = "assets/sprites/characters"
W, H = 32, 48  # Taille standard Gen V overworld

# ==========================================================================
# PALETTE 
# ==========================================================================
T = (0, 0, 0, 0)             # transparent
BK = (24, 24, 32, 255)       # outline noir
BK2 = (40, 40, 48, 255)      # outline doux

# Peau
SK1 = (255, 224, 184, 255)   # peau claire
SK2 = (240, 200, 160, 255)   # peau ombre
SK3 = (224, 176, 136, 255)   # peau foncée

# Yeux
EY1 = (32, 32, 32, 255)      # pupille
EY2 = (255, 255, 255, 255)   # blanc œil

# Rouge (casquette/veste Red)
RD1 = (216, 40, 40, 255)     # rouge vif
RD2 = (184, 24, 24, 255)     # rouge foncé
RD3 = (240, 72, 56, 255)     # rouge clair

# Bleu (jean)
BL1 = (56, 80, 160, 255)     # bleu jean
BL2 = (40, 56, 128, 255)     # bleu foncé
BL3 = (80, 104, 184, 255)    # bleu clair

# T-shirt noir
TS1 = (48, 48, 56, 255)
TS2 = (64, 64, 72, 255)

# Cheveux noirs
HR1 = (32, 32, 40, 255)
HR2 = (56, 48, 48, 255)

# Chaussures
SH1 = (200, 200, 208, 255)   # sneakers blanc
SH2 = (168, 168, 176, 255)   # ombre sneakers
SH3 = (224, 56, 48, 255)     # détail rouge

# Sac à dos
BP1 = (216, 192, 120, 255)   # sac jaune
BP2 = (184, 160, 96, 255)    # sac ombre

# Blanc (casquette bord, col)
WH = (248, 248, 248, 255)
WH2 = (224, 224, 232, 255)

# ==========================================================================
# DÉFINITION DU JOUEUR (RED)
# Chaque frame est une grille 32×48 de couleurs
# Les sprites utilisent . pour transparent, # pour outline
# ==========================================================================

def make_img(data, w=W, h=H):
    """Crée une image PIL à partir d'un tableau 2D de tuples RGBA."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(min(h, len(data))):
        row = data[y]
        for x in range(min(w, len(row))):
            px = row[x]
            if px != T:
                img.putpixel((x, y), px)
    return img


# === JOUEUR RED : BAS (face au joueur) ===
def player_front_idle():
    """Red face à la caméra, position neutre."""
    # Grille 32×48 — seul le centre est utilisé (~16px large)
    d = [[T]*32 for _ in range(48)]
    
    # Casquette (y=10-14)
    for x in range(10, 22): d[10][x] = RD1
    for x in range(9, 23): d[11][x] = RD1
    for x in range(9, 23): d[12][x] = RD2
    d[12][15] = WH; d[12][16] = WH  # logo casquette
    for x in range(8, 24): d[13][x] = BK  # visière
    for x in range(9, 23): d[13][x] = RD2
    # Bord visière
    for x in range(7, 25): d[14][x] = BK
    for x in range(8, 24): d[14][x] = WH2
    
    # Cheveux (sous casquette, côtés)
    d[15][9] = HR1; d[15][10] = HR1; d[15][21] = HR1; d[15][22] = HR1
    
    # Visage (y=15-20)
    for y in range(15, 21):
        for x in range(10, 22):
            d[y][x] = SK1
        d[y][10] = SK2; d[y][21] = SK2  # ombre bord
    # Yeux (y=17)
    d[17][12] = EY1; d[17][13] = EY1
    d[17][18] = EY1; d[17][19] = EY1
    d[16][12] = EY2; d[16][18] = EY2  # reflet
    # Bouche (y=19)
    d[19][14] = SK3; d[19][15] = SK3; d[19][16] = SK3; d[19][17] = SK3
    
    # Cou
    d[21][14] = SK2; d[21][15] = SK1; d[21][16] = SK1; d[21][17] = SK2
    
    # Veste rouge (y=22-30)
    for y in range(22, 31):
        for x in range(9, 23):
            d[y][x] = RD1
        d[y][9] = RD2; d[y][22] = RD2
    # Col
    d[22][13] = TS1; d[22][14] = TS1; d[22][15] = TS1
    d[22][16] = TS1; d[22][17] = TS1; d[22][18] = TS1
    # Fermeture éclair
    for y in range(23, 30):
        d[y][15] = BK; d[y][16] = BK
    # Boutons/détails
    d[25][12] = WH; d[25][19] = WH
    
    # Bras (côtés veste)
    for y in range(23, 30):
        d[y][7] = SK2; d[y][8] = RD2; d[y][9] = RD1
        d[y][22] = RD1; d[y][23] = RD2; d[y][24] = SK2
    # Mains
    d[30][7] = SK1; d[30][8] = SK1; d[30][23] = SK1; d[30][24] = SK1
    
    # Ceinture
    for x in range(9, 23): d[31][x] = BK
    d[31][15] = (200, 200, 56, 255); d[31][16] = (200, 200, 56, 255)  # boucle
    
    # Pantalon bleu (y=32-40)
    for y in range(32, 41):
        for x in range(10, 22):
            d[y][x] = BL1
        d[y][10] = BL2; d[y][21] = BL2
    # Séparation jambes
    for y in range(35, 41):
        d[y][15] = BL2; d[y][16] = BL2
    
    # Chaussures (y=41-44)
    for y in range(41, 45):
        for x in range(9, 16):
            d[y][x] = SH1
        for x in range(16, 23):
            d[y][x] = SH1
        d[y][9] = SH2; d[y][15] = SH2; d[y][16] = SH2; d[y][22] = SH2
    # Détail rouge sneakers
    d[42][10] = SH3; d[42][11] = SH3; d[42][20] = SH3; d[42][21] = SH3
    
    # Outline bas
    for x in range(9, 23):
        if d[45][x] == T and d[44][x] != T:
            d[45][x] = BK
    
    return d

def player_front_walk1():
    """Red face, pas gauche."""
    d = player_front_idle()
    # Décaler jambe gauche vers la gauche, droite vers la droite
    for y in range(37, 45):
        # Effacer jambes
        for x in range(9, 23): d[y][x] = T
    # Jambe gauche (décalée)
    for y in range(37, 43):
        for x in range(8, 15): d[y][x] = BL1
        d[y][8] = BL2
    for y in range(43, 46):
        for x in range(7, 14): d[y][x] = SH1
        d[y][7] = SH2; d[y][13] = SH2
        d[44][8] = SH3; d[44][9] = SH3
    # Jambe droite (pas derrière, plus haut)
    for y in range(37, 42):
        for x in range(17, 22): d[y][x] = BL2
    for y in range(42, 45):
        for x in range(17, 22): d[y][x] = SH2
    return d

def player_front_walk2():
    """Red face, pas droit."""
    d = player_front_idle()
    for y in range(37, 45):
        for x in range(9, 23): d[y][x] = T
    # Jambe droite (décalée)
    for y in range(37, 43):
        for x in range(17, 24): d[y][x] = BL1
        d[y][23] = BL2
    for y in range(43, 46):
        for x in range(18, 25): d[y][x] = SH1
        d[y][24] = SH2; d[y][18] = SH2
        d[44][22] = SH3; d[44][23] = SH3
    # Jambe gauche (derrière)
    for y in range(37, 42):
        for x in range(10, 15): d[y][x] = BL2
    for y in range(42, 45):
        for x in range(10, 15): d[y][x] = SH2
    return d


# === JOUEUR RED : HAUT (dos) ===
def player_back_idle():
    """Red vu de dos."""
    d = [[T]*32 for _ in range(48)]
    
    # Casquette arrière (y=10-14)
    for x in range(10, 22): d[10][x] = RD1
    for x in range(9, 23): d[11][x] = RD1
    for x in range(9, 23): d[12][x] = RD2
    for x in range(9, 23): d[13][x] = RD2
    # Pas de visière visible de dos
    for x in range(9, 23): d[14][x] = RD1
    # Ajustement lanière casquette
    d[14][15] = WH; d[14][16] = WH
    
    # Cheveux (visibles sous la casquette de dos)
    for y in range(15, 18):
        for x in range(10, 22): d[y][x] = HR1
        d[y][9] = HR2; d[y][22] = HR2
    d[18][11] = HR1; d[18][12] = HR1; d[18][19] = HR1; d[18][20] = HR1
    
    # Cou
    for y in range(18, 22):
        d[y][14] = SK2; d[y][15] = SK1; d[y][16] = SK1; d[y][17] = SK2
    
    # Veste rouge (dos) (y=22-30)  
    for y in range(22, 31):
        for x in range(9, 23):
            d[y][x] = RD1
        d[y][9] = RD2; d[y][22] = RD2
    # Sac à dos
    for y in range(23, 29):
        d[y][11] = BP1; d[y][12] = BP1; d[y][13] = BP1
        d[y][18] = BP1; d[y][19] = BP1; d[y][20] = BP1
    for y in range(24, 28):
        d[y][12] = BP2; d[y][19] = BP2
    
    # Bras
    for y in range(23, 30):
        d[y][7] = SK2; d[y][8] = RD2; d[y][9] = RD1
        d[y][22] = RD1; d[y][23] = RD2; d[y][24] = SK2
    d[30][7] = SK1; d[30][8] = SK1; d[30][23] = SK1; d[30][24] = SK1
    
    # Ceinture
    for x in range(9, 23): d[31][x] = BK
    
    # Jean (dos)
    for y in range(32, 41):
        for x in range(10, 22):
            d[y][x] = BL1
        d[y][10] = BL2; d[y][21] = BL2
    for y in range(35, 41):
        d[y][15] = BL2; d[y][16] = BL2
    
    # Chaussures
    for y in range(41, 45):
        for x in range(9, 16): d[y][x] = SH1
        for x in range(16, 23): d[y][x] = SH1
        d[y][9] = SH2; d[y][15] = SH2; d[y][16] = SH2; d[y][22] = SH2
    d[43][11] = SH3; d[43][12] = SH3; d[43][19] = SH3; d[43][20] = SH3
    
    return d

def player_back_walk1():
    d = player_back_idle()
    for y in range(37, 45):
        for x in range(9, 23): d[y][x] = T
    for y in range(37, 43):
        for x in range(8, 15): d[y][x] = BL1
        d[y][8] = BL2
    for y in range(43, 46):
        for x in range(7, 14): d[y][x] = SH1
        d[y][7] = SH2
    for y in range(37, 42):
        for x in range(17, 22): d[y][x] = BL2
    for y in range(42, 45):
        for x in range(17, 22): d[y][x] = SH2
    return d

def player_back_walk2():
    d = player_back_idle()
    for y in range(37, 45):
        for x in range(9, 23): d[y][x] = T
    for y in range(37, 43):
        for x in range(17, 24): d[y][x] = BL1
        d[y][23] = BL2
    for y in range(43, 46):
        for x in range(18, 25): d[y][x] = SH1
        d[y][24] = SH2
    for y in range(37, 42):
        for x in range(10, 15): d[y][x] = BL2
    for y in range(42, 45):
        for x in range(10, 15): d[y][x] = SH2
    return d


# === JOUEUR RED : GAUCHE (profil) ===
def player_left_idle():
    """Red vu du côté gauche."""
    d = [[T]*32 for _ in range(48)]
    
    # Casquette (profil gauche - bord vers la gauche)
    for x in range(10, 20): d[10][x] = RD1
    for x in range(9, 21): d[11][x] = RD1
    for x in range(8, 21): d[12][x] = RD2
    # Visière vers la gauche
    for x in range(5, 18): d[13][x] = BK
    for x in range(6, 17): d[13][x] = WH2
    for x in range(4, 17): d[14][x] = WH2
    d[14][4] = BK
    
    # Cheveux (profil)
    d[14][18] = HR1; d[14][19] = HR1; d[14][20] = HR1
    for y in range(15, 18):
        d[y][18] = HR1; d[y][19] = HR1; d[y][20] = HR1
    
    # Visage (profil - côté gauche visible)
    for y in range(15, 21):
        for x in range(10, 18):
            d[y][x] = SK1
        d[y][10] = SK2
    # Œil (profil gauche)
    d[17][11] = EY1; d[17][12] = EY1
    d[16][11] = EY2
    # Nez
    d[18][9] = SK1
    # Bouche  
    d[19][10] = SK3; d[19][11] = SK3
    
    # Cou
    d[21][13] = SK2; d[21][14] = SK1; d[21][15] = SK1
    
    # Veste (profil)
    for y in range(22, 31):
        for x in range(10, 21):
            d[y][x] = RD1
        d[y][10] = RD2; d[y][20] = RD2
    # Bras (profil)
    for y in range(23, 30):
        d[y][9] = RD2; d[y][10] = RD1
        d[y][20] = RD1; d[y][21] = RD2
    d[30][9] = SK1; d[30][10] = SK1
    # Sac à dos (visible de côté)
    for y in range(23, 28):
        d[y][20] = BP1; d[y][21] = BP1
        d[y][22] = BP2
    
    # Fermeture
    for y in range(23, 30):
        d[y][11] = BK
    
    # Ceinture
    for x in range(10, 21): d[31][x] = BK
    
    # Jean (profil)
    for y in range(32, 41):
        for x in range(11, 20):
            d[y][x] = BL1
        d[y][11] = BL2
    
    # Chaussures (profil)
    for y in range(41, 45):
        for x in range(9, 20):
            d[y][x] = SH1
        d[y][9] = SH2; d[y][19] = SH2
    d[43][10] = SH3; d[43][11] = SH3
    
    return d

def player_left_walk1():
    d = player_left_idle()
    for y in range(37, 45):
        for x in range(7, 23): d[y][x] = T
    # Jambe devant (gauche)
    for y in range(37, 43):
        for x in range(8, 15): d[y][x] = BL1
        d[y][8] = BL2
    for y in range(43, 46):
        for x in range(6, 14): d[y][x] = SH1
        d[y][6] = SH2
    # Jambe derrière
    for y in range(37, 42):
        for x in range(16, 21): d[y][x] = BL2
    for y in range(42, 45):
        for x in range(17, 21): d[y][x] = SH2
    return d

def player_left_walk2():
    d = player_left_idle()
    for y in range(37, 45):
        for x in range(7, 23): d[y][x] = T
    # Jambe devant
    for y in range(37, 43):
        for x in range(16, 22): d[y][x] = BL1
        d[y][21] = BL2  
    for y in range(43, 46):
        for x in range(17, 24): d[y][x] = SH1
        d[y][23] = SH2
    # Jambe derrière
    for y in range(37, 42):
        for x in range(10, 15): d[y][x] = BL2
    for y in range(42, 45):
        for x in range(10, 14): d[y][x] = SH2
    return d


def mirror_h(data, w=32):
    """Miroir horizontal pour créer le profil droit."""
    mirrored = []
    for row in data:
        new_row = list(row)
        for x in range(w):
            new_row[w - 1 - x] = row[x]
        mirrored.append(new_row)
    return mirrored


# ==========================================================================
# GÉNÉRATION PNJ GÉNÉRIQUES
# ==========================================================================

def make_generic_char(config):
    """Crée un personnage générique à partir d'un config dict."""
    hair = config.get("hair", HR1)
    hair2 = config.get("hair2", HR2)
    skin = config.get("skin", SK1)
    skin_s = config.get("skin_s", SK2)
    shirt = config.get("shirt", (64, 128, 200, 255))
    shirt_s = config.get("shirt_s", (48, 96, 168, 255))
    pants = config.get("pants", BL1)
    pants_s = config.get("pants_s", BL2)
    shoes = config.get("shoes", SH1)
    shoes_s = config.get("shoes_s", SH2)
    hat = config.get("hat", None)
    hat_s = config.get("hat_s", None)
    has_skirt = config.get("skirt", False)
    accessory = config.get("accessory", None)
    
    def _front_idle():
        d = [[T]*32 for _ in range(48)]
        hy = 10
        
        # Chapeau/cheveux
        if hat:
            for x in range(10, 22): d[hy][x] = hat
            for x in range(9, 23): d[hy+1][x] = hat
            for x in range(9, 23): d[hy+2][x] = hat_s or hat
            for x in range(9, 23): d[hy+3][x] = hat_s or hat
            ch_start = hy + 4
        else:
            # Cheveux sans chapeau
            for x in range(10, 22): d[hy][x] = hair
            for x in range(9, 23): d[hy+1][x] = hair
            for x in range(9, 23): d[hy+2][x] = hair
            d[hy+3][9] = hair2; d[hy+3][10] = hair2; d[hy+3][21] = hair2; d[hy+3][22] = hair2
            ch_start = hy + 3
        
        # Cheveux côtés
        d[ch_start][9] = hair; d[ch_start][10] = hair
        d[ch_start][21] = hair; d[ch_start][22] = hair
        
        # Visage
        face_start = ch_start + 1
        for y in range(face_start, face_start + 6):
            for x in range(10, 22): d[y][x] = skin
            d[y][10] = skin_s; d[y][21] = skin_s
        # Yeux
        ey = face_start + 2
        d[ey][12] = EY1; d[ey][13] = EY1; d[ey][18] = EY1; d[ey][19] = EY1
        # Bouche
        d[face_start+4][14] = skin_s; d[face_start+4][15] = skin_s; d[face_start+4][16] = skin_s; d[face_start+4][17] = skin_s
        
        # Cou
        ny = face_start + 6
        d[ny][14] = skin_s; d[ny][15] = skin; d[ny][16] = skin; d[ny][17] = skin_s
        
        # Chemise/haut
        sy = ny + 1
        for y in range(sy, sy + 9):
            for x in range(9, 23): d[y][x] = shirt
            d[y][9] = shirt_s; d[y][22] = shirt_s
        # Bras
        for y in range(sy + 1, sy + 7):
            d[y][7] = skin_s; d[y][8] = shirt_s
            d[y][23] = shirt_s; d[y][24] = skin_s
        d[sy+7][7] = skin; d[sy+7][8] = skin
        d[sy+7][23] = skin; d[sy+7][24] = skin
        
        # Ceinture
        by = sy + 9
        for x in range(9, 23): d[by][x] = BK
        
        # Pantalon ou jupe
        py = by + 1
        if has_skirt:
            for y in range(py, py + 5):
                w_skirt = 7 + y - py
                sx = 16 - w_skirt // 2
                ex = 16 + w_skirt // 2
                for x in range(sx, ex): d[y][x] = pants
                d[y][sx] = pants_s
            py2 = py + 5
            for y in range(py2, py2 + 4):
                for x in range(11, 21): d[y][x] = skin
                d[y][11] = skin_s
        else:
            for y in range(py, py + 9):
                for x in range(10, 22): d[y][x] = pants
                d[y][10] = pants_s; d[y][21] = pants_s
            for y in range(py + 3, py + 9):
                d[y][15] = pants_s; d[y][16] = pants_s
        
        # Chaussures
        shoe_y = py + 9 if not has_skirt else py + 9
        for y in range(shoe_y, min(shoe_y + 3, 48)):
            for x in range(9, 16): d[y][x] = shoes
            for x in range(16, 23): d[y][x] = shoes
            d[y][9] = shoes_s; d[y][22] = shoes_s
        
        # Accessoire
        if accessory == "labcoat":
            for y in range(sy, sy + 9):
                d[y][8] = WH; d[y][9] = WH
                d[y][22] = WH; d[y][23] = WH
        elif accessory == "nurse_cross":
            d[sy+2][15] = RD1; d[sy+2][16] = RD1
            d[sy+3][14] = RD1; d[sy+3][15] = RD1; d[sy+3][16] = RD1; d[sy+3][17] = RD1
            d[sy+4][15] = RD1; d[sy+4][16] = RD1
        elif accessory == "rocket_R":
            d[sy+2][14] = WH; d[sy+2][15] = WH; d[sy+2][16] = WH
            d[sy+3][14] = WH; d[sy+3][15] = WH
            d[sy+4][14] = WH; d[sy+4][15] = WH; d[sy+4][16] = WH
            d[sy+5][14] = WH; d[sy+5][16] = WH
            d[sy+6][14] = WH; d[sy+6][16] = WH; d[sy+6][17] = WH
        
        return d
    
    def _front_walk1():
        base = _front_idle()
        shoe_base = 41 if not has_skirt else 41
        for y in range(37, min(48, shoe_base + 4)):
            for x in range(7, 25): base[y][x] = T
        for y in range(37, 43):
            for x in range(8, 15): base[y][x] = pants
            base[y][8] = pants_s
        for y in range(43, min(46, 48)):
            for x in range(7, 14): base[y][x] = shoes
            base[y][7] = shoes_s
        for y in range(37, 42):
            for x in range(17, 22): base[y][x] = pants_s
        for y in range(42, min(45, 48)):
            for x in range(17, 22): base[y][x] = shoes_s
        return base
    
    def _front_walk2():
        base = _front_idle()
        for y in range(37, min(48, 46)):
            for x in range(7, 25): base[y][x] = T
        for y in range(37, 43):
            for x in range(17, 24): base[y][x] = pants
            base[y][23] = pants_s
        for y in range(43, min(46, 48)):
            for x in range(18, 25): base[y][x] = shoes
            base[y][24] = shoes_s
        for y in range(37, 42):
            for x in range(10, 15): base[y][x] = pants_s
        for y in range(42, min(45, 48)):
            for x in range(10, 15): base[y][x] = shoes_s
        return base
    
    def _back_idle():
        d = [[T]*32 for _ in range(48)]
        hy = 10
        if hat:
            for x in range(10, 22): d[hy][x] = hat
            for x in range(9, 23): d[hy+1][x] = hat
            for x in range(9, 23): d[hy+2][x] = hat_s or hat
            for x in range(9, 23): d[hy+3][x] = hat_s or hat
            for x in range(9, 23): d[hy+4][x] = hat
            ch_start = hy + 5
        else:
            for x in range(10, 22): d[hy][x] = hair
            for x in range(9, 23): d[hy+1][x] = hair
            for x in range(9, 23): d[hy+2][x] = hair
            for x in range(9, 23): d[hy+3][x] = hair
            ch_start = hy + 4
        for y in range(ch_start, ch_start + 3):
            for x in range(10, 22): d[y][x] = hair
            d[y][9] = hair2; d[y][22] = hair2
        ny = ch_start + 3
        d[ny][14] = skin_s; d[ny][15] = skin; d[ny][16] = skin; d[ny][17] = skin_s
        sy = ny + 1
        for y in range(sy, sy + 9):
            for x in range(9, 23): d[y][x] = shirt
            d[y][9] = shirt_s; d[y][22] = shirt_s
        for y in range(sy + 1, sy + 7):
            d[y][7] = skin_s; d[y][8] = shirt_s
            d[y][23] = shirt_s; d[y][24] = skin_s
        d[sy+7][7] = skin; d[sy+7][8] = skin
        d[sy+7][23] = skin; d[sy+7][24] = skin
        by = sy + 9
        for x in range(9, 23): d[by][x] = BK
        py = by + 1
        for y in range(py, py + 9):
            for x in range(10, 22): d[y][x] = pants
            d[y][10] = pants_s; d[y][21] = pants_s
        for y in range(py + 3, py + 9):
            d[y][15] = pants_s; d[y][16] = pants_s
        shoe_y = py + 9
        for y in range(shoe_y, min(shoe_y + 3, 48)):
            for x in range(9, 16): d[y][x] = shoes
            for x in range(16, 23): d[y][x] = shoes
            d[y][9] = shoes_s; d[y][22] = shoes_s
        if accessory == "labcoat":
            for y in range(sy, sy + 9):
                d[y][8] = WH; d[y][9] = WH; d[y][22] = WH; d[y][23] = WH
        return d
    
    def _back_walk1():
        base = _back_idle()
        for y in range(37, min(48, 46)):
            for x in range(7, 25): base[y][x] = T
        for y in range(37, 43):
            for x in range(8, 15): base[y][x] = pants
        for y in range(43, min(46, 48)):
            for x in range(7, 14): base[y][x] = shoes
        for y in range(37, 42):
            for x in range(17, 22): base[y][x] = pants_s
        for y in range(42, min(45, 48)):
            for x in range(17, 22): base[y][x] = shoes_s
        return base
    
    def _back_walk2():
        base = _back_idle()
        for y in range(37, min(48, 46)):
            for x in range(7, 25): base[y][x] = T
        for y in range(37, 43):
            for x in range(17, 24): base[y][x] = pants
        for y in range(43, min(46, 48)):
            for x in range(18, 25): base[y][x] = shoes
        for y in range(37, 42):
            for x in range(10, 15): base[y][x] = pants_s
        for y in range(42, min(45, 48)):
            for x in range(10, 15): base[y][x] = shoes_s
        return base
    
    def _left_idle():
        d = [[T]*32 for _ in range(48)]
        hy = 10
        if hat:
            for x in range(10, 20): d[hy][x] = hat
            for x in range(9, 21): d[hy+1][x] = hat
            for x in range(8, 21): d[hy+2][x] = hat_s or hat
            for x in range(5, 18): d[hy+3][x] = hat_s or hat
            ch_start = hy + 4
        else:
            for x in range(10, 20): d[hy][x] = hair
            for x in range(9, 21): d[hy+1][x] = hair
            for x in range(9, 21): d[hy+2][x] = hair
            ch_start = hy + 3
        d[ch_start][18] = hair; d[ch_start][19] = hair; d[ch_start][20] = hair
        for y in range(ch_start, ch_start + 3):
            d[y][18] = hair; d[y][19] = hair
        for y in range(ch_start + 1, ch_start + 7):
            for x in range(10, 18): d[y][x] = skin
            d[y][10] = skin_s
        ey = ch_start + 3
        d[ey][11] = EY1; d[ey][12] = EY1
        d[ch_start + 5][10] = skin_s; d[ch_start + 5][11] = skin_s
        ny = ch_start + 7
        d[ny][13] = skin_s; d[ny][14] = skin; d[ny][15] = skin
        sy = ny + 1
        for y in range(sy, sy + 9):
            for x in range(10, 21): d[y][x] = shirt
            d[y][10] = shirt_s
        for y in range(sy + 1, sy + 7):
            d[y][9] = shirt_s; d[y][21] = shirt_s
        d[sy+7][9] = skin; d[sy+7][10] = skin
        by = sy + 9
        for x in range(10, 21): d[by][x] = BK
        py = by + 1
        for y in range(py, py + 9):
            for x in range(11, 20): d[y][x] = pants
            d[y][11] = pants_s
        shoe_y = py + 9
        for y in range(shoe_y, min(shoe_y + 3, 48)):
            for x in range(9, 20): d[y][x] = shoes
            d[y][9] = shoes_s
        return d
    
    def _left_walk1():
        base = _left_idle()
        for y in range(37, min(48, 46)):
            for x in range(6, 23): base[y][x] = T
        for y in range(37, 43):
            for x in range(8, 15): base[y][x] = pants
        for y in range(43, min(46, 48)):
            for x in range(6, 14): base[y][x] = shoes
        for y in range(37, 42):
            for x in range(16, 21): base[y][x] = pants_s
        for y in range(42, min(45, 48)):
            for x in range(17, 21): base[y][x] = shoes_s
        return base
    
    def _left_walk2():
        base = _left_idle()
        for y in range(37, min(48, 46)):
            for x in range(6, 23): base[y][x] = T
        for y in range(37, 43):
            for x in range(16, 22): base[y][x] = pants
        for y in range(43, min(46, 48)):
            for x in range(17, 24): base[y][x] = shoes
        for y in range(37, 42):
            for x in range(10, 15): base[y][x] = pants_s
        for y in range(42, min(45, 48)):
            for x in range(10, 14): base[y][x] = shoes_s
        return base
    
    return {
        "bas": [_front_idle, _front_walk1, _front_walk2],
        "haut": [_back_idle, _back_walk1, _back_walk2],
        "gauche": [_left_idle, _left_walk1, _left_walk2],
        "droite": [
            lambda: mirror_h(_left_idle()),
            lambda: mirror_h(_left_walk1()),
            lambda: mirror_h(_left_walk2()),
        ]
    }


# ==========================================================================
# DÉFINITIONS DES PERSONNAGES
# ==========================================================================

CHARACTERS = {}

# --- JOUEUR (Red) ---
CHARACTERS["red_normal"] = {
    "custom": {
        "bas": [player_front_idle, player_front_walk1, player_front_walk2],
        "haut": [player_back_idle, player_back_walk1, player_back_walk2],
        "gauche": [player_left_idle, player_left_walk1, player_left_walk2],
        "droite": [
            lambda: mirror_h(player_left_idle()),
            lambda: mirror_h(player_left_walk1()),
            lambda: mirror_h(player_left_walk2()),
        ]
    }
}

# --- PNJ Homme ---
CHARACTERS["pnj_homme"] = {
    "generic": {
        "hair": (56, 40, 32, 255), "hair2": (72, 56, 48, 255),
        "shirt": (80, 128, 56, 255), "shirt_s": (56, 96, 40, 255),
    }
}

# --- PNJ Femme ---
CHARACTERS["pnj_femme"] = {
    "generic": {
        "hair": (160, 72, 40, 255), "hair2": (184, 96, 56, 255),
        "shirt": (200, 72, 112, 255), "shirt_s": (168, 48, 88, 255),
        "skirt": True,
    }
}

# --- PNJ Fille ---
CHARACTERS["pnj_fille"] = {
    "generic": {
        "hair": (208, 152, 56, 255), "hair2": (224, 176, 80, 255),
        "shirt": (240, 128, 160, 255), "shirt_s": (216, 96, 128, 255),
        "skirt": True,
        "shoes": (240, 120, 120, 255), "shoes_s": (200, 88, 88, 255),
    }
}

# --- PNJ Garçon ---
CHARACTERS["pnj_garcon"] = {
    "generic": {
        "hair": (56, 40, 32, 255), "hair2": (72, 56, 48, 255),
        "hat": (56, 120, 200, 255), "hat_s": (40, 88, 168, 255),
        "shirt": (240, 200, 56, 255), "shirt_s": (208, 168, 40, 255),
        "pants": (112, 72, 48, 255), "pants_s": (88, 56, 32, 255),
    }
}

# --- Scientifique ---
CHARACTERS["pnj_scientifique"] = {
    "generic": {
        "hair": (160, 160, 168, 255), "hair2": (176, 176, 184, 255),
        "shirt": (240, 240, 248, 255), "shirt_s": (208, 208, 216, 255),
        "accessory": "labcoat",
    }
}

# --- Infirmière ---
CHARACTERS["pnj_infirmiere"] = {
    "generic": {
        "hair": (232, 120, 160, 255), "hair2": (248, 144, 176, 255),
        "hat": (248, 248, 248, 255), "hat_s": (224, 224, 232, 255),
        "shirt": (248, 248, 248, 255), "shirt_s": (224, 224, 232, 255),
        "accessory": "nurse_cross",
        "skirt": True,
    }
}
CHARACTERS["infirmiere"] = CHARACTERS["pnj_infirmiere"]

# --- Vendeur ---
CHARACTERS["pnj_vendeur"] = {
    "generic": {
        "shirt": (72, 136, 72, 255), "shirt_s": (48, 104, 48, 255),
        "hat": (72, 136, 72, 255), "hat_s": (48, 104, 48, 255),
    }
}

# --- Rocket ---
ROCKET = {
    "hair": HR1, "hair2": HR2,
    "hat": (32, 32, 40, 255), "hat_s": (48, 48, 56, 255),
    "shirt": (32, 32, 40, 255), "shirt_s": (48, 48, 56, 255),
    "pants": (32, 32, 40, 255), "pants_s": (48, 48, 56, 255),
    "shoes": (88, 88, 96, 255), "shoes_s": (64, 64, 72, 255),
    "accessory": "rocket_R",
}
CHARACTERS["pnj_rocket"] = {"generic": ROCKET}
CHARACTERS["pnj_rocket_homme"] = {"generic": ROCKET}
CHARACTERS["rocket_m"] = {"generic": ROCKET}
CHARACTERS["pnj_rocket_femme"] = {"generic": {
    **ROCKET, "hair": (184, 48, 96, 255), "hair2": (200, 72, 112, 255), "skirt": True
}}

# --- Champion (générique) ---
CHARACTERS["pnj_champion"] = {"generic": {
    "hat": (200, 168, 56, 255), "hat_s": (168, 136, 40, 255),
    "shirt": (200, 56, 56, 255), "shirt_s": (168, 40, 40, 255),
}}
CHARACTERS["champion"] = CHARACTERS["pnj_champion"]
CHARACTERS["pnj_champion_bob"] = {"generic": {
    "skin": (168, 120, 72, 255), "skin_s": (136, 96, 56, 255),
    "shirt": (200, 120, 48, 255), "shirt_s": (168, 96, 32, 255),
}}
CHARACTERS["pnj_champion_ondine"] = {"generic": {
    "hair": (200, 120, 48, 255), "hair2": (216, 144, 72, 255),
    "shirt": (72, 152, 200, 255), "shirt_s": (48, 120, 168, 255),
    "skirt": True,
}}
CHARACTERS["champion_erika"] = {"generic": {
    "hair": (32, 32, 40, 255), "hair2": (56, 48, 48, 255),
    "shirt": (120, 200, 80, 255), "shirt_s": (88, 168, 56, 255),
    "skirt": True,
}}

# --- Vieux/Vieil homme ---
CHARACTERS["pnj_vieux"] = {"generic": {
    "hair": (200, 200, 208, 255), "hair2": (216, 216, 224, 255),
    "shirt": (160, 128, 96, 255), "shirt_s": (128, 96, 64, 255),
}}
CHARACTERS["pnj_vieil_homme"] = CHARACTERS["pnj_vieux"]

# --- Marin ---
CHARACTERS["pnj_marin"] = {"generic": {
    "hat": (248, 248, 248, 255), "hat_s": (224, 224, 232, 255),
    "shirt": (248, 248, 248, 255), "shirt_s": (224, 224, 232, 255),
    "pants": (56, 56, 120, 255), "pants_s": (40, 40, 88, 255),
}}

# --- Divers PNJ ---
for name, cfg in [
    ("pnj_gamin", {"hat": (56, 168, 56, 255), "hat_s": (40, 136, 40, 255),
                    "shirt": (248, 200, 56, 255), "shirt_s": (216, 168, 40, 255)}),
    ("pnj_gamine", {"hair": (208, 128, 56, 255), "hair2": (224, 152, 80, 255),
                     "shirt": (200, 128, 200, 255), "shirt_s": (168, 96, 168, 255), "skirt": True}),
    ("pnj_motard", {"shirt": (56, 56, 56, 255), "shirt_s": (40, 40, 40, 255),
                     "pants": (56, 56, 56, 255), "pants_s": (40, 40, 40, 255)}),
    ("pnj_karateka", {"shirt": (248, 248, 248, 255), "shirt_s": (224, 224, 232, 255),
                       "pants": (248, 248, 248, 255), "pants_s": (224, 224, 232, 255)}),
    ("pnj_nageur", {"shirt": (72, 152, 216, 255), "shirt_s": (48, 120, 184, 255)}),
    ("pnj_nageuse", {"shirt": (200, 72, 112, 255), "shirt_s": (168, 48, 88, 255), "skirt": True}),
    ("pnj_pecheur", {"hat": (168, 120, 56, 255), "hat_s": (136, 96, 40, 255),
                      "shirt": (120, 168, 72, 255), "shirt_s": (88, 136, 48, 255)}),
    ("pnj_medium", {"shirt": (120, 56, 168, 255), "shirt_s": (88, 40, 136, 255)}),
    ("pnj_dresseur", {"hat": (200, 56, 56, 255), "hat_s": (168, 40, 40, 255),
                       "shirt": (200, 200, 56, 255), "shirt_s": (168, 168, 40, 255)}),
    ("pnj_dresseur_m", {"hat": (200, 56, 56, 255), "hat_s": (168, 40, 40, 255),
                         "shirt": (200, 200, 56, 255), "shirt_s": (168, 168, 40, 255)}),
    ("dresseur", {"hat": (200, 56, 56, 255), "hat_s": (168, 40, 40, 255),
                   "shirt": (200, 200, 56, 255), "shirt_s": (168, 168, 40, 255)}),
    ("dresseur_m", {"hat": (200, 56, 56, 255), "hat_s": (168, 40, 40, 255),
                     "shirt": (200, 200, 56, 255), "shirt_s": (168, 168, 40, 255)}),
    ("dresseur_f", {"hair": (160, 72, 40, 255), "hair2": (184, 96, 56, 255),
                     "shirt": (200, 72, 112, 255), "shirt_s": (168, 48, 88, 255), "skirt": True}),
    ("dresseur_randonneur", {"hat": (136, 96, 48, 255), "hat_s": (104, 72, 32, 255),
                              "shirt": (136, 168, 72, 255), "shirt_s": (104, 136, 48, 255)}),
    ("pnj_giovanni", {"shirt": (200, 120, 48, 255), "shirt_s": (168, 96, 32, 255)}),
    ("pnj_jongleur", {"shirt": (200, 56, 200, 255), "shirt_s": (168, 40, 168, 255)}),
    ("pnj_garde", {"hat": (56, 56, 120, 255), "hat_s": (40, 40, 88, 255),
                    "shirt": (56, 80, 160, 255), "shirt_s": (40, 56, 128, 255)}),
    ("pnj_capitaine", {"hat": (248, 248, 248, 255), "hat_s": (224, 224, 232, 255),
                        "shirt": (56, 56, 120, 255), "shirt_s": (40, 40, 88, 255)}),
    ("pnj_fillette", {"hair": (208, 128, 56, 255), "hair2": (224, 152, 80, 255),
                       "shirt": (240, 168, 200, 255), "shirt_s": (216, 136, 168, 255), "skirt": True}),
    ("pnj_montagnard", {"hat": (136, 96, 48, 255), "hat_s": (104, 72, 32, 255),
                          "shirt": (160, 120, 80, 255), "shirt_s": (128, 88, 56, 255)}),
    ("pnj_randonneur", {"hat": (136, 96, 48, 255), "hat_s": (104, 72, 32, 255),
                          "shirt": (136, 168, 72, 255), "shirt_s": (104, 136, 48, 255)}),
    ("pnj_randonneuse", {"hair": (160, 72, 40, 255), "hair2": (184, 96, 56, 255),
                           "shirt": (136, 168, 72, 255), "shirt_s": (104, 136, 48, 255), "skirt": True}),
    ("pnj_campeur", {"hat": (56, 120, 200, 255), "hat_s": (40, 88, 168, 255),
                      "shirt": (200, 120, 48, 255), "shirt_s": (168, 96, 32, 255)}),
    ("pnj_insectomane", {"hat": (248, 248, 248, 255), "hat_s": (224, 224, 232, 255),
                          "shirt": (168, 200, 56, 255), "shirt_s": (136, 168, 40, 255)}),
    ("pnj_canon", {"shirt": (200, 56, 56, 255), "shirt_s": (168, 40, 40, 255)}),
]:
    CHARACTERS[name] = {"generic": cfg}


# ==========================================================================
# OBJETS STATIQUES (panneau, PC, etc.) 
# ==========================================================================

def make_sign_post():
    """Panneau en bois."""
    d = [[T]*32 for _ in range(48)]
    # Poteau
    for y in range(28, 46):
        for x in range(14, 18): d[y][x] = (120, 80, 40, 255)
        d[y][14] = (96, 64, 32, 255)
    # Panneau
    for y in range(14, 28):
        for x in range(6, 26): d[y][x] = (168, 128, 80, 255)
    for y in range(15, 27):
        for x in range(7, 25): d[y][x] = (184, 144, 96, 255)
    # Bord
    for x in range(6, 26): d[14][x] = (120, 80, 40, 255); d[27][x] = (120, 80, 40, 255)
    for y in range(14, 28): d[y][6] = (120, 80, 40, 255); d[y][25] = (120, 80, 40, 255)
    # Texte lignes
    for x in range(9, 23): d[18][x] = (96, 64, 32, 255)
    for x in range(9, 20): d[21][x] = (96, 64, 32, 255)
    for x in range(9, 22): d[24][x] = (96, 64, 32, 255)
    return d

def make_item_ball():
    """Pokéball au sol."""
    d = [[T]*32 for _ in range(48)]
    cx, cy = 16, 32
    for y in range(cy-6, cy+7):
        for x in range(cx-6, cx+7):
            dist = ((x-cx)**2 + (y-cy)**2)**0.5
            if dist < 6:
                if y < cy:
                    d[y][x] = (232, 56, 56, 255)
                else:
                    d[y][x] = (248, 248, 248, 255)
            elif dist < 7:
                d[y][x] = BK
    # Ligne centrale
    for x in range(cx-6, cx+7):
        d[cy][x] = BK
    # Bouton
    d[cy][cx] = (248, 248, 248, 255)
    d[cy-1][cx] = BK; d[cy+1][cx] = BK; d[cy][cx-1] = BK; d[cy][cx+1] = BK
    return d

def make_pc_terminal():
    """Terminal PC."""
    d = [[T]*32 for _ in range(48)]
    # Écran
    for y in range(16, 34):
        for x in range(8, 24): d[y][x] = (176, 176, 184, 255)
    for y in range(17, 31):
        for x in range(9, 23): d[y][x] = (32, 104, 48, 255)
    for y in range(18, 30):
        for x in range(10, 22): d[y][x] = (48, 168, 64, 255)
    # Pied
    for y in range(34, 40):
        for x in range(13, 19): d[y][x] = (160, 160, 168, 255)
    # Clavier
    for y in range(40, 44):
        for x in range(8, 24): d[y][x] = (192, 192, 200, 255)
    return d

def make_snorlax():
    """Ronflex bloquant."""
    d = [[T]*32 for _ in range(48)]
    cx, cy = 16, 30
    for y in range(16, 46):
        for x in range(4, 28):
            dx, dy = (x-cx)/12, (y-cy)/14
            if dx*dx + dy*dy < 1:
                if y < 22:
                    d[y][x] = (80, 96, 104, 255)  # tête foncée
                else:
                    d[y][x] = (216, 208, 176, 255)  # ventre
    # Tête
    for y in range(16, 24):
        for x in range(8, 24):
            dx = (x-cx)/8
            dy = (y-20)/5
            if dx*dx + dy*dy < 1:
                d[y][x] = (80, 96, 104, 255)
    # Yeux fermés
    for x in range(11, 14): d[20][x] = BK
    for x in range(18, 21): d[20][x] = BK
    return d

STATIC_SPRITES = {
    "panneau": make_sign_post,
    "pnj_panneau": make_sign_post,
    "pnj_objet": make_item_ball,
    "item_sol": make_item_ball,
    "pnj_pc": make_pc_terminal,
    "pc": make_pc_terminal,
    "pnj_ronflex": make_snorlax,
    "pokemon_legendaire": make_snorlax,
    "pnj_legendaire": make_snorlax,
}


# ==========================================================================
# SAUVEGARDE
# ==========================================================================

def save_sprite(name, direction, frame, data):
    path = os.path.join(OUT_DIR, f"{name}_{direction}_{frame}.png")
    img = make_img(data)
    img.save(path, "PNG")
    return path

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    count = 0
    
    for char_name, char_def in CHARACTERS.items():
        if "custom" in char_def:
            frames = char_def["custom"]
        else:
            cfg = char_def["generic"]
            gen = make_generic_char(cfg)
            frames = gen
        
        for direction, frame_funcs in frames.items():
            for i, func in enumerate(frame_funcs):
                data = func()
                save_sprite(char_name, direction, i, data)
                count += 1
    
    # Sprites statiques (même image pour toutes les directions)
    for name, func in STATIC_SPRITES.items():
        data = func()
        for direction in ["bas", "haut", "gauche", "droite"]:
            for i in range(3):
                save_sprite(name, direction, i, data)
                count += 1
    
    print(f"Total: {count} fichiers générés dans {OUT_DIR}/")

if __name__ == "__main__":
    main()
