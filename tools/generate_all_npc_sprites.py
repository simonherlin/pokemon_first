#!/usr/bin/env python3
"""
Générateur complet de sprites PNJ pour Pokémon FRLG HD.
Génère TOUS les types de PNJ utilisés dans le jeu.
Chaque sprite : 32×64 RGBA, style FRLG overworld.
4 directions × 3 frames (idle, pas_gauche, pas_droit) = 12 PNG par personnage.

Sprites statiques (panneau, objet) : 1 PNG (bas_0 uniquement).
"""

from PIL import Image, ImageDraw
import os

OUTPUT_DIR = "assets/sprites/characters"

# ============================================================================
# PALETTE COMMUNE
# ============================================================================
TRANSPARENT = (0, 0, 0, 0)
OUTLINE = (24, 24, 32, 255)
SKIN_LIGHT = (255, 224, 176, 255)
SKIN_MID = (232, 192, 144, 255)
SKIN_DARK = (200, 160, 112, 255)
SKIN_SHADOW = (168, 128, 88, 255)
EYE_WHITE = (255, 255, 255, 255)
EYE_BLACK = (16, 16, 32, 255)
HAIR_BLACK = (32, 32, 48, 255)
HAIR_DARK = (48, 40, 56, 255)
HAIR_BROWN = (120, 72, 40, 255)
HAIR_BROWN_L = (152, 96, 56, 255)
HAIR_RED = (192, 64, 48, 255)
HAIR_RED_L = (224, 96, 72, 255)
HAIR_BLUE = (64, 96, 168, 255)
HAIR_PINK = (232, 136, 168, 255)
HAIR_PINK_L = (248, 176, 200, 255)
HAIR_GREEN = (72, 144, 80, 255)
HAIR_GREY = (160, 160, 168, 255)
HAIR_GREY_L = (192, 192, 200, 255)
WHITE = (248, 248, 248, 255)
WHITE_S = (216, 216, 224, 255)
BLACK = (32, 32, 40, 255)
RED = (200, 48, 48, 255)
RED_L = (232, 80, 72, 255)
BLUE = (56, 88, 168, 255)
BLUE_L = (88, 120, 200, 255)
BLUE_D = (40, 64, 128, 255)
GREEN = (56, 152, 72, 255)
GREEN_L = (88, 184, 104, 255)
BROWN = (120, 80, 48, 255)
BROWN_L = (152, 104, 64, 255)
BROWN_D = (88, 56, 32, 255)
GREY = (128, 128, 136, 255)
GREY_L = (168, 168, 176, 255)
GREY_D = (88, 88, 96, 255)
YELLOW = (232, 200, 72, 255)
YELLOW_L = (248, 224, 112, 255)
PINK = (232, 136, 168, 255)
PINK_L = (248, 176, 200, 255)
PURPLE = (136, 72, 168, 255)
PURPLE_L = (168, 104, 200, 255)
ORANGE = (224, 144, 56, 255)
TEAL = (72, 168, 168, 255)
WOOD_LIGHT = (192, 152, 96, 255)
WOOD_MID = (152, 112, 64, 255)
WOOD_DARK = (112, 80, 40, 255)


# ============================================================================
# UTILITAIRES
# ============================================================================
def new_sprite():
    return Image.new("RGBA", (32, 64), TRANSPARENT)

def px(img, x, y, color):
    """Place un pixel si dans les limites."""
    if 0 <= x < 32 and 0 <= y < 64:
        img.putpixel((x, y), color)

def fill_rect(img, x1, y1, x2, y2, color):
    """Remplit un rectangle."""
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            px(img, x, y, color)

def draw_outline_rect(img, x1, y1, x2, y2, fill_color, outline_color=OUTLINE):
    """Rectangle avec contour."""
    fill_rect(img, x1, y1, x2, y2, fill_color)
    for x in range(x1, x2 + 1):
        px(img, x, y1, outline_color)
        px(img, x, y2, outline_color)
    for y in range(y1, y2 + 1):
        px(img, x1, y, outline_color)
        px(img, x2, y, outline_color)

def mirror_h(img):
    """Miroir horizontal."""
    return img.transpose(Image.FLIP_LEFT_RIGHT)


# ============================================================================
# DESSIN D'UN PERSONNAGE GÉNÉRIQUE
# ============================================================================
def draw_generic_character(
    img, facing, frame,
    hair_colors, shirt_colors, pants_colors, shoe_color,
    hair_style="short", has_hat=False, hat_colors=None,
    is_female=False, has_skirt=False, skirt_colors=None,
    accessory=None, accessory_colors=None
):
    """
    Dessine un personnage générique avec paramètres personnalisables.
    facing: 'bas', 'haut', 'gauche', 'droite'
    frame: 0 (idle), 1 (pas gauche), 2 (pas droit)
    hair_colors: (main, highlight)
    shirt_colors: (main, highlight, shadow)
    pants_colors: (main, highlight)
    shoe_color: color
    """
    hair_main, hair_hi = hair_colors
    shirt_main, shirt_hi, shirt_sh = shirt_colors
    pants_main, pants_hi = pants_colors
    
    # Offsets de marche
    foot_offset = 0
    if frame == 1:
        foot_offset = -1
    elif frame == 2:
        foot_offset = 1
    
    body_bob = 0
    if frame in (1, 2):
        body_bob = -1
    
    if facing == "bas":
        _draw_front(img, body_bob, foot_offset,
                   hair_main, hair_hi, shirt_main, shirt_hi, shirt_sh,
                   pants_main, pants_hi, shoe_color,
                   hair_style, has_hat, hat_colors, is_female, has_skirt, skirt_colors,
                   accessory, accessory_colors)
    elif facing == "haut":
        _draw_back(img, body_bob, foot_offset,
                  hair_main, hair_hi, shirt_main, shirt_hi, shirt_sh,
                  pants_main, pants_hi, shoe_color,
                  hair_style, has_hat, hat_colors, is_female, has_skirt, skirt_colors,
                  accessory, accessory_colors)
    elif facing == "gauche":
        _draw_side(img, body_bob, foot_offset, False,
                  hair_main, hair_hi, shirt_main, shirt_hi, shirt_sh,
                  pants_main, pants_hi, shoe_color,
                  hair_style, has_hat, hat_colors, is_female, has_skirt, skirt_colors,
                  accessory, accessory_colors)
    elif facing == "droite":
        _draw_side(img, body_bob, foot_offset, True,
                  hair_main, hair_hi, shirt_main, shirt_hi, shirt_sh,
                  pants_main, pants_hi, shoe_color,
                  hair_style, has_hat, hat_colors, is_female, has_skirt, skirt_colors,
                  accessory, accessory_colors)


def _draw_front(img, bob, foot_off, 
               hair_m, hair_h, shirt_m, shirt_h, shirt_s,
               pants_m, pants_h, shoe, hair_style, has_hat, hat_col,
               is_female, has_skirt, skirt_col, accessory, acc_col):
    """Vue de face (bas)."""
    y_off = 20 + bob  # Base Y offset for the head
    
    # --- Cheveux (arrière) ---
    if hair_style == "long" or is_female:
        fill_rect(img, 10, y_off - 2, 21, y_off + 14, hair_m)
        fill_rect(img, 11, y_off - 2, 20, y_off - 1, hair_h)
    
    # --- Tête ---
    # Crâne
    fill_rect(img, 11, y_off, 20, y_off + 11, SKIN_LIGHT)
    fill_rect(img, 12, y_off - 1, 19, y_off - 1, SKIN_LIGHT)
    # Contour
    for x in range(11, 21):
        px(img, x, y_off + 12, OUTLINE)
    for y in range(y_off, y_off + 12):
        px(img, 10, y, OUTLINE)
        px(img, 21, y, OUTLINE)
    for x in range(12, 20):
        px(img, x, y_off - 2, OUTLINE)
    px(img, 11, y_off - 1, OUTLINE)
    px(img, 20, y_off - 1, OUTLINE)
    
    # --- Cheveux (devant) ---
    if has_hat and hat_col:
        hat_m, hat_h = hat_col
        fill_rect(img, 10, y_off - 3, 21, y_off + 2, hat_m)
        fill_rect(img, 11, y_off - 3, 20, y_off - 2, hat_h)
        # Visière
        fill_rect(img, 8, y_off + 2, 23, y_off + 3, hat_m)
        for x in range(8, 24):
            px(img, x, y_off + 4, OUTLINE)
    else:
        # Cheveux
        fill_rect(img, 11, y_off - 1, 20, y_off + 2, hair_m)
        fill_rect(img, 12, y_off - 1, 19, y_off, hair_h)
        if hair_style == "long" or is_female:
            # Cheveux longs sur les côtés
            fill_rect(img, 9, y_off + 2, 10, y_off + 14, hair_m)
            fill_rect(img, 21, y_off + 2, 22, y_off + 14, hair_m)
    
    # --- Visage ---
    # Yeux
    px(img, 13, y_off + 5, EYE_WHITE)
    px(img, 14, y_off + 5, EYE_BLACK)
    px(img, 17, y_off + 5, EYE_BLACK)
    px(img, 18, y_off + 5, EYE_WHITE)
    # Bouche
    px(img, 15, y_off + 8, SKIN_DARK)
    px(img, 16, y_off + 8, SKIN_DARK)
    # Ombre menton
    fill_rect(img, 12, y_off + 10, 19, y_off + 11, SKIN_MID)
    
    # --- Corps (torse) ---
    body_y = y_off + 13
    fill_rect(img, 10, body_y, 21, body_y + 10, shirt_m)
    fill_rect(img, 12, body_y, 19, body_y + 2, shirt_h)
    fill_rect(img, 10, body_y + 8, 21, body_y + 10, shirt_s)
    # Contour corps
    for y in range(body_y, body_y + 11):
        px(img, 9, y, OUTLINE)
        px(img, 22, y, OUTLINE)
    # Bras
    fill_rect(img, 7, body_y + 2, 9, body_y + 8, shirt_m)
    fill_rect(img, 22, body_y + 2, 24, body_y + 8, shirt_m)
    fill_rect(img, 7, body_y + 9, 9, body_y + 10, SKIN_LIGHT)  # Mains
    fill_rect(img, 22, body_y + 9, 24, body_y + 10, SKIN_LIGHT)
    
    # --- Bas (pantalon/jupe) ---
    legs_y = body_y + 11
    if has_skirt and skirt_col:
        skirt_m, skirt_h = skirt_col
        # Jupe
        fill_rect(img, 9, legs_y, 22, legs_y + 4, skirt_m)
        fill_rect(img, 10, legs_y, 21, legs_y + 1, skirt_h)
        # Jambes sous la jupe
        fill_rect(img, 12, legs_y + 5, 14, legs_y + 8, SKIN_LIGHT)
        fill_rect(img, 17, legs_y + 5, 19, legs_y + 8, SKIN_LIGHT)
    else:
        # Pantalon
        fill_rect(img, 10, legs_y, 21, legs_y + 2, pants_m)
        fill_rect(img, 12, legs_y, 19, legs_y, pants_h)
        # Jambes
        x_left = 11 + foot_off
        x_right = 18 - foot_off
        fill_rect(img, x_left, legs_y + 3, x_left + 2, legs_y + 7, pants_m)
        fill_rect(img, x_right, legs_y + 3, x_right + 2, legs_y + 7, pants_m)
    
    # --- Chaussures ---
    shoe_y = legs_y + 8 if not (has_skirt and skirt_col) else legs_y + 9
    if has_skirt and skirt_col:
        fill_rect(img, 11 + foot_off, shoe_y, 14 + foot_off, shoe_y + 1, shoe)
        fill_rect(img, 16 - foot_off, shoe_y, 19 - foot_off, shoe_y + 1, shoe)
    else:
        fill_rect(img, 10 + foot_off, shoe_y, 13 + foot_off, shoe_y + 1, shoe)
        fill_rect(img, 17 - foot_off, shoe_y, 20 - foot_off, shoe_y + 1, shoe)
    
    # --- Accessoire ---
    if accessory == "letter_R" and acc_col:
        # Lettre R sur le torse (Team Rocket)
        r_col = acc_col[0]
        px(img, 14, body_y + 3, r_col)
        px(img, 15, body_y + 3, r_col)
        px(img, 16, body_y + 3, r_col)
        px(img, 14, body_y + 4, r_col)
        px(img, 16, body_y + 4, r_col)
        px(img, 14, body_y + 5, r_col)
        px(img, 15, body_y + 5, r_col)
        px(img, 14, body_y + 6, r_col)
        px(img, 16, body_y + 6, r_col)
    elif accessory == "apron" and acc_col:
        # Tablier (vendeur)
        ap_col = acc_col[0]
        fill_rect(img, 12, body_y + 3, 19, body_y + 9, ap_col)


def _draw_back(img, bob, foot_off,
              hair_m, hair_h, shirt_m, shirt_h, shirt_s,
              pants_m, pants_h, shoe, hair_style, has_hat, hat_col,
              is_female, has_skirt, skirt_col, accessory, acc_col):
    """Vue de dos (haut)."""
    y_off = 20 + bob
    
    # --- Tête (dos = cheveux visibles) ---
    fill_rect(img, 11, y_off, 20, y_off + 11, hair_m)
    fill_rect(img, 12, y_off - 1, 19, y_off - 1, hair_m)
    fill_rect(img, 12, y_off, 19, y_off + 3, hair_h)
    
    if has_hat and hat_col:
        hat_m, hat_h = hat_col
        fill_rect(img, 10, y_off - 3, 21, y_off + 2, hat_m)
        fill_rect(img, 11, y_off - 3, 20, y_off - 1, hat_h)
    
    if hair_style == "long" or is_female:
        fill_rect(img, 9, y_off + 2, 10, y_off + 15, hair_m)
        fill_rect(img, 21, y_off + 2, 22, y_off + 15, hair_m)
        fill_rect(img, 11, y_off + 12, 20, y_off + 15, hair_m)
    
    # Contour tête
    for x in range(11, 21):
        px(img, x, y_off + 12, OUTLINE)
    for y in range(y_off, y_off + 12):
        px(img, 10, y, OUTLINE)
        px(img, 21, y, OUTLINE)
    for x in range(12, 20):
        px(img, x, y_off - 2, OUTLINE)
    
    # Cou / oreilles
    fill_rect(img, 13, y_off + 9, 18, y_off + 11, SKIN_MID)
    
    # --- Corps ---
    body_y = y_off + 13
    fill_rect(img, 10, body_y, 21, body_y + 10, shirt_m)
    fill_rect(img, 10, body_y + 8, 21, body_y + 10, shirt_s)
    for y in range(body_y, body_y + 11):
        px(img, 9, y, OUTLINE)
        px(img, 22, y, OUTLINE)
    # Bras
    fill_rect(img, 7, body_y + 2, 9, body_y + 8, shirt_m)
    fill_rect(img, 22, body_y + 2, 24, body_y + 8, shirt_m)
    fill_rect(img, 7, body_y + 9, 9, body_y + 10, SKIN_LIGHT)
    fill_rect(img, 22, body_y + 9, 24, body_y + 10, SKIN_LIGHT)
    
    # --- Bas ---
    legs_y = body_y + 11
    if has_skirt and skirt_col:
        skirt_m, skirt_h = skirt_col
        fill_rect(img, 9, legs_y, 22, legs_y + 4, skirt_m)
        fill_rect(img, 12, legs_y + 5, 14, legs_y + 8, SKIN_LIGHT)
        fill_rect(img, 17, legs_y + 5, 19, legs_y + 8, SKIN_LIGHT)
    else:
        fill_rect(img, 10, legs_y, 21, legs_y + 2, pants_m)
        x_left = 11 + foot_off
        x_right = 18 - foot_off
        fill_rect(img, x_left, legs_y + 3, x_left + 2, legs_y + 7, pants_m)
        fill_rect(img, x_right, legs_y + 3, x_right + 2, legs_y + 7, pants_m)
    
    # Chaussures
    shoe_y = legs_y + 8 if not (has_skirt and skirt_col) else legs_y + 9
    if has_skirt and skirt_col:
        fill_rect(img, 11 + foot_off, shoe_y, 14 + foot_off, shoe_y + 1, shoe)
        fill_rect(img, 16 - foot_off, shoe_y, 19 - foot_off, shoe_y + 1, shoe)
    else:
        fill_rect(img, 10 + foot_off, shoe_y, 13 + foot_off, shoe_y + 1, shoe)
        fill_rect(img, 17 - foot_off, shoe_y, 20 - foot_off, shoe_y + 1, shoe)


def _draw_side(img, bob, foot_off, flip,
              hair_m, hair_h, shirt_m, shirt_h, shirt_s,
              pants_m, pants_h, shoe, hair_style, has_hat, hat_col,
              is_female, has_skirt, skirt_col, accessory, acc_col):
    """Vue de profil (gauche). Si flip=True, on dessine à gauche puis on miroir."""
    if flip:
        temp = new_sprite()
        _draw_side(temp, bob, foot_off, False,
                  hair_m, hair_h, shirt_m, shirt_h, shirt_s,
                  pants_m, pants_h, shoe, hair_style, has_hat, hat_col,
                  is_female, has_skirt, skirt_col, accessory, acc_col)
        flipped = mirror_h(temp)
        img.paste(flipped, (0, 0))
        return
    
    y_off = 20 + bob
    
    # --- Tête profil ---
    fill_rect(img, 11, y_off, 19, y_off + 11, SKIN_LIGHT)
    fill_rect(img, 12, y_off - 1, 18, y_off - 1, SKIN_LIGHT)
    # Ombre côté
    fill_rect(img, 11, y_off + 6, 12, y_off + 11, SKIN_MID)
    
    # Cheveux 
    fill_rect(img, 14, y_off - 1, 20, y_off + 3, hair_m)
    fill_rect(img, 15, y_off - 1, 19, y_off, hair_h)
    if hair_style == "long" or is_female:
        fill_rect(img, 18, y_off + 3, 21, y_off + 15, hair_m)
        fill_rect(img, 19, y_off + 3, 20, y_off + 12, hair_h)
    else:
        fill_rect(img, 18, y_off + 3, 20, y_off + 6, hair_m)
    
    if has_hat and hat_col:
        hat_m, hat_h = hat_col
        fill_rect(img, 10, y_off - 3, 20, y_off + 2, hat_m)
        fill_rect(img, 11, y_off - 3, 19, y_off - 1, hat_h)
        # Visière 
        fill_rect(img, 7, y_off + 2, 13, y_off + 3, hat_m)
    
    # Contour tête
    for x in range(11, 20):
        px(img, x, y_off + 12, OUTLINE)
    for y in range(y_off, y_off + 12):
        px(img, 10, y, OUTLINE)
        px(img, 20, y, OUTLINE)
    
    # Œil (profil = 1 seul œil)
    px(img, 12, y_off + 5, EYE_BLACK)
    px(img, 13, y_off + 5, EYE_WHITE)
    
    # Nez / bouche
    px(img, 10, y_off + 6, SKIN_DARK)
    px(img, 11, y_off + 8, SKIN_DARK)
    
    # --- Corps ---
    body_y = y_off + 13
    fill_rect(img, 11, body_y, 20, body_y + 10, shirt_m)
    fill_rect(img, 12, body_y, 18, body_y + 2, shirt_h)
    fill_rect(img, 11, body_y + 8, 20, body_y + 10, shirt_s)
    for y in range(body_y, body_y + 11):
        px(img, 10, y, OUTLINE)
        px(img, 21, y, OUTLINE)
    # Bras (devant)
    fill_rect(img, 9, body_y + 3, 11, body_y + 8, shirt_m)
    fill_rect(img, 9, body_y + 9, 10, body_y + 10, SKIN_LIGHT)
    
    # --- Bas ---
    legs_y = body_y + 11
    if has_skirt and skirt_col:
        skirt_m, skirt_h = skirt_col
        fill_rect(img, 10, legs_y, 21, legs_y + 4, skirt_m)
        fill_rect(img, 13, legs_y + 5, 17, legs_y + 8, SKIN_LIGHT)
    else:
        fill_rect(img, 11, legs_y, 20, legs_y + 2, pants_m)
        # Jambes profil
        front_x = 12 + foot_off
        back_x = 16 - foot_off
        fill_rect(img, front_x, legs_y + 3, front_x + 2, legs_y + 7, pants_m)
        fill_rect(img, back_x, legs_y + 3, back_x + 2, legs_y + 7, pants_m)
    
    # Chaussures
    shoe_y = legs_y + 8 if not (has_skirt and skirt_col) else legs_y + 9
    if has_skirt and skirt_col:
        fill_rect(img, 12 + foot_off, shoe_y, 15 + foot_off, shoe_y + 1, shoe)
    else:
        fill_rect(img, 11 + foot_off, shoe_y, 14 + foot_off, shoe_y + 1, shoe)
        fill_rect(img, 15 - foot_off, shoe_y, 18 - foot_off, shoe_y + 1, shoe)


# ============================================================================
# SPRITES STATIQUES (panneau, objets)
# ============================================================================
def draw_sign_post(img):
    """Panneau en bois."""
    # Poteau
    fill_rect(img, 14, 40, 17, 58, WOOD_DARK)
    fill_rect(img, 15, 40, 16, 58, WOOD_MID)
    # Panneau
    draw_outline_rect(img, 6, 24, 25, 40, WOOD_LIGHT)
    fill_rect(img, 7, 25, 24, 39, WOOD_MID)
    fill_rect(img, 8, 26, 23, 28, WOOD_LIGHT)
    # Texte simulé (lignes)
    fill_rect(img, 9, 30, 22, 30, OUTLINE)
    fill_rect(img, 9, 33, 20, 33, OUTLINE)
    fill_rect(img, 9, 36, 18, 36, OUTLINE)

def draw_item_ball(img):
    """Poké Ball au sol."""
    # Ombre
    fill_rect(img, 10, 48, 21, 50, (80, 80, 80, 100))
    # Ball
    cx, cy = 16, 40
    # Moitié haute (rouge)
    for y in range(cy - 6, cy):
        for x in range(cx - 6, cx + 7):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if dist <= 6:
                if dist >= 5:
                    px(img, x, y, OUTLINE)
                else:
                    px(img, x, y, RED)
    # Moitié basse (blanche)
    for y in range(cy, cy + 7):
        for x in range(cx - 6, cx + 7):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if dist <= 6:
                if dist >= 5:
                    px(img, x, y, OUTLINE)
                else:
                    px(img, x, y, WHITE)
    # Ligne centrale
    fill_rect(img, cx - 6, cy, cx + 6, cy, OUTLINE)
    # Bouton central
    px(img, cx - 1, cy - 1, OUTLINE)
    px(img, cx, cy - 1, OUTLINE)
    px(img, cx + 1, cy - 1, OUTLINE)
    px(img, cx - 1, cy, WHITE)
    px(img, cx, cy, OUTLINE)
    px(img, cx + 1, cy, WHITE)
    px(img, cx - 1, cy + 1, OUTLINE)
    px(img, cx, cy + 1, OUTLINE)
    px(img, cx + 1, cy + 1, OUTLINE)

def draw_pc_terminal(img):
    """Écran PC (statique)."""
    # Socle
    fill_rect(img, 10, 48, 21, 54, GREY_D)
    fill_rect(img, 8, 54, 23, 56, GREY)
    # Écran
    draw_outline_rect(img, 8, 28, 23, 48, GREY)
    fill_rect(img, 10, 30, 21, 46, (32, 80, 32, 255))  # Écran vert
    # Texte PC
    fill_rect(img, 12, 33, 19, 33, (120, 220, 120, 255))
    fill_rect(img, 12, 36, 17, 36, (120, 220, 120, 255))
    fill_rect(img, 12, 39, 19, 39, (120, 220, 120, 255))

def draw_snorlax(img):
    """Ronflex / Snorlax endormi."""
    # Corps gros et rond (bleu-noir)
    body_col = (64, 72, 80, 255)
    belly_col = (216, 200, 168, 255)
    cx, cy = 16, 40
    # Corps
    for y in range(cy - 12, cy + 10):
        for x in range(cx - 11, cx + 12):
            dist_x = (x - cx) / 11.0
            dist_y = (y - cy) / 10.0
            if dist_x**2 + dist_y**2 <= 1.0:
                px(img, x, y, body_col)
    # Ventre (crème)
    for y in range(cy - 6, cy + 8):
        for x in range(cx - 6, cx + 7):
            dist_x = (x - cx) / 6.0
            dist_y = (y - cy + 1) / 7.0
            if dist_x**2 + dist_y**2 <= 1.0:
                px(img, x, y, belly_col)
    # Tête
    for y in range(cy - 16, cy - 10):
        for x in range(cx - 6, cx + 7):
            dist = ((x - cx)**2 + (y - (cy-13))**2) ** 0.5
            if dist <= 5:
                px(img, x, y, body_col)
    # Yeux fermés (Z Z Z)
    px(img, 13, cy - 14, WHITE)
    px(img, 14, cy - 14, WHITE)
    px(img, 17, cy - 14, WHITE)
    px(img, 18, cy - 14, WHITE)
    # Petits Z de sommeil
    px(img, 22, cy - 18, WHITE)
    px(img, 23, cy - 19, WHITE)
    px(img, 24, cy - 18, WHITE)

def draw_legendary_pokemon(img):
    """Pokémon légendaire (silhouette mystérieuse)."""
    # Silhouette violette/sombre
    for y in range(24, 52):
        for x in range(8, 24):
            dx = (x - 16) / 8.0
            dy = (y - 38) / 14.0
            if dx**2 + dy**2 <= 1.0:
                if dx**2 + dy**2 > 0.8:
                    px(img, x, y, PURPLE)
                else:
                    px(img, x, y, PURPLE_L)
    # Yeux brillants
    px(img, 12, 34, (255, 255, 80, 255))
    px(img, 13, 34, (255, 255, 80, 255))
    px(img, 18, 34, (255, 255, 80, 255))
    px(img, 19, 34, (255, 255, 80, 255))
    # Aura
    for i in range(4):
        px(img, 16, 22 - i, (168, 120, 200, 128))


# ============================================================================
# DÉFINITIONS DES PERSONNAGES
# ============================================================================
CHARACTER_DEFS = {
    "pnj_homme": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (BLUE, BLUE_L, BLUE_D),
        "pants_colors": (BROWN, BROWN_L),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "pnj_femme": {
        "hair_colors": (HAIR_RED, HAIR_RED_L),
        "shirt_colors": (RED, RED_L, (160, 32, 32, 255)),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BROWN,
        "is_female": True,
        "has_skirt": True,
        "skirt_colors": (RED, RED_L),
        "hair_style": "long",
    },
    "pnj_fille": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (PINK, PINK_L, (200, 112, 144, 255)),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BROWN,
        "is_female": True,
        "has_skirt": True,
        "skirt_colors": (ORANGE, YELLOW),
        "hair_style": "long",
    },
    "pnj_garcon": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (GREEN, GREEN_L, (40, 120, 56, 255)),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "pnj_gamin": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLACK,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (BLUE, BLUE_L),
    },
    "pnj_gamine": {
        "hair_colors": (HAIR_RED, HAIR_RED_L),
        "shirt_colors": (YELLOW, YELLOW_L, ORANGE),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": RED,
        "is_female": True,
        "has_skirt": True,
        "skirt_colors": (YELLOW, YELLOW_L),
        "hair_style": "long",
    },
    "pnj_vendeur": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (BLACK, GREY_D),
        "shoe_color": BLACK,
        "hair_style": "short",
        "accessory": "apron",
        "accessory_colors": (GREEN,),
    },
    "pnj_infirmiere": {
        "hair_colors": (HAIR_PINK, HAIR_PINK_L),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (WHITE, WHITE_S),
        "shoe_color": WHITE,
        "is_female": True,
        "hair_style": "long",
        "has_hat": True,
        "hat_colors": (WHITE, PINK_L),
    },
    "pnj_scientifique": {
        "hair_colors": (HAIR_GREY, HAIR_GREY_L),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (GREY, GREY_L),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "pnj_vieux": {
        "hair_colors": (HAIR_GREY, HAIR_GREY_L),
        "shirt_colors": (BROWN, BROWN_L, BROWN_D),
        "pants_colors": (GREY, GREY_L),
        "shoe_color": BROWN_D,
        "hair_style": "short",
    },
    "pnj_vieil_homme": {
        "hair_colors": (HAIR_GREY, HAIR_GREY_L),
        "shirt_colors": (BROWN, BROWN_L, BROWN_D),
        "pants_colors": (GREY, GREY_L),
        "shoe_color": BROWN_D,
        "hair_style": "short",
    },
    "pnj_marin": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLACK,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (WHITE, BLUE_L),
    },
    "pnj_rocket": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (BLACK, GREY_D, (16, 16, 24, 255)),
        "pants_colors": (GREY, GREY_L),
        "shoe_color": BLACK,
        "hair_style": "short",
        "accessory": "letter_R",
        "accessory_colors": (RED,),
    },
    "pnj_rocket_homme": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (BLACK, GREY_D, (16, 16, 24, 255)),
        "pants_colors": (GREY, GREY_L),
        "shoe_color": BLACK,
        "hair_style": "short",
        "accessory": "letter_R",
        "accessory_colors": (RED,),
    },
    "pnj_rocket_femme": {
        "hair_colors": (HAIR_RED, HAIR_RED_L),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (BLACK, GREY_D),
        "shoe_color": BLACK,
        "is_female": True,
        "hair_style": "long",
        "accessory": "letter_R",
        "accessory_colors": (RED,),
    },
    "pnj_motard": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (BLACK, GREY_D, (16, 16, 24, 255)),
        "pants_colors": (BLACK, GREY_D),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "pnj_karateka": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (WHITE, WHITE_S),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "pnj_nageur": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (BLUE, BLUE_L, BLUE_D),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLUE,
        "hair_style": "short",
    },
    "pnj_nageuse": {
        "hair_colors": (HAIR_BLUE, (96, 128, 200, 255)),
        "shirt_colors": (RED, RED_L, (160, 32, 32, 255)),
        "pants_colors": (RED, RED_L),
        "shoe_color": RED,
        "is_female": True,
        "hair_style": "long",
    },
    "pnj_pecheur": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (TEAL, (96, 200, 200, 255), (48, 128, 128, 255)),
        "pants_colors": (BROWN, BROWN_L),
        "shoe_color": BROWN_D,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (YELLOW, YELLOW_L),
    },
    "pnj_medium": {
        "hair_colors": (PURPLE, PURPLE_L),
        "shirt_colors": (PURPLE, PURPLE_L, (104, 56, 136, 255)),
        "pants_colors": (PURPLE, PURPLE_L),
        "shoe_color": BLACK,
        "is_female": True,
        "hair_style": "long",
    },
    "pnj_dresseur": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (RED, RED_L, (160, 32, 32, 255)),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLACK,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (RED, RED_L),
    },
    "pnj_dresseur_m": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (RED, RED_L, (160, 32, 32, 255)),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLACK,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (RED, RED_L),
    },
    "pnj_champion": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (ORANGE, YELLOW, BROWN),
        "pants_colors": (GREY, GREY_L),
        "shoe_color": BROWN,
        "hair_style": "short",
    },
    "pnj_champion_bob": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (GREEN, GREEN_L, (40, 120, 56, 255)),
        "pants_colors": (BROWN, BROWN_L),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "pnj_champion_ondine": {
        "hair_colors": (ORANGE, YELLOW),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLUE,
        "is_female": True,
        "hair_style": "long",
    },
    "champion_erika": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (YELLOW, YELLOW_L, ORANGE),
        "pants_colors": (GREEN, GREEN_L),
        "shoe_color": BROWN,
        "is_female": True,
        "hair_style": "long",
    },
    "pnj_giovanni": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (ORANGE, YELLOW, BROWN),
        "pants_colors": (BLACK, GREY_D),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "pnj_jongleur": {
        "hair_colors": (HAIR_RED, HAIR_RED_L),
        "shirt_colors": (YELLOW, YELLOW_L, ORANGE),
        "pants_colors": (RED, RED_L),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "pnj_garde": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (BLUE, BLUE_L, BLUE_D),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLACK,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (BLUE, BLUE_L),
    },
    "pnj_capitaine": {
        "hair_colors": (HAIR_GREY, HAIR_GREY_L),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLACK,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (WHITE, GREY_L),
    },
    "pnj_fillette": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (PINK, PINK_L, (200, 112, 144, 255)),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": RED,
        "is_female": True,
        "has_skirt": True,
        "skirt_colors": (PINK, PINK_L),
        "hair_style": "long",
    },
    "pnj_montagnard": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (BROWN, BROWN_L, BROWN_D),
        "pants_colors": (GREEN, GREEN_L),
        "shoe_color": BROWN_D,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (BROWN, BROWN_L),
    },
    "pnj_randonneur": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (GREEN, GREEN_L, (40, 120, 56, 255)),
        "pants_colors": (BROWN, BROWN_L),
        "shoe_color": BROWN_D,
        "hair_style": "short",
    },
    "pnj_randonneuse": {
        "hair_colors": (HAIR_RED, HAIR_RED_L),
        "shirt_colors": (GREEN, GREEN_L, (40, 120, 56, 255)),
        "pants_colors": (BROWN, BROWN_L),
        "shoe_color": BROWN_D,
        "is_female": True,
        "hair_style": "long",
    },
    "pnj_campeur": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (ORANGE, YELLOW, BROWN),
        "pants_colors": (GREEN, GREEN_L),
        "shoe_color": BROWN,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (ORANGE, YELLOW),
    },
    "pnj_insectomane": {
        "hair_colors": (HAIR_GREEN, (96, 176, 104, 255)),
        "shirt_colors": (GREEN, GREEN_L, (40, 120, 56, 255)),
        "pants_colors": (BROWN, BROWN_L),
        "shoe_color": BROWN_D,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (GREEN, GREEN_L),
    },
    "pnj_canon": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (GREY, GREY_L, GREY_D),
        "pants_colors": (BROWN, BROWN_L),
        "shoe_color": BROWN_D,
        "hair_style": "short",
    },
    # Dresseurs alt
    "dresseur": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (RED, RED_L, (160, 32, 32, 255)),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "dresseur_f": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (RED, RED_L, (160, 32, 32, 255)),
        "pants_colors": (BLUE, BLUE_L),
        "shoe_color": RED,
        "is_female": True,
        "has_skirt": True,
        "skirt_colors": (RED, RED_L),
        "hair_style": "long",
    },
    "dresseur_m": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (BLUE, BLUE_L, BLUE_D),
        "pants_colors": (GREY, GREY_L),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "dresseur_randonneur": {
        "hair_colors": (HAIR_BROWN, HAIR_BROWN_L),
        "shirt_colors": (BROWN, BROWN_L, BROWN_D),
        "pants_colors": (GREEN, GREEN_L),
        "shoe_color": BROWN_D,
        "hair_style": "short",
        "has_hat": True,
        "hat_colors": (BROWN, BROWN_L),
    },
    "champion": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (PURPLE, PURPLE_L, (104, 56, 136, 255)),
        "pants_colors": (GREY, GREY_L),
        "shoe_color": BLACK,
        "hair_style": "short",
    },
    "infirmiere": {
        "hair_colors": (HAIR_PINK, HAIR_PINK_L),
        "shirt_colors": (WHITE, WHITE_S, GREY_L),
        "pants_colors": (WHITE, WHITE_S),
        "shoe_color": WHITE,
        "is_female": True,
        "hair_style": "long",
        "has_hat": True,
        "hat_colors": (WHITE, PINK_L),
    },
    "rocket_m": {
        "hair_colors": (HAIR_BLACK, HAIR_DARK),
        "shirt_colors": (BLACK, GREY_D, (16, 16, 24, 255)),
        "pants_colors": (GREY, GREY_L),
        "shoe_color": BLACK,
        "hair_style": "short",
        "accessory": "letter_R",
        "accessory_colors": (RED,),
    },
}

# Sprites statiques (un seul fichier bas_0)
STATIC_SPRITES = {
    "panneau": draw_sign_post,
    "pnj_panneau": draw_sign_post,
    "pnj_objet": draw_item_ball,
    "item_sol": draw_item_ball,
    "pnj_pc": draw_pc_terminal,
    "pc": draw_pc_terminal,
    "pnj_ronflex": draw_snorlax,
    "pokemon_legendaire": draw_legendary_pokemon,
    "pnj_legendaire": draw_legendary_pokemon,
}

DIRECTIONS = ["bas", "haut", "gauche", "droite"]
FRAMES = [0, 1, 2]

def generate_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total_files = 0
    
    # Personnages animés
    for name, params in CHARACTER_DEFS.items():
        for direction in DIRECTIONS:
            for frame in FRAMES:
                img = new_sprite()
                draw_generic_character(
                    img, direction, frame,
                    hair_colors=params["hair_colors"],
                    shirt_colors=params["shirt_colors"],
                    pants_colors=params["pants_colors"],
                    shoe_color=params["shoe_color"],
                    hair_style=params.get("hair_style", "short"),
                    has_hat=params.get("has_hat", False),
                    hat_colors=params.get("hat_colors"),
                    is_female=params.get("is_female", False),
                    has_skirt=params.get("has_skirt", False),
                    skirt_colors=params.get("skirt_colors"),
                    accessory=params.get("accessory"),
                    accessory_colors=params.get("accessory_colors"),
                )
                filename = f"{name}_{direction}_{frame}.png"
                filepath = os.path.join(OUTPUT_DIR, filename)
                img.save(filepath, "PNG")
                total_files += 1
        print(f"  ✓ {name} (12 sprites)")
    
    # Sprites statiques — créer aussi les 12 variantes (toutes identiques au bas_0)
    # pour éviter les erreurs quand le code essaie de charger d'autres frames
    for name, draw_func in STATIC_SPRITES.items():
        img = new_sprite()
        draw_func(img)
        for direction in DIRECTIONS:
            for frame in FRAMES:
                filename = f"{name}_{direction}_{frame}.png"
                filepath = os.path.join(OUTPUT_DIR, filename)
                img.save(filepath, "PNG")
                total_files += 1
        print(f"  ✓ {name} (statique, 12 copies)")
    
    print(f"\nTotal: {total_files} fichiers générés dans {OUTPUT_DIR}/")

if __name__ == "__main__":
    generate_all()
