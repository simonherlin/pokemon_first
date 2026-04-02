#!/usr/bin/env python3
"""
Générateur de tileset FRLG HD — v6 Qualité Professionnelle.
Produit 8×6 = 48 tiles 32×32px avec pixel art haute qualité.
Inspiration : FireRed/LeafGreen, HeartGold/SoulSilver, Emerald.
Amélioration majeure du rendu visuel par rapport à v5.
"""

from PIL import Image, ImageDraw
import os, random, math

random.seed(42)

TILE = 32
COLS = 8
ROWS = 6
OUT = "assets/sprites/tilesets/tileset_outdoor.png"

# ══════════════════════════════════════════════════════════════
# PALETTE FRLG FIDÈLE (couleurs extraites des sprites GBA)
# ══════════════════════════════════════════════════════════════

# Herbe normale — palette plus vive, 5 tons
G1 = (34, 111, 44)     # ombré profond
G2 = (50, 142, 58)     # ombré
G3 = (72, 176, 80)     # base principale
G4 = (100, 200, 104)   # éclairé
G5 = (136, 220, 136)   # highlight

# Hautes herbes — plus saturées et sombres
HG1 = (24, 80, 28)
HG2 = (36, 108, 40)
HG3 = (52, 136, 52)
HG4 = (72, 160, 68)
HG5 = (96, 180, 88)

# Chemin terre — beige/brun chaud
P1 = (120, 96, 64)     # ombre
P2 = (156, 132, 96)    # mid-ombre
P3 = (188, 164, 120)   # base
P4 = (212, 192, 148)   # éclairé
P5 = (228, 212, 172)   # highlight

# Eau — bleu profond avec reflets
W1 = (24, 64, 148)     # profond
W2 = (40, 96, 176)     # base
W3 = (64, 128, 200)    # moyen
W4 = (96, 164, 224)    # clair
W5 = (140, 196, 240)   # reflet

# Sable
S1 = (188, 172, 120)
S2 = (212, 196, 144)
S3 = (228, 216, 164)
S4 = (240, 228, 180)

# Feuillage arbre — vert profond riche
L1 = (16, 72, 24)      # ombre profonde
L2 = (28, 96, 36)      # ombre
L3 = (44, 124, 48)     # base
L4 = (60, 148, 64)     # éclairé
L5 = (80, 168, 80)     # highlight

# Tronc
TK1 = (56, 36, 16)     # ombre
TK2 = (80, 56, 28)     # base
TK3 = (108, 80, 44)    # éclairé
TK4 = (132, 104, 60)   # highlight

# Fleurs
FL_R = (216, 48, 64)
FL_P = (232, 112, 128)
FL_Y = (240, 208, 48)
FL_W = (248, 244, 228)
FL_O = (240, 148, 48)
FL_B = (96, 128, 232)

# Bâtiment mur — gris/beige clair
BM1 = (168, 160, 144)
BM2 = (192, 184, 168)
BM3 = (212, 204, 188)
BM4 = (228, 220, 204)

# Toit tuiles rouges — rouge brique FRLG
RF1 = (128, 32, 20)
RF2 = (168, 52, 36)
RF3 = (200, 72, 52)
RF4 = (224, 100, 72)

# Bois intérieur — parquet chaud
WD1 = (96, 60, 28)
WD2 = (128, 88, 48)
WD3 = (160, 116, 68)
WD4 = (184, 144, 92)

# Sol intérieur — plancher clair
SI1 = (184, 176, 160)
SI2 = (204, 196, 180)
SI3 = (220, 212, 196)
SI4 = (232, 228, 212)

# Mur intérieur
MI1 = (148, 136, 120)
MI2 = (172, 160, 144)
MI3 = (192, 180, 168)
MI4 = (208, 200, 188)

# Tapis rouge
TP1 = (136, 24, 24)
TP2 = (176, 40, 40)
TP3 = (208, 64, 64)
TP4 = (228, 100, 100)

# Carrelage
CL1 = (188, 192, 200)
CL2 = (212, 216, 224)
CL3 = (232, 232, 240)
CL4 = (244, 244, 248)

# Métal
MT1 = (112, 120, 132)
MT2 = (152, 160, 172)
MT3 = (188, 196, 204)
MT4 = (216, 220, 228)

# Clôture
FN1 = (80, 52, 24)
FN2 = (116, 80, 44)
FN3 = (148, 112, 68)
FN4 = (172, 140, 92)

# Fenêtre
WN1 = (120, 180, 220)
WN2 = (160, 208, 236)
WN3 = (200, 228, 244)

# Noir/gris pour outlines
BLK = (24, 24, 28)
DK_GREY = (64, 60, 56)
MD_GREY = (112, 108, 100)

# ══════════════════════════════════════════════════════════════
# UTILITAIRES DE DESSIN
# ══════════════════════════════════════════════════════════════

def px(draw, x, y, color):
    draw.point((x, y), fill=color)

def rect(draw, x1, y1, x2, y2, color):
    draw.rectangle([x1, y1, x2, y2], fill=color)

def hline(draw, x1, x2, y, color):
    for x in range(x1, x2 + 1):
        px(draw, x, y, color)

def vline(draw, x, y1, y2, color):
    for y in range(y1, y2 + 1):
        px(draw, x, y, color)

def noise_fill(draw, x0, y0, w, h, colors, seed=0):
    rng = random.Random(seed)
    for dy in range(h):
        for dx in range(w):
            px(draw, x0 + dx, y0 + dy, rng.choice(colors))

def weighted_noise(draw, x0, y0, w, h, color_weights, seed=0):
    """Remplissage pondéré — color_weights = [(color, weight), ...]"""
    rng = random.Random(seed)
    pool = []
    for c, w_ in color_weights:
        pool.extend([c] * w_)
    for dy in range(h):
        for dx in range(w):
            px(draw, x0 + dx, y0 + dy, rng.choice(pool))

def perlin_like(draw, x0, y0, w, h, colors, scale=6, seed=0):
    """Pseudo-Perlin naturel pour terrains avec interpolation douce."""
    rng = random.Random(seed)
    n = len(colors)
    # Grille basse résolution
    gw = (w // scale) + 2
    gh = (h // scale) + 2
    grid = [[rng.random() for _ in range(gw)] for _ in range(gh)]
    for dy in range(h):
        for dx in range(w):
            gx = dx / scale
            gy = dy / scale
            ix = int(gx)
            iy = int(gy)
            fx = gx - ix
            fy = gy - iy
            # Interpolation bilinéaire
            v00 = grid[iy % gh][ix % gw]
            v10 = grid[iy % gh][(ix + 1) % gw]
            v01 = grid[(iy + 1) % gh][ix % gw]
            v11 = grid[(iy + 1) % gh][(ix + 1) % gw]
            v = v00 * (1-fx)*(1-fy) + v10 * fx*(1-fy) + v01 * (1-fx)*fy + v11 * fx*fy
            idx = min(int(v * n), n - 1)
            px(draw, x0 + dx, y0 + dy, colors[idx])

def dither_rect(draw, x0, y0, w, h, c1, c2):
    """Dithering en damier."""
    for dy in range(h):
        for dx in range(w):
            c = c1 if (dx + dy) % 2 == 0 else c2
            px(draw, x0 + dx, y0 + dy, c)

def blend(c1, c2, t=0.5):
    """Mélange linéaire de deux couleurs."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

# ══════════════════════════════════════════════════════════════
# ROW 0 : TERRAIN EXTÉRIEUR (indices 0-7)
# ══════════════════════════════════════════════════════════════

def draw_herbe(draw, ox, oy):
    """Tile 0: Herbe verte avec texture naturelle riche."""
    # Base Perlin naturelle
    perlin_like(draw, ox, oy, 32, 32, [G2, G3, G3, G3, G4], scale=7, seed=100)
    # Brins d'herbe décoratifs — petits V et traits
    rng = random.Random(42)
    for _ in range(12):
        bx = rng.randint(1, 29) + ox
        by = rng.randint(2, 29) + oy
        px(draw, bx, by, G5)
        px(draw, bx, by - 1, G4)
    # Quelques pixels plus sombres pour la profondeur
    for _ in range(6):
        bx = rng.randint(0, 31) + ox
        by = rng.randint(0, 31) + oy
        px(draw, bx, by, G1)

def draw_herbe_haute(draw, ox, oy):
    """Tile 1: Herbes hautes (zone de rencontre) — touffes en V distinctes."""
    # Base sombre
    perlin_like(draw, ox, oy, 32, 32, [HG1, HG2, HG2, HG3], scale=5, seed=200)
    # Touffes d'herbe — motif reconnaissable comme FRLG
    tufts = [(4,6), (16,4), (28,7), (8,16), (22,14), (12,24), (26,22), (4,28), (18,26)]
    for bx, by in tufts:
        x = ox + bx
        y = oy + by
        # Brin central
        px(draw, x, y - 3, HG5)
        px(draw, x, y - 2, HG4)
        px(draw, x, y - 1, HG3)
        px(draw, x, y, HG2)
        # Brin gauche
        px(draw, x - 2, y - 1, HG5)
        px(draw, x - 1, y, HG4)
        # Brin droit
        px(draw, x + 2, y - 1, HG5)
        px(draw, x + 1, y, HG4)

def draw_chemin(draw, ox, oy):
    """Tile 2: Chemin de terre avec texture subtile."""
    perlin_like(draw, ox, oy, 32, 32, [P2, P3, P3, P4], scale=8, seed=300)
    # Bord supérieur (ombre naturelle)
    for x in range(32):
        px(draw, ox + x, oy, P1)
    # Cailloux dispersés
    rng = random.Random(301)
    stones = [(7, 12), (18, 8), (25, 20), (10, 24), (28, 28)]
    for sx, sy in stones:
        px(draw, ox + sx, oy + sy, P1)
        px(draw, ox + sx + 1, oy + sy, P2)
    # Craquelures subtiles
    for _ in range(3):
        cx = rng.randint(4, 27) + ox
        cy = rng.randint(6, 26) + oy
        px(draw, cx, cy, P1)
        px(draw, cx + 1, cy, P2)

def draw_sable(draw, ox, oy):
    """Tile 3: Sable de plage."""
    perlin_like(draw, ox, oy, 32, 32, [S1, S2, S2, S3, S3, S4], scale=6, seed=350)
    # Points clairs pour la texture
    rng = random.Random(351)
    for _ in range(8):
        px(draw, rng.randint(0, 31) + ox, rng.randint(0, 31) + oy, S4)
    for _ in range(4):
        px(draw, rng.randint(0, 31) + ox, rng.randint(0, 31) + oy, S1)

def draw_eau(draw, ox, oy):
    """Tile 4: Eau avec vagues et reflets animables."""
    # Base bleue profonde
    perlin_like(draw, ox, oy, 32, 32, [W1, W2, W2, W3], scale=10, seed=400)
    # Vagues horizontales
    for row in range(4):
        y = oy + row * 8 + 3
        offset = row * 4
        for x in range(32):
            phase = (x + offset) / 8.0
            if math.sin(phase * math.pi) > 0.5:
                px(draw, ox + x, y, W4)
            elif math.sin(phase * math.pi) > 0.2:
                px(draw, ox + x, y, W3)
    # Reflets blancs/clairs
    rng = random.Random(401)
    for _ in range(5):
        rx = rng.randint(2, 29) + ox
        ry = rng.randint(2, 29) + oy
        px(draw, rx, ry, W5)
        px(draw, rx + 1, ry, W4)

def draw_fleur(draw, ox, oy):
    """Tile 5: Herbe avec fleurs — décoratif."""
    # Base herbe
    perlin_like(draw, ox, oy, 32, 32, [G2, G3, G3, G4], scale=7, seed=500)
    # Fleurs à 5 pétales
    flowers = [
        (8, 8, FL_R, FL_Y), (22, 6, FL_P, FL_W), (14, 18, FL_Y, FL_O),
        (6, 24, FL_B, FL_W), (26, 22, FL_R, FL_Y), (18, 28, FL_P, FL_Y)
    ]
    for fx, fy, petal, center in flowers:
        x, y = ox + fx, oy + fy
        # 4 pétales
        px(draw, x, y - 1, petal)
        px(draw, x - 1, y, petal)
        px(draw, x + 1, y, petal)
        px(draw, x, y + 1, petal)
        # Centre
        px(draw, x, y, center)
        # Feuille
        px(draw, x + 1, y + 1, G2)

def draw_herbe_alt(draw, ox, oy):
    """Tile 6: Variante herbe (bord de chemin)."""
    perlin_like(draw, ox, oy, 32, 32, [G2, G3, G3, P3, G3], scale=6, seed=600)
    # Transition herbe/terre en bas
    for x in range(32):
        if (x + 5) % 4 < 2:
            px(draw, ox + x, oy + 30, P2)
            px(draw, ox + x, oy + 31, P3)
        else:
            px(draw, ox + x, oy + 30, G2)
            px(draw, ox + x, oy + 31, G3)

def draw_herbe_detail(draw, ox, oy):
    """Tile 7: Herbe détaillée avec petit caillou."""
    draw_herbe(draw, ox, oy)
    # Petit caillou gris
    rect(draw, ox + 14, oy + 20, ox + 17, oy + 22, MD_GREY)
    px(draw, ox + 15, oy + 20, SI3)
    px(draw, ox + 14, oy + 22, DK_GREY)

# ══════════════════════════════════════════════════════════════
# ROW 1 : VÉGÉTATION & CLÔTURES (indices 8-15)
# ══════════════════════════════════════════════════════════════

def draw_arbre_haut(draw, ox, oy):
    """Tile 8: Arbre — partie haute (canopée riche avec ombres)."""
    # Base herbe sous l'arbre
    rect(draw, ox, oy, ox + 31, oy + 31, G2)
    # Canopée ronde avec volume — ombre/lumière progressifs
    cx, cy = 16, 18
    for dy in range(-16, 14):
        for dx in range(-16, 16):
            d = math.sqrt(dx * dx + (dy * 1.1) ** 2)
            if d < 15:
                x, y = ox + cx + dx, oy + cy + dy
                if 0 <= x - ox < 32 and 0 <= y - oy < 32:
                    # Gradient basé sur la distance au centre et direction de la lumière
                    light = (dx + dy * 0.5) / 15.0  # lumière vient du haut-gauche
                    if d > 13:
                        px(draw, x, y, L1)  # bord extérieur sombre
                    elif light < -0.4:
                        px(draw, x, y, L1)
                    elif light < -0.1:
                        px(draw, x, y, L2)
                    elif light < 0.2:
                        px(draw, x, y, L3)
                    elif light < 0.5:
                        px(draw, x, y, L4)
                    else:
                        px(draw, x, y, L5)
    # Texture feuillage — groupes de pixels
    rng = random.Random(801)
    for _ in range(20):
        lx = rng.randint(3, 28)
        ly = rng.randint(3, 28)
        d = math.sqrt((lx - cx) ** 2 + ((ly - cy) * 1.1) ** 2)
        if d < 13:
            c = rng.choice([L1, L2, L5])
            px(draw, ox + lx, oy + ly, c)

def draw_arbre_bas(draw, ox, oy):
    """Tile 9: Arbre — partie basse (tronc + base de canopée)."""
    # Base herbe
    perlin_like(draw, ox, oy, 32, 32, [G2, G3, G3, G4], scale=7, seed=900)
    # Tronc central avec écorce détaillée
    trunk_left, trunk_right = 12, 19
    for y in range(0, 24):
        for x in range(trunk_left, trunk_right + 1):
            if x == trunk_left or x == trunk_right:
                px(draw, ox + x, oy + y, TK1)  # bords sombres
            elif x == trunk_left + 1:
                px(draw, ox + x, oy + y, TK2)
            elif x >= trunk_right - 1:
                px(draw, ox + x, oy + y, TK2)
            else:
                px(draw, ox + x, oy + y, TK3 if y % 3 != 0 else TK2)
    # Highlight sur le tronc
    for y in range(2, 22, 3):
        px(draw, ox + 15, oy + y, TK4)
    # Canopée qui descend sur les côtés
    for dx in range(-12, 13):
        max_y = int(5 * (1 - (abs(dx) / 13.0) ** 2))
        for dy in range(max_y):
            x = ox + 16 + dx
            y = oy + dy
            if 0 <= x - ox < 32 and 0 <= y - oy < 32:
                light = dx / 13.0
                if abs(dx) > 10:
                    px(draw, x, y, L1)
                elif light < -0.3:
                    px(draw, x, y, L2)
                elif light < 0.2:
                    px(draw, x, y, L3)
                else:
                    px(draw, x, y, L4)
    # Ombre au sol sous l'arbre
    for x in range(8, 24):
        t = abs(x - 16) / 8.0
        if t < 0.8:
            px(draw, ox + x, oy + 24, G1)
            px(draw, ox + x, oy + 25, blend(G1, G2, 0.5))

def draw_arbre_haut_r(draw, ox, oy):
    """Tile 10: Arbre variante (canopée plus dense)."""
    rect(draw, ox, oy, ox + 31, oy + 31, G2)
    cx, cy = 16, 17
    for dy in range(-15, 15):
        for dx in range(-15, 16):
            d = math.sqrt(dx * dx + (dy * 1.2) ** 2)
            if d < 14:
                x, y = ox + cx + dx, oy + cy + dy
                if 0 <= x - ox < 32 and 0 <= y - oy < 32:
                    light = (dx * 0.7 + dy * 0.7) / 14.0
                    if d > 12:
                        px(draw, x, y, L1)
                    elif light < -0.3:
                        px(draw, x, y, L1)
                    elif light < 0:
                        px(draw, x, y, L2)
                    elif light < 0.3:
                        px(draw, x, y, L3)
                    else:
                        px(draw, x, y, L4)
    rng = random.Random(1001)
    for _ in range(15):
        lx = rng.randint(4, 27)
        ly = rng.randint(4, 27)
        d = math.sqrt((lx - cx) ** 2 + ((ly - cy) * 1.2) ** 2)
        if d < 12:
            px(draw, ox + lx, oy + ly, rng.choice([L1, L5]))

def draw_arbre_bas_r(draw, ox, oy):
    """Tile 11: Tronc variante (légèrement décalé)."""
    perlin_like(draw, ox, oy, 32, 32, [G2, G3, G3, G4], scale=7, seed=1100)
    # Tronc plus fin
    for y in range(0, 22):
        for x in range(13, 19):
            if x in (13, 18):
                px(draw, ox + x, oy + y, TK1)
            elif x in (14, 17):
                px(draw, ox + x, oy + y, TK2)
            else:
                px(draw, ox + x, oy + y, TK3)
    for y in range(1, 20, 4):
        px(draw, ox + 15, oy + y, TK4)
    # Feuillage bas
    for dx in range(-10, 11):
        max_y = int(4 * (1 - (abs(dx) / 11.0) ** 2))
        for dy in range(max_y):
            x, y = ox + 16 + dx, oy + dy
            if 0 <= x - ox < 32:
                c = L2 if dx < -3 else L3 if dx < 3 else L4
                px(draw, x, y, c)
    for x in range(9, 23):
        px(draw, ox + x, oy + 22, G1)

def draw_cloture_h(draw, ox, oy):
    """Tile 12: Clôture horizontale."""
    # Base herbe
    perlin_like(draw, ox, oy, 32, 32, [G2, G3, G3, G4], scale=7, seed=1200)
    # Poteau gauche
    rect(draw, ox + 0, oy + 8, ox + 3, oy + 24, FN2)
    vline(draw, ox + 0, oy + 8, oy + 24, FN1)
    vline(draw, ox + 3, oy + 8, oy + 24, FN1)
    px(draw, ox + 2, oy + 9, FN4)
    # Rail haut
    rect(draw, ox + 0, oy + 11, ox + 31, oy + 13, FN2)
    hline(draw, ox, ox + 31, oy + 11, FN3)
    hline(draw, ox, ox + 31, oy + 13, FN1)
    # Rail bas
    rect(draw, ox + 0, oy + 18, ox + 31, oy + 20, FN2)
    hline(draw, ox, ox + 31, oy + 18, FN3)
    hline(draw, ox, ox + 31, oy + 20, FN1)
    # Poteau droite
    rect(draw, ox + 28, oy + 8, ox + 31, oy + 24, FN2)
    vline(draw, ox + 28, oy + 8, oy + 24, FN1)
    vline(draw, ox + 31, oy + 8, oy + 24, FN1)
    # Ombre au sol
    for x in range(32):
        px(draw, ox + x, oy + 25, G1)

def draw_cloture_v(draw, ox, oy):
    """Tile 13: Clôture verticale."""
    perlin_like(draw, ox, oy, 32, 32, [G2, G3, G3, G4], scale=7, seed=1300)
    # Poteau principal
    rect(draw, ox + 13, oy, ox + 18, oy + 31, FN2)
    vline(draw, ox + 13, oy, oy + 31, FN1)
    vline(draw, ox + 18, oy, oy + 31, FN1)
    vline(draw, ox + 15, oy, oy + 31, FN3)
    # Traverses horizontales
    for ty in [4, 14, 24]:
        rect(draw, ox + 10, oy + ty, ox + 21, oy + ty + 2, FN2)
        hline(draw, ox + 10, ox + 21, oy + ty, FN3)
        hline(draw, ox + 10, ox + 21, oy + ty + 2, FN1)
    # Ombre
    for y in range(32):
        px(draw, ox + 19, oy + y, blend(FN1, G2, 0.5))

def draw_buisson(draw, ox, oy):
    """Tile 14: Buisson taillé."""
    perlin_like(draw, ox, oy, 32, 32, [G2, G3, G3, G4], scale=7, seed=1400)
    # Buisson arrondi
    cx, cy = 16, 18
    for dy in range(-10, 10):
        for dx in range(-12, 13):
            d = math.sqrt((dx * 0.9) ** 2 + (dy * 1.1) ** 2)
            if d < 10:
                x, y = ox + cx + dx, oy + cy + dy
                if 0 <= x - ox < 32 and 0 <= y - oy < 32:
                    if d > 8:
                        px(draw, x, y, L1)
                    elif dy > 3 or dx < -5:
                        px(draw, x, y, L2)
                    elif dy < -3 or dx > 5:
                        px(draw, x, y, L4)
                    else:
                        px(draw, x, y, L3)
    # Highlight
    rng = random.Random(1401)
    for _ in range(6):
        lx = rng.randint(8, 24)
        ly = rng.randint(10, 22)
        d = math.sqrt(((lx - cx) * 0.9) ** 2 + ((ly - cy) * 1.1) ** 2)
        if d < 8:
            px(draw, ox + lx, oy + ly, L5)

def draw_herbe_detail2(draw, ox, oy):
    """Tile 15: Herbe détaillée 2 (variante)."""
    draw_herbe(draw, ox, oy)
    # Petite touffe d'herbe visible
    for dx in [-1, 0, 1]:
        px(draw, ox + 20 + dx, oy + 14, G5)
        px(draw, ox + 20 + dx, oy + 13, G4)
    px(draw, ox + 20, oy + 12, G5)

# ══════════════════════════════════════════════════════════════
# ROW 2 : BÂTIMENTS EXTÉRIEURS (indices 16-23)
# ══════════════════════════════════════════════════════════════

def draw_toit_gauche(draw, ox, oy):
    """Tile 16: Toit — coin gauche avec tuiles."""
    rect(draw, ox, oy, ox + 31, oy + 31, (180, 200, 220))  # ciel
    # Tuiles en pente
    for row in range(8):
        y_start = oy + 4 + row * 3
        x_start = ox + 24 - row * 3
        for x in range(x_start, ox + 32):
            if 0 <= y_start - oy < 32 and 0 <= x - ox < 32:
                if row % 2 == 0:
                    c = RF2 if (x - ox) % 4 < 2 else RF3
                else:
                    c = RF1 if (x - ox) % 4 < 2 else RF2
                px(draw, x, y_start, c)
                if y_start + 1 - oy < 32:
                    px(draw, x, y_start + 1, blend(c, RF1, 0.3))
                if y_start + 2 - oy < 32:
                    px(draw, x, y_start + 2, RF4 if (x - ox) % 4 == 1 else RF3)
    # Bord du toit
    for row in range(8):
        y = oy + 4 + row * 3
        x = ox + 24 - row * 3
        if 0 <= y - oy < 32 and 0 <= x - ox < 32:
            px(draw, x, y, RF1)
            if y + 1 - oy < 32:
                px(draw, x, y + 1, RF1)

def draw_toit_milieu(draw, ox, oy):
    """Tile 17: Toit — milieu avec tuiles régulières."""
    rect(draw, ox, oy, ox + 31, oy + 3, (180, 200, 220))  # ciel en haut
    # Tuiles
    for row in range(9):
        y = oy + 4 + row * 3
        if y - oy >= 32:
            break
        for x in range(32):
            offset = 2 if row % 2 else 0
            tile_phase = (x + offset) % 4
            if row % 2 == 0:
                c = RF2 if tile_phase < 2 else RF3
            else:
                c = RF1 if tile_phase < 2 else RF2
            px(draw, ox + x, y, c)
            if y + 1 - oy < 32:
                c2 = blend(c, RF1, 0.3) if tile_phase == 0 else c
                px(draw, ox + x, y + 1, c2)
            if y + 2 - oy < 32:
                px(draw, ox + x, y + 2, RF3 if tile_phase == 1 else RF2)
    # Faîtière en haut
    hline(draw, ox, ox + 31, oy + 4, RF1)

def draw_toit_droit(draw, ox, oy):
    """Tile 18: Toit — coin droit."""
    rect(draw, ox, oy, ox + 31, oy + 31, (180, 200, 220))
    for row in range(8):
        y_start = oy + 4 + row * 3
        x_end = ox + 7 + row * 3
        for x in range(ox, min(x_end + 1, ox + 32)):
            if 0 <= y_start - oy < 32:
                if row % 2 == 0:
                    c = RF2 if (x - ox) % 4 < 2 else RF3
                else:
                    c = RF1 if (x - ox) % 4 < 2 else RF2
                px(draw, x, y_start, c)
                if y_start + 1 - oy < 32:
                    px(draw, x, y_start + 1, blend(c, RF1, 0.3))
                if y_start + 2 - oy < 32:
                    px(draw, x, y_start + 2, RF4 if (x - ox) % 4 == 1 else RF3)
    # Bord droit
    for row in range(8):
        y = oy + 4 + row * 3
        x = ox + 7 + row * 3
        if 0 <= y - oy < 32 and 0 <= x - ox < 32:
            px(draw, x, y, RF1)
            if y + 1 - oy < 32:
                px(draw, x, y + 1, RF1)

def draw_mur_gauche(draw, ox, oy):
    """Tile 19: Mur extérieur — côté gauche."""
    rect(draw, ox, oy, ox + 31, oy + 31, BM3)
    # Bord gauche sombre
    vline(draw, ox, oy, oy + 31, BM1)
    vline(draw, ox + 1, oy, oy + 31, BM2)
    # Briques subtiles
    for row in range(8):
        y = oy + row * 4
        offset = 6 if row % 2 else 0
        for col in range(3):
            x = ox + 4 + col * 10 + offset
            if x < ox + 32:
                px(draw, x, y, BM2)
                px(draw, x, y + 1, BM2)
    # Ombre sous le toit
    hline(draw, ox, ox + 31, oy, BM1)
    hline(draw, ox, ox + 31, oy + 1, BM2)

def draw_mur_milieu(draw, ox, oy):
    """Tile 20: Mur extérieur — centre."""
    rect(draw, ox, oy, ox + 31, oy + 31, BM3)
    # Mortier entre briques
    for row in range(8):
        y = oy + row * 4
        hline(draw, ox, ox + 31, y, BM2)
        offset = 6 if row % 2 else 0
        for col in range(4):
            x = ox + col * 10 + offset
            if 0 <= x - ox < 32:
                vline(draw, x, y, min(y + 3, oy + 31), BM2)
    hline(draw, ox, ox + 31, oy, BM1)
    # Highlight supérieur des briques
    for row in range(8):
        y = oy + row * 4 + 1
        if y < oy + 32:
            hline(draw, ox, ox + 31, y, BM4)

def draw_mur_droit(draw, ox, oy):
    """Tile 21: Mur extérieur — côté droit."""
    rect(draw, ox, oy, ox + 31, oy + 31, BM3)
    vline(draw, ox + 31, oy, oy + 31, BM1)
    vline(draw, ox + 30, oy, oy + 31, BM2)
    for row in range(8):
        y = oy + row * 4
        offset = 6 if row % 2 else 0
        for col in range(3):
            x = ox + col * 10 + offset
            if 0 <= x - ox < 32:
                px(draw, x, y, BM2)
    hline(draw, ox, ox + 31, oy, BM1)
    hline(draw, ox, ox + 31, oy + 1, BM2)

def draw_porte(draw, ox, oy):
    """Tile 22: Porte d'entrée avec encadrement."""
    rect(draw, ox, oy, ox + 31, oy + 31, BM3)
    # Encadrement de porte
    rect(draw, ox + 8, oy + 4, ox + 23, oy + 31, BLK)
    # Battants de porte (bois sombre)
    rect(draw, ox + 9, oy + 5, ox + 15, oy + 31, WD2)
    rect(draw, ox + 16, oy + 5, ox + 22, oy + 31, WD3)
    # Panneau central
    rect(draw, ox + 10, oy + 8, ox + 14, oy + 16, WD1)
    rect(draw, ox + 17, oy + 8, ox + 21, oy + 16, WD1)
    rect(draw, ox + 10, oy + 20, ox + 14, oy + 28, WD1)
    rect(draw, ox + 17, oy + 20, ox + 21, oy + 28, WD1)
    # Poignée
    px(draw, ox + 14, oy + 19, MT3)
    px(draw, ox + 17, oy + 19, MT3)
    # Seuil
    hline(draw, ox + 8, ox + 23, oy + 4, BLK)
    # Marche
    rect(draw, ox + 6, oy + 30, ox + 25, oy + 31, P3)
    hline(draw, ox + 6, ox + 25, oy + 30, P4)

def draw_fenetre(draw, ox, oy):
    """Tile 23: Fenêtre extérieure avec reflets."""
    rect(draw, ox, oy, ox + 31, oy + 31, BM3)
    # Encadrement fenêtre
    rect(draw, ox + 6, oy + 6, ox + 25, oy + 25, BM1)
    # Vitre
    rect(draw, ox + 8, oy + 8, ox + 23, oy + 23, WN1)
    # Croisillon
    hline(draw, ox + 8, ox + 23, oy + 15, BM2)
    hline(draw, ox + 8, ox + 23, oy + 16, BM2)
    vline(draw, ox + 15, oy + 8, oy + 23, BM2)
    vline(draw, ox + 16, oy + 8, oy + 23, BM2)
    # Reflets en diagonale
    for i in range(5):
        x1, y1 = ox + 10 + i, oy + 9
        if x1 < ox + 15 and y1 < oy + 15:
            px(draw, x1, y1, WN3)
    for i in range(4):
        x1, y1 = ox + 18 + i, oy + 18
        if x1 < ox + 23 and y1 < oy + 23:
            px(draw, x1, y1, WN3)
    # Rebord
    rect(draw, ox + 6, oy + 24, ox + 25, oy + 25, BM1)
    hline(draw, ox + 6, ox + 25, oy + 26, BM2)

# ══════════════════════════════════════════════════════════════
# ROW 3 : INTÉRIEUR BASIQUE (indices 24-31)
# ══════════════════════════════════════════════════════════════

def draw_sol_interieur(draw, ox, oy):
    """Tile 24: Sol parquet intérieur avec lames de bois."""
    # Lames de parquet verticales
    for col in range(4):
        x = ox + col * 8
        c_base = WD2 if col % 2 == 0 else WD3
        c_joint = WD1
        rect(draw, x, oy, x + 7, oy + 31, c_base)
        # Joint entre lames
        vline(draw, x, oy, oy + 31, c_joint)
        # Grain du bois
        rng = random.Random(2400 + col)
        for _ in range(6):
            gy = rng.randint(1, 30)
            gx = rng.randint(1, 6)
            px(draw, x + gx, oy + gy, WD4)
        for _ in range(3):
            gy = rng.randint(1, 30)
            gx = rng.randint(1, 6)
            px(draw, x + gx, oy + gy, WD1)

def draw_mur_interieur(draw, ox, oy):
    """Tile 25: Mur intérieur avec plinthe détaillée."""
    # Mur supérieur
    rect(draw, ox, oy, ox + 31, oy + 25, MI3)
    # Texture subtile
    rng = random.Random(2500)
    for _ in range(12):
        px(draw, rng.randint(0, 31) + ox, rng.randint(0, 24) + oy, MI4)
    for _ in range(6):
        px(draw, rng.randint(0, 31) + ox, rng.randint(0, 24) + oy, MI2)
    # Ligne de séparation
    hline(draw, ox, ox + 31, oy + 24, MI1)
    # Plinthe
    rect(draw, ox, oy + 25, ox + 31, oy + 31, WD2)
    hline(draw, ox, ox + 31, oy + 25, WD3)
    hline(draw, ox, ox + 31, oy + 31, WD1)
    # Détail plinthe
    hline(draw, ox, ox + 31, oy + 27, WD3)

def draw_comptoir(draw, ox, oy):
    """Tile 26: Comptoir (boutique/centre pokémon)."""
    # Sol
    rect(draw, ox, oy + 24, ox + 31, oy + 31, CL2)
    # Comptoir - face avant
    rect(draw, ox, oy, ox + 31, oy + 23, MI2)
    # Dessus du comptoir
    rect(draw, ox, oy, ox + 31, oy + 3, MT3)
    hline(draw, ox, ox + 31, oy, MT4)
    hline(draw, ox, ox + 31, oy + 3, MT1)
    # Panneau avant avec détail
    rect(draw, ox + 2, oy + 6, ox + 29, oy + 21, MI3)
    rect(draw, ox + 3, oy + 7, ox + 28, oy + 20, MI4)
    # Croix rouge (Centre Pokémon)
    rect(draw, ox + 13, oy + 9, ox + 18, oy + 18, (220, 60, 60))
    rect(draw, ox + 10, oy + 12, ox + 21, oy + 15, (220, 60, 60))
    # Bord bas
    hline(draw, ox, ox + 31, oy + 23, MI1)

def draw_machine_soin(draw, ox, oy):
    """Tile 27: Machine de soin du Centre Pokémon."""
    # Sol
    rect(draw, ox, oy + 24, ox + 31, oy + 31, CL2)
    # Base de la machine
    rect(draw, ox + 4, oy + 8, ox + 27, oy + 23, MT2)
    rect(draw, ox + 4, oy + 8, ox + 27, oy + 9, MT3)
    # Écran
    rect(draw, ox + 8, oy + 11, ox + 23, oy + 17, (32, 48, 32))
    rect(draw, ox + 9, oy + 12, ox + 22, oy + 16, (48, 200, 64))
    # Croix sur l'écran
    hline(draw, ox + 13, ox + 18, oy + 14, (96, 240, 112))
    vline(draw, ox + 15, oy + 12, oy + 16, (96, 240, 112))
    vline(draw, ox + 16, oy + 12, oy + 16, (96, 240, 112))
    # Slots Poké Ball
    for i in range(3):
        sx = ox + 10 + i * 4
        rect(draw, sx, oy + 19, sx + 2, oy + 21, MT1)
        px(draw, sx + 1, oy + 20, (220, 60, 60))
    # Dessus
    rect(draw, ox + 2, oy + 6, ox + 29, oy + 8, MT3)
    hline(draw, ox + 2, ox + 29, oy + 6, MT4)
    # Bords
    vline(draw, ox + 4, oy + 8, oy + 23, MT1)
    vline(draw, ox + 27, oy + 8, oy + 23, MT1)

def draw_etagere(draw, ox, oy):
    """Tile 28: Étagère avec livres."""
    # Mur fond
    rect(draw, ox, oy, ox + 31, oy + 31, MI3)
    # Étagère cadre
    rect(draw, ox + 2, oy + 2, ox + 29, oy + 29, WD2)
    rect(draw, ox + 3, oy + 3, ox + 28, oy + 28, WD3)
    # Planches horizontales
    for sy in [3, 12, 21]:
        rect(draw, ox + 3, oy + sy, ox + 28, oy + sy + 1, WD2)
        hline(draw, ox + 3, ox + 28, oy + sy, WD1)
    # Livres - rang 1
    books1 = [(5, (180, 40, 40)), (8, (40, 80, 180)), (11, (40, 160, 60)),
              (14, (180, 140, 40)), (17, (140, 40, 140)), (20, (200, 100, 40)),
              (23, (60, 60, 180)), (26, (180, 60, 100))]
    for bx, bc in books1:
        rect(draw, ox + bx, oy + 5, ox + bx + 1, oy + 11, bc)
        px(draw, ox + bx, oy + 5, blend(bc, (255, 255, 255), 0.3))
    # Livres - rang 2
    books2 = [(4, (60, 120, 180)), (7, (180, 80, 40)), (10, (40, 140, 100)),
              (13, (160, 60, 160)), (16, (200, 180, 40)), (19, (60, 60, 140)),
              (22, (140, 40, 40)), (25, (40, 160, 160))]
    for bx, bc in books2:
        rect(draw, ox + bx, oy + 14, ox + bx + 1, oy + 20, bc)
        px(draw, ox + bx, oy + 14, blend(bc, (255, 255, 255), 0.3))
    # Objets rang 3
    rect(draw, ox + 6, oy + 24, ox + 10, oy + 28, (180, 80, 80))  # boîte
    rect(draw, ox + 18, oy + 23, ox + 22, oy + 28, MT2)  # objet métallique
    px(draw, ox + 20, oy + 24, MT4)

def draw_tapis(draw, ox, oy):
    """Tile 29: Tapis rouge avec motif."""
    # Base tapis
    rect(draw, ox, oy, ox + 31, oy + 31, TP2)
    # Bordure
    rect(draw, ox, oy, ox + 31, oy + 1, TP1)
    rect(draw, ox, oy + 30, ox + 31, oy + 31, TP1)
    rect(draw, ox, oy, ox + 1, oy + 31, TP1)
    rect(draw, ox + 30, oy, ox + 31, oy + 31, TP1)
    # Liseré doré
    hline(draw, ox + 2, ox + 29, oy + 2, (200, 168, 80))
    hline(draw, ox + 2, ox + 29, oy + 29, (200, 168, 80))
    vline(draw, ox + 2, oy + 2, oy + 29, (200, 168, 80))
    vline(draw, ox + 29, oy + 2, oy + 29, (200, 168, 80))
    # Motif central (diamant)
    for i in range(5):
        px(draw, ox + 16 + i, oy + 16 - i, TP4)
        px(draw, ox + 16 - i, oy + 16 - i, TP4)
        px(draw, ox + 16 + i, oy + 16 + i, TP4)
        px(draw, ox + 16 - i, oy + 16 + i, TP4)
    # Texture subtile
    rng = random.Random(2900)
    for _ in range(15):
        px(draw, rng.randint(3, 28) + ox, rng.randint(3, 28) + oy, TP3)

def draw_sol_carrelage(draw, ox, oy):
    """Tile 30: Sol carrelage blanc (Centre Pokémon)."""
    rect(draw, ox, oy, ox + 31, oy + 31, CL3)
    # Joints
    for y in range(0, 32, 8):
        hline(draw, ox, ox + 31, oy + y, CL1)
    for x in range(0, 32, 8):
        vline(draw, ox + x, oy, oy + 31, CL1)
    # Reflets sur chaque carreau
    for ty in range(4):
        for tx in range(4):
            px(draw, ox + tx * 8 + 2, oy + ty * 8 + 2, CL4)
            px(draw, ox + tx * 8 + 3, oy + ty * 8 + 2, CL4)

def draw_mur_motif(draw, ox, oy):
    """Tile 31: Mur intérieur avec papier peint à motif."""
    rect(draw, ox, oy, ox + 31, oy + 25, MI3)
    # Motif losange subtil
    for row in range(4):
        for col in range(4):
            cx = ox + 4 + col * 8
            cy = oy + 3 + row * 6
            px(draw, cx, cy, MI4)
            px(draw, cx - 1, cy + 1, MI2)
            px(draw, cx + 1, cy + 1, MI2)
            px(draw, cx, cy + 2, MI4)
    # Plinthe identique
    hline(draw, ox, ox + 31, oy + 24, MI1)
    rect(draw, ox, oy + 25, ox + 31, oy + 31, WD2)
    hline(draw, ox, ox + 31, oy + 25, WD3)
    hline(draw, ox, ox + 31, oy + 31, WD1)
    hline(draw, ox, ox + 31, oy + 27, WD3)

# ══════════════════════════════════════════════════════════════
# ROW 4 : CHAMBRE / SALON (indices 32-39)
# ══════════════════════════════════════════════════════════════

def draw_lit_tete(draw, ox, oy):
    """Tile 32: Lit — tête (oreiller + couverture haut)."""
    # Sol
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)
    # Cadre du lit
    rect(draw, ox + 2, oy + 2, ox + 29, oy + 29, WD1)
    rect(draw, ox + 3, oy + 3, ox + 28, oy + 28, WD2)
    # Matelas
    rect(draw, ox + 4, oy + 4, ox + 27, oy + 28, (232, 228, 216))
    # Oreiller
    rect(draw, ox + 6, oy + 6, ox + 25, oy + 14, (240, 236, 224))
    rect(draw, ox + 7, oy + 7, ox + 24, oy + 13, (248, 244, 232))
    # Plis de l'oreiller
    hline(draw, ox + 10, ox + 21, oy + 10, (232, 228, 216))
    # Couverture (bleue FRLG)
    rect(draw, ox + 4, oy + 16, ox + 27, oy + 28, (80, 120, 200))
    hline(draw, ox + 4, ox + 27, oy + 16, (60, 96, 176))
    # Motif couverture
    for x in range(6, 26, 4):
        px(draw, ox + x, oy + 20, (100, 140, 216))
        px(draw, ox + x, oy + 24, (100, 140, 216))
    # Pli central
    hline(draw, ox + 4, ox + 27, oy + 22, (68, 104, 184))

def draw_lit_pied(draw, ox, oy):
    """Tile 33: Lit — pied (couverture bas)."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)
    rect(draw, ox + 2, oy + 2, ox + 29, oy + 25, WD1)
    rect(draw, ox + 3, oy + 3, ox + 28, oy + 24, WD2)
    # Couverture
    rect(draw, ox + 4, oy + 3, ox + 27, oy + 20, (80, 120, 200))
    for x in range(6, 26, 4):
        px(draw, ox + x, oy + 6, (100, 140, 216))
        px(draw, ox + x, oy + 12, (100, 140, 216))
    hline(draw, ox + 4, ox + 27, oy + 8, (68, 104, 184))
    hline(draw, ox + 4, ox + 27, oy + 14, (68, 104, 184))
    # Pied du lit
    rect(draw, ox + 2, oy + 22, ox + 29, oy + 25, WD1)
    hline(draw, ox + 2, ox + 29, oy + 22, WD3)
    # Sol visible
    rect(draw, ox, oy + 26, ox + 31, oy + 31, WD2)

def draw_tv(draw, ox, oy):
    """Tile 34: Télévision style rétro."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)  # sol
    # Meuble TV
    rect(draw, ox + 2, oy + 16, ox + 29, oy + 28, WD1)
    hline(draw, ox + 2, ox + 29, oy + 16, WD3)
    # TV corps
    rect(draw, ox + 6, oy + 2, ox + 25, oy + 18, DK_GREY)
    rect(draw, ox + 7, oy + 3, ox + 24, oy + 17, BLK)
    # Écran
    rect(draw, ox + 8, oy + 4, ox + 22, oy + 15, (40, 60, 80))
    rect(draw, ox + 9, oy + 5, ox + 21, oy + 14, (60, 100, 140))
    # Reflet
    for i in range(4):
        px(draw, ox + 10 + i, oy + 6, (100, 160, 200))
    px(draw, ox + 10, oy + 7, (80, 130, 170))
    # Bouton
    px(draw, ox + 24, oy + 8, (200, 60, 60))
    px(draw, ox + 24, oy + 11, MD_GREY)
    # Antenne
    px(draw, ox + 12, oy + 2, DK_GREY)
    px(draw, ox + 11, oy + 1, DK_GREY)
    px(draw, ox + 19, oy + 2, DK_GREY)
    px(draw, ox + 20, oy + 1, DK_GREY)

def draw_pc(draw, ox, oy):
    """Tile 35: PC/ordinateur sur bureau."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)  # sol
    # Bureau
    rect(draw, ox + 2, oy + 14, ox + 29, oy + 28, WD3)
    hline(draw, ox + 2, ox + 29, oy + 14, WD4)
    hline(draw, ox + 2, ox + 29, oy + 28, WD1)
    # Moniteur cadre
    rect(draw, ox + 8, oy + 1, ox + 23, oy + 13, DK_GREY)
    # Écran
    rect(draw, ox + 9, oy + 2, ox + 22, oy + 12, (32, 48, 96))
    rect(draw, ox + 10, oy + 3, ox + 21, oy + 11, (48, 80, 160))
    # Texte sur écran
    for x in range(12, 20, 2):
        px(draw, ox + x, oy + 6, (128, 200, 255))
        px(draw, ox + x, oy + 8, (128, 200, 255))
    # Pied moniteur
    rect(draw, ox + 14, oy + 13, ox + 17, oy + 14, DK_GREY)
    # Clavier
    rect(draw, ox + 8, oy + 16, ox + 23, oy + 19, MD_GREY)
    rect(draw, ox + 9, oy + 17, ox + 22, oy + 18, DK_GREY)
    # Touches
    for x in range(10, 22, 2):
        px(draw, ox + x, oy + 17, MD_GREY)
    # Souris
    rect(draw, ox + 25, oy + 16, ox + 27, oy + 18, MD_GREY)

def draw_plante(draw, ox, oy):
    """Tile 36: Plante verte en pot."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)  # sol
    # Pot
    rect(draw, ox + 10, oy + 20, ox + 21, oy + 28, (180, 88, 44))
    rect(draw, ox + 11, oy + 19, ox + 20, oy + 20, (196, 104, 56))
    rect(draw, ox + 12, oy + 28, ox + 19, oy + 29, (160, 72, 36))
    # Terre
    rect(draw, ox + 11, oy + 20, ox + 20, oy + 21, (96, 64, 32))
    # Feuilles — forme buissonnante
    cx, cy = 16, 14
    for dy in range(-8, 6):
        for dx in range(-9, 10):
            d = math.sqrt((dx * 0.9) ** 2 + (dy * 1.2) ** 2)
            if d < 8:
                x, y = ox + cx + dx, oy + cy + dy
                if 0 <= y - oy < 20:
                    if d > 6:
                        px(draw, x, y, L1)
                    elif dy > 2:
                        px(draw, x, y, L2)
                    elif dx < -3:
                        px(draw, x, y, L2)
                    elif dx > 3:
                        px(draw, x, y, L4)
                    else:
                        px(draw, x, y, L3)
    # Highlight feuilles
    rng = random.Random(3600)
    for _ in range(4):
        lx = rng.randint(9, 23)
        ly = rng.randint(8, 18)
        d = math.sqrt(((lx - cx) * 0.9) ** 2 + ((ly - cy) * 1.2) ** 2)
        if d < 6:
            px(draw, ox + lx, oy + ly, L5)

def draw_escalier_up(draw, ox, oy):
    """Tile 37: Escalier montant."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)
    # Marches 3D — perspective descendante
    step_h = 4
    for i in range(8):
        y = oy + i * step_h
        shade = blend(WD3, WD1, i / 8.0)
        rect(draw, ox + 2, y, ox + 29, y + step_h - 1, shade)
        hline(draw, ox + 2, ox + 29, y, WD4)
        hline(draw, ox + 2, ox + 29, y + step_h - 1, WD1)
    # Rampe gauche
    vline(draw, ox + 1, oy, oy + 31, WD1)
    vline(draw, ox + 2, oy, oy + 31, WD1)
    # Rampe droite
    vline(draw, ox + 29, oy, oy + 31, WD1)
    vline(draw, ox + 30, oy, oy + 31, WD1)
    # Flèche indicative vers le haut
    px(draw, ox + 16, oy + 4, (255, 255, 200))
    px(draw, ox + 15, oy + 5, (255, 255, 200))
    px(draw, ox + 17, oy + 5, (255, 255, 200))

def draw_escalier_down(draw, ox, oy):
    """Tile 38: Escalier descendant."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)
    step_h = 4
    for i in range(8):
        y = oy + i * step_h
        shade = blend(WD1, WD3, i / 8.0)
        rect(draw, ox + 2, y, ox + 29, y + step_h - 1, shade)
        hline(draw, ox + 2, ox + 29, y, shade)
        hline(draw, ox + 2, ox + 29, y + step_h - 1, WD1)
    # Rampes
    vline(draw, ox + 1, oy, oy + 31, WD1)
    vline(draw, ox + 2, oy, oy + 31, WD1)
    vline(draw, ox + 29, oy, oy + 31, WD1)
    vline(draw, ox + 30, oy, oy + 31, WD1)
    # Effet de profondeur : plus sombre en bas
    rect(draw, ox + 3, oy + 28, ox + 28, oy + 31, BLK)
    rect(draw, ox + 3, oy + 26, ox + 28, oy + 27, DK_GREY)

def draw_paillasson(draw, ox, oy):
    """Tile 39: Paillasson devant la porte."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)  # sol
    # Paillasson rectangulaire
    rect(draw, ox + 4, oy + 10, ox + 27, oy + 22, (140, 108, 60))
    rect(draw, ox + 5, oy + 11, ox + 26, oy + 21, (160, 128, 76))
    # Bordure
    rect(draw, ox + 4, oy + 10, ox + 27, oy + 10, (120, 88, 44))
    rect(draw, ox + 4, oy + 22, ox + 27, oy + 22, (120, 88, 44))
    # Texture fibres
    for y in range(12, 21):
        for x in range(6, 26, 2):
            if (x + y) % 3 == 0:
                px(draw, ox + x, oy + y, (148, 116, 68))
            elif (x + y) % 5 == 0:
                px(draw, ox + x, oy + y, (132, 100, 56))
    # Texte "WELCOME" en pixels (simplifié)
    # W
    for dy in [14, 15, 16, 17]:
        px(draw, ox + 9, oy + dy, (100, 72, 36))
    px(draw, ox + 10, oy + 17, (100, 72, 36))
    for dy in [14, 15, 16, 17]:
        px(draw, ox + 11, oy + dy, (100, 72, 36))

# ══════════════════════════════════════════════════════════════
# ROW 5 : INTÉRIEUR AVANCÉ (indices 40-47)
# ══════════════════════════════════════════════════════════════

def draw_porte_int(draw, ox, oy):
    """Tile 40: Porte intérieure."""
    rect(draw, ox, oy, ox + 31, oy + 31, MI3)  # mur
    # Encadrement
    rect(draw, ox + 8, oy + 2, ox + 23, oy + 31, WD1)
    # Porte
    rect(draw, ox + 9, oy + 3, ox + 22, oy + 31, WD3)
    # Panneaux
    rect(draw, ox + 10, oy + 5, ox + 21, oy + 13, WD2)
    rect(draw, ox + 11, oy + 6, ox + 20, oy + 12, WD1)
    rect(draw, ox + 10, oy + 17, ox + 21, oy + 27, WD2)
    rect(draw, ox + 11, oy + 18, ox + 20, oy + 26, WD1)
    # Poignée ronde
    px(draw, ox + 20, oy + 16, MT4)
    px(draw, ox + 21, oy + 16, MT3)
    px(draw, ox + 20, oy + 15, MT3)

def draw_fenetre_int(draw, ox, oy):
    """Tile 41: Fenêtre intérieure avec rideaux."""
    rect(draw, ox, oy, ox + 31, oy + 31, MI3)
    # Encadrement bois
    rect(draw, ox + 4, oy + 2, ox + 27, oy + 24, WD1)
    # Vitre
    rect(draw, ox + 6, oy + 4, ox + 25, oy + 22, WN1)
    # Croisillon
    hline(draw, ox + 6, ox + 25, oy + 13, WD2)
    vline(draw, ox + 15, oy + 4, oy + 22, WD2)
    vline(draw, ox + 16, oy + 4, oy + 22, WD2)
    # Ciel à travers la fenêtre
    rect(draw, ox + 6, oy + 4, ox + 14, oy + 12, (160, 200, 240))
    rect(draw, ox + 17, oy + 4, ox + 25, oy + 12, (160, 200, 240))
    rect(draw, ox + 6, oy + 14, ox + 14, oy + 22, (140, 188, 232))
    rect(draw, ox + 17, oy + 14, ox + 25, oy + 22, (140, 188, 232))
    # Rideaux
    for y in range(4, 23):
        px(draw, ox + 6, oy + y, (200, 160, 60))
        px(draw, ox + 7, oy + y, (216, 176, 72))
        px(draw, ox + 24, oy + y, (216, 176, 72))
        px(draw, ox + 25, oy + y, (200, 160, 60))
    # Rebord
    rect(draw, ox + 4, oy + 23, ox + 27, oy + 24, WD2)
    hline(draw, ox + 4, ox + 27, oy + 23, WD3)
    # Tringle
    hline(draw, ox + 4, ox + 27, oy + 2, WD1)
    hline(draw, ox + 4, ox + 27, oy + 3, WD2)

def draw_sol_bois_fonce(draw, ox, oy):
    """Tile 42: Sol bois foncé (variante)."""
    for col in range(4):
        x = ox + col * 8
        c_base = WD1 if col % 2 == 0 else WD2
        c_joint = TK1
        rect(draw, x, oy, x + 7, oy + 31, c_base)
        vline(draw, x, oy, oy + 31, c_joint)
        # Nœuds du bois
        rng = random.Random(4200 + col)
        for _ in range(2):
            ny = rng.randint(4, 27)
            nx = rng.randint(2, 5)
            px(draw, x + nx, oy + ny, blend(c_base, TK1, 0.5))
            px(draw, x + nx + 1, oy + ny, blend(c_base, TK1, 0.3))

def draw_mur_ext_fenetre(draw, ox, oy):
    """Tile 43: Mur extérieur avec petite fenêtre."""
    rect(draw, ox, oy, ox + 31, oy + 31, BM3)
    # Briques
    for row in range(8):
        y = oy + row * 4
        hline(draw, ox, ox + 31, y, BM2)
    # Fenêtre
    rect(draw, ox + 10, oy + 8, ox + 21, oy + 20, BM1)
    rect(draw, ox + 11, oy + 9, ox + 20, oy + 19, WN1)
    vline(draw, ox + 15, oy + 9, oy + 19, BM2)
    vline(draw, ox + 16, oy + 9, oy + 19, BM2)
    # Reflet
    px(draw, ox + 13, oy + 11, WN3)
    px(draw, ox + 14, oy + 11, WN3)
    px(draw, ox + 13, oy + 12, WN2)
    # Rebord
    rect(draw, ox + 9, oy + 20, ox + 22, oy + 21, BM1)

def draw_table(draw, ox, oy):
    """Tile 44: Table ronde / de salle à manger."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)  # sol
    # Dessus de table ovale
    cx, cy = 16, 12
    for dy in range(-8, 9):
        for dx in range(-12, 13):
            d = math.sqrt((dx / 12.0) ** 2 + (dy / 8.0) ** 2)
            if d < 1.0:
                x, y = ox + cx + dx, oy + cy + dy
                if d > 0.85:
                    px(draw, x, y, WD1)
                elif dx + dy < -4:
                    px(draw, x, y, WD3)
                else:
                    px(draw, x, y, WD4)
    # Pied central
    rect(draw, ox + 14, oy + 20, ox + 17, oy + 28, WD1)
    px(draw, ox + 15, oy + 21, WD2)
    px(draw, ox + 16, oy + 21, WD2)
    # Objet sur la table (vase)
    rect(draw, ox + 14, oy + 7, ox + 17, oy + 11, (160, 60, 60))
    px(draw, ox + 15, oy + 6, L3)
    px(draw, ox + 16, oy + 5, L4)
    px(draw, ox + 14, oy + 6, L2)

def draw_chaise(draw, ox, oy):
    """Tile 45: Chaise en bois."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)  # sol
    # Pieds arrière (dossier vu de face)
    rect(draw, ox + 8, oy + 2, ox + 10, oy + 28, WD1)
    rect(draw, ox + 21, oy + 2, ox + 23, oy + 28, WD1)
    # Dossier
    rect(draw, ox + 8, oy + 2, ox + 23, oy + 4, WD1)
    hline(draw, ox + 8, ox + 23, oy + 2, WD3)
    # Barreaux dossier
    for x in [12, 16, 19]:
        vline(draw, ox + x, oy + 4, oy + 12, WD1)
    # Assise
    rect(draw, ox + 7, oy + 14, ox + 24, oy + 18, WD3)
    hline(draw, ox + 7, ox + 24, oy + 14, WD4)
    hline(draw, ox + 7, ox + 24, oy + 18, WD1)
    # Pieds avant
    rect(draw, ox + 7, oy + 18, ox + 9, oy + 28, WD1)
    rect(draw, ox + 22, oy + 18, ox + 24, oy + 28, WD1)

def draw_poster(draw, ox, oy):
    """Tile 46: Poster au mur (décoratif)."""
    rect(draw, ox, oy, ox + 31, oy + 31, MI3)  # mur
    # Cadre poster
    rect(draw, ox + 4, oy + 4, ox + 27, oy + 24, WD1)
    rect(draw, ox + 5, oy + 5, ox + 26, oy + 23, (240, 236, 224))
    # Image : paysage stylisé (montagne + ciel)
    rect(draw, ox + 6, oy + 6, ox + 25, oy + 12, (140, 180, 220))  # ciel
    rect(draw, ox + 6, oy + 13, ox + 25, oy + 22, (80, 160, 80))   # herbe
    # Montagne
    for i in range(8):
        px(draw, ox + 16 - i, oy + 12 - i, (120, 112, 100))
        px(draw, ox + 16 + i, oy + 12 - i, (120, 112, 100))
        if i < 6:
            hline(draw, ox + 16 - i, ox + 16 + i, oy + 12 - i, (136, 128, 112))
    # Soleil
    rect(draw, ox + 21, oy + 7, ox + 23, oy + 9, (248, 216, 64))
    # Clou
    px(draw, ox + 16, oy + 3, MD_GREY)

def draw_poubelle(draw, ox, oy):
    """Tile 47: Poubelle / corbeille."""
    rect(draw, ox, oy, ox + 31, oy + 31, WD2)  # sol
    # Corps cylindrique
    rect(draw, ox + 10, oy + 8, ox + 21, oy + 26, MD_GREY)
    # Couvercle
    rect(draw, ox + 8, oy + 6, ox + 23, oy + 8, DK_GREY)
    hline(draw, ox + 8, ox + 23, oy + 6, MD_GREY)
    # Poignée couvercle
    rect(draw, ox + 14, oy + 4, ox + 17, oy + 6, DK_GREY)
    px(draw, ox + 15, oy + 5, MD_GREY)
    # Bandes décoratives
    hline(draw, ox + 10, ox + 21, oy + 12, DK_GREY)
    hline(draw, ox + 10, ox + 21, oy + 20, DK_GREY)
    # Reflet
    for y in range(9, 25):
        px(draw, ox + 12, oy + y, blend(MD_GREY, (200, 200, 200), 0.3))
    # Base
    rect(draw, ox + 10, oy + 26, ox + 21, oy + 27, DK_GREY)
    # Ombre
    for x in range(22, 26):
        px(draw, ox + x, oy + 27, blend(WD2, BLK, 0.2))

# ══════════════════════════════════════════════════════════════
# ASSEMBLAGE FINAL
# ══════════════════════════════════════════════════════════════

TILE_FUNCTIONS = [
    # Row 0: Terrain extérieur
    draw_herbe, draw_herbe_haute, draw_chemin, draw_sable,
    draw_eau, draw_fleur, draw_herbe_alt, draw_herbe_detail,
    # Row 1: Végétation & clôtures
    draw_arbre_haut, draw_arbre_bas, draw_arbre_haut_r, draw_arbre_bas_r,
    draw_cloture_h, draw_cloture_v, draw_buisson, draw_herbe_detail2,
    # Row 2: Bâtiments extérieurs
    draw_toit_gauche, draw_toit_milieu, draw_toit_droit,
    draw_mur_gauche, draw_mur_milieu, draw_mur_droit,
    draw_porte, draw_fenetre,
    # Row 3: Intérieur basique
    draw_sol_interieur, draw_mur_interieur, draw_comptoir, draw_machine_soin,
    draw_etagere, draw_tapis, draw_sol_carrelage, draw_mur_motif,
    # Row 4: Chambre / Salon
    draw_lit_tete, draw_lit_pied, draw_tv, draw_pc,
    draw_plante, draw_escalier_up, draw_escalier_down, draw_paillasson,
    # Row 5: Intérieur avancé
    draw_porte_int, draw_fenetre_int, draw_sol_bois_fonce, draw_mur_ext_fenetre,
    draw_table, draw_chaise, draw_poster, draw_poubelle,
]

def main():
    img = Image.new("RGBA", (COLS * TILE, ROWS * TILE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for idx, func in enumerate(TILE_FUNCTIONS):
        col = idx % COLS
        row = idx // COLS
        ox = col * TILE
        oy = row * TILE
        func(draw, ox, oy)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT)
    print(f"✓ Tileset v6 FRLG HD généré : {OUT}")
    print(f"  {COLS}×{ROWS} = {COLS * ROWS} tiles de {TILE}×{TILE}px")
    print(f"  Taille image : {img.size[0]}×{img.size[1]}px")

    # Analyse qualité
    from collections import Counter
    total_colors = set()
    for idx, func in enumerate(TILE_FUNCTIONS):
        col = idx % COLS
        row = idx // COLS
        tile_img = img.crop((col * TILE, row * TILE, (col + 1) * TILE, (row + 1) * TILE))
        colors = set(tile_img.getdata())
        colors.discard((0, 0, 0, 0))
        total_colors.update(colors)
    print(f"  Couleurs uniques totales : {len(total_colors)}")

if __name__ == "__main__":
    main()
