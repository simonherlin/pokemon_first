#!/usr/bin/env python3
"""
Générateur de tileset pixel art style Pokémon FRLG
Crée des tiles 32x32 détaillées avec couleurs riches et formes reconnaissables
"""

from PIL import Image, ImageDraw

TILE = 32
COLS = 8
ROWS = 8
WIDTH = COLS * TILE
HEIGHT = ROWS * TILE

# Palette de couleurs FRLG (inspirée du style GBA)
# Herbe
C_HERBE_CLAIR = (120, 200, 80)
C_HERBE = (72, 168, 56)
C_HERBE_FONCE = (48, 128, 32)
C_HERBE_TRES_FONCE = (32, 96, 24)

# Chemin / Sable
C_CHEMIN_CLAIR = (232, 216, 176)
C_CHEMIN = (208, 184, 136)
C_CHEMIN_FONCE = (176, 152, 104)
C_SABLE_CLAIR = (248, 232, 192)
C_SABLE = (232, 208, 160)
C_SABLE_FONCE = (200, 176, 128)

# Eau
C_EAU_CLAIR = (104, 176, 248)
C_EAU = (64, 144, 232)
C_EAU_FONCE = (40, 112, 200)
C_EAU_TRES_FONCE = (24, 80, 168)

# Arbres
C_FEUILLE_CLAIR = (80, 184, 64)
C_FEUILLE = (48, 152, 40)
C_FEUILLE_FONCE = (24, 112, 24)
C_FEUILLE_TRES_FONCE = (16, 80, 16)
C_TRONC_CLAIR = (160, 120, 72)
C_TRONC = (128, 88, 48)
C_TRONC_FONCE = (96, 64, 32)

# Bâtiments extérieurs
C_TOIT_CLAIR = (200, 80, 72)
C_TOIT = (176, 56, 48)
C_TOIT_FONCE = (144, 40, 32)
C_MUR_EXT_CLAIR = (248, 240, 224)
C_MUR_EXT = (232, 216, 192)
C_MUR_EXT_FONCE = (200, 184, 160)
C_BRIQUE = (192, 168, 136)

# Porte extérieure
C_PORTE_BOIS = (136, 88, 48)
C_PORTE_BOIS_CLAIR = (168, 120, 72)
C_PORTE_BOIS_FONCE = (104, 64, 32)

# Fenêtre
C_VITRE = (176, 216, 248)
C_VITRE_FONCE = (128, 176, 224)
C_CADRE = (192, 176, 152)

# Intérieur - Sol parquet
C_PARQUET_CLAIR = (216, 192, 152)
C_PARQUET = (192, 168, 128)
C_PARQUET_FONCE = (168, 144, 104)
C_PARQUET_TRES_FONCE = (144, 120, 80)

# Intérieur - Mur
C_MUR_INT_CLAIR = (240, 232, 216)
C_MUR_INT = (224, 216, 200)
C_MUR_INT_FONCE = (200, 192, 176)
C_PLINTHE = (176, 160, 136)
C_PLINTHE_FONCE = (152, 136, 112)

# Lit
C_OREILLER = (240, 240, 248)
C_OREILLER_OMBRE = (208, 208, 224)
C_COUVERTURE = (88, 136, 216)
C_COUVERTURE_CLAIR = (120, 168, 240)
C_COUVERTURE_FONCE = (56, 104, 184)
C_LIT_BOIS = (152, 104, 56)
C_LIT_BOIS_FONCE = (120, 80, 40)

# TV
C_TV_ECRAN = (32, 32, 48)
C_TV_ECRAN_REFLET = (64, 72, 96)
C_TV_CORPS = (80, 80, 88)
C_TV_CORPS_CLAIR = (104, 104, 112)

# PC
C_PC_ECRAN = (80, 200, 120)
C_PC_ECRAN_CLAIR = (120, 232, 160)
C_PC_CORPS = (200, 200, 208)
C_PC_CORPS_FONCE = (168, 168, 176)
C_PC_CLAVIER = (64, 64, 72)

# Plante
C_POT = (176, 112, 64)
C_POT_FONCE = (144, 88, 48)
C_POT_TERRE = (120, 80, 48)
C_PLANTE_CLAIR = (96, 200, 80)
C_PLANTE = (64, 168, 48)
C_PLANTE_FONCE = (40, 128, 32)

# Escalier
C_ESCALIER_CLAIR = (184, 152, 112)
C_ESCALIER = (152, 120, 80)
C_ESCALIER_FONCE = (120, 88, 56)
C_ESCALIER_OMBRE = (96, 72, 48)

# Tapis (style FRLG - bleu/crème, pas rouge)
C_TAPIS = (72, 104, 160)
C_TAPIS_CLAIR = (96, 128, 184)
C_TAPIS_FONCE = (56, 80, 136)
C_TAPIS_BORD = (200, 184, 152)
C_TAPIS_MOTIF = (120, 152, 200)

# Clôture
C_CLOTURE_CLAIR = (224, 208, 176)
C_CLOTURE = (192, 176, 144)
C_CLOTURE_FONCE = (160, 144, 112)

# Fleurs
C_FLEUR_ROUGE = (232, 72, 72)
C_FLEUR_JAUNE = (248, 224, 72)
C_FLEUR_BLANC = (248, 248, 240)

# Comptoir / Table
C_TABLE_BOIS = (168, 128, 80)
C_TABLE_BOIS_CLAIR = (192, 152, 104)
C_TABLE_BOIS_FONCE = (136, 96, 56)

# Noir (outlines)
BLACK = (0, 0, 0)
NOIR = (24, 24, 32)
TRANSPARENT = (0, 0, 0, 0)

# Carrelage
C_CARRELAGE = (216, 224, 232)
C_CARRELAGE_FONCE = (192, 200, 208)
C_CARRELAGE_JOINT = (176, 184, 192)

# Machine de soin
C_MACHINE = (248, 248, 248)
C_MACHINE_FONCE = (216, 216, 224)
C_MACHINE_ROUGE = (224, 64, 64)
C_MACHINE_VERT = (64, 200, 80)

# Étagère
C_ETAGERE = (136, 96, 56)
C_ETAGERE_CLAIR = (168, 128, 80)
C_LIVRE_R = (200, 56, 56)
C_LIVRE_B = (56, 88, 168)
C_LIVRE_V = (56, 152, 72)
C_LIVRE_J = (216, 192, 72)

# Poster
C_POSTER_FOND = (240, 232, 208)
C_POSTER_CADRE = (120, 88, 56)

# Chaise
C_CHAISE = (160, 120, 72)
C_CHAISE_CLAIR = (184, 144, 96)
C_CHAISE_FONCE = (128, 88, 48)

# Poubelle
C_POUB = (168, 176, 184)
C_POUB_FONCE = (136, 144, 152)
C_POUB_COUVERCLE = (192, 200, 208)

# Herbe haute (vert foncé avec patterns)
C_HAUTE_CLAIR = (56, 168, 48)
C_HAUTE = (40, 136, 32)
C_HAUTE_FONCE = (24, 104, 16)
C_HAUTE_DETAIL = (80, 192, 64)

# Buisson
C_BUISSON_CLAIR = (72, 176, 56)
C_BUISSON = (48, 144, 40)
C_BUISSON_FONCE = (32, 112, 24)

# Paillasson
C_PAILL = (160, 128, 80)
C_PAILL_CLAIR = (184, 152, 104)
C_PAILL_FONCE = (136, 104, 64)


def put(img, x, y, color):
    """Place un pixel si dans les limites"""
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), color + (255,) if len(color) == 3 else color)


def fill_rect(img, x1, y1, x2, y2, color):
    """Remplit un rectangle"""
    c = color + (255,) if len(color) == 3 else color
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if 0 <= x < img.width and 0 <= y < img.height:
                img.putpixel((x, y), c)


def draw_outline_rect(img, x1, y1, x2, y2, color):
    """Dessine le contour d'un rectangle"""
    c = color + (255,) if len(color) == 3 else color
    for x in range(x1, x2 + 1):
        put(img, x, y1, c)
        put(img, x, y2, c)
    for y in range(y1, y2 + 1):
        put(img, x1, y, c)
        put(img, x2, y, c)


def tile_pos(tile_idx):
    """Retourne (x_offset, y_offset) pour un index de tile"""
    col = tile_idx % COLS
    row = tile_idx // COLS
    return col * TILE, row * TILE


# ===== DESSIN DES TILES =====

def draw_herbe(img, tx, ty):
    """Tile 0: Herbe verte avec texture"""
    # Base
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_HERBE)
    # Variations de couleur pour texture
    import random
    random.seed(42)
    for y in range(32):
        for x in range(32):
            r = random.random()
            if r < 0.15:
                put(img, tx + x, ty + y, C_HERBE_CLAIR)
            elif r < 0.25:
                put(img, tx + x, ty + y, C_HERBE_FONCE)
    # Petites touffes d'herbe
    for gy in range(0, 32, 8):
        for gx in range(0, 32, 8):
            # Brin d'herbe
            cx, cy = tx + gx + 3, ty + gy + 5
            put(img, cx, cy, C_HERBE_TRES_FONCE)
            put(img, cx, cy - 1, C_HERBE_FONCE)
            put(img, cx + 1, cy, C_HERBE_CLAIR)


def draw_herbe_haute(img, tx, ty):
    """Tile 1: Herbe haute (zones de rencontre)"""
    # Base plus sombre
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_HAUTE)
    # Motif dense d'herbe
    for y in range(0, 32, 2):
        for x in range(0, 32, 2):
            offset = (y // 2) % 2
            if (x + offset) % 4 < 2:
                put(img, tx + x, ty + y, C_HAUTE_CLAIR)
                put(img, tx + x + 1, ty + y, C_HAUTE_FONCE)
            else:
                put(img, tx + x, ty + y, C_HAUTE_FONCE)
                put(img, tx + x + 1, ty + y, C_HAUTE_DETAIL)
    # Brins individuels plus clairs
    for gx in range(2, 30, 6):
        for gy in range(1, 30, 7):
            put(img, tx + gx, ty + gy, C_HAUTE_DETAIL)
            put(img, tx + gx, ty + gy - 1, C_HERBE_CLAIR)


def draw_chemin(img, tx, ty):
    """Tile 2: Chemin de terre"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_CHEMIN)
    import random
    random.seed(100)
    for y in range(32):
        for x in range(32):
            r = random.random()
            if r < 0.12:
                put(img, tx + x, ty + y, C_CHEMIN_CLAIR)
            elif r < 0.2:
                put(img, tx + x, ty + y, C_CHEMIN_FONCE)
    # Petits cailloux
    for (sx, sy) in [(5, 8), (15, 4), (25, 12), (8, 22), (20, 26), (12, 16)]:
        put(img, tx + sx, ty + sy, C_CHEMIN_FONCE)
        put(img, tx + sx + 1, ty + sy, C_SABLE_FONCE)


def draw_sable(img, tx, ty):
    """Tile 3: Sable / plage"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_SABLE)
    import random
    random.seed(200)
    for y in range(32):
        for x in range(32):
            r = random.random()
            if r < 0.1:
                put(img, tx + x, ty + y, C_SABLE_CLAIR)
            elif r < 0.18:
                put(img, tx + x, ty + y, C_SABLE_FONCE)


def draw_eau(img, tx, ty):
    """Tile 4: Eau avec vagues"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_EAU)
    # Motif de vagues
    import math
    for y in range(32):
        for x in range(32):
            wave = math.sin((x + y * 0.5) * 0.4) * 0.5 + 0.5
            if wave > 0.7:
                put(img, tx + x, ty + y, C_EAU_CLAIR)
            elif wave < 0.3:
                put(img, tx + x, ty + y, C_EAU_FONCE)
    # Vagues blanches
    for wy in range(4, 28, 10):
        for wx in range(0, 32, 2):
            wave_x = int(math.sin(wx * 0.3 + wy) * 3)
            put(img, tx + (wx + wave_x) % 32, ty + wy, C_EAU_CLAIR)


def draw_fleurs(img, tx, ty):
    """Tile 5: Herbe avec fleurs"""
    # Base herbe
    draw_herbe(img, tx, ty)
    # Fleurs colorées
    flowers = [(4, 4, C_FLEUR_ROUGE), (12, 8, C_FLEUR_JAUNE), (24, 6, C_FLEUR_BLANC),
               (8, 18, C_FLEUR_JAUNE), (20, 14, C_FLEUR_ROUGE), (28, 22, C_FLEUR_JAUNE),
               (4, 26, C_FLEUR_BLANC), (16, 28, C_FLEUR_ROUGE)]
    for fx, fy, fc in flowers:
        put(img, tx + fx, ty + fy, fc)
        put(img, tx + fx + 1, ty + fy, fc)
        put(img, tx + fx, ty + fy + 1, fc)
        put(img, tx + fx + 1, ty + fy + 1, fc)
        # Centre jaune pour fleurs non jaunes
        if fc != C_FLEUR_JAUNE:
            put(img, tx + fx, ty + fy, C_FLEUR_JAUNE)


def draw_arbre_haut(img, tx, ty):
    """Tile 8: Canopée d'arbre (haut gauche)"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_HERBE)
    # Canopée ronde
    for y in range(4, 32):
        for x in range(0, 32):
            dx = x - 15.5
            dy = y - 20
            dist = (dx * dx / 256 + dy * dy / 200)
            if dist < 1.0:
                if dist < 0.3:
                    put(img, tx + x, ty + y, C_FEUILLE_CLAIR)
                elif dist < 0.6:
                    put(img, tx + x, ty + y, C_FEUILLE)
                elif dist < 0.85:
                    put(img, tx + x, ty + y, C_FEUILLE_FONCE)
                else:
                    put(img, tx + x, ty + y, C_FEUILLE_TRES_FONCE)
    # Détails de feuilles
    for (lx, ly) in [(8, 12), (20, 10), (14, 8), (6, 20), (22, 18), (12, 24)]:
        put(img, tx + lx, ty + ly, C_FEUILLE_CLAIR)
        put(img, tx + lx + 1, ty + ly, C_FEUILLE_CLAIR)


def draw_arbre_bas(img, tx, ty):
    """Tile 9: Tronc d'arbre (bas gauche)"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_HERBE)
    # Canopée continue du haut
    for y in range(0, 16):
        for x in range(0, 32):
            dx = x - 15.5
            dy = y - (-4)  # Continue from top tile
            dist = (dx * dx / 256 + dy * dy / 200)
            if dist < 1.0:
                if dist < 0.5:
                    put(img, tx + x, ty + y, C_FEUILLE)
                else:
                    put(img, tx + x, ty + y, C_FEUILLE_FONCE)
    # Tronc
    trunk_left = 12
    trunk_right = 19
    for y in range(8, 32):
        for x in range(trunk_left, trunk_right + 1):
            if x == trunk_left or x == trunk_left + 1:
                put(img, tx + x, ty + y, C_TRONC_FONCE)
            elif x >= trunk_right - 1:
                put(img, tx + x, ty + y, C_TRONC_FONCE)
            else:
                put(img, tx + x, ty + y, C_TRONC if y % 4 < 2 else C_TRONC_CLAIR)
    # Ombre du tronc
    for y in range(28, 32):
        for x in range(trunk_left - 2, trunk_right + 3):
            put(img, tx + x, ty + y, C_HERBE_FONCE)


def draw_arbre_haut_r(img, tx, ty):
    """Tile 10: Canopée droite (miroir de 8)"""
    draw_arbre_haut(img, tx, ty)  # Similaire


def draw_arbre_bas_r(img, tx, ty):
    """Tile 11: Tronc droite (miroir de 9)"""
    draw_arbre_bas(img, tx, ty)  # Similaire


def draw_fence_h(img, tx, ty):
    """Tile 12: Clôture horizontale"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_HERBE)
    # Poteau gauche
    fill_rect(img, tx, ty + 8, tx + 3, ty + 24, C_CLOTURE)
    fill_rect(img, tx, ty + 8, tx + 1, ty + 24, C_CLOTURE_CLAIR)
    put(img, tx + 3, ty + 8, C_CLOTURE_FONCE)
    # Barre horizontale haute
    fill_rect(img, tx, ty + 10, tx + 31, ty + 13, C_CLOTURE)
    fill_rect(img, tx, ty + 10, tx + 31, ty + 11, C_CLOTURE_CLAIR)
    # Barre horizontale basse
    fill_rect(img, tx, ty + 18, tx + 31, ty + 21, C_CLOTURE)
    fill_rect(img, tx, ty + 18, tx + 31, ty + 19, C_CLOTURE_CLAIR)
    # Poteau droite
    fill_rect(img, tx + 28, ty + 8, tx + 31, ty + 24, C_CLOTURE)
    fill_rect(img, tx + 28, ty + 8, tx + 29, ty + 24, C_CLOTURE_CLAIR)


def draw_fence_v(img, tx, ty):
    """Tile 13: Clôture verticale"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_HERBE)
    # Poteau vertical au centre
    fill_rect(img, tx + 12, ty, tx + 19, ty + 31, C_CLOTURE)
    fill_rect(img, tx + 12, ty, tx + 14, ty + 31, C_CLOTURE_CLAIR)
    fill_rect(img, tx + 17, ty, tx + 19, ty + 31, C_CLOTURE_FONCE)
    # Barre horizontale haute
    fill_rect(img, tx + 10, ty + 4, tx + 21, ty + 7, C_CLOTURE)
    # Barre horizontale basse
    fill_rect(img, tx + 10, ty + 24, tx + 21, ty + 27, C_CLOTURE)


def draw_buisson(img, tx, ty):
    """Tile 14: Buisson"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_HERBE)
    # Forme de buisson arrondi
    for y in range(4, 28):
        for x in range(4, 28):
            dx = x - 15.5
            dy = y - 15.5
            dist = (dx * dx + dy * dy) / 144
            if dist < 1.0:
                if dist < 0.3:
                    put(img, tx + x, ty + y, C_BUISSON_CLAIR)
                elif dist < 0.7:
                    put(img, tx + x, ty + y, C_BUISSON)
                else:
                    put(img, tx + x, ty + y, C_BUISSON_FONCE)
    # Highlight
    for (hx, hy) in [(10, 8), (8, 12), (12, 10)]:
        put(img, tx + hx, ty + hy, C_HERBE_CLAIR)


def draw_herbe_detail(img, tx, ty):
    """Tile 15: Herbe avec détails"""
    draw_herbe(img, tx, ty)
    # Touffes plus marquées et texturées
    for (gx, gy) in [(6, 6), (18, 4), (10, 16), (24, 12), (4, 24), (20, 22)]:
        for dy in range(-2, 1):
            put(img, tx + gx, ty + gy + dy, C_HERBE_TRES_FONCE)
        put(img, tx + gx - 1, ty + gy - 1, C_HERBE_FONCE)
        put(img, tx + gx + 1, ty + gy - 1, C_HERBE_FONCE)


def draw_toit_g(img, tx, ty):
    """Tile 16: Toit gauche"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_TOIT)
    # Tuiles de toit
    for y in range(0, 32, 4):
        offset = 2 if (y // 4) % 2 else 0
        for x in range(0, 32, 8):
            rx = x + offset
            fill_rect(img, tx + rx, ty + y, tx + rx + 6, ty + y + 2, C_TOIT_CLAIR)
            put(img, tx + rx, ty + y + 3, C_TOIT_FONCE)
            fill_rect(img, tx + rx, ty + y + 3, tx + rx + 6, ty + y + 3, C_TOIT_FONCE)
    # Bord gauche en pente
    for y in range(32):
        slope_x = min(y // 2, 8)
        for x in range(slope_x):
            put(img, tx + x, ty + y, C_TOIT_FONCE)
    # Bordure basse
    fill_rect(img, tx, ty + 30, tx + 31, ty + 31, C_TOIT_FONCE)


def draw_toit_m(img, tx, ty):
    """Tile 17: Toit milieu"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_TOIT)
    # Tuiles
    for y in range(0, 32, 4):
        offset = 2 if (y // 4) % 2 else 0
        for x in range(0, 32, 8):
            rx = (x + offset) % 32
            fill_rect(img, tx + rx, ty + y, tx + min(rx + 6, 31), ty + y + 2, C_TOIT_CLAIR)
            fill_rect(img, tx + rx, ty + y + 3, tx + min(rx + 6, 31), ty + y + 3, C_TOIT_FONCE)
    fill_rect(img, tx, ty + 30, tx + 31, ty + 31, C_TOIT_FONCE)


def draw_toit_d(img, tx, ty):
    """Tile 18: Toit droite"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_TOIT)
    for y in range(0, 32, 4):
        offset = 2 if (y // 4) % 2 else 0
        for x in range(0, 32, 8):
            rx = (x + offset) % 32
            fill_rect(img, tx + rx, ty + y, tx + min(rx + 6, 31), ty + y + 2, C_TOIT_CLAIR)
            fill_rect(img, tx + rx, ty + y + 3, tx + min(rx + 6, 31), ty + y + 3, C_TOIT_FONCE)
    # Bord droite en pente
    for y in range(32):
        slope_x = min(y // 2, 8)
        for x in range(32 - slope_x, 32):
            put(img, tx + x, ty + y, C_TOIT_FONCE)
    fill_rect(img, tx, ty + 30, tx + 31, ty + 31, C_TOIT_FONCE)


def draw_mur_g(img, tx, ty):
    """Tile 19: Mur extérieur gauche"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_MUR_EXT)
    # Motif de briques
    for y in range(0, 32, 8):
        offset = 4 if (y // 8) % 2 else 0
        # Lignes de jointure horizontale
        fill_rect(img, tx, ty + y, tx + 31, ty + y, C_BRIQUE)
        for x in range(offset, 32, 16):
            put(img, tx + x, ty + y + 1, C_BRIQUE)
            put(img, tx + x, ty + y + 2, C_BRIQUE)
            put(img, tx + x, ty + y + 3, C_BRIQUE)
    # Ombre bord gauche
    fill_rect(img, tx, ty, tx + 1, ty + 31, C_MUR_EXT_FONCE)


def draw_mur_m(img, tx, ty):
    """Tile 20: Mur extérieur milieu"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_MUR_EXT)
    for y in range(0, 32, 8):
        offset = 4 if (y // 8) % 2 else 0
        fill_rect(img, tx, ty + y, tx + 31, ty + y, C_BRIQUE)
        for x in range(offset, 32, 16):
            put(img, tx + x, ty + y + 1, C_BRIQUE)
            put(img, tx + x, ty + y + 2, C_BRIQUE)
            put(img, tx + x, ty + y + 3, C_BRIQUE)


def draw_mur_d(img, tx, ty):
    """Tile 21: Mur extérieur droite"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_MUR_EXT)
    for y in range(0, 32, 8):
        offset = 4 if (y // 8) % 2 else 0
        fill_rect(img, tx, ty + y, tx + 31, ty + y, C_BRIQUE)
        for x in range(offset, 32, 16):
            put(img, tx + x, ty + y + 1, C_BRIQUE)
            put(img, tx + x, ty + y + 2, C_BRIQUE)
    # Ombre bord droite
    fill_rect(img, tx + 30, ty, tx + 31, ty + 31, C_MUR_EXT_FONCE)


def draw_porte(img, tx, ty):
    """Tile 22: Porte extérieure"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_MUR_EXT)
    # Cadre de porte
    fill_rect(img, tx + 6, ty + 2, tx + 25, ty + 31, C_PORTE_BOIS_FONCE)
    fill_rect(img, tx + 8, ty + 4, tx + 23, ty + 31, C_PORTE_BOIS)
    # Panneau haut
    fill_rect(img, tx + 10, ty + 6, tx + 21, ty + 14, C_PORTE_BOIS_CLAIR)
    draw_outline_rect(img, tx + 10, ty + 6, tx + 21, ty + 14, C_PORTE_BOIS_FONCE)
    # Panneau bas
    fill_rect(img, tx + 10, ty + 17, tx + 21, ty + 29, C_PORTE_BOIS_CLAIR)
    draw_outline_rect(img, tx + 10, ty + 17, tx + 21, ty + 29, C_PORTE_BOIS_FONCE)
    # Poignée
    put(img, tx + 19, ty + 18, (224, 200, 96))
    put(img, tx + 20, ty + 18, (224, 200, 96))
    put(img, tx + 19, ty + 19, (192, 168, 64))
    put(img, tx + 20, ty + 19, (192, 168, 64))


def draw_fenetre_ext(img, tx, ty):
    """Tile 23: Fenêtre extérieure"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_MUR_EXT)
    # Briques de fond
    for y in range(0, 32, 8):
        fill_rect(img, tx, ty + y, tx + 31, ty + y, C_BRIQUE)
    # Cadre de fenêtre
    fill_rect(img, tx + 4, ty + 4, tx + 27, ty + 27, C_CADRE)
    # Vitre
    fill_rect(img, tx + 6, ty + 6, tx + 25, ty + 25, C_VITRE)
    # Croisillons
    fill_rect(img, tx + 15, ty + 6, tx + 16, ty + 25, C_CADRE)
    fill_rect(img, tx + 6, ty + 15, tx + 25, ty + 16, C_CADRE)
    # Reflets
    fill_rect(img, tx + 8, ty + 8, tx + 12, ty + 10, C_VITRE_FONCE)
    fill_rect(img, tx + 8, ty + 8, tx + 10, ty + 9, (224, 240, 255))


# ===== INTÉRIEUR =====

def draw_sol_int(img, tx, ty):
    """Tile 24: Sol intérieur parquet"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Motif de planches
    for y in range(0, 32, 4):
        offset = 8 if (y // 4) % 2 else 0
        # Jointures horizontales
        fill_rect(img, tx, ty + y, tx + 31, ty + y, C_PARQUET_FONCE)
        for x in range(offset, 32, 16):
            # Jointures verticales
            put(img, tx + x, ty + y + 1, C_PARQUET_FONCE)
            put(img, tx + x, ty + y + 2, C_PARQUET_FONCE)
            put(img, tx + x, ty + y + 3, C_PARQUET_FONCE)
        # Variation de couleur des planches
        for x in range(32):
            plank = ((x + offset) // 16) % 2
            if plank == 0:
                for dy in range(1, 4):
                    if (x + y) % 7 == 0:
                        put(img, tx + x, ty + y + dy, C_PARQUET_CLAIR)


def draw_mur_int(img, tx, ty):
    """Tile 25: Mur intérieur"""
    # Mur principal
    fill_rect(img, tx, ty, tx + 31, ty + 27, C_MUR_INT)
    # Cadrage supérieur
    fill_rect(img, tx, ty, tx + 31, ty + 1, C_MUR_INT_FONCE)
    # Motif subtil
    for y in range(2, 26):
        for x in range(32):
            if (x + y) % 12 == 0:
                put(img, tx + x, ty + y, C_MUR_INT_CLAIR)
    # Plinthe (bordure basse)
    fill_rect(img, tx, ty + 28, tx + 31, ty + 29, C_PLINTHE)
    fill_rect(img, tx, ty + 30, tx + 31, ty + 31, C_PLINTHE_FONCE)
    # Ligne séparatrice mur/plinthe
    fill_rect(img, tx, ty + 27, tx + 31, ty + 27, C_MUR_INT_FONCE)


def draw_comptoir(img, tx, ty):
    """Tile 26: Comptoir / Bureau"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Surface du comptoir
    fill_rect(img, tx + 2, ty + 4, tx + 29, ty + 14, C_TABLE_BOIS_CLAIR)
    draw_outline_rect(img, tx + 2, ty + 4, tx + 29, ty + 14, C_TABLE_BOIS_FONCE)
    # Face avant
    fill_rect(img, tx + 2, ty + 15, tx + 29, ty + 31, C_TABLE_BOIS)
    fill_rect(img, tx + 2, ty + 15, tx + 29, ty + 16, C_TABLE_BOIS_FONCE)
    fill_rect(img, tx + 4, ty + 18, tx + 27, ty + 28, C_TABLE_BOIS_FONCE)
    # Pieds
    fill_rect(img, tx + 4, ty + 29, tx + 6, ty + 31, C_TABLE_BOIS_FONCE)
    fill_rect(img, tx + 25, ty + 29, tx + 27, ty + 31, C_TABLE_BOIS_FONCE)


def draw_machine_soin(img, tx, ty):
    """Tile 27: Machine de soin Centre Pokémon"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_CARRELAGE)
    # Machine
    fill_rect(img, tx + 4, ty + 4, tx + 27, ty + 28, C_MACHINE)
    draw_outline_rect(img, tx + 4, ty + 4, tx + 27, ty + 28, C_MACHINE_FONCE)
    # Écran
    fill_rect(img, tx + 8, ty + 6, tx + 23, ty + 14, C_PC_ECRAN)
    fill_rect(img, tx + 8, ty + 6, tx + 15, ty + 10, C_PC_ECRAN_CLAIR)
    # Croix rouge
    fill_rect(img, tx + 13, ty + 17, tx + 18, ty + 26, C_MACHINE_ROUGE)
    fill_rect(img, tx + 10, ty + 20, tx + 21, ty + 23, C_MACHINE_ROUGE)
    # LED verte
    put(img, tx + 24, ty + 8, C_MACHINE_VERT)
    put(img, tx + 25, ty + 8, C_MACHINE_VERT)
    # Emplacement Poké Ball
    fill_rect(img, tx + 10, ty + 15, tx + 21, ty + 16, (64, 64, 72))


def draw_etagere(img, tx, ty):
    """Tile 28: Étagère avec livres"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_MUR_INT)
    # Structure étagère
    fill_rect(img, tx + 2, ty + 2, tx + 29, ty + 29, C_ETAGERE)
    # Étagères horizontales
    for sy in [2, 10, 18, 26]:
        fill_rect(img, tx + 2, ty + sy, tx + 29, ty + sy + 1, C_ETAGERE_CLAIR)
    # Livres rangée 1
    colors1 = [C_LIVRE_R, C_LIVRE_B, C_LIVRE_V, C_LIVRE_R, C_LIVRE_J, C_LIVRE_B]
    for i, c in enumerate(colors1):
        bx = 4 + i * 4
        fill_rect(img, tx + bx, ty + 4, tx + bx + 2, ty + 9, c)
    # Livres rangée 2
    colors2 = [C_LIVRE_V, C_LIVRE_J, C_LIVRE_R, C_LIVRE_B, C_LIVRE_V, C_LIVRE_R]
    for i, c in enumerate(colors2):
        bx = 4 + i * 4
        fill_rect(img, tx + bx, ty + 12, tx + bx + 2, ty + 17, c)
    # Livres rangée 3
    colors3 = [C_LIVRE_B, C_LIVRE_R, C_LIVRE_J, C_LIVRE_V, C_LIVRE_B, C_LIVRE_J]
    for i, c in enumerate(colors3):
        bx = 4 + i * 4
        fill_rect(img, tx + bx, ty + 20, tx + bx + 2, ty + 25, c)


def draw_tapis(img, tx, ty):
    """Tile 29: Tapis (bleu style FRLG, pas rouge)"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Tapis bleu avec bordure
    fill_rect(img, tx + 1, ty + 1, tx + 30, ty + 30, C_TAPIS)
    # Bordure décorative
    fill_rect(img, tx + 1, ty + 1, tx + 30, ty + 2, C_TAPIS_BORD)
    fill_rect(img, tx + 1, ty + 29, tx + 30, ty + 30, C_TAPIS_BORD)
    fill_rect(img, tx + 1, ty + 1, tx + 2, ty + 30, C_TAPIS_BORD)
    fill_rect(img, tx + 29, ty + 1, tx + 30, ty + 30, C_TAPIS_BORD)
    # Motif central discret
    for y in range(5, 27, 4):
        for x in range(5, 27, 4):
            put(img, tx + x, ty + y, C_TAPIS_MOTIF)
            put(img, tx + x + 1, ty + y, C_TAPIS_CLAIR)


def draw_sol_carrelage(img, tx, ty):
    """Tile 30: Sol carrelé (centre pokémon, boutique)"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_CARRELAGE)
    # Jointures
    fill_rect(img, tx + 15, ty, tx + 16, ty + 31, C_CARRELAGE_JOINT)
    fill_rect(img, tx, ty + 15, tx + 31, ty + 16, C_CARRELAGE_JOINT)
    # Coins
    put(img, tx, ty, C_CARRELAGE_JOINT)
    put(img, tx + 31, ty, C_CARRELAGE_JOINT)
    put(img, tx, ty + 31, C_CARRELAGE_JOINT)
    put(img, tx + 31, ty + 31, C_CARRELAGE_JOINT)
    # Reflet léger
    fill_rect(img, tx + 2, ty + 2, tx + 6, ty + 4, (232, 240, 248))


def draw_mur_motif(img, tx, ty):
    """Tile 31: Mur avec motif décoratif"""
    draw_mur_int(img, tx, ty)
    # Motif losanges
    for y in range(4, 24, 8):
        for x in range(4, 28, 8):
            for d in range(3):
                put(img, tx + x + d, ty + y - d + 2, C_MUR_INT_FONCE)
                put(img, tx + x + d, ty + y + d + 2, C_MUR_INT_FONCE)
                put(img, tx + x - d + 4, ty + y - d + 2, C_MUR_INT_FONCE)
                put(img, tx + x - d + 4, ty + y + d + 2, C_MUR_INT_FONCE)


# ===== MOBILIER (Ligne 4) =====

def draw_lit_tete(img, tx, ty):
    """Tile 32: Lit - tête (oreiller)"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Cadre du lit
    fill_rect(img, tx + 2, ty + 2, tx + 29, ty + 29, C_LIT_BOIS)
    fill_rect(img, tx + 2, ty + 2, tx + 29, ty + 4, C_LIT_BOIS_FONCE)  # Tête de lit
    # Oreiller
    fill_rect(img, tx + 5, ty + 6, tx + 26, ty + 16, C_OREILLER)
    fill_rect(img, tx + 5, ty + 14, tx + 26, ty + 16, C_OREILLER_OMBRE)
    draw_outline_rect(img, tx + 5, ty + 6, tx + 26, ty + 16, C_OREILLER_OMBRE)
    # Pli au milieu de l'oreiller
    fill_rect(img, tx + 15, ty + 7, tx + 16, ty + 15, C_OREILLER_OMBRE)
    # Couverture début
    fill_rect(img, tx + 4, ty + 17, tx + 27, ty + 29, C_COUVERTURE)
    fill_rect(img, tx + 4, ty + 17, tx + 27, ty + 19, C_COUVERTURE_CLAIR)
    # Motif couverture
    for x in range(6, 26, 4):
        put(img, tx + x, ty + 22, C_COUVERTURE_CLAIR)
        put(img, tx + x, ty + 26, C_COUVERTURE_FONCE)


def draw_lit_pied(img, tx, ty):
    """Tile 33: Lit - pied (couverture)"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Cadre du lit
    fill_rect(img, tx + 2, ty, tx + 29, ty + 27, C_LIT_BOIS)
    # Couverture
    fill_rect(img, tx + 4, ty, tx + 27, ty + 24, C_COUVERTURE)
    # Motif couverture
    for y in range(2, 22, 4):
        for x in range(6, 26, 4):
            put(img, tx + x, ty + y, C_COUVERTURE_CLAIR)
    for y in range(4, 24, 4):
        for x in range(8, 26, 4):
            put(img, tx + x, ty + y, C_COUVERTURE_FONCE)
    # Bord de couverture plié
    fill_rect(img, tx + 4, ty + 22, tx + 27, ty + 24, C_COUVERTURE_CLAIR)
    fill_rect(img, tx + 4, ty + 24, tx + 27, ty + 25, C_COUVERTURE_FONCE)
    # Pied du lit
    fill_rect(img, tx + 2, ty + 25, tx + 29, ty + 27, C_LIT_BOIS_FONCE)
    # Pieds
    fill_rect(img, tx + 3, ty + 28, tx + 5, ty + 31, C_LIT_BOIS_FONCE)
    fill_rect(img, tx + 26, ty + 28, tx + 28, ty + 31, C_LIT_BOIS_FONCE)


def draw_tv(img, tx, ty):
    """Tile 34: Téléviseur"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Meuble TV
    fill_rect(img, tx + 2, ty + 18, tx + 29, ty + 31, C_TABLE_BOIS)
    fill_rect(img, tx + 2, ty + 18, tx + 29, ty + 19, C_TABLE_BOIS_CLAIR)
    # Corps de la TV
    fill_rect(img, tx + 4, ty + 2, tx + 27, ty + 18, C_TV_CORPS)
    draw_outline_rect(img, tx + 4, ty + 2, tx + 27, ty + 18, NOIR)
    # Écran
    fill_rect(img, tx + 6, ty + 4, tx + 25, ty + 15, C_TV_ECRAN)
    # Reflet sur l'écran
    fill_rect(img, tx + 7, ty + 5, tx + 12, ty + 8, C_TV_ECRAN_REFLET)
    put(img, tx + 8, ty + 5, (80, 88, 112))
    # Boutons
    put(img, tx + 24, ty + 16, C_MACHINE_ROUGE)
    put(img, tx + 22, ty + 16, C_MACHINE_VERT)
    # Antenne
    put(img, tx + 12, ty + 1, NOIR)
    put(img, tx + 11, ty, NOIR)
    put(img, tx + 20, ty + 1, NOIR)
    put(img, tx + 21, ty, NOIR)


def draw_pc(img, tx, ty):
    """Tile 35: Ordinateur PC"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_MUR_INT)
    # Bureau
    fill_rect(img, tx + 2, ty + 20, tx + 29, ty + 31, C_TABLE_BOIS)
    fill_rect(img, tx + 2, ty + 20, tx + 29, ty + 21, C_TABLE_BOIS_CLAIR)
    # Moniteur
    fill_rect(img, tx + 6, ty + 2, tx + 25, ty + 18, C_PC_CORPS)
    draw_outline_rect(img, tx + 6, ty + 2, tx + 25, ty + 18, C_PC_CORPS_FONCE)
    # Écran
    fill_rect(img, tx + 8, ty + 4, tx + 23, ty + 15, C_PC_ECRAN)
    fill_rect(img, tx + 9, ty + 5, tx + 14, ty + 8, C_PC_ECRAN_CLAIR)
    # Pied moniteur
    fill_rect(img, tx + 13, ty + 18, tx + 18, ty + 20, C_PC_CORPS_FONCE)
    # Clavier
    fill_rect(img, tx + 8, ty + 22, tx + 23, ty + 26, C_PC_CLAVIER)
    # Touches
    for kx in range(9, 23, 2):
        put(img, tx + kx, ty + 23, (96, 96, 104))
        put(img, tx + kx, ty + 25, (96, 96, 104))
    # Souris
    fill_rect(img, tx + 25, ty + 23, tx + 27, ty + 26, C_PC_CORPS)


def draw_plante(img, tx, ty):
    """Tile 36: Plante d'intérieur"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Pot
    fill_rect(img, tx + 8, ty + 20, tx + 23, ty + 31, C_POT)
    fill_rect(img, tx + 10, ty + 18, tx + 21, ty + 20, C_POT)  # Rebord
    fill_rect(img, tx + 10, ty + 18, tx + 21, ty + 19, C_POT_FONCE)
    # Terre
    fill_rect(img, tx + 10, ty + 20, tx + 21, ty + 21, C_POT_TERRE)
    # Ombre pot
    fill_rect(img, tx + 20, ty + 20, tx + 23, ty + 31, C_POT_FONCE)
    # Feuilles
    leaves = [
        (15, 4, 8), (8, 8, 6), (22, 6, 6), (12, 12, 5),
        (20, 10, 5), (10, 16, 4), (22, 14, 4)
    ]
    for lx, ly, size in leaves:
        for d in range(size):
            for e in range(max(1, size - d)):
                px, py = tx + lx + d - size // 2, ty + ly + e - d // 2
                if 0 <= px - tx < 32 and 0 <= py - ty < 32:
                    if d < size // 3:
                        put(img, px, py, C_PLANTE_FONCE)
                    elif d < 2 * size // 3:
                        put(img, px, py, C_PLANTE)
                    else:
                        put(img, px, py, C_PLANTE_CLAIR)


def draw_escalier_up(img, tx, ty):
    """Tile 37: Escalier montant"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Cadre escalier
    fill_rect(img, tx + 2, ty + 2, tx + 29, ty + 29, C_ESCALIER_FONCE)
    # Marches
    for i in range(5):
        y_start = ty + 2 + i * 5
        shade = max(0, min(255, 152 + i * 12))
        color = (shade, shade - 32, shade - 72)
        fill_rect(img, tx + 4, y_start, tx + 27, y_start + 3, color)
        # Bord de marche (highlight)
        hl = (min(255, shade + 30), min(255, shade - 8), min(255, shade - 48))
        fill_rect(img, tx + 4, y_start, tx + 27, y_start, hl)
        # Ombre de marche
        sh = (max(0, shade - 40), max(0, shade - 72), max(0, shade - 112))
        fill_rect(img, tx + 4, y_start + 3, tx + 27, y_start + 3, sh)
    # Rampe gauche
    fill_rect(img, tx + 2, ty + 2, tx + 3, ty + 29, C_ESCALIER_OMBRE)
    # Rampe droite
    fill_rect(img, tx + 28, ty + 2, tx + 29, ty + 29, C_ESCALIER_OMBRE)
    # Flèche montante
    for d in range(4):
        put(img, tx + 15 - d, ty + 28 - d * 2, (240, 240, 248))
        put(img, tx + 16 + d, ty + 28 - d * 2, (240, 240, 248))
        put(img, tx + 15 - d, ty + 27 - d * 2, (240, 240, 248))
        put(img, tx + 16 + d, ty + 27 - d * 2, (240, 240, 248))


def draw_escalier_down(img, tx, ty):
    """Tile 38: Escalier descendant"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    fill_rect(img, tx + 2, ty + 2, tx + 29, ty + 29, C_ESCALIER_FONCE)
    # Marches (direction inversée)
    for i in range(5):
        y_start = ty + 2 + i * 5
        shade = max(0, min(255, 200 - i * 12))
        color = (shade, shade - 32, max(0, shade - 72))
        fill_rect(img, tx + 4, y_start, tx + 27, y_start + 3, color)
        hl = (min(255, shade + 30), min(255, shade - 8), max(0, min(255, shade - 48)))
        fill_rect(img, tx + 4, y_start, tx + 27, y_start, hl)
    fill_rect(img, tx + 2, ty + 2, tx + 3, ty + 29, C_ESCALIER_OMBRE)
    fill_rect(img, tx + 28, ty + 2, tx + 29, ty + 29, C_ESCALIER_OMBRE)
    # Flèche descendante
    for d in range(4):
        put(img, tx + 15 - d, ty + 22 + d * 2, (240, 240, 248))
        put(img, tx + 16 + d, ty + 22 + d * 2, (240, 240, 248))


def draw_paillasson(img, tx, ty):
    """Tile 39: Paillasson"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Paillasson
    fill_rect(img, tx + 4, ty + 8, tx + 27, ty + 24, C_PAILL)
    fill_rect(img, tx + 4, ty + 8, tx + 27, ty + 9, C_PAILL_CLAIR)
    fill_rect(img, tx + 4, ty + 23, tx + 27, ty + 24, C_PAILL_FONCE)
    # Bordure
    draw_outline_rect(img, tx + 4, ty + 8, tx + 27, ty + 24, C_PAILL_FONCE)
    # Motif "WELCOME" style (lignes décoratives)
    for x in range(6, 26, 3):
        fill_rect(img, tx + x, ty + 12, tx + x + 1, ty + 20, C_PAILL_FONCE)
    for y in range(12, 21, 4):
        fill_rect(img, tx + 6, ty + y, tx + 25, ty + y, C_PAILL_CLAIR)


# ===== MOBILIER AVANCÉ (Ligne 5) =====

def draw_porte_int(img, tx, ty):
    """Tile 40: Porte intérieure"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Cadre
    fill_rect(img, tx + 4, ty, tx + 27, ty + 31, C_PORTE_BOIS_FONCE)
    # Panneau de porte
    fill_rect(img, tx + 6, ty + 2, tx + 25, ty + 31, C_PORTE_BOIS)
    # Panneau haut
    fill_rect(img, tx + 8, ty + 4, tx + 23, ty + 14, C_PORTE_BOIS_CLAIR)
    draw_outline_rect(img, tx + 8, ty + 4, tx + 23, ty + 14, C_PORTE_BOIS_FONCE)
    # Panneau bas
    fill_rect(img, tx + 8, ty + 17, tx + 23, ty + 29, C_PORTE_BOIS_CLAIR)
    draw_outline_rect(img, tx + 8, ty + 17, tx + 23, ty + 29, C_PORTE_BOIS_FONCE)
    # Poignée
    fill_rect(img, tx + 21, ty + 18, tx + 23, ty + 20, (224, 200, 96))
    put(img, tx + 22, ty + 19, (255, 224, 128))


def draw_fenetre_int(img, tx, ty):
    """Tile 41: Fenêtre intérieure (vue depuis l'intérieur)"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_MUR_INT)
    # Cadre de fenêtre
    fill_rect(img, tx + 3, ty + 3, tx + 28, ty + 26, C_CADRE)
    fill_rect(img, tx + 3, ty + 3, tx + 28, ty + 4, C_MUR_INT_FONCE)  # ombre haut
    # Vitre — ciel bleu
    fill_rect(img, tx + 5, ty + 5, tx + 26, ty + 24, C_VITRE)
    # Croisillon
    fill_rect(img, tx + 15, ty + 5, tx + 16, ty + 24, C_CADRE)
    fill_rect(img, tx + 5, ty + 14, tx + 26, ty + 15, C_CADRE)
    # Reflets sur vitre
    fill_rect(img, tx + 7, ty + 7, tx + 11, ty + 9, (200, 224, 248))
    # Nuage visible
    fill_rect(img, tx + 18, ty + 8, tx + 24, ty + 10, (240, 248, 255))
    fill_rect(img, tx + 19, ty + 7, tx + 23, ty + 7, (240, 248, 255))
    # Rideaux
    fill_rect(img, tx + 3, ty + 5, tx + 4, ty + 24, (232, 216, 176))
    fill_rect(img, tx + 27, ty + 5, tx + 28, ty + 24, (232, 216, 176))
    # Plinthe sous fenêtre
    fill_rect(img, tx, ty + 27, tx + 31, ty + 31, C_PLINTHE)


def draw_sol_bois_fonce(img, tx, ty):
    """Tile 42: Sol bois foncé"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET_FONCE)
    for y in range(0, 32, 4):
        offset = 8 if (y // 4) % 2 else 0
        fill_rect(img, tx, ty + y, tx + 31, ty + y, C_PARQUET_TRES_FONCE)
        for x in range(offset, 32, 16):
            put(img, tx + x, ty + y + 1, C_PARQUET_TRES_FONCE)
            put(img, tx + x, ty + y + 2, C_PARQUET_TRES_FONCE)
            put(img, tx + x, ty + y + 3, C_PARQUET_TRES_FONCE)


def draw_mur_ext_fenetre(img, tx, ty):
    """Tile 43: Mur extérieur avec fenêtre (vu de l'intérieur)"""
    # Mur intérieur complet
    draw_mur_int(img, tx, ty)
    # Petite fenêtre
    fill_rect(img, tx + 8, ty + 4, tx + 23, ty + 18, C_CADRE)
    fill_rect(img, tx + 10, ty + 6, tx + 21, ty + 16, C_VITRE)
    fill_rect(img, tx + 15, ty + 6, tx + 16, ty + 16, C_CADRE)
    # Reflet
    fill_rect(img, tx + 11, ty + 7, tx + 13, ty + 9, (224, 240, 255))


def draw_table(img, tx, ty):
    """Tile 44: Table"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Plateau
    fill_rect(img, tx + 2, ty + 6, tx + 29, ty + 16, C_TABLE_BOIS_CLAIR)
    fill_rect(img, tx + 2, ty + 6, tx + 29, ty + 7, (208, 176, 128))  # highlight
    draw_outline_rect(img, tx + 2, ty + 6, tx + 29, ty + 16, C_TABLE_BOIS_FONCE)
    # Face avant
    fill_rect(img, tx + 2, ty + 17, tx + 29, ty + 20, C_TABLE_BOIS)
    fill_rect(img, tx + 2, ty + 17, tx + 29, ty + 17, C_TABLE_BOIS_FONCE)
    # Pieds
    fill_rect(img, tx + 4, ty + 21, tx + 6, ty + 31, C_TABLE_BOIS_FONCE)
    fill_rect(img, tx + 25, ty + 21, tx + 27, ty + 31, C_TABLE_BOIS_FONCE)
    # Objet sur la table (tasse)
    fill_rect(img, tx + 12, ty + 3, tx + 16, ty + 6, (248, 248, 248))
    put(img, tx + 17, ty + 4, (200, 200, 200))


def draw_chaise(img, tx, ty):
    """Tile 45: Chaise"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Dossier
    fill_rect(img, tx + 8, ty + 2, tx + 23, ty + 14, C_CHAISE)
    fill_rect(img, tx + 8, ty + 2, tx + 23, ty + 3, C_CHAISE_CLAIR)
    draw_outline_rect(img, tx + 8, ty + 2, tx + 23, ty + 14, C_CHAISE_FONCE)
    # Panneau dossier
    fill_rect(img, tx + 10, ty + 5, tx + 21, ty + 12, C_CHAISE_CLAIR)
    # Assise
    fill_rect(img, tx + 6, ty + 15, tx + 25, ty + 20, C_CHAISE)
    fill_rect(img, tx + 6, ty + 15, tx + 25, ty + 16, C_CHAISE_CLAIR)
    draw_outline_rect(img, tx + 6, ty + 15, tx + 25, ty + 20, C_CHAISE_FONCE)
    # Pieds
    fill_rect(img, tx + 8, ty + 21, tx + 10, ty + 31, C_CHAISE_FONCE)
    fill_rect(img, tx + 21, ty + 21, tx + 23, ty + 31, C_CHAISE_FONCE)


def draw_poster(img, tx, ty):
    """Tile 46: Poster sur le mur"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_MUR_INT)
    # Cadre du poster
    fill_rect(img, tx + 4, ty + 2, tx + 27, ty + 26, C_POSTER_CADRE)
    # Image du poster (carte du monde Pokémon simplifié)
    fill_rect(img, tx + 6, ty + 4, tx + 25, ty + 24, C_POSTER_FOND)
    # Dessin simplifié dans le poster (une Poké Ball)
    # Moitié rouge
    for y in range(8, 14):
        for x in range(10, 22):
            dx = x - 15.5
            dy = y - 14
            if dx * dx + dy * dy < 42:
                put(img, tx + x, ty + y, (224, 56, 56))
    # Moitié blanche
    for y in range(14, 20):
        for x in range(10, 22):
            dx = x - 15.5
            dy = y - 14
            if dx * dx + dy * dy < 42:
                put(img, tx + x, ty + y, (240, 240, 240))
    # Ligne centrale
    fill_rect(img, tx + 10, ty + 13, tx + 21, ty + 14, NOIR)
    # Bouton central
    fill_rect(img, tx + 14, ty + 12, tx + 17, ty + 15, (240, 240, 240))
    draw_outline_rect(img, tx + 14, ty + 12, tx + 17, ty + 15, NOIR)
    # Plinthe
    fill_rect(img, tx, ty + 28, tx + 31, ty + 31, C_PLINTHE)


def draw_poubelle(img, tx, ty):
    """Tile 47: Poubelle"""
    fill_rect(img, tx, ty, tx + 31, ty + 31, C_PARQUET)
    # Corps
    fill_rect(img, tx + 8, ty + 10, tx + 23, ty + 29, C_POUB)
    fill_rect(img, tx + 20, ty + 10, tx + 23, ty + 29, C_POUB_FONCE)
    # Couvercle
    fill_rect(img, tx + 6, ty + 6, tx + 25, ty + 10, C_POUB_COUVERCLE)
    fill_rect(img, tx + 6, ty + 6, tx + 25, ty + 7, (208, 216, 224))
    # Poignée couvercle
    fill_rect(img, tx + 14, ty + 4, tx + 17, ty + 6, C_POUB_FONCE)
    # Bande décorative
    fill_rect(img, tx + 8, ty + 18, tx + 23, ty + 19, C_POUB_FONCE)
    # Ombre au sol
    fill_rect(img, tx + 10, ty + 30, tx + 25, ty + 31, C_PARQUET_FONCE)


# ===== ASSEMBLAGE =====

def main():
    img = Image.new("RGBA", (WIDTH, HEIGHT), TRANSPARENT)

    # Tableau de correspondance tile_index → fonction de dessin
    draw_funcs = {
        0: draw_herbe,
        1: draw_herbe_haute,
        2: draw_chemin,
        3: draw_sable,
        4: draw_eau,
        5: draw_fleurs,
        # 6, 7: réservés (vides)
        8: draw_arbre_haut,
        9: draw_arbre_bas,
        10: draw_arbre_haut_r,
        11: draw_arbre_bas_r,
        12: draw_fence_h,
        13: draw_fence_v,
        14: draw_buisson,
        15: draw_herbe_detail,
        16: draw_toit_g,
        17: draw_toit_m,
        18: draw_toit_d,
        19: draw_mur_g,
        20: draw_mur_m,
        21: draw_mur_d,
        22: draw_porte,
        23: draw_fenetre_ext,
        24: draw_sol_int,
        25: draw_mur_int,
        26: draw_comptoir,
        27: draw_machine_soin,
        28: draw_etagere,
        29: draw_tapis,
        30: draw_sol_carrelage,
        31: draw_mur_motif,
        32: draw_lit_tete,
        33: draw_lit_pied,
        34: draw_tv,
        35: draw_pc,
        36: draw_plante,
        37: draw_escalier_up,
        38: draw_escalier_down,
        39: draw_paillasson,
        40: draw_porte_int,
        41: draw_fenetre_int,
        42: draw_sol_bois_fonce,
        43: draw_mur_ext_fenetre,
        44: draw_table,
        45: draw_chaise,
        46: draw_poster,
        47: draw_poubelle,
    }

    for idx, func in draw_funcs.items():
        tx, ty = tile_pos(idx)
        func(img, tx, ty)

    # Remplir les tiles vides (6, 7, 48-63) avec du transparent
    for idx in range(64):
        if idx not in draw_funcs:
            tx, ty = tile_pos(idx)
            fill_rect(img, tx, ty, tx + 31, ty + 31, TRANSPARENT)

    output = "assets/sprites/tilesets/tileset_outdoor.png"
    img.save(output)
    print(f"Tileset FRLG généré: {img.size} — {len(draw_funcs)} tiles dessinées")

    # Stats de qualité
    for idx in sorted(draw_funcs.keys()):
        tx, ty = tile_pos(idx)
        tile = img.crop((tx, ty, tx + 32, ty + 32))
        colors = len(set(tile.getdata()))
        print(f"  Tile {idx:2d}: {colors:3d} couleurs uniques")


if __name__ == "__main__":
    main()
