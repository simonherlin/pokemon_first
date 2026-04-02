#!/usr/bin/env python3
"""
Générateur de sprites joueur style Pokémon FRLG
Crée Red (Rouge) avec 4 directions × 3 frames = 12 sprites
Taille : 32×64 pixels (2 tiles de haut)
"""

from PIL import Image

# Palette Red/Rouge (style FRLG GBA)
T = (0, 0, 0, 0)       # Transparent
K = (16, 16, 24, 255)   # Noir (outlines)
# Casquette
R1 = (232, 64, 48, 255)   # Rouge clair
R2 = (200, 40, 32, 255)   # Rouge moyen
R3 = (160, 24, 16, 255)   # Rouge foncé
# Cheveux
H1 = (80, 48, 32, 255)    # Cheveux clair
H2 = (56, 32, 16, 255)    # Cheveux foncé
# Peau
S1 = (248, 208, 168, 255) # Peau clair
S2 = (224, 176, 128, 255) # Peau moyen
S3 = (192, 144, 96, 255)  # Peau foncé
# Yeux
E1 = (40, 40, 56, 255)    # Yeux
# T-shirt / Veste
W1 = (248, 248, 255, 255) # Blanc
W2 = (216, 216, 232, 255) # Gris clair
W3 = (184, 184, 200, 255) # Gris
# Pantalon (jean bleu)
B1 = (80, 112, 184, 255)  # Bleu clair
B2 = (56, 80, 152, 255)   # Bleu
B3 = (40, 56, 120, 255)   # Bleu foncé
# Chaussures
SH1 = (168, 88, 48, 255)  # Chaussure clair
SH2 = (128, 64, 32, 255)  # Chaussure foncé
# Sac à dos
BK1 = (248, 176, 56, 255) # Sac jaune
BK2 = (216, 144, 32, 255) # Sac jaune foncé

def create_sprite(width=32, height=64):
    """Crée une image RGBA transparente"""
    return Image.new("RGBA", (width, height), T)

def set_pixels(img, pixel_data, ox=0, oy=0):
    """Place des pixels à partir d'un dictionnaire {(x,y): color}"""
    for (x, y), c in pixel_data.items():
        px, py = x + ox, y + oy
        if 0 <= px < img.width and 0 <= py < img.height:
            img.putpixel((px, py), c)

def mirror_h(pixel_data, center_x=15):
    """Miroir horizontal autour de center_x"""
    mirrored = {}
    for (x, y), c in pixel_data.items():
        mx = 2 * center_x - x + 1
        mirrored[(mx, y)] = c
    return mirrored


# ========== BAS (face au joueur) ==========

def draw_bas_idle():
    """Red vu de face, position neutre"""
    img = create_sprite()
    p = {}

    # --- Casquette (rangées 24-30) ---
    # Visière
    for x in range(9, 23):
        p[(x, 24)] = R3
    for x in range(8, 24):
        p[(x, 25)] = R2
    for x in range(7, 25):
        p[(x, 26)] = R1
    # Dôme de la casquette
    for x in range(9, 23):
        p[(x, 27)] = R2
    for x in range(10, 22):
        p[(x, 28)] = R1
    # Logo casquette
    p[(15, 26)] = W1
    p[(16, 26)] = W1
    p[(15, 27)] = W2
    p[(16, 27)] = W2

    # --- Cheveux sur les côtés ---
    for y in range(28, 32):
        p[(8, y)] = H1
        p[(9, y)] = H2
        p[(22, y)] = H2
        p[(23, y)] = H1

    # --- Visage (rangées 29-35) ---
    # Forme du visage
    for x in range(10, 22):
        for y in range(29, 35):
            p[(x, y)] = S1
    # Ombrage bas du visage
    for x in range(10, 22):
        p[(x, 34)] = S2
    p[(10, 33)] = S2
    p[(21, 33)] = S2
    # Yeux
    p[(12, 31)] = E1
    p[(13, 31)] = E1
    p[(18, 31)] = E1
    p[(19, 31)] = E1
    # Reflet yeux
    p[(12, 30)] = W1
    p[(18, 30)] = W1
    # Bouche
    p[(15, 33)] = S3
    p[(16, 33)] = S3
    # Nez
    p[(15, 32)] = S2
    p[(16, 32)] = S2
    # Contour visage
    for y in range(29, 35):
        p[(9, y)] = K
        p[(22, y)] = K
    for x in range(10, 22):
        p[(x, 35)] = K  # Menton

    # --- Cou ---
    for x in range(13, 19):
        p[(x, 36)] = S2

    # --- T-shirt / Veste (rangées 37-43) ---
    for y in range(37, 44):
        for x in range(8, 24):
            p[(x, y)] = W1
    # Ombres veste
    for y in range(37, 44):
        p[(8, y)] = W3
        p[(9, y)] = W2
        p[(22, y)] = W2
        p[(23, y)] = W3
    # Col
    for x in range(12, 20):
        p[(x, 37)] = K
    p[(13, 38)] = K
    p[(18, 38)] = K
    # Bras (manches courtes)
    for y in range(38, 42):
        p[(7, y)] = W2
        p[(6, y)] = S1
        p[(24, y)] = W2
        p[(25, y)] = S1
    for y in range(42, 45):
        p[(6, y)] = S2
        p[(25, y)] = S2
    # Mains
    p[(6, 45)] = S1
    p[(25, 45)] = S1
    # Ouverture veste
    p[(15, 39)] = K
    p[(16, 39)] = K
    p[(15, 40)] = K
    p[(16, 40)] = K
    p[(15, 41)] = K
    p[(16, 41)] = K
    # Contour veste
    for y in range(37, 44):
        p[(7, y)] = K
        p[(24, y)] = K
    for x in range(8, 24):
        p[(x, 44)] = K  # Bas veste

    # --- Pantalon (rangées 44-52) ---
    for y in range(44, 53):
        for x in range(9, 23):
            p[(x, y)] = B1
    # Ombres pantalon
    for y in range(44, 53):
        p[(9, y)] = B3
        p[(22, y)] = B3
    # Séparation jambes
    for y in range(48, 53):
        p[(15, y)] = B3
        p[(16, y)] = B3
    # Ceinture
    for x in range(9, 23):
        p[(x, 44)] = B3
    p[(15, 44)] = BK1  # Boucle
    p[(16, 44)] = BK1
    # Contour pantalon
    for y in range(44, 53):
        p[(8, y)] = K
        p[(23, y)] = K

    # --- Chaussures (rangées 53-56) ---
    for y in range(53, 57):
        for x in range(8, 15):
            p[(x, y)] = SH1
        for x in range(17, 24):
            p[(x, y)] = SH1
    for x in range(8, 15):
        p[(x, 56)] = SH2
    for x in range(17, 24):
        p[(x, 56)] = SH2
    # Contour chaussures
    for y in range(53, 57):
        p[(7, y)] = K
        p[(15, y)] = K
        p[(16, y)] = K
        p[(24, y)] = K

    set_pixels(img, p)
    return img


def draw_bas_walk1():
    """Red vu de face, jambe gauche avancée"""
    img = draw_bas_idle()
    # Décaler jambe gauche d'un pixel vers la gauche
    # et jambe droite vers la droite pour effet de marche
    p = {}
    # Effacer les pieds actuels
    for y in range(53, 57):
        for x in range(7, 25):
            p[(x, y)] = T
    # Pied gauche avancé (décalé gauche de 2px)
    for y in range(53, 58):
        for x in range(6, 13):
            p[(x, y)] = SH1
    for x in range(6, 13):
        p[(x, 57)] = SH2
    for y in range(53, 58):
        p[(5, y)] = K
        p[(13, y)] = K
    # Pied droit reculé
    for y in range(52, 56):
        for x in range(18, 25):
            p[(x, y)] = SH1
    for x in range(18, 25):
        p[(x, 55)] = SH2
    for y in range(52, 56):
        p[(17, y)] = K
        p[(25, y)] = K

    set_pixels(img, p)
    return img


def draw_bas_walk2():
    """Red vu de face, jambe droite avancée"""
    img = draw_bas_idle()
    p = {}
    for y in range(53, 57):
        for x in range(7, 25):
            p[(x, y)] = T
    # Pied droit avancé
    for y in range(53, 58):
        for x in range(19, 26):
            p[(x, y)] = SH1
    for x in range(19, 26):
        p[(x, 57)] = SH2
    for y in range(53, 58):
        p[(18, y)] = K
        p[(26, y)] = K
    # Pied gauche reculé
    for y in range(52, 56):
        for x in range(7, 14):
            p[(x, y)] = SH1
    for x in range(7, 14):
        p[(x, 55)] = SH2
    for y in range(52, 56):
        p[(6, y)] = K
        p[(14, y)] = K

    set_pixels(img, p)
    return img


# ========== HAUT (dos) ==========

def draw_haut_idle():
    """Red vu de dos, position neutre"""
    img = create_sprite()
    p = {}

    # --- Casquette (vue de dos) ---
    for x in range(9, 23):
        p[(x, 24)] = R3
    for x in range(8, 24):
        p[(x, 25)] = R2
    for x in range(8, 24):
        p[(x, 26)] = R1
    for x in range(9, 23):
        p[(x, 27)] = R2
        p[(x, 28)] = R2
    # Bande arrière casquette
    for x in range(12, 20):
        p[(x, 26)] = R3

    # --- Cheveux ---
    for y in range(27, 33):
        p[(8, y)] = H1
        p[(9, y)] = H2
        p[(22, y)] = H2
        p[(23, y)] = H1
    # Arrière tête
    for x in range(10, 22):
        for y in range(28, 34):
            p[(x, y)] = H2
    for x in range(11, 21):
        for y in range(29, 33):
            p[(x, y)] = H1
    # Bas cheveux
    for x in range(10, 22):
        p[(x, 34)] = H2
    p[(10, 35)] = H2
    p[(21, 35)] = H2
    # Bout de peau visible (nuque)
    for x in range(13, 19):
        p[(x, 35)] = S2
    for x in range(12, 20):
        p[(x, 34)] = H2

    # --- Cou ---
    for x in range(13, 19):
        p[(x, 36)] = S2

    # --- Veste (dos) ---
    for y in range(37, 44):
        for x in range(8, 24):
            p[(x, y)] = W1
    for y in range(37, 44):
        p[(8, y)] = W3
        p[(23, y)] = W3
        p[(9, y)] = W2
        p[(22, y)] = W2
    # Sac à dos
    for y in range(38, 43):
        for x in range(11, 21):
            p[(x, y)] = BK1
    for y in range(38, 43):
        p[(11, y)] = BK2
        p[(20, y)] = BK2
    for x in range(11, 21):
        p[(x, 43)] = BK2
    # Bras
    for y in range(38, 42):
        p[(7, y)] = W2
        p[(6, y)] = S1
        p[(24, y)] = W2
        p[(25, y)] = S1
    for y in range(42, 45):
        p[(6, y)] = S2
        p[(25, y)] = S2
    p[(6, 45)] = S1
    p[(25, 45)] = S1
    # Contour
    for y in range(37, 44):
        p[(7, y)] = K
        p[(24, y)] = K

    # --- Pantalon ---
    for y in range(44, 53):
        for x in range(9, 23):
            p[(x, y)] = B1
    for y in range(44, 53):
        p[(9, y)] = B3
        p[(22, y)] = B3
    for y in range(48, 53):
        p[(15, y)] = B3
        p[(16, y)] = B3
    for x in range(9, 23):
        p[(x, 44)] = B3
    for y in range(44, 53):
        p[(8, y)] = K
        p[(23, y)] = K

    # --- Chaussures ---
    for y in range(53, 57):
        for x in range(8, 15):
            p[(x, y)] = SH1
        for x in range(17, 24):
            p[(x, y)] = SH1
    for x in range(8, 15):
        p[(x, 56)] = SH2
    for x in range(17, 24):
        p[(x, 56)] = SH2
    for y in range(53, 57):
        p[(7, y)] = K
        p[(15, y)] = K
        p[(16, y)] = K
        p[(24, y)] = K

    set_pixels(img, p)
    return img


def draw_haut_walk1():
    """Red vu de dos, marche 1"""
    img = draw_haut_idle()
    p = {}
    for y in range(53, 57):
        for x in range(7, 25):
            p[(x, y)] = T
    for y in range(53, 58):
        for x in range(6, 13):
            p[(x, y)] = SH1
    for x in range(6, 13):
        p[(x, 57)] = SH2
    for y in range(53, 58):
        p[(5, y)] = K
        p[(13, y)] = K
    for y in range(52, 56):
        for x in range(18, 25):
            p[(x, y)] = SH1
    for x in range(18, 25):
        p[(x, 55)] = SH2
    for y in range(52, 56):
        p[(17, y)] = K
        p[(25, y)] = K
    set_pixels(img, p)
    return img


def draw_haut_walk2():
    """Red vu de dos, marche 2"""
    img = draw_haut_idle()
    p = {}
    for y in range(53, 57):
        for x in range(7, 25):
            p[(x, y)] = T
    for y in range(53, 58):
        for x in range(19, 26):
            p[(x, y)] = SH1
    for x in range(19, 26):
        p[(x, 57)] = SH2
    for y in range(53, 58):
        p[(18, y)] = K
        p[(26, y)] = K
    for y in range(52, 56):
        for x in range(7, 14):
            p[(x, y)] = SH1
    for x in range(7, 14):
        p[(x, 55)] = SH2
    for y in range(52, 56):
        p[(6, y)] = K
        p[(14, y)] = K
    set_pixels(img, p)
    return img


# ========== GAUCHE ==========

def draw_gauche_idle():
    """Red vu de profil gauche, position neutre"""
    img = create_sprite()
    p = {}

    # --- Casquette ---
    for x in range(6, 20):
        p[(x, 24)] = R3
    for x in range(5, 20):
        p[(x, 25)] = R2
    for x in range(4, 20):
        p[(x, 26)] = R1
    # Visière vers la gauche
    for x in range(2, 10):
        p[(x, 27)] = R1
    for x in range(10, 20):
        p[(x, 27)] = R2
    for x in range(3, 10):
        p[(x, 28)] = R3
    for x in range(10, 19):
        p[(x, 28)] = R2

    # --- Cheveux ---
    for y in range(28, 33):
        p[(18, y)] = H1
        p[(19, y)] = H1
    for y in range(29, 34):
        p[(17, y)] = H2

    # --- Visage (profil) ---
    for x in range(9, 18):
        for y in range(29, 35):
            p[(x, y)] = S1
    # Ombrage
    for x in range(9, 18):
        p[(x, 34)] = S2
    p[(9, 33)] = S2
    # Oeil
    p[(10, 31)] = E1
    p[(11, 31)] = E1
    p[(10, 30)] = W1  # reflet
    # Nez
    p[(8, 32)] = S2
    # Bouche
    p[(10, 33)] = S3
    # Oreille
    p[(17, 31)] = S2
    p[(17, 32)] = S2
    # Contour
    for y in range(29, 35):
        p[(8, y)] = K
        p[(18, y)] = K
    for x in range(9, 18):
        p[(x, 35)] = K

    # --- Cou ---
    for x in range(12, 17):
        p[(x, 36)] = S2

    # --- Veste ---
    for y in range(37, 44):
        for x in range(8, 22):
            p[(x, y)] = W1
    for y in range(37, 44):
        p[(8, y)] = W3
        p[(21, y)] = W2
    # Col
    for x in range(10, 17):
        p[(x, 37)] = K
    # Bras (profil gauche = bras visible à droite)
    for y in range(38, 45):
        p[(7, y)] = S1
    for y in range(38, 42):
        p[(6, y)] = S2
    p[(7, 45)] = S1
    # Sac à dos (visible à droite)
    for y in range(38, 43):
        p[(22, y)] = BK1
        p[(23, y)] = BK2
    # Contour
    for y in range(37, 44):
        p[(6, y)] = K
        p[(24, y)] = K if y < 43 else K

    # --- Pantalon ---
    for y in range(44, 53):
        for x in range(9, 21):
            p[(x, y)] = B1
    for y in range(44, 53):
        p[(9, y)] = B3
        p[(20, y)] = B3
    for x in range(9, 21):
        p[(x, 44)] = B3
    for y in range(44, 53):
        p[(8, y)] = K
        p[(21, y)] = K

    # --- Chaussures ---
    for y in range(53, 57):
        for x in range(8, 21):
            p[(x, y)] = SH1
    for x in range(8, 21):
        p[(x, 56)] = SH2
    for y in range(53, 57):
        p[(7, y)] = K
        p[(21, y)] = K

    set_pixels(img, p)
    return img


def draw_gauche_walk1():
    """Red profil gauche, marche 1"""
    img = draw_gauche_idle()
    p = {}
    for y in range(53, 57):
        for x in range(7, 22):
            p[(x, y)] = T
    # Pied avant (gauche)
    for y in range(53, 58):
        for x in range(5, 14):
            p[(x, y)] = SH1
    for x in range(5, 14):
        p[(x, 57)] = SH2
    for y in range(53, 58):
        p[(4, y)] = K
        p[(14, y)] = K
    # Pied arrière
    for y in range(52, 56):
        for x in range(14, 22):
            p[(x, y)] = SH1
    for x in range(14, 22):
        p[(x, 55)] = SH2
    for y in range(52, 56):
        p[(13, y)] = K
        p[(22, y)] = K
    set_pixels(img, p)
    return img


def draw_gauche_walk2():
    """Red profil gauche, marche 2"""
    img = draw_gauche_idle()
    p = {}
    for y in range(53, 57):
        for x in range(7, 22):
            p[(x, y)] = T
    for y in range(53, 58):
        for x in range(10, 19):
            p[(x, y)] = SH1
    for x in range(10, 19):
        p[(x, 57)] = SH2
    for y in range(53, 58):
        p[(9, y)] = K
        p[(19, y)] = K
    set_pixels(img, p)
    return img


# ========== DROITE (miroir de GAUCHE) ==========

def mirror_image(img, width=32):
    """Miroir horizontal d'une image"""
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def draw_droite_idle():
    return mirror_image(draw_gauche_idle())

def draw_droite_walk1():
    return mirror_image(draw_gauche_walk1())

def draw_droite_walk2():
    return mirror_image(draw_gauche_walk2())


# ========== ASSEMBLAGE ==========

def main():
    output_dir = "assets/sprites/characters"

    sprites = {
        "red_normal_bas_0": draw_bas_idle,
        "red_normal_bas_1": draw_bas_walk1,
        "red_normal_bas_2": draw_bas_walk2,
        "red_normal_haut_0": draw_haut_idle,
        "red_normal_haut_1": draw_haut_walk1,
        "red_normal_haut_2": draw_haut_walk2,
        "red_normal_gauche_0": draw_gauche_idle,
        "red_normal_gauche_1": draw_gauche_walk1,
        "red_normal_gauche_2": draw_gauche_walk2,
        "red_normal_droite_0": draw_droite_idle,
        "red_normal_droite_1": draw_droite_walk1,
        "red_normal_droite_2": draw_droite_walk2,
    }

    for name, func in sprites.items():
        img = func()
        path = f"{output_dir}/{name}.png"
        img.save(path)

        # Count non-transparent pixels
        pixels = list(img.getdata())
        opaque = sum(1 for p in pixels if p[3] > 0)
        colors = len(set(p for p in pixels if p[3] > 0))
        print(f"  {name}: {opaque} opaque pixels, {colors} colors")

    print(f"\n12 sprites générés dans {output_dir}/")


if __name__ == "__main__":
    main()
