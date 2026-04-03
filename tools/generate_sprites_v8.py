#!/usr/bin/env python3
"""
Générateur sprites v8 — Haute qualité FRLG
==========================================
Canvas 32×64 pixels (grille logique 16×32, chaque pixel logique = 2×2).
Génère : Red (joueur), Prof. Chen, rival Blue/Green, PNJ génériques.

Chaque personnage a 12 sprites (4 directions × 3 frames : idle + 2 walk).
Style fidèle aux sprites overworld de Pokémon Rouge Feu / Vert Feuille (GBA).
"""
from PIL import Image, ImageDraw
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "..", "assets", "sprites", "characters")

W, H = 32, 64       # Taille physique du canvas
LW, LH = 16, 32     # Taille logique (grille)

# =============================================================================
# PALETTES DE COULEURS — Style GBA FRLG authentique
# =============================================================================
T = None  # Transparent

# --- Couleurs communes ---
K   = ( 24,  24,  32)   # Contour (noir bleuté, pas noir pur comme sur GBA)
KK  = (  8,   8,  16)   # Contour plus foncé
WHT = (248, 248, 255)   # Blanc
GRY = (192, 192, 200)   # Gris clair

# --- Red (joueur) ---
RED_CAP     = (216,  40,  48)   # Casquette rouge vif
RED_CAP_D   = (176,  24,  32)   # Casquette ombre
RED_CAP_H   = (240,  72,  64)   # Casquette highlight
RED_VISOR   = (136,  16,  24)   # Visière (sombre)
SKIN        = (255, 208, 168)   # Peau claire
SKIN_S      = (232, 176, 128)   # Peau ombre
SKIN_H      = (255, 224, 192)   # Peau highlight
HAIR_BR     = ( 80,  48,  24)   # Cheveux bruns
HAIR_BR_D   = ( 56,  32,  16)   # Cheveux sombres
TSHIRT      = ( 32,  32,  40)   # T-shirt noir
TSHIRT_H    = ( 56,  56,  64)   # T-shirt highlight
VEST_RED    = (200,  48,  48)   # Gilet rouge (ouvert)
VEST_RED_D  = (160,  32,  32)   # Gilet ombre
JEAN        = ( 64,  88, 168)   # Jean bleu
JEAN_D      = ( 48,  64, 128)   # Jean ombre
JEAN_H      = ( 88, 112, 192)   # Jean highlight
SHOE_RED    = (216,  48,  40)   # Sneakers rouges
SHOE_WHT    = (248, 248, 248)   # Semelles blanches
BACKPK      = (232, 192,  48)   # Sac à dos jaune
BACKPK_D    = (192, 152,  32)   # Sac ombre
BELT        = ( 48,  48,  56)   # Ceinture

# --- Prof. Chen (Oak) ---
CHEN_HAIR   = (168, 152, 136)   # Cheveux gris-brun
CHEN_HAIR_D = (136, 120, 104)   # Cheveux ombre
CHEN_COAT   = (248, 248, 248)   # Blouse blanche
CHEN_COAT_D = (216, 216, 224)   # Blouse ombre
CHEN_COAT_H = (255, 255, 255)   # Blouse highlight
CHEN_SHIRT  = (176,  48,  48)   # Chemise rouge en dessous
CHEN_PANTS  = ( 96,  80,  64)   # Pantalon brun
CHEN_PANTS_D= ( 72,  56,  40)   # Pantalon ombre
CHEN_SHOE   = ( 80,  56,  40)   # Chaussures brunes

# --- Rival (Blue/Green) ---
RIV_HAIR    = (128,  80,  40)   # Cheveux auburn
RIV_HAIR_D  = ( 96,  56,  24)   # Cheveux ombre
RIV_SHIRT   = ( 40,  40,  48)   # T-shirt noir
RIV_JACKET  = ( 80,  56, 160)   # Veste violette
RIV_JACKET_D= ( 56,  40, 120)   # Veste ombre
RIV_PANTS   = (112,  80, 168)   # Pantalon
RIV_PANTS_D = ( 80,  56, 128)   # Pantalon ombre
RIV_SHOE    = (104,  88,  72)   # Chaussures

# --- PNJ Homme ---
NPC_M_HAIR  = ( 56,  40,  32)   # Cheveux noirs
NPC_M_SHIRT = ( 48, 120, 200)   # Chemise bleue
NPC_M_SHIRT_D=(32,  88, 160)    # Chemise ombre
NPC_M_PANTS = (104,  88,  72)   # Pantalon kaki
NPC_M_PANTS_D=(80,  64,  48)    # Pantalon ombre

# --- PNJ Femme ---
NPC_F_HAIR  = (160,  72,  40)   # Cheveux roux
NPC_F_HAIR_D= (128,  48,  24)   # Cheveux ombre
NPC_F_DRESS = (232, 104, 136)   # Robe rose
NPC_F_DRESS_D=(200, 72, 104)    # Robe ombre
NPC_F_SHOE  = (200,  72,  56)   # Chaussures

# --- PNJ Vieux ---
NPC_V_HAIR  = (200, 192, 176)   # Cheveux blancs/gris
NPC_V_SHIRT = (112, 136,  96)   # Chemise verte
NPC_V_SHIRT_D=(80, 104, 64)     # Chemise ombre
NPC_V_PANTS = ( 96,  80,  64)   # Pantalon
NPC_V_PANTS_D=(72,  56,  40)    # Pantalon ombre

# --- Infirmière ---
NURSE_HAIR  = (232, 120, 152)   # Cheveux roses
NURSE_HAIR_D= (200,  88, 120)   # Cheveux ombre
NURSE_CAP   = (248, 248, 255)   # Chapeau blanc
NURSE_DRESS = (248, 248, 255)   # Robe blanche
NURSE_DRESS_D=(216, 216, 224)   # Robe ombre
NURSE_CROSS = (216,  48,  48)   # Croix rouge
NURSE_SHOE  = (248, 200, 216)   # Chaussures

# =============================================================================
# MOTEUR DE RENDU
# =============================================================================

def grid_to_image(grid):
    """Convertit une grille logique 16×32 en image 32×64 (pixel logique → 2×2)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    for ly, row in enumerate(grid):
        for lx, col in enumerate(row):
            if col is None:
                continue
            for dy in range(2):
                for dx in range(2):
                    px_x, px_y = lx * 2 + dx, ly * 2 + dy
                    if 0 <= px_x < W and 0 <= px_y < H:
                        px[px_x, px_y] = col + (255,)
    return img


def hmirror(grid):
    """Miroir horizontal d'une grille logique 16 colonnes."""
    return [list(reversed(row)) for row in grid]


def make_grid():
    """Crée une grille vide 16×32."""
    return [[T] * LW for _ in range(LH)]


def copy_rows(src, dst, y_start, y_end):
    """Copie les lignes y_start..y_end-1 de src vers dst."""
    for y in range(y_start, y_end):
        dst[y] = list(src[y])


# =============================================================================
# RED (JOUEUR) — 12 sprites
# =============================================================================

def red_face_idle():
    g = make_grid()
    # -- Casquette (y=10-13) --
    g[10] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[11] = [T,T,T,T, K,RED_CAP,RED_CAP,RED_CAP_H,RED_CAP_H,RED_CAP,RED_CAP, K,T,T,T,T]
    g[12] = [T,T,T, K,RED_CAP,RED_CAP, WHT, WHT,RED_CAP,RED_CAP,RED_CAP,RED_CAP, K,T,T,T]
    g[13] = [T,T, K,RED_VISOR,RED_VISOR,RED_VISOR,RED_VISOR,RED_VISOR,RED_VISOR,RED_VISOR,RED_VISOR,RED_VISOR,RED_VISOR, K,T,T]
    # -- Visage (y=14-18) --
    g[14] = [T,T,T, K,HAIR_BR,SKIN,SKIN,SKIN_H,SKIN_H,SKIN,SKIN,HAIR_BR, K,T,T,T]
    g[15] = [T,T,T, K,SKIN,SKIN, K, K,SKIN,SKIN, K, K,SKIN, K,T,T]  # yeux (noir)
    g[15] = [T,T,T, K,SKIN, K,KK,WHT,SKIN, K,KK,WHT, K,T,T,T]  # yeux détaillés
    g[16] = [T,T,T, K,SKIN,SKIN_S,SKIN,SKIN,SKIN,SKIN,SKIN_S,SKIN, K,T,T,T]
    g[17] = [T,T,T,T, K,SKIN_S,SKIN, K, K,SKIN,SKIN_S, K,T,T,T,T]  # bouche
    g[18] = [T,T,T,T,T, K,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T]  # menton
    # -- Cou --
    g[19] = [T,T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T]
    # -- Torse (y=20-24) : gilet rouge ouvert sur T-shirt noir --
    g[20] = [T,T,T, K,VEST_RED,VEST_RED, WHT,TSHIRT,TSHIRT, WHT,VEST_RED,VEST_RED, K,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,VEST_RED,TSHIRT,TSHIRT,TSHIRT,TSHIRT,VEST_RED, K,SKIN_S, K,T,T]
    g[22] = [T,T, K,SKIN, K,VEST_RED,TSHIRT,TSHIRT_H,TSHIRT_H,TSHIRT,VEST_RED, K,SKIN, K,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,VEST_RED_D,VEST_RED,VEST_RED,VEST_RED_D, K,SKIN_S, K,T,T,T]
    g[24] = [T,T,T,T, K, K,BELT,BELT,BELT,BELT, K, K,T,T,T,T]
    # -- Jean (y=25-28) --
    g[25] = [T,T,T,T, K,JEAN,JEAN,JEAN_H,JEAN_H,JEAN,JEAN, K,T,T,T,T]
    g[26] = [T,T,T,T, K,JEAN,JEAN,JEAN,JEAN,JEAN,JEAN, K,T,T,T,T]
    g[27] = [T,T,T,T, K,JEAN,JEAN_D, K, K,JEAN_D,JEAN, K,T,T,T,T]
    g[28] = [T,T,T,T, K,JEAN_D, K,T,T, K,JEAN_D, K,T,T,T,T]
    # -- Chaussures (y=29-30) --
    g[29] = [T,T,T, K,SHOE_RED,SHOE_RED, K,T,T, K,SHOE_RED,SHOE_RED, K,T,T,T]
    g[30] = [T,T,T, K,SHOE_WHT,SHOE_WHT, K,T,T, K,SHOE_WHT,SHOE_WHT, K,T,T,T]
    return g


def red_face_walk1():
    """Pas droit avancé."""
    g = make_grid()
    idle = red_face_idle()
    copy_rows(idle, g, 10, 25)  # Copier le haut du corps
    # Jambes en mouvement — pied droit avancé
    g[25] = [T,T,T, K,JEAN,JEAN,JEAN_H,T,T,JEAN,JEAN,JEAN, K,T,T,T]
    g[26] = [T,T, K,JEAN,JEAN, K,T,T,T, K,JEAN_D,JEAN, K,T,T,T]
    g[27] = [T,T, K,JEAN_D, K,T,T,T,T,T, K,JEAN_D, K,T,T,T]
    g[28] = [T, K,SHOE_RED,SHOE_RED, K,T,T,T,T, K,SHOE_RED, K,T,T,T,T]
    g[29] = [T, K,SHOE_WHT,SHOE_WHT, K,T,T,T,T,T, K,SHOE_WHT, K,T,T,T]
    return g


def red_face_walk2():
    """Pas gauche avancé (miroir jambes)."""
    g = make_grid()
    idle = red_face_idle()
    copy_rows(idle, g, 10, 25)
    g[25] = [T,T,T, K,JEAN,JEAN,T,T,T,JEAN_H,JEAN,JEAN, K,T,T,T]
    g[26] = [T,T,T, K,JEAN,JEAN_D, K,T,T, K,JEAN,JEAN, K,T,T,T]
    g[27] = [T,T,T, K,JEAN_D, K,T,T,T,T, K,JEAN_D, K,T,T,T]
    g[28] = [T,T,T,T, K,SHOE_RED, K,T,T, K,SHOE_RED,SHOE_RED, K,T,T,T]
    g[29] = [T,T,T, K,SHOE_WHT, K,T,T,T, K,SHOE_WHT,SHOE_WHT, K,T,T,T]
    return g


def red_back_idle():
    g = make_grid()
    # -- Casquette dos (y=10-13) --
    g[10] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[11] = [T,T,T,T, K,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP, K,T,T,T,T]
    g[12] = [T,T,T, K,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP, K,T,T,T]
    g[13] = [T,T,T, K,RED_CAP_D,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP_D, K,T,T,T]
    # -- Arrière tête (y=14-18) --
    g[14] = [T,T,T, K,HAIR_BR,HAIR_BR,HAIR_BR_D,HAIR_BR_D,HAIR_BR_D,HAIR_BR_D,HAIR_BR,HAIR_BR, K,T,T,T]
    g[15] = [T,T,T, K,HAIR_BR,HAIR_BR_D,HAIR_BR_D,HAIR_BR,HAIR_BR,HAIR_BR_D,HAIR_BR_D,HAIR_BR, K,T,T,T]
    g[16] = [T,T,T, K,HAIR_BR,HAIR_BR_D,HAIR_BR_D,HAIR_BR,HAIR_BR,HAIR_BR_D,HAIR_BR_D,HAIR_BR, K,T,T,T]
    g[17] = [T,T,T,T, K,HAIR_BR,SKIN_S,SKIN,SKIN,SKIN_S,HAIR_BR, K,T,T,T,T]
    g[18] = [T,T,T,T,T, K,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T]
    # -- Cou + Dos --
    g[19] = [T,T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T]
    g[20] = [T,T,T, K,VEST_RED,VEST_RED,VEST_RED,TSHIRT,TSHIRT,VEST_RED,VEST_RED,VEST_RED, K,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,VEST_RED,VEST_RED,VEST_RED_D,VEST_RED_D,VEST_RED,VEST_RED, K,SKIN_S, K,T,T]
    g[22] = [T,T, K,SKIN, K,VEST_RED,BACKPK,BACKPK,BACKPK,BACKPK,VEST_RED, K,SKIN, K,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,BACKPK_D,BACKPK,BACKPK,BACKPK_D, K,SKIN_S, K,T,T,T]
    g[24] = [T,T,T,T, K, K,BELT,BELT,BELT,BELT, K, K,T,T,T,T]
    # -- Jean --
    g[25] = [T,T,T,T, K,JEAN,JEAN,JEAN_H,JEAN_H,JEAN,JEAN, K,T,T,T,T]
    g[26] = [T,T,T,T, K,JEAN,JEAN,JEAN,JEAN,JEAN,JEAN, K,T,T,T,T]
    g[27] = [T,T,T,T, K,JEAN,JEAN_D, K, K,JEAN_D,JEAN, K,T,T,T,T]
    g[28] = [T,T,T,T, K,JEAN_D, K,T,T, K,JEAN_D, K,T,T,T,T]
    g[29] = [T,T,T, K,SHOE_RED,SHOE_RED, K,T,T, K,SHOE_RED,SHOE_RED, K,T,T,T]
    g[30] = [T,T,T, K,SHOE_WHT,SHOE_WHT, K,T,T, K,SHOE_WHT,SHOE_WHT, K,T,T,T]
    return g


def red_back_walk1():
    g = make_grid()
    idle = red_back_idle()
    copy_rows(idle, g, 10, 25)
    g[25] = [T,T,T, K,JEAN,JEAN,JEAN_H,T,T,JEAN,JEAN,JEAN, K,T,T,T]
    g[26] = [T,T, K,JEAN,JEAN, K,T,T,T, K,JEAN_D,JEAN, K,T,T,T]
    g[27] = [T,T, K,JEAN_D, K,T,T,T,T,T, K,JEAN_D, K,T,T,T]
    g[28] = [T, K,SHOE_RED,SHOE_RED, K,T,T,T,T, K,SHOE_RED, K,T,T,T,T]
    g[29] = [T, K,SHOE_WHT,SHOE_WHT, K,T,T,T,T,T, K,SHOE_WHT, K,T,T,T]
    return g


def red_back_walk2():
    g = make_grid()
    idle = red_back_idle()
    copy_rows(idle, g, 10, 25)
    g[25] = [T,T,T, K,JEAN,JEAN,T,T,T,JEAN_H,JEAN,JEAN, K,T,T,T]
    g[26] = [T,T,T, K,JEAN,JEAN_D, K,T,T, K,JEAN,JEAN, K,T,T,T]
    g[27] = [T,T,T, K,JEAN_D, K,T,T,T,T, K,JEAN_D, K,T,T,T]
    g[28] = [T,T,T,T, K,SHOE_RED, K,T,T, K,SHOE_RED,SHOE_RED, K,T,T,T]
    g[29] = [T,T,T, K,SHOE_WHT, K,T,T,T, K,SHOE_WHT,SHOE_WHT, K,T,T,T]
    return g


def red_left_idle():
    g = make_grid()
    # -- Casquette profil gauche (visière vers la gauche) --
    g[10] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[11] = [T,T,T, K, K,RED_CAP,RED_CAP,RED_CAP,RED_CAP,RED_CAP, K,T,T,T,T,T]
    g[12] = [T,T, K,RED_VISOR,RED_VISOR, K,RED_CAP,RED_CAP,RED_CAP,RED_CAP, K,T,T,T,T,T]
    g[13] = [T, K,RED_VISOR,RED_VISOR,RED_VISOR, K,RED_CAP_D,RED_CAP,RED_CAP, K,T,T,T,T,T,T]
    # -- Visage profil --
    g[14] = [T,T,T, K,HAIR_BR,SKIN,SKIN,SKIN,SKIN,HAIR_BR_D, K,T,T,T,T,T]
    g[15] = [T,T, K,SKIN,SKIN, K,KK,SKIN,SKIN,SKIN, K,T,T,T,T,T]
    g[16] = [T,T, K,SKIN,SKIN_S,SKIN,SKIN,SKIN,SKIN_S, K,T,T,T,T,T,T]
    g[17] = [T,T,T, K,SKIN_S, K,SKIN,SKIN, K,T,T,T,T,T,T,T]
    g[18] = [T,T,T,T, K,SKIN,SKIN,SKIN, K,T,T,T,T,T,T,T]
    # -- Cou --
    g[19] = [T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T,T]
    # -- Torse profil (gilet + t-shirt + sac dos derrière) --
    g[20] = [T,T,T, K,VEST_RED,TSHIRT,TSHIRT,VEST_RED, K,BACKPK, K,T,T,T,T,T]
    g[21] = [T,T,T, K,SKIN_S, K,TSHIRT,TSHIRT, K,BACKPK,BACKPK_D, K,T,T,T,T]
    g[22] = [T,T,T, K,SKIN, K,TSHIRT_H,TSHIRT, K,BACKPK,BACKPK, K,T,T,T,T]
    g[23] = [T,T,T,T, K,SKIN_S, K,VEST_RED_D, K,BACKPK_D, K,T,T,T,T,T]
    g[24] = [T,T,T,T,T, K,BELT,BELT,BELT, K,T,T,T,T,T,T]
    # -- Jean --
    g[25] = [T,T,T,T, K,JEAN,JEAN,JEAN_H,JEAN, K,T,T,T,T,T,T]
    g[26] = [T,T,T,T, K,JEAN,JEAN,JEAN,JEAN, K,T,T,T,T,T,T]
    g[27] = [T,T,T,T, K,JEAN,JEAN_D, K,JEAN_D, K,T,T,T,T,T,T]
    g[28] = [T,T,T,T, K,JEAN_D, K,T, K,JEAN_D, K,T,T,T,T,T]
    g[29] = [T,T,T, K,SHOE_RED,SHOE_RED, K, K,SHOE_RED, K,T,T,T,T,T,T]
    g[30] = [T,T,T, K,SHOE_WHT,SHOE_WHT, K, K,SHOE_WHT, K,T,T,T,T,T,T]
    return g


def red_left_walk1():
    g = make_grid()
    idle = red_left_idle()
    copy_rows(idle, g, 10, 25)
    g[25] = [T,T,T, K,JEAN,JEAN,JEAN_H, K,JEAN, K,T,T,T,T,T,T]
    g[26] = [T,T, K,JEAN,JEAN, K,T,T, K,JEAN_D, K,T,T,T,T,T]
    g[27] = [T, K,JEAN_D, K,T,T,T,T, K,JEAN_D, K,T,T,T,T,T]
    g[28] = [K,SHOE_RED,SHOE_RED, K,T,T,T,T, K,SHOE_RED, K,T,T,T,T,T]
    g[29] = [K,SHOE_WHT,SHOE_WHT, K,T,T,T,T, K,SHOE_WHT, K,T,T,T,T,T]
    return g


def red_left_walk2():
    g = make_grid()
    idle = red_left_idle()
    copy_rows(idle, g, 10, 25)
    g[25] = [T,T,T,T, K,JEAN,JEAN, K,JEAN_H,JEAN, K,T,T,T,T,T]
    g[26] = [T,T,T,T, K,JEAN_D, K,T, K,JEAN,JEAN, K,T,T,T,T]
    g[27] = [T,T,T,T, K,JEAN_D, K,T,T, K,JEAN_D, K,T,T,T,T]
    g[28] = [T,T,T,T, K,SHOE_RED, K,T, K,SHOE_RED,SHOE_RED, K,T,T,T,T]
    g[29] = [T,T,T,T, K,SHOE_WHT, K,T, K,SHOE_WHT,SHOE_WHT, K,T,T,T,T]
    return g


# =============================================================================
# PROF. CHEN (OAK) — 12 sprites
# =============================================================================

def chen_face_idle():
    g = make_grid()
    # -- Cheveux gris (y=11-13) --
    g[11] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[12] = [T,T,T,T, K,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR, K,T,T,T,T]
    g[13] = [T,T,T, K,CHEN_HAIR,CHEN_HAIR_D,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR_D,CHEN_HAIR, K,T,T,T,T]
    # -- Visage (y=14-18) --
    g[14] = [T,T,T, K,CHEN_HAIR,SKIN,SKIN,SKIN_H,SKIN_H,SKIN,SKIN,CHEN_HAIR, K,T,T,T]
    g[15] = [T,T,T, K,SKIN, K,KK,SKIN,SKIN, K,KK,SKIN, K,T,T,T]
    g[16] = [T,T,T, K,SKIN,SKIN_S,SKIN,SKIN,SKIN,SKIN,SKIN_S,SKIN, K,T,T,T]
    g[17] = [T,T,T,T, K,SKIN_S,SKIN, K, K,SKIN,SKIN_S, K,T,T,T,T]
    g[18] = [T,T,T,T,T, K,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T]
    # -- Cou --
    g[19] = [T,T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T]
    # -- Blouse blanche (y=20-25) --
    g[20] = [T,T,T, K,CHEN_COAT,CHEN_COAT,CHEN_SHIRT,CHEN_SHIRT,CHEN_SHIRT,CHEN_COAT,CHEN_COAT, K,T,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT, K,SKIN_S, K,T,T]
    g[22] = [T,T, K,SKIN, K,CHEN_COAT,CHEN_COAT_H,CHEN_COAT_H,CHEN_COAT_H,CHEN_COAT,CHEN_COAT, K,SKIN, K,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,CHEN_COAT_D,CHEN_COAT,CHEN_COAT,CHEN_COAT_D, K,SKIN_S, K,T,T,T]
    g[24] = [T,T,T,T, K,CHEN_COAT_D,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT_D, K,T,T,T,T]
    g[25] = [T,T,T,T, K, K, K, K, K, K, K, K,T,T,T,T]
    # -- Pantalon (y=26-28) --
    g[26] = [T,T,T,T, K,CHEN_PANTS,CHEN_PANTS,CHEN_PANTS,CHEN_PANTS,CHEN_PANTS,CHEN_PANTS, K,T,T,T,T]
    g[27] = [T,T,T,T, K,CHEN_PANTS,CHEN_PANTS_D, K, K,CHEN_PANTS_D,CHEN_PANTS, K,T,T,T,T]
    g[28] = [T,T,T,T, K,CHEN_PANTS_D, K,T,T, K,CHEN_PANTS_D, K,T,T,T,T]
    # -- Chaussures --
    g[29] = [T,T,T, K,CHEN_SHOE,CHEN_SHOE, K,T,T, K,CHEN_SHOE,CHEN_SHOE, K,T,T,T]
    g[30] = [T,T,T, K, K, K, K,T,T, K, K, K, K,T,T,T]
    return g


def chen_face_walk1():
    g = make_grid()
    idle = chen_face_idle()
    copy_rows(idle, g, 11, 26)
    g[26] = [T,T,T, K,CHEN_PANTS,CHEN_PANTS, K,T,T,CHEN_PANTS,CHEN_PANTS, K,T,T,T,T]
    g[27] = [T,T, K,CHEN_PANTS, K,T,T,T,T, K,CHEN_PANTS_D, K,T,T,T,T]
    g[28] = [T, K,CHEN_SHOE,CHEN_SHOE, K,T,T,T,T, K,CHEN_SHOE, K,T,T,T,T]
    g[29] = [T, K, K, K, K,T,T,T,T, K, K, K,T,T,T,T]
    return g


def chen_face_walk2():
    g = make_grid()
    idle = chen_face_idle()
    copy_rows(idle, g, 11, 26)
    g[26] = [T,T,T,T,CHEN_PANTS,CHEN_PANTS, K,T,T, K,CHEN_PANTS,CHEN_PANTS, K,T,T,T]
    g[27] = [T,T,T,T, K,CHEN_PANTS_D, K,T,T,T, K,CHEN_PANTS, K,T,T,T]
    g[28] = [T,T,T,T, K,CHEN_SHOE, K,T,T, K,CHEN_SHOE,CHEN_SHOE, K,T,T,T]
    g[29] = [T,T,T,T, K, K, K,T,T, K, K, K, K,T,T,T]
    return g


def chen_back_idle():
    g = make_grid()
    g[11] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[12] = [T,T,T,T, K,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR, K,T,T,T,T]
    g[13] = [T,T,T, K,CHEN_HAIR,CHEN_HAIR_D,CHEN_HAIR_D,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR_D,CHEN_HAIR_D, K,T,T,T,T]
    g[14] = [T,T,T, K,CHEN_HAIR_D,CHEN_HAIR_D,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR_D,CHEN_HAIR_D, K,T,T,T]
    g[15] = [T,T,T, K,CHEN_HAIR,CHEN_HAIR_D,CHEN_HAIR_D,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR_D,CHEN_HAIR_D,CHEN_HAIR, K,T,T,T]
    g[16] = [T,T,T, K,CHEN_HAIR,CHEN_HAIR_D,SKIN_S,SKIN,SKIN,SKIN_S,CHEN_HAIR_D,CHEN_HAIR, K,T,T,T]
    g[17] = [T,T,T,T, K,CHEN_HAIR,SKIN_S,SKIN,SKIN,SKIN_S,CHEN_HAIR, K,T,T,T,T]
    g[18] = [T,T,T,T,T, K,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T]
    g[19] = [T,T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T]
    g[20] = [T,T,T, K,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT, K,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,CHEN_COAT,CHEN_COAT_D,CHEN_COAT,CHEN_COAT,CHEN_COAT_D,CHEN_COAT, K,SKIN_S, K,T,T]
    g[22] = [T,T, K,SKIN, K,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT, K,SKIN, K,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,CHEN_COAT_D,CHEN_COAT_D,CHEN_COAT_D,CHEN_COAT_D, K,SKIN_S, K,T,T,T]
    g[24] = [T,T,T,T, K,CHEN_COAT_D,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT,CHEN_COAT_D, K,T,T,T,T]
    g[25] = [T,T,T,T, K, K, K, K, K, K, K, K,T,T,T,T]
    g[26] = [T,T,T,T, K,CHEN_PANTS,CHEN_PANTS,CHEN_PANTS,CHEN_PANTS,CHEN_PANTS,CHEN_PANTS, K,T,T,T,T]
    g[27] = [T,T,T,T, K,CHEN_PANTS,CHEN_PANTS_D, K, K,CHEN_PANTS_D,CHEN_PANTS, K,T,T,T,T]
    g[28] = [T,T,T,T, K,CHEN_PANTS_D, K,T,T, K,CHEN_PANTS_D, K,T,T,T,T]
    g[29] = [T,T,T, K,CHEN_SHOE,CHEN_SHOE, K,T,T, K,CHEN_SHOE,CHEN_SHOE, K,T,T,T]
    g[30] = [T,T,T, K, K, K, K,T,T, K, K, K, K,T,T,T]
    return g


def chen_back_walk1():
    g = make_grid()
    idle = chen_back_idle()
    copy_rows(idle, g, 11, 26)
    g[26] = [T,T,T, K,CHEN_PANTS,CHEN_PANTS, K,T,T,CHEN_PANTS,CHEN_PANTS, K,T,T,T,T]
    g[27] = [T,T, K,CHEN_PANTS, K,T,T,T,T, K,CHEN_PANTS_D, K,T,T,T,T]
    g[28] = [T, K,CHEN_SHOE,CHEN_SHOE, K,T,T,T,T, K,CHEN_SHOE, K,T,T,T,T]
    g[29] = [T, K, K, K, K,T,T,T,T, K, K, K,T,T,T,T]
    return g


def chen_back_walk2():
    g = make_grid()
    idle = chen_back_idle()
    copy_rows(idle, g, 11, 26)
    g[26] = [T,T,T,T,CHEN_PANTS,CHEN_PANTS, K,T,T, K,CHEN_PANTS,CHEN_PANTS, K,T,T,T]
    g[27] = [T,T,T,T, K,CHEN_PANTS_D, K,T,T,T, K,CHEN_PANTS, K,T,T,T]
    g[28] = [T,T,T,T, K,CHEN_SHOE, K,T,T, K,CHEN_SHOE,CHEN_SHOE, K,T,T,T]
    g[29] = [T,T,T,T, K, K, K,T,T, K, K, K, K,T,T,T]
    return g


def chen_left_idle():
    g = make_grid()
    g[11] = [T,T,T,T,T, K, K, K, K, K,T,T,T,T,T,T]
    g[12] = [T,T,T,T, K,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR,CHEN_HAIR, K,T,T,T,T,T,T]
    g[13] = [T,T,T, K,CHEN_HAIR,CHEN_HAIR_D,CHEN_HAIR,CHEN_HAIR, K,T,T,T,T,T,T,T]
    g[14] = [T,T,T, K,CHEN_HAIR,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T,T]
    g[15] = [T,T, K,SKIN,SKIN, K,KK,SKIN,SKIN, K,T,T,T,T,T,T]
    g[16] = [T,T, K,SKIN,SKIN_S,SKIN,SKIN,SKIN, K,T,T,T,T,T,T,T]
    g[17] = [T,T,T, K,SKIN_S, K,SKIN, K,T,T,T,T,T,T,T,T]
    g[18] = [T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T,T,T]
    g[19] = [T,T,T,T,T, K,SKIN, K,T,T,T,T,T,T,T,T]
    g[20] = [T,T,T, K,CHEN_COAT,CHEN_SHIRT,CHEN_COAT, K,T,T,T,T,T,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,CHEN_COAT,CHEN_COAT,CHEN_COAT_D, K,T,T,T,T,T,T,T]
    g[22] = [T,T, K,SKIN, K,CHEN_COAT_H,CHEN_COAT,CHEN_COAT, K,T,T,T,T,T,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,CHEN_COAT_D,CHEN_COAT, K,T,T,T,T,T,T,T]
    g[24] = [T,T,T,T, K,CHEN_COAT_D,CHEN_COAT,CHEN_COAT_D, K,T,T,T,T,T,T,T]
    g[25] = [T,T,T,T, K, K, K, K, K,T,T,T,T,T,T,T]
    g[26] = [T,T,T,T, K,CHEN_PANTS,CHEN_PANTS,CHEN_PANTS, K,T,T,T,T,T,T,T]
    g[27] = [T,T,T,T, K,CHEN_PANTS,CHEN_PANTS_D, K, K,T,T,T,T,T,T,T]
    g[28] = [T,T,T,T, K,CHEN_PANTS_D, K,T, K,T,T,T,T,T,T,T]
    g[29] = [T,T,T, K,CHEN_SHOE,CHEN_SHOE, K, K,CHEN_SHOE, K,T,T,T,T,T,T]
    g[30] = [T,T,T, K, K, K, K, K, K, K,T,T,T,T,T,T]
    return g


def chen_left_walk1():
    g = make_grid()
    idle = chen_left_idle()
    copy_rows(idle, g, 11, 26)
    g[26] = [T,T,T, K,CHEN_PANTS,CHEN_PANTS, K,CHEN_PANTS, K,T,T,T,T,T,T,T]
    g[27] = [T,T, K,CHEN_PANTS, K,T,T, K,CHEN_PANTS_D, K,T,T,T,T,T,T]
    g[28] = [T, K,CHEN_SHOE, K,T,T,T, K,CHEN_SHOE, K,T,T,T,T,T,T]
    g[29] = [T, K, K, K,T,T,T, K, K, K,T,T,T,T,T,T]
    return g


def chen_left_walk2():
    g = make_grid()
    idle = chen_left_idle()
    copy_rows(idle, g, 11, 26)
    g[26] = [T,T,T,T, K,CHEN_PANTS, K,CHEN_PANTS,CHEN_PANTS, K,T,T,T,T,T,T]
    g[27] = [T,T,T,T, K,CHEN_PANTS_D, K,T, K,CHEN_PANTS, K,T,T,T,T,T]
    g[28] = [T,T,T,T, K,CHEN_SHOE, K,T, K,CHEN_SHOE, K,T,T,T,T,T]
    g[29] = [T,T,T,T, K, K, K,T, K, K, K,T,T,T,T,T]
    return g


# =============================================================================
# GENERIC NPC CREATION HELPERS
# =============================================================================

def create_npc_face(hair, hair_d, shirt, shirt_d, pants, pants_d, shoe):
    """Crée un PNJ homme de face (idle)."""
    g = make_grid()
    g[11] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[12] = [T,T,T,T, K,hair,hair,hair,hair,hair,hair, K,T,T,T,T]
    g[13] = [T,T,T, K,hair,hair_d,hair,hair,hair,hair_d,hair, K,T,T,T,T]
    g[14] = [T,T,T, K,hair,SKIN,SKIN,SKIN_H,SKIN_H,SKIN,SKIN,hair, K,T,T,T]
    g[15] = [T,T,T, K,SKIN, K,KK,SKIN,SKIN, K,KK,SKIN, K,T,T,T]
    g[16] = [T,T,T, K,SKIN,SKIN_S,SKIN,SKIN,SKIN,SKIN,SKIN_S,SKIN, K,T,T,T]
    g[17] = [T,T,T,T, K,SKIN_S,SKIN,SKIN,SKIN,SKIN,SKIN_S, K,T,T,T,T]
    g[18] = [T,T,T,T,T, K,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T]
    g[19] = [T,T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T]
    g[20] = [T,T,T, K,shirt,shirt,shirt,shirt,shirt,shirt,shirt, K,T,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,shirt,shirt,shirt_d,shirt_d,shirt,shirt, K,SKIN_S, K,T,T]
    g[22] = [T,T, K,SKIN, K,shirt,shirt,shirt,shirt,shirt,shirt, K,SKIN, K,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,shirt_d,shirt,shirt,shirt_d, K,SKIN_S, K,T,T,T]
    g[24] = [T,T,T,T, K, K, K, K, K, K, K, K,T,T,T,T]
    g[25] = [T,T,T,T, K,pants,pants,pants,pants,pants,pants, K,T,T,T,T]
    g[26] = [T,T,T,T, K,pants,pants,pants,pants,pants,pants, K,T,T,T,T]
    g[27] = [T,T,T,T, K,pants,pants_d, K, K,pants_d,pants, K,T,T,T,T]
    g[28] = [T,T,T,T, K,pants_d, K,T,T, K,pants_d, K,T,T,T,T]
    g[29] = [T,T,T, K,shoe,shoe, K,T,T, K,shoe,shoe, K,T,T,T]
    g[30] = [T,T,T, K, K, K, K,T,T, K, K, K, K,T,T,T]
    return g


def create_npc_back(hair, hair_d, shirt, shirt_d, pants, pants_d, shoe):
    g = make_grid()
    g[11] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[12] = [T,T,T,T, K,hair,hair,hair,hair,hair,hair, K,T,T,T,T]
    g[13] = [T,T,T, K,hair,hair_d,hair_d,hair,hair,hair_d,hair_d, K,T,T,T,T]
    g[14] = [T,T,T, K,hair_d,hair_d,hair,hair,hair,hair,hair_d,hair_d, K,T,T,T]
    g[15] = [T,T,T, K,hair,hair_d,hair_d,hair,hair,hair_d,hair_d,hair, K,T,T,T]
    g[16] = [T,T,T, K,hair,hair,SKIN_S,SKIN,SKIN,SKIN_S,hair,hair, K,T,T,T]
    g[17] = [T,T,T,T, K,hair,SKIN_S,SKIN,SKIN,SKIN_S,hair, K,T,T,T,T]
    g[18] = [T,T,T,T,T, K,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T]
    g[19] = [T,T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T]
    g[20] = [T,T,T, K,shirt,shirt,shirt,shirt,shirt,shirt,shirt, K,T,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,shirt,shirt_d,shirt,shirt,shirt_d,shirt, K,SKIN_S, K,T,T]
    g[22] = [T,T, K,SKIN, K,shirt,shirt,shirt,shirt,shirt,shirt, K,SKIN, K,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,shirt_d,shirt_d,shirt_d,shirt_d, K,SKIN_S, K,T,T,T]
    g[24] = [T,T,T,T, K, K, K, K, K, K, K, K,T,T,T,T]
    g[25] = [T,T,T,T, K,pants,pants,pants,pants,pants,pants, K,T,T,T,T]
    g[26] = [T,T,T,T, K,pants,pants,pants,pants,pants,pants, K,T,T,T,T]
    g[27] = [T,T,T,T, K,pants,pants_d, K, K,pants_d,pants, K,T,T,T,T]
    g[28] = [T,T,T,T, K,pants_d, K,T,T, K,pants_d, K,T,T,T,T]
    g[29] = [T,T,T, K,shoe,shoe, K,T,T, K,shoe,shoe, K,T,T,T]
    g[30] = [T,T,T, K, K, K, K,T,T, K, K, K, K,T,T,T]
    return g


def create_npc_left(hair, hair_d, shirt, shirt_d, pants, pants_d, shoe):
    g = make_grid()
    g[11] = [T,T,T,T,T, K, K, K, K, K,T,T,T,T,T,T]
    g[12] = [T,T,T,T, K,hair,hair,hair,hair, K,T,T,T,T,T,T]
    g[13] = [T,T,T, K,hair,hair_d,hair,hair, K,T,T,T,T,T,T,T]
    g[14] = [T,T,T, K,hair,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T,T]
    g[15] = [T,T, K,SKIN,SKIN, K,KK,SKIN, K,T,T,T,T,T,T,T]
    g[16] = [T,T, K,SKIN,SKIN_S,SKIN,SKIN, K,T,T,T,T,T,T,T,T]
    g[17] = [T,T,T, K,SKIN_S, K,SKIN, K,T,T,T,T,T,T,T,T]
    g[18] = [T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T,T,T]
    g[19] = [T,T,T,T,T, K,SKIN, K,T,T,T,T,T,T,T,T]
    g[20] = [T,T,T, K,shirt,shirt,shirt, K,T,T,T,T,T,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,shirt,shirt,shirt_d, K,T,T,T,T,T,T,T]
    g[22] = [T,T, K,SKIN, K,shirt,shirt,shirt, K,T,T,T,T,T,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,shirt_d,shirt, K,T,T,T,T,T,T,T]
    g[24] = [T,T,T,T, K, K, K, K, K,T,T,T,T,T,T,T]
    g[25] = [T,T,T,T, K,pants,pants,pants, K,T,T,T,T,T,T,T]
    g[26] = [T,T,T,T, K,pants,pants,pants, K,T,T,T,T,T,T,T]
    g[27] = [T,T,T,T, K,pants,pants_d, K, K,T,T,T,T,T,T,T]
    g[28] = [T,T,T,T, K,pants_d, K,T, K,T,T,T,T,T,T,T]
    g[29] = [T,T,T, K,shoe,shoe, K, K,shoe, K,T,T,T,T,T,T]
    g[30] = [T,T,T, K, K, K, K, K, K, K,T,T,T,T,T,T]
    return g


def create_walks_from_idle(idle_func, max_torso_y=25):
    """Crée walk1 et walk2 à partir d'un idle."""
    idle = idle_func()
    
    # Trouver les lignes de jambes/pieds (après max_torso_y)
    # Walk1 : pied droit avancé
    w1 = make_grid()
    copy_rows(idle, w1, 0, max_torso_y + 1)
    
    # Chercher les tiles de pantalon et chaussure
    pants = None
    pants_d = None
    shoe = None
    for y in range(max_torso_y + 1, 31):
        for x in range(16):
            col = idle[y][x]
            if col is not None and col != K and col != KK:
                if pants is None:
                    pants = col
                elif col != pants and pants_d is None:
                    pants_d = col
                elif col != pants and col != pants_d and shoe is None:
                    shoe = col
    
    if pants_d is None: pants_d = pants
    if shoe is None: shoe = K
    
    base_y = max_torso_y + 1
    w1[base_y]   = [T,T,T, K,pants,pants,pants, K,T,T,pants,pants, K,T,T,T]
    w1[base_y+1] = [T,T, K,pants, K,T,T,T,T, K,pants_d, K,T,T,T,T]
    w1[base_y+2] = [T, K,shoe,shoe, K,T,T,T,T, K,shoe, K,T,T,T,T]
    w1[base_y+3] = [T, K, K, K, K,T,T,T,T, K, K, K,T,T,T,T]
    
    w2 = make_grid()
    copy_rows(idle, w2, 0, max_torso_y + 1)
    w2[base_y]   = [T,T,T, K,pants,pants, K,T,T,pants,pants,pants, K,T,T,T]
    w2[base_y+1] = [T,T,T,T, K,pants_d, K,T,T, K,pants, K,T,T,T,T]
    w2[base_y+2] = [T,T,T,T, K,shoe, K,T, K,shoe,shoe, K,T,T,T,T]
    w2[base_y+3] = [T,T,T,T, K, K, K,T, K, K, K, K,T,T,T,T]
    
    return w1, w2


# =============================================================================
# FEMALE NPC — Robe/jupe (forme différente)
# =============================================================================

def create_npc_female_face(hair, hair_d, dress, dress_d, shoe):
    g = make_grid()
    # -- Cheveux longs (y=10-13) --
    g[10] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[11] = [T,T,T,T, K,hair,hair,hair,hair,hair,hair, K,T,T,T,T]
    g[12] = [T,T,T, K,hair,hair_d,hair,hair,hair,hair_d,hair, K,T,T,T,T]
    g[13] = [T,T,T, K,hair,hair,hair,hair,hair,hair,hair,hair, K,T,T,T,T]
    # -- Visage --
    g[14] = [T,T,T, K,hair,SKIN,SKIN,SKIN_H,SKIN_H,SKIN,SKIN,hair, K,T,T,T]
    g[15] = [T,T,T, K,SKIN, K,KK,SKIN,SKIN, K,KK,SKIN, K,T,T,T]
    g[16] = [T,T,T, K,SKIN,SKIN_S,SKIN,SKIN,SKIN,SKIN,SKIN_S,SKIN, K,T,T,T]
    g[17] = [T,T,T, K,hair,SKIN_S,SKIN,SKIN,SKIN,SKIN,SKIN_S,hair, K,T,T,T]
    g[18] = [T,T,T,T, K,SKIN,SKIN,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T]
    # -- Cou --
    g[19] = [T,T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T]
    # -- Robe (y=20-27) --
    g[20] = [T,T,T, K,dress,dress,dress,dress,dress,dress,dress, K,T,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,dress,dress,dress_d,dress_d,dress,dress, K,SKIN_S, K,T,T]
    g[22] = [T,T, K,SKIN, K,dress,dress,dress,dress,dress,dress, K,SKIN, K,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,dress_d,dress,dress,dress_d, K,SKIN_S, K,T,T,T]
    g[24] = [T,T,T,T, K,dress,dress,dress,dress,dress,dress, K,T,T,T,T]
    g[25] = [T,T,T,T, K,dress,dress_d,dress,dress,dress_d,dress, K,T,T,T,T]
    g[26] = [T,T,T,T,T, K,dress_d,dress,dress,dress_d, K,T,T,T,T,T]
    g[27] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    # -- Jambes + chaussures --
    g[28] = [T,T,T,T,T, K,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T]
    g[29] = [T,T,T,T, K,shoe,shoe, K, K,shoe,shoe, K,T,T,T,T]
    g[30] = [T,T,T,T, K, K, K, K, K, K, K, K,T,T,T,T]
    return g


def create_npc_female_back(hair, hair_d, dress, dress_d, shoe):
    g = make_grid()
    g[10] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[11] = [T,T,T,T, K,hair,hair,hair,hair,hair,hair, K,T,T,T,T]
    g[12] = [T,T,T, K,hair,hair_d,hair_d,hair,hair,hair_d,hair_d, K,T,T,T,T]
    g[13] = [T,T,T, K,hair,hair,hair,hair,hair,hair,hair,hair, K,T,T,T,T]
    g[14] = [T,T,T, K,hair_d,hair_d,hair,hair,hair,hair,hair_d,hair_d, K,T,T,T]
    g[15] = [T,T,T, K,hair,hair_d,hair_d,hair,hair,hair_d,hair_d,hair, K,T,T,T]
    g[16] = [T,T,T, K,hair,hair,SKIN_S,SKIN,SKIN,SKIN_S,hair,hair, K,T,T,T]
    g[17] = [T,T,T, K,hair,hair,SKIN_S,SKIN,SKIN,SKIN_S,hair,hair, K,T,T,T]
    g[18] = [T,T,T,T, K,hair,SKIN,SKIN,SKIN,SKIN,hair, K,T,T,T,T]
    g[19] = [T,T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T]
    g[20] = [T,T,T, K,dress,dress,dress,dress,dress,dress,dress, K,T,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,dress,dress_d,dress,dress,dress_d,dress, K,SKIN_S, K,T,T]
    g[22] = [T,T, K,SKIN, K,dress,dress,dress,dress,dress,dress, K,SKIN, K,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,dress_d,dress_d,dress_d,dress_d, K,SKIN_S, K,T,T,T]
    g[24] = [T,T,T,T, K,dress,dress,dress,dress,dress,dress, K,T,T,T,T]
    g[25] = [T,T,T,T, K,dress,dress_d,dress,dress,dress_d,dress, K,T,T,T,T]
    g[26] = [T,T,T,T,T, K,dress_d,dress,dress,dress_d, K,T,T,T,T,T]
    g[27] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[28] = [T,T,T,T,T, K,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T]
    g[29] = [T,T,T,T, K,shoe,shoe, K, K,shoe,shoe, K,T,T,T,T]
    g[30] = [T,T,T,T, K, K, K, K, K, K, K, K,T,T,T,T]
    return g


def create_npc_female_left(hair, hair_d, dress, dress_d, shoe):
    g = make_grid()
    g[11] = [T,T,T,T, K, K, K, K, K,T,T,T,T,T,T,T]
    g[12] = [T,T,T, K,hair,hair,hair,hair, K,T,T,T,T,T,T,T]
    g[13] = [T,T, K,hair,hair_d,hair,hair,hair, K,T,T,T,T,T,T,T]
    g[14] = [T,T, K,hair,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T,T,T]
    g[15] = [T, K,SKIN,SKIN, K,KK,SKIN, K,T,T,T,T,T,T,T,T]
    g[16] = [T,T, K,SKIN,SKIN_S,SKIN,SKIN, K,T,T,T,T,T,T,T,T]
    g[17] = [T,T, K,hair,SKIN_S, K,SKIN, K,T,T,T,T,T,T,T,T]
    g[18] = [T,T,T, K,SKIN,SKIN,SKIN, K,T,T,T,T,T,T,T,T]
    g[19] = [T,T,T,T, K,SKIN, K,T,T,T,T,T,T,T,T,T]
    g[20] = [T,T,T, K,dress,dress,dress, K,T,T,T,T,T,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,dress,dress,dress_d, K,T,T,T,T,T,T,T]
    g[22] = [T,T, K,SKIN, K,dress,dress,dress, K,T,T,T,T,T,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,dress_d,dress, K,T,T,T,T,T,T,T]
    g[24] = [T,T,T,T, K,dress,dress,dress, K,T,T,T,T,T,T,T]
    g[25] = [T,T,T,T, K,dress_d,dress,dress_d, K,T,T,T,T,T,T,T]
    g[26] = [T,T,T,T,T, K,dress,dress, K,T,T,T,T,T,T,T]
    g[27] = [T,T,T,T,T, K, K, K, K,T,T,T,T,T,T,T]
    g[28] = [T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T,T,T]
    g[29] = [T,T,T, K,shoe,shoe, K,shoe, K,T,T,T,T,T,T,T]
    g[30] = [T,T,T, K, K, K, K, K, K,T,T,T,T,T,T,T]
    return g


# =============================================================================
# INFIRMIÈRE (Nurse Joy)
# =============================================================================

def nurse_face_idle():
    g = make_grid()
    # Chapeau blanc avec croix
    g[10] = [T,T,T,T,T, K, K, K, K, K,T,T,T,T,T,T]
    g[11] = [T,T,T,T, K,NURSE_CAP,NURSE_CAP,NURSE_CROSS,NURSE_CAP,NURSE_CAP, K,T,T,T,T,T]
    g[12] = [T,T,T, K,NURSE_HAIR,NURSE_HAIR,NURSE_HAIR,NURSE_HAIR,NURSE_HAIR,NURSE_HAIR,NURSE_HAIR, K,T,T,T,T]
    g[13] = [T,T,T, K,NURSE_HAIR,NURSE_HAIR_D,NURSE_HAIR,NURSE_HAIR,NURSE_HAIR,NURSE_HAIR_D,NURSE_HAIR, K,T,T,T,T]
    g[14] = [T,T,T, K,NURSE_HAIR,SKIN,SKIN,SKIN_H,SKIN_H,SKIN,SKIN,NURSE_HAIR, K,T,T,T]
    g[15] = [T,T,T, K,SKIN, K,KK,SKIN,SKIN, K,KK,SKIN, K,T,T,T]
    g[16] = [T,T,T, K,SKIN,SKIN_S,SKIN,SKIN,SKIN,SKIN,SKIN_S,SKIN, K,T,T,T]
    g[17] = [T,T,T,T, K,SKIN_S,SKIN,SKIN,SKIN,SKIN,SKIN_S, K,T,T,T,T]
    g[18] = [T,T,T,T,T, K,SKIN,SKIN,SKIN,SKIN, K,T,T,T,T,T]
    g[19] = [T,T,T,T,T,T, K,SKIN,SKIN, K,T,T,T,T,T,T]
    # Robe blanche d'infirmière avec croix rouge
    g[20] = [T,T,T, K,NURSE_DRESS,NURSE_DRESS,NURSE_CROSS,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS, K,T,T,T,T,T]
    g[21] = [T,T, K,SKIN_S, K,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS_D,NURSE_DRESS,NURSE_DRESS, K,SKIN_S, K,T,T,T]
    g[22] = [T,T, K,SKIN, K,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS, K,SKIN, K,T,T,T]
    g[23] = [T,T,T, K,SKIN_S, K,NURSE_DRESS_D,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS_D, K,SKIN_S, K,T,T,T]
    g[24] = [T,T,T,T, K,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS, K,T,T,T,T,T]
    g[25] = [T,T,T,T, K,NURSE_DRESS_D,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS_D, K,T,T,T,T,T]
    g[26] = [T,T,T,T,T, K,NURSE_DRESS,NURSE_DRESS,NURSE_DRESS, K,T,T,T,T,T,T]
    g[27] = [T,T,T,T,T, K, K, K, K, K,T,T,T,T,T,T]
    g[28] = [T,T,T,T,T, K,SKIN,SKIN,SKIN, K,T,T,T,T,T,T]
    g[29] = [T,T,T,T, K,NURSE_SHOE,NURSE_SHOE, K,NURSE_SHOE,NURSE_SHOE, K,T,T,T,T,T]
    g[30] = [T,T,T,T, K, K, K, K, K, K, K,T,T,T,T,T]
    return g


# =============================================================================
# OBJETS SPÉCIAUX (non-personnages)
# =============================================================================

def create_sign():
    """Panneau en bois."""
    g = make_grid()
    WOOD = (168, 120, 72)
    WOOD_D = (136, 88, 48)
    WOOD_H = (200, 152, 96)
    POST = (120, 80, 40)
    # Panneau (y=18-24)
    g[18] = [T,T,T,T, K, K, K, K, K, K, K, K,T,T,T,T]
    g[19] = [T,T,T, K,WOOD,WOOD,WOOD_H,WOOD_H,WOOD_H,WOOD_H,WOOD,WOOD, K,T,T,T]
    g[20] = [T,T,T, K,WOOD,WOOD,WOOD,WOOD,WOOD,WOOD,WOOD,WOOD, K,T,T,T]
    g[21] = [T,T,T, K,WOOD_D,WOOD,WOOD,WOOD,WOOD,WOOD,WOOD,WOOD_D, K,T,T,T]
    g[22] = [T,T,T, K,WOOD_D,WOOD,WOOD,WOOD,WOOD,WOOD,WOOD,WOOD_D, K,T,T,T]
    g[23] = [T,T,T, K, K, K, K, K, K, K, K, K, K,T,T,T]
    # Poteau
    g[24] = [T,T,T,T,T,T, K,POST,POST, K,T,T,T,T,T,T]
    g[25] = [T,T,T,T,T,T, K,POST,POST, K,T,T,T,T,T,T]
    g[26] = [T,T,T,T,T,T, K,POST,POST, K,T,T,T,T,T,T]
    g[27] = [T,T,T,T,T,T, K,POST,POST, K,T,T,T,T,T,T]
    return g


def create_pc():
    """Terminal PC."""
    g = make_grid()
    BX = (160, 168, 184)  # Boîtier gris
    BX_D = (120, 128, 144)
    SCR = (64, 200, 120)  # Écran vert
    SCR_D = (40, 160, 88)
    g[16] = [T,T,T,T, K, K, K, K, K, K, K, K,T,T,T,T]
    g[17] = [T,T,T, K,BX,BX,BX,BX,BX,BX,BX,BX, K,T,T,T]
    g[18] = [T,T,T, K,BX, K,SCR,SCR,SCR,SCR, K,BX, K,T,T,T]
    g[19] = [T,T,T, K,BX, K,SCR,SCR_D,SCR,SCR_D, K,BX, K,T,T,T]
    g[20] = [T,T,T, K,BX, K,SCR_D,SCR,SCR_D,SCR, K,BX, K,T,T,T]
    g[21] = [T,T,T, K,BX, K,SCR,SCR,SCR,SCR, K,BX, K,T,T,T]
    g[22] = [T,T,T, K,BX, K, K, K, K, K, K,BX, K,T,T,T]
    g[23] = [T,T,T, K,BX_D,BX_D,BX_D,BX_D,BX_D,BX_D,BX_D,BX_D, K,T,T,T]
    g[24] = [T,T,T, K, K, K, K, K, K, K, K, K, K,T,T,T]
    g[25] = [T,T,T,T,T, K,BX_D,BX_D,BX_D,BX_D, K,T,T,T,T,T]
    g[26] = [T,T,T,T,T, K,BX_D,BX_D,BX_D,BX_D, K,T,T,T,T,T]
    return g


def create_item_sol():
    """Objet au sol (Poké Ball)."""
    g = make_grid()
    R = (216, 40, 48)
    R_D = (176, 24, 32)
    g[22] = [T,T,T,T,T,T, K, K, K, K,T,T,T,T,T,T]
    g[23] = [T,T,T,T,T, K,R,R,R,R, K,T,T,T,T,T]
    g[24] = [T,T,T,T, K,R,R_D,R,R,R_D,R, K,T,T,T,T]
    g[25] = [T,T,T,T, K, K, K,WHT,WHT, K, K, K,T,T,T,T]
    g[26] = [T,T,T,T, K,WHT,WHT,WHT,WHT,WHT,WHT, K,T,T,T,T]
    g[27] = [T,T,T,T,T, K,WHT,WHT,WHT,WHT, K,T,T,T,T,T]
    g[28] = [T,T,T,T,T,T, K, K, K, K,T,T,T,T,T,T]
    return g


def create_ronflex():
    """Ronflex (Snorlax) bloquant le passage."""
    g = make_grid()
    BD = (56, 80, 104)     # Corps bleu foncé
    BD_D = (40, 64, 80)
    BLY = (200, 192, 168)   # Ventre beige
    BLY_D = (168, 160, 136)
    g[12] = [T,T,T,T, K, K, K, K, K, K, K, K,T,T,T,T]
    g[13] = [T,T,T, K,BD,BD,BD,BD,BD,BD,BD,BD, K,T,T,T]
    g[14] = [T,T, K,BD,BD, K, K,BD,BD, K, K,BD,BD, K,T,T]
    g[15] = [T,T, K,BD,BD,BD,BD,BD,BD,BD,BD,BD,BD, K,T,T]
    g[16] = [T,T, K,BD,BD,BD, K,BD,BD, K,BD,BD,BD, K,T,T]
    g[17] = [T, K,BD,BD,BD,BD,BD,BD,BD,BD,BD,BD,BD,BD, K,T]
    g[18] = [T, K,BD,BD,BD,BLY,BLY,BLY,BLY,BLY,BLY,BD,BD, K,T,T]
    g[19] = [T, K,BD,BD,BLY,BLY,BLY_D,BLY,BLY,BLY_D,BLY,BLY,BD, K,T,T]
    g[20] = [T, K,BD,BD,BLY,BLY,BLY,BLY,BLY,BLY,BLY,BLY,BD, K,T,T]
    g[21] = [T, K,BD,BD,BLY,BLY_D,BLY,BLY,BLY,BLY,BLY_D,BLY,BD, K,T,T]
    g[22] = [T, K,BD,BD,BD,BLY,BLY,BLY,BLY,BLY,BLY,BD,BD, K,T,T]
    g[23] = [T, K,BD_D,BD,BD,BD,BD,BD,BD,BD,BD,BD,BD_D, K,T,T]
    g[24] = [T, K,BD_D,BD_D,BD_D, K, K, K, K, K,BD_D,BD_D,BD_D, K,T,T]
    g[25] = [T,T, K,BD_D, K,BD_D,BD_D, K,BD_D,BD_D, K,BD_D, K,T,T,T]
    g[26] = [T,T, K, K,T, K, K, K, K, K,T, K, K,T,T,T]
    return g


def create_legendary():
    """Pokémon légendaire (silhouette violet/bleu mystique)."""
    g = make_grid()
    LP = (120, 72, 200)    # Corps violet
    LP_D = (88, 48, 168)
    LP_H = (152, 104, 232)
    EY = (248, 216, 72)     # Yeux jaunes
    g[12] = [T,T,T,T,T, K, K, K, K, K, K,T,T,T,T,T]
    g[13] = [T,T,T,T, K,LP,LP,LP_H,LP_H,LP,LP, K,T,T,T,T]
    g[14] = [T,T,T, K,LP,LP_H,LP,LP,LP,LP,LP_H,LP, K,T,T,T]
    g[15] = [T,T,T, K,LP, K,EY,LP,LP, K,EY,LP, K,T,T,T]
    g[16] = [T,T, K,LP,LP,LP,LP,LP,LP,LP,LP,LP,LP, K,T,T]
    g[17] = [T,T, K,LP_D,LP,LP, K,LP, K,LP,LP,LP_D, K,T,T,T]
    g[18] = [T, K,LP,LP_D,LP,LP,LP,LP,LP,LP,LP,LP_D,LP, K,T,T]
    g[19] = [T, K,LP,LP,LP_D,LP,LP,LP,LP,LP,LP_D,LP,LP, K,T,T]
    g[20] = [T, K,LP,LP,LP,LP_D,LP_D,LP_D,LP_D,LP_D,LP,LP,LP, K,T,T]
    g[21] = [T,T, K,LP,LP,LP,LP,LP,LP,LP,LP,LP, K,T,T,T]
    g[22] = [T,T,T, K,LP_D,LP,LP,LP,LP,LP,LP_D, K,T,T,T,T]
    g[23] = [T,T,T, K, K,LP_D,LP_D, K,LP_D,LP_D, K, K,T,T,T,T]
    g[24] = [T,T,T,T, K, K, K,T, K, K, K,T,T,T,T,T]
    return g


# =============================================================================
# GENERATION PRINCIPALE
# =============================================================================

# Définir tous les personnages à générer
CHARACTERS = {
    # --- Joueur (Red) ---
    "red_normal": {
        "bas":    [red_face_idle, red_face_walk1, red_face_walk2],
        "haut":   [red_back_idle, red_back_walk1, red_back_walk2],
        "gauche": [red_left_idle, red_left_walk1, red_left_walk2],
        "droite": "mirror_gauche",
    },
    # --- Prof. Chen ---
    "pnj_chen": {
        "bas":    [chen_face_idle, chen_face_walk1, chen_face_walk2],
        "haut":   [chen_back_idle, chen_back_walk1, chen_back_walk2],
        "gauche": [chen_left_idle, chen_left_walk1, chen_left_walk2],
        "droite": "mirror_gauche",
    },
    "prof_chen": "alias:pnj_chen",
    # --- PNJ Homme ---
    "pnj_homme": {
        "bas":    [lambda: create_npc_face(NPC_M_HAIR, NPC_M_HAIR, NPC_M_SHIRT, NPC_M_SHIRT_D, NPC_M_PANTS, NPC_M_PANTS_D, (80, 64, 48))],
        "haut":   [lambda: create_npc_back(NPC_M_HAIR, NPC_M_HAIR, NPC_M_SHIRT, NPC_M_SHIRT_D, NPC_M_PANTS, NPC_M_PANTS_D, (80, 64, 48))],
        "gauche": [lambda: create_npc_left(NPC_M_HAIR, NPC_M_HAIR, NPC_M_SHIRT, NPC_M_SHIRT_D, NPC_M_PANTS, NPC_M_PANTS_D, (80, 64, 48))],
        "droite": "mirror_gauche",
    },
    # --- PNJ Femme ---
    "pnj_femme": {
        "bas":    [lambda: create_npc_female_face(NPC_F_HAIR, NPC_F_HAIR_D, NPC_F_DRESS, NPC_F_DRESS_D, NPC_F_SHOE)],
        "haut":   [lambda: create_npc_female_back(NPC_F_HAIR, NPC_F_HAIR_D, NPC_F_DRESS, NPC_F_DRESS_D, NPC_F_SHOE)],
        "gauche": [lambda: create_npc_female_left(NPC_F_HAIR, NPC_F_HAIR_D, NPC_F_DRESS, NPC_F_DRESS_D, NPC_F_SHOE)],
        "droite": "mirror_gauche",
    },
    # --- PNJ Vieux ---
    "pnj_vieux": {
        "bas":    [lambda: create_npc_face(NPC_V_HAIR, NPC_V_HAIR, NPC_V_SHIRT, NPC_V_SHIRT_D, NPC_V_PANTS, NPC_V_PANTS_D, (72, 56, 40))],
        "haut":   [lambda: create_npc_back(NPC_V_HAIR, NPC_V_HAIR, NPC_V_SHIRT, NPC_V_SHIRT_D, NPC_V_PANTS, NPC_V_PANTS_D, (72, 56, 40))],
        "gauche": [lambda: create_npc_left(NPC_V_HAIR, NPC_V_HAIR, NPC_V_SHIRT, NPC_V_SHIRT_D, NPC_V_PANTS, NPC_V_PANTS_D, (72, 56, 40))],
        "droite": "mirror_gauche",
    },
    "pnj_vieil_homme": "alias:pnj_vieux",
    # --- Infirmière ---
    "pnj_infirmiere": {
        "bas":    [nurse_face_idle],
        "haut":   [lambda: create_npc_female_back(NURSE_HAIR, NURSE_HAIR_D, NURSE_DRESS, NURSE_DRESS_D, NURSE_SHOE)],
        "gauche": [lambda: create_npc_female_left(NURSE_HAIR, NURSE_HAIR_D, NURSE_DRESS, NURSE_DRESS_D, NURSE_SHOE)],
        "droite": "mirror_gauche",
    },
    "infirmiere": "alias:pnj_infirmiere",
    # --- Vendeur ---
    "pnj_vendeur": {
        "bas":    [lambda: create_npc_face((56, 40, 32), (56, 40, 32), (80, 136, 64), (56, 104, 40), (104, 88, 72), (80, 64, 48), (80, 56, 40))],
        "haut":   [lambda: create_npc_back((56, 40, 32), (56, 40, 32), (80, 136, 64), (56, 104, 40), (104, 88, 72), (80, 64, 48), (80, 56, 40))],
        "gauche": [lambda: create_npc_left((56, 40, 32), (56, 40, 32), (80, 136, 64), (56, 104, 40), (104, 88, 72), (80, 64, 48), (80, 56, 40))],
        "droite": "mirror_gauche",
    },
    "vendeur": "alias:pnj_vendeur",

    # --- Rival (Blue/Green) ---
    "pnj_rival": {
        "bas":    [lambda: create_npc_face(RIV_HAIR, RIV_HAIR_D, RIV_JACKET, RIV_JACKET_D, RIV_PANTS, RIV_PANTS_D, RIV_SHOE)],
        "haut":   [lambda: create_npc_back(RIV_HAIR, RIV_HAIR_D, RIV_JACKET, RIV_JACKET_D, RIV_PANTS, RIV_PANTS_D, RIV_SHOE)],
        "gauche": [lambda: create_npc_left(RIV_HAIR, RIV_HAIR_D, RIV_JACKET, RIV_JACKET_D, RIV_PANTS, RIV_PANTS_D, RIV_SHOE)],
        "droite": "mirror_gauche",
    },

    # --- Dresseur (homme générique) ---
    "pnj_dresseur": {
        "bas":    [lambda: create_npc_face((80,56,32), (56,40,24), (200,64,64), (168,40,40), (48,48,120), (32,32,88), (80,56,40))],
        "haut":   [lambda: create_npc_back((80,56,32), (56,40,24), (200,64,64), (168,40,40), (48,48,120), (32,32,88), (80,56,40))],
        "gauche": [lambda: create_npc_left((80,56,32), (56,40,24), (200,64,64), (168,40,40), (48,48,120), (32,32,88), (80,56,40))],
        "droite": "mirror_gauche",
    },
    "pnj_dresseur_m": "alias:pnj_dresseur",
    "dresseur": "alias:pnj_dresseur",
    "dresseur_m": "alias:pnj_dresseur",

    # --- Dresseuse ---
    "dresseur_f": {
        "bas":    [lambda: create_npc_female_face((160,72,40), (128,48,24), (240,120,120), (208,88,88), (200,72,56))],
        "haut":   [lambda: create_npc_female_back((160,72,40), (128,48,24), (240,120,120), (208,88,88), (200,72,56))],
        "gauche": [lambda: create_npc_female_left((160,72,40), (128,48,24), (240,120,120), (208,88,88), (200,72,56))],
        "droite": "mirror_gauche",
    },

    # --- Gamin / Garçon ---
    "pnj_gamin": {
        "bas":    [lambda: create_npc_face((80,56,32), (64,40,24), (248,200,48), (216,168,32), (80,128,64), (56,96,40), (200,72,56))],
        "haut":   [lambda: create_npc_back((80,56,32), (64,40,24), (248,200,48), (216,168,32), (80,128,64), (56,96,40), (200,72,56))],
        "gauche": [lambda: create_npc_left((80,56,32), (64,40,24), (248,200,48), (216,168,32), (80,128,64), (56,96,40), (200,72,56))],
        "droite": "mirror_gauche",
    },
    "pnj_garcon": "alias:pnj_gamin",

    # --- Gamine / Fillette / Fille ---
    "pnj_gamine": {
        "bas":    [lambda: create_npc_female_face((56,40,32), (40,28,20), (248,168,96), (216,136,64), (200,72,56))],
        "haut":   [lambda: create_npc_female_back((56,40,32), (40,28,20), (248,168,96), (216,136,64), (200,72,56))],
        "gauche": [lambda: create_npc_female_left((56,40,32), (40,28,20), (248,168,96), (216,136,64), (200,72,56))],
        "droite": "mirror_gauche",
    },
    "pnj_fille": "alias:pnj_gamine",
    "pnj_fillette": "alias:pnj_gamine",

    # --- Campeur ---
    "pnj_campeur": {
        "bas":    [lambda: create_npc_face((56,40,32), (40,28,20), (80,136,64), (56,104,40), (104,88,72), (80,64,48), (88,72,56))],
        "haut":   [lambda: create_npc_back((56,40,32), (40,28,20), (80,136,64), (56,104,40), (104,88,72), (80,64,48), (88,72,56))],
        "gauche": [lambda: create_npc_left((56,40,32), (40,28,20), (80,136,64), (56,104,40), (104,88,72), (80,64,48), (88,72,56))],
        "droite": "mirror_gauche",
    },

    # --- Insectomane (Bug Catcher) ---
    "pnj_insectomane": {
        "bas":    [lambda: create_npc_face((80,56,32), (56,40,24), (248,248,232), (216,216,200), (104,160,88), (72,128,56), (80,56,40))],
        "haut":   [lambda: create_npc_back((80,56,32), (56,40,24), (248,248,232), (216,216,200), (104,160,88), (72,128,56), (80,56,40))],
        "gauche": [lambda: create_npc_left((80,56,32), (56,40,24), (248,248,232), (216,216,200), (104,160,88), (72,128,56), (80,56,40))],
        "droite": "mirror_gauche",
    },

    # --- Karatéka ---
    "pnj_karateka": {
        "bas":    [lambda: create_npc_face((56,40,32), (40,28,20), (248,248,248), (216,216,216), (248,248,248), (216,216,216), (40,40,40))],
        "haut":   [lambda: create_npc_back((56,40,32), (40,28,20), (248,248,248), (216,216,216), (248,248,248), (216,216,216), (40,40,40))],
        "gauche": [lambda: create_npc_left((56,40,32), (40,28,20), (248,248,248), (216,216,216), (248,248,248), (216,216,216), (40,40,40))],
        "droite": "mirror_gauche",
    },

    # --- Jongleur ---
    "pnj_jongleur": {
        "bas":    [lambda: create_npc_face((200,56,56), (168,40,40), (160,64,192), (128,40,160), (160,64,192), (128,40,160), (96,48,128))],
        "haut":   [lambda: create_npc_back((200,56,56), (168,40,40), (160,64,192), (128,40,160), (160,64,192), (128,40,160), (96,48,128))],
        "gauche": [lambda: create_npc_left((200,56,56), (168,40,40), (160,64,192), (128,40,160), (160,64,192), (128,40,160), (96,48,128))],
        "droite": "mirror_gauche",
    },

    # --- Médium (Channeler) --- violet + mystique
    "pnj_medium": {
        "bas":    [lambda: create_npc_female_face((96,56,144), (72,40,112), (120,72,168), (88,48,136), (112,72,144))],
        "haut":   [lambda: create_npc_female_back((96,56,144), (72,40,112), (120,72,168), (88,48,136), (112,72,144))],
        "gauche": [lambda: create_npc_female_left((96,56,144), (72,40,112), (120,72,168), (88,48,136), (112,72,144))],
        "droite": "mirror_gauche",
    },

    # --- Montagnard / Randonneur (Hiker) ---
    "pnj_montagnard": {
        "bas":    [lambda: create_npc_face((104,72,40), (80,48,24), (136,96,48), (104,72,32), (96,80,56), (72,56,40), (88,64,40))],
        "haut":   [lambda: create_npc_back((104,72,40), (80,48,24), (136,96,48), (104,72,32), (96,80,56), (72,56,40), (88,64,40))],
        "gauche": [lambda: create_npc_left((104,72,40), (80,48,24), (136,96,48), (104,72,32), (96,80,56), (72,56,40), (88,64,40))],
        "droite": "mirror_gauche",
    },
    "pnj_randonneur": "alias:pnj_montagnard",
    "dresseur_randonneur": "alias:pnj_montagnard",

    # --- Randonneuse ---
    "pnj_randonneuse": {
        "bas":    [lambda: create_npc_female_face((104,72,40), (80,48,24), (136,112,72), (104,80,48), (96,72,48))],
        "haut":   [lambda: create_npc_female_back((104,72,40), (80,48,24), (136,112,72), (104,80,48), (96,72,48))],
        "gauche": [lambda: create_npc_female_left((104,72,40), (80,48,24), (136,112,72), (104,80,48), (96,72,48))],
        "droite": "mirror_gauche",
    },

    # --- Marin ---
    "pnj_marin": {
        "bas":    [lambda: create_npc_face((56,40,32), (40,28,20), (248,248,255), (216,216,224), (64,88,168), (48,64,128), (56,40,32))],
        "haut":   [lambda: create_npc_back((56,40,32), (40,28,20), (248,248,255), (216,216,224), (64,88,168), (48,64,128), (56,40,32))],
        "gauche": [lambda: create_npc_left((56,40,32), (40,28,20), (248,248,255), (216,216,224), (64,88,168), (48,64,128), (56,40,32))],
        "droite": "mirror_gauche",
    },
    "pnj_capitaine": "alias:pnj_marin",

    # --- Nageur --- (torse nu bleu)
    "pnj_nageur": {
        "bas":    [lambda: create_npc_face((56,40,32), (40,28,20), (48,120,200), (32,88,160), (48,120,200), (32,88,160), (48,120,200))],
        "haut":   [lambda: create_npc_back((56,40,32), (40,28,20), (48,120,200), (32,88,160), (48,120,200), (32,88,160), (48,120,200))],
        "gauche": [lambda: create_npc_left((56,40,32), (40,28,20), (48,120,200), (32,88,160), (48,120,200), (32,88,160), (48,120,200))],
        "droite": "mirror_gauche",
    },

    # --- Nageuse ---
    "pnj_nageuse": {
        "bas":    [lambda: create_npc_female_face((56,40,32), (40,28,20), (200,72,88), (168,48,64), (200,72,88))],
        "haut":   [lambda: create_npc_female_back((56,40,32), (40,28,20), (200,72,88), (168,48,64), (200,72,88))],
        "gauche": [lambda: create_npc_female_left((56,40,32), (40,28,20), (200,72,88), (168,48,64), (200,72,88))],
        "droite": "mirror_gauche",
    },

    # --- Pêcheur ---
    "pnj_pecheur": {
        "bas":    [lambda: create_npc_face((168,152,136), (136,120,104), (232,200,128), (200,168,96), (120,96,64), (88,64,40), (80,56,40))],
        "haut":   [lambda: create_npc_back((168,152,136), (136,120,104), (232,200,128), (200,168,96), (120,96,64), (88,64,40), (80,56,40))],
        "gauche": [lambda: create_npc_left((168,152,136), (136,120,104), (232,200,128), (200,168,96), (120,96,64), (88,64,40), (80,56,40))],
        "droite": "mirror_gauche",
    },

    # --- Motard (Biker) ---
    "pnj_motard": {
        "bas":    [lambda: create_npc_face((56,40,32), (40,28,20), (40,40,48), (24,24,32), (40,40,48), (24,24,32), (56,40,32))],
        "haut":   [lambda: create_npc_back((56,40,32), (40,28,20), (40,40,48), (24,24,32), (40,40,48), (24,24,32), (56,40,32))],
        "gauche": [lambda: create_npc_left((56,40,32), (40,28,20), (40,40,48), (24,24,32), (40,40,48), (24,24,32), (56,40,32))],
        "droite": "mirror_gauche",
    },

    # --- Rocket (homme) ---
    "pnj_rocket": {
        "bas":    [lambda: create_npc_face((80,136,72), (56,104,48), (40,40,48), (24,24,32), (248,248,255), (216,216,224), (40,40,48))],
        "haut":   [lambda: create_npc_back((80,136,72), (56,104,48), (40,40,48), (24,24,32), (248,248,255), (216,216,224), (40,40,48))],
        "gauche": [lambda: create_npc_left((80,136,72), (56,104,48), (40,40,48), (24,24,32), (248,248,255), (216,216,224), (40,40,48))],
        "droite": "mirror_gauche",
    },
    "pnj_rocket_homme": "alias:pnj_rocket",
    "rocket_m": "alias:pnj_rocket",

    # --- Rocket (femme) ---
    "pnj_rocket_femme": {
        "bas":    [lambda: create_npc_female_face((200,48,96), (168,32,72), (248,248,255), (216,216,224), (40,40,48))],
        "haut":   [lambda: create_npc_female_back((200,48,96), (168,32,72), (248,248,255), (216,216,224), (40,40,48))],
        "gauche": [lambda: create_npc_female_left((200,48,96), (168,32,72), (248,248,255), (216,216,224), (40,40,48))],
        "droite": "mirror_gauche",
    },

    # --- Giovanni --- costume gris foncé, cheveux lisses
    "pnj_giovanni": {
        "bas":    [lambda: create_npc_face((56,48,40), (40,32,24), (80,80,88), (56,56,64), (72,72,80), (48,48,56), (40,40,48))],
        "haut":   [lambda: create_npc_back((56,48,40), (40,32,24), (80,80,88), (56,56,64), (72,72,80), (48,48,56), (40,40,48))],
        "gauche": [lambda: create_npc_left((56,48,40), (40,32,24), (80,80,88), (56,56,64), (72,72,80), (48,48,56), (40,40,48))],
        "droite": "mirror_gauche",
    },

    # --- Scientifique (blouse blanche, lunettes) ---
    "pnj_scientifique": {
        "bas":    [lambda: create_npc_face((136,120,96), (104,88,64), (248,248,255), (216,216,224), (120,120,128), (88,88,96), (80,64,48))],
        "haut":   [lambda: create_npc_back((136,120,96), (104,88,64), (248,248,255), (216,216,224), (120,120,128), (88,88,96), (80,64,48))],
        "gauche": [lambda: create_npc_left((136,120,96), (104,88,64), (248,248,255), (216,216,224), (120,120,128), (88,88,96), (80,64,48))],
        "droite": "mirror_gauche",
    },

    # --- Garde (uniforme bleu foncé) ---
    "pnj_garde": {
        "bas":    [lambda: create_npc_face((48,48,56), (32,32,40), (48,64,128), (32,48,96), (48,64,128), (32,48,96), (40,40,48))],
        "haut":   [lambda: create_npc_back((48,48,56), (32,32,40), (48,64,128), (32,48,96), (48,64,128), (32,48,96), (40,40,48))],
        "gauche": [lambda: create_npc_left((48,48,56), (32,32,40), (48,64,128), (32,48,96), (48,64,128), (32,48,96), (40,40,48))],
        "droite": "mirror_gauche",
    },

    # --- Canon (homme musclé ?) ---
    "pnj_canon": {
        "bas":    [lambda: create_npc_face((56,40,32), (40,28,20), (176,56,56), (144,40,40), (88,88,96), (64,64,72), (80,56,40))],
        "haut":   [lambda: create_npc_back((56,40,32), (40,28,20), (176,56,56), (144,40,40), (88,88,96), (64,64,72), (80,56,40))],
        "gauche": [lambda: create_npc_left((56,40,32), (40,28,20), (176,56,56), (144,40,40), (88,88,96), (64,64,72), (80,56,40))],
        "droite": "mirror_gauche",
    },

    # --- Champions d'arène ---
    "pnj_champion": {
        "bas":    [lambda: create_npc_face((80,56,32), (56,40,24), (200,160,48), (168,128,32), (104,88,72), (80,64,48), (80,56,40))],
        "haut":   [lambda: create_npc_back((80,56,32), (56,40,24), (200,160,48), (168,128,32), (104,88,72), (80,64,48), (80,56,40))],
        "gauche": [lambda: create_npc_left((80,56,32), (56,40,24), (200,160,48), (168,128,32), (104,88,72), (80,64,48), (80,56,40))],
        "droite": "mirror_gauche",
    },
    "champion": "alias:pnj_champion",

    # --- Ondine (Misty) — cheveux roux, maillot bleu ---
    "pnj_champion_ondine": {
        "bas":    [lambda: create_npc_female_face((232,120,48), (200,88,32), (64,160,232), (40,128,200), (200,72,56))],
        "haut":   [lambda: create_npc_female_back((232,120,48), (200,88,32), (64,160,232), (40,128,200), (200,72,56))],
        "gauche": [lambda: create_npc_female_left((232,120,48), (200,88,32), (64,160,232), (40,128,200), (200,72,56))],
        "droite": "mirror_gauche",
    },

    # --- Bob (Lt. Surge) — blond, t-shirt vert militaire ---
    "pnj_champion_bob": {
        "bas":    [lambda: create_npc_face((232,200,104), (200,168,72), (80,112,64), (56,88,40), (104,88,72), (80,64,48), (80,56,40))],
        "haut":   [lambda: create_npc_back((232,200,104), (200,168,72), (80,112,64), (56,88,40), (104,88,72), (80,64,48), (80,56,40))],
        "gauche": [lambda: create_npc_left((232,200,104), (200,168,72), (80,112,64), (56,88,40), (104,88,72), (80,64,48), (80,56,40))],
        "droite": "mirror_gauche",
    },

    # --- Érika — cheveux noirs, kimono vert ---
    "champion_erika": {
        "bas":    [lambda: create_npc_female_face((40,40,48), (24,24,32), (120,192,104), (88,160,72), (200,72,56))],
        "haut":   [lambda: create_npc_female_back((40,40,48), (24,24,32), (120,192,104), (88,160,72), (200,72,56))],
        "gauche": [lambda: create_npc_female_left((40,40,48), (24,24,32), (120,192,104), (88,160,72), (200,72,56))],
        "droite": "mirror_gauche",
    },

    # =================================================================
    # OBJETS SPÉCIAUX
    # =================================================================

    # --- Panneau ---
    "panneau": {
        "bas":    [create_sign],
        "haut":   [create_sign],
        "gauche": [create_sign],
        "droite": "mirror_gauche",
    },
    "pnj_panneau": "alias:panneau",

    # --- PC ---
    "pc": {
        "bas":    [create_pc],
        "haut":   [create_pc],
        "gauche": [create_pc],
        "droite": "mirror_gauche",
    },
    "pnj_pc": "alias:pc",

    # --- Objet au sol ---
    "item_sol": {
        "bas":    [create_item_sol],
        "haut":   [create_item_sol],
        "gauche": [create_item_sol],
        "droite": "mirror_gauche",
    },
    "pnj_objet": "alias:item_sol",

    # --- Ronflex ---
    "pnj_ronflex": {
        "bas":    [create_ronflex],
        "haut":   [create_ronflex],
        "gauche": [create_ronflex],
        "droite": "mirror_gauche",
    },

    # --- Pokémon légendaire ---
    "pnj_legendaire": {
        "bas":    [create_legendary],
        "haut":   [create_legendary],
        "gauche": [create_legendary],
        "droite": "mirror_gauche",
    },
    "pokemon_legendaire": "alias:pnj_legendaire",
}


def generate_character(name, spec, out_dir):
    """Génère tous les sprites d'un personnage."""
    # Résoudre les alias
    if isinstance(spec, str) and spec.startswith("alias:"):
        target = spec[6:]
        spec = CHARACTERS[target]
    
    if isinstance(spec, str):
        return  # Skip aliases non résolus

    # Générer les sprites gauche d'abord (nécessaire pour mirror)
    gauche_images = []
    gauche_grids = []
    
    if "gauche" in spec and spec["gauche"] != "mirror_gauche":
        for frame_func in spec["gauche"]:
            grid = frame_func()
            gauche_grids.append(grid)
            gauche_images.append(grid_to_image(grid))
    
    dirs_to_process = ["bas", "haut", "gauche", "droite"]
    
    for direction in dirs_to_process:
        if direction not in spec:
            continue
            
        dir_spec = spec[direction]
        
        if dir_spec == "mirror_gauche":
            # Miroir horizontal des sprites gauche
            for i, grid in enumerate(gauche_grids):
                mirrored = hmirror(grid)
                img = grid_to_image(mirrored)
                fname = f"{name}_{direction}_{i}.png"
                fpath = os.path.join(out_dir, fname)
                img.save(fpath)
            # Si seulement 1 frame, dupliquer pour walk
            if len(gauche_grids) == 1:
                for i in [1, 2]:
                    fname = f"{name}_{direction}_{i}.png"
                    fpath = os.path.join(out_dir, fname)
                    grid_to_image(hmirror(gauche_grids[0])).save(fpath)
        else:
            for i, frame_func in enumerate(dir_spec):
                grid = frame_func()
                img = grid_to_image(grid)
                fname = f"{name}_{direction}_{i}.png"
                fpath = os.path.join(out_dir, fname)
                img.save(fpath)
            # Dupliquer idle pour walk si manquant
            if len(dir_spec) == 1:
                for i in [1, 2]:
                    fname = f"{name}_{direction}_{i}.png"
                    fpath = os.path.join(out_dir, fname)
                    grid_to_image(dir_spec[0]()).save(fpath)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    print("=" * 60)
    print("  Générateur sprites v8 — Haute qualité FRLG")
    print("=" * 60)
    
    count = 0
    for name, spec in CHARACTERS.items():
        if isinstance(spec, str) and spec.startswith("alias:"):
            target_name = spec[6:]
            target_spec = CHARACTERS.get(target_name)
            if target_spec is None or isinstance(target_spec, str):
                continue
            print(f"  {name} (alias → {target_name})")
            generate_character(name, target_spec, OUT_DIR)
        elif isinstance(spec, dict):
            print(f"  {name}")
            generate_character(name, spec, OUT_DIR)
        count += 1
    
    print(f"\n✓ {count} personnages générés dans {OUT_DIR}")
    print("  → Chaque personnage : 4 directions × 3 frames = 12 sprites")


if __name__ == "__main__":
    main()
