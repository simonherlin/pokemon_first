#!/usr/bin/env python3
"""
Générateur de tileset FRLG HD amélioré.
Produit des tiles 32×32 avec des textures riches, plus de couleurs,
dithering et motifs détaillés inspirés de Pokémon FRLG.
Atlas 256×256 (8×8 = 64 tiles).
"""

from PIL import Image, ImageDraw
import random
import math

TILE = 32
COLS = 8
ROWS = 8
W, H = COLS * TILE, ROWS * TILE

# Seed fixe pour résultats reproductibles
random.seed(42)

# ============================================================================
# PALETTE FRLG AMÉLIORÉE
# ============================================================================
# Herbe
G1 = (48, 160, 48)    # vert foncé
G2 = (64, 184, 64)    # vert moyen
G3 = (88, 200, 80)    # vert clair
G4 = (112, 216, 96)   # vert lumineux
G5 = (40, 136, 40)    # vert très foncé

# Herbe haute
HG1 = (32, 128, 48)
HG2 = (48, 152, 56)
HG3 = (64, 168, 72)
HG4 = (80, 184, 88)

# Chemin / terre
P1 = (192, 168, 128)  # sable clair
P2 = (176, 152, 112)  # terre
P3 = (160, 136, 96)   # terre foncée
P4 = (200, 180, 144)  # sable très clair
P5 = (144, 120, 80)   # terre sombre

# Sable
S1 = (232, 216, 168)
S2 = (216, 200, 152)
S3 = (200, 184, 136)
S4 = (240, 224, 184)

# Eau
W1 = (48, 104, 200)   # bleu foncé
W2 = (72, 128, 216)   # bleu moyen
W3 = (96, 152, 232)   # bleu clair
W4 = (120, 176, 240)  # bleu lumineux
W5 = (32, 80, 168)    # bleu profond

# Arbres
T1 = (24, 96, 32)     # feuillage foncé
T2 = (40, 120, 48)    # feuillage moyen
T3 = (56, 144, 56)    # feuillage clair
T4 = (72, 160, 72)    # feuillage lumineux
TB = (96, 64, 40)     # tronc
TB2 = (120, 80, 48)   # tronc clair

# Toits (rouge FRLG)
R1 = (176, 48, 48)
R2 = (200, 72, 64)
R3 = (224, 96, 80)
R4 = (152, 32, 32)

# Murs extérieurs
MW1 = (216, 208, 192)  # mur clair
MW2 = (192, 184, 168)  # mur moyen
MW3 = (168, 160, 144)  # mur foncé
MW4 = (232, 224, 208)  # mur très clair

# Sol intérieur (parquet)
FL1 = (200, 168, 120)
FL2 = (184, 152, 104)
FL3 = (216, 184, 136)
FL4 = (168, 136, 88)

# Mur intérieur
WI1 = (232, 224, 200)
WI2 = (216, 208, 184)
WI3 = (200, 192, 168)
WI4 = (240, 232, 208)

# Carrelage
CR1 = (224, 232, 240)
CR2 = (208, 216, 224)
CR3 = (192, 200, 208)
CR4 = (232, 240, 248)

# Bois
WOOD1 = (152, 112, 64)
WOOD2 = (136, 96, 48)
WOOD3 = (168, 128, 80)
WOOD4 = (120, 80, 40)

# Fleurs
FL_R = (232, 72, 72)
FL_Y = (240, 216, 72)
FL_W = (248, 248, 232)
FL_P = (232, 128, 192)

# Clôture
FE1 = (184, 152, 112)
FE2 = (168, 136, 96)
FE3 = (200, 168, 128)

# Tapis (bleu)
TA1 = (72, 104, 160)
TA2 = (88, 120, 176)
TA3 = (56, 88, 144)
TA4 = (104, 136, 192)

# Outline
OL = (32, 32, 40)

def _clamp(v):
    return max(0, min(255, v))

def _noisy(col, amount=8):
    """Add per-pixel noise to a color."""
    return tuple(_clamp(c + random.randint(-amount, amount)) for c in col[:3])

def px(img, x, y, col, ox=0, oy=0, noise=0):
    """Set pixel with offset and optional noise."""
    ax, ay = ox + x, oy + y
    if 0 <= ax < W and 0 <= ay < H:
        if noise > 0:
            c = _noisy(col, noise)
        else:
            c = col[:3]
        img.putpixel((ax, ay), c + (255,))

def fill(img, x1, y1, x2, y2, col, ox=0, oy=0, noise=6):
    for yy in range(y1, y2 + 1):
        for xx in range(x1, x2 + 1):
            px(img, xx, yy, col, ox, oy, noise=noise)

def noise_fill(img, x1, y1, x2, y2, colors, ox=0, oy=0, weights=None, noise=10):
    """Fill with random color picks + per-pixel noise."""
    if weights is None:
        weights = [1] * len(colors)
    total = sum(weights)
    for yy in range(y1, y2 + 1):
        for xx in range(x1, x2 + 1):
            r = random.random() * total
            cumul = 0
            for i, w in enumerate(weights):
                cumul += w
                if r <= cumul:
                    px(img, xx, yy, colors[i], ox, oy, noise=noise)
                    break

def dither_fill(img, x1, y1, x2, y2, c1, c2, ox=0, oy=0, noise=6):
    """Checkerboard dithering between two colors."""
    for yy in range(y1, y2 + 1):
        for xx in range(x1, x2 + 1):
            if (xx + yy) % 2 == 0:
                px(img, xx, yy, c1, ox, oy, noise=noise)
            else:
                px(img, xx, yy, c2, ox, oy, noise=noise)

def tile_origin(idx):
    """Return (ox, oy) for tile index."""
    return (idx % COLS) * TILE, (idx // COLS) * TILE


# ============================================================================
# TILE DRAWING FUNCTIONS
# ============================================================================

def draw_grass(img, idx):
    """Tile 0: Herbe de base avec texture."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [G1, G2, G3, G4, G5], ox, oy, [2, 4, 3, 1, 1])

def draw_tall_grass(img, idx):
    """Tile 1: Herbe haute."""
    ox, oy = tile_origin(idx)
    # Base herbe
    noise_fill(img, 0, 0, 31, 31, [G1, G2, G3], ox, oy, [2, 3, 2])
    # Touffes d'herbe haute (motif en V)
    tufts = [(4, 2), (12, 5), (20, 3), (28, 6), (8, 14), (16, 12), (24, 15),
             (4, 22), (12, 25), (20, 22), (28, 26), (8, 18), (16, 28)]
    for tx, ty in tufts:
        for dy in range(-4, 0):
            px(img, tx - 1, ty + dy, HG1, ox, oy)
            px(img, tx, ty + dy, HG2, ox, oy)
            px(img, tx + 1, ty + dy, HG3, ox, oy)
        px(img, tx - 2, ty - 2, HG4, ox, oy)
        px(img, tx + 2, ty - 2, HG4, ox, oy)

def draw_path(img, idx):
    """Tile 2: Chemin / terre."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [P1, P2, P3, P4, P5], ox, oy, [3, 3, 2, 2, 1])
    # Petits cailloux
    for _ in range(8):
        cx, cy = random.randint(2, 29), random.randint(2, 29)
        px(img, cx, cy, P5, ox, oy)
        px(img, cx + 1, cy, P3, ox, oy)

def draw_sand(img, idx):
    """Tile 3: Sable."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [S1, S2, S3, S4], ox, oy, [3, 3, 2, 2])

def draw_water(img, idx):
    """Tile 4: Eau avec vagues."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [W1, W2, W3, W5], ox, oy, [2, 3, 2, 1])
    # Vagues horizontales
    for wave_y in [6, 14, 22, 30]:
        for x in range(0, 32, 2):
            offset = int(2 * math.sin(x * 0.5))
            py = wave_y + offset
            if 0 <= py < 32:
                px(img, x, py, W4, ox, oy)
                px(img, x + 1, py, W3, ox, oy)

def draw_flowers(img, idx):
    """Tile 5: Herbe avec fleurs."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [G1, G2, G3, G4], ox, oy, [2, 4, 3, 1])
    # Petites fleurs
    colors = [FL_R, FL_Y, FL_W, FL_P]
    positions = [(4, 4), (15, 7), (26, 3), (8, 16), (20, 14), (4, 26), (15, 24), (26, 28)]
    for i, (fx, fy) in enumerate(positions):
        c = colors[i % len(colors)]
        px(img, fx, fy, c, ox, oy)
        px(img, fx - 1, fy, c, ox, oy)
        px(img, fx + 1, fy, c, ox, oy)
        px(img, fx, fy - 1, c, ox, oy)
        px(img, fx, fy + 1, G5, ox, oy)

def draw_tree_top(img, idx, side="left"):
    """Tile 8/10: Haut d'arbre."""
    ox, oy = tile_origin(idx)
    # Fond transparent (herbe pour seamless)
    noise_fill(img, 0, 0, 31, 31, [G1, G2, G3], ox, oy, [2, 3, 2])
    # Feuillage (cercle en haut)
    cx, cy = (24 if side == "left" else 8), 16
    for y in range(0, 32):
        for x in range(0, 32):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if dist < 14:
                if dist < 6:
                    c = T3 if (x + y) % 3 == 0 else T4
                elif dist < 10:
                    c = T2 if (x + y) % 2 == 0 else T3
                else:
                    c = T1 if (x + y) % 2 == 0 else T2
                px(img, x, y, c, ox, oy)
    # Contour
    for y in range(0, 32):
        for x in range(0, 32):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if 13 <= dist < 15:
                px(img, x, y, T1, ox, oy)

def draw_tree_bottom(img, idx, side="left"):
    """Tile 9/11: Bas d'arbre (tronc + base feuillage)."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [G1, G2, G3], ox, oy, [2, 3, 2])
    cx = 24 if side == "left" else 8
    # Feuillage (partie basse du cercle)
    for y in range(0, 20):
        for x in range(0, 32):
            dist = ((x - cx) ** 2 + (y + 16 - 16) ** 2) ** 0.5
            if dist < 14:
                c = T2 if (x + y) % 2 == 0 else T3
                px(img, x, y, c, ox, oy)
    # Tronc
    fill(img, cx - 3, 10, cx + 2, 31, TB, ox, oy)
    fill(img, cx - 2, 10, cx + 1, 31, TB2, ox, oy)
    # Ombre tronc
    fill(img, cx - 3, 10, cx - 3, 31, WOOD4, ox, oy)

def draw_fence_h(img, idx):
    """Tile 12: Clôture horizontale."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [G1, G2, G3], ox, oy, [2, 3, 2])
    # Barre horizontale
    fill(img, 0, 12, 31, 14, FE2, ox, oy)
    fill(img, 0, 13, 31, 13, FE3, ox, oy)
    fill(img, 0, 18, 31, 20, FE2, ox, oy)
    fill(img, 0, 19, 31, 19, FE3, ox, oy)
    # Poteaux
    for px_x in [0, 15, 31]:
        fill(img, px_x, 8, px_x + 1, 24, FE1, ox, oy)
        px(img, px_x, 8, OL, ox, oy)
        px(img, px_x + 1, 8, OL, ox, oy)

def draw_fence_v(img, idx):
    """Tile 13: Clôture verticale."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [G1, G2, G3], ox, oy, [2, 3, 2])
    # Barre verticale
    fill(img, 13, 0, 15, 31, FE2, ox, oy)
    fill(img, 14, 0, 14, 31, FE3, ox, oy)
    fill(img, 17, 0, 19, 31, FE2, ox, oy)
    fill(img, 18, 0, 18, 31, FE3, ox, oy)
    # Traverses
    for py_y in [0, 15, 31]:
        fill(img, 10, py_y, 22, py_y + 1, FE1, ox, oy)

def draw_bush(img, idx):
    """Tile 14: Buisson."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [G1, G2, G3], ox, oy, [2, 3, 2])
    # Buisson rond
    cx, cy = 16, 20
    for y in range(8, 32):
        for x in range(2, 30):
            dist = ((x - cx) ** 2 / 169 + (y - cy) ** 2 / 120)
            if dist < 1.0:
                if dist < 0.3:
                    c = T4
                elif dist < 0.6:
                    c = T3 if (x + y) % 2 == 0 else T2
                else:
                    c = T2 if (x + y) % 2 == 0 else T1
                px(img, x, y, c, ox, oy)

def draw_grass_detail(img, idx):
    """Tile 15: Herbe avec détails."""
    ox, oy = tile_origin(idx)
    noise_fill(img, 0, 0, 31, 31, [G2, G3, G4], ox, oy, [3, 3, 2])
    # Quelques brins plus foncés
    for _ in range(12):
        bx = random.randint(2, 29)
        by = random.randint(4, 29)
        px(img, bx, by, G5, ox, oy)
        px(img, bx, by - 1, G1, ox, oy)
        px(img, bx, by - 2, G1, ox, oy)

def draw_roof(img, idx, side):
    """Tile 16/17/18: Toit de maison."""
    ox, oy = tile_origin(idx)
    # Remplir avec tuiles rouges
    for y in range(0, 32):
        for x in range(0, 32):
            row = y // 4
            col = (x + (row % 2) * 4) // 8
            if y % 4 == 0:
                c = R4  # ligne de séparation
            elif (x + (row % 2) * 4) % 8 == 0:
                c = R4
            else:
                c = R2 if (row + col) % 2 == 0 else R3
            px(img, x, y, c, ox, oy, noise=8)
    # Ombre sur le bord
    if side == "left":
        for y in range(0, 32):
            px(img, 0, y, R4, ox, oy)
    elif side == "right":
        for y in range(0, 32):
            px(img, 31, y, R4, ox, oy)
    # Bord inférieur
    fill(img, 0, 30, 31, 31, R4, ox, oy)

def draw_wall(img, idx, side):
    """Tile 19/20/21: Mur extérieur de maison."""
    ox, oy = tile_origin(idx)
    # Mur en briques
    for y in range(0, 32):
        for x in range(0, 32):
            row = y // 4
            offset = (row % 2) * 4
            if y % 4 == 0:
                c = MW3
            elif (x + offset) % 8 == 0:
                c = MW3
            else:
                c = MW1 if (x + y) % 7 < 4 else MW2
            px(img, x, y, c, ox, oy, noise=8)
    # Ombre bord gauche
    if side == "left":
        fill(img, 0, 0, 1, 31, MW3, ox, oy)
    elif side == "right":
        fill(img, 30, 0, 31, 31, MW3, ox, oy)

def draw_door(img, idx):
    """Tile 22: Porte extérieure."""
    ox, oy = tile_origin(idx)
    # Mur autour
    noise_fill(img, 0, 0, 31, 31, [MW1, MW2, MW4], ox, oy, [3, 2, 2])
    # Porte
    fill(img, 8, 4, 23, 31, WOOD2, ox, oy)
    fill(img, 9, 5, 22, 30, WOOD1, ox, oy)
    fill(img, 10, 6, 21, 29, WOOD3, ox, oy)
    # Panneau porte
    fill(img, 11, 8, 20, 16, WOOD2, ox, oy)
    fill(img, 11, 20, 20, 28, WOOD2, ox, oy)
    # Poignée
    px(img, 19, 18, (216, 200, 72), ox, oy)
    px(img, 19, 19, (200, 184, 56), ox, oy)
    # Encadrement
    fill(img, 7, 3, 7, 31, OL, ox, oy)
    fill(img, 24, 3, 24, 31, OL, ox, oy)
    fill(img, 7, 3, 24, 3, OL, ox, oy)

def draw_window(img, idx):
    """Tile 23: Fenêtre."""
    ox, oy = tile_origin(idx)
    # Mur
    noise_fill(img, 0, 0, 31, 31, [MW1, MW2, MW4], ox, oy, [3, 2, 2])
    # Cadre fenêtre
    fill(img, 6, 6, 25, 25, OL, ox, oy)
    fill(img, 7, 7, 24, 24, (56, 96, 168), ox, oy)  # bleu ciel
    fill(img, 8, 8, 23, 23, (88, 152, 216), ox, oy)
    # Croisillons
    fill(img, 15, 7, 16, 24, MW4, ox, oy)
    fill(img, 7, 15, 24, 16, MW4, ox, oy)
    # Reflet
    fill(img, 9, 9, 14, 14, (120, 184, 240), ox, oy)
    px(img, 10, 10, (168, 208, 248), ox, oy)
    px(img, 11, 10, (168, 208, 248), ox, oy)
    # Rideaux (petits triangles)
    for y in range(8, 14):
        w = y - 7
        px(img, 8, y, (200, 72, 72), ox, oy)
        if w > 1:
            px(img, 8 + w, y, (200, 72, 72), ox, oy)
        px(img, 23, y, (200, 72, 72), ox, oy)
        if w > 1:
            px(img, 23 - w, y, (200, 72, 72), ox, oy)

def draw_floor_int(img, idx):
    """Tile 24: Sol intérieur (parquet)."""
    ox, oy = tile_origin(idx)
    for y in range(0, 32):
        for x in range(0, 32):
            plank = x // 4
            if x % 4 == 0:
                c = FL4  # joint
            elif (plank + y // 16) % 2 == 0:
                c = FL1 if y % 3 != 0 else FL2
            else:
                c = FL2 if y % 3 != 0 else FL3
            px(img, x, y, c, ox, oy, noise=8)

def draw_wall_int(img, idx):
    """Tile 25: Mur intérieur."""
    ox, oy = tile_origin(idx)
    # Partie haute (mur)
    for y in range(0, 24):
        for x in range(0, 32):
            if y < 4:
                c = WI3  # corniche
            else:
                c = WI1 if (x + y) % 5 < 3 else WI2
            px(img, x, y, c, ox, oy)
    # Plinthe (bas)
    fill(img, 0, 24, 31, 25, WI3, ox, oy)
    fill(img, 0, 26, 31, 31, WOOD2, ox, oy)
    fill(img, 0, 27, 31, 27, WOOD3, ox, oy)
    # Ligne séparation
    fill(img, 0, 24, 31, 24, OL, ox, oy)

def draw_counter(img, idx):
    """Tile 26: Comptoir."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Surface comptoir
    fill(img, 2, 8, 29, 28, WOOD2, ox, oy)
    fill(img, 3, 9, 28, 27, WOOD1, ox, oy)
    fill(img, 4, 10, 27, 26, WOOD3, ox, oy)
    # Bord supérieur
    fill(img, 2, 6, 29, 8, WOOD4, ox, oy)
    fill(img, 3, 7, 28, 7, WOOD2, ox, oy)

def draw_heal_machine(img, idx):
    """Tile 27: Machine de soin."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, CR1, ox, oy)
    # Machine
    fill(img, 6, 6, 25, 28, (200, 200, 208), ox, oy)
    fill(img, 7, 7, 24, 27, (216, 216, 224), ox, oy)
    # Écran
    fill(img, 10, 10, 21, 18, (32, 80, 48), ox, oy)
    fill(img, 11, 11, 20, 17, (56, 160, 72), ox, oy)
    # Croix rouge
    fill(img, 14, 12, 17, 12, (232, 56, 56), ox, oy)
    fill(img, 15, 11, 16, 13, (232, 56, 56), ox, oy)
    # Emplacements balls
    fill(img, 10, 21, 14, 25, (248, 248, 248), ox, oy)
    fill(img, 17, 21, 21, 25, (248, 248, 248), ox, oy)
    px(img, 12, 23, (232, 56, 56), ox, oy)
    px(img, 19, 23, (232, 56, 56), ox, oy)

def draw_shelf(img, idx):
    """Tile 28: Étagère."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, WI1, ox, oy)
    # Étagères (3 niveaux)
    for shelf_y in [4, 14, 24]:
        fill(img, 3, shelf_y, 28, shelf_y + 1, WOOD2, ox, oy)
        fill(img, 3, shelf_y, 28, shelf_y, WOOD3, ox, oy)
        # Livres / objets
        for bx in range(5, 27, 3):
            h = random.randint(3, 5)
            c = random.choice([(200, 56, 56), (56, 56, 200), (56, 168, 56), (200, 168, 56)])
            fill(img, bx, shelf_y - h, bx + 1, shelf_y - 1, c, ox, oy)

def draw_carpet(img, idx):
    """Tile 29: Tapis bleu avec motif."""
    ox, oy = tile_origin(idx)
    # Base tapis
    noise_fill(img, 0, 0, 31, 31, [TA1, TA2, TA3], ox, oy, [3, 3, 2])
    # Bordure
    fill(img, 0, 0, 31, 1, TA3, ox, oy)
    fill(img, 0, 30, 31, 31, TA3, ox, oy)
    fill(img, 0, 0, 1, 31, TA3, ox, oy)
    fill(img, 30, 0, 31, 31, TA3, ox, oy)
    # Motif central (losange)
    cx, cy = 16, 16
    for y in range(4, 28):
        for x in range(4, 28):
            if abs(x - cx) + abs(y - cy) <= 10:
                px(img, x, y, TA4, ox, oy)
            elif abs(x - cx) + abs(y - cy) <= 12:
                px(img, x, y, TA2, ox, oy)

def draw_tile_floor(img, idx):
    """Tile 30: Carrelage."""
    ox, oy = tile_origin(idx)
    for y in range(0, 32):
        for x in range(0, 32):
            if x % 8 == 0 or y % 8 == 0:
                c = CR3
            else:
                tile_x, tile_y = x // 8, y // 8
                if (tile_x + tile_y) % 2 == 0:
                    c = CR1
                else:
                    c = CR4
            px(img, x, y, c, ox, oy, noise=6)

def draw_wall_pattern(img, idx):
    """Tile 31: Mur avec motif."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, WI1, ox, oy)
    # Motif losange
    for y in range(0, 32):
        for x in range(0, 32):
            if (x + y) % 8 == 0 or abs(x - y) % 8 == 0:
                px(img, x, y, WI3, ox, oy, noise=6)
    # Plinthe
    fill(img, 0, 26, 31, 31, WOOD2, ox, oy)

# Ligne 4 : Chambre
def draw_bed_head(img, idx):
    """Tile 32: Tête de lit."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Tête de lit (cadre bois)
    fill(img, 4, 2, 27, 31, WOOD2, ox, oy)
    fill(img, 5, 3, 26, 30, WOOD3, ox, oy)
    # Oreiller
    fill(img, 7, 12, 24, 22, (240, 240, 248), ox, oy)
    fill(img, 8, 13, 23, 21, (248, 248, 255), ox, oy)
    # Pli oreiller
    fill(img, 15, 14, 16, 20, (232, 232, 240), ox, oy)
    # Couverture (en haut)
    fill(img, 6, 23, 25, 30, (72, 112, 200), ox, oy)
    fill(img, 7, 24, 24, 29, (88, 128, 216), ox, oy)

def draw_bed_foot(img, idx):
    """Tile 33: Pied de lit."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Couverture
    fill(img, 4, 0, 27, 24, (72, 112, 200), ox, oy)
    fill(img, 5, 1, 26, 23, (88, 128, 216), ox, oy)
    fill(img, 6, 2, 25, 22, (104, 144, 224), ox, oy)
    # Motif couverture
    for y in range(4, 22, 4):
        fill(img, 8, y, 23, y, (72, 112, 200), ox, oy)
    # Cadre bois (pied)
    fill(img, 4, 25, 27, 30, WOOD2, ox, oy)
    fill(img, 5, 26, 26, 29, WOOD3, ox, oy)

def draw_tv(img, idx):
    """Tile 34: Télévision."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Meuble TV
    fill(img, 4, 18, 27, 30, WOOD2, ox, oy)
    fill(img, 5, 19, 26, 29, WOOD3, ox, oy)
    # TV
    fill(img, 6, 4, 25, 18, OL, ox, oy)
    fill(img, 7, 5, 24, 17, (40, 48, 56), ox, oy)
    # Écran
    fill(img, 8, 6, 23, 16, (56, 72, 88), ox, oy)
    fill(img, 9, 7, 22, 15, (72, 136, 160), ox, oy)
    # Reflet
    for y in range(8, 12):
        px(img, 10, y, (120, 184, 200), ox, oy)
        px(img, 11, y, (104, 168, 184), ox, oy)
    # LED
    px(img, 15, 17, (232, 56, 56), ox, oy)
    px(img, 16, 17, (56, 200, 56), ox, oy)

def draw_pc(img, idx):
    """Tile 35: Ordinateur PC."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Bureau
    fill(img, 2, 20, 29, 30, WOOD2, ox, oy)
    fill(img, 3, 21, 28, 29, WOOD3, ox, oy)
    # Moniteur
    fill(img, 8, 2, 23, 18, (192, 192, 200), ox, oy)
    fill(img, 9, 3, 22, 17, OL, ox, oy)
    fill(img, 10, 4, 21, 16, (32, 104, 48), ox, oy)
    fill(img, 11, 5, 20, 15, (48, 168, 64), ox, oy)
    # Texte écran
    for ty in [7, 10, 13]:
        fill(img, 12, ty, 12 + random.randint(4, 7), ty, (96, 216, 104), ox, oy)
    # Pied moniteur
    fill(img, 13, 18, 18, 20, (176, 176, 184), ox, oy)
    # Clavier
    fill(img, 8, 22, 23, 26, (208, 208, 216), ox, oy)
    for ky in [23, 25]:
        for kx in range(9, 23, 2):
            px(img, kx, ky, (176, 176, 184), ox, oy)

def draw_plant(img, idx):
    """Tile 36: Plante en pot."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Pot
    fill(img, 10, 22, 21, 30, (168, 80, 48), ox, oy)
    fill(img, 11, 23, 20, 29, (192, 104, 64), ox, oy)
    fill(img, 9, 22, 22, 22, (152, 72, 40), ox, oy)  # bord
    # Terre
    fill(img, 11, 21, 20, 22, (96, 64, 40), ox, oy)
    # Feuilles
    leaves = [(16, 8), (10, 12), (22, 12), (12, 6), (20, 6), (16, 3)]
    for lx, ly in leaves:
        fill(img, lx - 2, ly - 1, lx + 2, ly + 1, T3, ox, oy)
        fill(img, lx - 1, ly - 2, lx + 1, ly, T4, ox, oy)
    # Tige
    fill(img, 15, 10, 16, 21, T1, ox, oy)

def draw_stairs_up(img, idx):
    """Tile 37: Escalier montant."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL2, ox, oy)
    # Marches
    for i in range(6):
        y = 26 - i * 4
        shade = min(255, FL3[0] + i * 8), min(255, FL3[1] + i * 8), min(255, FL3[2] + i * 8)
        fill(img, 4, y, 27, y + 3, shade, ox, oy)
        fill(img, 4, y, 27, y, WOOD4, ox, oy)  # nez de marche
    # Flèche vers le haut
    for dy in range(0, 4):
        fill(img, 15 - dy, 4 + dy, 16 + dy, 4 + dy, OL, ox, oy)

def draw_stairs_down(img, idx):
    """Tile 38: Escalier descendant."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL2, ox, oy)
    # Marches (inverse)
    for i in range(6):
        y = 4 + i * 4
        shade = min(255, FL3[0] - i * 8), min(255, FL3[1] - i * 8), min(255, FL3[2] - i * 8)
        shade = tuple(max(0, c) for c in shade)
        fill(img, 4, y, 27, y + 3, shade, ox, oy)
        fill(img, 4, y, 27, y, WOOD4, ox, oy)
    # Flèche vers le bas
    for dy in range(0, 4):
        fill(img, 15 - dy, 28 - dy, 16 + dy, 28 - dy, OL, ox, oy)

def draw_doormat(img, idx):
    """Tile 39: Paillasson."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Paillasson
    fill(img, 4, 10, 27, 24, (152, 120, 80), ox, oy)
    fill(img, 5, 11, 26, 23, (168, 136, 96), ox, oy)
    # Texture fibres
    for y in range(12, 23):
        for x in range(6, 26):
            if (x + y) % 3 == 0:
                px(img, x, y, (144, 112, 72), ox, oy)

# Ligne 5 : Intérieur avancé
def draw_door_int(img, idx):
    """Tile 40: Porte intérieure."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, WI1, ox, oy)
    # Porte
    fill(img, 7, 2, 24, 31, WOOD2, ox, oy)
    fill(img, 8, 3, 23, 30, WOOD3, ox, oy)
    # Panneaux
    fill(img, 10, 5, 21, 14, WOOD2, ox, oy)
    fill(img, 10, 18, 21, 28, WOOD2, ox, oy)
    # Poignée
    px(img, 21, 17, (216, 200, 72), ox, oy)
    px(img, 21, 18, (200, 184, 56), ox, oy)
    # Encadrement
    fill(img, 6, 1, 6, 31, WOOD4, ox, oy)
    fill(img, 25, 1, 25, 31, WOOD4, ox, oy)
    fill(img, 6, 1, 25, 1, WOOD4, ox, oy)

def draw_window_int(img, idx):
    """Tile 41: Fenêtre intérieure."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, WI1, ox, oy)
    # Plinthe
    fill(img, 0, 26, 31, 31, WOOD2, ox, oy)
    # Cadre
    fill(img, 6, 2, 25, 22, OL, ox, oy)
    fill(img, 7, 3, 24, 21, (88, 152, 216), ox, oy)
    # Croisillons
    fill(img, 15, 3, 16, 21, WI4, ox, oy)
    fill(img, 7, 12, 24, 12, WI4, ox, oy)
    # Reflet
    fill(img, 8, 4, 14, 11, (120, 184, 240), ox, oy)
    px(img, 9, 5, (168, 216, 248), ox, oy)
    # Nuages
    fill(img, 18, 6, 22, 8, (216, 232, 248), ox, oy)
    # Rideaux
    for y in range(4, 10):
        px(img, 7, y, (200, 72, 72), ox, oy)
        px(img, 8, y, (216, 88, 88), ox, oy)
        px(img, 23, y, (216, 88, 88), ox, oy)
        px(img, 24, y, (200, 72, 72), ox, oy)

def draw_dark_wood_floor(img, idx):
    """Tile 42: Sol bois foncé."""
    ox, oy = tile_origin(idx)
    for y in range(0, 32):
        for x in range(0, 32):
            plank = x // 4
            if x % 4 == 0:
                c = WOOD4
            elif (plank + y // 16) % 2 == 0:
                c = WOOD1 if y % 3 != 0 else WOOD2
            else:
                c = WOOD2 if y % 3 != 0 else WOOD3
            px(img, x, y, c, ox, oy, noise=8)

def draw_wall_ext_window(img, idx):
    """Tile 43: Mur extérieur avec fenêtre."""
    ox, oy = tile_origin(idx)
    # Mur briques
    for y in range(0, 32):
        for x in range(0, 32):
            row = y // 4
            offset = (row % 2) * 4
            if y % 4 == 0 or (x + offset) % 8 == 0:
                c = MW3
            else:
                c = MW1 if (x + y) % 7 < 4 else MW2
            px(img, x, y, c, ox, oy, noise=8)
    # Petite fenêtre
    fill(img, 10, 8, 21, 23, OL, ox, oy)
    fill(img, 11, 9, 20, 22, (88, 152, 216), ox, oy)
    fill(img, 15, 9, 16, 22, MW4, ox, oy)
    fill(img, 11, 15, 20, 16, MW4, ox, oy)

def draw_table(img, idx):
    """Tile 44: Table."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Plateau table
    fill(img, 4, 10, 27, 14, WOOD2, ox, oy)
    fill(img, 5, 11, 26, 13, WOOD3, ox, oy)
    fill(img, 4, 10, 27, 10, WOOD4, ox, oy)
    # Pieds
    fill(img, 6, 15, 7, 28, WOOD2, ox, oy)
    fill(img, 24, 15, 25, 28, WOOD2, ox, oy)

def draw_chair(img, idx):
    """Tile 45: Chaise."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Dossier
    fill(img, 10, 4, 21, 16, WOOD2, ox, oy)
    fill(img, 11, 5, 20, 15, WOOD3, ox, oy)
    # Assise
    fill(img, 8, 16, 23, 22, WOOD2, ox, oy)
    fill(img, 9, 17, 22, 21, WOOD3, ox, oy)
    # Pieds
    fill(img, 10, 23, 11, 30, WOOD4, ox, oy)
    fill(img, 20, 23, 21, 30, WOOD4, ox, oy)

def draw_poster(img, idx):
    """Tile 46: Poster."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, WI1, ox, oy)
    # Plinthe
    fill(img, 0, 26, 31, 31, WOOD2, ox, oy)
    # Cadre poster
    fill(img, 6, 4, 25, 22, OL, ox, oy)
    fill(img, 7, 5, 24, 21, (248, 248, 240), ox, oy)
    # Image dans le poster (carte de Kanto stylisée)
    fill(img, 8, 6, 23, 20, (200, 224, 200), ox, oy)
    # Petite île
    fill(img, 12, 10, 18, 14, (88, 184, 80), ox, oy)
    fill(img, 14, 8, 16, 10, (88, 184, 80), ox, oy)
    # Eau
    for y in range(15, 20):
        for x in range(9, 23):
            if not (12 <= x <= 18 and 10 <= y <= 14):
                px(img, x, y, (88, 152, 216), ox, oy)
    # Texte "KANTO"
    fill(img, 10, 18, 22, 19, (80, 80, 80), ox, oy)

def draw_trashcan(img, idx):
    """Tile 47: Poubelle."""
    ox, oy = tile_origin(idx)
    fill(img, 0, 0, 31, 31, FL1, ox, oy)
    # Poubelle cylindrique
    fill(img, 10, 10, 21, 28, (160, 168, 176), ox, oy)
    fill(img, 11, 11, 20, 27, (176, 184, 192), ox, oy)
    # Couvercle
    fill(img, 9, 8, 22, 10, (144, 152, 160), ox, oy)
    fill(img, 10, 8, 21, 9, (160, 168, 176), ox, oy)
    # Poignée couvercle
    fill(img, 14, 6, 17, 8, (128, 136, 144), ox, oy)
    # Bandes
    fill(img, 10, 16, 21, 17, (144, 152, 160), ox, oy)
    fill(img, 10, 22, 21, 23, (144, 152, 160), ox, oy)


# ============================================================================
# ASSEMBLAGE
# ============================================================================

TILE_FUNCS = {
    0: draw_grass,
    1: draw_tall_grass,
    2: draw_path,
    3: draw_sand,
    4: draw_water,
    5: draw_flowers,
    8: lambda img, idx: draw_tree_top(img, idx, "left"),
    9: lambda img, idx: draw_tree_bottom(img, idx, "left"),
    10: lambda img, idx: draw_tree_top(img, idx, "right"),
    11: lambda img, idx: draw_tree_bottom(img, idx, "right"),
    12: draw_fence_h,
    13: draw_fence_v,
    14: draw_bush,
    15: draw_grass_detail,
    16: lambda img, idx: draw_roof(img, idx, "left"),
    17: lambda img, idx: draw_roof(img, idx, "middle"),
    18: lambda img, idx: draw_roof(img, idx, "right"),
    19: lambda img, idx: draw_wall(img, idx, "left"),
    20: lambda img, idx: draw_wall(img, idx, "middle"),
    21: lambda img, idx: draw_wall(img, idx, "right"),
    22: draw_door,
    23: draw_window,
    24: draw_floor_int,
    25: draw_wall_int,
    26: draw_counter,
    27: draw_heal_machine,
    28: draw_shelf,
    29: draw_carpet,
    30: draw_tile_floor,
    31: draw_wall_pattern,
    32: draw_bed_head,
    33: draw_bed_foot,
    34: draw_tv,
    35: draw_pc,
    36: draw_plant,
    37: draw_stairs_up,
    38: draw_stairs_down,
    39: draw_doormat,
    40: draw_door_int,
    41: draw_window_int,
    42: draw_dark_wood_floor,
    43: draw_wall_ext_window,
    44: draw_table,
    45: draw_chair,
    46: draw_poster,
    47: draw_trashcan,
}

def main():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    for idx, func in TILE_FUNCS.items():
        func(img, idx)
    
    # Tiles 6, 7 (non définis) — laisser vides
    # Tiles 48-63 — laisser vides (pour extensions futures)
    
    out = "assets/sprites/tilesets/tileset_outdoor.png"
    img.save(out, "PNG")
    
    # Stats
    total_colors = set()
    for idx in TILE_FUNCS:
        row, col = idx // COLS, idx % COLS
        tile = img.crop((col * TILE, row * TILE, (col + 1) * TILE, (row + 1) * TILE))
        colors = len(set(tile.getdata()))
        total_colors.update(tile.getdata())
        print(f"  Tile {idx:2d}: {colors:3d} couleurs")
    
    print(f"\nTileset sauvegardé: {out}")
    print(f"Couleurs uniques totales: {len(total_colors)}")

if __name__ == "__main__":
    main()
