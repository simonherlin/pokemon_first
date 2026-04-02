#!/usr/bin/env python3
"""
Générateur de tileset FRLG HD — v4 corrigé.
Produit 8×6 = 48 tiles 32×32px, layout exact de tileset_builder.gd.

Rangée 0: HERBE, HERBE_HAUTE, CHEMIN, SABLE, EAU, FLEUR, (vide6), (vide7)
Rangée 1: ARBRE_HAUT, ARBRE_BAS, ARBRE_HAUT_R, ARBRE_BAS_R, FENCE_H, FENCE_V, BUISSON, HERBE_DETAIL
Rangée 2: TOIT_G, TOIT_M, TOIT_D, MUR_G, MUR_M, MUR_D, PORTE, FENETRE
Rangée 3: SOL_INT, MUR_INT, COMPTOIR, MACHINE_SOIN, ETAGERE, TAPIS, SOL_CARRELAGE, MUR_MOTIF
Rangée 4: LIT_TETE, LIT_PIED, TV, PC, PLANTE, ESCALIER_UP, ESCALIER_DOWN, PAILLASSON
Rangée 5: PORTE_INT, FENETRE_INT, SOL_BOIS_FONCE, MUR_EXT_FENETRE, TABLE, CHAISE, POSTER, POUBELLE
"""

from PIL import Image, ImageDraw
import os

TILE = 32
COLS = 8
ROWS = 6
OUT = "assets/sprites/tilesets/tileset_outdoor.png"

# ── PALETTE ──

# Herbe
G1 = (72, 176, 72)
G2 = (56, 144, 56)
G3 = (48, 120, 48)
G4 = (88, 192, 88)

# Hautes herbes
HG1 = (56, 136, 40)
HG2 = (40, 112, 32)
HG3 = (72, 152, 48)
HG4 = (48, 120, 36)

# Chemin
P1 = (208, 184, 136)
P2 = (184, 160, 112)
P3 = (160, 136, 96)
P4 = (224, 200, 152)

# Eau
W1 = (64, 128, 216)
W2 = (48, 104, 192)
W3 = (40, 88, 168)
W4 = (80, 152, 232)

# Sable
S1 = (240, 224, 168)
S2 = (216, 200, 144)
S3 = (200, 184, 128)

# Arbre
TR1 = (32, 120, 48)
TR2 = (48, 144, 56)
TR3 = (40, 136, 52)
TR4 = (64, 160, 64)
TRK = (104, 80, 48)
TRK2 = (88, 64, 40)

# Roche
R1 = (168, 160, 144)
R2 = (144, 136, 120)
R3 = (120, 112, 96)
R4 = (184, 176, 160)

# Bâtiment murs
BM1 = (232, 224, 208)
BM2 = (216, 208, 192)
BM3 = (200, 192, 176)

# Toit rouge
RF1 = (192, 64, 48)
RF2 = (168, 48, 32)
RF3 = (216, 80, 64)

# Toit bleu
RB1 = (64, 96, 176)
RB2 = (48, 80, 152)
RB3 = (80, 112, 192)

# Bois
F1 = (176, 144, 96)
F2 = (152, 120, 80)
F3 = (128, 96, 64)

# Intérieur
IN1 = (232, 224, 200)
IN2 = (216, 208, 184)
IN3 = (200, 192, 168)

# Porte
DR1 = (136, 96, 56)
DR2 = (112, 80, 48)

# Fenêtre
WN1 = (160, 200, 232)
WN2 = (128, 168, 208)

# Fleurs
FL_R = (232, 72, 72)
FL_Y = (248, 216, 56)
FL_B = (72, 120, 232)
FL_W = (248, 248, 240)


def draw_tile(img, col, row, draw_func):
    tile = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 255))
    draw_func(tile)
    img.paste(tile, (col * TILE, row * TILE))


# ════════════════════════════════════════════════════════════════════
# RANGÉE 0 : Terrain de base
# ════════════════════════════════════════════════════════════════════

def tile_herbe(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    for y in range(0, 32, 4):
        for x in range(0, 32, 4):
            s = (x * 7 + y * 13) % 17
            if s < 4: d.point((x+1, y+1), fill=G4)
            elif s < 8: d.point((x+2, y), fill=G2)
            elif s < 11: d.point((x, y+2), fill=G3)
    for y in range(2, 30, 8):
        for x in range(3, 29, 8):
            if (x * 31 + y * 47) % 23 < 8:
                d.line([(x, y+3), (x, y)], fill=G2)
                d.line([(x+1, y+2), (x+2, y)], fill=G4)


def tile_herbe_haute(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=HG1)
    for y in range(0, 32, 3):
        for x in range(0, 32, 3):
            s = (x * 17 + y * 29) % 11
            if s < 3: d.rectangle([x, y, x+2, y+2], fill=HG2)
            elif s < 6: d.rectangle([x, y, x+1, y+2], fill=HG3)
    for y in range(1, 30, 6):
        for x in range(1, 30, 6):
            sx = (x * 7 + y * 3) % 5
            d.line([(x+sx, y+4), (x+sx, y)], fill=HG2)
            d.line([(x+sx+1, y+3), (x+sx+2, y)], fill=HG3)
            d.line([(x+sx-1, y+3), (x+sx-2, y+1)], fill=HG4)


def tile_chemin(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=P1)
    for y in range(0, 32, 3):
        for x in range(0, 32, 3):
            s = (x * 23 + y * 37) % 13
            if s < 3: d.point((x, y), fill=P2)
            elif s < 5: d.point((x+1, y+1), fill=P4)
            elif s < 7: d.point((x, y+1), fill=P3)


def tile_sable(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=S1)
    for y in range(0, 32, 2):
        for x in range(0, 32, 2):
            s = (x * 19 + y * 41) % 17
            if s < 3: d.point((x, y), fill=S2)
            elif s < 5: d.point((x+1, y), fill=S3)


def tile_eau(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=W1)
    for y in range(2, 30, 6):
        for x in range(0, 32):
            p = (x + y * 3) % 12
            if p < 3: d.point((x, y), fill=W4)
            elif p < 5: d.point((x, y+1), fill=W2)
    for y in range(0, 32, 8):
        for x in range(0, 32, 8):
            sx = (x * 11 + y * 7) % 6
            d.rectangle([x+sx, y+1, x+sx+2, y+1], fill=W4)


def tile_fleur(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    flowers = [(5,8,FL_R),(14,4,FL_Y),(24,10,FL_B),(8,20,FL_W),
               (18,18,FL_R),(26,24,FL_Y),(4,28,FL_B),(20,28,FL_W)]
    for fx, fy, fc in flowers:
        d.point((fx, fy-1), fill=fc)
        d.point((fx-1, fy), fill=fc)
        d.point((fx, fy), fill=FL_Y if fc != FL_Y else FL_W)
        d.point((fx+1, fy), fill=fc)
        d.point((fx, fy+1), fill=fc)
    for y in range(3, 30, 7):
        for x in range(2, 30, 7):
            d.line([(x, y+2), (x, y)], fill=G2)


def tile_vide(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(16, 16, 24))


# ════════════════════════════════════════════════════════════════════
# RANGÉE 1 : Arbres et végétation
# ════════════════════════════════════════════════════════════════════

def _draw_tree_top(img, mirror=False):
    """Cime d'arbre. mirror=True pour la version droite."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    cx = 14 if not mirror else 17
    cy = 12
    for y in range(0, 26):
        for x in range(0, 32):
            dx, dy = x - cx, y - cy
            dist = (dx*dx/196 + dy*dy/144)
            if dist < 0.6: d.point((x, y), fill=TR3)
            elif dist < 0.8: d.point((x, y), fill=TR2)
            elif dist < 1.0: d.point((x, y), fill=TR1)
    for y in range(2, 22, 3):
        for x in range(4, 28, 3):
            dx, dy = x - cx, y - cy
            if dx*dx/196 + dy*dy/144 < 0.7:
                s = (x * 11 + y * 7) % 7
                if s < 2: d.point((x, y), fill=TR4)
                elif s < 4: d.point((x, y), fill=TR3)


def _draw_tree_bottom(img, mirror=False):
    """Tronc d'arbre. mirror=True pour version droite."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    cx = 14 if not mirror else 17
    for y in range(0, 8):
        for x in range(2, 30):
            dx = x - cx
            if abs(dx) < 14 - y:
                d.point((x, y), fill=TR2)
    trunk_l = 11 if not mirror else 14
    trunk_r = 19 if not mirror else 22
    for y in range(4, 28):
        for x in range(trunk_l, trunk_r):
            d.point((x, y), fill=TRK)
        d.point((trunk_l, y), fill=TRK2)
        d.point((trunk_r-1, y), fill=TRK2)
    rl = trunk_l - 2 if not mirror else trunk_r
    rr = trunk_r + 2 if not mirror else trunk_r + 2
    d.line([(trunk_l-2, 26), (trunk_l, 28)], fill=TRK2, width=2)
    d.line([(trunk_r, 26), (trunk_r+2, 28)], fill=TRK2, width=2)


def tile_arbre_haut(img):
    _draw_tree_top(img, mirror=False)

def tile_arbre_bas(img):
    _draw_tree_bottom(img, mirror=False)

def tile_arbre_haut_r(img):
    _draw_tree_top(img, mirror=True)

def tile_arbre_bas_r(img):
    _draw_tree_bottom(img, mirror=True)


def tile_fence_h(img):
    """Clôture horizontale."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    for x in [4, 28]:
        d.rectangle([x-2, 8, x+1, 31], fill=F1)
        d.rectangle([x-2, 8, x-2, 31], fill=F2)
    d.rectangle([2, 12, 30, 15], fill=F1)
    d.rectangle([2, 12, 30, 12], fill=F2)
    d.rectangle([2, 22, 30, 25], fill=F1)
    d.rectangle([2, 22, 30, 22], fill=F2)


def tile_fence_v(img):
    """Clôture verticale."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    for y in [4, 28]:
        d.rectangle([12, y-2, 19, y+1], fill=F1)
        d.rectangle([12, y-2, 19, y-2], fill=F2)
    d.rectangle([13, 2, 16, 30], fill=F1)
    d.rectangle([13, 2, 13, 30], fill=F2)


def tile_buisson(img):
    """Buisson dense."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    # buisson rond
    for y in range(4, 28):
        for x in range(4, 28):
            dx, dy = x - 16, y - 16
            dist = dx*dx + dy*dy
            if dist < 120:
                d.point((x, y), fill=TR3)
            elif dist < 150:
                d.point((x, y), fill=TR2)
            elif dist < 170:
                d.point((x, y), fill=TR1)
    for y in range(6, 26, 3):
        for x in range(6, 26, 3):
            if (x-16)**2 + (y-16)**2 < 120:
                s = (x*13+y*7)%7
                if s < 2: d.point((x,y), fill=TR4)


def tile_herbe_detail(img):
    """Herbe avec détails variés."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    for y in range(1, 31, 4):
        for x in range(1, 31, 4):
            s = (x*17+y*31)%13
            if s < 3:
                d.line([(x, y+3), (x, y)], fill=G2)
                d.line([(x+1, y+2), (x+2, y)], fill=G4)
            elif s < 6:
                d.line([(x+2, y+3), (x+2, y)], fill=G3)
                d.line([(x, y+2), (x+1, y)], fill=G2)
    # Petits cailloux
    for pos in [(6,14),(20,8),(12,24),(26,20)]:
        d.point(pos, fill=R2)


# ════════════════════════════════════════════════════════════════════
# RANGÉE 2 : Bâtiments extérieur (toit + murs)
# ════════════════════════════════════════════════════════════════════

def tile_toit_g(img):
    """Toit gauche (rouge)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=RF1)
    for y in range(0, 32, 4):
        offset = 4 if (y//4) % 2 else 0
        for x in range(-4, 36, 8):
            tx = x + offset
            d.line([(tx, y), (tx, y+3)], fill=RF2)
            d.line([(tx+1, y), (tx+7, y)], fill=RF3)
    # Bord gauche
    d.rectangle([0, 0, 2, 31], fill=RF2)
    d.line([(0, 0), (0, 31)], fill=(160, 40, 24))


def tile_toit_m(img):
    """Toit milieu (rouge)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=RF1)
    for y in range(0, 32, 4):
        offset = 4 if (y//4) % 2 else 0
        for x in range(-4, 36, 8):
            tx = x + offset
            d.line([(tx, y), (tx, y+3)], fill=RF2)
            d.line([(tx+1, y), (tx+7, y)], fill=RF3)


def tile_toit_d(img):
    """Toit droit (rouge)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=RF1)
    for y in range(0, 32, 4):
        offset = 4 if (y//4) % 2 else 0
        for x in range(-4, 36, 8):
            tx = x + offset
            d.line([(tx, y), (tx, y+3)], fill=RF2)
            d.line([(tx+1, y), (tx+7, y)], fill=RF3)
    # Bord droit
    d.rectangle([29, 0, 31, 31], fill=RF2)
    d.line([(31, 0), (31, 31)], fill=(160, 40, 24))


def tile_mur_g(img):
    """Mur gauche."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)
    for y in range(0, 32, 8):
        offset = 8 if (y//8)%2 else 0
        for x in range(-8, 40, 16):
            bx = x + offset
            d.rectangle([bx, y, bx+14, y+6], outline=BM3, fill=BM1)
            d.rectangle([bx+1, y+1, bx+13, y+5], fill=BM2)
    # Bord gauche
    d.rectangle([0, 0, 2, 31], fill=BM3)


def tile_mur_m(img):
    """Mur central."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)
    for y in range(0, 32, 8):
        offset = 8 if (y//8)%2 else 0
        for x in range(-8, 40, 16):
            bx = x + offset
            d.rectangle([bx, y, bx+14, y+6], outline=BM3, fill=BM1)
            d.rectangle([bx+1, y+1, bx+13, y+5], fill=BM2)


def tile_mur_d(img):
    """Mur droit."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)
    for y in range(0, 32, 8):
        offset = 8 if (y//8)%2 else 0
        for x in range(-8, 40, 16):
            bx = x + offset
            d.rectangle([bx, y, bx+14, y+6], outline=BM3, fill=BM1)
            d.rectangle([bx+1, y+1, bx+13, y+5], fill=BM2)
    # Bord droit
    d.rectangle([29, 0, 31, 31], fill=BM3)


def tile_porte(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)
    d.rectangle([6, 2, 25, 31], fill=DR1)
    d.rectangle([7, 3, 24, 30], fill=DR1)
    d.rectangle([6, 2, 25, 2], fill=DR2)
    d.rectangle([6, 2, 6, 31], fill=DR2)
    d.rectangle([25, 2, 25, 31], fill=DR2)
    d.ellipse([20, 14, 23, 17], fill=(200, 168, 56))


def tile_fenetre(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)
    d.rectangle([6, 6, 25, 25], fill=WN2)
    d.rectangle([7, 7, 24, 24], fill=WN1)
    d.line([(15, 6), (15, 25)], fill=BM3, width=2)
    d.line([(6, 15), (25, 15)], fill=BM3, width=2)
    d.line([(8, 8), (14, 8)], fill=(200, 224, 248))
    d.line([(8, 8), (8, 14)], fill=(200, 224, 248))


# ════════════════════════════════════════════════════════════════════
# RANGÉE 3 : Intérieur de base
# ════════════════════════════════════════════════════════════════════

def tile_sol_int(img):
    """Sol intérieur carrelage clair."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    d.line([(0, 0), (31, 0)], fill=IN3)
    d.line([(0, 0), (0, 31)], fill=IN3)
    d.line([(0, 31), (31, 31)], fill=IN2)
    d.line([(31, 0), (31, 31)], fill=IN2)
    d.line([(15, 0), (15, 31)], fill=IN2)
    d.line([(0, 15), (31, 15)], fill=IN2)


def tile_mur_int(img):
    """Mur intérieur."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(216, 208, 192))
    d.line([(0, 28), (31, 28)], fill=(184, 176, 160), width=2)
    d.line([(0, 30), (31, 30)], fill=(168, 160, 144), width=2)


def tile_comptoir(img):
    """Comptoir (Centre Pokémon / boutique)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Comptoir
    d.rectangle([0, 8, 31, 24], fill=(168, 128, 80))
    d.rectangle([0, 8, 31, 10], fill=(184, 144, 96))
    d.rectangle([0, 22, 31, 24], fill=(136, 104, 64))
    # Surface
    d.rectangle([0, 10, 31, 12], fill=(200, 168, 120))


def tile_machine_soin(img):
    """Machine de soin Centre Pokémon."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Machine
    d.rectangle([4, 4, 27, 28], fill=(200, 200, 208))
    d.rectangle([6, 6, 25, 26], fill=(216, 216, 224))
    # Écran
    d.rectangle([10, 8, 21, 16], fill=(48, 192, 96))
    # Pokeball slots
    for x in [9, 15, 21]:
        d.ellipse([x, 19, x+5, 24], fill=(232, 80, 72))
        d.line([(x, 21), (x+5, 21)], fill=(40, 40, 40))
    # LED
    d.rectangle([12, 26, 14, 28], fill=(72, 232, 72))


def tile_etagere(img):
    """Étagère."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(216, 208, 192))  # mur fond
    # Étagère bois
    d.rectangle([2, 4, 29, 28], fill=F1)
    d.rectangle([2, 4, 29, 5], fill=F2)
    # Planches horizontales
    for y in [4, 12, 20, 28]:
        d.rectangle([2, y, 29, y+1], fill=F2)
    # Livres / objets
    for y_base in [6, 14, 22]:
        for x in range(4, 28, 5):
            c = [(184,56,48),(56,96,184),(56,160,72),(184,160,56)][(x//5)%4]
            d.rectangle([x, y_base, x+3, y_base+5], fill=c)


def tile_tapis(img):
    """Tapis rouge."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(184, 48, 48))
    d.rectangle([1, 1, 30, 30], fill=(200, 56, 56))
    d.rectangle([2, 2, 29, 29], fill=(216, 64, 64))
    for y in range(4, 28, 6):
        for x in range(4, 28, 6):
            d.rectangle([x, y, x+2, y+2], fill=(184, 48, 48))


def tile_sol_carrelage(img):
    """Sol carrelage damier."""
    d = ImageDraw.Draw(img)
    for y in range(0, 32, 8):
        for x in range(0, 32, 8):
            c = IN1 if ((x+y)//8) % 2 == 0 else IN3
            d.rectangle([x, y, x+7, y+7], fill=c)
    # Joints
    for i in range(0, 33, 8):
        d.line([(i, 0), (i, 31)], fill=IN2)
        d.line([(0, i), (31, i)], fill=IN2)


def tile_mur_motif(img):
    """Mur intérieur avec motif (plinthe)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(216, 208, 192))
    # Plinthe en bas
    d.rectangle([0, 24, 31, 31], fill=(184, 136, 96))
    d.rectangle([0, 24, 31, 25], fill=(200, 152, 112))
    # Motif de moulure en haut
    d.line([(0, 4), (31, 4)], fill=(200, 192, 176))
    d.line([(0, 6), (31, 6)], fill=(200, 192, 176))


# ════════════════════════════════════════════════════════════════════
# RANGÉE 4 : Mobilier
# ════════════════════════════════════════════════════════════════════

def tile_lit_tete(img):
    """Lit — tête (oreiller)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Cadre du lit
    d.rectangle([2, 2, 29, 29], fill=(176, 136, 96))
    d.rectangle([4, 4, 27, 27], fill=(232, 232, 240))  # drap blanc
    # Oreiller
    d.rectangle([6, 6, 25, 16], fill=(248, 248, 248))
    d.rectangle([6, 6, 25, 7], fill=(240, 240, 248))
    # Couverture
    d.rectangle([4, 18, 27, 27], fill=(120, 160, 200))
    d.line([(4, 18), (27, 18)], fill=(100, 140, 180))


def tile_lit_pied(img):
    """Lit — pied."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    d.rectangle([2, 0, 29, 27], fill=(176, 136, 96))
    d.rectangle([4, 0, 27, 25], fill=(120, 160, 200))
    # Pied du lit
    d.rectangle([2, 25, 29, 29], fill=(152, 112, 72))
    d.line([(2, 25), (29, 25)], fill=(136, 96, 56))


def tile_tv(img):
    """Télévision."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Meuble
    d.rectangle([2, 16, 29, 29], fill=F1)
    d.rectangle([2, 16, 29, 17], fill=F2)
    # TV
    d.rectangle([4, 2, 27, 18], fill=(48, 48, 56))
    d.rectangle([6, 4, 25, 16], fill=(64, 120, 168))
    # Reflet
    d.line([(7, 5), (12, 5)], fill=(120, 176, 216))
    # Antenne
    d.line([(12, 2), (8, 0)], fill=(48, 48, 56))
    d.line([(20, 2), (24, 0)], fill=(48, 48, 56))


def tile_pc(img):
    """PC / ordinateur."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Bureau
    d.rectangle([2, 16, 29, 29], fill=F1)
    d.rectangle([2, 16, 29, 17], fill=F2)
    # Écran
    d.rectangle([6, 2, 25, 16], fill=(56, 56, 64))
    d.rectangle([8, 4, 23, 14], fill=(40, 80, 160))
    # Texte sur écran
    for y in range(6, 13, 3):
        d.line([(10, y), (18, y)], fill=(120, 200, 120))
    # Clavier
    d.rectangle([8, 18, 23, 22], fill=(192, 192, 200))


def tile_plante(img):
    """Plante d'intérieur."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Pot
    d.rectangle([10, 20, 21, 29], fill=(184, 96, 56))
    d.rectangle([8, 19, 23, 21], fill=(200, 112, 72))
    # Feuillage
    for y in range(4, 22):
        for x in range(4, 28):
            dx, dy = x - 16, y - 12
            dist = dx*dx/100 + dy*dy/64
            if dist < 0.7: d.point((x,y), fill=TR3)
            elif dist < 0.9: d.point((x,y), fill=TR2)
            elif dist < 1.0: d.point((x,y), fill=TR4)


def tile_escalier_up(img):
    """Escalier montant."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=R2)
    for y in range(0, 32, 8):
        shade = R1 if (y//8)%2 == 0 else R2
        d.rectangle([0, y, 31, y+6], fill=shade)
        d.line([(0, y+7), (31, y+7)], fill=R3)
        d.line([(0, y), (31, y)], fill=R4)
    # Flèche vers le haut
    d.polygon([(16,4),(12,12),(20,12)], fill=(248,248,248))


def tile_escalier_down(img):
    """Escalier descendant."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=R2)
    for y in range(0, 32, 8):
        shade = R3 if (y//8)%2 == 0 else R2
        d.rectangle([0, y, 31, y+6], fill=shade)
        d.line([(0, y+7), (31, y+7)], fill=(96, 88, 72))
        d.line([(0, y), (31, y)], fill=R2)
    # Flèche vers le bas
    d.polygon([(16,28),(12,20),(20,20)], fill=(248,248,248))


def tile_paillasson(img):
    """Paillasson devant une porte."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Paillasson
    d.rectangle([4, 8, 27, 24], fill=(152, 120, 80))
    d.rectangle([5, 9, 26, 23], fill=(168, 136, 88))
    # Bordure
    d.rectangle([4, 8, 27, 8], fill=(136, 104, 64))
    d.rectangle([4, 24, 27, 24], fill=(136, 104, 64))


# ════════════════════════════════════════════════════════════════════
# RANGÉE 5 : Intérieur avancé
# ════════════════════════════════════════════════════════════════════

def tile_porte_int(img):
    """Porte intérieure."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(216, 208, 192))
    d.rectangle([6, 0, 25, 31], fill=DR1)
    d.rectangle([6, 0, 25, 1], fill=DR2)
    d.rectangle([6, 0, 6, 31], fill=DR2)
    d.rectangle([25, 0, 25, 31], fill=DR2)
    d.ellipse([20, 14, 23, 17], fill=(200, 168, 56))


def tile_fenetre_int(img):
    """Fenêtre intérieure (mur haut avec fenêtre)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(216, 208, 192))
    d.rectangle([6, 4, 25, 24], fill=WN2)
    d.rectangle([7, 5, 24, 23], fill=WN1)
    d.line([(15, 4), (15, 24)], fill=BM3, width=2)
    d.line([(6, 14), (25, 14)], fill=BM3, width=2)
    d.line([(8, 6), (14, 6)], fill=(200, 224, 248))
    # Rideau à gauche
    d.rectangle([3, 2, 6, 26], fill=(200, 160, 120))
    # Rideau à droite
    d.rectangle([25, 2, 28, 26], fill=(200, 160, 120))


def tile_sol_bois_fonce(img):
    """Sol en bois foncé."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=F1)
    # Veines du bois
    for y in range(0, 32, 4):
        d.line([(0, y), (31, y)], fill=F2)
    for y in range(2, 32, 4):
        d.line([(0, y), (31, y)], fill=F3)
    # Joints
    for x in [0, 8, 16, 24]:
        d.line([(x, 0), (x, 31)], fill=F3)


def tile_mur_ext_fenetre(img):
    """Mur extérieur avec fenêtre (vu de dehors)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)
    # Briques de fond
    for y in range(0, 32, 8):
        offset = 8 if (y//8)%2 else 0
        for x in range(-8, 40, 16):
            bx = x + offset
            d.rectangle([bx, y, bx+14, y+6], outline=BM3, fill=BM1)
    # Petite fenêtre
    d.rectangle([8, 8, 23, 23], fill=WN2)
    d.rectangle([9, 9, 22, 22], fill=WN1)
    d.line([(15, 8), (15, 23)], fill=BM3, width=2)
    d.line([(8, 15), (23, 15)], fill=BM3, width=2)


def tile_table(img):
    """Table."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Dessus de table
    d.rectangle([2, 8, 29, 24], fill=F1)
    d.rectangle([2, 8, 29, 9], fill=F2)
    # Pieds
    d.rectangle([3, 24, 5, 29], fill=F3)
    d.rectangle([26, 24, 28, 29], fill=F3)


def tile_chaise(img):
    """Chaise."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Dossier
    d.rectangle([8, 2, 23, 12], fill=F1)
    d.rectangle([8, 2, 23, 3], fill=F2)
    # Assise
    d.rectangle([6, 12, 25, 20], fill=F1)
    d.rectangle([6, 12, 25, 13], fill=F2)
    # Pieds
    d.rectangle([7, 20, 9, 29], fill=F3)
    d.rectangle([22, 20, 24, 29], fill=F3)


def tile_poster(img):
    """Poster au mur."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(216, 208, 192))
    # Poster
    d.rectangle([4, 4, 27, 27], fill=(248, 248, 240))
    d.rectangle([5, 5, 26, 26], fill=(56, 96, 176))
    # Image stylisée (Pokéball)
    d.ellipse([10, 8, 21, 19], fill=(232, 80, 72))
    d.rectangle([10, 13, 21, 14], fill=(40, 40, 40))
    d.ellipse([14, 12, 17, 15], fill=(248, 248, 248))
    # Texte en bas
    d.rectangle([8, 21, 23, 24], fill=(248, 248, 240))


def tile_poubelle(img):
    """Poubelle."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Corps
    d.rectangle([8, 8, 23, 28], fill=(136, 144, 152))
    d.rectangle([8, 8, 23, 9], fill=(160, 168, 176))
    # Couvercle
    d.rectangle([6, 4, 25, 8], fill=(152, 160, 168))
    d.rectangle([6, 4, 25, 5], fill=(176, 184, 192))
    # Poignée
    d.rectangle([14, 2, 17, 4], fill=(120, 128, 136))


# ════════════════════════════════════════════════════════════════════
# ASSEMBLAGE
# ════════════════════════════════════════════════════════════════════

TILE_MAP = [
    # Row 0: Terrain de base (indices 0-7)
    [tile_herbe, tile_herbe_haute, tile_chemin, tile_sable,
     tile_eau, tile_fleur, tile_vide, tile_vide],
    # Row 1: Arbres et végétation (indices 8-15)
    [tile_arbre_haut, tile_arbre_bas, tile_arbre_haut_r, tile_arbre_bas_r,
     tile_fence_h, tile_fence_v, tile_buisson, tile_herbe_detail],
    # Row 2: Bâtiments (indices 16-23)
    [tile_toit_g, tile_toit_m, tile_toit_d, tile_mur_g,
     tile_mur_m, tile_mur_d, tile_porte, tile_fenetre],
    # Row 3: Intérieur base (indices 24-31)
    [tile_sol_int, tile_mur_int, tile_comptoir, tile_machine_soin,
     tile_etagere, tile_tapis, tile_sol_carrelage, tile_mur_motif],
    # Row 4: Mobilier (indices 32-39)
    [tile_lit_tete, tile_lit_pied, tile_tv, tile_pc,
     tile_plante, tile_escalier_up, tile_escalier_down, tile_paillasson],
    # Row 5: Intérieur avancé (indices 40-47)
    [tile_porte_int, tile_fenetre_int, tile_sol_bois_fonce, tile_mur_ext_fenetre,
     tile_table, tile_chaise, tile_poster, tile_poubelle],
]


def main():
    width = COLS * TILE
    height = ROWS * TILE
    img = Image.new("RGBA", (width, height), (0, 0, 0, 255))

    for row_idx, row_tiles in enumerate(TILE_MAP):
        for col_idx, tile_func in enumerate(row_tiles):
            draw_tile(img, col_idx, row_idx, tile_func)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG")
    print(f"Tileset généré : {OUT} ({width}×{height}px, {COLS}×{ROWS} = {COLS*ROWS} tiles)")


if __name__ == "__main__":
    main()
