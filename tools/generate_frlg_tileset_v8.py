#!/usr/bin/env python3
"""
Générateur Tileset v8 — Style FRLG fidèle, pixel art soigné
============================================================
256×192 px (8×6 = 48 tiles de 32×32)
Chaque tile est dessinée pixel-par-pixel pour reproduire le style
Pokémon Rouge Feu / Vert Feuille.
"""
from PIL import Image, ImageDraw
import os, random

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "tilesets")

# ============================================================================
# Palette FRLG fidèle
# ============================================================================
# Herbe
G1 = (80, 184, 56)     # vert clair herbe
G2 = (56, 152, 40)     # vert moyen herbe
G3 = (40, 128, 32)     # vert foncé herbe

# Herbe haute
HG1 = (48, 168, 40)    # vert haute herbe
HG2 = (32, 136, 24)    # vert foncé haute herbe
HG3 = (24, 112, 16)    # vert très foncé

# Chemin
P1 = (216, 200, 152)   # sable chemin
P2 = (192, 176, 128)   # sable ombre
P3 = (168, 152, 104)   # bordure chemin

# Sable
S1 = (240, 224, 168)   # sable clair
S2 = (216, 200, 144)   # sable moyen
S3 = (192, 176, 120)   # sable ombre

# Eau
W1 = (64, 128, 216)    # eau clair
W2 = (48, 104, 192)    # eau moyen
W3 = (32, 80, 168)     # eau foncé
WH = (128, 184, 248)   # reflet eau

# Fleurs
FL1 = (248, 80, 80)    # pétale rouge
FL2 = (248, 248, 80)   # pétale jaune
FL3 = (248, 248, 248)  # pétale blanc

# Arbre
TG1 = (32, 128, 32)    # canopée clair
TG2 = (16, 96, 16)     # canopée foncé
TG3 = (8, 72, 8)       # canopée très foncé
TB1 = (120, 80, 40)    # tronc
TB2 = (88, 56, 24)     # tronc ombre

# Clôture
FC1 = (200, 168, 120)  # bois clair
FC2 = (168, 136, 88)   # bois foncé

# Buisson
BU1 = (48, 152, 48)    # buisson clair
BU2 = (32, 120, 32)    # buisson foncé
BU3 = (24, 96, 24)     # buisson ombre

# Toit maison (rouge FRLG)
R1 = (208, 72, 48)     # toit rouge clair
R2 = (176, 48, 32)     # toit rouge moyen
R3 = (144, 32, 16)     # toit rouge foncé

# Mur maison
MW1 = (240, 232, 208)  # mur crème clair
MW2 = (216, 208, 184)  # mur crème ombre
MW3 = (192, 184, 160)  # mur bordure

# Porte
DR1 = (136, 88, 40)    # porte bois
DR2 = (104, 64, 24)    # porte bois foncé
DK  = (48, 32, 16)     # porte très foncé

# Fenêtre
FW1 = (160, 208, 248)  # vitre clair
FW2 = (120, 168, 216)  # vitre ombre
FWF = (128, 112, 80)   # cadre fenêtre

# Intérieur — Parquet
IW1 = (200, 168, 112)  # parquet clair
IW2 = (176, 144, 96)   # parquet foncé
IW3 = (152, 120, 72)   # parquet lignes

# Mur intérieur
IM1 = (232, 224, 200)  # mur int clair
IM2 = (208, 200, 176)  # mur int moyen
IM3 = (184, 176, 152)  # plinthes

# Comptoir (bleu Pokémon Center)
CT1 = (72, 136, 200)   # comptoir bleu
CT2 = (48, 104, 168)   # comptoir bleu foncé

# Machine Soin (rose)
MS1 = (248, 168, 168)  # machine rose
MS2 = (224, 120, 120)  # machine rose foncé
MSL = (248, 248, 128)  # lumière jaune

# Étagère
SH1 = (176, 136, 88)   # étagère bois
SH2 = (144, 104, 64)   # étagère ombre

# Tapis rouge
TP1 = (200, 56, 40)    # tapis rouge
TP2 = (168, 40, 24)    # tapis bordeaux

# Carrelage
CR1 = (232, 232, 240)  # carrelage blanc
CR2 = (208, 208, 216)  # carrelage gris

# Meubles chambre
LT1 = (248, 248, 248)  # lit blanc
LT2 = (200, 200, 208)  # lit ombre
LB1 = (80, 136, 200)   # couverture bleue
LB2 = (56, 104, 168)   # couverture bleue foncé

# TV / PC
TV1 = (56, 56, 64)     # écran off
TV2 = (128, 200, 128)  # écran on vert
TV3 = (80, 80, 88)     # boîtier

# Plante
PL1 = (64, 168, 56)    # feuille
PL2 = (40, 128, 32)    # feuille foncé
PP1 = (184, 120, 72)   # pot

# Escaliers
ES1 = (160, 128, 88)   # marche
ES2 = (128, 96, 64)    # marche ombre

# Sol bois foncé
DB1 = (152, 120, 80)   # bois foncé
DB2 = (128, 96, 64)    # bois très foncé

# Table / Chaise
TA1 = (176, 136, 80)   # table bois
TA2 = (144, 104, 56)   # table ombre
CH1 = (200, 56, 40)    # chaise rouge

# Poster / Poubelle
PO1 = (200, 200, 128)  # poster
PB1 = (160, 160, 168)  # poubelle gris
PB2 = (128, 128, 136)  # poubelle ombre

BLK = (16, 16, 16)     # noir contour

def R(draw, x, y, w, h, col):
    """Rectangle rempli."""
    draw.rectangle([x, y, x+w-1, y+h-1], fill=col)

def Px(draw, x, y, col):
    """Pixel unique."""
    draw.point((x, y), fill=col)

# ============================================================================
# Tile 0 — Herbe (base)
# ============================================================================
def tile_herbe(d, x0, y0):
    R(d, x0, y0, 32, 32, G1)
    # Motif de brins d'herbe typique FRLG
    for gy in range(0, 32, 8):
        for gx in range(0, 32, 8):
            ox = x0 + gx
            oy = y0 + gy
            # Petit brin en V
            Px(d, ox+2, oy+3, G2)
            Px(d, ox+3, oy+2, G2)
            Px(d, ox+4, oy+3, G2)
            # Deuxième motif décalé
            Px(d, ox+6, oy+6, G3)
            Px(d, ox+7, oy+5, G3)

# Tile 1 — Herbe haute
def tile_herbe_haute(d, x0, y0):
    R(d, x0, y0, 32, 32, HG1)
    for gy in range(0, 32, 4):
        for gx in range(0, 32, 6):
            ox = x0 + gx + (gy % 8 == 4) * 3
            oy = y0 + gy
            if ox < x0 + 32:
                Px(d, ox, oy+1, HG2)
                Px(d, ox+1, oy, HG2)
                Px(d, ox+2, oy+1, HG2)
                if oy + 2 < y0 + 32:
                    Px(d, ox, oy+2, HG3)
                    Px(d, ox+2, oy+2, HG3)

# Tile 2 — Chemin
def tile_chemin(d, x0, y0):
    R(d, x0, y0, 32, 32, P1)
    # Petits cailloux
    for i in range(6):
        cx = x0 + random.randint(2, 28)
        cy = y0 + random.randint(2, 28)
        Px(d, cx, cy, P2)
    # Bordure subtile
    for x in range(32):
        Px(d, x0+x, y0, P2)
        Px(d, x0+x, y0+31, P2)

# Tile 3 — Sable
def tile_sable(d, x0, y0):
    R(d, x0, y0, 32, 32, S1)
    for i in range(10):
        Px(d, x0 + random.randint(0, 31), y0 + random.randint(0, 31), S2)
    for i in range(4):
        Px(d, x0 + random.randint(0, 31), y0 + random.randint(0, 31), S3)

# Tile 4 — Eau
def tile_eau(d, x0, y0):
    R(d, x0, y0, 32, 32, W2)
    # Vagues horizontales style FRLG
    for wy in range(0, 32, 8):
        for wx in range(0, 32, 4):
            Px(d, x0 + wx, y0 + wy, W1)
            Px(d, x0 + wx + 1, y0 + wy, WH)
            Px(d, x0 + wx + 2, y0 + wy, W1)
        # Ligne foncée dessous
        for wx in range(32):
            Px(d, x0 + wx, y0 + wy + 4, W3)

# Tile 5 — Fleurs
def tile_fleurs(d, x0, y0):
    R(d, x0, y0, 32, 32, G1)
    # Herbe de base
    for gy in range(0, 32, 8):
        for gx in range(0, 32, 8):
            Px(d, x0+gx+3, y0+gy+2, G2)
    # Fleurs colorées
    positions = [(4, 4, FL1), (12, 2, FL2), (24, 6, FL3),
                 (8, 14, FL3), (20, 12, FL1), (28, 16, FL2),
                 (2, 22, FL2), (16, 24, FL1), (26, 22, FL3),
                 (6, 28, FL1), (18, 30, FL2)]
    for fx, fy, col in positions:
        if fx < 31 and fy < 31:
            Px(d, x0+fx, y0+fy, col)
            Px(d, x0+fx+1, y0+fy, col)
            Px(d, x0+fx, y0+fy+1, col)
            Px(d, x0+fx+1, y0+fy+1, col)

# Tile 6 — Herbe + cailloux
def tile_herbe_cailloux(d, x0, y0):
    R(d, x0, y0, 32, 32, G1)
    # Brins
    for gy in range(0, 32, 8):
        for gx in range(0, 32, 8):
            Px(d, x0+gx+3, y0+gy+2, G2)
    # Cailloux gris
    stones = [(6, 8), (18, 4), (10, 20), (24, 16), (14, 28)]
    for sx, sy in stones:
        R(d, x0+sx, y0+sy, 4, 3, (168, 168, 176))
        R(d, x0+sx+1, y0+sy, 2, 1, (200, 200, 208))
        R(d, x0+sx, y0+sy+2, 4, 1, (136, 136, 144))

# Tile 7 — Transition herbe/chemin
def tile_transition(d, x0, y0):
    # Moitié haute herbe, moitié basse chemin
    R(d, x0, y0, 32, 16, G1)
    R(d, x0, y0+16, 32, 16, P1)
    # Bordure diagonale douce
    for x in range(32):
        y_mid = 16 + int(2 * (0.5 - abs(x / 32.0 - 0.5)))
        Px(d, x0+x, y0+y_mid-1, G2)
        Px(d, x0+x, y0+y_mid, P2)

# ============================================================================
# Row 1 — Végétation
# ============================================================================

# Tile 8 — Arbre haut gauche (canopée)
def tile_arbre_hg(d, x0, y0):
    R(d, x0, y0, 32, 32, (0, 0, 0, 0))  # transparent (sera sur herbe)
    # Canopée arrondie - partie haute gauche
    # Forme : rond en haut, descend vers le tronc
    # Contour
    for y in range(4, 32):
        for x in range(0, 32):
            # Forme ovale : centre (16, 16), rayon x=15, rayon y=14
            dx = (x - 16)
            dy = (y - 14)
            if dx*dx / 240.0 + dy*dy / 200.0 <= 1.0:
                if dx*dx / 200.0 + dy*dy / 170.0 <= 1.0:
                    # Intérieur
                    if dy < -2:
                        Px(d, x0+x, y0+y, TG1)
                    elif dx < 0:
                        Px(d, x0+x, y0+y, TG2)
                    else:
                        Px(d, x0+x, y0+y, TG1)
                else:
                    # Bordure
                    Px(d, x0+x, y0+y, TG3)
    # Reflets lumineux
    for ly in range(6, 12):
        for lx in range(8, 16):
            if random.random() < 0.3:
                if 0 <= lx < 32 and 0 <= ly < 32:
                    Px(d, x0+lx, y0+ly, TG1)

# Tile 9 — Arbre bas gauche (tronc)
def tile_arbre_bg(d, x0, y0):
    R(d, x0, y0, 32, 32, (0, 0, 0, 0))
    # Suite de la canopée en haut
    for y in range(0, 16):
        for x in range(2, 30):
            dx = (x - 16)
            dy = (y + 18 - 14)  # continuation de la forme du dessus
            if dx*dx / 240.0 + dy*dy / 200.0 <= 1.0:
                if dx*dx / 200.0 + dy*dy / 170.0 <= 1.0:
                    Px(d, x0+x, y0+y, TG2 if dx > 2 else TG1)
                else:
                    Px(d, x0+x, y0+y, TG3)
    # Tronc
    R(d, x0+12, y0+12, 8, 20, TB1)
    R(d, x0+12, y0+12, 2, 20, TB2)
    # Herbe à la base
    R(d, x0, y0+28, 32, 4, G1)
    R(d, x0, y0+28, 32, 1, G2)

# Tile 10 — Arbre haut droit (similaire à 8 mais décalé)
def tile_arbre_hd(d, x0, y0):
    tile_arbre_hg(d, x0, y0)  # Même canopée (les arbres sont symétriques)

# Tile 11 — Arbre bas droit
def tile_arbre_bd(d, x0, y0):
    tile_arbre_bg(d, x0, y0)

# Tile 12 — Clôture horizontale
def tile_cloture_h(d, x0, y0):
    R(d, x0, y0, 32, 32, G1)  # herbe dessous
    # Poteaux
    R(d, x0+2, y0+10, 4, 14, FC2)
    R(d, x0+3, y0+10, 2, 14, FC1)
    R(d, x0+26, y0+10, 4, 14, FC2)
    R(d, x0+27, y0+10, 2, 14, FC1)
    # Barres horizontales
    R(d, x0, y0+14, 32, 3, FC2)
    R(d, x0, y0+15, 32, 1, FC1)
    R(d, x0, y0+20, 32, 3, FC2)
    R(d, x0, y0+21, 32, 1, FC1)

# Tile 13 — Clôture verticale
def tile_cloture_v(d, x0, y0):
    R(d, x0, y0, 32, 32, G1)
    # Poteau central vertical
    R(d, x0+13, y0, 6, 32, FC2)
    R(d, x0+14, y0, 4, 32, FC1)
    # Petits traversins
    R(d, x0+11, y0+6, 10, 3, FC2)
    R(d, x0+11, y0+7, 10, 1, FC1)
    R(d, x0+11, y0+22, 10, 3, FC2)
    R(d, x0+11, y0+23, 10, 1, FC1)

# Tile 14 — Buisson
def tile_buisson(d, x0, y0):
    R(d, x0, y0, 32, 32, G1)
    # Buisson rond
    for y in range(6, 28):
        for x in range(4, 28):
            dx = x - 16
            dy = y - 17
            if dx*dx / 144.0 + dy*dy / 100.0 <= 1.0:
                if dx*dx / 120.0 + dy*dy / 80.0 <= 1.0:
                    c = BU1 if dy < -2 else BU2
                    Px(d, x0+x, y0+y, c)
                else:
                    Px(d, x0+x, y0+y, BU3)

# Tile 15 — Herbe détail
def tile_herbe_detail(d, x0, y0):
    R(d, x0, y0, 32, 32, G1)
    # Touffes d'herbe plus visibles
    for gy in range(0, 32, 6):
        for gx in range(0, 32, 8):
            ox = x0 + gx + (gy % 12 == 6) * 4
            oy = y0 + gy
            if ox + 3 <= x0 + 32:
                Px(d, ox, oy+2, G3)
                Px(d, ox+1, oy+1, G2)
                Px(d, ox+2, oy, G3)
                Px(d, ox+3, oy+1, G2)
                Px(d, ox+1, oy+3, G3)
                Px(d, ox+2, oy+3, G3)

# ============================================================================
# Row 2 — Maisons extérieur (style FRLG)
# ============================================================================

# Tile 16 — Toit gauche
def tile_toit_g(d, x0, y0):
    # Toit rouge en pente vers la gauche
    R(d, x0, y0, 32, 32, R2)
    # Lignes de tuiles horizontales
    for ty in range(0, 32, 4):
        R(d, x0, y0+ty, 32, 1, R3)
        R(d, x0, y0+ty+1, 32, 1, R1)
    # Bord gauche (descente)
    for y in range(32):
        R(d, x0, y0+y, 2, 1, R3)
    # Bord bas
    R(d, x0, y0+30, 32, 2, R3)
    # Faîtière en haut
    R(d, x0, y0, 32, 3, R3)
    R(d, x0+2, y0+1, 28, 1, R1)

# Tile 17 — Toit milieu
def tile_toit_m(d, x0, y0):
    R(d, x0, y0, 32, 32, R2)
    for ty in range(0, 32, 4):
        R(d, x0, y0+ty, 32, 1, R3)
        R(d, x0, y0+ty+1, 32, 1, R1)
    # Faîtière
    R(d, x0, y0, 32, 3, R3)
    R(d, x0, y0+1, 32, 1, R1)
    # Bord bas
    R(d, x0, y0+30, 32, 2, R3)

# Tile 18 — Toit droit
def tile_toit_d(d, x0, y0):
    R(d, x0, y0, 32, 32, R2)
    for ty in range(0, 32, 4):
        R(d, x0, y0+ty, 32, 1, R3)
        R(d, x0, y0+ty+1, 32, 1, R1)
    # Bord droit
    for y in range(32):
        R(d, x0+30, y0+y, 2, 1, R3)
    R(d, x0, y0, 32, 3, R3)
    R(d, x0+2, y0+1, 28, 1, R1)
    R(d, x0, y0+30, 32, 2, R3)

# Tile 19 — Mur gauche
def tile_mur_g(d, x0, y0):
    R(d, x0, y0, 32, 32, MW1)
    # Bordure gauche
    R(d, x0, y0, 2, 32, MW3)
    # Ligne horizontale au milieu (séparation étage)
    R(d, x0, y0+15, 32, 2, MW3)
    # Texture briques subtile
    for by in range(0, 32, 8):
        for bx in range(4, 32, 12):
            off = 6 if (by // 8) % 2 else 0
            R(d, x0+bx+off, y0+by+3, 8, 1, MW2)

# Tile 20 — Mur milieu
def tile_mur_m(d, x0, y0):
    R(d, x0, y0, 32, 32, MW1)
    R(d, x0, y0+15, 32, 2, MW3)
    for by in range(0, 32, 8):
        for bx in range(0, 32, 12):
            off = 6 if (by // 8) % 2 else 0
            bx2 = bx + off
            if bx2 < 28:
                R(d, x0+bx2, y0+by+3, 8, 1, MW2)

# Tile 21 — Mur droit
def tile_mur_d(d, x0, y0):
    R(d, x0, y0, 32, 32, MW1)
    R(d, x0+30, y0, 2, 32, MW3)
    R(d, x0, y0+15, 32, 2, MW3)
    for by in range(0, 32, 8):
        for bx in range(0, 28, 12):
            off = 6 if (by // 8) % 2 else 0
            R(d, x0+bx+off, y0+by+3, 8, 1, MW2)

# Tile 22 — Porte
def tile_porte(d, x0, y0):
    R(d, x0, y0, 32, 32, MW1)
    # Cadre de porte
    R(d, x0+6, y0+2, 20, 28, DK)
    R(d, x0+8, y0+2, 16, 26, DR2)
    R(d, x0+9, y0+3, 14, 24, DR1)
    # Panneau haut
    R(d, x0+11, y0+5, 10, 8, DR2)
    # Panneau bas
    R(d, x0+11, y0+16, 10, 8, DR2)
    # Poignée
    R(d, x0+20, y0+16, 2, 3, (240, 216, 80))
    # Seuil
    R(d, x0+6, y0+28, 20, 4, MW3)
    R(d, x0+8, y0+29, 16, 2, P2)

# Tile 23 — Fenêtre extérieure
def tile_fenetre_ext(d, x0, y0):
    R(d, x0, y0, 32, 32, MW1)
    # Cadre bois
    R(d, x0+5, y0+4, 22, 20, FWF)
    # Vitre
    R(d, x0+7, y0+6, 18, 16, FW2)
    R(d, x0+8, y0+7, 7, 6, FW1)
    # Croisillon
    R(d, x0+15, y0+6, 2, 16, FWF)
    R(d, x0+7, y0+13, 18, 2, FWF)
    # Appui de fenêtre
    R(d, x0+4, y0+24, 24, 3, MW3)
    # Texture mur
    R(d, x0, y0+15, 5, 2, MW3)
    R(d, x0+27, y0+15, 5, 2, MW3)

# ============================================================================
# Row 3 — Intérieur base
# ============================================================================

# Tile 24 — Sol parquet
def tile_parquet(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Lames de parquet
    for py in range(0, 32, 8):
        R(d, x0, y0+py, 32, 1, IW3)
        off = 12 if (py // 8) % 2 else 0
        for px in range(off, 32, 16):
            R(d, x0+px, y0+py, 1, 8, IW3)
        # Reflet clair
        R(d, x0, y0+py+2, 32, 1, IW1)

# Tile 25 — Mur intérieur
def tile_mur_int(d, x0, y0):
    R(d, x0, y0, 32, 32, IM1)
    # Plinthes en bas
    R(d, x0, y0+26, 32, 6, IM3)
    R(d, x0, y0+26, 32, 1, IM2)
    # Ligne déco au milieu
    R(d, x0, y0+12, 32, 2, IM2)

# Tile 26 — Comptoir (Pokémon Center style)
def tile_comptoir(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)  # sol de base
    # Comptoir
    R(d, x0, y0+8, 32, 20, CT2)
    R(d, x0+1, y0+9, 30, 18, CT1)
    # Surface haute
    R(d, x0, y0+6, 32, 4, CT2)
    R(d, x0+1, y0+7, 30, 2, (96, 160, 224))
    # Détail vertical
    R(d, x0+15, y0+10, 2, 16, CT2)

# Tile 27 — Machine de soin
def tile_machine_soin(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Corps machine
    R(d, x0+6, y0+4, 20, 24, MS2)
    R(d, x0+8, y0+6, 16, 20, MS1)
    # Écran
    R(d, x0+10, y0+8, 12, 8, (200, 240, 200))
    # Croix rouge au centre
    R(d, x0+14, y0+9, 4, 6, (224, 48, 48))
    R(d, x0+12, y0+11, 8, 2, (224, 48, 48))
    # Slots Poké Balls
    for i in range(3):
        R(d, x0+10+i*4, y0+20, 3, 3, (248, 248, 248))
        R(d, x0+10+i*4, y0+21, 3, 1, (200, 200, 200))
    # Lumière
    R(d, x0+14, y0+4, 4, 2, MSL)

# Tile 28 — Étagère
def tile_etagere(d, x0, y0):
    R(d, x0, y0, 32, 32, IM1)
    # Étagère bois
    R(d, x0+2, y0+2, 28, 28, SH2)
    R(d, x0+4, y0+4, 24, 24, SH1)
    # Étagères horizontales
    R(d, x0+2, y0+12, 28, 2, SH2)
    R(d, x0+2, y0+20, 28, 2, SH2)
    # Livres colorés
    books = [(200, 56, 40), (56, 120, 200), (56, 168, 56), (200, 168, 40), (168, 56, 168)]
    for i, col in enumerate(books):
        R(d, x0+5+i*4, y0+5, 3, 7, col)
    for i, col in enumerate(books[:3]):
        R(d, x0+6+i*5, y0+14, 4, 6, col)

# Tile 29 — Tapis rouge
def tile_tapis(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Tapis
    R(d, x0+2, y0+2, 28, 28, TP2)
    R(d, x0+4, y0+4, 24, 24, TP1)
    # Bordure dorée
    R(d, x0+3, y0+3, 26, 1, (200, 168, 40))
    R(d, x0+3, y0+28, 26, 1, (200, 168, 40))
    R(d, x0+3, y0+3, 1, 26, (200, 168, 40))
    R(d, x0+28, y0+3, 1, 26, (200, 168, 40))

# Tile 30 — Sol carrelage
def tile_carrelage(d, x0, y0):
    R(d, x0, y0, 32, 32, CR1)
    # Lignes de joint
    for i in range(0, 32, 16):
        R(d, x0+i, y0, 1, 32, CR2)
        R(d, x0, y0+i, 32, 1, CR2)
    # Légère variation
    R(d, x0+1, y0+1, 14, 14, CR1)
    R(d, x0+17, y0+1, 14, 14, (224, 224, 232))

# Tile 31 — Mur motif
def tile_mur_motif(d, x0, y0):
    R(d, x0, y0, 32, 32, IM1)
    # Motif papier peint
    for py in range(0, 32, 8):
        for px in range(0, 32, 8):
            off = 4 if (py // 8) % 2 else 0
            R(d, x0+px+off+2, y0+py+2, 4, 4, IM2)
    # Plinthes
    R(d, x0, y0+26, 32, 6, IM3)

# ============================================================================
# Row 4 — Chambre
# ============================================================================

# Tile 32 — Lit tête
def tile_lit_tete(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Tête de lit
    R(d, x0+2, y0+4, 28, 8, SH2)
    R(d, x0+3, y0+5, 26, 6, SH1)
    # Oreiller
    R(d, x0+4, y0+12, 24, 8, LT1)
    R(d, x0+4, y0+18, 24, 2, LT2)
    # Couverture
    R(d, x0+2, y0+20, 28, 10, LB1)
    R(d, x0+4, y0+22, 24, 6, LB2)
    # Bordure lit
    R(d, x0+2, y0+4, 1, 26, SH2)
    R(d, x0+29, y0+4, 1, 26, SH2)

# Tile 33 — Lit pied
def tile_lit_pied(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Couverture (continuation)
    R(d, x0+2, y0, 28, 18, LB1)
    R(d, x0+4, y0+2, 24, 14, LB2)
    # Pied de lit
    R(d, x0+2, y0+18, 28, 6, SH2)
    R(d, x0+3, y0+19, 26, 4, SH1)
    # Bordures
    R(d, x0+2, y0, 1, 24, SH2)
    R(d, x0+29, y0, 1, 24, SH2)

# Tile 34 — TV
def tile_tv(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Meuble TV
    R(d, x0+4, y0+20, 24, 10, SH2)
    R(d, x0+5, y0+21, 22, 8, SH1)
    # TV elle-même
    R(d, x0+4, y0+2, 24, 20, TV3)
    R(d, x0+6, y0+4, 20, 14, TV1)
    R(d, x0+7, y0+5, 8, 6, TV2)  # reflet écran
    # Bouton
    R(d, x0+26, y0+17, 2, 2, (200, 56, 40))

# Tile 35 — PC
def tile_pc(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Bureau
    R(d, x0+2, y0+18, 28, 12, SH2)
    R(d, x0+3, y0+19, 26, 10, SH1)
    # Moniteur
    R(d, x0+6, y0+2, 20, 18, (72, 72, 80))
    R(d, x0+8, y0+4, 16, 12, (40, 80, 120))
    R(d, x0+9, y0+5, 6, 4, (80, 160, 200))  # reflet
    # Clavier
    R(d, x0+8, y0+20, 16, 4, (200, 200, 208))
    R(d, x0+9, y0+21, 14, 2, (232, 232, 240))

# Tile 36 — Plante
def tile_plante(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Pot
    R(d, x0+8, y0+20, 16, 10, PP1)
    R(d, x0+10, y0+18, 12, 4, PP1)
    R(d, x0+9, y0+20, 14, 1, (200, 136, 88))
    # Terre
    R(d, x0+11, y0+18, 10, 2, (96, 64, 32))
    # Feuilles (buisson rond)
    for y in range(4, 20):
        for x in range(6, 26):
            dx = x - 16
            dy = y - 12
            if dx*dx / 80.0 + dy*dy / 50.0 <= 1.0:
                c = PL1 if dy < -1 else PL2
                Px(d, x0+x, y0+y, c)

# Tile 37 — Escalier up
def tile_escalier_up(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Marches montantes (vers le haut)
    for i in range(5):
        y = y0 + 4 + i * 6
        shade = (160 - i*16, 128 - i*12, 88 - i*8)
        R(d, x0+2, y, 28, 5, shade)
        R(d, x0+2, y, 28, 1, ES2)
        R(d, x0+3, y+1, 26, 1, ES1)
    # Rampes
    R(d, x0+2, y0+4, 2, 28, ES2)
    R(d, x0+28, y0+4, 2, 28, ES2)
    # Flèche vers le haut
    for i in range(3):
        Px(d, x0+15-i, y0+2+i, BLK)
        Px(d, x0+16+i, y0+2+i, BLK)
    Px(d, x0+15, y0+2, BLK)

# Tile 38 — Escalier down
def tile_escalier_down(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    for i in range(5):
        y = y0 + 4 + i * 6
        shade = (160 + (i-4)*12, 128 + (i-4)*8, 88 + (i-4)*6)
        shade = tuple(max(0, min(255, c)) for c in shade)
        R(d, x0+2, y, 28, 5, shade)
        R(d, x0+2, y, 28, 1, ES2)
        R(d, x0+3, y+1, 26, 1, ES1)
    R(d, x0+2, y0+4, 2, 28, ES2)
    R(d, x0+28, y0+4, 2, 28, ES2)
    # Flèche vers le bas
    for i in range(3):
        Px(d, x0+15-i, y0+29-i, BLK)
        Px(d, x0+16+i, y0+29-i, BLK)

# Tile 39 — Paillasson
def tile_paillasson(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Paillasson brun
    R(d, x0+4, y0+10, 24, 14, (152, 120, 72))
    R(d, x0+6, y0+12, 20, 10, (136, 104, 56))
    # Texture fibre
    for py in range(12, 22, 2):
        for px in range(6, 26, 3):
            Px(d, x0+px, y0+py, (168, 136, 80))

# ============================================================================
# Row 5 — Intérieur avancé
# ============================================================================

# Tile 40 — Porte intérieure
def tile_porte_int(d, x0, y0):
    R(d, x0, y0, 32, 32, IM1)
    # Porte
    R(d, x0+6, y0+2, 20, 28, SH2)
    R(d, x0+8, y0+3, 16, 26, SH1)
    # Panneau
    R(d, x0+10, y0+6, 12, 8, (160, 128, 80))
    R(d, x0+10, y0+17, 12, 8, (160, 128, 80))
    # Poignée
    R(d, x0+21, y0+16, 2, 3, (200, 200, 72))
    # Seuil
    R(d, x0+6, y0+28, 20, 4, IM3)

# Tile 41 — Fenêtre intérieure
def tile_fenetre_int(d, x0, y0):
    R(d, x0, y0, 32, 32, IM1)
    # Cadre
    R(d, x0+6, y0+4, 20, 18, IM3)
    # Vitre (vue extérieure bleu ciel)
    R(d, x0+8, y0+6, 16, 14, (168, 216, 248))
    R(d, x0+9, y0+7, 6, 5, (200, 232, 248))  # reflet ciel
    # Croisillon
    R(d, x0+15, y0+6, 2, 14, IM3)
    R(d, x0+8, y0+12, 16, 2, IM3)
    # Rideaux
    R(d, x0+4, y0+3, 4, 20, (200, 72, 56))
    R(d, x0+24, y0+3, 4, 20, (200, 72, 56))
    # Plinthes
    R(d, x0, y0+26, 32, 6, IM3)

# Tile 42 — Sol bois foncé
def tile_sol_bois_fonce(d, x0, y0):
    R(d, x0, y0, 32, 32, DB1)
    for py in range(0, 32, 8):
        R(d, x0, y0+py, 32, 1, DB2)
        off = 8 if (py // 8) % 2 else 0
        for px in range(off, 32, 16):
            if px < 32:
                R(d, x0+px, y0+py, 1, 8, DB2)

# Tile 43 — Mur ext. avec fenêtre
def tile_mur_ext_fenetre(d, x0, y0):
    R(d, x0, y0, 32, 32, MW1)
    # Fenêtre petite
    R(d, x0+8, y0+6, 16, 12, FWF)
    R(d, x0+10, y0+8, 12, 8, FW2)
    R(d, x0+11, y0+9, 4, 3, FW1)
    R(d, x0+15, y0+8, 2, 8, FWF)
    R(d, x0+10, y0+11, 12, 2, FWF)
    # Appui
    R(d, x0+7, y0+18, 18, 2, MW3)
    # Texture mur
    R(d, x0, y0+15, 8, 2, MW3)
    R(d, x0+24, y0+15, 8, 2, MW3)

# Tile 44 — Table
def tile_table(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Plateau
    R(d, x0+2, y0+8, 28, 4, TA2)
    R(d, x0+3, y0+8, 26, 2, TA1)
    # Pieds
    R(d, x0+4, y0+12, 3, 18, TA2)
    R(d, x0+5, y0+12, 1, 18, TA1)
    R(d, x0+25, y0+12, 3, 18, TA2)
    R(d, x0+26, y0+12, 1, 18, TA1)

# Tile 45 — Chaise
def tile_chaise(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Dossier
    R(d, x0+8, y0+2, 16, 12, CH1)
    R(d, x0+10, y0+4, 12, 8, (168, 40, 24))
    # Assise
    R(d, x0+6, y0+14, 20, 6, TA2)
    R(d, x0+7, y0+15, 18, 4, TA1)
    # Pieds
    R(d, x0+8, y0+20, 2, 10, TA2)
    R(d, x0+22, y0+20, 2, 10, TA2)

# Tile 46 — Poster
def tile_poster(d, x0, y0):
    R(d, x0, y0, 32, 32, IM1)
    # Cadre
    R(d, x0+4, y0+4, 24, 20, BLK)
    R(d, x0+5, y0+5, 22, 18, PO1)
    # Image (étoile/Pokémon silhouette)
    R(d, x0+10, y0+8, 12, 12, (200, 120, 72))
    R(d, x0+13, y0+10, 6, 6, (248, 200, 80))
    # Plinthes
    R(d, x0, y0+26, 32, 6, IM3)

# Tile 47 — Poubelle
def tile_poubelle(d, x0, y0):
    R(d, x0, y0, 32, 32, IW1)
    # Corps poubelle
    R(d, x0+8, y0+8, 16, 22, PB2)
    R(d, x0+10, y0+10, 12, 18, PB1)
    # Couvercle
    R(d, x0+6, y0+6, 20, 4, PB2)
    R(d, x0+8, y0+7, 16, 2, PB1)
    # Poignée
    R(d, x0+14, y0+4, 4, 3, PB2)
    # Lignes
    R(d, x0+10, y0+16, 12, 1, PB2)
    R(d, x0+10, y0+22, 12, 1, PB2)

# ============================================================================
# Dispatch et génération
# ============================================================================
TILES = [
    tile_herbe, tile_herbe_haute, tile_chemin, tile_sable,
    tile_eau, tile_fleurs, tile_herbe_cailloux, tile_transition,
    tile_arbre_hg, tile_arbre_bg, tile_arbre_hd, tile_arbre_bd,
    tile_cloture_h, tile_cloture_v, tile_buisson, tile_herbe_detail,
    tile_toit_g, tile_toit_m, tile_toit_d, tile_mur_g,
    tile_mur_m, tile_mur_d, tile_porte, tile_fenetre_ext,
    tile_parquet, tile_mur_int, tile_comptoir, tile_machine_soin,
    tile_etagere, tile_tapis, tile_carrelage, tile_mur_motif,
    tile_lit_tete, tile_lit_pied, tile_tv, tile_pc,
    tile_plante, tile_escalier_up, tile_escalier_down, tile_paillasson,
    tile_porte_int, tile_fenetre_int, tile_sol_bois_fonce, tile_mur_ext_fenetre,
    tile_table, tile_chaise, tile_poster, tile_poubelle,
]

def main():
    os.makedirs(OUT, exist_ok=True)
    img = Image.new("RGBA", (256, 192), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for idx, fn in enumerate(TILES):
        col = idx % 8
        row = idx // 8
        x0 = col * 32
        y0 = row * 32
        fn(draw, x0, y0)
    path = os.path.join(OUT, "tileset_outdoor.png")
    img.save(path)
    print(f"✓ Tileset v8 sauvegardé : {path}")
    print(f"  256×192 px — {len(TILES)} tiles de 32×32")
    print(f"  Style FRLG : toits rouges, murs crème, herbe vive, eau bleue profonde")
    # Vérification des pixels
    import numpy as np
    arr = np.array(img)
    for idx in range(len(TILES)):
        col = idx % 8
        row = idx // 8
        tile = arr[row*32:(row+1)*32, col*32:(col+1)*32]
        opaque = int(np.sum(tile[:,:,3] > 0))
        print(f"  [{idx:2d}] {TILES[idx].__name__:24s} : {opaque:4d} px opaques")

if __name__ == "__main__":
    main()
