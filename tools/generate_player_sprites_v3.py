#!/usr/bin/env python3
"""
Générateur de sprites joueur — Style Pokémon FRLG HD (v3)
Red/Rouge, 4 directions × 3 frames = 12 sprites
Canvas : 32×64 pixels
Personnage proportions chibi FRLG : grosse tête, petit corps
"""

from PIL import Image
import os, sys

# ══════════════════════════════════════════════════════════════
# PALETTE  (31 couleurs uniques + transparent)
# ══════════════════════════════════════════════════════════════
T = (0, 0, 0, 0)

PALETTE = {
    '.': T,
    # Outline
    'K': (16, 16, 24, 255),
    # Casquette rouge
    '1': (240, 64, 56, 255),   # rouge vif
    '2': (208, 48, 40, 255),   # rouge moyen
    '3': (168, 32, 24, 255),   # rouge foncé
    '4': (128, 20, 12, 255),   # rouge ombre
    # Blanc casquette (logo pokeball)
    'W': (255, 255, 255, 255),
    'w': (224, 224, 232, 255),
    # Cheveux bruns
    'H': (104, 72, 48, 255),   # brun clair
    'h': (80, 56, 36, 255),    # brun moyen
    'd': (56, 40, 24, 255),    # brun foncé
    # Peau
    'S': (255, 216, 168, 255), # clair
    's': (240, 192, 144, 255), # moyen
    'x': (208, 160, 112, 255), # foncé
    # Yeux
    'E': (32, 32, 48, 255),    # iris
    'e': (248, 248, 255, 255), # reflet
    # Veste bleue
    'J': (96, 144, 232, 255),  # bleu clair
    'j': (72, 112, 200, 255),  # bleu moyen
    'k': (48, 80, 168, 255),   # bleu foncé
    'z': (32, 56, 128, 255),   # bleu ombre
    # T-shirt noir
    'N': (48, 48, 56, 255),
    'n': (32, 32, 40, 255),
    # Pantalon blue jean
    'P': (88, 128, 192, 255),  # jean clair
    'p': (64, 100, 168, 255),  # jean moyen
    'o': (44, 72, 136, 255),   # jean foncé
    # Chaussures
    'A': (240, 80, 64, 255),   # sneaker rouge
    'a': (200, 56, 48, 255),   # sneaker moyen
    'b': (152, 40, 32, 255),   # sneaker foncé
    'G': (248, 248, 252, 255), # blanc sneaker
    'g': (216, 216, 224, 255), # gris sneaker
    # Sac
    'L': (248, 192, 64, 255),  # jaune
    'l': (216, 152, 40, 255),  # orange
    'm': (184, 120, 32, 255),  # foncé
}

W = 32
H = 64
PAD = '.' * W  # ligne vide


def row(s):
    """Construit une ligne de 32 chars exactement. Padding à droite si trop court."""
    if len(s) > W:
        print(f"ERREUR: ligne trop longue ({len(s)}): {s}", file=sys.stderr)
        return s[:W]
    return s.ljust(W, '.')


def make_grid(lines_fn):
    """Construit une grille de 64 lignes à partir d'une fonction qui retourne les lignes non-vides."""
    rows = lines_fn()
    # Valider
    for i, r in enumerate(rows):
        if len(r) != W:
            print(f"WARN: line {i} len={len(r)} != {W}", file=sys.stderr)
    # Pad to 64 rows (top-aligned: content starts where defined)
    while len(rows) < H:
        rows.append(PAD)
    return rows[:H]


# ════════════════════════════════════════════════════════════════
# SPRITE DEFINITIONS
# Le personnage est centré horizontalement et positionné pour que
# les pieds soient vers row 44-46 (aligne avec collision à y=24)
# ════════════════════════════════════════════════════════════════

def bas_idle():
    """Face (vers le bas) — position repos."""
    return [
        PAD,                                          # 0
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,  # 1-9
        PAD, PAD,                                     # 10-11
        row('..........KK3333KK..............'),       # 12  casquette dessus
        row('.........K32111123K.............'),       # 13
        row('........K2111WW1112K............'),       # 14  logo pokeball
        row('........K1111WW1113K............'),       # 15
        row('........K3222222234K............'),       # 16  bord casquette
        row('.......KK4333333343KK...........'),       # 17  visière
        row('.......KdhHSSSSSSHhdK...........'),       # 18  cheveux+front
        row('.......KhSSSSSSSSSShK...........'),       # 19  front
        row('.......KHSEeSSSSEeSHK...........'),       # 20  yeux
        row('.......KhSEESSSSEEShK...........'),       # 21  yeux bas
        row('.......KdsSSSssSSSsdK...........'),       # 22  nez
        row('........KxSSSSSSSSxK............'),       # 23  bouche
        row('.........KsSSSSSssK.............'),       # 24  mâchoire
        row('..........KxsssxK...............'),       # 25  cou
        row('.......KKzkjNNNjkzKK............'),       # 26  col
        row('......KzjJJJNNJJJjzK............'),       # 27  torse haut
        row('......KzjJJJNNJJJjzK............'),       # 28
        row('.....KxkjJJJJJJJJkxK............'),       # 29  manche+bras
        row('.....KSzjJJJJJJJjzSK............'),       # 30
        row('.....KSzkjjjjjjjkzSK............'),       # 31  bas veste
        row('......KSKzkkkkkkKSK.............'),       # 32  ceinture
        row('......KKKopPPPPoKKK.............'),       # 33  pantalon haut
        row('.......KopPPPpPPPoK.............'),       # 34
        row('.......KopPPPpPPPoK.............'),       # 35
        row('.......KopPPo.oPPPoK............'),       # 36
        row('.......KopPo...oPPoK............'),       # 37  entre-jambes
        row('.......Kooo.....oooK............'),       # 38  chevilles
        row('......KKaAG.....GAaKK...........'),       # 39  chaussures haut
        row('......KbaGg.....gGabK...........'),       # 40  chaussures bas
        row('.......KKK.......KKK............'),       # 41  semelle
        PAD, PAD, PAD,                                 # 42-44
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,  # 45-53
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,  # 54-62
        PAD,                                           # 63
    ]

def bas_walk1():
    """Face — jambe gauche avancée (corps remonte 1px = bounce)."""
    return [
        PAD,                                          # 0
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,                                          # 10
        row('..........KK3333KK..............'),       # 11
        row('.........K32111123K.............'),       # 12
        row('........K2111WW1112K............'),       # 13
        row('........K1111WW1113K............'),       # 14
        row('........K3222222234K............'),       # 15
        row('.......KK4333333343KK...........'),       # 16
        row('.......KdhHSSSSSSHhdK...........'),       # 17
        row('.......KhSSSSSSSSSShK...........'),       # 18
        row('.......KHSEeSSSSEeSHK...........'),       # 19
        row('.......KhSEESSSSEEShK...........'),       # 20
        row('.......KdsSSSssSSSsdK...........'),       # 21
        row('........KxSSSSSSSSxK............'),       # 22
        row('.........KsSSSSSssK.............'),       # 23
        row('..........KxsssxK...............'),       # 24
        row('.......KKzkjNNNjkzKK............'),       # 25
        row('......KzjJJJNNJJJjzK............'),       # 26
        row('......KzjJJJNNJJJjzK............'),       # 27
        row('.....KxkjJJJJJJJJkxK............'),       # 28
        row('.....KSzjJJJJJJJjzSK............'),       # 29
        row('.....KSzkjjjjjjjkzSK............'),       # 30
        row('......KSKzkkkkkkKSK.............'),       # 31
        row('......KKKopPPPPoKKK.............'),       # 32
        row('.......KopPPPpPPPoK.............'),       # 33
        row('......KopPPo..pPPPoK............'),       # 34
        row('.....KopPo.....oPPoK............'),       # 35  jambes écartées
        row('.....Kooo.......oooK............'),       # 36
        row('....KKaAG.......GAaKK...........'),       # 37
        row('....KbaGg.......gGabK...........'),       # 38
        row('.....KKK.........KKK............'),       # 39
        PAD, PAD, PAD, PAD, PAD,                       # 40-44
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,  # 45-53
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,  # 54-62
        PAD,                                           # 63
    ]

def bas_walk2():
    """Face — jambe droite avancée (bounce)."""
    return [
        PAD,                                          # 0
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,                                          # 10
        row('..........KK3333KK..............'),       # 11
        row('.........K32111123K.............'),
        row('........K2111WW1112K............'),
        row('........K1111WW1113K............'),
        row('........K3222222234K............'),
        row('.......KK4333333343KK...........'),
        row('.......KdhHSSSSSSHhdK...........'),
        row('.......KhSSSSSSSSSShK...........'),
        row('.......KHSEeSSSSEeSHK...........'),
        row('.......KhSEESSSSEEShK...........'),       # 20
        row('.......KdsSSSssSSSsdK...........'),
        row('........KxSSSSSSSSxK............'),
        row('.........KsSSSSSssK.............'),
        row('..........KxsssxK...............'),
        row('.......KKzkjNNNjkzKK............'),       # 25
        row('......KzjJJJNNJJJjzK............'),
        row('......KzjJJJNNJJJjzK............'),
        row('.....KxkjJJJJJJJJkxK............'),
        row('.....KSzjJJJJJJJjzSK............'),
        row('.....KSzkjjjjjjjkzSK............'),       # 30
        row('......KSKzkkkkkkKSK.............'),
        row('......KKKopPPPPoKKK.............'),
        row('.......KopPPPpPPPoK.............'),
        row('.......KopPPo..oPPPoK...........'),       # 34
        row('........KopPo.....oPPK..........'),       # 35
        row('........Kooo.......oooK.........'),       # 36
        row('.........KaAG.......GAaKK.......'),       # 37
        row('.........KbaGg.....gGabK........'),       # 38
        row('..........KKK.......KKK.........'),       # 39
        PAD, PAD, PAD, PAD, PAD,                       # 40-44
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,
    ]

def haut_idle():
    """Dos (vers le haut) — position repos."""
    return [
        PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD, PAD,                                     # 10-11
        row('..........KK3333KK..............'),       # 12
        row('.........K321111123K............'),       # 13
        row('........K21111111112K...........'),       # 14
        row('........K11111111113K...........'),       # 15
        row('........K3222222234K............'),       # 16
        row('.......KKhHHHHHHHHhKK...........'),       # 17
        row('.......KhHHHHHHHHHHhK...........'),       # 18
        row('.......KhHHHHHHHHHHhK...........'),       # 19
        row('.......KdhhHHHHHHhhdK...........'),       # 20
        row('.......KdhhhhhhhhhhdK...........'),       # 21
        row('........KdhhhhhhhdK.............'),       # 22
        row('.........KddhhhhddK.............'),       # 23
        row('..........KddddddK.............'),       # 24
        row('..........KxssssxK..............'),       # 25  cou
        row('.......KKzkjjjjjkzKK............'),       # 26
        row('......KzjJJJJJJJJjzK............'),       # 27
        row('......KzjJJJJJJJJjzK............'),       # 28
        row('.....KxkjJJJJJJJJkxK............'),       # 29
        row('.....KSzjJJJJJJJjzSK............'),       # 30
        row('.....KSzkjjjjjjjkzSK............'),       # 31
        row('......KSKzkkkkkkKSK.............'),       # 32
        row('......KKKopPPPPoKKK.............'),       # 33
        row('.......KopPPPPPPPoK.............'),       # 34
        row('.......KopPPPPPPPoK.............'),       # 35
        row('.......KopPPo.oPPPoK............'),       # 36
        row('.......KopPo...oPPoK............'),       # 37
        row('.......Kooo.....oooK............'),       # 38
        row('......KKaAG.....GAaKK...........'),       # 39
        row('......KbaGg.....gGabK...........'),       # 40
        row('.......KKK.......KKK............'),       # 41
        PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,
    ]

def haut_walk1():
    """Dos — jambe gauche avancée."""
    return [
        PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,                                          # 10
        row('..........KK3333KK..............'),       # 11
        row('.........K321111123K............'),
        row('........K21111111112K...........'),
        row('........K11111111113K...........'),
        row('........K3222222234K............'),
        row('.......KKhHHHHHHHHhKK...........'),
        row('.......KhHHHHHHHHHHhK...........'),
        row('.......KhHHHHHHHHHHhK...........'),
        row('.......KdhhHHHHHHhhdK...........'),       # 20
        row('.......KdhhhhhhhhhhdK...........'),
        row('........KdhhhhhhhdK.............'),
        row('.........KddhhhhddK.............'),
        row('..........KddddddK.............'),
        row('..........KxssssxK..............'),       # 25
        row('.......KKzkjjjjjkzKK............'),
        row('......KzjJJJJJJJJjzK............'),
        row('......KzjJJJJJJJJjzK............'),
        row('.....KxkjJJJJJJJJkxK............'),
        row('.....KSzjJJJJJJJjzSK............'),       # 30
        row('.....KSzkjjjjjjjkzSK............'),
        row('......KSKzkkkkkkKSK.............'),
        row('......KKKopPPPPoKKK.............'),
        row('.......KopPPPPPPPoK.............'),
        row('......KopPPo..pPPPoK............'),       # 35
        row('.....KopPo.....oPPoK............'),
        row('.....Kooo.......oooK............'),
        row('....KKaAG.......GAaKK...........'),
        row('....KbaGg.......gGabK...........'),
        row('.....KKK.........KKK............'),       # 40
        PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
    ]

def haut_walk2():
    """Dos — jambe droite avancée."""
    return [
        PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,                                          # 10
        row('..........KK3333KK..............'),
        row('.........K321111123K............'),
        row('........K21111111112K...........'),
        row('........K11111111113K...........'),
        row('........K3222222234K............'),
        row('.......KKhHHHHHHHHhKK...........'),
        row('.......KhHHHHHHHHHHhK...........'),
        row('.......KhHHHHHHHHHHhK...........'),
        row('.......KdhhHHHHHHhhdK...........'),       # 20
        row('.......KdhhhhhhhhhhdK...........'),
        row('........KdhhhhhhhdK.............'),
        row('.........KddhhhhddK.............'),
        row('..........KddddddK.............'),
        row('..........KxssssxK..............'),       # 25
        row('.......KKzkjjjjjkzKK............'),
        row('......KzjJJJJJJJJjzK............'),
        row('......KzjJJJJJJJJjzK............'),
        row('.....KxkjJJJJJJJJkxK............'),
        row('.....KSzjJJJJJJJjzSK............'),       # 30
        row('.....KSzkjjjjjjjkzSK............'),
        row('......KSKzkkkkkkKSK.............'),
        row('......KKKopPPPPoKKK.............'),
        row('.......KopPPPPPPPoK.............'),
        row('.......KopPPP..oPPPoK...........'),       # 35
        row('........KopPo.....oPPK..........'),
        row('........Kooo.......oooK.........'),
        row('.........KaAG.......GAaKK.......'),
        row('.........KbaGg.....gGabK........'),
        row('..........KKK.......KKK.........'),       # 40
        PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
    ]

def gauche_idle():
    """Profil gauche — repos."""
    return [
        PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD, PAD,                                     # 10-11
        row('...........KK333KK..............'),       # 12  casquette
        row('..........K321112K..............'),       # 13
        row('.........K3211113K..............'),       # 14
        row('.........K321111K...............'),       # 15
        row('.........K332223K...............'),       # 16
        row('........KK43334KK...............'),       # 17  visière
        row('........KdhHHHSSK...............'),       # 18  cheveux
        row('........KhHHSSSSKK..............'),       # 19
        row('........KhHSEeSSsK..............'),       # 20  oeil
        row('........KdhSEESSsK..............'),       # 21
        row('........KdhSSSSSsK..............'),       # 22
        row('.........KxSSsSsxK..............'),       # 23
        row('.........KxsSSSsK...............'),       # 24
        row('..........KxssxK................'),       # 25  cou
        row('.........KKkjjkzKK..............'),       # 26
        row('........KzjJJJjkzK..............'),       # 27
        row('........KzjJJJjkzK..............'),       # 28
        row('.......KxkjJJJjkK...............'),       # 29
        row('.......KSzjJJJjzK...............'),       # 30
        row('.......KSkjjjjjkK...............'),       # 31
        row('........KSzkkkkzK...............'),       # 32
        row('........KKopPPoKK...............'),       # 33
        row('.........KopPPPoK...............'),       # 34
        row('.........KopPPPoK...............'),       # 35
        row('.........KopPpPoK...............'),       # 36
        row('.........KopP.PoK...............'),       # 37
        row('.........Koo..ooK...............'),       # 38
        row('........KKaG.GaKK...............'),       # 39
        row('........KbGg.gGbK...............'),       # 40
        row('.........KKK.KKK................'),       # 41
        PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,
    ]

def gauche_walk1():
    """Profil gauche — jambe gauche avancée."""
    return [
        PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,                                          # 10
        row('...........KK333KK..............'),       # 11
        row('..........K321112K..............'),
        row('.........K3211113K..............'),
        row('.........K321111K...............'),
        row('.........K332223K...............'),
        row('........KK43334KK...............'),
        row('........KdhHHHSSK...............'),
        row('........KhHHSSSSKK..............'),
        row('........KhHSEeSSsK..............'),       # 19
        row('........KdhSEESSsK..............'),
        row('........KdhSSSSSsK..............'),
        row('.........KxSSsSsxK..............'),
        row('.........KxsSSSsK...............'),
        row('..........KxssxK................'),       # 24
        row('.........KKkjjkzKK..............'),
        row('........KzjJJJjkzK..............'),
        row('........KzjJJJjkzK..............'),
        row('.......KxkjJJJjkK...............'),
        row('.......KSzjJJJjzK...............'),
        row('.......KSkjjjjjkK...............'),       # 30
        row('........KSzkkkkzK...............'),
        row('........KKopPPoKK...............'),
        row('.........KopPPPoK...............'),
        row('........KopPo.PoK...............'),       # 34
        row('.......KopPo..oK................'),       # 35
        row('.......Kooo..ooK................'),       # 36
        row('......KKaAG.GaKK................'),       # 37
        row('......KbGg..gGbK................'),       # 38
        row('.......KKK...KKK................'),       # 39
        PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,
    ]

def gauche_walk2():
    """Profil gauche — jambe droite avancée."""
    return [
        PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,                                          # 10
        row('...........KK333KK..............'),
        row('..........K321112K..............'),
        row('.........K3211113K..............'),
        row('.........K321111K...............'),
        row('.........K332223K...............'),
        row('........KK43334KK...............'),
        row('........KdhHHHSSK...............'),
        row('........KhHHSSSSKK..............'),
        row('........KhHSEeSSsK..............'),       # 19
        row('........KdhSEESSsK..............'),
        row('........KdhSSSSSsK..............'),
        row('.........KxSSsSsxK..............'),
        row('.........KxsSSSsK...............'),
        row('..........KxssxK................'),       # 24
        row('.........KKkjjkzKK..............'),
        row('........KzjJJJjkzK..............'),
        row('........KzjJJJjkzK..............'),
        row('.......KxkjJJJjkK...............'),
        row('.......KSzjJJJjzK...............'),
        row('.......KSkjjjjjkK...............'),       # 30
        row('........KSzkkkkzK...............'),
        row('........KKopPPoKK...............'),
        row('.........KopPPPoK...............'),
        row('.........KopPP.PoK..............'),       # 34
        row('..........KoPo..oPK.............'),       # 35
        row('..........Koo...ooK.............'),       # 36
        row('.........KKaG..GaKK.............'),       # 37
        row('.........KbGg..gGbK.............'),       # 38
        row('..........KKK..KKK..............'),       # 39
        PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD, PAD,
        PAD,
    ]


# ════════════════════════════════════════════════════════════════
# RENDU
# ════════════════════════════════════════════════════════════════

def grid_to_image(grid, y_offset=7):
    """Grille → Image RGBA 32×64. y_offset décale le contenu vers le bas
    pour aligner les pieds avec la CollisionShape (y=24 local → row ~48)."""
    img = Image.new("RGBA", (W, H), T)
    for y, line in enumerate(grid):
        dy = y + y_offset
        if dy >= H:
            break
        if dy < 0:
            continue
        line = line.ljust(W, '.')
        for x, ch in enumerate(line[:W]):
            c = PALETTE.get(ch, T)
            if c != T:
                img.putpixel((x, dy), c)
    return img


def mirror(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def main():
    out = "assets/sprites/characters"
    os.makedirs(out, exist_ok=True)

    # Construire les grilles
    g_idle = make_grid(gauche_idle)
    g_w1 = make_grid(gauche_walk1)
    g_w2 = make_grid(gauche_walk2)

    gi = grid_to_image(g_idle)
    gw1 = grid_to_image(g_w1)
    gw2 = grid_to_image(g_w2)

    sprites = {
        "red_normal_bas_0":     grid_to_image(make_grid(bas_idle)),
        "red_normal_bas_1":     grid_to_image(make_grid(bas_walk1)),
        "red_normal_bas_2":     grid_to_image(make_grid(bas_walk2)),
        "red_normal_haut_0":    grid_to_image(make_grid(haut_idle)),
        "red_normal_haut_1":    grid_to_image(make_grid(haut_walk1)),
        "red_normal_haut_2":    grid_to_image(make_grid(haut_walk2)),
        "red_normal_gauche_0":  gi,
        "red_normal_gauche_1":  gw1,
        "red_normal_gauche_2":  gw2,
        "red_normal_droite_0":  mirror(gi),
        "red_normal_droite_1":  mirror(gw1),
        "red_normal_droite_2":  mirror(gw2),
    }

    for name, img in sprites.items():
        path = os.path.join(out, f"{name}.png")
        img.save(path)
        px = list(img.getdata())
        opaque = sum(1 for p in px if p[3] > 0)
        colors = len(set(p for p in px if p[3] > 0))
        print(f"  {name}: {img.size}, {opaque}px, {colors} couleurs")

    print(f"\n✓ 12 sprites Red FRLG v3 (32×64) → {out}/")


if __name__ == "__main__":
    main()
