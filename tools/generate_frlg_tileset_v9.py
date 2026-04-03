#!/usr/bin/env python3
"""
Générateur tileset v9 — Qualité FRLG maximale
Palette GBA fidèle, shading 3 tons, dithering, outlines nets
256×192 px (8×6 grid, 48 tiles de 32×32)
"""

from PIL import Image, ImageDraw
import random, os

random.seed(42)
T = 32  # taille tile
COLS, ROWS = 8, 6
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "tilesets", "tileset_outdoor.png")

img = Image.new("RGBA", (COLS * T, ROWS * T), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# ─── Palette FRLG fidèle ───────────────────────────────────────
# Herbe
G1 = (88, 168, 48)     # herbe base
G2 = (112, 192, 56)    # herbe clair
G3 = (64, 136, 32)     # herbe ombre
G4 = (72, 152, 40)     # herbe moyen

# Herbe haute
HG1 = (56, 144, 40)    # herbe haute base
HG2 = (80, 168, 56)    # herbe haute clair
HG3 = (40, 112, 24)    # herbe haute sombre

# Chemin
P1 = (216, 200, 136)   # chemin base
P2 = (232, 216, 160)   # chemin clair
P3 = (192, 176, 112)   # chemin ombre
P4 = (200, 184, 120)   # chemin moyen

# Sable
S1 = (232, 216, 168)
S2 = (248, 232, 184)
S3 = (208, 192, 144)

# Eau
W1 = (56, 104, 200)    # eau base
W2 = (80, 136, 224)    # eau clair/reflet
W3 = (40, 80, 160)     # eau sombre
W4 = (64, 112, 208)    # eau moyen

# Fleurs
FL1 = (232, 64, 64)    # pétale rouge
FL2 = (248, 168, 56)   # pétale jaune
FL3 = (240, 240, 240)  # pétale blanc

# Arbre canopée
TC1 = (48, 128, 48)    # canopée base
TC2 = (72, 160, 56)    # canopée clair
TC3 = (32, 96, 32)     # canopée ombre
TC4 = (40, 112, 40)    # canopée moyen-ombre

# Arbre tronc
TK1 = (136, 104, 56)   # tronc base
TK2 = (168, 128, 72)   # tronc clair
TK3 = (104, 80, 40)    # tronc ombre

# Clôture
FN1 = (200, 176, 128)
FN2 = (224, 200, 152)
FN3 = (168, 144, 96)

# Buisson
BU1 = (56, 136, 48)
BU2 = (80, 160, 64)
BU3 = (40, 104, 32)

# Toit rouge
R1 = (216, 64, 40)     # toit base
R2 = (240, 96, 64)     # toit clair (bord haut)
R3 = (176, 48, 32)     # toit ombre
R4 = (152, 40, 24)     # toit ombre profonde

# Mur extérieur
MW1 = (240, 232, 200)  # mur crème base
MW2 = (248, 244, 224)  # mur clair
MW3 = (216, 208, 176)  # mur ombre
MW4 = (200, 192, 160)  # mur ombre profonde

# Porte
D1 = (136, 88, 48)     # porte bois base
D2 = (168, 112, 64)    # porte bois clair
D3 = (104, 64, 32)     # porte bois sombre

# Fenêtre
WI1 = (160, 208, 248)  # verre clair
WI2 = (120, 168, 224)  # verre base
WI3 = (88, 136, 200)   # verre sombre
WIF = (200, 192, 160)  # cadre

# Intérieurs
PQ1 = (200, 168, 112)  # parquet base
PQ2 = (224, 192, 136)  # parquet clair
PQ3 = (168, 136, 88)   # parquet ombre

MI1 = (232, 224, 208)  # mur intérieur base
MI2 = (248, 240, 224)  # mur intérieur clair
MI3 = (208, 200, 184)  # mur intérieur ombre

CT1 = (88, 120, 176)   # comptoir base
CT2 = (112, 144, 200)  # comptoir clair
CT3 = (64, 96, 144)    # comptoir ombre

MH1 = (240, 160, 176)  # machine soin rose
MH2 = (248, 192, 200)  # machine soin clair
MH3 = (216, 128, 152)  # machine soin sombre

SH1 = (160, 120, 72)   # étagère base
SH2 = (192, 152, 96)   # étagère clair
SH3 = (128, 88, 48)    # étagère ombre

TP1 = (200, 56, 48)    # tapis rouge
TP2 = (224, 80, 64)    # tapis clair
TP3 = (168, 40, 32)    # tapis sombre

CL1 = (200, 200, 208)  # carrelage
CL2 = (224, 224, 232)  # carrelage clair
CL3 = (176, 176, 184)  # carrelage ombre

BK = (16, 16, 24)      # noir outline
WT = (248, 248, 248)   # blanc pur
GY = (168, 168, 176)   # gris moyen

TRANS = (0, 0, 0, 0)

# ─── Helpers ─────────────────────────────────────────────────────
def px(x, y, col):
    """Pixel unique sur le tileset"""
    if len(col) == 3:
        col = col + (255,)
    img.putpixel((x, y), col)

def tile_origin(idx):
    """Retourne le coin supérieur gauche d'un tile par son index"""
    return (idx % COLS) * T, (idx // COLS) * T

def fill_tile(idx, col):
    """Remplit un tile entier d'une couleur"""
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            px(ox + x, oy + y, col)

def rect(ox, oy, x1, y1, x2, y2, col):
    """Rectangle rempli relatif à l'origine du tile"""
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            px(ox + x, oy + y, col)

def dither_2(ox, oy, x1, y1, x2, y2, c1, c2, pattern="checker"):
    """Remplissage dithering 2 couleurs"""
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if pattern == "checker":
                col = c1 if (x + y) % 2 == 0 else c2
            elif pattern == "h_stripe":
                col = c1 if y % 2 == 0 else c2
            else:
                col = c1 if random.random() < 0.5 else c2
            px(ox + x, oy + y, col)

def noise_fill(ox, oy, x1, y1, x2, y2, base, variants, probs=None):
    """Remplissage avec bruit : base + variants aléatoires"""
    if probs is None:
        probs = [1.0 / len(variants)] * len(variants)
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            r = random.random()
            cum = 0
            chosen = base
            for i, (v, p) in enumerate(zip(variants, probs)):
                cum += p
                if r < cum:
                    chosen = v
                    break
            else:
                chosen = base
            px(ox + x, oy + y, chosen)

# ═══════════════════════════════════════════════════════════════════
# TILE 0 — Herbe (style FRLG : motif de petites touffes)
# ═══════════════════════════════════════════════════════════════════
def draw_grass(idx):
    ox, oy = tile_origin(idx)
    # Remplir base verte avec variation subtile
    for y in range(T):
        for x in range(T):
            # Pattern diagonale subtile comme FRLG
            if (x + y * 3) % 7 == 0:
                px(ox + x, oy + y, G2)
            elif (x * 2 + y) % 11 == 0:
                px(ox + x, oy + y, G3)
            elif (x + y) % 5 == 0:
                px(ox + x, oy + y, G4)
            else:
                px(ox + x, oy + y, G1)
    # Petites touffes d'herbe (3 pixels en V) dispersées
    tufts = [(4,6), (12,3), (20,8), (28,4), (8,14), (16,12), (24,16),
             (6,22), (14,20), (22,24), (30,22), (10,28), (18,26), (26,30),
             (3,18), (19,2), (27,14)]
    for tx, ty in tufts:
        if tx < T and ty < T:
            px(ox + tx, oy + ty, G3)
            if tx > 0 and ty > 0:
                px(ox + tx - 1, oy + ty - 1, G2)
            if tx < T-1 and ty > 0:
                px(ox + tx + 1, oy + ty - 1, G2)

draw_grass(0)

# ═══════════════════════════════════════════════════════════════════
# TILE 1 — Herbe haute (plus sombre, motif dense)
# ═══════════════════════════════════════════════════════════════════
def draw_tall_grass(idx):
    ox, oy = tile_origin(idx)
    # Base plus sombre
    for y in range(T):
        for x in range(T):
            if (x + y) % 3 == 0:
                px(ox + x, oy + y, HG2)
            elif (x * 3 + y * 2) % 7 == 0:
                px(ox + x, oy + y, HG3)
            else:
                px(ox + x, oy + y, HG1)
    # Brins d'herbe verticaux denses
    for bx in range(1, T - 1, 3):
        for by in range(0, T, 6):
            h = random.randint(3, 5)
            for dy in range(h):
                if by + dy < T:
                    px(ox + bx, oy + by + dy, HG3)
                    if bx + 1 < T:
                        px(ox + bx + 1, oy + by + dy, HG2 if dy < 2 else HG1)

draw_tall_grass(1)

# ═══════════════════════════════════════════════════════════════════
# TILE 2 — Chemin (sable/terre battue, style FRLG)
# ═══════════════════════════════════════════════════════════════════
def draw_path(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            if (x * 5 + y * 3) % 13 == 0:
                px(ox + x, oy + y, P2)
            elif (x + y * 7) % 17 == 0:
                px(ox + x, oy + y, P3)
            elif (x * 2 + y) % 9 == 0:
                px(ox + x, oy + y, P4)
            else:
                px(ox + x, oy + y, P1)
    # Quelques petits cailloux
    for _ in range(6):
        cx, cy = random.randint(2, T-3), random.randint(2, T-3)
        px(ox + cx, oy + cy, P3)

draw_path(2)

# ═══════════════════════════════════════════════════════════════════
# TILE 3 — Sable
# ═══════════════════════════════════════════════════════════════════
def draw_sand(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            if (x + y * 2) % 7 == 0:
                px(ox + x, oy + y, S2)
            elif (x * 3 + y) % 11 == 0:
                px(ox + x, oy + y, S3)
            else:
                px(ox + x, oy + y, S1)

draw_sand(3)

# ═══════════════════════════════════════════════════════════════════
# TILE 4 — Eau (style FRLG : bleu profond avec ondulations)
# ═══════════════════════════════════════════════════════════════════
def draw_water(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            # Ondulations horizontales avec décalage
            wave = (x + y // 4 * 3) % 8
            if wave < 2:
                px(ox + x, oy + y, W2)
            elif wave < 5:
                px(ox + x, oy + y, W1)
            elif wave < 7:
                px(ox + x, oy + y, W4)
            else:
                px(ox + x, oy + y, W3)
    # Reflets blancs épars
    for _ in range(5):
        rx, ry = random.randint(3, T-4), random.randint(3, T-4)
        px(ox + rx, oy + ry, (200, 216, 248))

draw_water(4)

# ═══════════════════════════════════════════════════════════════════
# TILE 5 — Fleurs (herbe avec fleurs colorées)
# ═══════════════════════════════════════════════════════════════════
def draw_flowers(idx):
    ox, oy = tile_origin(idx)
    # Base herbe
    for y in range(T):
        for x in range(T):
            px(ox + x, oy + y, G1 if (x + y) % 3 != 0 else G2)
    # Fleurs dispersées
    flowers = [(4,4,FL1), (12,8,FL2), (20,4,FL3), (28,10,FL1),
               (8,16,FL2), (16,20,FL1), (24,24,FL3), (6,28,FL2),
               (14,14,FL3), (22,18,FL1), (30,26,FL2), (10,6,FL1)]
    for fx, fy, fc in flowers:
        if fx < T and fy < T:
            px(ox + fx, oy + fy, fc)
            # Pétales autour
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = fx + dx, fy + dy
                if 0 <= nx < T and 0 <= ny < T:
                    px(ox + nx, oy + ny, fc)
            # Centre jaune
            px(ox + fx, oy + fy, (248, 224, 64))

draw_flowers(5)

# ═══════════════════════════════════════════════════════════════════
# TILE 6 — Herbe avec cailloux
# ═══════════════════════════════════════════════════════════════════
def draw_grass_rocks(idx):
    ox, oy = tile_origin(idx)
    draw_grass(idx)  # Base herbe
    # Petits cailloux gris
    rocks = [(6,10), (14,6), (22,14), (10,22), (18,28), (26,8), (4,18)]
    for rx, ry in rocks:
        px(ox + rx, oy + ry, GY)
        px(ox + rx + 1, oy + ry, (184, 184, 192))
        px(ox + rx, oy + ry + 1, (144, 144, 152))

draw_grass_rocks(6)

# ═══════════════════════════════════════════════════════════════════
# TILE 7 — Transition herbe/chemin
# ═══════════════════════════════════════════════════════════════════
def draw_transition(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            if y < T // 2 - 2:
                px(ox + x, oy + y, G1 if (x + y) % 3 != 0 else G2)
            elif y > T // 2 + 2:
                px(ox + x, oy + y, P1 if (x + y) % 5 != 0 else P2)
            else:
                # Zone de transition
                if (x + y) % 2 == 0:
                    px(ox + x, oy + y, G4)
                else:
                    px(ox + x, oy + y, P4)

draw_transition(7)

# ═══════════════════════════════════════════════════════════════════
# TILES 8-11 — Arbre 2×2 (canopée ronde FRLG)
# ═══════════════════════════════════════════════════════════════════
def draw_tree():
    """Dessine un arbre 2×2 (tiles 8=HG, 9=BG, 10=HD, 11=BD)"""
    # Travailler sur un canvas 64×64 puis découper
    tree = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    
    # Définir la canopée comme un grand cercle/ovale
    cx, cy = 32, 24  # centre de la canopée
    rx, ry = 28, 22  # rayons
    
    for y in range(64):
        for x in range(64):
            # Distance normalisée au centre de la canopée
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            dist = dx * dx + dy * dy
            
            if dist <= 1.0:
                # Dans la canopée
                # Gradient d'éclairage (lumière haut-gauche)
                light = 1.0 - dist * 0.4 - dx * 0.15 - dy * 0.15
                
                # Variation avec bruit
                noise = random.random() * 0.15
                val = light + noise
                
                if val > 0.85:
                    tree.putpixel((x, y), TC2 + (255,))
                elif val > 0.65:
                    tree.putpixel((x, y), TC1 + (255,))
                elif val > 0.45:
                    tree.putpixel((x, y), TC4 + (255,))
                else:
                    tree.putpixel((x, y), TC3 + (255,))
                
                # Outline pour le bord de la canopée
                if dist > 0.85:
                    tree.putpixel((x, y), TC3 + (255,))
            
            # Tronc (en bas au centre)
            elif 28 <= x <= 35 and 40 <= y <= 63:
                ty = (y - 40) / 23.0
                if x <= 30:
                    tree.putpixel((x, y), TK3 + (255,))
                elif x >= 34:
                    tree.putpixel((x, y), TK3 + (255,))
                elif ty < 0.3:
                    tree.putpixel((x, y), TK2 + (255,))
                else:
                    tree.putpixel((x, y), TK1 + (255,))
    
    # Ajouter quelques highlights lumineux sur la canopée
    highlights = [(18,14), (22,10), (26,12), (20,18), (24,16)]
    for hx, hy in highlights:
        if 0 <= hx < 64 and 0 <= hy < 64:
            tree.putpixel((hx, hy), (96, 184, 72, 255))
    
    # Découper en 4 tiles de 32×32
    for i, (sx, sy) in enumerate([(0,0), (0,32), (32,0), (32,32)]):
        tile_idx = 8 + i
        tox, toy = tile_origin(tile_idx)
        crop = tree.crop((sx, sy, sx + 32, sy + 32))
        img.paste(crop, (tox, toy))

draw_tree()

# ═══════════════════════════════════════════════════════════════════
# TILE 12 — Clôture horizontale
# ═══════════════════════════════════════════════════════════════════
def draw_fence_h(idx):
    ox, oy = tile_origin(idx)
    # Herbe en fond
    for y in range(T):
        for x in range(T):
            px(ox + x, oy + y, G1)
    # Poteaux
    for post_x in [4, 28]:
        rect(ox, oy, post_x, 8, post_x + 3, 24, FN1)
        rect(ox, oy, post_x, 8, post_x + 3, 9, FN2)  # highlight haut
        rect(ox, oy, post_x + 3, 8, post_x + 3, 24, FN3)  # ombre droite
    # Traverses
    rect(ox, oy, 4, 12, 31, 13, FN1)
    rect(ox, oy, 4, 12, 31, 12, FN2)
    rect(ox, oy, 4, 18, 31, 19, FN1)
    rect(ox, oy, 4, 18, 31, 18, FN2)

draw_fence_h(12)

# ═══════════════════════════════════════════════════════════════════
# TILE 13 — Clôture verticale
# ═══════════════════════════════════════════════════════════════════
def draw_fence_v(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            px(ox + x, oy + y, G1)
    # Poteau vertical
    rect(ox, oy, 13, 0, 18, 31, FN1)
    rect(ox, oy, 13, 0, 14, 31, FN2)
    rect(ox, oy, 17, 0, 18, 31, FN3)
    # Traverses latérales (en haut et bas du tile)
    for ty in [4, 28]:
        rect(ox, oy, 6, ty, 25, ty + 1, FN1)
        rect(ox, oy, 6, ty, 25, ty, FN2)

draw_fence_v(13)

# ═══════════════════════════════════════════════════════════════════
# TILE 14 — Buisson
# ═══════════════════════════════════════════════════════════════════
def draw_bush(idx):
    ox, oy = tile_origin(idx)
    # Herbe en fond
    for y in range(T):
        for x in range(T):
            px(ox + x, oy + y, G1)
    # Buisson arrondi
    cx, cy = 16, 18
    for y in range(4, 30):
        for x in range(3, 29):
            dx = (x - cx) / 13.0
            dy = (y - cy) / 12.0
            dist = dx*dx + dy*dy
            if dist <= 1.0:
                light = 1.0 - dist * 0.3 - dx * 0.2 - dy * 0.2
                noise = random.random() * 0.1
                val = light + noise
                if val > 0.75:
                    px(ox + x, oy + y, BU2)
                elif val > 0.5:
                    px(ox + x, oy + y, BU1)
                else:
                    px(ox + x, oy + y, BU3)

draw_bush(14)

# ═══════════════════════════════════════════════════════════════════
# TILE 15 — Herbe détail (variante)
# ═══════════════════════════════════════════════════════════════════
def draw_grass_detail(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            if (x * 3 + y * 5) % 11 == 0:
                px(ox + x, oy + y, G2)
            elif (x + y * 2) % 7 == 0:
                px(ox + x, oy + y, G3)
            else:
                px(ox + x, oy + y, G1)

draw_grass_detail(15)

# ═══════════════════════════════════════════════════════════════════
# TILES 16-18 — Toit (gauche, milieu, droite)
# Style FRLG : rouge tuile avec motif de rangées
# ═══════════════════════════════════════════════════════════════════
def draw_roof(idx, part):
    """part: 'left', 'mid', 'right'"""
    ox, oy = tile_origin(idx)
    
    for y in range(T):
        for x in range(T):
            # Rangées de tuiles alternées
            row = y // 4
            offset = (row % 2) * 4
            tile_x = (x + offset) % 8
            
            # Couleur basée sur la position dans la "tuile"
            if y % 4 == 0:
                # Ligne du haut de la tuile = ombre
                c = R3
            elif tile_x <= 1:
                # Bord gauche de la tuile = plus sombre
                c = R3
            elif y % 4 == 3:
                # Bas de la tuile = highlight
                c = R2
            else:
                c = R1
            
            # Effets de bord de toit
            if part == 'left' and x <= 1:
                c = R4
            elif part == 'right' and x >= T - 2:
                c = R4
            
            # Ligne tout en haut = faîtage
            if y <= 1:
                c = R4
            # Ligne tout en bas = bord de toit avec ombre
            if y >= T - 2:
                c = R3
            
            px(ox + x, oy + y, c)
    
    # Ombre portée en bas
    for x in range(T):
        px(ox + x, oy + T - 1, R4)

draw_roof(16, 'left')
draw_roof(17, 'mid')
draw_roof(18, 'right')

# ═══════════════════════════════════════════════════════════════════
# TILES 19-21 — Mur extérieur (gauche, milieu, droite)
# Style FRLG : crème avec texture briques subtile
# ═══════════════════════════════════════════════════════════════════
def draw_wall(idx, part):
    """part: 'left', 'mid', 'right'"""
    ox, oy = tile_origin(idx)
    
    for y in range(T):
        for x in range(T):
            # Motif briques subtil
            row = y // 4
            offset = (row % 2) * 8
            brick_x = (x + offset) % 16
            
            # Jointures de briques (très subtiles)
            if y % 4 == 0:
                c = MW3
            elif brick_x == 0:
                c = MW3
            elif y % 4 == 1 and (brick_x <= 2 or brick_x >= 14):
                c = MW3
            else:
                c = MW1
            
            # Highlight au centre
            if 8 <= y <= 24 and 8 <= x <= 24:
                if c == MW1:
                    c = MW2
            
            # Bordures
            if part == 'left' and x <= 1:
                c = MW4
            elif part == 'right' and x >= T - 2:
                c = MW4
            
            # Base en bas (fondation)
            if y >= T - 3:
                c = MW4
            
            px(ox + x, oy + y, c)

draw_wall(19, 'left')
draw_wall(20, 'mid')
draw_wall(21, 'right')

# ═══════════════════════════════════════════════════════════════════
# TILE 22 — Porte (bois avec poignée)
# ═══════════════════════════════════════════════════════════════════
def draw_door(idx):
    ox, oy = tile_origin(idx)
    # Fond mur
    for y in range(T):
        for x in range(T):
            px(ox + x, oy + y, MW1)
    # Cadre de porte
    rect(ox, oy, 4, 2, 27, 31, D1)
    # Panneau intérieur (plus clair)
    rect(ox, oy, 6, 4, 25, 29, D2)
    # Rainure centrale
    rect(ox, oy, 15, 4, 16, 29, D1)
    # Panneaux decoratifs
    rect(ox, oy, 7, 5, 14, 14, D1)
    rect(ox, oy, 8, 6, 13, 13, D2)
    rect(ox, oy, 17, 5, 24, 14, D1)
    rect(ox, oy, 18, 6, 23, 13, D2)
    rect(ox, oy, 7, 17, 14, 28, D1)
    rect(ox, oy, 8, 18, 13, 27, D2)
    rect(ox, oy, 17, 17, 24, 28, D1)
    rect(ox, oy, 18, 18, 23, 27, D2)
    # Poignée
    px(ox + 22, oy + 18, (200, 200, 64))
    px(ox + 22, oy + 19, (184, 184, 48))
    # Ombre gauche du cadre
    for y in range(2, 32):
        px(ox + 4, oy + y, D3)
    # Seuil
    rect(ox, oy, 4, 30, 27, 31, MW4)
    # Fondation
    for y in range(T - 3, T):
        for x in range(T):
            if x < 4 or x > 27:
                px(ox + x, oy + y, MW4)

draw_door(22)

# ═══════════════════════════════════════════════════════════════════
# TILE 23 — Fenêtre extérieure
# ═══════════════════════════════════════════════════════════════════
def draw_window_ext(idx):
    ox, oy = tile_origin(idx)
    # Fond mur briques
    for y in range(T):
        for x in range(T):
            row = y // 4
            offset = (row % 2) * 8
            brick_x = (x + offset) % 16
            if y % 4 == 0 or brick_x == 0:
                px(ox + x, oy + y, MW3)
            else:
                px(ox + x, oy + y, MW1)
    # Fondation bas
    for y in range(T - 3, T):
        for x in range(T):
            px(ox + x, oy + y, MW4)
    # Cadre de fenêtre
    rect(ox, oy, 6, 4, 25, 23, WIF)
    # Verre
    rect(ox, oy, 8, 6, 23, 21, WI2)
    # Reflet (diagonale claire)
    for i in range(8):
        wx = 9 + i
        wy = 7 + i
        if wx <= 23 and wy <= 21:
            px(ox + wx, oy + wy, WI1)
            if wx + 1 <= 23:
                px(ox + wx + 1, oy + wy, WI1)
    # Croisillon
    rect(ox, oy, 15, 6, 16, 21, WIF)
    rect(ox, oy, 8, 13, 23, 14, WIF)
    # Ombre sombre au bord bas
    rect(ox, oy, 8, 20, 23, 21, WI3)
    # Rebord
    rect(ox, oy, 5, 24, 26, 25, MW3)

draw_window_ext(23)

# ═══════════════════════════════════════════════════════════════════
# TILES 24-31 — Intérieurs
# ═══════════════════════════════════════════════════════════════════
def draw_floor_parquet(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            # Lames de parquet
            plank = x // 8
            offset = (plank % 2) * 4
            py = (y + offset) % 8
            if py == 0:
                px(ox + x, oy + y, PQ3)
            elif x % 8 == 0:
                px(ox + x, oy + y, PQ3)
            elif py <= 2:
                px(ox + x, oy + y, PQ2)
            else:
                px(ox + x, oy + y, PQ1)

draw_floor_parquet(24)

def draw_wall_int(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            if y <= 1:
                px(ox + x, oy + y, MI3)
            elif y >= T - 2:
                px(ox + x, oy + y, MI3)
            elif y <= 4:
                px(ox + x, oy + y, MI2)
            else:
                px(ox + x, oy + y, MI1)
    # Plinthe en bas
    rect(ox, oy, 0, T-4, T-1, T-2, (184, 152, 104))
    rect(ox, oy, 0, T-1, T-1, T-1, (160, 128, 80))

draw_wall_int(25)

def draw_counter(idx):
    ox, oy = tile_origin(idx)
    # Sol
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Comptoir
    rect(ox, oy, 0, 4, T-1, T-1, CT1)
    rect(ox, oy, 0, 4, T-1, 6, CT2)  # highlight haut
    rect(ox, oy, 0, T-2, T-1, T-1, CT3)  # ombre bas
    # Ligne décorative
    rect(ox, oy, 0, 14, T-1, 15, CT2)

draw_counter(26)

def draw_healing_machine(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, CL1)
    # Machine
    rect(ox, oy, 4, 8, 27, 28, MH1)
    rect(ox, oy, 4, 8, 27, 10, MH2)
    rect(ox, oy, 4, 26, 27, 28, MH3)
    # Fente de ball
    rect(ox, oy, 10, 14, 21, 22, (240, 240, 248))
    # Croix rouge au centre
    rect(ox, oy, 14, 16, 17, 20, (232, 56, 48))
    rect(ox, oy, 12, 17, 19, 19, (232, 56, 48))
    # Indicateur LED
    px(ox + 8, oy + 12, (64, 232, 64))

draw_healing_machine(27)

def draw_shelf(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, MI1)
    # Étagère
    rect(ox, oy, 2, 2, T-3, T-1, SH1)
    rect(ox, oy, 2, 2, T-3, 3, SH2)
    # Planches
    for sy in [10, 18, 26]:
        rect(ox, oy, 2, sy, T-3, sy+1, SH2)
        rect(ox, oy, 2, sy+1, T-3, sy+1, SH3)
    # Livres colorés sur les étagères
    book_colors = [(200,56,48), (48,96,200), (56,168,56), (200,168,48)]
    for sy_base, col in zip([4, 12, 20], book_colors[:3]):
        for bx in range(4, T-4, 5):
            bc = book_colors[random.randint(0, 3)]
            rect(ox, oy, bx, sy_base, bx+3, sy_base+5, bc)

draw_shelf(28)

def draw_carpet(idx):
    ox, oy = tile_origin(idx)
    # Sol de base
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Tapis avec bordure
    rect(ox, oy, 2, 2, T-3, T-3, TP1)
    rect(ox, oy, 3, 3, T-4, T-4, TP2)
    rect(ox, oy, 4, 4, T-5, T-5, TP1)
    # Motif central
    rect(ox, oy, 10, 10, 21, 21, TP3)
    rect(ox, oy, 12, 12, 19, 19, TP1)

draw_carpet(29)

def draw_tiled_floor(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            if x % 8 == 0 or y % 8 == 0:
                px(ox + x, oy + y, CL3)
            elif (x // 8 + y // 8) % 2 == 0:
                px(ox + x, oy + y, CL1)
            else:
                px(ox + x, oy + y, CL2)

draw_tiled_floor(30)

def draw_wall_pattern(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            if y <= 1 or y >= T-2:
                px(ox + x, oy + y, MI3)
            elif (x + y) % 8 < 4:
                px(ox + x, oy + y, MI1)
            else:
                px(ox + x, oy + y, MI2)

draw_wall_pattern(31)

# ═══════════════════════════════════════════════════════════════════
# TILES 32-39 — Mobilier chambre/escaliers
# ═══════════════════════════════════════════════════════════════════
def draw_bed_head(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Tête de lit
    rect(ox, oy, 2, 4, T-3, T-1, (160, 120, 72))
    rect(ox, oy, 4, 6, T-5, T-1, (232, 232, 240))  # draps blancs
    # Oreiller
    rect(ox, oy, 6, 8, T-7, 16, WT)
    rect(ox, oy, 7, 9, T-8, 15, (240, 240, 248))
    # Couverture bleue
    rect(ox, oy, 4, 18, T-5, T-1, (96, 136, 208))
    rect(ox, oy, 4, 18, T-5, 19, (120, 160, 224))

draw_bed_head(32)

def draw_bed_foot(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Pied de lit
    rect(ox, oy, 2, 0, T-3, 24, (160, 120, 72))
    # Couverture
    rect(ox, oy, 4, 0, T-5, 20, (96, 136, 208))
    rect(ox, oy, 4, 0, T-5, 2, (120, 160, 224))
    # Pied
    rect(ox, oy, 2, 22, T-3, 24, (136, 96, 56))

draw_bed_foot(33)

def draw_tv(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Meuble TV
    rect(ox, oy, 4, 16, T-5, T-1, (168, 136, 88))
    # TV
    rect(ox, oy, 6, 4, T-7, 20, (48, 48, 56))
    rect(ox, oy, 8, 6, T-9, 18, (72, 72, 88))
    # Reflet écran
    rect(ox, oy, 9, 7, 14, 10, (96, 96, 112))
    # Boutons
    px(ox + T-9, oy + 14, (232, 56, 48))
    px(ox + T-9, oy + 16, (64, 232, 64))

draw_tv(34)

def draw_pc(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Bureau
    rect(ox, oy, 2, 18, T-3, T-1, (168, 136, 88))
    # Écran
    rect(ox, oy, 8, 2, T-9, 16, (56, 56, 64))
    rect(ox, oy, 10, 4, T-11, 14, (80, 120, 200))
    # Pied écran
    rect(ox, oy, 14, 16, 17, 18, (96, 96, 104))
    # Clavier
    rect(ox, oy, 8, 20, T-9, 22, (200, 200, 208))
    # Souris
    rect(ox, oy, T-8, 20, T-5, 22, (200, 200, 208))

draw_pc(35)

def draw_plant(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Pot
    rect(ox, oy, 10, 22, 21, 30, (184, 120, 72))
    rect(ox, oy, 8, 20, 23, 22, (200, 136, 88))
    # Plante
    cx, cy = 16, 14
    for y in range(4, 22):
        for x in range(6, 26):
            dx = (x - cx) / 10.0
            dy = (y - cy) / 10.0
            if dx*dx + dy*dy <= 1.0:
                if random.random() < 0.3:
                    px(ox + x, oy + y, (96, 184, 64))
                elif random.random() < 0.5:
                    px(ox + x, oy + y, (56, 144, 40))
                else:
                    px(ox + x, oy + y, (72, 160, 48))

draw_plant(36)

def draw_stairs_up(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        step = y // 4
        shade = 200 - step * 15
        for x in range(T):
            px(ox + x, oy + y, (shade, shade - 20, shade - 60))
        # Highlight en haut de chaque marche
        if y % 4 == 0:
            for x in range(T):
                px(ox + x, oy + y, (shade + 20, shade, shade - 40))

draw_stairs_up(37)

def draw_stairs_down(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        step = (T - 1 - y) // 4
        shade = 200 - step * 15
        for x in range(T):
            px(ox + x, oy + y, (shade, shade - 20, shade - 60))
        if y % 4 == 3:
            for x in range(T):
                px(ox + x, oy + y, (max(60, shade - 30), max(40, shade - 50), max(20, shade - 90)))

draw_stairs_down(38)

def draw_doormat(idx):
    ox, oy = tile_origin(idx)
    # Sol
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Paillasson
    rect(ox, oy, 4, 10, T-5, 22, (168, 136, 72))
    rect(ox, oy, 5, 11, T-6, 21, (184, 152, 88))
    # Texture
    for y in range(12, 21, 2):
        for x in range(6, T-6, 2):
            px(ox + x, oy + y, (168, 136, 72))

draw_doormat(39)

# ═══════════════════════════════════════════════════════════════════
# TILES 40-47 — Intérieur avancé
# ═══════════════════════════════════════════════════════════════════
def draw_door_int(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, MI1)
    # Porte
    rect(ox, oy, 6, 2, 25, T-1, D1)
    rect(ox, oy, 8, 4, 23, T-1, D2)
    # Panneau
    rect(ox, oy, 10, 6, 21, 16, D1)
    rect(ox, oy, 10, 20, 21, 28, D1)
    # Poignée
    px(ox + 20, oy + 18, (200, 200, 64))
    px(ox + 20, oy + 19, (184, 184, 48))

draw_door_int(40)

def draw_window_int(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, MI1)
    # Cadre
    rect(ox, oy, 4, 4, 27, 24, WIF)
    # Verre
    rect(ox, oy, 6, 6, 25, 22, WI2)
    # Reflet
    for i in range(6):
        px(ox + 7 + i, oy + 7 + i, WI1)
        px(ox + 8 + i, oy + 7 + i, WI1)
    # Croisillon
    rect(ox, oy, 15, 6, 16, 22, WIF)
    rect(ox, oy, 6, 13, 25, 14, WIF)
    # Rideaux
    for y in range(4, 25):
        px(ox + 4, oy + y, (232, 216, 184))
        px(ox + 5, oy + y, (240, 224, 192))
        px(ox + 26, oy + y, (240, 224, 192))
        px(ox + 27, oy + y, (232, 216, 184))

draw_window_int(41)

def draw_dark_wood(idx):
    ox, oy = tile_origin(idx)
    for y in range(T):
        for x in range(T):
            plank = x // 6
            offset = (plank % 2) * 3
            py = (y + offset) % 6
            if py == 0 or x % 6 == 0:
                px(ox + x, oy + y, (120, 88, 48))
            elif py <= 2:
                px(ox + x, oy + y, (160, 128, 80))
            else:
                px(ox + x, oy + y, (144, 112, 64))

draw_dark_wood(42)

def draw_wall_ext_window(idx):
    """Mur extérieur avec fenêtre intégrée"""
    draw_window_ext(idx)

draw_wall_ext_window(43)

def draw_table(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Table
    rect(ox, oy, 4, 8, T-5, 20, (176, 144, 96))
    rect(ox, oy, 4, 8, T-5, 10, (192, 160, 112))  # highlight
    # Pieds
    rect(ox, oy, 5, 20, 7, T-3, (144, 112, 72))
    rect(ox, oy, T-8, 20, T-6, T-3, (144, 112, 72))

draw_table(44)

def draw_chair(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Chaise vue de face
    # Dossier
    rect(ox, oy, 8, 4, 23, 8, (176, 144, 96))
    rect(ox, oy, 9, 5, 22, 7, (192, 160, 112))
    # Siège
    rect(ox, oy, 8, 16, 23, 20, (176, 144, 96))
    rect(ox, oy, 8, 16, 23, 17, (192, 160, 112))
    # Pieds
    rect(ox, oy, 9, 8, 10, 16, (144, 112, 72))
    rect(ox, oy, 21, 8, 22, 16, (144, 112, 72))
    rect(ox, oy, 9, 20, 10, T-4, (144, 112, 72))
    rect(ox, oy, 21, 20, 22, T-4, (144, 112, 72))

draw_chair(45)

def draw_poster(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, MI1)
    # Poster
    rect(ox, oy, 6, 4, 25, 26, BK)
    rect(ox, oy, 7, 5, 24, 25, (232, 224, 200))
    # Dessin sur le poster (Pokémon stylisé)
    # Cercle rouge (Pokéball)
    cx, cy = 16, 14
    for y in range(8, 22):
        for x in range(10, 22):
            dx = (x - cx) / 6.0
            dy = (y - cy) / 7.0
            if dx*dx + dy*dy <= 1.0:
                if y < 14:
                    px(ox + x, oy + y, (224, 64, 48))
                elif y == 14:
                    px(ox + x, oy + y, BK)
                else:
                    px(ox + x, oy + y, WT)
    # Bouton central
    px(ox + 16, oy + 14, WT)
    px(ox + 15, oy + 14, WT)

draw_poster(46)

def draw_trashcan(idx):
    ox, oy = tile_origin(idx)
    rect(ox, oy, 0, 0, T-1, T-1, PQ1)
    # Poubelle
    rect(ox, oy, 10, 10, 21, 28, GY)
    rect(ox, oy, 10, 10, 21, 12, (184, 184, 192))  # rebord
    rect(ox, oy, 10, 26, 21, 28, (144, 144, 152))  # ombre
    # Couvercle
    rect(ox, oy, 8, 8, 23, 10, (184, 184, 192))
    # Poignée
    rect(ox, oy, 14, 6, 17, 8, (168, 168, 176))

draw_trashcan(47)

# ═══════════════════════════════════════════════════════════════════
# Sauvegarde
# ═══════════════════════════════════════════════════════════════════
os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, "PNG")

# Stats
total_opaque = 0
for y in range(img.height):
    for x in range(img.width):
        if img.getpixel((x, y))[3] > 0:
            total_opaque += 1

print(f"✓ Tileset v9 sauvegardé : {OUT}")
print(f"  {img.width}×{img.height} px — {COLS * ROWS} tiles de {T}×{T}")
print(f"  Style FRLG : palette GBA fidèle, shading 3 tons, dithering, tuiles détaillées")

# Détail par tile
tile_names = [
    "herbe", "herbe_haute", "chemin", "sable", "eau", "fleurs", "herbe_cailloux", "transition",
    "arbre_hg", "arbre_bg", "arbre_hd", "arbre_bd", "cloture_h", "cloture_v", "buisson", "herbe_detail",
    "toit_g", "toit_m", "toit_d", "mur_g", "mur_m", "mur_d", "porte", "fenetre_ext",
    "parquet", "mur_int", "comptoir", "machine_soin", "etagere", "tapis", "carrelage", "mur_motif",
    "lit_tete", "lit_pied", "tv", "pc", "plante", "escalier_up", "escalier_down", "paillasson",
    "porte_int", "fenetre_int", "sol_bois_fonce", "mur_ext_fenetre", "table", "chaise", "poster", "poubelle"
]
for i, name in enumerate(tile_names):
    tox, toy = tile_origin(i)
    opaque = 0
    colors = set()
    for y in range(T):
        for x in range(T):
            p = img.getpixel((tox + x, toy + y))
            if p[3] > 0:
                opaque += 1
                colors.add(p[:3])
    print(f"  [{i:2d}] {name:24s}: {opaque:4d} px opaques, {len(colors):2d} couleurs")
