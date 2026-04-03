#!/usr/bin/env python3
"""
Générateur de tileset HD inspiré Pokémon Rouge Feu / Vert Feuille
Crée un tileset 16×16 grille (256 tiles) à 32×32px = 512×512px total
Palette de couleurs fidèle au style GBA RFVF
"""

from PIL import Image, ImageDraw
import os, random, json

# --- Configuration ---
TILE_SIZE = 32
COLS = 16
ROWS = 16
SHEET_W = COLS * TILE_SIZE  # 512
SHEET_H = ROWS * TILE_SIZE  # 512

# --- Palette RFVF (couleurs GBA authentiques) ---
PAL = {
    # Herbe / Nature
    "grass_light":    (120, 208, 80),    # Herbe claire RFVF
    "grass_mid":      (96, 184, 64),     # Herbe moyenne
    "grass_dark":     (72, 152, 48),     # Herbe foncée
    "grass_shadow":   (56, 128, 40),     # Ombre herbe
    "tall_grass":     (64, 168, 56),     # Hautes herbes
    "tall_grass_tip": (88, 200, 72),     # Pointes hautes herbes
    "flower_red":     (232, 72, 56),     # Fleurs rouges
    "flower_yellow":  (248, 216, 64),    # Fleurs jaunes
    "flower_white":   (248, 248, 240),   # Fleurs blanches
    
    # Chemin / Sol
    "path_light":     (216, 184, 136),   # Chemin clair
    "path_mid":       (192, 160, 112),   # Chemin moyen
    "path_dark":      (168, 136, 96),    # Chemin foncé
    "path_edge":      (144, 120, 80),    # Bord de chemin
    "dirt":           (184, 152, 104),   # Terre
    
    # Eau
    "water_light":    (104, 144, 240),   # Eau claire
    "water_mid":      (80, 120, 216),    # Eau moyenne
    "water_dark":     (56, 96, 192),     # Eau foncée
    "water_foam":     (168, 200, 248),   # Écume
    "water_shore":    (152, 184, 232),   # Rivage
    "sand":           (232, 216, 168),   # Sable plage
    "sand_wet":       (200, 184, 144),   # Sable mouillé
    
    # Arbres (style RFVF)
    "tree_canopy":    (48, 120, 48),     # Feuillage dense
    "tree_canopy_l":  (64, 144, 56),     # Feuillage clair
    "tree_canopy_h":  (80, 160, 72),     # Highlight feuillage
    "tree_trunk":     (128, 88, 48),     # Tronc
    "tree_trunk_d":   (104, 72, 40),     # Tronc foncé
    
    # Maisons (style RFVF - toits rouges/bruns)
    "roof_red":       (200, 72, 56),     # Toit rouge
    "roof_red_l":     (224, 96, 72),     # Toit rouge clair
    "roof_red_d":     (168, 56, 40),     # Toit rouge foncé
    "roof_blue":      (80, 120, 192),    # Toit bleu (labo)
    "roof_blue_l":    (104, 144, 216),   # Toit bleu clair
    "roof_blue_d":    (56, 96, 160),     # Toit bleu foncé
    "wall_cream":     (240, 224, 192),   # Mur crème
    "wall_cream_d":   (216, 200, 168),   # Mur crème ombré
    "wall_stone":     (200, 192, 176),   # Mur pierre
    "door_brown":     (144, 96, 56),     # Porte bois
    "door_brown_d":   (120, 80, 40),     # Porte bois foncé
    "window_glass":   (168, 216, 240),   # Vitre
    "window_frame":   (192, 176, 152),   # Cadre fenêtre
    "step_stone":     (192, 184, 168),   # Marche/seuil
    
    # Centre Pokémon (toit rouge vif + croix)
    "pkcenter_roof":  (232, 56, 48),     # Toit centre pkmn
    "pkcenter_roof_l":(248, 88, 72),     # Clair
    "pkcenter_wall":  (248, 240, 224),   # Mur blanc Centre
    "pk_cross":       (248, 248, 248),   # Croix blanche
    
    # Boutique (toit bleu)
    "mart_roof":      (72, 112, 200),    # Toit boutique
    "mart_roof_l":    (96, 136, 224),    # Clair
    "mart_wall":      (232, 232, 240),   # Mur boutique
    
    # Clôtures / Panneaux
    "fence_wood":     (176, 136, 88),    # Clôture bois
    "fence_wood_d":   (144, 112, 72),    # Clôture bois foncé
    "sign_wood":      (160, 120, 72),    # Panneau bois
    "sign_face":      (232, 224, 200),   # Face panneau
    
    # Rebords / Ledges
    "ledge_top":      (88, 168, 64),     # Ledge (haut)
    "ledge_face":     (120, 96, 64),     # Face ledge
    "ledge_grass":    (80, 152, 56),     # Herbe sur ledge
    
    # Intérieur
    "floor_wood":     (216, 184, 144),   # Sol bois
    "floor_wood_d":   (192, 160, 120),   # Sol bois foncé
    "floor_tile":     (224, 224, 232),   # Carrelage
    "floor_tile_d":   (200, 200, 208),   # Carrelage ombré
    "int_wall":       (240, 232, 216),   # Mur intérieur
    "int_wall_d":     (216, 208, 192),   # Mur int ombré
    "counter_top":    (184, 152, 112),   # Comptoir haut
    "counter_front":  (160, 128, 88),    # Comptoir face
    "shelf":          (168, 136, 96),    # Étagère
    "shelf_d":        (144, 112, 72),    # Étagère foncée
    "machine_body":   (200, 208, 224),   # Machine soin
    "machine_screen": (120, 224, 120),   # Écran machine
    "carpet_red":     (200, 64, 56),     # Tapis rouge
    "carpet_red_d":   (176, 48, 40),     # Tapis foncé
    
    # Grotte
    "rock":           (152, 136, 120),   # Rocher
    "rock_d":         (128, 112, 96),    # Rocher foncé
    "rock_l":         (176, 160, 144),   # Rocher clair
    
    # Noir / Vide
    "black":          (16, 16, 24),
    "void":           (24, 24, 32),
}

def c(name):
    """Raccourci couleur"""
    return PAL[name]

# ============================================================
# DESSIN DES TILES
# ============================================================

def draw_grass_plain(draw, x0, y0):
    """Tile 0: Herbe plain RFVF — base verte avec micro-variations"""
    S = TILE_SIZE
    # Base
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Petites variations de texture (style GBA)
    random.seed(0)  # Reproductible
    for _ in range(12):
        px = x0 + random.randint(0, S-2)
        py = y0 + random.randint(0, S-2)
        col = c("grass_light") if random.random() > 0.5 else c("grass_dark")
        draw.rectangle([px, py, px+1, py+1], fill=col)

def draw_grass_variant(draw, x0, y0):
    """Tile 1: Herbe variante avec plus de détails"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    random.seed(1)
    for _ in range(20):
        px = x0 + random.randint(0, S-3)
        py = y0 + random.randint(0, S-3)
        col = c("grass_light") if random.random() > 0.4 else c("grass_shadow")
        draw.rectangle([px, py, px+1, py+1], fill=col)

def draw_grass_flowers(draw, x0, y0):
    """Tile 2: Herbe avec fleurs (style RFVF Bourg Palette)"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Petites fleurs
    positions = [(6, 6), (22, 10), (12, 22), (26, 26), (4, 18)]
    colors = [c("flower_red"), c("flower_yellow"), c("flower_white"), c("flower_red"), c("flower_yellow")]
    for (fx, fy), col in zip(positions, colors):
        draw.rectangle([x0+fx, y0+fy, x0+fx+1, y0+fy+1], fill=col)
        draw.point((x0+fx+1, y0+fy-1), fill=c("grass_light"))

def draw_tall_grass(draw, x0, y0):
    """Tile 3: Hautes herbes (zones de rencontre)"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("tall_grass"))
    # Brins d'herbe qui dépassent
    for i in range(0, S, 4):
        h = random.randint(6, 14)
        bx = x0 + i + random.randint(0, 2)
        draw.line([(bx, y0+S-1), (bx, y0+S-1-h)], fill=c("tall_grass_tip"), width=1)
        draw.line([(bx+1, y0+S-1), (bx+1, y0+S-2-h)], fill=c("grass_dark"), width=1)
    # Texture de fond
    random.seed(3)
    for _ in range(15):
        px = x0 + random.randint(0, S-2)
        py = y0 + random.randint(0, S-2)
        draw.point((px, py), fill=c("grass_shadow"))

def draw_path_center(draw, x0, y0):
    """Tile 4: Chemin centre (plein)"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("path_mid"))
    # Texture gravier
    random.seed(4)
    for _ in range(18):
        px = x0 + random.randint(1, S-3)
        py = y0 + random.randint(1, S-3)
        col = c("path_light") if random.random() > 0.5 else c("path_dark")
        draw.point((px, py), fill=col)

def draw_path_edge_top(draw, x0, y0):
    """Tile 5: Chemin bord haut (herbe en haut, chemin en bas)"""
    S = TILE_SIZE
    # Herbe en haut
    draw.rectangle([x0, y0, x0+S-1, y0+7], fill=c("grass_mid"))
    # Transition
    draw.rectangle([x0, y0+8, x0+S-1, y0+10], fill=c("path_edge"))
    # Chemin en bas
    draw.rectangle([x0, y0+11, x0+S-1, y0+S-1], fill=c("path_mid"))
    # Douceur de transition
    for i in range(0, S, 3):
        draw.point((x0+i, y0+8), fill=c("grass_dark"))
        draw.point((x0+i+1, y0+9), fill=c("path_dark"))

def draw_path_edge_bottom(draw, x0, y0):
    """Tile 6: Chemin bord bas"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+20], fill=c("path_mid"))
    draw.rectangle([x0, y0+21, x0+S-1, y0+23], fill=c("path_edge"))
    draw.rectangle([x0, y0+24, x0+S-1, y0+S-1], fill=c("grass_mid"))
    for i in range(0, S, 3):
        draw.point((x0+i, y0+22), fill=c("path_dark"))
        draw.point((x0+i+1, y0+24), fill=c("grass_dark"))

def draw_path_edge_left(draw, x0, y0):
    """Tile 7: Chemin bord gauche"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+7, y0+S-1], fill=c("grass_mid"))
    draw.rectangle([x0+8, y0, x0+10, y0+S-1], fill=c("path_edge"))
    draw.rectangle([x0+11, y0, x0+S-1, y0+S-1], fill=c("path_mid"))

def draw_path_edge_right(draw, x0, y0):
    """Tile 8: Chemin bord droit"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+20, y0+S-1], fill=c("path_mid"))
    draw.rectangle([x0+21, y0, x0+23, y0+S-1], fill=c("path_edge"))
    draw.rectangle([x0+24, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))

def draw_path_corner(draw, x0, y0, corner="tl"):
    """Tile 9-12: Coins de chemin"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    if corner == "tl":
        draw.rectangle([x0+11, y0+11, x0+S-1, y0+S-1], fill=c("path_mid"))
        draw.rectangle([x0+8, y0+8, x0+10, y0+S-1], fill=c("path_edge"))
        draw.rectangle([x0+8, y0+8, x0+S-1, y0+10], fill=c("path_edge"))
    elif corner == "tr":
        draw.rectangle([x0, y0+11, x0+20, y0+S-1], fill=c("path_mid"))
        draw.rectangle([x0+21, y0+8, x0+23, y0+S-1], fill=c("path_edge"))
        draw.rectangle([x0, y0+8, x0+23, y0+10], fill=c("path_edge"))
    elif corner == "bl":
        draw.rectangle([x0+11, y0, x0+S-1, y0+20], fill=c("path_mid"))
        draw.rectangle([x0+8, y0, x0+10, y0+23], fill=c("path_edge"))
        draw.rectangle([x0+8, y0+21, x0+S-1, y0+23], fill=c("path_edge"))
    elif corner == "br":
        draw.rectangle([x0, y0, x0+20, y0+20], fill=c("path_mid"))
        draw.rectangle([x0+21, y0, x0+23, y0+23], fill=c("path_edge"))
        draw.rectangle([x0, y0+21, x0+23, y0+23], fill=c("path_edge"))

def draw_path_inner_corner(draw, x0, y0, corner="tl"):
    """Tile 13-14: Coins intérieurs de chemin (inverse des coins normaux)"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("path_mid"))
    if corner == "tl":
        draw.rectangle([x0, y0, x0+10, y0+10], fill=c("grass_mid"))
        draw.rectangle([x0+8, y0+8, x0+12, y0+12], fill=c("path_edge"))
    elif corner == "tr":
        draw.rectangle([x0+21, y0, x0+S-1, y0+10], fill=c("grass_mid"))
        draw.rectangle([x0+19, y0+8, x0+23, y0+12], fill=c("path_edge"))
    elif corner == "bl":
        draw.rectangle([x0, y0+21, x0+10, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+8, y0+19, x0+12, y0+23], fill=c("path_edge"))
    elif corner == "br":
        draw.rectangle([x0+21, y0+21, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+19, y0+19, x0+23, y0+23], fill=c("path_edge"))

def draw_sand(draw, x0, y0):
    """Tile 15: Sable"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("sand"))
    random.seed(15)
    for _ in range(10):
        px = x0 + random.randint(0, S-2)
        py = y0 + random.randint(0, S-2)
        draw.point((px, py), fill=c("sand_wet"))

# --- Row 1: Eau et rivages ---
def draw_water(draw, x0, y0):
    """Tile 16: Eau profonde avec vagues"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("water_mid"))
    # Vagues
    for row in range(0, S, 8):
        for col in range(0, S, 6):
            ox = (row // 8 * 3) % 6
            draw.line([(x0+col+ox, y0+row+2), (x0+col+ox+3, y0+row)], fill=c("water_light"), width=1)
            draw.line([(x0+col+ox, y0+row+4), (x0+col+ox+3, y0+row+3)], fill=c("water_dark"), width=1)

def draw_water_shore(draw, x0, y0, side="top"):
    """Tiles 17-20: Rivage eau (transition herbe-eau)"""
    S = TILE_SIZE
    if side == "top":
        draw.rectangle([x0, y0, x0+S-1, y0+11], fill=c("grass_mid"))
        draw.rectangle([x0, y0+12, x0+S-1, y0+14], fill=c("sand"))
        draw.rectangle([x0, y0+15, x0+S-1, y0+S-1], fill=c("water_mid"))
        for i in range(0, S, 5):
            draw.point((x0+i, y0+15), fill=c("water_foam"))
    elif side == "bottom":
        draw.rectangle([x0, y0, x0+S-1, y0+16], fill=c("water_mid"))
        draw.rectangle([x0, y0+17, x0+S-1, y0+19], fill=c("sand"))
        draw.rectangle([x0, y0+20, x0+S-1, y0+S-1], fill=c("grass_mid"))
        for i in range(0, S, 5):
            draw.point((x0+i+2, y0+16), fill=c("water_foam"))
    elif side == "left":
        draw.rectangle([x0, y0, x0+11, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+12, y0, x0+14, y0+S-1], fill=c("sand"))
        draw.rectangle([x0+15, y0, x0+S-1, y0+S-1], fill=c("water_mid"))
    elif side == "right":
        draw.rectangle([x0, y0, x0+16, y0+S-1], fill=c("water_mid"))
        draw.rectangle([x0+17, y0, x0+19, y0+S-1], fill=c("sand"))
        draw.rectangle([x0+20, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))

def draw_water_corner(draw, x0, y0, corner="tl"):
    """Tiles 21-24: Coins eau-herbe"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("water_mid"))
    if corner == "tl":
        draw.rectangle([x0, y0, x0+11, y0+11], fill=c("grass_mid"))
        draw.rectangle([x0+10, y0+10, x0+14, y0+14], fill=c("sand"))
    elif corner == "tr":
        draw.rectangle([x0+20, y0, x0+S-1, y0+11], fill=c("grass_mid"))
        draw.rectangle([x0+17, y0+10, x0+21, y0+14], fill=c("sand"))
    elif corner == "bl":
        draw.rectangle([x0, y0+20, x0+11, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+10, y0+17, x0+14, y0+21], fill=c("sand"))
    elif corner == "br":
        draw.rectangle([x0+20, y0+20, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+17, y0+17, x0+21, y0+21], fill=c("sand"))

def draw_water_inner_corner(draw, x0, y0, corner="tl"):
    """Tiles 25-28: Coins intérieurs eau (herbe qui dépasse dans l'eau)"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    if corner == "tl":
        draw.rectangle([x0+15, y0+15, x0+S-1, y0+S-1], fill=c("water_mid"))
        draw.rectangle([x0+13, y0+13, x0+16, y0+16], fill=c("sand"))
    elif corner == "tr":
        draw.rectangle([x0, y0+15, x0+16, y0+S-1], fill=c("water_mid"))
        draw.rectangle([x0+15, y0+13, x0+18, y0+16], fill=c("sand"))
    elif corner == "bl":
        draw.rectangle([x0+15, y0, x0+S-1, y0+16], fill=c("water_mid"))
        draw.rectangle([x0+13, y0+15, x0+16, y0+18], fill=c("sand"))
    elif corner == "br":
        draw.rectangle([x0, y0, x0+16, y0+16], fill=c("water_mid"))
        draw.rectangle([x0+15, y0+15, x0+18, y0+18], fill=c("sand"))

# --- Row 2: Arbres RFVF (2×2 tiles pour un arbre) ---
def draw_tree_top_left(draw, x0, y0):
    """Tile 32: Arbre haut-gauche — feuillage dense"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Canopée arrondie
    draw.ellipse([x0+2, y0+4, x0+S+8, y0+S+8], fill=c("tree_canopy"))
    draw.ellipse([x0+4, y0+6, x0+S+6, y0+S+4], fill=c("tree_canopy_l"))
    # Highlights
    draw.ellipse([x0+8, y0+8, x0+22, y0+18], fill=c("tree_canopy_h"))
    # Ombres
    draw.rectangle([x0, y0+S-4, x0+S-1, y0+S-1], fill=c("tree_canopy"))
    # Détails feuilles
    random.seed(32)
    for _ in range(8):
        px = x0 + random.randint(4, S-4)
        py = y0 + random.randint(6, S-4)
        draw.point((px, py), fill=c("tree_canopy_l"))

def draw_tree_top_right(draw, x0, y0):
    """Tile 33: Arbre haut-droit"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    draw.ellipse([x0-8, y0+4, x0+S-2, y0+S+8], fill=c("tree_canopy"))
    draw.ellipse([x0-6, y0+6, x0+S-4, y0+S+4], fill=c("tree_canopy_l"))
    draw.ellipse([x0+10, y0+8, x0+24, y0+18], fill=c("tree_canopy_h"))
    draw.rectangle([x0, y0+S-4, x0+S-1, y0+S-1], fill=c("tree_canopy"))
    random.seed(33)
    for _ in range(8):
        px = x0 + random.randint(2, S-6)
        py = y0 + random.randint(6, S-4)
        draw.point((px, py), fill=c("tree_canopy_l"))

def draw_tree_bottom_left(draw, x0, y0):
    """Tile 34: Arbre bas-gauche — tronc + feuillage bas"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Feuillage continue
    draw.rectangle([x0, y0, x0+S-1, y0+16], fill=c("tree_canopy"))
    draw.rectangle([x0+2, y0, x0+S-1, y0+12], fill=c("tree_canopy_l"))
    # Tronc
    draw.rectangle([x0+20, y0+10, x0+28, y0+S-1], fill=c("tree_trunk"))
    draw.rectangle([x0+20, y0+10, x0+23, y0+S-1], fill=c("tree_trunk_d"))
    # Ombre au sol
    draw.ellipse([x0+8, y0+S-6, x0+S-2, y0+S-1], fill=c("grass_shadow"))

def draw_tree_bottom_right(draw, x0, y0):
    """Tile 35: Arbre bas-droit"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    draw.rectangle([x0, y0, x0+S-1, y0+16], fill=c("tree_canopy"))
    draw.rectangle([x0, y0, x0+S-3, y0+12], fill=c("tree_canopy_l"))
    # Tronc
    draw.rectangle([x0+4, y0+10, x0+12, y0+S-1], fill=c("tree_trunk"))
    draw.rectangle([x0+9, y0+10, x0+12, y0+S-1], fill=c("tree_trunk_d"))
    # Ombre
    draw.ellipse([x0+2, y0+S-6, x0+24, y0+S-1], fill=c("grass_shadow"))

def draw_bush(draw, x0, y0):
    """Tile 36: Buisson (coupable avec Coupe)"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Buisson rond
    draw.ellipse([x0+4, y0+6, x0+28, y0+28], fill=c("tree_canopy"))
    draw.ellipse([x0+6, y0+8, x0+26, y0+24], fill=c("tree_canopy_l"))
    draw.ellipse([x0+10, y0+10, x0+20, y0+18], fill=c("tree_canopy_h"))

def draw_small_tree(draw, x0, y0):
    """Tile 37: Petit arbre décoratif"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Couronne
    draw.ellipse([x0+6, y0+2, x0+26, y0+20], fill=c("tree_canopy"))
    draw.ellipse([x0+8, y0+4, x0+24, y0+16], fill=c("tree_canopy_l"))
    # Tronc
    draw.rectangle([x0+13, y0+18, x0+19, y0+S-1], fill=c("tree_trunk"))
    draw.rectangle([x0+13, y0+18, x0+15, y0+S-1], fill=c("tree_trunk_d"))

def draw_rock(draw, x0, y0):
    """Tile 38: Rocher"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Pierre
    pts = [(x0+8, y0+S-4), (x0+4, y0+16), (x0+6, y0+8), (x0+14, y0+4),
           (x0+24, y0+4), (x0+28, y0+10), (x0+28, y0+20), (x0+24, y0+S-4)]
    draw.polygon(pts, fill=c("rock"), outline=c("rock_d"))
    # Highlight
    draw.line([(x0+10, y0+8), (x0+22, y0+8)], fill=c("rock_l"), width=2)

def draw_fence_h(draw, x0, y0):
    """Tile 39: Clôture horizontale"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Poteaux
    draw.rectangle([x0, y0+8, x0+4, y0+S-4], fill=c("fence_wood_d"))
    draw.rectangle([x0+S-5, y0+8, x0+S-1, y0+S-4], fill=c("fence_wood_d"))
    # Barres horizontales
    draw.rectangle([x0, y0+12, x0+S-1, y0+15], fill=c("fence_wood"))
    draw.rectangle([x0, y0+20, x0+S-1, y0+23], fill=c("fence_wood"))
    draw.line([(x0, y0+12), (x0+S-1, y0+12)], fill=c("fence_wood_d"))

def draw_fence_v(draw, x0, y0):
    """Tile 40: Clôture verticale"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Poteau central
    draw.rectangle([x0+12, y0, x0+19, y0+S-1], fill=c("fence_wood"))
    draw.rectangle([x0+12, y0, x0+14, y0+S-1], fill=c("fence_wood_d"))

def draw_sign(draw, x0, y0):
    """Tile 41: Panneau indicateur"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Poteau
    draw.rectangle([x0+14, y0+18, x0+18, y0+S-1], fill=c("sign_wood"))
    # Panneau
    draw.rectangle([x0+6, y0+6, x0+26, y0+19], fill=c("sign_wood"))
    draw.rectangle([x0+8, y0+8, x0+24, y0+17], fill=c("sign_face"))

def draw_mailbox(draw, x0, y0):
    """Tile 42: Boîte aux lettres"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    # Poteau
    draw.rectangle([x0+14, y0+16, x0+18, y0+S-1], fill=c("fence_wood_d"))
    # Boîte
    draw.rectangle([x0+10, y0+8, x0+22, y0+17], fill=c("roof_red"))
    draw.rectangle([x0+10, y0+8, x0+22, y0+10], fill=c("roof_red_l"))

def draw_ledge_top(draw, x0, y0):
    """Tile 43: Ledge (rebord sautable) — vue de dessus"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+12], fill=c("grass_mid"))
    draw.rectangle([x0, y0+13, x0+S-1, y0+17], fill=c("ledge_grass"))
    draw.rectangle([x0, y0+18, x0+S-1, y0+S-1], fill=c("ledge_face"))
    draw.line([(x0, y0+18), (x0+S-1, y0+18)], fill=c("grass_shadow"), width=1)
    # Détail herbe sur le bord
    for i in range(0, S, 5):
        draw.line([(x0+i, y0+16), (x0+i, y0+13)], fill=c("grass_dark"), width=1)

def draw_ledge_left(draw, x0, y0):
    """Tile 44: Ledge gauche (bout)"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    draw.rectangle([x0, y0+13, x0+8, y0+17], fill=c("ledge_grass"))
    draw.rectangle([x0, y0+18, x0+8, y0+S-1], fill=c("ledge_face"))
    # Arrondi
    draw.arc([x0-4, y0+13, x0+10, y0+S-1], 0, 90, fill=c("grass_shadow"))

def draw_ledge_right(draw, x0, y0):
    """Tile 45: Ledge droit (bout)"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    draw.rectangle([x0+23, y0+13, x0+S-1, y0+17], fill=c("ledge_grass"))
    draw.rectangle([x0+23, y0+18, x0+S-1, y0+S-1], fill=c("ledge_face"))

def draw_stump(draw, x0, y0):
    """Tile 46: Souche d'arbre coupé"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
    draw.ellipse([x0+8, y0+12, x0+24, y0+26], fill=c("tree_trunk"))
    draw.ellipse([x0+10, y0+10, x0+22, y0+18], fill=c("tree_trunk_d"))
    # Anneaux
    draw.ellipse([x0+13, y0+13, x0+19, y0+17], fill=(160, 120, 72))

def draw_empty_grass(draw, x0, y0):
    """Tile 47: Herbe vide (réserve)"""
    draw_grass_plain(draw, x0, y0)

# --- Row 3: Maisons toits rouges (style RFVF) ---
def draw_house_roof(draw, x0, y0, part="tl", color="red"):
    """Tiles 48-53: Pièces de toit de maison"""
    S = TILE_SIZE
    roof = c(f"roof_{color}")
    roof_l = c(f"roof_{color}_l")
    roof_d = c(f"roof_{color}_d")
    
    if part == "tl":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        # Toit avec pente
        draw.polygon([(x0, y0+S-1), (x0+S-1, y0+S-1), (x0+S-1, y0+4), (x0+12, y0+4)],
                     fill=roof)
        draw.rectangle([x0+12, y0+4, x0+S-1, y0+12], fill=roof_l)
        draw.line([(x0+12, y0+4), (x0, y0+S-1)], fill=roof_d, width=2)
    elif part == "tm":
        draw.rectangle([x0, y0, x0+S-1, y0+3], fill=c("grass_mid"))
        draw.rectangle([x0, y0+4, x0+S-1, y0+S-1], fill=roof)
        draw.rectangle([x0, y0+4, x0+S-1, y0+12], fill=roof_l)
        draw.line([(x0, y0+4), (x0+S-1, y0+4)], fill=roof_d)
        # Lignes de tuiles
        for i in range(y0+8, y0+S, 6):
            draw.line([(x0, i), (x0+S-1, i)], fill=roof_d, width=1)
    elif part == "tr":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.polygon([(x0, y0+S-1), (x0, y0+4), (x0+20, y0+4), (x0+S-1, y0+S-1)],
                     fill=roof)
        draw.rectangle([x0, y0+4, x0+20, y0+12], fill=roof_l)
        draw.line([(x0+20, y0+4), (x0+S-1, y0+S-1)], fill=roof_d, width=2)
    elif part == "bl":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=roof)
        draw.rectangle([x0, y0, x0+S-1, y0+6], fill=roof_l)
        draw.line([(x0, y0+S-1), (x0+S-1, y0+S-1)], fill=roof_d, width=2)
        # Avant-toit
        draw.rectangle([x0, y0+S-4, x0+S-1, y0+S-1], fill=roof_d)
    elif part == "bm":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=roof)
        draw.rectangle([x0, y0, x0+S-1, y0+6], fill=roof_l)
        for i in range(y0+2, y0+S-4, 6):
            draw.line([(x0, i), (x0+S-1, i)], fill=roof_d, width=1)
        draw.rectangle([x0, y0+S-4, x0+S-1, y0+S-1], fill=roof_d)
    elif part == "br":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=roof)
        draw.rectangle([x0, y0, x0+S-1, y0+6], fill=roof_l)
        draw.rectangle([x0, y0+S-4, x0+S-1, y0+S-1], fill=roof_d)

def draw_house_wall(draw, x0, y0, part="l"):
    """Tiles 54-58: Murs de maison"""
    S = TILE_SIZE
    if part == "l":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+4, y0, x0+S-1, y0+S-1], fill=c("wall_cream"))
        draw.line([(x0+4, y0), (x0+4, y0+S-1)], fill=c("wall_cream_d"), width=2)
    elif part == "m":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("wall_cream"))
        # Lignes de briques subtiles
        for i in range(y0+8, y0+S, 8):
            draw.line([(x0, i), (x0+S-1, i)], fill=c("wall_cream_d"), width=1)
    elif part == "r":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0, y0, x0+S-5, y0+S-1], fill=c("wall_cream"))
        draw.line([(x0+S-5, y0), (x0+S-5, y0+S-1)], fill=c("wall_cream_d"), width=2)
    elif part == "window":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("wall_cream"))
        for i in range(y0+8, y0+S, 8):
            draw.line([(x0, i), (x0+S-1, i)], fill=c("wall_cream_d"), width=1)
        # Fenêtre
        draw.rectangle([x0+8, y0+6, x0+24, y0+20], fill=c("window_frame"))
        draw.rectangle([x0+10, y0+8, x0+22, y0+18], fill=c("window_glass"))
        draw.line([(x0+16, y0+8), (x0+16, y0+18)], fill=c("window_frame"))
        draw.line([(x0+10, y0+13), (x0+22, y0+13)], fill=c("window_frame"))
    elif part == "door":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("wall_cream"))
        # Porte
        draw.rectangle([x0+8, y0+2, x0+24, y0+S-1], fill=c("door_brown"))
        draw.rectangle([x0+8, y0+2, x0+15, y0+S-1], fill=c("door_brown_d"))
        # Poignée
        draw.rectangle([x0+20, y0+14, x0+22, y0+16], fill=c("fence_wood"))
        # Marche
        draw.rectangle([x0+4, y0+S-4, x0+28, y0+S-1], fill=c("step_stone"))

# --- Row 4: Bâtiments spéciaux (labo Chen - toit bleu) ---
def draw_lab_roof(draw, x0, y0, part="tl"):
    draw_house_roof(draw, x0, y0, part, color="blue")

def draw_lab_wall(draw, x0, y0, part="l"):
    """Murs du labo - légèrement différents"""
    S = TILE_SIZE
    if part == "l":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+4, y0, x0+S-1, y0+S-1], fill=c("wall_stone"))
        draw.line([(x0+4, y0), (x0+4, y0+S-1)], fill=c("wall_cream_d"), width=2)
    elif part == "m":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("wall_stone"))
    elif part == "r":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0, y0, x0+S-5, y0+S-1], fill=c("wall_stone"))
        draw.line([(x0+S-5, y0), (x0+S-5, y0+S-1)], fill=c("wall_cream_d"), width=2)
    elif part == "window":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("wall_stone"))
        draw.rectangle([x0+8, y0+6, x0+24, y0+20], fill=c("window_frame"))
        draw.rectangle([x0+10, y0+8, x0+22, y0+18], fill=c("window_glass"))
        draw.line([(x0+16, y0+8), (x0+16, y0+18)], fill=c("window_frame"))
        draw.line([(x0+10, y0+13), (x0+22, y0+13)], fill=c("window_frame"))
    elif part == "door":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("wall_stone"))
        draw.rectangle([x0+6, y0+2, x0+26, y0+S-1], fill=c("door_brown"))
        draw.rectangle([x0+6, y0+2, x0+15, y0+S-1], fill=c("door_brown_d"))
        draw.rectangle([x0+22, y0+14, x0+24, y0+16], fill=c("fence_wood"))
        draw.rectangle([x0+2, y0+S-4, x0+30, y0+S-1], fill=c("step_stone"))

# --- Row 5: Centre Pokémon et Boutique ---
def draw_pkcenter_roof(draw, x0, y0, part="l"):
    S = TILE_SIZE
    rc = c("pkcenter_roof")
    rl = c("pkcenter_roof_l")
    if part == "l":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+4, y0+8, x0+S-1, y0+S-1], fill=rc)
        draw.rectangle([x0+4, y0+8, x0+S-1, y0+14], fill=rl)
    elif part == "m":
        draw.rectangle([x0, y0, x0+S-1, y0+7], fill=c("grass_mid"))
        draw.rectangle([x0, y0+8, x0+S-1, y0+S-1], fill=rc)
        draw.rectangle([x0, y0+8, x0+S-1, y0+14], fill=rl)
        # Croix blanche Centre Pokémon
        cross = c("pk_cross")
        draw.rectangle([x0+12, y0+16, x0+20, y0+28], fill=cross)
        draw.rectangle([x0+8, y0+20, x0+24, y0+24], fill=cross)
    elif part == "r":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0, y0+8, x0+S-5, y0+S-1], fill=rc)
        draw.rectangle([x0, y0+8, x0+S-5, y0+14], fill=rl)

def draw_pkcenter_wall(draw, x0, y0, part="l"):
    S = TILE_SIZE
    wall = c("pkcenter_wall")
    if part == "l":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+4, y0, x0+S-1, y0+S-1], fill=wall)
    elif part == "door":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=wall)
        # Grande porte vitrée
        draw.rectangle([x0+4, y0+2, x0+28, y0+S-1], fill=c("window_glass"))
        draw.line([(x0+16, y0+2), (x0+16, y0+S-1)], fill=c("window_frame"), width=2)
        draw.rectangle([x0+2, y0+S-3, x0+30, y0+S-1], fill=c("step_stone"))
    elif part == "r":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0, y0, x0+S-5, y0+S-1], fill=wall)

def draw_mart_roof(draw, x0, y0, part="l"):
    S = TILE_SIZE
    mr = c("mart_roof")
    ml = c("mart_roof_l")
    if part == "l":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+4, y0+8, x0+S-1, y0+S-1], fill=mr)
        draw.rectangle([x0+4, y0+8, x0+S-1, y0+14], fill=ml)
    elif part == "m":
        draw.rectangle([x0, y0, x0+S-1, y0+7], fill=c("grass_mid"))
        draw.rectangle([x0, y0+8, x0+S-1, y0+S-1], fill=mr)
        draw.rectangle([x0, y0+8, x0+S-1, y0+14], fill=ml)
        # Texte "MART" stylisé
        draw.rectangle([x0+6, y0+18, x0+26, y0+26], fill=(248, 248, 248))
    elif part == "r":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0, y0+8, x0+S-5, y0+S-1], fill=mr)
        draw.rectangle([x0, y0+8, x0+S-5, y0+14], fill=ml)

def draw_mart_wall(draw, x0, y0, part="l"):
    S = TILE_SIZE
    wall = c("mart_wall")
    if part == "l":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0+4, y0, x0+S-1, y0+S-1], fill=wall)
    elif part == "door":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=wall)
        draw.rectangle([x0+8, y0+2, x0+24, y0+S-1], fill=c("door_brown"))
        draw.rectangle([x0+8, y0+2, x0+15, y0+S-1], fill=c("door_brown_d"))
        draw.rectangle([x0+4, y0+S-3, x0+28, y0+S-1], fill=c("step_stone"))
    elif part == "r":
        draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("grass_mid"))
        draw.rectangle([x0, y0, x0+S-5, y0+S-1], fill=wall)

# --- Row 6-7: Intérieur ---
def draw_floor_wood(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    for i in range(y0, y0+S, 8):
        draw.line([(x0, i), (x0+S-1, i)], fill=c("floor_wood_d"), width=1)
    for j in range(x0, x0+S, 16):
        off = 8 if ((j - x0) // 16) % 2 else 0
        for i in range(y0+off, y0+S, 16):
            draw.line([(j, i), (j, i+7)], fill=c("floor_wood_d"), width=1)

def draw_floor_tile(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_tile"))
    for i in range(y0, y0+S, 16):
        draw.line([(x0, i), (x0+S-1, i)], fill=c("floor_tile_d"), width=1)
    for j in range(x0, x0+S, 16):
        draw.line([(j, y0), (j, y0+S-1)], fill=c("floor_tile_d"), width=1)

def draw_int_wall(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("int_wall"))
    draw.rectangle([x0, y0+S-4, x0+S-1, y0+S-1], fill=c("int_wall_d"))
    draw.line([(x0, y0+S-4), (x0+S-1, y0+S-4)], fill=c("wall_cream_d"))

def draw_counter(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_tile"))
    draw.rectangle([x0, y0+8, x0+S-1, y0+S-1], fill=c("counter_front"))
    draw.rectangle([x0, y0+8, x0+S-1, y0+14], fill=c("counter_top"))
    draw.line([(x0, y0+8), (x0+S-1, y0+8)], fill=c("shelf_d"))

def draw_healing_machine(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_tile"))
    # Machine
    draw.rectangle([x0+4, y0+4, x0+28, y0+S-1], fill=c("machine_body"))
    draw.rectangle([x0+4, y0+4, x0+28, y0+10], fill=(180, 188, 204))
    # Écran vert
    draw.rectangle([x0+10, y0+12, x0+22, y0+20], fill=c("machine_screen"))
    # Slots pokeball
    draw.ellipse([x0+8, y0+22, x0+14, y0+28], fill=(240, 80, 80))
    draw.ellipse([x0+18, y0+22, x0+24, y0+28], fill=(240, 80, 80))

def draw_shelf(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("int_wall"))
    draw.rectangle([x0+2, y0+4, x0+S-3, y0+S-4], fill=c("shelf"))
    draw.rectangle([x0+2, y0+4, x0+S-3, y0+8], fill=c("shelf_d"))
    draw.rectangle([x0+2, y0+15, x0+S-3, y0+19], fill=c("shelf_d"))
    # Objets sur étagère
    draw.rectangle([x0+6, y0+9, x0+12, y0+14], fill=(200, 80, 80))
    draw.rectangle([x0+16, y0+9, x0+22, y0+14], fill=(80, 120, 200))
    draw.rectangle([x0+8, y0+20, x0+14, y0+26], fill=(200, 200, 80))
    draw.rectangle([x0+18, y0+20, x0+26, y0+26], fill=(80, 200, 120))

def draw_carpet(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("carpet_red"))
    draw.rectangle([x0+2, y0+2, x0+S-3, y0+S-3], fill=c("carpet_red_d"))
    draw.rectangle([x0+4, y0+4, x0+S-5, y0+S-5], fill=c("carpet_red"))

def draw_int_floor_tile2(draw, x0, y0):
    """Carrelage motif différent"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_tile"))
    for i in range(0, S, 8):
        for j in range(0, S, 8):
            if (i + j) % 16 == 0:
                draw.rectangle([x0+j, y0+i, x0+j+7, y0+i+7], fill=c("floor_tile_d"))

def draw_int_wall_pattern(draw, x0, y0):
    """Mur intérieur décoré"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("int_wall"))
    draw.rectangle([x0, y0+S-6, x0+S-1, y0+S-1], fill=c("int_wall_d"))
    # Bande décorative
    draw.rectangle([x0, y0+S-8, x0+S-1, y0+S-6], fill=c("wall_cream_d"))

# Row 4 intérieur: Mobilier
def draw_bed_head(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    draw.rectangle([x0+4, y0+2, x0+S-5, y0+S-1], fill=(248, 232, 216))
    draw.rectangle([x0+6, y0+4, x0+S-7, y0+10], fill=(200, 200, 220))
    draw.rectangle([x0+4, y0+2, x0+S-5, y0+4], fill=(160, 120, 80))

def draw_bed_foot(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    draw.rectangle([x0+4, y0, x0+S-5, y0+24], fill=(200, 200, 220))
    draw.rectangle([x0+4, y0+24, x0+S-5, y0+28], fill=(160, 120, 80))

def draw_tv(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    draw.rectangle([x0+6, y0+4, x0+26, y0+22], fill=(60, 60, 60))
    draw.rectangle([x0+8, y0+6, x0+24, y0+20], fill=(120, 160, 200))
    draw.rectangle([x0+12, y0+22, x0+20, y0+S-1], fill=(80, 80, 80))

def draw_pc(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    # Écran
    draw.rectangle([x0+6, y0+2, x0+26, y0+18], fill=(60, 60, 68))
    draw.rectangle([x0+8, y0+4, x0+24, y0+16], fill=(80, 160, 200))
    # Base  
    draw.rectangle([x0+12, y0+18, x0+20, y0+22], fill=(100, 100, 108))
    # Clavier
    draw.rectangle([x0+4, y0+24, x0+28, y0+S-2], fill=(180, 180, 188))

def draw_plant(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    draw.rectangle([x0+10, y0+18, x0+22, y0+S-1], fill=(180, 120, 80))
    draw.ellipse([x0+6, y0+4, x0+26, y0+22], fill=c("tree_canopy_l"))
    draw.ellipse([x0+8, y0+6, x0+24, y0+18], fill=c("tree_canopy_h"))

def draw_stairs_up(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    for i in range(4):
        y = y0 + i * 7
        shade = max(0, 180 - i * 30)
        draw.rectangle([x0+2, y, x0+S-3, y+6], fill=(shade+40, shade+20, shade))

def draw_stairs_down(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    for i in range(4):
        y = y0 + i * 7
        shade = min(255, 80 + i * 30)
        draw.rectangle([x0+2, y, x0+S-3, y+6], fill=(shade+40, shade+20, shade))

def draw_doormat(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    draw.rectangle([x0+6, y0+8, x0+26, y0+24], fill=(160, 120, 80))
    draw.rectangle([x0+8, y0+10, x0+24, y0+22], fill=(180, 140, 96))

# Intérieur avancé
def draw_int_door(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("int_wall"))
    draw.rectangle([x0+8, y0+4, x0+24, y0+S-1], fill=c("door_brown"))
    draw.rectangle([x0+8, y0+4, x0+15, y0+S-1], fill=c("door_brown_d"))

def draw_int_window(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("int_wall"))
    draw.rectangle([x0+6, y0+4, x0+26, y0+22], fill=c("window_frame"))
    draw.rectangle([x0+8, y0+6, x0+24, y0+20], fill=(160, 216, 248))
    draw.line([(x0+16, y0+6), (x0+16, y0+20)], fill=c("window_frame"))

def draw_dark_wood(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood_d"))
    for i in range(y0, y0+S, 8):
        draw.line([(x0, i), (x0+S-1, i)], fill=(160, 128, 88), width=1)

def draw_wall_ext_window(draw, x0, y0):
    """Mur extérieur vu de l'intérieur avec fenêtre"""
    draw_int_window(draw, x0, y0)

def draw_table(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    draw.rectangle([x0+4, y0+6, x0+28, y0+26], fill=(160, 120, 72))
    draw.rectangle([x0+4, y0+6, x0+28, y0+10], fill=(180, 140, 88))

def draw_chair(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_wood"))
    draw.rectangle([x0+8, y0+4, x0+24, y0+12], fill=(140, 100, 60))
    draw.rectangle([x0+10, y0+14, x0+22, y0+22], fill=(160, 120, 72))
    draw.rectangle([x0+10, y0+22, x0+12, y0+S-2], fill=(120, 80, 48))
    draw.rectangle([x0+20, y0+22, x0+22, y0+S-2], fill=(120, 80, 48))

def draw_poster(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("int_wall"))
    draw.rectangle([x0+6, y0+4, x0+26, y0+24], fill=(220, 200, 160))
    draw.rectangle([x0+8, y0+6, x0+24, y0+22], fill=(200, 160, 120))

def draw_trashcan(draw, x0, y0):
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=c("floor_tile"))
    draw.rectangle([x0+8, y0+8, x0+24, y0+S-2], fill=(160, 160, 168))
    draw.rectangle([x0+6, y0+6, x0+26, y0+10], fill=(140, 140, 148))

def draw_black(draw, x0, y0):
    draw.rectangle([x0, y0, x0+TILE_SIZE-1, y0+TILE_SIZE-1], fill=c("black"))

def draw_void_tile(draw, x0, y0):
    draw.rectangle([x0, y0, x0+TILE_SIZE-1, y0+TILE_SIZE-1], fill=c("void"))

# --- Arène tiles ---
def draw_gym_floor(draw, x0, y0):
    """Sol d'arène avec motif"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=(200, 180, 140))
    # Motif en losange
    for i in range(0, S, 16):
        for j in range(0, S, 16):
            draw.polygon([(x0+j+8, y0+i), (x0+j+16, y0+i+8),
                         (x0+j+8, y0+i+16), (x0+j, y0+i+8)],
                        outline=(180, 160, 120))

def draw_gym_statue(draw, x0, y0):
    """Statue d'arène"""
    S = TILE_SIZE
    draw.rectangle([x0, y0, x0+S-1, y0+S-1], fill=(200, 180, 140))
    draw.rectangle([x0+8, y0+12, x0+24, y0+S-1], fill=c("rock"))
    draw.rectangle([x0+10, y0+4, x0+22, y0+14], fill=c("rock_l"))
    draw.ellipse([x0+12, y0+2, x0+20, y0+10], fill=c("rock_l"))


# ============================================================
# ASSEMBLAGE
# ============================================================

def generate_tileset():
    img = Image.new("RGBA", (SHEET_W, SHEET_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    def pos(index):
        """Index -> (x0, y0) pixel position"""
        col = index % COLS
        row = index // COLS
        return col * TILE_SIZE, row * TILE_SIZE
    
    # === Row 0 (0-15): Sols extérieurs ===
    draw_grass_plain(draw, *pos(0))
    draw_grass_variant(draw, *pos(1))
    draw_grass_flowers(draw, *pos(2))
    draw_tall_grass(draw, *pos(3))
    draw_path_center(draw, *pos(4))
    draw_path_edge_top(draw, *pos(5))
    draw_path_edge_bottom(draw, *pos(6))
    draw_path_edge_left(draw, *pos(7))
    draw_path_edge_right(draw, *pos(8))
    draw_path_corner(draw, *pos(9), corner="tl")
    draw_path_corner(draw, *pos(10), corner="tr")
    draw_path_corner(draw, *pos(11), corner="bl")
    draw_path_corner(draw, *pos(12), corner="br")
    draw_path_inner_corner(draw, *pos(13), corner="tl")
    draw_path_inner_corner(draw, *pos(14), corner="tr")
    draw_sand(draw, *pos(15))
    
    # === Row 1 (16-31): Eau et rivages ===
    draw_water(draw, *pos(16))
    draw_water_shore(draw, *pos(17), side="top")
    draw_water_shore(draw, *pos(18), side="bottom")
    draw_water_shore(draw, *pos(19), side="left")
    draw_water_shore(draw, *pos(20), side="right")
    draw_water_corner(draw, *pos(21), corner="tl")
    draw_water_corner(draw, *pos(22), corner="tr")
    draw_water_corner(draw, *pos(23), corner="bl")
    draw_water_corner(draw, *pos(24), corner="br")
    draw_water_inner_corner(draw, *pos(25), corner="tl")
    draw_water_inner_corner(draw, *pos(26), corner="tr")
    draw_water_inner_corner(draw, *pos(27), corner="bl")
    draw_water_inner_corner(draw, *pos(28), corner="br")
    draw_path_inner_corner(draw, *pos(29), corner="bl")  # coin chemin intérieur BL
    draw_path_inner_corner(draw, *pos(30), corner="br")  # coin chemin intérieur BR
    draw_grass_plain(draw, *pos(31))  # Réserve
    
    # === Row 2 (32-47): Arbres, végétation, obstacles ===
    draw_tree_top_left(draw, *pos(32))
    draw_tree_top_right(draw, *pos(33))
    draw_tree_bottom_left(draw, *pos(34))
    draw_tree_bottom_right(draw, *pos(35))
    draw_bush(draw, *pos(36))
    draw_small_tree(draw, *pos(37))
    draw_rock(draw, *pos(38))
    draw_fence_h(draw, *pos(39))
    draw_fence_v(draw, *pos(40))
    draw_sign(draw, *pos(41))
    draw_mailbox(draw, *pos(42))
    draw_ledge_top(draw, *pos(43))
    draw_ledge_left(draw, *pos(44))
    draw_ledge_right(draw, *pos(45))
    draw_stump(draw, *pos(46))
    draw_empty_grass(draw, *pos(47))
    
    # === Row 3 (48-63): Maisons toit rouge ===
    draw_house_roof(draw, *pos(48), part="tl", color="red")
    draw_house_roof(draw, *pos(49), part="tm", color="red")
    draw_house_roof(draw, *pos(50), part="tr", color="red")
    draw_house_roof(draw, *pos(51), part="bl", color="red")
    draw_house_roof(draw, *pos(52), part="bm", color="red")
    draw_house_roof(draw, *pos(53), part="br", color="red")
    draw_house_wall(draw, *pos(54), part="l")
    draw_house_wall(draw, *pos(55), part="m")
    draw_house_wall(draw, *pos(56), part="r")
    draw_house_wall(draw, *pos(57), part="window")
    draw_house_wall(draw, *pos(58), part="door")
    draw_grass_flowers(draw, *pos(59))  # Jardin devant maison
    draw_grass_plain(draw, *pos(60))
    draw_grass_plain(draw, *pos(61))
    draw_grass_plain(draw, *pos(62))
    draw_grass_plain(draw, *pos(63))
    
    # === Row 4 (64-79): Labo Chen (toit bleu) ===
    draw_lab_roof(draw, *pos(64), part="tl")
    draw_lab_roof(draw, *pos(65), part="tm")
    draw_lab_roof(draw, *pos(66), part="tr")
    draw_lab_roof(draw, *pos(67), part="bl")
    draw_lab_roof(draw, *pos(68), part="bm")
    draw_lab_roof(draw, *pos(69), part="br")
    draw_lab_wall(draw, *pos(70), part="l")
    draw_lab_wall(draw, *pos(71), part="m")
    draw_lab_wall(draw, *pos(72), part="r")
    draw_lab_wall(draw, *pos(73), part="window")
    draw_lab_wall(draw, *pos(74), part="door")
    draw_grass_plain(draw, *pos(75))
    draw_grass_plain(draw, *pos(76))
    draw_grass_plain(draw, *pos(77))
    draw_grass_plain(draw, *pos(78))
    draw_grass_plain(draw, *pos(79))
    
    # === Row 5 (80-95): Centre Pokémon + Boutique ===
    draw_pkcenter_roof(draw, *pos(80), part="l")
    draw_pkcenter_roof(draw, *pos(81), part="m")
    draw_pkcenter_roof(draw, *pos(82), part="r")
    draw_pkcenter_wall(draw, *pos(83), part="l")
    draw_pkcenter_wall(draw, *pos(84), part="door")
    draw_pkcenter_wall(draw, *pos(85), part="r")
    draw_mart_roof(draw, *pos(86), part="l")
    draw_mart_roof(draw, *pos(87), part="m")
    draw_mart_roof(draw, *pos(88), part="r")
    draw_mart_wall(draw, *pos(89), part="l")
    draw_mart_wall(draw, *pos(90), part="door")
    draw_mart_wall(draw, *pos(91), part="r")
    draw_gym_floor(draw, *pos(92))
    draw_gym_statue(draw, *pos(93))
    draw_grass_plain(draw, *pos(94))
    draw_grass_plain(draw, *pos(95))
    
    # === Row 6 (96-111): Intérieur base ===
    draw_floor_wood(draw, *pos(96))
    draw_int_wall(draw, *pos(97))
    draw_counter(draw, *pos(98))
    draw_healing_machine(draw, *pos(99))
    draw_shelf(draw, *pos(100))
    draw_carpet(draw, *pos(101))
    draw_floor_tile(draw, *pos(102))
    draw_int_wall_pattern(draw, *pos(103))
    draw_bed_head(draw, *pos(104))
    draw_bed_foot(draw, *pos(105))
    draw_tv(draw, *pos(106))
    draw_pc(draw, *pos(107))
    draw_plant(draw, *pos(108))
    draw_stairs_up(draw, *pos(109))
    draw_stairs_down(draw, *pos(110))
    draw_doormat(draw, *pos(111))
    
    # === Row 7 (112-127): Intérieur avancé ===
    draw_int_door(draw, *pos(112))
    draw_int_window(draw, *pos(113))
    draw_dark_wood(draw, *pos(114))
    draw_wall_ext_window(draw, *pos(115))
    draw_table(draw, *pos(116))
    draw_chair(draw, *pos(117))
    draw_poster(draw, *pos(118))
    draw_trashcan(draw, *pos(119))
    draw_int_floor_tile2(draw, *pos(120))
    draw_black(draw, *pos(121))
    draw_void_tile(draw, *pos(122))
    draw_grass_plain(draw, *pos(123))
    draw_grass_plain(draw, *pos(124))
    draw_grass_plain(draw, *pos(125))
    draw_grass_plain(draw, *pos(126))
    draw_grass_plain(draw, *pos(127))
    
    # === Rows 8-15: Réserve (herbe par défaut) ===
    for i in range(128, 256):
        draw_grass_plain(draw, *pos(i))
    
    return img

def generate_tileset_map_json():
    """Génère le JSON de métadonnées pour le nouveau tileset"""
    tiles = {}
    
    names = {
        # Row 0: Sols
        0: "herbe", 1: "herbe_variante", 2: "herbe_fleurs", 3: "herbe_haute",
        4: "chemin", 5: "chemin_bord_haut", 6: "chemin_bord_bas",
        7: "chemin_bord_gauche", 8: "chemin_bord_droit",
        9: "chemin_coin_hg", 10: "chemin_coin_hd", 11: "chemin_coin_bg", 12: "chemin_coin_bd",
        13: "chemin_coin_int_hg", 14: "chemin_coin_int_hd", 15: "sable",
        # Row 1: Eau
        16: "eau", 17: "eau_rivage_haut", 18: "eau_rivage_bas",
        19: "eau_rivage_gauche", 20: "eau_rivage_droit",
        21: "eau_coin_hg", 22: "eau_coin_hd", 23: "eau_coin_bg", 24: "eau_coin_bd",
        25: "eau_coin_int_hg", 26: "eau_coin_int_hd", 27: "eau_coin_int_bg", 28: "eau_coin_int_bd",
        29: "chemin_coin_int_bg", 30: "chemin_coin_int_bd", 31: "reserve",
        # Row 2: Arbres
        32: "arbre_hg", 33: "arbre_hd", 34: "arbre_bg", 35: "arbre_bd",
        36: "buisson", 37: "petit_arbre", 38: "rocher",
        39: "cloture_h", 40: "cloture_v", 41: "panneau", 42: "boite_lettres",
        43: "rebord_haut", 44: "rebord_gauche", 45: "rebord_droit",
        46: "souche", 47: "herbe_reserve",
        # Row 3: Maisons rouges
        48: "maison_toit_hg", 49: "maison_toit_hm", 50: "maison_toit_hd",
        51: "maison_toit_bg", 52: "maison_toit_bm", 53: "maison_toit_bd",
        54: "maison_mur_g", 55: "maison_mur_m", 56: "maison_mur_d",
        57: "maison_fenetre", 58: "maison_porte",
        # Row 4: Labo bleu
        64: "labo_toit_hg", 65: "labo_toit_hm", 66: "labo_toit_hd",
        67: "labo_toit_bg", 68: "labo_toit_bm", 69: "labo_toit_bd",
        70: "labo_mur_g", 71: "labo_mur_m", 72: "labo_mur_d",
        73: "labo_fenetre", 74: "labo_porte",
        # Row 5: Centre & Boutique
        80: "centre_toit_g", 81: "centre_toit_m", 82: "centre_toit_d",
        83: "centre_mur_g", 84: "centre_porte", 85: "centre_mur_d",
        86: "boutique_toit_g", 87: "boutique_toit_m", 88: "boutique_toit_d",
        89: "boutique_mur_g", 90: "boutique_porte", 91: "boutique_mur_d",
        92: "arene_sol", 93: "arene_statue",
        # Row 6: Intérieur
        96: "sol_bois", 97: "mur_interieur", 98: "comptoir",
        99: "machine_soin", 100: "etagere", 101: "tapis",
        102: "sol_carrelage", 103: "mur_motif",
        104: "lit_tete", 105: "lit_pied", 106: "tv", 107: "pc",
        108: "plante", 109: "escalier_haut", 110: "escalier_bas", 111: "paillasson",
        # Row 7: Intérieur avancé
        112: "porte_int", 113: "fenetre_int", 114: "bois_fonce",
        115: "mur_ext_fenetre", 116: "table", 117: "chaise",
        118: "poster", 119: "poubelle", 120: "carrelage_motif",
        121: "noir", 122: "vide",
    }
    
    for idx, name in names.items():
        col = idx % COLS
        row = idx // COLS
        tiles[f"tile_{idx}"] = {
            "name": name,
            "atlas_x": col * TILE_SIZE,
            "atlas_y": row * TILE_SIZE,
            "col": col,
            "row": row
        }
    
    return tiles


if __name__ == "__main__":
    print("Génération du tileset HD style RFVF...")
    
    # Générer le tileset
    img = generate_tileset()
    
    # Sauvegarder
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites", "tilesets")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "tileset_outdoor.png")
    img.save(output_path, "PNG")
    print(f"Tileset sauvegardé: {output_path} ({img.size[0]}x{img.size[1]} px)")
    
    # Générer le JSON de métadonnées
    tilemap_json = generate_tileset_map_json()
    json_path = os.path.join(output_dir, "tileset_map.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tilemap_json, f, indent=2, ensure_ascii=False)
    print(f"Métadonnées sauvegardées: {json_path}")
    
    print("Terminé !")
