#!/usr/bin/env python3
"""
Générateur de sprites joueur v5 — Style FRLG fidèle
=====================================
Canvas 32×48 px — personnage de ~16×28 px centré
Dessin pixel-par-pixel pour un contrôle total.

Style : Red de Pokémon FRLG — casquette rouge + logo blanc, T-shirt noir,
jean bleu, sneakers rouges+blanc, sac à dos jaune, cheveux bruns.
"""
from PIL import Image
import os, sys

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "characters")

# =============================================================================
# Palette FRLG
# =============================================================================
T  = (0, 0, 0, 0)
K  = (16, 16, 16, 255)       # contour noir
R1 = (224, 40, 40, 255)      # rouge casquette
R2 = (176, 24, 24, 255)      # rouge sombre
RW = (248, 248, 248, 255)    # blanc logo
S1 = (248, 208, 168, 255)    # peau
S2 = (224, 176, 128, 255)    # peau ombre
H1 = (80, 48, 24, 255)       # cheveux
H2 = (56, 32, 16, 255)       # cheveux ombre
V1 = (40, 40, 40, 255)       # t-shirt
V2 = (24, 24, 24, 255)       # t-shirt ombre
J1 = (64, 104, 192, 255)     # jean
J2 = (48, 72, 152, 255)      # jean ombre
SN = (224, 40, 40, 255)      # sneakers
SS = (248, 248, 248, 255)    # semelle
B1 = (240, 200, 48, 255)     # sac jaune
B2 = (192, 160, 32, 255)     # sac jaune ombre

def _frame(rows, w=32, h=48):
    """rows = list of (y, list_of_(x, color))"""
    img = Image.new("RGBA", (w, h), T)
    px = img.load()
    for y, cols in rows:
        for x, c in cols:
            if 0 <= x < w and 0 <= y < h and c != T:
                px[x, y] = c
    return img

def _row(y, x_start, colors):
    """Helper : dessine une ligne à partir de x_start."""
    return (y, [(x_start + i, c) for i, c in enumerate(colors)])

def _hmirror(rows):
    """Miroir horizontal dans un canvas 32px."""
    out = []
    for y, cols in rows:
        out.append((y, [(31 - x, c) for x, c in cols]))
    return out

# =============================================================================
# BAS (face) — idle
# =============================================================================
def _bas_0():
    r = []
    # Casquette (y=9..13, largeur 16px, centre x=8..23)
    r.append(_row(9,  10, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(10,  9, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(11,  8, [R2, R1, R1, RW, RW, RW, RW, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(12,  8, [R2, R1, R1, RW, R1, R1, RW, R1, R1, R1, R1, R1, R1, R2]))
    # Visière
    r.append(_row(13,  7, [K, K, K, K, K, K, K, K, K, K, K, K, K, K, K, K]))
    # Visage (y=14..19)
    r.append(_row(14,  9, [K, H1, S1, S1, S1, S1, S1, S1, S1, S1, S1, H1, K]))
    r.append(_row(15,  9, [K, S1, S1, S1, S1, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(16,  9, [K, S1, S1, K, K, S1, S1, S1, K, K, S1, S1, K]))
    r.append(_row(17,  9, [K, S1, S1, S1, S1, S1, S2, S1, S1, S1, S1, S1, K]))
    r.append(_row(18, 10, [K, S1, S1, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(19, 11, [K, S1, S1, S1, S1, S1, S1, S1, K]))
    # Cou
    r.append(_row(20, 12, [K, S1, S1, S1, S1, S1, K]))
    # T-shirt (y=21..27)
    r.append(_row(21, 10, [K, V1, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(22,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(23,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(24, 10, [K, K, V1, V1, V1, V1, V1, V1, V1, V1, K, K]))
    r.append(_row(25, 11, [K, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(26, 11, [K, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(27, 11, [K, V2, V1, V1, V1, V1, V1, V1, V2, K]))
    # Jean (y=28..33)
    r.append(_row(28, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(29, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(30, 11, [K, J1, J1, J1, K, K, J1, J1, J1, K]))
    r.append(_row(31, 11, [K, J1, J1, J2, K, K, J2, J1, J1, K]))
    r.append(_row(32, 11, [K, J1, J2, J2, K, K, J2, J2, J1, K]))
    r.append(_row(33, 11, [K, J2, J2, K, T, T, K, J2, J2, K]))
    # Chaussures (y=34..35)
    r.append(_row(34, 10, [K, SN, SN, K, T, T, T, K, SN, SN, K]))
    r.append(_row(35, 10, [K, SS, SS, K, T, T, T, K, SS, SS, K]))
    return r

# BAS marche gauche
def _bas_1():
    r = []
    # Casquette + tête (identique)
    r.append(_row(9,  10, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(10,  9, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(11,  8, [R2, R1, R1, RW, RW, RW, RW, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(12,  8, [R2, R1, R1, RW, R1, R1, RW, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(13,  7, [K, K, K, K, K, K, K, K, K, K, K, K, K, K, K, K]))
    r.append(_row(14,  9, [K, H1, S1, S1, S1, S1, S1, S1, S1, S1, S1, H1, K]))
    r.append(_row(15,  9, [K, S1, S1, S1, S1, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(16,  9, [K, S1, S1, K, K, S1, S1, S1, K, K, S1, S1, K]))
    r.append(_row(17,  9, [K, S1, S1, S1, S1, S1, S2, S1, S1, S1, S1, S1, K]))
    r.append(_row(18, 10, [K, S1, S1, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(19, 11, [K, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(20, 12, [K, S1, S1, S1, S1, S1, K]))
    # T-shirt
    r.append(_row(21, 10, [K, V1, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(22,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(23,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(24, 10, [K, K, V1, V1, V1, V1, V1, V1, V1, V1, K, K]))
    r.append(_row(25, 11, [K, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(26, 11, [K, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(27, 11, [K, V2, V1, V1, V1, V1, V1, V1, V2, K]))
    # Jean — jambe gauche avance
    r.append(_row(28, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(29, 10, [K, J1, J1, J1, K, K, J1, J1, J1, K]))
    r.append(_row(30,  9, [K, J1, J1, J2, K, T, K, J1, J1, J1, K]))
    r.append(_row(31,  8, [K, J1, J2, K, T, T, T, K, J2, J1, K]))
    r.append(_row(32,  8, [K, SN, SN, K, T, T, T, K, J2, J2, K]))
    r.append(_row(33,  8, [K, SS, SS, K, T, T, T, T, K, J2, K]))
    r.append(_row(34,  9, [K, K, T, T, T, T, T, K, SN, SN, K]))
    r.append(_row(35, 18, [K, SS, SS, K]))
    return r

# BAS marche droite
def _bas_2():
    r = []
    # Tête identique
    r.append(_row(9,  10, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(10,  9, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(11,  8, [R2, R1, R1, RW, RW, RW, RW, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(12,  8, [R2, R1, R1, RW, R1, R1, RW, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(13,  7, [K, K, K, K, K, K, K, K, K, K, K, K, K, K, K, K]))
    r.append(_row(14,  9, [K, H1, S1, S1, S1, S1, S1, S1, S1, S1, S1, H1, K]))
    r.append(_row(15,  9, [K, S1, S1, S1, S1, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(16,  9, [K, S1, S1, K, K, S1, S1, S1, K, K, S1, S1, K]))
    r.append(_row(17,  9, [K, S1, S1, S1, S1, S1, S2, S1, S1, S1, S1, S1, K]))
    r.append(_row(18, 10, [K, S1, S1, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(19, 11, [K, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(20, 12, [K, S1, S1, S1, S1, S1, K]))
    r.append(_row(21, 10, [K, V1, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(22,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(23,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(24, 10, [K, K, V1, V1, V1, V1, V1, V1, V1, V1, K, K]))
    r.append(_row(25, 11, [K, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(26, 11, [K, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(27, 11, [K, V2, V1, V1, V1, V1, V1, V1, V2, K]))
    # Jean — jambe droite avance
    r.append(_row(28, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(29, 11, [K, J1, J1, J1, K, K, J1, J1, J1, J1, K]))
    r.append(_row(30, 11, [K, J1, J1, J1, K, T, K, J2, J1, J1, J1, K]))
    r.append(_row(31, 11, [K, J1, J2, K, T, T, T, K, J2, J1, J1, K]))
    r.append(_row(32, 11, [K, J2, J2, K, T, T, T, K, SN, SN, K]))
    r.append(_row(33, 12, [K, J2, K, T, T, T, T, K, SS, SS, K]))
    r.append(_row(34, 10, [K, SN, SN, K, T, T, T, T, T, K, K]))
    r.append(_row(35, 10, [K, SS, SS, K]))
    return r

# =============================================================================
# HAUT (dos)
# =============================================================================
def _haut_0():
    r = []
    r.append(_row(9,  10, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(10,  9, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(11,  8, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(12,  8, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(13,  8, [K, K, K, K, K, K, K, K, K, K, K, K, K, K]))
    r.append(_row(14,  9, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(15,  9, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(16,  9, [K, H1, H2, H1, H2, H1, H1, H2, H1, H2, H1, H1, K]))
    r.append(_row(17, 10, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(18, 11, [K, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(19, 11, [K, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(20, 12, [K, S1, S1, S1, S1, S1, K]))
    r.append(_row(21, 10, [K, V1, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(22,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(23,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(24, 10, [K, K, V1, V1, V1, V1, V1, V1, V1, V1, K, K]))
    # Sac à dos
    r.append(_row(25, 11, [K, V1, V1, B1, B1, B1, B1, V1, V1, K]))
    r.append(_row(26, 11, [K, V1, B1, B1, B2, B2, B1, B1, V1, K]))
    r.append(_row(27, 11, [K, V1, B1, B2, B2, B2, B2, B1, V1, K]))
    # Jean
    r.append(_row(28, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(29, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(30, 11, [K, J1, J1, J1, K, K, J1, J1, J1, K]))
    r.append(_row(31, 11, [K, J1, J1, J2, K, K, J2, J1, J1, K]))
    r.append(_row(32, 11, [K, J1, J2, J2, K, K, J2, J2, J1, K]))
    r.append(_row(33, 11, [K, J2, J2, K, T, T, K, J2, J2, K]))
    r.append(_row(34, 10, [K, SN, SN, K, T, T, T, K, SN, SN, K]))
    r.append(_row(35, 10, [K, SS, SS, K, T, T, T, K, SS, SS, K]))
    return r

def _haut_1():
    r = []
    # Tête identique à haut_0
    r.append(_row(9,  10, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(10,  9, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(11,  8, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(12,  8, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(13,  8, [K, K, K, K, K, K, K, K, K, K, K, K, K, K]))
    r.append(_row(14,  9, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(15,  9, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(16,  9, [K, H1, H2, H1, H2, H1, H1, H2, H1, H2, H1, H1, K]))
    r.append(_row(17, 10, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(18, 11, [K, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(19, 11, [K, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(20, 12, [K, S1, S1, S1, S1, S1, K]))
    r.append(_row(21, 10, [K, V1, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(22,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(23,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(24, 10, [K, K, V1, V1, V1, V1, V1, V1, V1, V1, K, K]))
    r.append(_row(25, 11, [K, V1, V1, B1, B1, B1, B1, V1, V1, K]))
    r.append(_row(26, 11, [K, V1, B1, B1, B2, B2, B1, B1, V1, K]))
    r.append(_row(27, 11, [K, V1, B1, B2, B2, B2, B2, B1, V1, K]))
    # Jambe gauche avance
    r.append(_row(28, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(29, 10, [K, J1, J1, J1, K, K, J1, J1, J1, K]))
    r.append(_row(30,  9, [K, J1, J1, J2, K, T, K, J1, J1, J1, K]))
    r.append(_row(31,  8, [K, J1, J2, K, T, T, T, K, J2, J1, K]))
    r.append(_row(32,  8, [K, SN, SN, K, T, T, T, K, J2, J2, K]))
    r.append(_row(33,  8, [K, SS, SS, K, T, T, T, T, K, J2, K]))
    r.append(_row(34,  9, [K, K, T, T, T, T, T, K, SN, SN, K]))
    r.append(_row(35, 18, [K, SS, SS, K]))
    return r

def _haut_2():
    r = []
    r.append(_row(9,  10, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(10,  9, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(11,  8, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(12,  8, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(13,  8, [K, K, K, K, K, K, K, K, K, K, K, K, K, K]))
    r.append(_row(14,  9, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(15,  9, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(16,  9, [K, H1, H2, H1, H2, H1, H1, H2, H1, H2, H1, H1, K]))
    r.append(_row(17, 10, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(18, 11, [K, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(19, 11, [K, H1, H1, H1, H1, H1, H1, H1, K]))
    r.append(_row(20, 12, [K, S1, S1, S1, S1, S1, K]))
    r.append(_row(21, 10, [K, V1, V1, V1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(22,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(23,  9, [K, S1, V1, V1, V1, V1, V1, V1, V1, V1, V1, S1, K]))
    r.append(_row(24, 10, [K, K, V1, V1, V1, V1, V1, V1, V1, V1, K, K]))
    r.append(_row(25, 11, [K, V1, V1, B1, B1, B1, B1, V1, V1, K]))
    r.append(_row(26, 11, [K, V1, B1, B1, B2, B2, B1, B1, V1, K]))
    r.append(_row(27, 11, [K, V1, B1, B2, B2, B2, B2, B1, V1, K]))
    # Jambe droite avance
    r.append(_row(28, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(29, 11, [K, J1, J1, J1, K, K, J1, J1, J1, J1, K]))
    r.append(_row(30, 11, [K, J1, J1, J1, K, T, K, J2, J1, J1, J1, K]))
    r.append(_row(31, 11, [K, J1, J2, K, T, T, T, K, J2, J1, J1, K]))
    r.append(_row(32, 11, [K, J2, J2, K, T, T, T, K, SN, SN, K]))
    r.append(_row(33, 12, [K, J2, K, T, T, T, T, K, SS, SS, K]))
    r.append(_row(34, 10, [K, SN, SN, K, T, T, T, T, T, K, K]))
    r.append(_row(35, 10, [K, SS, SS, K]))
    return r

# =============================================================================
# GAUCHE (profil)
# =============================================================================
def _gauche_0():
    r = []
    # Casquette avec visière gauche
    r.append(_row(9,  10, [R2, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(10,  9, [R2, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(11,  7, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(12,  7, [K, K, K, K, K, K, K, K, K, K, K, K]))
    # Visage
    r.append(_row(13,  9, [K, H1, H1, S1, S1, S1, S1, S1, H1, K]))
    r.append(_row(14,  9, [K, H1, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(15,  9, [K, S1, S1, K, S1, S1, S1, S1, S1, K]))
    r.append(_row(16,  9, [K, S1, S1, S1, S1, S2, S1, S1, K]))
    r.append(_row(17, 10, [K, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(18, 11, [K, S1, S1, S1, S1, K]))
    # Cou
    r.append(_row(19, 12, [K, S1, S1, S1, K]))
    # T-shirt + sac
    r.append(_row(20, 11, [K, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(21, 10, [K, S1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(22, 10, [K, K, V1, V1, V1, V1, V1, V1, B1, K]))
    r.append(_row(23, 11, [K, V1, V1, V1, V1, V1, V1, B1, K]))
    r.append(_row(24, 11, [K, V1, V1, V1, V1, V1, V1, B2, K]))
    r.append(_row(25, 11, [K, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(26, 11, [K, V2, V1, V1, V1, V1, V2, K]))
    # Jean
    r.append(_row(27, 11, [K, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(28, 11, [K, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(29, 11, [K, J1, J1, K, J1, J1, J1, K]))
    r.append(_row(30, 11, [K, J1, J2, K, J2, J1, J1, K]))
    r.append(_row(31, 11, [K, J2, J2, K, J2, J2, K]))
    # Chaussures
    r.append(_row(32, 10, [K, SN, SN, K, K, SN, SN, K]))
    r.append(_row(33, 10, [K, SS, SS, K, K, SS, SS, K]))
    return r

def _gauche_1():
    r = []
    r.append(_row(9,  10, [R2, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(10,  9, [R2, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(11,  7, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(12,  7, [K, K, K, K, K, K, K, K, K, K, K, K]))
    r.append(_row(13,  9, [K, H1, H1, S1, S1, S1, S1, S1, H1, K]))
    r.append(_row(14,  9, [K, H1, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(15,  9, [K, S1, S1, K, S1, S1, S1, S1, S1, K]))
    r.append(_row(16,  9, [K, S1, S1, S1, S1, S2, S1, S1, K]))
    r.append(_row(17, 10, [K, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(18, 11, [K, S1, S1, S1, S1, K]))
    r.append(_row(19, 12, [K, S1, S1, S1, K]))
    r.append(_row(20, 11, [K, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(21, 10, [K, S1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(22, 10, [K, K, V1, V1, V1, V1, V1, V1, B1, K]))
    r.append(_row(23, 11, [K, V1, V1, V1, V1, V1, V1, B1, K]))
    r.append(_row(24, 11, [K, V1, V1, V1, V1, V1, V1, B2, K]))
    r.append(_row(25, 11, [K, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(26, 11, [K, V2, V1, V1, V1, V1, V2, K]))
    # Jambe gauche avance
    r.append(_row(27, 11, [K, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(28, 10, [K, J1, J1, K, J1, J1, J1, K]))
    r.append(_row(29,  9, [K, J1, J2, K, K, J1, J1, K]))
    r.append(_row(30,  8, [K, J2, K, T, K, J2, J1, K]))
    r.append(_row(31,  8, [K, SN, K, T, K, J2, K]))
    r.append(_row(32,  8, [K, SS, K, T, K, SN, SN, K]))
    r.append(_row(33, 14, [K, SS, SS, K]))
    return r

def _gauche_2():
    r = []
    r.append(_row(9,  10, [R2, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(10,  9, [R2, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(11,  7, [R2, R1, R1, R1, R1, R1, R1, R1, R1, R1, R1, R2]))
    r.append(_row(12,  7, [K, K, K, K, K, K, K, K, K, K, K, K]))
    r.append(_row(13,  9, [K, H1, H1, S1, S1, S1, S1, S1, H1, K]))
    r.append(_row(14,  9, [K, H1, S1, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(15,  9, [K, S1, S1, K, S1, S1, S1, S1, S1, K]))
    r.append(_row(16,  9, [K, S1, S1, S1, S1, S2, S1, S1, K]))
    r.append(_row(17, 10, [K, S1, S1, S1, S1, S1, S1, K]))
    r.append(_row(18, 11, [K, S1, S1, S1, S1, K]))
    r.append(_row(19, 12, [K, S1, S1, S1, K]))
    r.append(_row(20, 11, [K, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(21, 10, [K, S1, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(22, 10, [K, K, V1, V1, V1, V1, V1, V1, B1, K]))
    r.append(_row(23, 11, [K, V1, V1, V1, V1, V1, V1, B1, K]))
    r.append(_row(24, 11, [K, V1, V1, V1, V1, V1, V1, B2, K]))
    r.append(_row(25, 11, [K, V1, V1, V1, V1, V1, V1, K]))
    r.append(_row(26, 11, [K, V2, V1, V1, V1, V1, V2, K]))
    # Jambe droite avance
    r.append(_row(27, 11, [K, J1, J1, J1, J1, J1, J1, K]))
    r.append(_row(28, 11, [K, J1, J1, J1, K, J1, J1, K]))
    r.append(_row(29, 11, [K, J1, J1, K, K, J2, J1, K]))
    r.append(_row(30, 11, [K, J1, J2, K, T, K, J2, K]))
    r.append(_row(31, 11, [K, J2, K, T, K, SN, K]))
    r.append(_row(32, 10, [K, SN, SN, K, T, K, SS, K]))
    r.append(_row(33, 10, [K, SS, SS, K]))
    return r

# =============================================================================
# DROITE = miroir de GAUCHE
# =============================================================================
def _droite_0(): return _hmirror(_gauche_0())
def _droite_1(): return _hmirror(_gauche_2())  # inversé pour marche
def _droite_2(): return _hmirror(_gauche_1())

# =============================================================================
# Génération
# =============================================================================
FRAMES = {
    "bas":    [_bas_0, _bas_1, _bas_2],
    "haut":   [_haut_0, _haut_1, _haut_2],
    "gauche": [_gauche_0, _gauche_1, _gauche_2],
    "droite": [_droite_0, _droite_1, _droite_2],
}

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for direction, fns in FRAMES.items():
        for i, fn in enumerate(fns):
            name = f"red_normal_{direction}_{i}.png"
            rows = fn()
            img = _frame(rows)
            path = os.path.join(OUT_DIR, name)
            img.save(path)
            import numpy as np
            arr = np.array(img)
            opaque = int(np.sum(arr[:,:,3] > 0))
            colors = len(set(tuple(arr[y,x]) for y in range(48) for x in range(32) if arr[y,x,3] > 0))
            print(f"  ✓ {name}: 32×48, {opaque} px opaques, {colors} couleurs")
    print(f"\n✓ 12 sprites joueur v5 générés dans {OUT_DIR}")
    print("  Style FRLG : casquette rouge+logo, T-shirt noir, jean bleu, sac jaune, sneakers rouges")

if __name__ == "__main__":
    main()
