#!/usr/bin/env python3
"""
Générateur de sprites joueur — Style Pokémon FRLG (v4)
Red/Rouge — 4 directions × 3 frames = 12 sprites
Canvas : 32×48 pixels — personnage remplit ~80% du canvas
Style : bold, lisible, immédiatement reconnaissable comme Red de Pokémon
"""

from PIL import Image, ImageDraw
import os

# Dimensions
W, H = 32, 48
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "characters")

# ═══════════════════════════════════════════════════════════
# PALETTE (couleurs saturées, lisibles à petite taille)
# ═══════════════════════════════════════════════════════════
T  = (0, 0, 0, 0)         # transparent

# Outline
OL = (24, 24, 32, 255)

# Casquette rouge
C1 = (232, 56, 48, 255)   # rouge vif principal
C2 = (200, 40, 32, 255)   # rouge moyen/ombre
C3 = (160, 28, 20, 255)   # rouge foncé (visière)
CW = (255, 255, 255, 255) # blanc logo Pokéball
CH = (255, 88, 72, 255)   # highlight casquette

# Cheveux
H1 = (104, 72, 40, 255)   # brun principal
H2 = (80, 52, 28, 255)    # brun foncé

# Peau
S1 = (255, 216, 168, 255) # peau claire
S2 = (240, 192, 144, 255) # peau ombre
S3 = (216, 168, 120, 255) # peau foncée

# Yeux
EB = (24, 24, 48, 255)    # noir iris
EW = (255, 255, 255, 255) # blanc reflet

# Veste bleue
J1 = (88, 152, 240, 255)  # bleu vif principal
J2 = (64, 120, 208, 255)  # bleu ombre
J3 = (112, 176, 255, 255) # bleu highlight

# T-shirt noir
BK = (40, 40, 48, 255)

# Jean bleu
P1 = (96, 136, 208, 255)  # jean principal
P2 = (72, 112, 184, 255)  # jean ombre

# Chaussures
R1 = (232, 72, 56, 255)   # sneaker rouge
R2 = (192, 48, 36, 255)   # sneaker foncé
RW = (248, 248, 252, 255) # blanc sneaker

# Sac à dos (vue latérale/dos)
Y1 = (248, 200, 64, 255)  # jaune vif
Y2 = (224, 168, 40, 255)  # jaune ombre
Y3 = (200, 144, 32, 255)  # jaune foncé


def new_img():
    return Image.new("RGBA", (W, H), T)


def add_outline(img):
    """Ajoute un contour 1px noir autour de tous les pixels opaques."""
    px = img.load()
    out = Image.new("RGBA", (W, H), T)
    opx = out.load()
    for y in range(H):
        for x in range(W):
            if px[x, y][3] > 0:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < W and 0 <= ny < H and px[nx, ny][3] == 0:
                        opx[nx, ny] = OL
    result = Image.new("RGBA", (W, H), T)
    result.paste(out, (0, 0))
    result.paste(img, (0, 0), img)
    return result


def R(d, x1, y1, x2, y2, c):
    """Rectangle shorthand."""
    d.rectangle([x1, y1, x2, y2], fill=c)


def P(d, pts, c):
    """Points shorthand."""
    d.point(pts, fill=c)


# ═══════════════════════════════════════════════════════════
#  FACE (BAS) — vers le joueur
# ═══════════════════════════════════════════════════════════

def front_idle():
    img = new_img()
    d = ImageDraw.Draw(img)
    # Casquette  
    R(d, 12, 2, 19, 2, CH)     # sommet highlight
    R(d, 11, 3, 20, 4, C1)     # dôme
    R(d, 10, 5, 21, 6, C1)     # corps casquette
    R(d, 14, 4, 17, 4, CW)     # logo Pokéball
    R(d, 14, 5, 17, 5, CW)     # logo bas
    R(d, 9, 7, 22, 7, C2)      # bord casquette
    R(d, 8, 8, 23, 8, C3)      # visière ombre
    # Cheveux
    R(d, 10, 9, 11, 15, H1)    # cheveux gauche
    R(d, 20, 9, 21, 15, H1)    # cheveux droit
    R(d, 10, 9, 10, 15, H2)    # ombre gauche
    R(d, 21, 9, 21, 15, H2)    # ombre droit
    # Visage
    R(d, 12, 9, 19, 16, S1)    # peau face
    R(d, 12, 16, 19, 16, S2)   # menton ombre
    # Yeux
    R(d, 13, 11, 14, 12, EB)   # œil gauche
    R(d, 17, 11, 18, 12, EB)   # œil droit
    P(d, [(13, 11)], EW)       # reflet G
    P(d, [(17, 11)], EW)       # reflet D
    # Bouche
    P(d, [(15, 15), (16, 15)], S2)
    # Cou
    R(d, 14, 17, 17, 17, S2)
    # --- Corps ---
    # Col / t-shirt noir visible
    R(d, 13, 18, 18, 19, BK)
    # Veste
    R(d, 10, 18, 21, 26, J1)   # torse
    R(d, 14, 18, 17, 19, BK)   # t-shirt V
    R(d, 10, 18, 10, 26, J2)   # bord gauche ombre
    R(d, 21, 18, 21, 26, J2)   # bord droit ombre
    # Bras
    R(d, 8, 20, 10, 26, J1)    # bras gauche
    R(d, 21, 20, 23, 26, J1)   # bras droit
    R(d, 8, 20, 8, 26, J2)     # ombre bras G
    R(d, 23, 20, 23, 26, J2)   # ombre bras D
    # Mains
    R(d, 8, 27, 9, 27, S1)     # main G
    R(d, 22, 27, 23, 27, S1)   # main D
    # Ceinture
    R(d, 11, 27, 20, 27, J2)
    # Jean
    R(d, 11, 28, 20, 35, P1)
    R(d, 11, 28, 11, 35, P2)   # ombre G
    R(d, 20, 28, 20, 35, P2)   # ombre D
    # Séparation jambes
    R(d, 15, 33, 16, 35, T)
    R(d, 11, 33, 14, 35, P1)   # jambe G
    R(d, 17, 33, 20, 35, P1)   # jambe D
    # Chaussures
    R(d, 10, 36, 14, 38, R1)   # chaussure G
    R(d, 17, 36, 21, 38, R1)   # chaussure D
    R(d, 10, 38, 14, 38, R2)   # semelle G
    R(d, 17, 38, 21, 38, R2)   # semelle D
    P(d, [(10, 37)], RW)       # bande blanche G
    P(d, [(21, 37)], RW)       # bande blanche D
    return add_outline(img)


def front_walk1():
    """Marche face — jambe gauche avancée, corps +1px haut."""
    img = new_img()
    d = ImageDraw.Draw(img)
    yo = -1  # bounce up
    # Casquette
    R(d, 12, 2+yo, 19, 2+yo, CH)
    R(d, 11, 3+yo, 20, 4+yo, C1)
    R(d, 10, 5+yo, 21, 6+yo, C1)
    R(d, 14, 4+yo, 17, 4+yo, CW)
    R(d, 14, 5+yo, 17, 5+yo, CW)
    R(d, 9, 7+yo, 22, 7+yo, C2)
    R(d, 8, 8+yo, 23, 8+yo, C3)
    # Cheveux
    R(d, 10, 9+yo, 11, 15+yo, H1)
    R(d, 20, 9+yo, 21, 15+yo, H1)
    R(d, 10, 9+yo, 10, 15+yo, H2)
    R(d, 21, 9+yo, 21, 15+yo, H2)
    # Visage
    R(d, 12, 9+yo, 19, 16+yo, S1)
    R(d, 12, 16+yo, 19, 16+yo, S2)
    R(d, 13, 11+yo, 14, 12+yo, EB)
    R(d, 17, 11+yo, 18, 12+yo, EB)
    P(d, [(13, 11+yo)], EW)
    P(d, [(17, 11+yo)], EW)
    P(d, [(15, 15+yo), (16, 15+yo)], S2)
    # Cou
    R(d, 14, 17+yo, 17, 17+yo, S2)
    # Corps (identique, décalé)
    R(d, 13, 18+yo, 18, 19+yo, BK)
    R(d, 10, 18+yo, 21, 26+yo, J1)
    R(d, 14, 18+yo, 17, 19+yo, BK)
    R(d, 10, 18+yo, 10, 26+yo, J2)
    R(d, 21, 18+yo, 21, 26+yo, J2)
    R(d, 8, 20+yo, 10, 26+yo, J1)
    R(d, 21, 20+yo, 23, 26+yo, J1)
    R(d, 8, 20+yo, 8, 26+yo, J2)
    R(d, 23, 20+yo, 23, 26+yo, J2)
    R(d, 8, 27+yo, 9, 27+yo, S1)
    R(d, 22, 27+yo, 23, 27+yo, S1)
    R(d, 11, 27+yo, 20, 27+yo, J2)
    # Jean — jambes écartées
    R(d, 11, 28+yo, 20, 31+yo, P1)
    R(d, 11, 28+yo, 11, 31+yo, P2)
    R(d, 20, 28+yo, 20, 31+yo, P2)
    # Jambe gauche avancée (plus bas)
    R(d, 10, 32, 14, 36, P1)
    R(d, 10, 32, 10, 36, P2)
    R(d, 9, 37, 14, 39, R1)
    R(d, 9, 39, 14, 39, R2)
    P(d, [(9, 38)], RW)
    # Jambe droite en arrière (plus haut)
    R(d, 17, 32, 21, 34, P1)
    R(d, 21, 32, 21, 34, P2)
    R(d, 17, 35, 22, 37, R1)
    R(d, 17, 37, 22, 37, R2)
    P(d, [(22, 36)], RW)
    return add_outline(img)


def front_walk2():
    """Marche face — jambe droite avancée, corps +1px haut."""
    img = new_img()
    d = ImageDraw.Draw(img)
    yo = -1
    # Casquette
    R(d, 12, 2+yo, 19, 2+yo, CH)
    R(d, 11, 3+yo, 20, 4+yo, C1)
    R(d, 10, 5+yo, 21, 6+yo, C1)
    R(d, 14, 4+yo, 17, 4+yo, CW)
    R(d, 14, 5+yo, 17, 5+yo, CW)
    R(d, 9, 7+yo, 22, 7+yo, C2)
    R(d, 8, 8+yo, 23, 8+yo, C3)
    R(d, 10, 9+yo, 11, 15+yo, H1)
    R(d, 20, 9+yo, 21, 15+yo, H1)
    R(d, 10, 9+yo, 10, 15+yo, H2)
    R(d, 21, 9+yo, 21, 15+yo, H2)
    R(d, 12, 9+yo, 19, 16+yo, S1)
    R(d, 12, 16+yo, 19, 16+yo, S2)
    R(d, 13, 11+yo, 14, 12+yo, EB)
    R(d, 17, 11+yo, 18, 12+yo, EB)
    P(d, [(13, 11+yo)], EW)
    P(d, [(17, 11+yo)], EW)
    P(d, [(15, 15+yo), (16, 15+yo)], S2)
    R(d, 14, 17+yo, 17, 17+yo, S2)
    R(d, 13, 18+yo, 18, 19+yo, BK)
    R(d, 10, 18+yo, 21, 26+yo, J1)
    R(d, 14, 18+yo, 17, 19+yo, BK)
    R(d, 10, 18+yo, 10, 26+yo, J2)
    R(d, 21, 18+yo, 21, 26+yo, J2)
    R(d, 8, 20+yo, 10, 26+yo, J1)
    R(d, 21, 20+yo, 23, 26+yo, J1)
    R(d, 8, 20+yo, 8, 26+yo, J2)
    R(d, 23, 20+yo, 23, 26+yo, J2)
    R(d, 8, 27+yo, 9, 27+yo, S1)
    R(d, 22, 27+yo, 23, 27+yo, S1)
    R(d, 11, 27+yo, 20, 27+yo, J2)
    R(d, 11, 28+yo, 20, 31+yo, P1)
    R(d, 11, 28+yo, 11, 31+yo, P2)
    R(d, 20, 28+yo, 20, 31+yo, P2)
    # Jambe droite avancée (plus bas)
    R(d, 17, 32, 21, 36, P1)
    R(d, 21, 32, 21, 36, P2)
    R(d, 17, 37, 22, 39, R1)
    R(d, 17, 39, 22, 39, R2)
    P(d, [(22, 38)], RW)
    # Jambe gauche en arrière (plus haut)
    R(d, 10, 32, 14, 34, P1)
    R(d, 10, 32, 10, 34, P2)
    R(d, 9, 35, 14, 37, R1)
    R(d, 9, 37, 14, 37, R2)
    P(d, [(9, 36)], RW)
    return add_outline(img)


# ═══════════════════════════════════════════════════════════
#  DOS (HAUT) — s'éloigne du joueur
# ═══════════════════════════════════════════════════════════

def back_idle():
    img = new_img()
    d = ImageDraw.Draw(img)
    # Casquette (vue arrière — pas de logo visible)
    R(d, 12, 2, 19, 2, C1)
    R(d, 11, 3, 20, 4, C1)
    R(d, 10, 5, 21, 6, C1)
    R(d, 10, 5, 21, 5, CH)     # highlight haut
    R(d, 9, 7, 22, 7, C2)
    R(d, 10, 8, 21, 8, C3)     # ombre bord (plus court vu de dos)
    # Cheveux (plus visibles de dos)
    R(d, 10, 9, 21, 11, H1)
    R(d, 10, 9, 10, 11, H2)
    R(d, 21, 9, 21, 11, H2)
    # Mèches qui dépassent
    P(d, [(9, 10), (22, 10)], H1)
    P(d, [(9, 11), (22, 11)], H1)
    # Nuque
    R(d, 12, 12, 19, 13, S1)
    R(d, 11, 12, 11, 13, H1)
    R(d, 20, 12, 20, 13, H1)
    # Cou
    R(d, 14, 14, 17, 15, S2)
    # Col arrière
    R(d, 12, 16, 19, 16, J2)
    # Sac à dos (centré sur le dos)
    R(d, 12, 17, 19, 26, Y1)   # sac principal
    R(d, 12, 17, 12, 26, Y2)   # ombre G
    R(d, 19, 17, 19, 26, Y2)   # ombre D
    R(d, 13, 17, 18, 17, Y2)   # bord haut
    R(d, 12, 24, 19, 24, Y3)   # poche/bande
    R(d, 12, 26, 19, 26, Y3)   # bord bas
    # Bras (visibles sur les côtés du sac)
    R(d, 9, 18, 11, 26, J1)
    R(d, 20, 18, 22, 26, J1)
    R(d, 9, 18, 9, 26, J2)
    R(d, 22, 18, 22, 26, J2)
    # Mains
    R(d, 9, 27, 10, 27, S1)
    R(d, 21, 27, 22, 27, S1)
    # Ceinture
    R(d, 11, 27, 20, 27, J2)
    # Jean
    R(d, 11, 28, 20, 35, P1)
    R(d, 11, 28, 11, 35, P2)
    R(d, 20, 28, 20, 35, P2)
    R(d, 15, 33, 16, 35, T)
    R(d, 11, 33, 14, 35, P1)
    R(d, 17, 33, 20, 35, P1)
    # Chaussures
    R(d, 10, 36, 14, 38, R1)
    R(d, 17, 36, 21, 38, R1)
    R(d, 10, 38, 14, 38, R2)
    R(d, 17, 38, 21, 38, R2)
    P(d, [(10, 37)], RW)
    P(d, [(21, 37)], RW)
    return add_outline(img)


def back_walk1():
    img = new_img()
    d = ImageDraw.Draw(img)
    yo = -1
    # Casquette
    R(d, 12, 2+yo, 19, 2+yo, C1)
    R(d, 11, 3+yo, 20, 4+yo, C1)
    R(d, 10, 5+yo, 21, 6+yo, C1)
    R(d, 10, 5+yo, 21, 5+yo, CH)
    R(d, 9, 7+yo, 22, 7+yo, C2)
    R(d, 10, 8+yo, 21, 8+yo, C3)
    # Cheveux
    R(d, 10, 9+yo, 21, 11+yo, H1)
    R(d, 10, 9+yo, 10, 11+yo, H2)
    R(d, 21, 9+yo, 21, 11+yo, H2)
    P(d, [(9, 10+yo), (22, 10+yo)], H1)
    P(d, [(9, 11+yo), (22, 11+yo)], H1)
    R(d, 12, 12+yo, 19, 13+yo, S1)
    R(d, 11, 12+yo, 11, 13+yo, H1)
    R(d, 20, 12+yo, 20, 13+yo, H1)
    R(d, 14, 14+yo, 17, 15+yo, S2)
    R(d, 12, 16+yo, 19, 16+yo, J2)
    # Sac
    R(d, 12, 17+yo, 19, 26+yo, Y1)
    R(d, 12, 17+yo, 12, 26+yo, Y2)
    R(d, 19, 17+yo, 19, 26+yo, Y2)
    R(d, 13, 17+yo, 18, 17+yo, Y2)
    R(d, 12, 24+yo, 19, 24+yo, Y3)
    R(d, 12, 26+yo, 19, 26+yo, Y3)
    R(d, 9, 18+yo, 11, 26+yo, J1)
    R(d, 20, 18+yo, 22, 26+yo, J1)
    R(d, 9, 18+yo, 9, 26+yo, J2)
    R(d, 22, 18+yo, 22, 26+yo, J2)
    R(d, 9, 27+yo, 10, 27+yo, S1)
    R(d, 21, 27+yo, 22, 27+yo, S1)
    R(d, 11, 27+yo, 20, 27+yo, J2)
    # Jean haut
    R(d, 11, 28+yo, 20, 31+yo, P1)
    R(d, 11, 28+yo, 11, 31+yo, P2)
    R(d, 20, 28+yo, 20, 31+yo, P2)
    # Jambe G avancée
    R(d, 10, 32, 14, 36, P1)
    R(d, 10, 32, 10, 36, P2)
    R(d, 9, 37, 14, 39, R1)
    R(d, 9, 39, 14, 39, R2)
    P(d, [(9, 38)], RW)
    # Jambe D en retrait
    R(d, 17, 32, 21, 34, P1)
    R(d, 21, 32, 21, 34, P2)
    R(d, 17, 35, 22, 37, R1)
    R(d, 17, 37, 22, 37, R2)
    P(d, [(22, 36)], RW)
    return add_outline(img)


def back_walk2():
    img = new_img()
    d = ImageDraw.Draw(img)
    yo = -1
    R(d, 12, 2+yo, 19, 2+yo, C1)
    R(d, 11, 3+yo, 20, 4+yo, C1)
    R(d, 10, 5+yo, 21, 6+yo, C1)
    R(d, 10, 5+yo, 21, 5+yo, CH)
    R(d, 9, 7+yo, 22, 7+yo, C2)
    R(d, 10, 8+yo, 21, 8+yo, C3)
    R(d, 10, 9+yo, 21, 11+yo, H1)
    R(d, 10, 9+yo, 10, 11+yo, H2)
    R(d, 21, 9+yo, 21, 11+yo, H2)
    P(d, [(9, 10+yo), (22, 10+yo)], H1)
    P(d, [(9, 11+yo), (22, 11+yo)], H1)
    R(d, 12, 12+yo, 19, 13+yo, S1)
    R(d, 11, 12+yo, 11, 13+yo, H1)
    R(d, 20, 12+yo, 20, 13+yo, H1)
    R(d, 14, 14+yo, 17, 15+yo, S2)
    R(d, 12, 16+yo, 19, 16+yo, J2)
    R(d, 12, 17+yo, 19, 26+yo, Y1)
    R(d, 12, 17+yo, 12, 26+yo, Y2)
    R(d, 19, 17+yo, 19, 26+yo, Y2)
    R(d, 13, 17+yo, 18, 17+yo, Y2)
    R(d, 12, 24+yo, 19, 24+yo, Y3)
    R(d, 12, 26+yo, 19, 26+yo, Y3)
    R(d, 9, 18+yo, 11, 26+yo, J1)
    R(d, 20, 18+yo, 22, 26+yo, J1)
    R(d, 9, 18+yo, 9, 26+yo, J2)
    R(d, 22, 18+yo, 22, 26+yo, J2)
    R(d, 9, 27+yo, 10, 27+yo, S1)
    R(d, 21, 27+yo, 22, 27+yo, S1)
    R(d, 11, 27+yo, 20, 27+yo, J2)
    R(d, 11, 28+yo, 20, 31+yo, P1)
    R(d, 11, 28+yo, 11, 31+yo, P2)
    R(d, 20, 28+yo, 20, 31+yo, P2)
    # Jambe D avancée
    R(d, 17, 32, 21, 36, P1)
    R(d, 21, 32, 21, 36, P2)
    R(d, 17, 37, 22, 39, R1)
    R(d, 17, 39, 22, 39, R2)
    P(d, [(22, 38)], RW)
    # Jambe G en retrait
    R(d, 10, 32, 14, 34, P1)
    R(d, 10, 32, 10, 34, P2)
    R(d, 9, 35, 14, 37, R1)
    R(d, 9, 37, 14, 37, R2)
    P(d, [(9, 36)], RW)
    return add_outline(img)


# ═══════════════════════════════════════════════════════════
#  GAUCHE — profil tourné à gauche
# ═══════════════════════════════════════════════════════════

def left_idle():
    img = new_img()
    d = ImageDraw.Draw(img)
    # Casquette (profil G, visière pointe à gauche)
    R(d, 12, 2, 19, 2, C1)     # sommet
    R(d, 11, 3, 20, 5, C1)     # dôme
    R(d, 11, 3, 20, 3, CH)     # highlight
    R(d, 6, 6, 20, 7, C2)      # visière longue vers la gauche
    R(d, 7, 8, 20, 8, C3)      # ombre visière
    # Cheveux (côté droit, visible derrière)
    R(d, 19, 9, 21, 13, H1)
    R(d, 21, 9, 21, 13, H2)
    # Visage profil
    R(d, 11, 9, 18, 16, S1)
    R(d, 11, 16, 18, 16, S2)
    # Œil (un seul visible, côté gauche)
    R(d, 12, 11, 13, 12, EB)
    P(d, [(12, 11)], EW)
    # Nez (pointe vers la gauche)
    P(d, [(10, 13)], S2)
    # Bouche
    P(d, [(11, 15)], S2)
    # Cou
    R(d, 14, 17, 17, 17, S2)
    # Sac à dos (visible derrière, côté droit)
    R(d, 18, 18, 22, 26, Y1)
    R(d, 22, 18, 22, 26, Y2)
    R(d, 18, 26, 22, 26, Y3)
    R(d, 18, 23, 22, 23, Y3)   # bande
    # Veste corps
    R(d, 11, 18, 18, 26, J1)
    R(d, 12, 18, 16, 19, BK)   # t-shirt visible
    R(d, 11, 18, 11, 26, J2)   # bord ombre
    # Bras (juste le gauche visible, devant le corps)
    R(d, 9, 20, 11, 26, J1)
    R(d, 9, 20, 9, 26, J2)
    R(d, 9, 27, 10, 27, S1)    # main
    # Ceinture
    R(d, 11, 27, 19, 27, J2)
    # Jean
    R(d, 12, 28, 19, 35, P1)
    R(d, 12, 28, 12, 35, P2)
    R(d, 19, 28, 19, 35, P2)
    # Séparation (vue de côté, jambes décalées)
    R(d, 12, 33, 15, 35, P1)   # jambe avant
    R(d, 16, 33, 19, 35, P1)   # jambe arrière
    # Chaussures
    R(d, 10, 36, 15, 38, R1)   # avant
    R(d, 16, 36, 20, 38, R1)   # arrière
    R(d, 10, 38, 15, 38, R2)
    R(d, 16, 38, 20, 38, R2)
    P(d, [(10, 37)], RW)
    return add_outline(img)


def left_walk1():
    img = new_img()
    d = ImageDraw.Draw(img)
    yo = -1
    # Tête (identique, décalée)
    R(d, 12, 2+yo, 19, 2+yo, C1)
    R(d, 11, 3+yo, 20, 5+yo, C1)
    R(d, 11, 3+yo, 20, 3+yo, CH)
    R(d, 6, 6+yo, 20, 7+yo, C2)
    R(d, 7, 8+yo, 20, 8+yo, C3)
    R(d, 19, 9+yo, 21, 13+yo, H1)
    R(d, 21, 9+yo, 21, 13+yo, H2)
    R(d, 11, 9+yo, 18, 16+yo, S1)
    R(d, 11, 16+yo, 18, 16+yo, S2)
    R(d, 12, 11+yo, 13, 12+yo, EB)
    P(d, [(12, 11+yo)], EW)
    P(d, [(10, 13+yo)], S2)
    P(d, [(11, 15+yo)], S2)
    R(d, 14, 17+yo, 17, 17+yo, S2)
    # Sac
    R(d, 18, 18+yo, 22, 26+yo, Y1)
    R(d, 22, 18+yo, 22, 26+yo, Y2)
    R(d, 18, 26+yo, 22, 26+yo, Y3)
    R(d, 18, 23+yo, 22, 23+yo, Y3)
    # Corps
    R(d, 11, 18+yo, 18, 26+yo, J1)
    R(d, 12, 18+yo, 16, 19+yo, BK)
    R(d, 11, 18+yo, 11, 26+yo, J2)
    R(d, 9, 20+yo, 11, 26+yo, J1)
    R(d, 9, 20+yo, 9, 26+yo, J2)
    R(d, 9, 27+yo, 10, 27+yo, S1)
    R(d, 11, 27+yo, 19, 27+yo, J2)
    # Jean haut
    R(d, 12, 28+yo, 19, 31+yo, P1)
    R(d, 12, 28+yo, 12, 31+yo, P2)
    R(d, 19, 28+yo, 19, 31+yo, P2)
    # Jambe avant (gauche, étirée vers la gauche)
    R(d, 9, 32, 14, 36, P1)
    R(d, 9, 32, 9, 36, P2)
    R(d, 7, 37, 14, 39, R1)
    R(d, 7, 39, 14, 39, R2)
    P(d, [(7, 38)], RW)
    # Jambe arrière
    R(d, 16, 32, 20, 34, P1)
    R(d, 20, 32, 20, 34, P2)
    R(d, 16, 35, 21, 37, R1)
    R(d, 16, 37, 21, 37, R2)
    return add_outline(img)


def left_walk2():
    img = new_img()
    d = ImageDraw.Draw(img)
    yo = -1
    R(d, 12, 2+yo, 19, 2+yo, C1)
    R(d, 11, 3+yo, 20, 5+yo, C1)
    R(d, 11, 3+yo, 20, 3+yo, CH)
    R(d, 6, 6+yo, 20, 7+yo, C2)
    R(d, 7, 8+yo, 20, 8+yo, C3)
    R(d, 19, 9+yo, 21, 13+yo, H1)
    R(d, 21, 9+yo, 21, 13+yo, H2)
    R(d, 11, 9+yo, 18, 16+yo, S1)
    R(d, 11, 16+yo, 18, 16+yo, S2)
    R(d, 12, 11+yo, 13, 12+yo, EB)
    P(d, [(12, 11+yo)], EW)
    P(d, [(10, 13+yo)], S2)
    P(d, [(11, 15+yo)], S2)
    R(d, 14, 17+yo, 17, 17+yo, S2)
    R(d, 18, 18+yo, 22, 26+yo, Y1)
    R(d, 22, 18+yo, 22, 26+yo, Y2)
    R(d, 18, 26+yo, 22, 26+yo, Y3)
    R(d, 18, 23+yo, 22, 23+yo, Y3)
    R(d, 11, 18+yo, 18, 26+yo, J1)
    R(d, 12, 18+yo, 16, 19+yo, BK)
    R(d, 11, 18+yo, 11, 26+yo, J2)
    R(d, 9, 20+yo, 11, 26+yo, J1)
    R(d, 9, 20+yo, 9, 26+yo, J2)
    R(d, 9, 27+yo, 10, 27+yo, S1)
    R(d, 11, 27+yo, 19, 27+yo, J2)
    R(d, 12, 28+yo, 19, 31+yo, P1)
    R(d, 12, 28+yo, 12, 31+yo, P2)
    R(d, 19, 28+yo, 19, 31+yo, P2)
    # Jambe arrière (gauche, étirée vers la gauche)
    R(d, 16, 32, 20, 36, P1)
    R(d, 20, 32, 20, 36, P2)
    R(d, 16, 37, 22, 39, R1)
    R(d, 16, 39, 22, 39, R2)
    # Jambe avant (plus haut)
    R(d, 9, 32, 14, 34, P1)
    R(d, 9, 32, 9, 34, P2)
    R(d, 7, 35, 14, 37, R1)
    R(d, 7, 37, 14, 37, R2)
    P(d, [(7, 36)], RW)
    return add_outline(img)


# ═══════════════════════════════════════════════════════════
#  DROITE = flip horizontal de GAUCHE
# ═══════════════════════════════════════════════════════════

def flip_h(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


# ═══════════════════════════════════════════════════════════
#  GÉNÉRATION
# ═══════════════════════════════════════════════════════════

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    sprites = {
        "red_normal_bas_0.png":     front_idle(),
        "red_normal_bas_1.png":     front_walk1(),
        "red_normal_bas_2.png":     front_walk2(),
        "red_normal_haut_0.png":    back_idle(),
        "red_normal_haut_1.png":    back_walk1(),
        "red_normal_haut_2.png":    back_walk2(),
        "red_normal_gauche_0.png":  left_idle(),
        "red_normal_gauche_1.png":  left_walk1(),
        "red_normal_gauche_2.png":  left_walk2(),
        "red_normal_droite_0.png":  flip_h(left_idle()),
        "red_normal_droite_1.png":  flip_h(left_walk1()),
        "red_normal_droite_2.png":  flip_h(left_walk2()),
    }

    for name, img in sprites.items():
        path = os.path.join(OUT_DIR, name)
        img.save(path)
        # Stats
        px = img.load()
        opaque = sum(1 for y in range(H) for x in range(W) if px[x, y][3] > 0)
        colors = len(set(px[x, y] for y in range(H) for x in range(W) if px[x, y][3] > 0))
        print(f"  ✓ {name}: {img.size[0]}×{img.size[1]}, {opaque} px opaques, {colors} couleurs")

    print(f"\n✓ 12 sprites joueur v4 générés dans {OUT_DIR}")
    print(f"  Canvas : {W}×{H} px — style FRLG bold et lisible")


if __name__ == "__main__":
    main()
