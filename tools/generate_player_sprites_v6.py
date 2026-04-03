#!/usr/bin/env python3
"""
Générateur sprites joueur v6 — Style FRLG amélioré
32×48 px par frame, pixel-par-pixel
Améliorations : contours nets, ombrage 3 tons, détails vêtements, meilleure animation
"""

from PIL import Image
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "characters")

# ─── Palette FRLG fidèle ─────────────────────────────────
T  = (0, 0, 0, 0)        # transparent
K  = (16, 16, 24, 255)    # noir outline
R1 = (224, 48, 40, 255)   # casquette rouge vif
R2 = (176, 32, 24, 255)   # casquette rouge ombre
RW = (248, 248, 248, 255) # logo casquette blanc
S1 = (248, 208, 168, 255) # peau claire
S2 = (224, 176, 136, 255) # peau ombre
S3 = (200, 152, 112, 255) # peau ombre profonde
H1 = (96, 64, 32, 255)    # cheveux bruns
H2 = (72, 48, 24, 255)    # cheveux ombre
EY = (16, 16, 16, 255)    # yeux noir
EW = (248, 248, 248, 255) # blanc des yeux
V1 = (48, 48, 56, 255)    # T-shirt foncé
V2 = (32, 32, 40, 255)    # T-shirt ombre
V3 = (72, 72, 80, 255)    # T-shirt highlight
J1 = (72, 104, 176, 255)  # jean bleu
J2 = (56, 80, 144, 255)   # jean ombre
J3 = (96, 128, 200, 255)  # jean highlight
SN = (208, 48, 40, 255)   # sneakers rouge
SS = (240, 240, 240, 255) # semelle blanche
B1 = (232, 192, 56, 255)  # sac jaune
B2 = (200, 160, 40, 255)  # sac jaune ombre

W, H = 32, 48

def new_frame():
    return Image.new("RGBA", (W, H), T)

def draw_pixels(img, y_start, rows):
    """Dessine des lignes de pixels depuis y_start, chaque ligne = liste de (x, couleur)"""
    for dy, line in enumerate(rows):
        y = y_start + dy
        if y >= H:
            break
        for x, col in line:
            if 0 <= x < W:
                img.putpixel((x, y), col)

def row(y, x_start, colors):
    """Retourne une liste de (x, color) pour une ligne"""
    return [(x_start + i, c) for i, c in enumerate(colors) if c != T]

# ═══════════════════════════════════════════════════════════════
# FACE (bas) — idle
# ═══════════════════════════════════════════════════════════════
def draw_face_idle():
    img = new_frame()
    lines = [
        # y=10: sommet casquette
        (10, row(10, 12, [K, K, K, K, K, K, K, K])),
        # y=11: casquette bord haut
        (11, row(11, 11, [K, R1, R1, R1, R1, R1, R1, R1, R1, K])),
        # y=12: casquette avec logo
        (12, row(12, 10, [K, R1, R1, R1, RW, RW, R1, R1, R1, R1, R1, K])),
        # y=13: casquette bord bas (visière)
        (13, row(13, 9, [K, R2, R2, R2, R2, R2, R2, R2, R2, R2, R2, R2, R2, K])),
        # y=14: visière + front cheveux
        (14, row(14, 9, [K, K, K, K, K, K, K, K, K, K, K, K, K, K])),
        # y=15: cheveux + front
        (15, row(15, 10, [K, H1, H1, S1, S1, S1, S1, S1, S1, H1, H1, K])),
        # y=16: visage — yeux
        (16, row(16, 10, [K, S1, S1, EY, EW, S1, S1, EW, EY, S1, S1, K])),
        # y=17: visage — joues + nez
        (17, row(17, 10, [K, S1, S2, S1, S1, S1, S1, S1, S1, S2, S1, K])),
        # y=18: visage — bouche
        (18, row(18, 11, [K, S1, S1, S1, S2, S2, S1, S1, S1, K])),
        # y=19: menton
        (19, row(19, 11, [K, S2, S1, S1, S1, S1, S1, S1, S2, K])),
        # y=20: cou
        (20, row(20, 13, [K, S1, S1, S1, S1, K])),
        # y=21: épaules T-shirt
        (21, row(21, 10, [K, V1, V1, V1, V1, V1, V1, V1, V1, V1, V1, K])),
        # y=22: T-shirt + bras
        (22, row(22, 9, [K, S1, K, V1, V3, V1, V1, V1, V3, V1, K, S1, K])),
        # y=23: T-shirt + bras
        (23, row(23, 9, [K, S1, K, V1, V1, V1, V1, V1, V1, V1, K, S1, K])),
        # y=24: T-shirt + mains
        (24, row(24, 10, [K, S2, K, V1, V1, V1, V1, V1, V1, K, S2, K])),
        # y=25: bas T-shirt
        (25, row(25, 11, [K, V2, V1, V1, V1, V1, V1, V1, V2, K])),
        # y=26: ceinture
        (26, row(26, 11, [K, V2, V2, V2, V2, V2, V2, V2, V2, K])),
        # y=27: jean haut
        (27, row(27, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K])),
        # y=28: jean
        (28, row(28, 11, [K, J1, J3, J1, J1, J1, J1, J3, J1, K])),
        # y=29: jean
        (29, row(29, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K])),
        # y=30: jean — séparation jambes
        (30, row(30, 11, [K, J1, J1, J2, K, K, J2, J1, J1, K])),
        # y=31: jean bas
        (31, row(31, 11, [K, J1, J1, K, T, T, K, J1, J1, K])),
        # y=32: jean bas
        (32, row(32, 11, [K, J2, J1, K, T, T, K, J1, J2, K])),
        # y=33: cheville
        (33, row(33, 11, [K, J2, K, T, T, T, T, K, J2, K])),
        # y=34: sneakers
        (34, row(34, 10, [K, SN, SN, K, T, T, K, SN, SN, K])),
        # y=35: semelle
        (35, row(35, 10, [K, SS, SS, K, T, T, K, SS, SS, K])),
    ]
    for y, line in lines:
        for x, col in line:
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), col)
    return img

# ═══════════════════════════════════════════════════════════════
# FACE (bas) — walk frame 1 (pied droit avancé)
# ═══════════════════════════════════════════════════════════════
def draw_face_walk1():
    img = draw_face_idle()
    # Modifier les jambes pour la marche (pied droit avancé, gauche reculé)
    # Effacer les jambes existantes (y=30-35)
    for y in range(30, 36):
        for x in range(9, 23):
            img.putpixel((x, y), T)
    # Redessiner les jambes en marche
    walk_legs = [
        (30, row(30, 10, [K, J1, J1, J2, T, T, T, J2, J1, K])),
        (31, row(31, 9, [K, J1, J1, K, T, T, T, T, K, J1, K])),
        (32, row(32, 9, [K, J2, J1, K, T, T, T, T, K, J1, J2, K])),
        (33, row(33, 9, [K, SN, K, T, T, T, T, T, T, K, J2, K])),
        (34, row(34, 9, [K, SS, K, T, T, T, T, T, K, SN, SN, K])),
        (35, row(35, 9, [T, T, T, T, T, T, T, T, K, SS, SS, K])),
    ]
    for y, line in walk_legs:
        for x, col in line:
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), col)
    return img

# ═══════════════════════════════════════════════════════════════
# FACE (bas) — walk frame 2 (pied gauche avancé)
# ═══════════════════════════════════════════════════════════════
def draw_face_walk2():
    img = draw_face_idle()
    for y in range(30, 36):
        for x in range(9, 23):
            img.putpixel((x, y), T)
    walk_legs = [
        (30, row(30, 11, [T, J2, J1, T, T, T, J2, J1, J1, K])),
        (31, row(31, 11, [K, J1, K, T, T, T, T, K, J1, J1, K])),
        (32, row(32, 10, [K, J2, J1, K, T, T, T, T, K, J1, J2, K])),
        (33, row(33, 10, [K, J2, K, T, T, T, T, T, T, K, SN, K])),
        (34, row(34, 10, [K, SN, SN, K, T, T, T, T, T, K, SS, K])),
        (35, row(35, 10, [K, SS, SS, K, T, T, T, T, T, T, T, T])),
    ]
    for y, line in walk_legs:
        for x, col in line:
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), col)
    return img

# ═══════════════════════════════════════════════════════════════
# DOS (haut) — idle
# ═══════════════════════════════════════════════════════════════
def draw_back_idle():
    img = new_frame()
    lines = [
        (10, row(10, 12, [K, K, K, K, K, K, K, K])),
        (11, row(11, 11, [K, R1, R1, R1, R1, R1, R1, R1, R1, K])),
        (12, row(12, 10, [K, R1, R1, R1, R1, R2, R1, R1, R1, R1, R1, K])),
        (13, row(13, 10, [K, R2, R2, R2, R2, R2, R2, R2, R2, R2, R2, K])),
        # y=14: cheveux arrière
        (14, row(14, 10, [K, H1, H1, H1, H1, H1, H1, H1, H1, H1, H1, K])),
        (15, row(15, 10, [K, H1, H2, H1, H2, H1, H2, H1, H2, H1, H2, K])),
        (16, row(16, 10, [K, H2, H1, H2, H1, H2, H1, H2, H1, H2, H1, K])),
        (17, row(17, 11, [K, H1, H2, H1, H2, H1, H2, H1, H2, K])),
        (18, row(18, 12, [K, H2, H1, H1, H1, H1, H2, K])),
        # y=19: cou
        (19, row(19, 13, [K, S2, S1, S1, S2, K])),
        # y=20: sac à dos + épaules
        (20, row(20, 9, [K, B1, B1, K, V1, V1, V1, V1, V1, V1, K, B1, B1, K])),
        # y=21: sac + T-shirt dos
        (21, row(21, 9, [K, B1, B2, K, V1, V1, V1, V1, V1, V1, K, B2, B1, K])),
        # y=22: sac + bras
        (22, row(22, 9, [K, S1, K, K, V1, V2, V1, V1, V2, V1, K, K, S1, K])),
        (23, row(23, 9, [K, S1, K, B1, V1, V1, V1, V1, V1, V1, B1, K, S1, K])),
        (24, row(24, 10, [K, S2, K, B2, V1, V1, V1, V1, V1, V1, B2, K, S2, K])),
        # y=25: bas T-shirt
        (25, row(25, 11, [K, B2, K, V2, V1, V1, V1, V1, V2, K, B2, K])),
        # y=26: ceinture
        (26, row(26, 11, [K, K, V2, V2, V2, V2, V2, V2, V2, K, K, T])),
        # y=27-33: jean (identique face)
        (27, row(27, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K])),
        (28, row(28, 11, [K, J1, J1, J2, J1, J1, J2, J1, J1, K])),
        (29, row(29, 11, [K, J1, J1, J1, J1, J1, J1, J1, J1, K])),
        (30, row(30, 11, [K, J1, J1, J2, K, K, J2, J1, J1, K])),
        (31, row(31, 11, [K, J1, J1, K, T, T, K, J1, J1, K])),
        (32, row(32, 11, [K, J2, J1, K, T, T, K, J1, J2, K])),
        (33, row(33, 11, [K, J2, K, T, T, T, T, K, J2, K])),
        (34, row(34, 10, [K, SN, SN, K, T, T, K, SN, SN, K])),
        (35, row(35, 10, [K, SS, SS, K, T, T, K, SS, SS, K])),
    ]
    for y, line in lines:
        for x, col in line:
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), col)
    return img

def draw_back_walk1():
    img = draw_back_idle()
    for y in range(30, 36):
        for x in range(9, 23):
            img.putpixel((x, y), T)
    walk_legs = [
        (30, row(30, 10, [K, J1, J1, J2, T, T, T, J2, J1, K])),
        (31, row(31, 9, [K, J1, J1, K, T, T, T, T, K, J1, K])),
        (32, row(32, 9, [K, J2, J1, K, T, T, T, T, K, J1, J2, K])),
        (33, row(33, 9, [K, SN, K, T, T, T, T, T, T, K, J2, K])),
        (34, row(34, 9, [K, SS, K, T, T, T, T, T, K, SN, SN, K])),
        (35, row(35, 9, [T, T, T, T, T, T, T, T, K, SS, SS, K])),
    ]
    for y, line in walk_legs:
        for x, col in line:
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), col)
    return img

def draw_back_walk2():
    img = draw_back_idle()
    for y in range(30, 36):
        for x in range(9, 23):
            img.putpixel((x, y), T)
    walk_legs = [
        (30, row(30, 11, [T, J2, J1, T, T, T, J2, J1, J1, K])),
        (31, row(31, 11, [K, J1, K, T, T, T, T, K, J1, J1, K])),
        (32, row(32, 10, [K, J2, J1, K, T, T, T, T, K, J1, J2, K])),
        (33, row(33, 10, [K, J2, K, T, T, T, T, T, T, K, SN, K])),
        (34, row(34, 10, [K, SN, SN, K, T, T, T, T, T, K, SS, K])),
        (35, row(35, 10, [K, SS, SS, K, T, T, T, T, T, T, T, T])),
    ]
    for y, line in walk_legs:
        for x, col in line:
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), col)
    return img

# ═══════════════════════════════════════════════════════════════
# PROFIL GAUCHE — idle
# ═══════════════════════════════════════════════════════════════
def draw_left_idle():
    img = new_frame()
    lines = [
        (10, row(10, 12, [K, K, K, K, K, K])),
        (11, row(11, 11, [K, R1, R1, R1, R1, R1, R1, K])),
        (12, row(12, 10, [K, R1, R1, R1, R1, R1, R1, R1, K])),
        # y=13: visière étendue à gauche
        (13, row(13, 7, [K, R2, R2, R2, K, R2, R2, R2, R2, R2, R2, K])),
        (14, row(14, 7, [K, K, K, K, K, H1, H1, H1, H1, H1, K, T])),
        # y=15: visage profil
        (15, row(15, 10, [K, H1, S1, S1, S1, S1, H1, K])),
        (16, row(16, 10, [K, S1, S1, EY, S1, S1, S1, K])),
        (17, row(17, 10, [K, S1, S1, S1, S1, S2, K, T])),
        (18, row(18, 11, [K, S1, S1, S2, S1, K, T])),
        (19, row(19, 11, [K, S2, S1, S1, K, T, T])),
        # y=20: cou + épaule
        (20, row(20, 12, [K, S1, S1, K, T, T])),
        # y=21: T-shirt profil
        (21, row(21, 11, [K, V1, V1, V1, V1, V1, K])),
        (22, row(22, 11, [K, S1, V1, V1, V3, V1, V1, K])),
        (23, row(23, 11, [K, S1, V1, V1, V1, V1, V1, K])),
        (24, row(24, 11, [K, S2, V2, V1, V1, V1, K, T])),
        (25, row(25, 12, [K, V2, V1, V1, V2, K, T])),
        # y=26: ceinture
        (26, row(26, 12, [K, V2, V2, V2, V2, K])),
        # y=27: jean profil
        (27, row(27, 12, [K, J1, J1, J1, J1, K])),
        (28, row(28, 12, [K, J1, J3, J1, J1, K])),
        (29, row(29, 12, [K, J1, J1, J1, J1, K])),
        (30, row(30, 12, [K, J1, J2, J1, J1, K])),
        (31, row(31, 12, [K, J1, K, K, J1, K])),
        (32, row(32, 12, [K, J2, K, K, J2, K])),
        (33, row(33, 12, [K, J2, K, K, J2, K])),
        (34, row(34, 11, [K, SN, SN, K, SN, SN, K])),
        (35, row(35, 11, [K, SS, SS, K, SS, SS, K])),
    ]
    for y, line in lines:
        for x, col in line:
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), col)
    return img

def draw_left_walk1():
    img = draw_left_idle()
    for y in range(31, 36):
        for x in range(9, 22):
            img.putpixel((x, y), T)
    walk_legs = [
        (31, row(31, 11, [K, J1, K, T, K, J1, K])),
        (32, row(32, 10, [K, J2, K, T, T, K, J2, K])),
        (33, row(33, 10, [K, SN, K, T, T, T, K, J2, K])),
        (34, row(34, 10, [K, SS, K, T, T, K, SN, SN, K])),
        (35, row(35, 10, [T, T, T, T, T, K, SS, SS, K])),
    ]
    for y, line in walk_legs:
        for x, col in line:
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), col)
    return img

def draw_left_walk2():
    img = draw_left_idle()
    for y in range(31, 36):
        for x in range(9, 22):
            img.putpixel((x, y), T)
    walk_legs = [
        (31, row(31, 12, [K, J1, K, T, K, J1, K])),
        (32, row(32, 12, [K, J2, K, T, K, J2, K])),
        (33, row(33, 11, [K, J2, K, T, T, T, K, SN, K])),
        (34, row(34, 11, [K, SN, SN, K, T, T, K, SS, K])),
        (35, row(35, 11, [K, SS, SS, K, T, T, T, T, T])),
    ]
    for y, line in walk_legs:
        for x, col in line:
            if 0 <= x < W and 0 <= y < H:
                img.putpixel((x, y), col)
    return img

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
    "red_normal_bas_0": draw_face_idle(),
    "red_normal_bas_1": draw_face_walk1(),
    "red_normal_bas_2": draw_face_walk2(),
    "red_normal_haut_0": draw_back_idle(),
    "red_normal_haut_1": draw_back_walk1(),
    "red_normal_haut_2": draw_back_walk2(),
    "red_normal_gauche_0": draw_left_idle(),
    "red_normal_gauche_1": draw_left_walk1(),
    "red_normal_gauche_2": draw_left_walk2(),
}

# Droite = miroir du gauche
sprites["red_normal_droite_0"] = mirror_h(sprites["red_normal_gauche_0"])
sprites["red_normal_droite_1"] = mirror_h(sprites["red_normal_gauche_1"])
sprites["red_normal_droite_2"] = mirror_h(sprites["red_normal_gauche_2"])

for name, frame in sprites.items():
    path = os.path.join(OUT_DIR, f"{name}.png")
    frame.save(path, "PNG")
    # Stats
    import numpy as np
    arr = np.array(frame)
    opaque = int(np.sum(arr[:, :, 3] > 0))
    unique_colors = len(set(tuple(p) for row in arr for p in row if p[3] > 0))
    print(f"  ✓ {name}.png: {W}×{H}, {opaque} px opaques, {unique_colors} couleurs")

print(f"\n✓ 12 sprites joueur v6 générés dans {OUT_DIR}")
print(f"  Style FRLG : casquette rouge+logo, T-shirt foncé, jean bleu, sac jaune, sneakers rouges")
print(f"  Améliorations v6 : contours K nets, ombrage 3 tons, yeux détaillés, sac à dos profil arrière")
