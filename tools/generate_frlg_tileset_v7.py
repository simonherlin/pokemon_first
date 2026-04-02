#!/usr/bin/env python3
"""
Générateur de tileset FRLG — v7 Bright & Colorful
Produit 8×6 = 48 tiles de 32×32px
Palette LUMINEUSE fidèle à FireRed/LeafGreen (pas de gris terne !)
"""

from PIL import Image, ImageDraw
import os, math, random

random.seed(42)

TILE = 32
COLS = 8
ROWS = 6
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "tilesets", "tileset_outdoor.png")

# ══════════════════════════════════════════════════════════════
# PALETTE FRLG LUMINEUSE — extraite de captures réelles du jeu
# Chaque matière a 3-5 tons du clair au foncé
# ══════════════════════════════════════════════════════════════

# --- HERBE ---
GR1 = (40, 168, 56)    # herbe base (vert vif FRLG)
GR2 = (56, 192, 72)    # herbe clair
GR3 = (32, 144, 48)    # herbe ombre
GR4 = (72, 208, 88)    # herbe highlight
GR5 = (24, 120, 40)    # herbe très foncé

# --- HERBE HAUTE ---
HG1 = (32, 152, 48)    # base
HG2 = (24, 128, 36)    # foncé
HG3 = (48, 176, 64)    # clair
HG4 = (16, 104, 28)    # très foncé

# --- CHEMIN ---
PT1 = (224, 208, 168)  # chemin clair (sable/terre FRLG)
PT2 = (208, 192, 152)  # base
PT3 = (192, 176, 136)  # ombre
PT4 = (240, 224, 184)  # highlight

# --- SABLE ---
SA1 = (248, 232, 184)  # sable clair FRLG
SA2 = (240, 224, 168)  # base
SA3 = (232, 216, 152)  # ombre
SA4 = (248, 240, 200)  # highlight

# --- EAU ---
WA1 = (48, 120, 232)   # eau profonde
WA2 = (72, 152, 248)   # eau base
WA3 = (96, 176, 255)   # eau reflet
WA4 = (128, 200, 255)  # mousse/écume
WA5 = (32, 96, 208)    # eau très profonde

# --- FLEURS ---
FL_R = (248, 64, 80)   # rouge
FL_Y = (255, 224, 48)  # jaune
FL_W = (255, 252, 240) # blanc
FL_P = (248, 128, 168) # rose

# --- ARBRE FEUILLAGE ---
LF1 = (24, 112, 32)    # canopée foncée
LF2 = (40, 144, 48)    # canopée base
LF3 = (56, 168, 64)    # canopée claire
LF4 = (72, 192, 80)    # canopée highlight
LF5 = (16, 88, 24)     # canopée très foncée

# --- ARBRE TRONC ---
TK1 = (96, 64, 32)     # tronc foncé
TK2 = (128, 88, 48)    # tronc base
TK3 = (152, 112, 64)   # tronc clair
TK4 = (72, 48, 24)     # tronc ombre

# --- CLÔTURE BOIS ---
FN1 = (200, 168, 112)  # bois clair
FN2 = (176, 144, 88)   # bois base
FN3 = (152, 120, 72)   # bois foncé

# --- TOIT MAISON (rouge-brun FRLG) ---
RF1 = (208, 72, 48)    # toit principal
RF2 = (184, 56, 36)    # toit ombre
RF3 = (232, 96, 64)    # toit clair
RF4 = (160, 44, 28)    # toit très foncé

# --- MUR EXTÉRIEUR MAISON (crème) ---
XW1 = (248, 240, 216)  # mur extérieur clair
XW2 = (240, 232, 200)  # mur base
XW3 = (224, 216, 184)  # mur ombre

# --- PORTE BOIS ---
DR1 = (168, 112, 56)   # porte base
DR2 = (144, 96, 48)    # porte foncé
DR3 = (192, 136, 72)   # porte clair

# --- FENÊTRE EXTÉRIEURE ---
WN1 = (136, 200, 248)  # vitre (bleu ciel)
WN2 = (104, 176, 240)  # vitre foncée
WN3 = (255, 255, 255)  # cadre blanc

# ══════ INTÉRIEUR (LUMINEUX !) ══════

# --- MUR INTÉRIEUR (crème chaud, PAS gris !!) ---
IW1 = (252, 244, 224)  # mur clair (presque blanc chaud)
IW2 = (244, 236, 208)  # mur base
IW3 = (232, 224, 196)  # mur ombre
IW4 = (200, 176, 136)  # plinthe bois

# --- SOL INTÉRIEUR (parquet chaud clair) ---
IF1 = (232, 200, 152)  # parquet clair
IF2 = (216, 184, 136)  # parquet base
IF3 = (200, 168, 120)  # parquet ombre
IF4 = (248, 216, 168)  # parquet highlight

# --- CARRELAGE (blanc-bleu froid, centres Pokémon) ---
CT1 = (240, 244, 248)  # carrelage clair
CT2 = (224, 232, 240)  # carrelage base
CT3 = (200, 212, 224)  # carrelage joint

# --- TAPIS ROUGE ---
TP1 = (224, 48, 56)    # tapis rouge vif
TP2 = (192, 36, 44)    # tapis bord
TP3 = (208, 40, 48)    # tapis moyen
TP4 = (240, 72, 80)    # tapis highlight

# --- COMPTOIR (bois clair) ---
CK1 = (216, 184, 136)  # comptoir dessus
CK2 = (192, 160, 112)  # comptoir face
CK3 = (176, 144, 96)   # comptoir ombre

# --- MACHINE SOIN (blanc + vert + rouge) ---
MS1 = (240, 240, 244)  # corps blanc
MS2 = (72, 208, 96)    # lumière verte
MS3 = (248, 64, 72)    # lumière rouge
MS4 = (200, 200, 208)  # métal

# --- ÉTAGÈRE ---
SH1 = (192, 160, 112)  # étagère bois
SH2 = (168, 136, 96)   # étagère ombre
SH3 = (80, 160, 232)   # livres bleus
SH4 = (232, 80, 72)    # livres rouges

# --- LIT ---
BD1 = (80, 144, 240)   # couverture bleue
BD2 = (56, 112, 208)   # couverture ombre
BD3 = (248, 244, 232)  # oreiller/drap blanc
BD4 = (104, 168, 255)  # couverture highlight

# --- TV ---
TV1 = (48, 48, 56)     # boîtier TV noir
TV2 = (72, 200, 240)   # écran allumé
TV3 = (96, 216, 255)   # écran clair

# --- PC ---
PC1 = (208, 200, 184)  # boîtier beige
PC2 = (56, 144, 232)   # écran bleu
PC3 = (80, 168, 248)   # écran clair

# --- PLANTE ---
PL1 = (56, 176, 72)    # feuille verte
PL2 = (40, 144, 56)    # feuille foncée
PL3 = (80, 200, 96)    # feuille claire
PL4 = (184, 120, 56)   # pot terre cuite
PL5 = (160, 96, 40)    # pot ombre

# --- ESCALIER ---
ST1 = (208, 184, 144)  # marche claire
ST2 = (184, 160, 120)  # marche ombre
ST3 = (168, 144, 104)  # côté marche

# --- TABLE ---
TB1 = (200, 168, 112)  # dessus table
TB2 = (176, 144, 88)   # pied table
TB3 = (168, 136, 80)   # ombre table

# --- CHAISE ---
CH1 = (200, 168, 112)  # chaise bois
CH2 = (176, 144, 88)   # chaise ombre
CH3 = (224, 56, 48)    # coussin rouge

# --- POSTER ---
PS1 = (72, 168, 88)    # fond vert nature
PS2 = (136, 200, 248)  # ciel bleu
PS3 = (240, 240, 200)  # cadre
PS4 = (248, 200, 64)   # soleil jaune

# --- POUBELLE ---
PB1 = (176, 176, 184)  # métal
PB2 = (152, 152, 160)  # métal ombre
PB3 = (200, 200, 208)  # métal clair

# --- PORTE INTÉRIEURE ---
ID1 = (168, 120, 64)   # porte bois
ID2 = (144, 100, 48)   # porte ombre
ID3 = (192, 144, 80)   # porte clair
ID4 = (248, 216, 72)   # poignée dorée


def R(d, x1, y1, x2, y2, c):
    d.rectangle([x1, y1, x2, y2], fill=c)


def Px(d, pts, c):
    d.point(pts, fill=c)


# ══════════════════════════════════════════════════════════════
# FONCTIONS DE DESSIN PAR TILE (0-47)
# ══════════════════════════════════════════════════════════════

def draw_tile(d, tx, ty, index):
    """Dessine le tile 'index' à la position (tx, ty) dans l'atlas."""
    x0, y0 = tx * TILE, ty * TILE
    fn = TILE_DRAW.get(index)
    if fn:
        fn(d, x0, y0)
    else:
        # Fallback : damier rose (debug pour tiles manquants)
        for py in range(TILE):
            for px in range(TILE):
                if (px + py) % 2 == 0:
                    d.point([(x0 + px, y0 + py)], fill=(255, 0, 255))


def _noise(x, y, seed=0):
    """Pseudo-noise simple pour variation de texture."""
    n = (x * 73 + y * 97 + seed * 113) & 0xFFFF
    return ((n * n * 3697) >> 8) & 0xFF


def _blend(c1, c2, t):
    """Mélange linéaire entre deux couleurs (t=0→c1, t=1→c2)."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


# ── Ligne 0 : Terrain de base ──

def tile_herbe(d, x0, y0):
    """Tile 0 : Herbe normale — texture vive avec variation."""
    R(d, x0, y0, x0+31, y0+31, GR1)
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 1)
            if n < 40:
                Px(d, [(x0+x, y0+y)], GR2)
            elif n < 70:
                Px(d, [(x0+x, y0+y)], GR3)
            elif n > 230:
                Px(d, [(x0+x, y0+y)], GR4)

def tile_herbe_haute(d, x0, y0):
    """Tile 1 : Herbes hautes — plus foncées avec motif W."""
    R(d, x0, y0, x0+31, y0+31, HG1)
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 2)
            if n < 50:
                Px(d, [(x0+x, y0+y)], HG2)
            elif n > 200:
                Px(d, [(x0+x, y0+y)], HG3)
    # Motif herbe haute : brins en V
    for cx in range(4, 32, 8):
        for cy in range(4, 32, 10):
            for i in range(5):
                px1 = cx - i
                px2 = cx + i
                py = cy + i
                if 0 <= px1 < 32 and 0 <= py < 32:
                    Px(d, [(x0+px1, y0+py)], HG4)
                if 0 <= px2 < 32 and 0 <= py < 32:
                    Px(d, [(x0+px2, y0+py)], HG4)

def tile_chemin(d, x0, y0):
    """Tile 2 : Chemin de terre."""
    R(d, x0, y0, x0+31, y0+31, PT2)
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 3)
            if n < 50:
                Px(d, [(x0+x, y0+y)], PT1)
            elif n < 80:
                Px(d, [(x0+x, y0+y)], PT3)
            elif n > 230:
                Px(d, [(x0+x, y0+y)], PT4)

def tile_sable(d, x0, y0):
    """Tile 3 : Sable."""
    R(d, x0, y0, x0+31, y0+31, SA2)
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 4)
            if n < 60:
                Px(d, [(x0+x, y0+y)], SA1)
            elif n < 90:
                Px(d, [(x0+x, y0+y)], SA3)
            elif n > 220:
                Px(d, [(x0+x, y0+y)], SA4)

def tile_eau(d, x0, y0):
    """Tile 4 : Eau animée."""
    R(d, x0, y0, x0+31, y0+31, WA2)
    # Vagues horizontales
    for y in range(32):
        wave = int(2 * math.sin(y * 0.5))
        for x in range(32):
            n = _noise(x + wave, y, 5)
            if n < 40:
                Px(d, [(x0+x, y0+y)], WA1)
            elif n < 70:
                Px(d, [(x0+x, y0+y)], WA5)
            elif n > 200:
                Px(d, [(x0+x, y0+y)], WA3)
            elif n > 240:
                Px(d, [(x0+x, y0+y)], WA4)

def tile_fleur(d, x0, y0):
    """Tile 5 : Herbe avec fleurs."""
    tile_herbe(d, x0, y0)
    # Fleurs dispersées
    flowers = [(4, 6, FL_R), (14, 3, FL_Y), (24, 8, FL_W),
               (8, 18, FL_P), (20, 22, FL_R), (28, 14, FL_Y),
               (3, 28, FL_W), (16, 26, FL_P)]
    for fx, fy, fc in flowers:
        Px(d, [(x0+fx, y0+fy)], fc)
        if fx > 0: Px(d, [(x0+fx-1, y0+fy)], fc)
        if fx < 31: Px(d, [(x0+fx+1, y0+fy)], fc)
        if fy > 0: Px(d, [(x0+fx, y0+fy-1)], fc)
        if fy < 31: Px(d, [(x0+fx, y0+fy+1)], fc)

def tile_empty6(d, x0, y0):
    """Tile 6 : réservé — herbe variante."""
    tile_herbe(d, x0, y0)
    # Quelques cailloux
    for cx, cy in [(8, 12), (22, 20), (14, 28)]:
        R(d, x0+cx, y0+cy, x0+cx+2, y0+cy+1, (180, 176, 168))
        R(d, x0+cx, y0+cy, x0+cx+2, y0+cy, (200, 196, 188))

def tile_empty7(d, x0, y0):
    """Tile 7 : réservé — chemin+herbe transition."""
    R(d, x0, y0, x0+31, y0+15, GR1)
    R(d, x0, y0+16, x0+31, y0+31, PT2)
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 7)
            if y < 16 and n < 40:
                Px(d, [(x0+x, y0+y)], GR2)
            elif y >= 16 and n < 40:
                Px(d, [(x0+x, y0+y)], PT1)


# ── Ligne 1 : Arbres et végétation ──

def _draw_canopy(d, x0, y0, offset=0):
    """Canopée d'arbre volumétrique."""
    cx, cy = 16, 16
    for y in range(32):
        for x in range(32):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 15:
                # Éclairage directionnel (lumière en haut-gauche)
                light = 1.0 - (dx + dy) / 30.0
                light = max(0.0, min(1.0, light))
                n = _noise(x + offset, y + offset, 10 + offset)
                nf = n / 255.0 * 0.3  # variation texture
                t = light * 0.6 + nf
                if t > 0.7:
                    c = LF4
                elif t > 0.5:
                    c = LF3
                elif t > 0.3:
                    c = LF2
                elif t > 0.15:
                    c = LF1
                else:
                    c = LF5
                Px(d, [(x0+x, y0+y)], c)

def tile_arbre_haut(d, x0, y0):
    """Tile 8 : Arbre haut gauche — canopée."""
    _draw_canopy(d, x0, y0, 0)

def tile_arbre_bas(d, x0, y0):
    """Tile 9 : Arbre bas gauche — tronc + base canopée."""
    # Fond herbe
    R(d, x0, y0, x0+31, y0+31, GR1)
    for y in range(20, 32):
        for x in range(32):
            n = _noise(x, y, 9)
            if n < 40:
                Px(d, [(x0+x, y0+y)], GR2)
    # Tronc au centre
    R(d, x0+12, y0, x0+19, y0+24, TK2)
    R(d, x0+12, y0, x0+14, y0+24, TK1)  # ombre
    R(d, x0+17, y0, x0+19, y0+24, TK3)  # lumière
    # Canopée basse (déborde du tile du dessus)
    for y in range(12):
        for x in range(32):
            dx, dy = x - 16, y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 14:
                n = _noise(x, y, 19)
                c = LF2 if n < 128 else LF3
                Px(d, [(x0+x, y0+y)], c)

def tile_arbre_haut_r(d, x0, y0):
    """Tile 10 : Arbre haut droit — canopée variante."""
    _draw_canopy(d, x0, y0, 42)

def tile_arbre_bas_r(d, x0, y0):
    """Tile 11 : Arbre bas droit — tronc variante."""
    tile_arbre_bas(d, x0, y0)
    # Petit détail racine
    R(d, x0+10, y0+22, x0+12, y0+24, TK1)
    R(d, x0+19, y0+23, x0+21, y0+24, TK1)

def tile_fence_h(d, x0, y0):
    """Tile 12 : Clôture horizontale."""
    R(d, x0, y0, x0+31, y0+31, GR1)
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 12)
            if n < 40:
                Px(d, [(x0+x, y0+y)], GR2)
    # Poteaux
    R(d, x0+2, y0+8, x0+5, y0+24, FN2)
    R(d, x0+26, y0+8, x0+29, y0+24, FN2)
    R(d, x0+2, y0+8, x0+2, y0+24, FN3)
    R(d, x0+26, y0+8, x0+26, y0+24, FN3)
    # Barres horizontales
    R(d, x0, y0+12, x0+31, y0+14, FN1)
    R(d, x0, y0+12, x0+31, y0+12, FN3)
    R(d, x0, y0+19, x0+31, y0+21, FN1)
    R(d, x0, y0+19, x0+31, y0+19, FN3)

def tile_fence_v(d, x0, y0):
    """Tile 13 : Clôture verticale."""
    R(d, x0, y0, x0+31, y0+31, GR1)
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 13)
            if n < 40:
                Px(d, [(x0+x, y0+y)], GR2)
    R(d, x0+13, y0, x0+18, y0+31, FN1)
    R(d, x0+13, y0, x0+13, y0+31, FN3)
    R(d, x0+18, y0, x0+18, y0+31, FN3)

def tile_buisson(d, x0, y0):
    """Tile 14 : Buisson."""
    R(d, x0, y0, x0+31, y0+31, GR1)
    # Formes rondes de buisson
    cx, cy = 16, 18
    for y in range(32):
        for x in range(32):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 12:
                light = 1.0 - (dx + dy) / 24.0
                light = max(0, min(1, light))
                if light > 0.6:
                    Px(d, [(x0+x, y0+y)], LF3)
                elif light > 0.3:
                    Px(d, [(x0+x, y0+y)], LF2)
                else:
                    Px(d, [(x0+x, y0+y)], LF1)

def tile_herbe_detail(d, x0, y0):
    """Tile 15 : Herbe avec des touffes."""
    tile_herbe(d, x0, y0)
    # Touffes d'herbe en accent
    for bx, by in [(8, 8), (20, 6), (6, 22), (24, 20), (14, 16)]:
        for i in range(4):
            Px(d, [(x0+bx, y0+by-i)], GR5)
            Px(d, [(x0+bx+1, y0+by-i-1)], GR5)


# ── Ligne 2 : Maisons extérieures ──

def tile_toit_g(d, x0, y0):
    """Tile 16 : Toit gauche."""
    R(d, x0, y0, x0+31, y0+31, RF1)
    # Tuiles en rangées
    for row_i in range(4):
        ry = y0 + row_i * 8
        R(d, x0, ry, x0+31, ry, RF4)
        R(d, x0, ry+1, x0+31, ry+1, RF3)
    # Bord gauche (gouttière)
    R(d, x0, y0, x0+2, y0+31, RF4)
    R(d, x0+3, y0, x0+3, y0+31, RF2)

def tile_toit_m(d, x0, y0):
    """Tile 17 : Toit milieu."""
    R(d, x0, y0, x0+31, y0+31, RF1)
    for row_i in range(4):
        ry = y0 + row_i * 8
        R(d, x0, ry, x0+31, ry, RF4)
        R(d, x0, ry+1, x0+31, ry+1, RF3)
        # Décalage tuiles
        for col_i in range(4):
            cx = col_i * 8 + (4 if row_i % 2 else 0)
            if 0 <= cx < 32:
                Px(d, [(x0+cx, y0+row_i*8+4)], RF2)

def tile_toit_d(d, x0, y0):
    """Tile 18 : Toit droit."""
    R(d, x0, y0, x0+31, y0+31, RF1)
    for row_i in range(4):
        ry = y0 + row_i * 8
        R(d, x0, ry, x0+31, ry, RF4)
        R(d, x0, ry+1, x0+31, ry+1, RF3)
    R(d, x0+28, y0, x0+31, y0+31, RF4)
    R(d, x0+27, y0, x0+27, y0+31, RF2)

def tile_mur_g(d, x0, y0):
    """Tile 19 : Mur extérieur gauche."""
    R(d, x0, y0, x0+31, y0+31, XW2)
    R(d, x0, y0, x0+31, y0+1, XW3)  # ombre sous toit
    R(d, x0, y0, x0+2, y0+31, XW3)  # bord gauche
    R(d, x0+3, y0, x0+3, y0+31, XW1)  # relief

def tile_mur_m(d, x0, y0):
    """Tile 20 : Mur extérieur milieu."""
    R(d, x0, y0, x0+31, y0+31, XW2)
    R(d, x0, y0, x0+31, y0+1, XW3)

def tile_mur_d(d, x0, y0):
    """Tile 21 : Mur extérieur droit."""
    R(d, x0, y0, x0+31, y0+31, XW2)
    R(d, x0, y0, x0+31, y0+1, XW3)
    R(d, x0+28, y0, x0+31, y0+31, XW3)
    R(d, x0+27, y0, x0+27, y0+31, XW1)

def tile_porte(d, x0, y0):
    """Tile 22 : Porte d'entrée maison."""
    R(d, x0, y0, x0+31, y0+31, XW2)
    # Porte centrale
    R(d, x0+8, y0+4, x0+23, y0+31, DR1)
    R(d, x0+8, y0+4, x0+8, y0+31, DR2)
    R(d, x0+23, y0+4, x0+23, y0+31, DR2)
    R(d, x0+8, y0+4, x0+23, y0+4, DR3)
    # Poignée
    R(d, x0+20, y0+16, x0+21, y0+18, ID4)
    # Cadre
    R(d, x0+6, y0+2, x0+25, y0+3, XW3)
    R(d, x0+6, y0+2, x0+7, y0+31, XW3)
    R(d, x0+24, y0+2, x0+25, y0+31, XW3)
    # Paillasson
    R(d, x0+10, y0+28, x0+21, y0+31, (168, 136, 88))

def tile_fenetre_ext(d, x0, y0):
    """Tile 23 : Fenêtre extérieure."""
    R(d, x0, y0, x0+31, y0+31, XW2)
    # Fenêtre
    R(d, x0+6, y0+6, x0+25, y0+25, WN3)  # cadre blanc
    R(d, x0+8, y0+8, x0+23, y0+23, WN1)  # vitre ciel
    R(d, x0+8, y0+8, x0+23, y0+14, WN2)  # vitre haute
    # Croisillons
    R(d, x0+15, y0+6, x0+16, y0+25, WN3)
    R(d, x0+6, y0+15, x0+25, y0+16, WN3)
    # Rebord
    R(d, x0+5, y0+26, x0+26, y0+27, XW3)


# ── Ligne 3 : Intérieur de base ──

def tile_sol_int(d, x0, y0):
    """Tile 24 : Sol intérieur parquet — CHAUD ET LUMINEUX."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Lattes de parquet horizontales
    for ly in range(0, 32, 8):
        R(d, x0, y0+ly, x0+31, y0+ly, IF3)  # joint
        for lx in range(0, 32, 16):
            offset = 8 if (ly // 8) % 2 else 0
            ax = lx + offset
            if 0 <= ax < 32:
                R(d, x0+ax, y0+ly, x0+ax, y0+ly+7, IF3)
    # Variation de teinte
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 24)
            if n < 30:
                Px(d, [(x0+x, y0+y)], IF1)
            elif n > 235:
                Px(d, [(x0+x, y0+y)], IF4)

def tile_mur_int(d, x0, y0):
    """Tile 25 : Mur intérieur — CRÈME CHAUD, PAS GRIS !"""
    R(d, x0, y0, x0+31, y0+31, IW1)
    # Légère texture mur
    for y in range(28):
        for x in range(32):
            n = _noise(x, y, 25)
            if n < 20:
                Px(d, [(x0+x, y0+y)], IW2)
            elif n > 240:
                Px(d, [(x0+x, y0+y)], (255, 248, 232))
    # Plinthe bois en bas
    R(d, x0, y0+28, x0+31, y0+31, IW4)
    R(d, x0, y0+28, x0+31, y0+28, IW3)  # ligne de séparation
    # Moulure décorative en haut
    R(d, x0, y0, x0+31, y0+1, IW3)

def tile_comptoir(d, x0, y0):
    """Tile 26 : Comptoir (Centre Pokémon)."""
    # Sol carrelé en dessous
    R(d, x0, y0+20, x0+31, y0+31, CT1)
    # Comptoir
    R(d, x0, y0, x0+31, y0+4, CK1)  # dessus
    R(d, x0, y0+5, x0+31, y0+19, CK2)  # face
    R(d, x0, y0+5, x0, y0+19, CK3)  # ombre gauche
    R(d, x0+31, y0+5, x0+31, y0+19, CK3)
    R(d, x0, y0, x0+31, y0, CK1)  # highlight dessus
    # Décoration face comptoir
    R(d, x0+4, y0+8, x0+27, y0+10, CK3)
    R(d, x0+4, y0+14, x0+27, y0+16, CK3)

def tile_machine_soin(d, x0, y0):
    """Tile 27 : Machine de soin."""
    R(d, x0, y0, x0+31, y0+31, CT1)  # fond carrelage
    # Corps machine
    R(d, x0+6, y0+4, x0+25, y0+28, MS1)
    R(d, x0+6, y0+4, x0+6, y0+28, MS4)
    R(d, x0+25, y0+4, x0+25, y0+28, MS4)
    R(d, x0+6, y0+4, x0+25, y0+4, MS4)
    # Écran
    R(d, x0+10, y0+8, x0+21, y0+16, (200, 240, 200))
    # Voyants
    R(d, x0+10, y0+20, x0+12, y0+22, MS2)  # vert
    R(d, x0+15, y0+20, x0+17, y0+22, MS3)  # rouge
    # Pokéball slot
    R(d, x0+12, y0+24, x0+19, y0+27, MS4)
    R(d, x0+13, y0+25, x0+18, y0+26, (248, 248, 248))

def tile_etagere(d, x0, y0):
    """Tile 28 : Étagère avec livres."""
    R(d, x0, y0, x0+31, y0+31, IW1)  # mur derrière
    # Structure étagère
    R(d, x0+2, y0+2, x0+29, y0+29, SH1)
    # Planches horizontales
    for sy in [2, 10, 18, 26]:
        R(d, x0+2, y0+sy, x0+29, y0+sy+1, SH2)
    # Livres (rangée du haut)
    R(d, x0+4, y0+4, x0+7, y0+9, SH3)   # livre bleu
    R(d, x0+8, y0+4, x0+11, y0+9, SH4)  # livre rouge
    R(d, x0+12, y0+5, x0+15, y0+9, SH3)
    R(d, x0+16, y0+4, x0+19, y0+9, (248, 200, 64))  # jaune
    R(d, x0+20, y0+4, x0+23, y0+9, SH4)
    R(d, x0+24, y0+5, x0+27, y0+9, SH3)
    # Livres (rangée milieu)
    R(d, x0+5, y0+12, x0+8, y0+17, SH4)
    R(d, x0+9, y0+12, x0+14, y0+17, SH3)
    R(d, x0+16, y0+13, x0+20, y0+17, (248, 200, 64))
    R(d, x0+22, y0+12, x0+26, y0+17, SH4)
    # Objets (rangée basse)
    R(d, x0+6, y0+20, x0+12, y0+25, MS1)  # boîte blanche
    R(d, x0+18, y0+20, x0+24, y0+25, (248, 64, 64))  # objet rouge

def tile_tapis(d, x0, y0):
    """Tile 29 : Tapis rouge vif."""
    R(d, x0, y0, x0+31, y0+31, TP1)
    # Bordure
    R(d, x0, y0, x0+31, y0+1, TP2)
    R(d, x0, y0+30, x0+31, y0+31, TP2)
    R(d, x0, y0, x0+1, y0+31, TP2)
    R(d, x0+30, y0, x0+31, y0+31, TP2)
    # Frange décorative
    R(d, x0+2, y0+2, x0+29, y0+3, TP3)
    R(d, x0+2, y0+28, x0+29, y0+29, TP3)
    # Highlight central
    R(d, x0+8, y0+8, x0+23, y0+23, TP4)
    R(d, x0+10, y0+10, x0+21, y0+21, TP1)

def tile_sol_carrelage(d, x0, y0):
    """Tile 30 : Sol carrelé (Centre Pokémon)."""
    R(d, x0, y0, x0+31, y0+31, CT1)
    # Joints en croix
    R(d, x0+15, y0, x0+16, y0+31, CT3)
    R(d, x0, y0+15, x0+31, y0+16, CT3)
    # Subtile variation
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 30)
            if n < 15:
                Px(d, [(x0+x, y0+y)], CT2)

def tile_mur_motif(d, x0, y0):
    """Tile 31 : Mur intérieur avec motif."""
    R(d, x0, y0, x0+31, y0+31, IW1)
    # Motif losange subtil
    for y in range(32):
        for x in range(32):
            if (x + y) % 8 == 0 or (x - y) % 8 == 0:
                Px(d, [(x0+x, y0+y)], IW2)
    # Plinthe
    R(d, x0, y0+28, x0+31, y0+31, IW4)
    R(d, x0, y0+28, x0+31, y0+28, IW3)


# ── Ligne 4 : Chambre / Salon ── (CRITIQUE : c'est la chambre du joueur !)

def tile_lit_tete(d, x0, y0):
    """Tile 32 : Tête de lit — oreiller + couverture haut."""
    R(d, x0, y0, x0+31, y0+31, IF2)  # fond parquet
    # Tête de lit (bois)
    R(d, x0+2, y0+0, x0+29, y0+4, TK2)
    R(d, x0+2, y0+0, x0+29, y0+1, TK3)
    # Oreiller
    R(d, x0+4, y0+5, x0+27, y0+12, BD3)
    R(d, x0+4, y0+5, x0+27, y0+6, (255, 252, 244))  # highlight
    R(d, x0+14, y0+7, x0+17, y0+10, (240, 236, 224))  # pli
    # Couverture
    R(d, x0+2, y0+13, x0+29, y0+31, BD1)
    R(d, x0+2, y0+13, x0+29, y0+14, BD4)  # highlight
    R(d, x0+2, y0+13, x0+2, y0+31, BD2)
    R(d, x0+29, y0+13, x0+29, y0+31, BD2)
    # Plis couverture
    R(d, x0+10, y0+18, x0+10, y0+28, BD2)
    R(d, x0+20, y0+20, x0+20, y0+26, BD2)

def tile_lit_pied(d, x0, y0):
    """Tile 33 : Pied de lit — couverture bas."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Couverture suite
    R(d, x0+2, y0+0, x0+29, y0+24, BD1)
    R(d, x0+2, y0+0, x0+2, y0+24, BD2)
    R(d, x0+29, y0+0, x0+29, y0+24, BD2)
    R(d, x0+10, y0+2, x0+10, y0+16, BD2)
    R(d, x0+20, y0+0, x0+20, y0+12, BD2)
    # Pied de lit (bois)
    R(d, x0+2, y0+25, x0+29, y0+28, TK2)
    R(d, x0+2, y0+25, x0+29, y0+26, TK3)
    R(d, x0+2, y0+28, x0+29, y0+28, TK1)

def tile_tv(d, x0, y0):
    """Tile 34 : Télévision."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Meuble TV
    R(d, x0+4, y0+20, x0+27, y0+28, TK2)
    R(d, x0+4, y0+20, x0+27, y0+21, TK3)
    R(d, x0+4, y0+28, x0+27, y0+28, TK1)
    # TV
    R(d, x0+6, y0+2, x0+25, y0+19, TV1)  # boîtier
    R(d, x0+8, y0+4, x0+23, y0+17, TV2)  # écran
    R(d, x0+8, y0+4, x0+23, y0+8, TV3)  # reflet
    # Antenne
    R(d, x0+13, y0+0, x0+14, y0+2, TV1)
    R(d, x0+17, y0+0, x0+18, y0+2, TV1)
    # Bouton
    R(d, x0+15, y0+18, x0+16, y0+18, (232, 72, 56))

def tile_pc(d, x0, y0):
    """Tile 35 : Ordinateur PC."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Bureau
    R(d, x0+2, y0+20, x0+29, y0+28, TK2)
    R(d, x0+2, y0+20, x0+29, y0+21, TK3)
    # Écran
    R(d, x0+6, y0+2, x0+22, y0+18, PC1)  # boîtier
    R(d, x0+8, y0+4, x0+20, y0+16, PC2)  # écran
    R(d, x0+8, y0+4, x0+20, y0+8, PC3)  # reflet écran
    # Texte sur écran (lignes vertes)
    for ly in [10, 12, 14]:
        R(d, x0+10, y0+ly, x0+18, y0+ly, (120, 248, 120))
    # Clavier
    R(d, x0+7, y0+22, x0+21, y0+25, (200, 200, 208))
    R(d, x0+8, y0+23, x0+20, y0+24, (176, 176, 184))
    # Unité centrale (petite, à côté)
    R(d, x0+24, y0+8, x0+28, y0+19, PC1)
    R(d, x0+24, y0+8, x0+28, y0+9, (184, 176, 160))

def tile_plante(d, x0, y0):
    """Tile 36 : Plante en pot."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Pot
    R(d, x0+10, y0+20, x0+21, y0+29, PL4)
    R(d, x0+10, y0+20, x0+10, y0+29, PL5)
    R(d, x0+11, y0+20, x0+20, y0+20, PL5)
    # Terre
    R(d, x0+11, y0+21, x0+20, y0+22, (120, 80, 40))
    # Feuillage (boule verte)
    cx, cy = 16, 14
    for y in range(32):
        for x in range(32):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 9:
                light = 1.0 - (dx + dy) / 18.0
                light = max(0, min(1, light))
                if light > 0.6:
                    Px(d, [(x0+x, y0+y)], PL3)
                elif light > 0.3:
                    Px(d, [(x0+x, y0+y)], PL1)
                else:
                    Px(d, [(x0+x, y0+y)], PL2)
    # Tige
    R(d, x0+15, y0+18, x0+16, y0+21, PL2)

def tile_escalier_up(d, x0, y0):
    """Tile 37 : Escalier montant."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Marches (vue de dessus, allant vers le haut)
    for i in range(4):
        sy = y0 + i * 8
        R(d, x0+2, sy, x0+29, sy+6, ST1)
        R(d, x0+2, sy+6, x0+29, sy+7, ST2)
        R(d, x0+2, sy, x0+2, sy+7, ST3)
        R(d, x0+29, sy, x0+29, sy+7, ST3)
        # Highlight marche
        R(d, x0+3, sy, x0+28, sy, (224, 200, 160))
    # Rampe gauche
    R(d, x0, y0, x0+1, y0+31, TK2)

def tile_escalier_down(d, x0, y0):
    """Tile 38 : Escalier descendant."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Marches inversées (plus sombres = descendent)
    for i in range(4):
        sy = y0 + i * 8
        R(d, x0+2, sy, x0+29, sy+6, ST2)
        R(d, x0+2, sy+6, x0+29, sy+7, ST3)
        R(d, x0+2, sy, x0+2, sy+7, ST3)
        R(d, x0+29, sy, x0+29, sy+7, ST3)
        # Ombre profonde
        R(d, x0+3, sy+5, x0+28, sy+5, ST3)
    R(d, x0, y0, x0+1, y0+31, TK2)

def tile_paillasson(d, x0, y0):
    """Tile 39 : Paillasson d'entrée."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Paillasson
    R(d, x0+4, y0+8, x0+27, y0+24, (168, 136, 88))
    R(d, x0+4, y0+8, x0+27, y0+9, (152, 120, 72))
    R(d, x0+4, y0+23, x0+27, y0+24, (152, 120, 72))
    R(d, x0+4, y0+8, x0+5, y0+24, (152, 120, 72))
    R(d, x0+26, y0+8, x0+27, y0+24, (152, 120, 72))
    # Texte "BIENVENUE" (motif)
    for x in range(8, 24, 2):
        Px(d, [(x0+x, y0+15), (x0+x, y0+17)], (192, 160, 104))


# ── Ligne 5 : Intérieur avancé ──

def tile_porte_int(d, x0, y0):
    """Tile 40 : Porte intérieure."""
    R(d, x0, y0, x0+31, y0+31, IW1)
    # Porte
    R(d, x0+6, y0+2, x0+25, y0+31, ID1)
    R(d, x0+6, y0+2, x0+6, y0+31, ID2)
    R(d, x0+25, y0+2, x0+25, y0+31, ID2)
    R(d, x0+7, y0+2, x0+24, y0+3, ID3)
    # Panneau du haut
    R(d, x0+9, y0+5, x0+22, y0+14, ID3)
    R(d, x0+9, y0+5, x0+22, y0+5, ID1)
    R(d, x0+9, y0+14, x0+22, y0+14, ID2)
    # Panneau du bas
    R(d, x0+9, y0+17, x0+22, y0+28, ID3)
    R(d, x0+9, y0+17, x0+22, y0+17, ID1)
    R(d, x0+9, y0+28, x0+22, y0+28, ID2)
    # Poignée
    R(d, x0+21, y0+16, x0+22, y0+17, ID4)
    # Cadre
    R(d, x0+4, y0+0, x0+5, y0+31, IW3)
    R(d, x0+26, y0+0, x0+27, y0+31, IW3)
    R(d, x0+4, y0+0, x0+27, y0+1, IW3)

def tile_fenetre_int(d, x0, y0):
    """Tile 41 : Fenêtre intérieure — LUMINEUSE avec rideaux."""
    R(d, x0, y0, x0+31, y0+31, IW1)
    # Cadre fenêtre
    R(d, x0+4, y0+2, x0+27, y0+27, WN3)
    # Vitre (ciel bleu clair)
    R(d, x0+6, y0+4, x0+25, y0+25, (160, 216, 255))
    R(d, x0+6, y0+4, x0+25, y0+12, (136, 200, 248))
    # Nuages
    R(d, x0+8, y0+7, x0+14, y0+9, (240, 248, 255))
    R(d, x0+18, y0+10, x0+23, y0+12, (240, 248, 255))
    # Croisillon
    R(d, x0+15, y0+2, x0+16, y0+27, WN3)
    R(d, x0+4, y0+14, x0+27, y0+15, WN3)
    # Rideaux (jaune/crème comme FRLG)
    R(d, x0+4, y0+2, x0+7, y0+27, (248, 224, 128))
    R(d, x0+24, y0+2, x0+27, y0+27, (248, 224, 128))
    R(d, x0+4, y0+2, x0+5, y0+27, (240, 208, 96))
    R(d, x0+26, y0+2, x0+27, y0+27, (240, 208, 96))
    # Rebord
    R(d, x0+3, y0+28, x0+28, y0+29, IW3)

def tile_sol_bois_fonce(d, x0, y0):
    """Tile 42 : Sol bois foncé."""
    R(d, x0, y0, x0+31, y0+31, (184, 152, 104))
    for ly in range(0, 32, 8):
        R(d, x0, y0+ly, x0+31, y0+ly, (168, 136, 88))
        for lx in range(0, 32, 16):
            offset = 8 if (ly // 8) % 2 else 0
            ax = lx + offset
            if 0 <= ax < 32:
                R(d, x0+ax, y0+ly, x0+ax, y0+ly+7, (168, 136, 88))
    for y in range(32):
        for x in range(32):
            n = _noise(x, y, 42)
            if n < 20:
                Px(d, [(x0+x, y0+y)], (200, 168, 120))

def tile_mur_ext_fenetre(d, x0, y0):
    """Tile 43 : Mur extérieur avec petite fenêtre."""
    R(d, x0, y0, x0+31, y0+31, XW2)
    R(d, x0+8, y0+8, x0+23, y0+20, WN3)
    R(d, x0+10, y0+10, x0+21, y0+18, WN1)
    R(d, x0+15, y0+8, x0+16, y0+20, WN3)
    R(d, x0+8, y0+14, x0+23, y0+14, WN3)

def tile_table(d, x0, y0):
    """Tile 44 : Table."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Plateau
    R(d, x0+2, y0+8, x0+29, y0+14, TB1)
    R(d, x0+2, y0+8, x0+29, y0+9, (216, 184, 128))
    R(d, x0+2, y0+14, x0+29, y0+14, TB3)
    # Pieds
    R(d, x0+4, y0+15, x0+6, y0+28, TB2)
    R(d, x0+25, y0+15, x0+27, y0+28, TB2)

def tile_chaise(d, x0, y0):
    """Tile 45 : Chaise."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Dossier
    R(d, x0+8, y0+2, x0+23, y0+8, CH1)
    R(d, x0+8, y0+2, x0+23, y0+3, (216, 184, 128))
    # Tiges dossier
    R(d, x0+8, y0+8, x0+9, y0+18, CH2)
    R(d, x0+22, y0+8, x0+23, y0+18, CH2)
    # Assise (coussin rouge)
    R(d, x0+6, y0+16, x0+25, y0+22, CH3)
    R(d, x0+6, y0+16, x0+25, y0+17, (240, 72, 64))
    # Pieds
    R(d, x0+8, y0+23, x0+9, y0+28, CH2)
    R(d, x0+22, y0+23, x0+23, y0+28, CH2)

def tile_poster(d, x0, y0):
    """Tile 46 : Poster au mur — paysage coloré."""
    R(d, x0, y0, x0+31, y0+31, IW1)
    # Cadre
    R(d, x0+4, y0+4, x0+27, y0+27, PS3)
    # Image : ciel + montagne + herbe
    R(d, x0+6, y0+6, x0+25, y0+25, PS2)   # ciel
    R(d, x0+6, y0+16, x0+25, y0+25, PS1)  # herbe
    # Montagne
    pts = []
    for mx in range(6, 26):
        my = 16 - int(6 * math.sin((mx - 6) * 3.14159 / 20.0))
        for filly in range(my, 17):
            pts.append((x0+mx, y0+filly))
    if pts:
        Px(d, pts, (128, 160, 96))
    # Soleil
    R(d, x0+20, y0+8, x0+23, y0+11, PS4)
    # Plinthe
    R(d, x0, y0+28, x0+31, y0+31, IW4)

def tile_poubelle(d, x0, y0):
    """Tile 47 : Poubelle."""
    R(d, x0, y0, x0+31, y0+31, IF2)
    # Corps poubelle
    R(d, x0+10, y0+8, x0+21, y0+28, PB1)
    R(d, x0+10, y0+8, x0+10, y0+28, PB2)
    R(d, x0+21, y0+8, x0+21, y0+28, PB2)
    # Couvercle
    R(d, x0+8, y0+6, x0+23, y0+8, PB3)
    R(d, x0+8, y0+6, x0+23, y0+6, PB1)
    # Poignée couvercle
    R(d, x0+14, y0+4, x0+17, y0+6, PB2)
    # Bandes
    R(d, x0+10, y0+14, x0+21, y0+15, PB2)
    R(d, x0+10, y0+22, x0+21, y0+23, PB2)


# ══════════════════════════════════════════════════════════════
# TABLE DE DISPATCH
# ══════════════════════════════════════════════════════════════

TILE_DRAW = {
    # Ligne 0 : Terrain
    0: tile_herbe, 1: tile_herbe_haute, 2: tile_chemin, 3: tile_sable,
    4: tile_eau, 5: tile_fleur, 6: tile_empty6, 7: tile_empty7,
    # Ligne 1 : Végétation
    8: tile_arbre_haut, 9: tile_arbre_bas, 10: tile_arbre_haut_r, 11: tile_arbre_bas_r,
    12: tile_fence_h, 13: tile_fence_v, 14: tile_buisson, 15: tile_herbe_detail,
    # Ligne 2 : Maisons
    16: tile_toit_g, 17: tile_toit_m, 18: tile_toit_d, 19: tile_mur_g,
    20: tile_mur_m, 21: tile_mur_d, 22: tile_porte, 23: tile_fenetre_ext,
    # Ligne 3 : Intérieur base
    24: tile_sol_int, 25: tile_mur_int, 26: tile_comptoir, 27: tile_machine_soin,
    28: tile_etagere, 29: tile_tapis, 30: tile_sol_carrelage, 31: tile_mur_motif,
    # Ligne 4 : Chambre/Salon
    32: tile_lit_tete, 33: tile_lit_pied, 34: tile_tv, 35: tile_pc,
    36: tile_plante, 37: tile_escalier_up, 38: tile_escalier_down, 39: tile_paillasson,
    # Ligne 5 : Intérieur avancé
    40: tile_porte_int, 41: tile_fenetre_int, 42: tile_sol_bois_fonce, 43: tile_mur_ext_fenetre,
    44: tile_table, 45: tile_chaise, 46: tile_poster, 47: tile_poubelle,
}


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    img = Image.new("RGBA", (COLS * TILE, ROWS * TILE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    for index in range(COLS * ROWS):
        tx = index % COLS
        ty = index // COLS
        draw_tile(d, tx, ty, index)
        print(f"  Tile {index:2d} ({tx},{ty}) dessiné")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT)

    # Stats
    pixels = img.load()
    all_colors = set()
    for y in range(img.height):
        for x in range(img.width):
            c = pixels[x, y]
            if c[3] > 0:
                all_colors.add(c[:3])
    print(f"\n✓ Tileset v7 FRLG Bright généré : {OUT}")
    print(f"  Taille : {img.size[0]}×{img.size[1]} px ({COLS}×{ROWS} = {COLS*ROWS} tiles)")
    print(f"  Couleurs uniques : {len(all_colors)}")
    print(f"  Palette LUMINEUSE — murs crème, parquet chaud, mobilier coloré")


if __name__ == "__main__":
    main()
