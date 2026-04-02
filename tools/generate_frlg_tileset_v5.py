#!/usr/bin/env python3
"""
Générateur de tileset FRLG HD — v5 Pixel Art Qualité.
Produit 8×6 = 48 tiles 32×32px avec vrai pixel art détaillé.
Style inspiré des RPG GBA (FireRed/LeafGreen).
"""

from PIL import Image, ImageDraw
import os, random

random.seed(42)

TILE = 32
COLS = 8
ROWS = 6
OUT = "assets/sprites/tilesets/tileset_outdoor.png"

# ══════════════════════════════════════════════════════════════
# PALETTE ENRICHIE STYLE GBA
# ══════════════════════════════════════════════════════════════

# Herbe — 4 tons verts naturels
G_DARK = (40, 120, 48)
G_MID = (64, 168, 72)
G_LIGHT = (88, 192, 96)
G_BRIGHT = (112, 208, 112)

# Hautes herbes — tons plus foncés et saturés
HG_DARK = (32, 96, 32)
HG_MID = (48, 128, 40)
HG_LIGHT = (64, 152, 56)
HG_TIP = (80, 168, 64)

# Chemin — terre battue beige/brun
P_DARK = (152, 128, 88)
P_MID = (192, 168, 120)
P_LIGHT = (216, 192, 144)
P_EDGE = (128, 104, 72)

# Eau — bleus profonds
W_DARK = (32, 80, 168)
W_MID = (56, 112, 200)
W_LIGHT = (80, 144, 224)
W_SHINE = (128, 184, 248)

# Sable
S_DARK = (200, 184, 128)
S_MID = (224, 208, 152)
S_LIGHT = (240, 224, 176)

# Arbre feuilles
L_DARK = (24, 88, 32)
L_MID = (40, 120, 48)
L_LIGHT = (56, 152, 64)
L_SHINE = (72, 168, 80)
# Arbre tronc
TK_DARK = (72, 48, 24)
TK_MID = (104, 72, 40)
TK_LIGHT = (128, 96, 56)

# Fleur
FL_RED = (224, 64, 80)
FL_PINK = (240, 128, 144)
FL_YELLOW = (248, 216, 64)
FL_WHITE = (248, 248, 232)

# Roche/Grotte
R_DARK = (96, 88, 80)
R_MID = (136, 128, 112)
R_LIGHT = (168, 160, 144)
R_SHINE = (192, 184, 168)

# Bâtiment mur extérieur
BM_DARK = (184, 176, 160)
BM_MID = (216, 208, 192)
BM_LIGHT = (232, 224, 208)

# Toit rouge brique
RF_DARK = (152, 40, 24)
RF_MID = (192, 64, 48)
RF_LIGHT = (224, 88, 64)

# Bois intérieur
WD_DARK = (112, 72, 40)
WD_MID = (144, 104, 64)
WD_LIGHT = (176, 136, 88)

# Sol intérieur
SI_DARK = (192, 184, 168)
SI_MID = (216, 208, 192)
SI_LIGHT = (232, 224, 208)

# Mur intérieur
MI_DARK = (160, 144, 128)
MI_MID = (184, 168, 152)
MI_LIGHT = (200, 192, 176)

# Tapis rouge
TP_DARK = (152, 32, 32)
TP_MID = (192, 48, 48)
TP_LIGHT = (224, 72, 72)

# Carrelage (Centre Pokémon / Arène)
CL_DARK = (200, 200, 208)
CL_MID = (224, 224, 232)
CL_LIGHT = (240, 240, 248)

# Métal (machine)
MT_DARK = (128, 136, 144)
MT_MID = (168, 176, 184)
MT_LIGHT = (200, 208, 216)

# Clôture bois
FN_DARK = (96, 64, 32)
FN_MID = (136, 96, 56)
FN_LIGHT = (168, 128, 80)


def px(draw, x, y, color):
    """Dessiner un pixel."""
    draw.point((x, y), fill=color)


def rect(draw, x1, y1, x2, y2, color):
    """Remplir un rectangle."""
    draw.rectangle([x1, y1, x2, y2], fill=color)


def dither_fill(draw, x0, y0, w, h, c1, c2, pattern="checker"):
    """Remplissage avec motif de dithering."""
    for dy in range(h):
        for dx in range(w):
            if pattern == "checker":
                c = c1 if (dx + dy) % 2 == 0 else c2
            elif pattern == "horizontal":
                c = c1 if dy % 2 == 0 else c2
            elif pattern == "vertical":
                c = c1 if dx % 2 == 0 else c2
            else:
                c = c1
            px(draw, x0 + dx, y0 + dy, c)


def noise_fill(draw, x0, y0, w, h, colors, seed=0):
    """Remplissage avec bruit (choix aléatoire parmi couleurs)."""
    random.seed(seed)
    for dy in range(h):
        for dx in range(w):
            c = random.choice(colors)
            px(draw, x0 + dx, y0 + dy, c)


# ══════════════════════════════════════════════════════════════
# FONCTIONS DE DESSIN PAR TILE
# ══════════════════════════════════════════════════════════════

def draw_herbe(draw, ox, oy):
    """Tile 0: Herbe verte avec texture."""
    # Base verte
    noise_fill(draw, ox, oy, 32, 32, [G_MID, G_MID, G_MID, G_LIGHT, G_DARK], seed=100)
    # Brins d'herbe plus clairs
    for i in range(8):
        x = (i * 7 + 3) % 30 + ox
        y = (i * 5 + 2) % 28 + oy
        px(draw, x, y, G_BRIGHT)
        px(draw, x, y-1, G_LIGHT)


def draw_herbe_haute(draw, ox, oy):
    """Tile 1: Herbes hautes (zone de rencontre)."""
    # Base verte foncée
    noise_fill(draw, ox, oy, 32, 32, [HG_DARK, HG_MID, HG_DARK, HG_MID], seed=200)
    # Touffes d'herbe en V
    for i in range(6):
        bx = (i * 5 + 1) % 28 + ox
        by = (i * 4 + 4) % 24 + oy + 4
        # Brin gauche
        px(draw, bx, by, HG_TIP)
        px(draw, bx-1, by+1, HG_LIGHT)
        px(draw, bx-2, by+2, HG_MID)
        # Brin droit
        px(draw, bx+2, by, HG_TIP)
        px(draw, bx+3, by+1, HG_LIGHT)
        px(draw, bx+4, by+2, HG_MID)


def draw_chemin(draw, ox, oy):
    """Tile 2: Chemin de terre."""
    noise_fill(draw, ox, oy, 32, 32, [P_MID, P_MID, P_LIGHT, P_DARK, P_MID], seed=300)
    # Bord supérieur plus foncé (ombre)
    for x in range(32):
        px(draw, ox+x, oy, P_EDGE)
        px(draw, ox+x, oy+1, P_DARK)
    # Petits cailloux
    for i in range(4):
        cx = (i * 9 + 5) % 28 + ox
        cy = (i * 7 + 8) % 24 + oy + 4
        px(draw, cx, cy, R_LIGHT)
        px(draw, cx+1, cy, R_MID)


def draw_sable(draw, ox, oy):
    """Tile 3: Sable."""
    noise_fill(draw, ox, oy, 32, 32, [S_MID, S_MID, S_LIGHT, S_DARK, S_MID], seed=400)
    # Ondulations du sable
    for row in range(0, 32, 6):
        for x in range(32):
            if (x + row) % 8 < 2:
                px(draw, ox+x, oy+row, S_LIGHT)


def draw_eau(draw, ox, oy):
    """Tile 4: Eau avec reflets animés."""
    # Base bleue
    for y in range(32):
        for x in range(32):
            # Vagues horizontales
            wave = (x + y * 2) % 12
            if wave < 3:
                c = W_DARK
            elif wave < 6:
                c = W_MID
            elif wave < 9:
                c = W_LIGHT
            else:
                c = W_MID
            px(draw, ox+x, oy+y, c)
    # Reflets brillants
    for i in range(5):
        sx = (i * 7 + 4) % 28 + ox
        sy = (i * 6 + 3) % 26 + oy
        px(draw, sx, sy, W_SHINE)
        px(draw, sx+1, sy, W_SHINE)


def draw_fleur(draw, ox, oy):
    """Tile 5: Prairie fleurie."""
    # Base herbe
    noise_fill(draw, ox, oy, 32, 32, [G_MID, G_MID, G_LIGHT, G_DARK], seed=500)
    # Fleurs colorées (petits motifs 3×3)
    fleurs = [(6, 6, FL_RED), (18, 4, FL_YELLOW), (10, 16, FL_PINK),
              (24, 12, FL_WHITE), (4, 22, FL_YELLOW), (20, 24, FL_RED),
              (14, 28, FL_PINK)]
    for fx, fy, fc in fleurs:
        cx, cy = ox+fx, oy+fy
        px(draw, cx, cy-1, fc)
        px(draw, cx-1, cy, fc)
        px(draw, cx+1, cy, fc)
        px(draw, cx, cy+1, fc)
        px(draw, cx, cy, FL_WHITE)


def draw_arbre_haut(draw, ox, oy):
    """Tile 8: Haut de l'arbre (feuillage dense)."""
    # Fond transparent → herbe
    noise_fill(draw, ox, oy, 32, 32, [G_MID, G_MID, G_DARK], seed=810)
    # Canopée large ovale
    for y in range(4, 30):
        width = int(14 - abs(y - 16) * 0.9)
        if width < 2:
            continue
        cx = 16
        for x in range(cx - width, cx + width):
            if 0 <= x < 32:
                dist = abs(x - cx) / max(width, 1)
                if dist < 0.3:
                    c = L_SHINE if (x+y) % 5 == 0 else L_LIGHT
                elif dist < 0.6:
                    c = L_MID
                else:
                    c = L_DARK
                px(draw, ox+x, oy+y, c)
    # Ombrage supérieur
    for x in range(8, 24):
        px(draw, ox+x, oy+4, L_DARK)


def draw_arbre_bas(draw, ox, oy):
    """Tile 9: Bas de l'arbre (tronc + base feuillage)."""
    # Fond herbe
    noise_fill(draw, ox, oy, 32, 32, [G_MID, G_MID, G_DARK], seed=910)
    # Feuillage inférieur (arc)
    for y in range(0, 14):
        width = int(14 - abs(y - 2) * 0.6)
        if width < 2:
            continue
        cx = 16
        for x in range(cx - width, cx + width):
            if 0 <= x < 32:
                dist = abs(x - cx) / max(width, 1)
                c = L_LIGHT if dist < 0.4 else (L_MID if dist < 0.7 else L_DARK)
                px(draw, ox+x, oy+y, c)
    # Tronc
    for y in range(10, 28):
        trunk_w = 3 if y < 20 else 4
        for x in range(16 - trunk_w, 16 + trunk_w):
            if x == 16 - trunk_w or x == 16 + trunk_w - 1:
                c = TK_DARK
            elif x == 16 - trunk_w + 1:
                c = TK_LIGHT
            else:
                c = TK_MID
            px(draw, ox+x, oy+y, c)
    # Ombre au sol
    for x in range(10, 22):
        px(draw, ox+x, oy+28, G_DARK)
        px(draw, ox+x, oy+29, G_DARK)


def draw_arbre_haut_r(draw, ox, oy):
    """Tile 10: Arbre haut (variante droite)."""
    draw_arbre_haut(draw, ox, oy)
    # Ajout reflets à droite
    for y in range(6, 24):
        px(draw, ox+22, oy+y, L_SHINE)


def draw_arbre_bas_r(draw, ox, oy):
    """Tile 11: Arbre bas (variante droite)."""
    draw_arbre_bas(draw, ox, oy)


def draw_fence_h(draw, ox, oy):
    """Tile 12: Clôture horizontale."""
    noise_fill(draw, ox, oy, 32, 32, [G_MID, G_MID, G_DARK], seed=1210)
    # Poteaux
    for px_x in [2, 14, 28]:
        rect(draw, ox+px_x, oy+8, ox+px_x+3, oy+28, FN_MID)
        rect(draw, ox+px_x, oy+8, ox+px_x, oy+28, FN_DARK)
        rect(draw, ox+px_x+3, oy+8, ox+px_x+3, oy+28, FN_DARK)
        # Sommet
        rect(draw, ox+px_x-1, oy+6, ox+px_x+4, oy+8, FN_LIGHT)
    # Traverses
    rect(draw, ox, oy+14, ox+31, oy+16, FN_MID)
    rect(draw, ox, oy+14, ox+31, oy+14, FN_LIGHT)
    rect(draw, ox, oy+22, ox+31, oy+24, FN_MID)
    rect(draw, ox, oy+22, ox+31, oy+22, FN_LIGHT)


def draw_fence_v(draw, ox, oy):
    """Tile 13: Clôture verticale."""
    noise_fill(draw, ox, oy, 32, 32, [G_MID, G_MID, G_DARK], seed=1310)
    # Poteau vertical au centre
    rect(draw, ox+13, oy, ox+18, oy+31, FN_MID)
    rect(draw, ox+13, oy, ox+13, oy+31, FN_DARK)
    rect(draw, ox+18, oy, ox+18, oy+31, FN_DARK)
    rect(draw, ox+14, oy, ox+15, oy+31, FN_LIGHT)
    # Traverses
    for ty in [4, 16, 28]:
        rect(draw, ox+10, oy+ty, ox+21, oy+ty+2, FN_MID)
        rect(draw, ox+10, oy+ty, ox+21, oy+ty, FN_LIGHT)


def draw_buisson(draw, ox, oy):
    """Tile 14: Buisson dense."""
    noise_fill(draw, ox, oy, 32, 32, [G_MID, G_MID, G_DARK], seed=1410)
    # Buisson rond
    for y in range(6, 28):
        for x in range(4, 28):
            dist = ((x-16)**2 + (y-17)**2) ** 0.5
            if dist < 11:
                if dist < 5:
                    c = L_LIGHT if (x+y) % 4 == 0 else L_MID
                elif dist < 8:
                    c = L_MID if (x+y) % 3 == 0 else L_DARK
                else:
                    c = L_DARK
                px(draw, ox+x, oy+y, c)


def draw_herbe_detail(draw, ox, oy):
    """Tile 15: Herbe détaillée."""
    noise_fill(draw, ox, oy, 32, 32, [G_MID, G_LIGHT, G_MID, G_DARK, G_MID], seed=1510)
    # Détails de texture : petites touffes
    for i in range(12):
        bx = (i * 5 + 2) % 30 + ox
        by = (i * 4 + 1) % 28 + oy + 2
        px(draw, bx, by, G_BRIGHT)
        px(draw, bx-1, by+1, G_LIGHT)
        px(draw, bx+1, by+1, G_LIGHT)


def draw_toit_g(draw, ox, oy):
    """Tile 16: Toit gauche."""
    rect(draw, ox, oy, ox+31, oy+31, BM_MID)
    for y in range(32):
        # Pente du toit : rouge brique
        end_x = min(31, y + 4)
        for x in range(0, end_x):
            if (x + y) % 4 == 0:
                c = RF_LIGHT
            elif (x + y) % 4 == 2:
                c = RF_DARK
            else:
                c = RF_MID
            px(draw, ox+x, oy+y, c)
        # Bord
        if end_x < 32:
            px(draw, ox+end_x, oy+y, RF_DARK)


def draw_toit_m(draw, ox, oy):
    """Tile 17: Toit milieu."""
    for y in range(32):
        for x in range(32):
            if (x + y) % 4 == 0:
                c = RF_LIGHT
            elif (x + y) % 4 == 2:
                c = RF_DARK
            else:
                c = RF_MID
            px(draw, ox+x, oy+y, c)
    # Ligne faîtière
    rect(draw, ox, oy, ox+31, oy+2, RF_DARK)
    rect(draw, ox, oy+1, ox+31, oy+1, RF_LIGHT)


def draw_toit_d(draw, ox, oy):
    """Tile 18: Toit droit."""
    rect(draw, ox, oy, ox+31, oy+31, BM_MID)
    for y in range(32):
        start_x = max(0, 28 - y)
        for x in range(start_x, 32):
            if (x + y) % 4 == 0:
                c = RF_LIGHT
            elif (x + y) % 4 == 2:
                c = RF_DARK
            else:
                c = RF_MID
            px(draw, ox+x, oy+y, c)
        if start_x > 0:
            px(draw, ox+start_x, oy+y, RF_DARK)


def draw_mur_g(draw, ox, oy):
    """Tile 19: Mur gauche bâtiment."""
    rect(draw, ox, oy, ox+31, oy+31, BM_MID)
    # Bord gauche ombré
    rect(draw, ox, oy, ox+2, oy+31, BM_DARK)
    # Texture mur
    for y in range(0, 32, 4):
        for x in range(3, 32):
            if y % 8 < 4:
                if x % 8 == 0:
                    px(draw, ox+x, oy+y, BM_DARK)
            else:
                if (x + 4) % 8 == 0:
                    px(draw, ox+x, oy+y, BM_DARK)


def draw_mur_m(draw, ox, oy):
    """Tile 20: Mur milieu bâtiment."""
    rect(draw, ox, oy, ox+31, oy+31, BM_MID)
    # Briques régulières
    for y in range(0, 32, 4):
        for x in range(0, 32):
            if y % 8 < 4:
                if x % 8 == 0:
                    px(draw, ox+x, oy+y, BM_DARK)
            else:
                if (x + 4) % 8 == 0:
                    px(draw, ox+x, oy+y, BM_DARK)
    # Ligne séparatrice horizontale
    for x in range(32):
        px(draw, ox+x, oy, BM_DARK)


def draw_mur_d(draw, ox, oy):
    """Tile 21: Mur droit bâtiment."""
    rect(draw, ox, oy, ox+31, oy+31, BM_MID)
    # Bord droit ombré
    rect(draw, ox+29, oy, ox+31, oy+31, BM_DARK)
    # Texture
    for y in range(0, 32, 4):
        for x in range(0, 29):
            if y % 8 < 4:
                if x % 8 == 0:
                    px(draw, ox+x, oy+y, BM_DARK)
            else:
                if (x + 4) % 8 == 0:
                    px(draw, ox+x, oy+y, BM_DARK)


def draw_porte(draw, ox, oy):
    """Tile 22: Porte de bâtiment."""
    rect(draw, ox, oy, ox+31, oy+31, BM_MID)
    # Cadre de porte
    rect(draw, ox+8, oy+2, ox+23, oy+31, WD_DARK)
    rect(draw, ox+9, oy+3, ox+22, oy+31, WD_MID)
    # Panneaux de porte
    rect(draw, ox+10, oy+4, ox+15, oy+14, WD_LIGHT)
    rect(draw, ox+16, oy+4, ox+21, oy+14, WD_LIGHT)
    rect(draw, ox+10, oy+16, ox+15, oy+30, WD_LIGHT)
    rect(draw, ox+16, oy+16, ox+21, oy+30, WD_LIGHT)
    # Poignée
    rect(draw, ox+20, oy+18, ox+21, oy+20, (200, 180, 64))
    # Ombre
    rect(draw, ox+8, oy+2, ox+8, oy+31, (64, 48, 24))


def draw_fenetre(draw, ox, oy):
    """Tile 23: Fenêtre bâtiment."""
    rect(draw, ox, oy, ox+31, oy+31, BM_MID)
    # Cadre fenêtre
    rect(draw, ox+6, oy+6, ox+25, oy+25, WD_DARK)
    # Vitre (bleu clair)
    rect(draw, ox+8, oy+8, ox+23, oy+23, (160, 200, 232))
    # Croisillon
    rect(draw, ox+15, oy+8, ox+16, oy+23, WD_MID)
    rect(draw, ox+8, oy+15, ox+23, oy+16, WD_MID)
    # Reflet
    rect(draw, ox+10, oy+10, ox+13, oy+13, (200, 224, 248))
    # Texture mur
    for y in range(0, 6):
        for x in range(0, 32, 8):
            px(draw, ox+x, oy+y, BM_DARK)


def draw_sol_int(draw, ox, oy):
    """Tile 24: Sol intérieur basique."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Carrelage subtil
    for y in range(0, 32, 8):
        for x in range(32):
            px(draw, ox+x, oy+y, SI_DARK)
    for x in range(0, 32, 8):
        for y in range(32):
            px(draw, ox+x, oy+y, SI_DARK)
    # Reflets
    for i in range(4):
        sx = (i * 9 + 3) % 28 + ox
        sy = (i * 7 + 2) % 28 + oy
        px(draw, sx, sy, SI_LIGHT)


def draw_mur_int(draw, ox, oy):
    """Tile 25: Mur intérieur."""
    # Moitié haute : mur
    rect(draw, ox, oy, ox+31, oy+19, MI_MID)
    # Moitié basse : plinthe
    rect(draw, ox, oy+20, ox+31, oy+31, MI_DARK)
    # Moulure séparatrice
    rect(draw, ox, oy+18, ox+31, oy+20, MI_LIGHT)
    # Texture mur vertical
    for x in range(0, 32, 6):
        for y in range(0, 18):
            px(draw, ox+x, oy+y, MI_DARK)


def draw_comptoir(draw, ox, oy):
    """Tile 26: Comptoir (boutique/centre)."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Surface du comptoir
    rect(draw, ox+2, oy+8, ox+29, oy+24, WD_MID)
    rect(draw, ox+2, oy+8, ox+29, oy+10, WD_LIGHT)
    # Bord avant
    rect(draw, ox+2, oy+24, ox+29, oy+26, WD_DARK)
    # Panneau frontal
    rect(draw, ox+4, oy+12, ox+27, oy+22, WD_DARK)
    rect(draw, ox+5, oy+13, ox+26, oy+21, WD_MID)


def draw_machine_soin(draw, ox, oy):
    """Tile 27: Machine de soin Pokémon."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Corps machine
    rect(draw, ox+6, oy+4, ox+25, oy+28, MT_MID)
    rect(draw, ox+6, oy+4, ox+6, oy+28, MT_DARK)
    rect(draw, ox+25, oy+4, ox+25, oy+28, MT_DARK)
    rect(draw, ox+6, oy+4, ox+25, oy+4, MT_LIGHT)
    # Écran
    rect(draw, ox+10, oy+8, ox+21, oy+16, (64, 200, 120))
    # Croix rouge (soin)
    rect(draw, ox+14, oy+9, ox+17, oy+15, (232, 48, 48))
    rect(draw, ox+11, oy+11, ox+20, oy+13, (232, 48, 48))
    # Boutons
    rect(draw, ox+10, oy+20, ox+13, oy+22, (48, 48, 200))
    rect(draw, ox+18, oy+20, ox+21, oy+22, (200, 48, 48))


def draw_etagere(draw, ox, oy):
    """Tile 28: Étagère."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Étagère en bois
    for shelf_y in [4, 14, 24]:
        rect(draw, ox+3, oy+shelf_y, ox+28, oy+shelf_y+1, WD_DARK)
        rect(draw, ox+3, oy+shelf_y, ox+28, oy+shelf_y, WD_LIGHT)
    # Montants
    rect(draw, ox+3, oy+2, ox+5, oy+30, WD_MID)
    rect(draw, ox+26, oy+2, ox+28, oy+30, WD_MID)
    # Objets sur étagères (rectangles colorés)
    colors = [(232, 64, 64), (64, 64, 232), (64, 200, 64), (232, 200, 64)]
    for i, sy in enumerate([6, 16]):
        for j in range(3):
            c = colors[(i*3+j) % len(colors)]
            bx = 8 + j * 7
            rect(draw, ox+bx, oy+sy, ox+bx+4, oy+sy+6, c)


def draw_tapis(draw, ox, oy):
    """Tile 29: Tapis rouge."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Tapis
    rect(draw, ox+2, oy+2, ox+29, oy+29, TP_MID)
    # Bordure
    rect(draw, ox+2, oy+2, ox+29, oy+3, TP_DARK)
    rect(draw, ox+2, oy+28, ox+29, oy+29, TP_DARK)
    rect(draw, ox+2, oy+2, ox+3, oy+29, TP_DARK)
    rect(draw, ox+28, oy+2, ox+29, oy+29, TP_DARK)
    # Motif intérieur
    rect(draw, ox+5, oy+5, ox+26, oy+26, TP_LIGHT)
    rect(draw, ox+6, oy+6, ox+25, oy+25, TP_MID)


def draw_sol_carrelage(draw, ox, oy):
    """Tile 30: Sol carrelage."""
    rect(draw, ox, oy, ox+31, oy+31, CL_MID)
    # Grille de carrelage
    for y in range(0, 32, 16):
        for x in range(32):
            px(draw, ox+x, oy+y, CL_DARK)
    for x in range(0, 32, 16):
        for y in range(32):
            px(draw, ox+x, oy+y, CL_DARK)
    # Reflets
    rect(draw, ox+3, oy+3, ox+6, oy+6, CL_LIGHT)
    rect(draw, ox+19, oy+19, ox+22, oy+22, CL_LIGHT)


def draw_mur_motif(draw, ox, oy):
    """Tile 31: Mur avec motif (grotte/roche)."""
    rect(draw, ox, oy, ox+31, oy+31, R_MID)
    # Texture roche irrégulière
    noise_fill(draw, ox, oy, 32, 32, [R_DARK, R_MID, R_MID, R_LIGHT, R_MID], seed=3100)
    # Fissures
    for i in range(3):
        sx = (i * 11 + 5) % 28 + ox
        sy = (i * 9 + 2) % 24 + oy
        for j in range(6):
            px(draw, sx + j % 3, sy + j, R_DARK)


def draw_lit_tete(draw, ox, oy):
    """Tile 32: Lit (tête)."""
    rect(draw, ox, oy, ox+31, oy+31, WD_MID)
    # Tête de lit
    rect(draw, ox+2, oy+2, ox+29, oy+8, WD_DARK)
    rect(draw, ox+3, oy+3, ox+28, oy+7, WD_MID)
    # Oreiller
    rect(draw, ox+6, oy+10, ox+25, oy+18, (240, 240, 248))
    rect(draw, ox+7, oy+11, ox+24, oy+17, (248, 248, 255))
    # Couverture
    rect(draw, ox+4, oy+19, ox+27, oy+31, (96, 144, 200))
    rect(draw, ox+5, oy+20, ox+26, oy+30, (112, 160, 216))


def draw_lit_pied(draw, ox, oy):
    """Tile 33: Lit (pied)."""
    rect(draw, ox, oy, ox+31, oy+31, WD_MID)
    # Couverture
    rect(draw, ox+4, oy, ox+27, oy+22, (96, 144, 200))
    rect(draw, ox+5, oy, ox+26, oy+21, (112, 160, 216))
    # Pied de lit
    rect(draw, ox+2, oy+23, ox+29, oy+28, WD_DARK)
    rect(draw, ox+3, oy+24, ox+28, oy+27, WD_MID)


def draw_tv(draw, ox, oy):
    """Tile 34: Télévision."""
    rect(draw, ox, oy, ox+31, oy+31, WD_MID)
    # Boîtier TV
    rect(draw, ox+4, oy+4, ox+27, oy+24, (48, 48, 56))
    # Écran
    rect(draw, ox+6, oy+6, ox+25, oy+20, (80, 120, 160))
    # Reflet
    rect(draw, ox+8, oy+8, ox+14, oy+12, (120, 160, 200))
    # Pied
    rect(draw, ox+12, oy+25, ox+19, oy+28, (48, 48, 56))
    # Antenne
    px(draw, ox+12, oy+2, (48, 48, 56))
    px(draw, ox+11, oy+1, (48, 48, 56))
    px(draw, ox+20, oy+2, (48, 48, 56))
    px(draw, ox+21, oy+1, (48, 48, 56))


def draw_pc(draw, ox, oy):
    """Tile 35: Ordinateur PC."""
    rect(draw, ox, oy, ox+31, oy+31, WD_MID)
    # Écran
    rect(draw, ox+6, oy+2, ox+25, oy+18, (48, 48, 56))
    rect(draw, ox+8, oy+4, ox+23, oy+16, (64, 128, 200))
    # Texte à l'écran
    for ty in [6, 9, 12]:
        rect(draw, ox+10, oy+ty, ox+20, oy+ty+1, (120, 200, 120))
    # Clavier
    rect(draw, ox+8, oy+22, ox+23, oy+28, (80, 80, 88))
    # Touches
    for ky in [23, 25, 27]:
        for kx in range(9, 23, 3):
            rect(draw, ox+kx, oy+ky, ox+kx+1, oy+ky, (120, 120, 128))


def draw_plante(draw, ox, oy):
    """Tile 36: Plante en pot."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Pot
    rect(draw, ox+10, oy+20, ox+21, oy+30, (176, 96, 48))
    rect(draw, ox+11, oy+21, ox+20, oy+29, (200, 120, 64))
    rect(draw, ox+9, oy+20, ox+22, oy+21, (152, 80, 40))
    # Feuilles
    for angle in range(8):
        fx = 16 + int(8 * [1, 0.7, 0, -0.7, -1, -0.7, 0, 0.7][angle])
        fy = 12 + int(6 * [0, -0.7, -1, -0.7, 0, 0.7, 1, 0.7][angle])
        for r in range(4):
            lx = 16 + int((fx-16) * r / 4)
            ly = 14 + int((fy-14) * r / 4)
            if 0 <= lx < 32 and 0 <= ly < 32:
                px(draw, ox+lx, oy+ly, L_LIGHT if r < 2 else L_MID)


def draw_escalier_up(draw, ox, oy):
    """Tile 37: Escalier montant."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Marches (montant vers le haut)
    for i in range(6):
        y = 28 - i * 5
        shade = SI_DARK if i % 2 == 0 else MI_MID
        rect(draw, ox+2, oy+y, ox+29, oy+y+3, shade)
        rect(draw, ox+2, oy+y, ox+29, oy+y, MI_LIGHT)
    # Rampe gauche
    rect(draw, ox+1, oy, ox+3, oy+31, WD_DARK)
    # Flèche vers le haut
    for i in range(4):
        lx = 14 - i
        rx = 17 + i
        rect(draw, ox+lx, oy+4-i, ox+rx, oy+4-i, (255, 255, 200))


def draw_escalier_down(draw, ox, oy):
    """Tile 38: Escalier descendant."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Marches (descendant)
    for i in range(6):
        y = 2 + i * 5
        shade = R_DARK if i % 2 == 0 else R_MID
        rect(draw, ox+2, oy+y, ox+29, oy+y+3, shade)
        rect(draw, ox+2, oy+y, ox+29, oy+y, R_LIGHT)
    # Obscurité au fond
    rect(draw, ox+4, oy+28, ox+27, oy+31, (32, 32, 40))


def draw_paillasson(draw, ox, oy):
    """Tile 39: Paillasson."""
    noise_fill(draw, ox, oy, 32, 32, [G_MID, G_MID, G_DARK], seed=3900)
    # Tapis d'entrée brun
    rect(draw, ox+4, oy+10, ox+27, oy+26, (136, 96, 56))
    dither_fill(draw, ox+5, oy+11, 22, 14, (152, 112, 72), (128, 88, 48))
    # Bordure
    rect(draw, ox+4, oy+10, ox+27, oy+10, (104, 72, 40))
    rect(draw, ox+4, oy+26, ox+27, oy+26, (104, 72, 40))


def draw_porte_int(draw, ox, oy):
    """Tile 40: Porte intérieure."""
    rect(draw, ox, oy, ox+31, oy+31, MI_MID)
    # Porte
    rect(draw, ox+8, oy+2, ox+23, oy+31, WD_MID)
    rect(draw, ox+8, oy+2, ox+8, oy+31, WD_DARK)
    rect(draw, ox+23, oy+2, ox+23, oy+31, WD_DARK)
    # Panneaux
    rect(draw, ox+10, oy+4, ox+21, oy+14, WD_LIGHT)
    rect(draw, ox+10, oy+16, ox+21, oy+30, WD_LIGHT)
    # Cadre
    rect(draw, ox+8, oy+2, ox+23, oy+2, WD_DARK)
    # Poignée
    px(draw, ox+20, oy+18, (200, 180, 64))
    px(draw, ox+20, oy+19, (200, 180, 64))


def draw_fenetre_int(draw, ox, oy):
    """Tile 41: Fenêtre intérieure."""
    rect(draw, ox, oy, ox+31, oy+31, MI_MID)
    # Cadre
    rect(draw, ox+5, oy+4, ox+26, oy+24, WD_DARK)
    # Vitre (bleu ciel)
    rect(draw, ox+7, oy+6, ox+24, oy+22, (168, 208, 240))
    # Croisillon
    rect(draw, ox+15, oy+6, ox+16, oy+22, WD_MID)
    rect(draw, ox+7, oy+13, ox+24, oy+14, WD_MID)
    # Reflet
    rect(draw, ox+9, oy+8, ox+13, oy+11, (200, 232, 255))
    # Rideau
    rect(draw, ox+5, oy+4, ox+7, oy+22, (200, 160, 120))
    rect(draw, ox+24, oy+4, ox+26, oy+22, (200, 160, 120))


def draw_sol_bois(draw, ox, oy):
    """Tile 42: Sol bois foncé."""
    rect(draw, ox, oy, ox+31, oy+31, WD_MID)
    # Planches de bois
    for y in range(0, 32, 8):
        rect(draw, ox, oy+y, ox+31, oy+y, WD_DARK)
        # Grain du bois
        for x in range(0, 32, 3):
            px(draw, ox+x, oy+y+3, WD_LIGHT)
            px(draw, ox+x+1, oy+y+5, WD_DARK)
    # Noeud de bois
    px(draw, ox+12, oy+12, WD_DARK)
    px(draw, ox+11, oy+12, WD_DARK)
    px(draw, ox+12, oy+11, WD_DARK)


def draw_mur_ext_fenetre(draw, ox, oy):
    """Tile 43: Mur extérieur avec fenêtre."""
    rect(draw, ox, oy, ox+31, oy+31, BM_MID)
    # Texture mur
    for y in range(0, 32, 4):
        for x in range(0, 32):
            if y % 8 < 4:
                if x % 8 == 0:
                    px(draw, ox+x, oy+y, BM_DARK)
            else:
                if (x + 4) % 8 == 0:
                    px(draw, ox+x, oy+y, BM_DARK)
    # Petite fenêtre
    rect(draw, ox+10, oy+8, ox+21, oy+20, WD_DARK)
    rect(draw, ox+11, oy+9, ox+20, oy+19, (160, 200, 232))
    rect(draw, ox+15, oy+9, ox+16, oy+19, WD_MID)


def draw_table(draw, ox, oy):
    """Tile 44: Table."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Plateau
    rect(draw, ox+4, oy+8, ox+27, oy+14, WD_MID)
    rect(draw, ox+4, oy+8, ox+27, oy+9, WD_LIGHT)
    rect(draw, ox+4, oy+14, ox+27, oy+14, WD_DARK)
    # Pieds
    rect(draw, ox+6, oy+15, ox+8, oy+28, WD_DARK)
    rect(draw, ox+23, oy+15, ox+25, oy+28, WD_DARK)


def draw_chaise(draw, ox, oy):
    """Tile 45: Chaise."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Dossier
    rect(draw, ox+10, oy+2, ox+21, oy+14, WD_MID)
    rect(draw, ox+10, oy+2, ox+21, oy+3, WD_LIGHT)
    rect(draw, ox+10, oy+2, ox+10, oy+14, WD_DARK)
    rect(draw, ox+21, oy+2, ox+21, oy+14, WD_DARK)
    # Assise
    rect(draw, ox+8, oy+14, ox+23, oy+18, WD_MID)
    rect(draw, ox+8, oy+14, ox+23, oy+14, WD_LIGHT)
    # Pieds
    rect(draw, ox+9, oy+19, ox+10, oy+28, WD_DARK)
    rect(draw, ox+21, oy+19, ox+22, oy+28, WD_DARK)


def draw_poster(draw, ox, oy):
    """Tile 46: Poster mural."""
    rect(draw, ox, oy, ox+31, oy+31, MI_MID)
    # Cadre du poster
    rect(draw, ox+5, oy+3, ox+26, oy+28, (48, 48, 56))
    # Contenu (image stylisée — Pokeball)
    rect(draw, ox+7, oy+5, ox+24, oy+26, (240, 232, 216))
    # Dessin simplifié d'une Pokéball
    cx, cy = ox+15, oy+15
    for angle_y in range(-8, 9):
        for angle_x in range(-8, 9):
            dist = (angle_x**2 + angle_y**2) ** 0.5
            if dist <= 8:
                if angle_y < 0:
                    c = (232, 48, 48) if dist > 2 else (248, 248, 248)
                else:
                    c = (248, 248, 248) if dist > 2 else (248, 248, 248)
                if abs(angle_y) <= 1 and dist > 2:
                    c = (32, 32, 32)
                if dist > 7:
                    c = (32, 32, 32)
                px(draw, cx+angle_x, cy+angle_y, c)


def draw_poubelle(draw, ox, oy):
    """Tile 47: Poubelle."""
    rect(draw, ox, oy, ox+31, oy+31, SI_MID)
    # Corps de la poubelle
    rect(draw, ox+9, oy+8, ox+22, oy+28, (128, 128, 136))
    rect(draw, ox+9, oy+8, ox+9, oy+28, (96, 96, 104))
    rect(draw, ox+22, oy+8, ox+22, oy+28, (96, 96, 104))
    # Couvercle
    rect(draw, ox+7, oy+6, ox+24, oy+9, (144, 144, 152))
    rect(draw, ox+7, oy+6, ox+24, oy+6, (168, 168, 176))
    # Poignée
    rect(draw, ox+14, oy+4, ox+17, oy+6, (160, 160, 168))
    # Rayures
    for sy in [14, 20]:
        rect(draw, ox+11, oy+sy, ox+20, oy+sy, (112, 112, 120))


# ══════════════════════════════════════════════════════════════
# TABLE DE DISPATCH — correspondance index → fonction
# ══════════════════════════════════════════════════════════════
TILE_FUNCS = {
    0: draw_herbe, 1: draw_herbe_haute, 2: draw_chemin, 3: draw_sable,
    4: draw_eau, 5: draw_fleur,
    # 6, 7: vides (herbe par défaut)
    8: draw_arbre_haut, 9: draw_arbre_bas, 10: draw_arbre_haut_r, 11: draw_arbre_bas_r,
    12: draw_fence_h, 13: draw_fence_v, 14: draw_buisson, 15: draw_herbe_detail,
    16: draw_toit_g, 17: draw_toit_m, 18: draw_toit_d,
    19: draw_mur_g, 20: draw_mur_m, 21: draw_mur_d, 22: draw_porte, 23: draw_fenetre,
    24: draw_sol_int, 25: draw_mur_int, 26: draw_comptoir, 27: draw_machine_soin,
    28: draw_etagere, 29: draw_tapis, 30: draw_sol_carrelage, 31: draw_mur_motif,
    32: draw_lit_tete, 33: draw_lit_pied, 34: draw_tv, 35: draw_pc,
    36: draw_plante, 37: draw_escalier_up, 38: draw_escalier_down, 39: draw_paillasson,
    40: draw_porte_int, 41: draw_fenetre_int, 42: draw_sol_bois, 43: draw_mur_ext_fenetre,
    44: draw_table, 45: draw_chaise, 46: draw_poster, 47: draw_poubelle,
}


def main():
    img = Image.new("RGBA", (COLS * TILE, ROWS * TILE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for row in range(ROWS):
        for col in range(COLS):
            idx = row * COLS + col
            ox = col * TILE
            oy = row * TILE
            if idx in TILE_FUNCS:
                TILE_FUNCS[idx](draw, ox, oy)
            else:
                # Tiles vides → herbe par défaut
                draw_herbe(draw, ox, oy)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT)
    print(f"Tileset v5 généré : {img.width}×{img.height}px, {COLS}×{ROWS} = {COLS*ROWS} tiles")
    print(f"Sauvé dans : {OUT}")


if __name__ == "__main__":
    main()
