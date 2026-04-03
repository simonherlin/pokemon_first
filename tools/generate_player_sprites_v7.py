#!/usr/bin/env python3
"""
Générateur sprites joueur v7 — FRLG fidèle, 32×64 pixels
Chaque pixel logique = bloc 2×2 (identique au style rival/Chen)
Palette GBA FRLG, proportions identiques aux PNJ existants.
"""
from PIL import Image
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "characters")
W, H = 32, 64  # Taille réelle du canvas

# ─── Palette GBA FRLG (même base que rival) ──────────────────
T  = None  # transparent
K  = (  0,   0,   0)  # outline noir
R1 = (197,  57,  57)  # rouge vest principal
R2 = (255, 106,  74)  # rouge vif highlight
R3 = (123,  65,  65)  # rouge sombre ombre
WH = (238, 238, 255)  # blanc (logo casquette, col, semelle)
S1 = (255, 197, 148)  # peau claire
S2 = (222, 148, 115)  # peau ombre
H1 = ( 57,  57, 123)  # cheveux/sombre (= dark blue des sprites GBA)
H2 = ( 65,  65, 213)  # cheveux highlight
J1 = ( 57,  57, 123)  # jean principal (= même dark blue)
J2 = ( 65,  65, 213)  # jean highlight
JD = ( 40,  40,  90)  # jean ombre profonde
L  = (180, 180, 213)  # gris-bleu clair (highlight vêtements)
Y  = (189, 156,  57)  # jaune (boucle sac)
BK = ( 40,  40,  48)  # t-shirt noir sous le gilet


def logical_to_image(grid):
    """Convertit une grille logique 16×32 en image 32×64 (chaque pixel → 2×2)"""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for ly, row in enumerate(grid):
        for lx, col in enumerate(row):
            if col is None:
                continue
            rx, ry = lx * 2, ly * 2
            for dy in range(2):
                for dx in range(2):
                    px, py = rx + dx, ry + dy
                    if 0 <= px < W and 0 <= py < H:
                        img.putpixel((px, py), col + (255,))
    return img


# ═══════════════════════════════════════════════════════════════
# FACE (bas) — Red FRLG vu de face
# Grille logique 16 colonnes × 32 lignes
# Le personnage occupe environ lignes 12-30
# ═══════════════════════════════════════════════════════════════

def make_face_idle():
    # 16 colonnes. T = transparent
    g = [[T]*16 for _ in range(32)]

    # Ligne 12 : sommet casquette
    g[12] = [T, T, T, T, K, K, K, K, K, K, K, K, T, T, T, T]
    # Ligne 13 : casquette avec logo blanc
    g[13] = [T, T, T, K, R1,R1,R1,WH,WH,R1,R1,R1, K, T, T, T]
    # Ligne 14 : casquette corps
    g[14] = [T, T, T, K, R1,R1,R1,R1,R1,R1,R1,R1, K, T, T, T]
    # Ligne 15 : visière (plus large, dépasse la tête)
    g[15] = [T, T, K, R3,R3,R3,R3,R3,R3,R3,R3,R3,R3, K, T, T]
    # Ligne 16 : front — cheveux + peau
    g[16] = [T, T, K, K, H1,S1,S1,S1,S1,S1,S1,H1, K, K, T, T]
    # Ligne 17 : yeux
    g[17] = [T, T, T, K, S1, K,WH,S1,S1,WH, K,S1, K, T, T, T]
    # Ligne 18 : joues + nez
    g[18] = [T, T, T, K, S1,S2,S1,S1,S1,S1,S2,S1, K, T, T, T]
    # Ligne 19 : bouche + menton
    g[19] = [T, T, T, T, K,S2,S1,S1,S1,S1,S2, K, T, T, T, T]
    # Ligne 20 : cou
    g[20] = [T, T, T, T, T, K,S1,S1,S1,S1, K, T, T, T, T, T]
    # Ligne 21 : épaules — col blanc + gilet rouge (LARGE)
    g[21] = [T, T, K, R1,R1,R1,WH,BK,BK,WH,R1,R1,R1, K, T, T]
    # Ligne 22 : bras + gilet
    g[22] = [T, K,S1,S1, K,R1,BK,BK,BK,BK,R1, K,S1,S1, K, T]
    # Ligne 23 : bras + gilet détail
    g[23] = [T, K,S1,S1, K,R1,BK,R2,R2,BK,R1, K,S1,S1, K, T]
    # Ligne 24 : mains + gilet bas
    g[24] = [T, T, K,S2,S2, K,R1,R1,R1,R1, K,S2,S2, K, T, T]
    # Ligne 25 : ceinture (LARGE)
    g[25] = [T, T, T, T, K, K,BK, Y,Y,BK, K, K, T, T, T, T]
    # Ligne 26 : jean haut
    g[26] = [T, T, T, T, K, J1,J1,J2,J2,J1,J1, K, T, T, T, T]
    # Ligne 27 : jean
    g[27] = [T, T, T, T, K, J1,J1,J1,J1,J1,J1, K, T, T, T, T]
    # Ligne 28 : jean — séparation jambes
    g[28] = [T, T, T, T, K, J1,J1, K, K,J1,J1, K, T, T, T, T]
    # Ligne 29 : sneakers
    g[29] = [T, T, T, K,R1,R1,R1, K, K,R1,R1,R1, K, T, T, T]
    # Ligne 30 : semelles
    g[30] = [T, T, T, T, K,WH,WH, K, K,WH,WH, K, T, T, T, T]
    return logical_to_image(g)


def make_face_walk1():
    """Pied droit avancé."""
    g = [[T]*16 for _ in range(32)]
    # Copier le haut du corps (identique à idle)
    g[12] = [T, T, T, T, K, K, K, K, K, K, K, K, T, T, T, T]
    g[13] = [T, T, T, K, R1,R1,R1,WH,WH,R1,R1,R1, K, T, T, T]
    g[14] = [T, T, T, K, R1,R1,R1,R1,R1,R1,R1,R1, K, T, T, T]
    g[15] = [T, T, K, R3,R3,R3,R3,R3,R3,R3,R3,R3,R3, K, T, T]
    g[16] = [T, T, K, K, H1,S1,S1,S1,S1,S1,S1,H1, K, K, T, T]
    g[17] = [T, T, T, K, S1, K,WH,S1,S1,WH, K,S1, K, T, T, T]
    g[18] = [T, T, T, K, S1,S2,S1,S1,S1,S1,S2,S1, K, T, T, T]
    g[19] = [T, T, T, T, K,S2,S1,S1,S1,S1,S2, K, T, T, T, T]
    g[20] = [T, T, T, T, T, K,S1,S1,S1,S1, K, T, T, T, T, T]
    g[21] = [T, T, K, R1,R1,R1,WH,BK,BK,WH,R1,R1,R1, K, T, T]
    g[22] = [T, K,S1,S1, K,R1,BK,BK,BK,BK,R1, K,S1,S1, K, T]
    g[23] = [T, K,S1,S1, K,R1,BK,R2,R2,BK,R1, K,S1,S1, K, T]
    g[24] = [T, T, K,S2,S2, K,R1,R1,R1,R1, K,S2,S2, K, T, T]
    g[25] = [T, T, T, T, K, K,BK, Y,Y,BK, K, K, T, T, T, T]
    # Jambes en marche — pied droit avancé
    g[26] = [T, T, T, K, J1,J1,J1, T, T, T,J2,J1, K, T, T, T]
    g[27] = [T, T, K, J1,J1, K, T, T, T, K, J1,J1, K, T, T, T]
    g[28] = [T, T, K,JD, K, T, T, T, T, T, K, J1, K, T, T, T]
    g[29] = [T, K,R1,R1, K, T, T, T, T, K,R1,R1,R1, K, T, T]
    g[30] = [T, K,WH,WH, K, T, T, T, T, T, K,WH,WH, K, T, T]
    return logical_to_image(g)


def make_face_walk2():
    """Pied gauche avancé."""
    g = [[T]*16 for _ in range(32)]
    g[12] = [T, T, T, T, K, K, K, K, K, K, K, K, T, T, T, T]
    g[13] = [T, T, T, K, R1,R1,R1,WH,WH,R1,R1,R1, K, T, T, T]
    g[14] = [T, T, T, K, R1,R1,R1,R1,R1,R1,R1,R1, K, T, T, T]
    g[15] = [T, T, K, R3,R3,R3,R3,R3,R3,R3,R3,R3,R3, K, T, T]
    g[16] = [T, T, K, K, H1,S1,S1,S1,S1,S1,S1,H1, K, K, T, T]
    g[17] = [T, T, T, K, S1, K,WH,S1,S1,WH, K,S1, K, T, T, T]
    g[18] = [T, T, T, K, S1,S2,S1,S1,S1,S1,S2,S1, K, T, T, T]
    g[19] = [T, T, T, T, K,S2,S1,S1,S1,S1,S2, K, T, T, T, T]
    g[20] = [T, T, T, T, T, K,S1,S1,S1,S1, K, T, T, T, T, T]
    g[21] = [T, T, K, R1,R1,R1,WH,BK,BK,WH,R1,R1,R1, K, T, T]
    g[22] = [T, K,S1,S1, K,R1,BK,BK,BK,BK,R1, K,S1,S1, K, T]
    g[23] = [T, K,S1,S1, K,R1,BK,R2,R2,BK,R1, K,S1,S1, K, T]
    g[24] = [T, T, K,S2,S2, K,R1,R1,R1,R1, K,S2,S2, K, T, T]
    g[25] = [T, T, T, T, K, K,BK, Y,Y,BK, K, K, T, T, T, T]
    # Jambes en marche — pied gauche avancé (miroir)
    g[26] = [T, T, T, K, J1,J2, T, T, T,J1,J1,J1, K, T, T, T]
    g[27] = [T, T, T, K, J1,J1, K, T, T, K,J1,J1, K, T, T, T]
    g[28] = [T, T, T, K, J1, K, T, T, T, T, T, K,JD, K, T, T]
    g[29] = [T, T, K, R1,R1,R1, K, T, T, T, K,R1,R1, K, T, T]
    g[30] = [T, T, K, WH,WH, K, T, T, T, T, K,WH,WH, K, T, T]
    return logical_to_image(g)


# ═══════════════════════════════════════════════════════════════
# DOS (haut) — Red FRLG vu de dos
# ═══════════════════════════════════════════════════════════════

def make_back_idle():
    g = [[T]*16 for _ in range(32)]
    # Ligne 12 : sommet casquette
    g[12] = [T, T, T, T, K, K, K, K, K, K, K, K, T, T, T, T]
    # Ligne 13 : casquette dos
    g[13] = [T, T, T, K, R1,R1,R1,R1,R1,R1,R1,R1, K, T, T, T]
    # Ligne 14 : casquette dos
    g[14] = [T, T, T, K, R1,R3,R1,R1,R1,R1,R3,R1, K, T, T, T]
    # Ligne 15 : bas casquette / cheveux arrière
    g[15] = [T, T, K, R3,R3,R3,R3,R3,R3,R3,R3,R3,R3, K, T, T]
    # Ligne 16 : cheveux arrière
    g[16] = [T, T, K, K, H1,H1,H1,H1,H1,H1,H1,H1, K, K, T, T]
    # Ligne 17 : cheveux — texture
    g[17] = [T, T, T, K, H1,H2,H1,H2,H2,H1,H2,H1, K, T, T, T]
    # Ligne 18 : cheveux bas
    g[18] = [T, T, T, T, K, H1,H2,H1,H1,H2,H1, K, T, T, T, T]
    # Ligne 19 : nuque
    g[19] = [T, T, T, T, T, K,S2,S1,S1,S2, K, T, T, T, T, T]
    # Ligne 20 : sac à dos + col
    g[20] = [T, T, K, Y, K, R1,WH,BK,BK,WH,R1, K, Y, K, T, T]
    # Ligne 21 : sac + gilet dos
    g[21] = [T, T, K, Y, K, R1,R1,R1,R1,R1,R1, K, Y, K, T, T]
    # Ligne 22 : bras + sac + gilet
    g[22] = [T, K,S1,S1, K, R1,BK,BK,BK,BK,R1, K,S1,S1, K, T]
    # Ligne 23 : bras + sac
    g[23] = [T, K,S1,S1, K, R1,R3,R1,R1,R3,R1, K,S1,S1, K, T]
    # Ligne 24 : mains + bas gilet
    g[24] = [T, T, K,S2,S2, K, R1,R1,R1,R1, K,S2,S2, K, T, T]
    # Ligne 25 : ceinture
    g[25] = [T, T, T, T, K, K,BK, Y,Y,BK, K, K, T, T, T, T]
    # Ligne 26 : jean
    g[26] = [T, T, T, T, K, J1,J1,J1,J1,J1,J1, K, T, T, T, T]
    # Ligne 27 : jean
    g[27] = [T, T, T, T, K, J1,J1,J2,J2,J1,J1, K, T, T, T, T]
    # Ligne 28 : jean — séparation
    g[28] = [T, T, T, T, K, J1,J1, K, K,J1,J1, K, T, T, T, T]
    # Ligne 29 : sneakers
    g[29] = [T, T, T, K,R1,R1,R1, K, K,R1,R1,R1, K, T, T, T]
    # Ligne 30 : semelles
    g[30] = [T, T, T, T, K,WH,WH, K, K,WH,WH, K, T, T, T, T]
    return logical_to_image(g)


def make_back_walk1():
    g = [[T]*16 for _ in range(32)]
    # Haut identique
    for y, row in enumerate(_back_upper()):
        g[y] = row
    # Jambes marche — pied droit avancé
    g[26] = [T, T, T, K, J1,J1,J1, T, T, T,J2,J1, K, T, T, T]
    g[27] = [T, T, K, J1,J1, K, T, T, T, K, J1,J1, K, T, T, T]
    g[28] = [T, T, K,JD, K, T, T, T, T, T, K, J1, K, T, T, T]
    g[29] = [T, K,R1,R1, K, T, T, T, T, K,R1,R1,R1, K, T, T]
    g[30] = [T, K,WH,WH, K, T, T, T, T, T, K,WH,WH, K, T, T]
    return logical_to_image(g)


def make_back_walk2():
    g = [[T]*16 for _ in range(32)]
    for y, row in enumerate(_back_upper()):
        g[y] = row
    # Jambes marche — pied gauche avancé (miroir)
    g[26] = [T, T, T, K, J1,J2, T, T, T,J1,J1,J1, K, T, T, T]
    g[27] = [T, T, T, K, J1,J1, K, T, T, K,J1,J1, K, T, T, T]
    g[28] = [T, T, T, K, J1, K, T, T, T, T, T, K,JD, K, T, T]
    g[29] = [T, T, K,R1,R1,R1, K, T, T, T, K,R1,R1, K, T, T]
    g[30] = [T, T, K,WH,WH, K, T, T, T, T, K,WH,WH, K, T, T]
    return logical_to_image(g)


def _back_upper():
    """Lignes 0-25 du sprite de dos (partagées entre idle et walk)."""
    rows = [[T]*16 for _ in range(32)]
    rows[12] = [T, T, T, T, K, K, K, K, K, K, K, K, T, T, T, T]
    rows[13] = [T, T, T, K, R1,R1,R1,R1,R1,R1,R1,R1, K, T, T, T]
    rows[14] = [T, T, T, K, R1,R3,R1,R1,R1,R1,R3,R1, K, T, T, T]
    rows[15] = [T, T, K, R3,R3,R3,R3,R3,R3,R3,R3,R3,R3, K, T, T]
    rows[16] = [T, T, K, K, H1,H1,H1,H1,H1,H1,H1,H1, K, K, T, T]
    rows[17] = [T, T, T, K, H1,H2,H1,H2,H2,H1,H2,H1, K, T, T, T]
    rows[18] = [T, T, T, T, K, H1,H2,H1,H1,H2,H1, K, T, T, T, T]
    rows[19] = [T, T, T, T, T, K,S2,S1,S1,S2, K, T, T, T, T, T]
    rows[20] = [T, T, K, Y, K, R1,WH,BK,BK,WH,R1, K, Y, K, T, T]
    rows[21] = [T, T, K, Y, K, R1,R1,R1,R1,R1,R1, K, Y, K, T, T]
    rows[22] = [T, K,S1,S1, K, R1,BK,BK,BK,BK,R1, K,S1,S1, K, T]
    rows[23] = [T, K,S1,S1, K, R1,R3,R1,R1,R3,R1, K,S1,S1, K, T]
    rows[24] = [T, T, K,S2,S2, K, R1,R1,R1,R1, K,S2,S2, K, T, T]
    rows[25] = [T, T, T, T, K, K,BK, Y,Y,BK, K, K, T, T, T, T]
    return rows


# ═══════════════════════════════════════════════════════════════
# PROFIL GAUCHE — Red vu du côté gauche
# ═══════════════════════════════════════════════════════════════

def make_left_idle():
    g = [[T]*16 for _ in range(32)]
    # Casquette (profil — visière étendue à gauche)
    g[12] = [T, T, T, T, T, K, K, K, K, K, K, T, T, T, T, T]
    g[13] = [T, T, T, T, K, R1,R1,R1,R1,R1, K, T, T, T, T, T]
    g[14] = [T, T, T, K, R1,R1,R1,R1,R1,R1,R1, K, T, T, T, T]
    # Visière s'étend vers la gauche
    g[15] = [T, K, R3,R3,R3,R3,R3, K,R3,R3,R3,R3, K, T, T, T]
    # Cheveux + front profil
    g[16] = [T, T, T, K, K, H1,S1,S1,S1,S1,S1,H1, K, T, T, T]
    # Oeil (un seul visible en profil)
    g[17] = [T, T, T, T, K, H1,S1, K,WH,S1,S1, K, T, T, T, T]
    # Nez/joue
    g[18] = [T, T, T, T, K, S1,S1,S1,S1,S2, K, T, T, T, T, T]
    # Menton
    g[19] = [T, T, T, T, T, K,S2,S1,S1,S1, K, T, T, T, T, T]
    # Cou
    g[20] = [T, T, T, T, T, K, S1,S1,S1, K, T, T, T, T, T, T]
    # Épaule + gilet profil + sac dos visible
    g[21] = [T, T, T, T, K, R1,R1,R1,R1,R1, K, Y, K, T, T, T]
    # Bras + gilet + sac
    g[22] = [T, T, T, K,S1,S1,R1,BK,BK,R1, K, Y, K, T, T, T]
    g[23] = [T, T, T, K,S1,S1,R1,BK,R2,R1, K, Y, K, T, T, T]
    # Main + bas gilet
    g[24] = [T, T, T, T, K,S2,S2,R1,R1,R1, K, K, T, T, T, T]
    # Ceinture
    g[25] = [T, T, T, T, T, K,BK, Y,BK,BK, K, T, T, T, T, T]
    # Jean profil
    g[26] = [T, T, T, T, T, K, J1,J2,J1,J1, K, T, T, T, T, T]
    g[27] = [T, T, T, T, K, J1,J1,J1,J1, K, T, T, T, T, T, T]
    # Jean — jambes
    g[28] = [T, T, T, T, K, J1,J1, K,J1,J1, K, T, T, T, T, T]
    # Sneakers
    g[29] = [T, T, T, K, R1,R1,R1, K,R1,R1,R1, K, T, T, T, T]
    # Semelles
    g[30] = [T, T, T, K, WH,WH, K, K,WH,WH, K, T, T, T, T, T]
    return logical_to_image(g)


def make_left_walk1():
    g = [[T]*16 for _ in range(32)]
    # Copier le haut
    for y, row in enumerate(_left_upper()):
        g[y] = row
    # Jambes en marche (profil) — pied avant avancé
    g[26] = [T, T, T, K, J1,J1,J2, T, T,J1,J1, K, T, T, T, T]
    g[27] = [T, T, K, J1,J1, K, T, T, K, J1,J1, K, T, T, T, T]
    g[28] = [T, T, K, JD, K, T, T, T, K, J1,J1, K, T, T, T, T]
    g[29] = [T, K,R1,R1, K, T, T, K,R1,R1,R1, K, T, T, T, T]
    g[30] = [T, K,WH,WH, K, T, T, K,WH,WH, K, T, T, T, T, T]
    return logical_to_image(g)


def make_left_walk2():
    g = [[T]*16 for _ in range(32)]
    for y, row in enumerate(_left_upper()):
        g[y] = row
    # Jambes en marche (profil) — pied arrière avancé
    g[26] = [T, T, T, T, K, J1,J1, T, T,J2,J1, K, T, T, T, T]
    g[27] = [T, T, T, T, K, J1,J1, K, T, K,J1, K, T, T, T, T]
    g[28] = [T, T, T, T, K, J1,J1, K, T, K,JD, K, T, T, T, T]
    g[29] = [T, T, T, K,R1,R1,R1, K, T, K,R1, K, T, T, T, T]
    g[30] = [T, T, T, K,WH,WH, K, T, T, K,WH, K, T, T, T, T]
    return logical_to_image(g)


def _left_upper():
    """Lignes 0-25 du profil gauche (partagées)."""
    rows = [[T]*16 for _ in range(32)]
    rows[12] = [T, T, T, T, T, K, K, K, K, K, K, T, T, T, T, T]
    rows[13] = [T, T, T, T, K, R1,R1,R1,R1,R1, K, T, T, T, T, T]
    rows[14] = [T, T, T, K, R1,R1,R1,R1,R1,R1,R1, K, T, T, T, T]
    rows[15] = [T, K, R3,R3,R3,R3,R3, K,R3,R3,R3,R3, K, T, T, T]
    rows[16] = [T, T, T, K, K, H1,S1,S1,S1,S1,S1,H1, K, T, T, T]
    rows[17] = [T, T, T, T, K, H1,S1, K,WH,S1,S1, K, T, T, T, T]
    rows[18] = [T, T, T, T, K, S1,S1,S1,S1,S2, K, T, T, T, T, T]
    rows[19] = [T, T, T, T, T, K,S2,S1,S1,S1, K, T, T, T, T, T]
    rows[20] = [T, T, T, T, T, K, S1,S1,S1, K, T, T, T, T, T, T]
    rows[21] = [T, T, T, T, K, R1,R1,R1,R1,R1, K, Y, K, T, T, T]
    rows[22] = [T, T, T, K,S1,S1,R1,BK,BK,R1, K, Y, K, T, T, T]
    rows[23] = [T, T, T, K,S1,S1,R1,BK,R2,R1, K, Y, K, T, T, T]
    rows[24] = [T, T, T, T, K,S2,S2,R1,R1,R1, K, K, T, T, T, T]
    rows[25] = [T, T, T, T, T, K,BK, Y,BK,BK, K, T, T, T, T, T]
    return rows


# ═══════════════════════════════════════════════════════════════
# PROFIL DROIT — miroir horizontal du gauche
# ═══════════════════════════════════════════════════════════════

def mirror_h(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


# ═══════════════════════════════════════════════════════════════
# Génération et sauvegarde
# ═══════════════════════════════════════════════════════════════
os.makedirs(OUT_DIR, exist_ok=True)

sprites = {
    "red_normal_bas_0": make_face_idle(),
    "red_normal_bas_1": make_face_walk1(),
    "red_normal_bas_2": make_face_walk2(),
    "red_normal_haut_0": make_back_idle(),
    "red_normal_haut_1": make_back_walk1(),
    "red_normal_haut_2": make_back_walk2(),
    "red_normal_gauche_0": make_left_idle(),
    "red_normal_gauche_1": make_left_walk1(),
    "red_normal_gauche_2": make_left_walk2(),
}

sprites["red_normal_droite_0"] = mirror_h(sprites["red_normal_gauche_0"])
sprites["red_normal_droite_1"] = mirror_h(sprites["red_normal_gauche_1"])
sprites["red_normal_droite_2"] = mirror_h(sprites["red_normal_gauche_2"])

import numpy as np
for name, frame in sprites.items():
    path = os.path.join(OUT_DIR, f"{name}.png")
    frame.save(path, "PNG")
    arr = np.array(frame)
    opaque = int(np.sum(arr[:, :, 3] > 0))
    unique = len(set(tuple(p[:3]) for row in arr for p in row if p[3] > 0))
    # Bounding box
    alpha = arr[:, :, 3]
    rows_mask = np.any(alpha > 0, axis=1)
    cols_mask = np.any(alpha > 0, axis=0)
    if rows_mask.any():
        rmin, rmax = np.where(rows_mask)[0][[0, -1]]
        cmin, cmax = np.where(cols_mask)[0][[0, -1]]
        bbox = f"y{rmin}-{rmax} x{cmin}-{cmax}"
    else:
        bbox = "vide"
    print(f"  ✓ {name}.png: {W}×{H}, {opaque}px opaques, {unique} couleurs, bbox={bbox}")

print(f"\n✓ 12 sprites joueur v7 générés dans {OUT_DIR}")
print(f"  Taille identique aux PNJ : 32×64 (blocs 2×2 = 16×32 logique)")
print(f"  Palette GBA FRLG, style identique à pnj_rival / pnj_chen")
print(f"  Red : casquette rouge+logo blanc, gilet rouge+col blanc, jean bleu, sac jaune")
