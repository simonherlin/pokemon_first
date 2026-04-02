#!/usr/bin/env python3
"""
Générateur de tileset FRLG HD pour Pokémon Rouge/Bleu HD.
Produit des tiles 32×32px style FireRed/LeafGreen avec des couleurs riches
et des détails soignés. Pas de bruit aléatoire — pixel art déterministe propre.
"""

from PIL import Image, ImageDraw
import os, random

random.seed(42)

TILE = 32
COLS = 8  # 8 colonnes
OUT = "assets/sprites/tilesets/tileset_outdoor.png"

# ==========================================================================
# PALETTE FRLG STYLE
# ==========================================================================

# Herbe
G1 = (72, 176, 72)    # herbe vif
G2 = (56, 144, 56)    # herbe moyen
G3 = (48, 120, 48)    # herbe foncé
G4 = (88, 192, 88)    # herbe clair
G5 = (64, 160, 64)    # herbe base

# Hautes herbes
HG1 = (56, 136, 40)
HG2 = (40, 112, 32)
HG3 = (72, 152, 48)
HG4 = (48, 120, 36)

# Chemin/terre
P1 = (208, 184, 136)  # chemin clair
P2 = (184, 160, 112)  # chemin moyen
P3 = (160, 136, 96)   # chemin foncé
P4 = (224, 200, 152)  # chemin très clair

# Eau
W1 = (64, 128, 216)   # eau vif
W2 = (48, 104, 192)   # eau moyen
W3 = (40, 88, 168)    # eau foncé
W4 = (80, 152, 232)   # eau reflet

# Sable
S1 = (240, 224, 168)  # sable clair
S2 = (216, 200, 144)  # sable moyen
S3 = (200, 184, 128)  # sable foncé

# Arbre
TR1 = (32, 96, 32)    # feuillage foncé
TR2 = (48, 128, 48)   # feuillage moyen
TR3 = (64, 152, 56)   # feuillage clair
TR4 = (40, 112, 40)   # feuillage ombre
TRK = (88, 64, 40)    # tronc
TRK2 = (72, 48, 32)   # tronc ombre

# Rocher
R1 = (168, 168, 176)  # rocher clair
R2 = (136, 136, 144)  # rocher moyen
R3 = (104, 104, 112)  # rocher foncé
R4 = (184, 184, 192)  # rocher reflet

# Bâtiment (murs)
BM1 = (232, 224, 208)  # mur clair
BM2 = (208, 200, 184)  # mur moyen
BM3 = (184, 176, 160)  # mur foncé

# Toit rouge
RF1 = (200, 56, 40)    # toit rouge vif
RF2 = (168, 40, 32)    # toit rouge foncé
RF3 = (224, 80, 56)    # toit rouge clair

# Toit bleu
RB1 = (56, 88, 168)    # toit bleu
RB2 = (40, 64, 136)    # toit bleu foncé
RB3 = (80, 112, 192)   # toit bleu clair

# Porte/fenêtre
DR1 = (120, 72, 40)    # porte bois
DR2 = (96, 56, 32)     # porte ombre
WN1 = (160, 200, 232)  # fenêtre verre
WN2 = (120, 168, 208)  # fenêtre ombre

# Clôture
F1 = (200, 176, 136)   # clôture bois
F2 = (168, 144, 104)   # clôture ombre

# Fleurs
FL_R = (232, 72, 72)   # fleur rouge
FL_Y = (248, 216, 56)  # fleur jaune
FL_B = (96, 128, 232)  # fleur bleue
FL_W = (248, 248, 248) # fleur blanche

# Intérieur
IN1 = (200, 184, 152)  # sol intérieur
IN2 = (176, 160, 128)  # sol ombre
IN3 = (224, 208, 176)  # sol clair


def draw_tile(img, col, row, draw_func):
    """Dessine un tile à la position (col, row) dans l'image."""
    x0 = col * TILE
    y0 = row * TILE
    tile = Image.new("RGB", (TILE, TILE))
    draw_func(tile)
    img.paste(tile, (x0, y0))


# ==========================================================================
# FONCTIONS DE DESSIN DES TILES
# ==========================================================================

def tile_herbe(img):
    """Herbe verte classique FRLG."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    # Motif subtil d'herbe
    for y in range(0, 32, 4):
        for x in range(0, 32, 4):
            offset = (x * 7 + y * 13) % 17
            if offset < 4:
                d.point((x+1, y+1), fill=G4)
            elif offset < 8:
                d.point((x+2, y), fill=G2)
            elif offset < 11:
                d.point((x, y+2), fill=G3)
    # Brins d'herbe décoratifs
    for y in range(2, 30, 8):
        for x in range(3, 29, 8):
            seed = (x * 31 + y * 47) % 23
            if seed < 8:
                d.line([(x, y+3), (x, y)], fill=G2, width=1)
                d.line([(x+1, y+2), (x+2, y)], fill=G4, width=1)


def tile_hautes_herbes(img):
    """Hautes herbes (zones de rencontre sauvage)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=HG1)
    # Motif dense de hautes herbes
    for y in range(0, 32, 3):
        for x in range(0, 32, 3):
            seed = (x * 17 + y * 29) % 11
            if seed < 3:
                d.rectangle([x, y, x+2, y+2], fill=HG2)
            elif seed < 6:
                d.rectangle([x, y, x+1, y+2], fill=HG3)
    # Touffes
    for y in range(1, 30, 6):
        for x in range(1, 30, 6):
            sx = (x * 7 + y * 3) % 5
            d.line([(x+sx, y+4), (x+sx, y)], fill=HG2, width=1)
            d.line([(x+sx+1, y+3), (x+sx+2, y)], fill=HG3, width=1)
            d.line([(x+sx-1, y+3), (x+sx-2, y+1)], fill=HG4, width=1)


def tile_chemin(img):
    """Chemin de terre/route."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=P1)
    # Texture de terre
    for y in range(0, 32, 3):
        for x in range(0, 32, 3):
            seed = (x * 23 + y * 37) % 13
            if seed < 3:
                d.point((x, y), fill=P2)
            elif seed < 5:
                d.point((x+1, y+1), fill=P4)
            elif seed < 7:
                d.point((x, y+1), fill=P3)


def tile_eau(img):
    """Eau avec reflets."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=W1)
    # Vagues
    for y in range(2, 30, 6):
        for x in range(0, 32):
            phase = (x + y * 3) % 12
            if phase < 3:
                d.point((x, y), fill=W4)
            elif phase < 5:
                d.point((x, y+1), fill=W2)
    # Reflets lumineux
    for y in range(0, 32, 8):
        for x in range(0, 32, 8):
            sx = (x * 11 + y * 7) % 6
            d.rectangle([x+sx, y+1, x+sx+2, y+1], fill=W4)


def tile_eau_profonde(img):
    """Eau profonde/foncée."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=W3)
    for y in range(3, 30, 7):
        for x in range(0, 32):
            phase = (x + y * 5) % 14
            if phase < 2:
                d.point((x, y), fill=W2)
            elif phase < 4:
                d.point((x, y+1), fill=W1)


def tile_sable(img):
    """Plage / sable."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=S1)
    for y in range(0, 32, 2):
        for x in range(0, 32, 2):
            seed = (x * 19 + y * 41) % 17
            if seed < 3:
                d.point((x, y), fill=S2)
            elif seed < 5:
                d.point((x+1, y), fill=S3)


def tile_arbre_haut(img):
    """Cime d'arbre (partie supérieure)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)  # fond herbe
    # Couronne d'arbre (rond dans la moitié sup)
    cx, cy = 16, 12
    for y in range(0, 26):
        for x in range(0, 32):
            dx, dy = x - cx, y - cy
            dist = (dx*dx/196 + dy*dy/144)  # ellipse 14×12
            if dist < 0.6:
                d.point((x, y), fill=TR3)
            elif dist < 0.8:
                d.point((x, y), fill=TR2)
            elif dist < 1.0:
                d.point((x, y), fill=TR1)
    # Détails de feuillage
    for y in range(2, 22, 3):
        for x in range(4, 28, 3):
            dx, dy = x - cx, y - cy
            if dx*dx/196 + dy*dy/144 < 0.7:
                seed = (x * 11 + y * 7) % 7
                if seed < 2:
                    d.point((x, y), fill=TR4)
                elif seed < 4:
                    d.point((x, y), fill=TR3)


def tile_arbre_bas(img):
    """Tronc d'arbre (partie inférieure)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)  # fond herbe
    # Couronne déborde en haut
    for y in range(0, 8):
        for x in range(2, 30):
            dx = x - 16
            if abs(dx) < 14 - y:
                d.point((x, y), fill=TR2)
    # Tronc central
    for y in range(4, 28):
        for x in range(12, 20):
            d.point((x, y), fill=TRK)
        d.point((12, y), fill=TRK2)
        d.point((19, y), fill=TRK2)
    # Racines
    d.line([(10, 26), (12, 28)], fill=TRK2, width=2)
    d.line([(20, 26), (22, 28)], fill=TRK2, width=2)
    # Herbe autour du tronc
    for x in range(0, 12):
        d.point((x, 28), fill=G2)
    for x in range(20, 32):
        d.point((x, 28), fill=G2)


def tile_arbre_dense(img):
    """Arbre dense (mur d'arbres)."""
    d = ImageDraw.Draw(img)
    # Remplir de feuillage dense
    for y in range(32):
        for x in range(32):
            seed = (x * 13 + y * 31) % 19
            if seed < 5:
                d.point((x, y), fill=TR1)
            elif seed < 10:
                d.point((x, y), fill=TR2)
            elif seed < 14:
                d.point((x, y), fill=TR3)
            else:
                d.point((x, y), fill=TR4)
    # Highlights
    for y in range(2, 30, 5):
        for x in range(2, 30, 5):
            d.point((x, y), fill=TR3)


def tile_rocher(img):
    """Rocher/falaise."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=R2)
    # Texture rocheuse
    for y in range(0, 32, 2):
        for x in range(0, 32, 2):
            seed = (x * 23 + y * 41) % 11
            if seed < 3:
                d.rectangle([x, y, x+1, y+1], fill=R1)
            elif seed < 5:
                d.rectangle([x, y, x+1, y+1], fill=R3)
            elif seed < 7:
                d.point((x, y), fill=R4)
    # Fissures diagonales
    for i in range(5):
        sx = (i * 7 + 3) % 28
        sy = (i * 11 + 1) % 28
        d.line([(sx, sy), (sx+3, sy+3)], fill=R3, width=1)


def tile_mur(img):
    """Mur de bâtiment."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)
    # Briques
    for y in range(0, 32, 8):
        offset = 8 if (y // 8) % 2 else 0
        for x in range(-8, 40, 16):
            bx = x + offset
            d.rectangle([bx, y, bx+14, y+6], outline=BM3, fill=BM1)
            d.rectangle([bx+1, y+1, bx+13, y+5], fill=BM2)
            # Reflet
            d.line([(bx+1, y+1), (bx+13, y+1)], fill=BM1)


def tile_toit_rouge(img):
    """Toit rouge."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=RF1)
    # Tuiles
    for y in range(0, 32, 4):
        offset = 4 if (y // 4) % 2 else 0
        for x in range(-4, 36, 8):
            tx = x + offset
            d.line([(tx, y), (tx, y+3)], fill=RF2, width=1)
            d.line([(tx+1, y), (tx+7, y)], fill=RF3, width=1)


def tile_toit_bleu(img):
    """Toit bleu."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=RB1)
    for y in range(0, 32, 4):
        offset = 4 if (y // 4) % 2 else 0
        for x in range(-4, 36, 8):
            tx = x + offset
            d.line([(tx, y), (tx, y+3)], fill=RB2, width=1)
            d.line([(tx+1, y), (tx+7, y)], fill=RB3, width=1)


def tile_porte(img):
    """Porte d'entrée."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)  # mur fond
    # Porte
    d.rectangle([6, 2, 25, 31], fill=DR1)
    d.rectangle([7, 3, 24, 30], fill=DR1)
    d.rectangle([6, 2, 25, 2], fill=DR2)  # linteau
    d.rectangle([6, 2, 6, 31], fill=DR2)  # montant gauche
    d.rectangle([25, 2, 25, 31], fill=DR2)  # montant droit
    # Poignée
    d.ellipse([20, 14, 23, 17], fill=(200, 168, 56))


def tile_fenetre(img):
    """Mur avec fenêtre."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)
    # Fenêtre
    d.rectangle([6, 6, 25, 25], fill=WN2)
    d.rectangle([7, 7, 24, 24], fill=WN1)
    # Croisillon
    d.line([(15, 6), (15, 25)], fill=BM3, width=2)
    d.line([(6, 15), (25, 15)], fill=BM3, width=2)
    # Reflet
    d.line([(8, 8), (14, 8)], fill=(200, 224, 248))
    d.line([(8, 8), (8, 14)], fill=(200, 224, 248))


def tile_cloture(img):
    """Clôture en bois."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)  # herbe fond
    # Poteaux
    for x in [4, 28]:
        d.rectangle([x-2, 8, x+1, 31], fill=F1)
        d.rectangle([x-2, 8, x-2, 31], fill=F2)
    # Barres horizontales
    d.rectangle([2, 12, 30, 15], fill=F1)
    d.rectangle([2, 12, 30, 12], fill=F2)
    d.rectangle([2, 22, 30, 25], fill=F1)
    d.rectangle([2, 22, 30, 22], fill=F2)


def tile_fleurs(img):
    """Herbe avec fleurs."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    # Fleurs parsemées
    flowers = [(5, 8, FL_R), (14, 4, FL_Y), (24, 10, FL_B), (8, 20, FL_W),
               (18, 18, FL_R), (26, 24, FL_Y), (4, 28, FL_B), (20, 28, FL_W)]
    for fx, fy, fc in flowers:
        # Pétales (croix 3px)
        d.point((fx, fy-1), fill=fc)
        d.point((fx-1, fy), fill=fc)
        d.point((fx, fy), fill=FL_Y if fc != FL_Y else FL_W)
        d.point((fx+1, fy), fill=fc)
        d.point((fx, fy+1), fill=fc)
    # Brins d'herbe
    for y in range(3, 30, 7):
        for x in range(2, 30, 7):
            d.line([(x, y+2), (x, y)], fill=G2, width=1)


def tile_sol_interieur(img):
    """Sol d'intérieur (carrelage)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=IN1)
    # Carrelage
    d.line([(0, 0), (31, 0)], fill=IN3, width=1)
    d.line([(0, 0), (0, 31)], fill=IN3, width=1)
    d.line([(0, 31), (31, 31)], fill=IN2, width=1)
    d.line([(31, 0), (31, 31)], fill=IN2, width=1)
    # Joints
    d.line([(15, 0), (15, 31)], fill=IN2, width=1)
    d.line([(0, 15), (31, 15)], fill=IN2, width=1)


def tile_escalier(img):
    """Escalier."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=R2)
    # Marches
    for y in range(0, 32, 8):
        shade = R1 if (y // 8) % 2 == 0 else R2
        d.rectangle([0, y, 31, y+6], fill=shade)
        d.line([(0, y+7), (31, y+7)], fill=R3, width=1)
        d.line([(0, y), (31, y)], fill=R4, width=1)


def tile_centre_pokemon_toit(img):
    """Toit Centre Pokémon (rouge avec croix)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=RF1)
    # Tuiles
    for y in range(0, 32, 4):
        d.line([(0, y), (31, y)], fill=RF3, width=1)
    # Croix blanche au centre
    d.rectangle([13, 8, 18, 23], fill=(248, 248, 248))
    d.rectangle([8, 13, 23, 18], fill=(248, 248, 248))


def tile_boutique_toit(img):
    """Toit Boutique (bleu)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=RB1)
    for y in range(0, 32, 4):
        d.line([(0, y), (31, y)], fill=RB3, width=1)


def tile_corniche(img):
    """Corniche/bordure de bâtiment."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=BM1)
    d.rectangle([0, 0, 31, 4], fill=BM3)
    d.line([(0, 0), (31, 0)], fill=R3)
    d.line([(0, 5), (31, 5)], fill=BM2)


def tile_vide(img):
    """Tile noir (collision/vide)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(16, 16, 24))


def tile_grotte_sol(img):
    """Sol de grotte."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(112, 96, 80))
    for y in range(0, 32, 3):
        for x in range(0, 32, 3):
            seed = (x * 17 + y * 31) % 11
            if seed < 3:
                d.point((x, y), fill=(128, 112, 96))
            elif seed < 5:
                d.point((x, y), fill=(96, 80, 64))


def tile_grotte_mur(img):
    """Mur de grotte."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(80, 72, 64))
    for y in range(0, 32, 2):
        for x in range(0, 32, 2):
            seed = (x * 23 + y * 37) % 13
            if seed < 4:
                d.point((x, y), fill=(96, 88, 80))
            elif seed < 7:
                d.point((x, y), fill=(64, 56, 48))


def tile_pont(img):
    """Pont en bois."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=W1)  # eau sous le pont
    # Planches
    for y in range(0, 32, 6):
        d.rectangle([2, y, 29, y+4], fill=F1)
        d.line([(2, y), (29, y)], fill=F2, width=1)
        d.line([(2, y+4), (29, y+4)], fill=(152, 128, 88), width=1)
    # Rambardes
    d.rectangle([0, 0, 1, 31], fill=F2)
    d.rectangle([30, 0, 31, 31], fill=F2)


def tile_neige(img):
    """Sol enneigé."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(240, 240, 248))
    for y in range(0, 32, 3):
        for x in range(0, 32, 3):
            seed = (x * 19 + y * 29) % 11
            if seed < 3:
                d.point((x, y), fill=(224, 224, 232))
            elif seed < 5:
                d.point((x, y), fill=(248, 248, 255))


def tile_lave(img):
    """Lave."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(200, 72, 24))
    for y in range(0, 32, 2):
        for x in range(0, 32, 2):
            seed = (x * 13 + y * 23) % 9
            if seed < 2:
                d.point((x, y), fill=(240, 120, 40))
            elif seed < 4:
                d.point((x, y), fill=(248, 168, 48))
            elif seed < 6:
                d.point((x, y), fill=(168, 48, 16))


def tile_herbe_bord_haut(img):
    """Herbe avec bordure de chemin en haut."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    d.rectangle([0, 0, 31, 5], fill=P1)
    d.line([(0, 5), (31, 5)], fill=P3, width=1)
    d.line([(0, 6), (31, 6)], fill=G3, width=1)
    # Brins d'herbe
    for y in range(8, 30, 6):
        for x in range(3, 29, 6):
            d.line([(x, y+2), (x, y)], fill=G2, width=1)


def tile_herbe_bord_gauche(img):
    """Herbe avec bordure de chemin à gauche."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    d.rectangle([0, 0, 5, 31], fill=P1)
    d.line([(5, 0), (5, 31)], fill=P3, width=1)
    d.line([(6, 0), (6, 31)], fill=G3, width=1)


def tile_pancarte(img):
    """Pancarte directionnelle."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=G1)
    # Poteau
    d.rectangle([14, 16, 17, 31], fill=F2)
    # Panneau
    d.rectangle([4, 4, 27, 16], fill=F1)
    d.rectangle([4, 4, 27, 4], fill=F2)
    d.rectangle([4, 4, 4, 16], fill=F2)
    d.rectangle([27, 4, 27, 16], fill=F2)
    d.rectangle([4, 16, 27, 16], fill=F2)
    # Texte (lignes décoratives)
    d.line([(7, 7), (24, 7)], fill=(88, 64, 40))
    d.line([(7, 10), (20, 10)], fill=(88, 64, 40))
    d.line([(7, 13), (22, 13)], fill=(88, 64, 40))


def tile_tapis_rouge(img):
    """Tapis rouge (intérieur)."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(184, 48, 48))
    d.rectangle([1, 1, 30, 30], fill=(200, 56, 56))
    d.rectangle([2, 2, 29, 29], fill=(216, 64, 64))
    # Motif
    for y in range(4, 28, 6):
        for x in range(4, 28, 6):
            d.rectangle([x, y, x+2, y+2], fill=(184, 48, 48))


def tile_mur_interieur(img):
    """Mur intérieur."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], fill=(216, 208, 192))
    d.line([(0, 28), (31, 28)], fill=(184, 176, 160), width=2)
    d.line([(0, 30), (31, 30)], fill=(168, 160, 144), width=2)


# ==========================================================================
# ASSEMBLAGE DU TILESET
# ==========================================================================

# Disposition du tileset : 8 colonnes × N lignes
# Range 0 : terrain de base
# Range 1 : eau et transitions
# Range 2 : arbres et végétation
# Range 3 : bâtiments
# Range 4 : intérieur
# Range 5 : spécial

TILE_MAP = [
    # Rangée 0 : terrain de base
    [tile_herbe, tile_hautes_herbes, tile_chemin, tile_sable,
     tile_fleurs, tile_herbe_bord_haut, tile_herbe_bord_gauche, tile_neige],
    # Rangée 1 : eau
    [tile_eau, tile_eau_profonde, tile_pont, tile_lave,
     tile_vide, tile_vide, tile_vide, tile_vide],
    # Rangée 2 : arbres et nature
    [tile_arbre_haut, tile_arbre_bas, tile_arbre_dense, tile_rocher,
     tile_cloture, tile_pancarte, tile_vide, tile_vide],
    # Rangée 3 : bâtiments extérieur
    [tile_mur, tile_fenetre, tile_porte, tile_toit_rouge,
     tile_toit_bleu, tile_centre_pokemon_toit, tile_boutique_toit, tile_corniche],
    # Rangée 4 : intérieur
    [tile_sol_interieur, tile_escalier, tile_tapis_rouge, tile_mur_interieur,
     tile_grotte_sol, tile_grotte_mur, tile_vide, tile_vide],
]

def main():
    rows = len(TILE_MAP)
    width = COLS * TILE
    height = rows * TILE
    img = Image.new("RGB", (width, height), (0, 0, 0))
    
    for row_idx, row_tiles in enumerate(TILE_MAP):
        for col_idx, tile_func in enumerate(row_tiles):
            draw_tile(img, col_idx, row_idx, tile_func)
    
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG")
    print(f"Tileset généré : {OUT} ({width}×{height}px, {COLS}×{rows} tiles)")

if __name__ == "__main__":
    main()
