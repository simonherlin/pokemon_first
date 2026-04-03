#!/usr/bin/env python3
"""
build_frlg_tileset.py — Construit tileset_outdoor.png à partir des metatiles FRLG.

Utilise les metatiles rendus depuis les données de décompilation pokefirered
pour créer le tileset 512×512 (16×16 tiles à 32×32px) utilisé par le jeu.

Chaque position dans le tileset correspond à un TILE_* dans tileset_builder.gd.
"""

import os
import sys
import numpy as np
from PIL import Image

# Répertoires
BASE = os.path.dirname(os.path.abspath(__file__))
RENDERED_DIR = os.path.join(BASE, "source_sprites", "frlg_rendered")
OUTPUT = os.path.join(BASE, "..", "assets", "sprites", "tilesets", "tileset_outdoor.png")

TILE_SIZE = 32  # Chaque metatile rendu en 2× = 32×32
COLS = 16
ROWS = 16

def load_rendered_sheet(name):
    """Charge une feuille de metatiles rendus (32×32 par cell, 16 colonnes)."""
    path = os.path.join(RENDERED_DIR, f"{name}_32.png")
    if not os.path.exists(path):
        print(f"WARN: {path} not found")
        return None
    return np.array(Image.open(path).convert("RGBA"))

def get_metatile(sheet, idx):
    """Extrait un metatile 32×32 depuis une feuille rendue (16 cols)."""
    if sheet is None:
        return np.zeros((TILE_SIZE, TILE_SIZE, 4), dtype=np.uint8)
    cols = sheet.shape[1] // TILE_SIZE
    row = idx // cols
    col = idx % cols
    y0, y1 = row * TILE_SIZE, (row + 1) * TILE_SIZE
    x0, x1 = col * TILE_SIZE, (col + 1) * TILE_SIZE
    if y1 > sheet.shape[0] or x1 > sheet.shape[1]:
        return np.zeros((TILE_SIZE, TILE_SIZE, 4), dtype=np.uint8)
    return sheet[y0:y1, x0:x1].copy()


def main():
    # Charger les feuilles rendues
    print("Chargement des feuilles rendues...")
    general = load_rendered_sheet("primary_general")     # Outdoor shared
    building = load_rendered_sheet("primary_building")    # Indoor shared
    pallet = load_rendered_sheet("pallet_town")           # Bourg Palette (general + secondary)
    viridian = load_rendered_sheet("viridian_city")       # Jadielle
    pokemon_center = load_rendered_sheet("pokemon_center")  # Centre Pokémon interior
    mart = load_rendered_sheet("mart")                     # Boutique interior
    cave = load_rendered_sheet("cave")                     # Grottes
    
    # Feuille de sortie 512×512
    output = np.zeros((ROWS * TILE_SIZE, COLS * TILE_SIZE, 4), dtype=np.uint8)
    
    def place(game_idx, sheet, meta_idx):
        """Place un metatile FRLG à la position du game tile."""
        tile = get_metatile(sheet, meta_idx)
        row = game_idx // COLS
        col = game_idx % COLS
        y0 = row * TILE_SIZE
        x0 = col * TILE_SIZE
        output[y0:y0+TILE_SIZE, x0:x0+TILE_SIZE] = tile
    
    # =========================================================================
    # MAPPING : game TILE_* index → (source_sheet, FRLG_metatile_index)
    # =========================================================================
    # Indices dans les sheets combinées (general: 0-639, secondary: 640+)
    # Pour pallet_town sheet: indices 0-639 = primary_general, 640+ = secondary
    # Metatile hex = index in FRLG: primary 0x000-0x27F, secondary 0x280+
    # secondary[N] in rendered sheet = index 640 + N
    
    # Conversions pratiques
    def sec(frlg_hex):
        """Convertit un ID metatile FRLG secondaire (>= 0x280) en index rendu."""
        return frlg_hex - 0x280 + 640
    
    print("Construction du tileset...")
    
    # === LIGNE 0 : Sols extérieurs (0-15) ===
    # TILE_HERBE (0) = herbe d'encounter
    place(0, general, 13)          # 0x00D = General_Plain_Grass
    # TILE_HERBE_VARIANTE (1) = sol sans herbe
    place(1, general, 1)           # 0x001 = General_Plain_Mowed
    # TILE_HERBE_FLEURS (2) = variante fleurie - utiliser une variante de ground
    place(2, general, 5)           # ground variant with some detail
    # TILE_HERBE_HAUTE (3) = herbe haute/sombre
    place(3, general, 10)          # 0x00A = General_ThinTreeTop_Grass (darker green)
    # TILE_CHEMIN (4) = chemin plat
    place(4, general, 8)           # flat walkable ground
    # TILE_CHEMIN_BORD_HAUT (5) = bord de chemin haut
    place(5, general, 22)          # path edge variant
    # TILE_CHEMIN_BORD_BAS (6)
    place(6, general, 38)          # path edge south
    # TILE_CHEMIN_BORD_GAUCHE (7)
    place(7, general, 36)          # path edge west
    # TILE_CHEMIN_BORD_DROIT (8)
    place(8, general, 37)          # path edge east
    # TILE_CHEMIN_COIN_HG (9)
    place(9, general, 20)          # corner NW
    # TILE_CHEMIN_COIN_HD (10)
    place(10, general, 21)         # corner NE
    # TILE_CHEMIN_COIN_BG (11)
    place(11, general, 28)         # corner SW
    # TILE_CHEMIN_COIN_BD (12)
    place(12, general, 29)         # corner SE
    # TILE_CHEMIN_COIN_INT_HG (13)
    place(13, general, 30)         # inner corner NW
    # TILE_CHEMIN_COIN_INT_HD (14)
    place(14, general, 31)         # inner corner NE
    # TILE_SABLE (15)
    place(15, general, 24)         # sand/gravel colored tile
    
    # === LIGNE 1 : Eau et rivages (16-31) ===
    # TILE_EAU (16)
    place(16, general, 299)        # 0x12B = General_CalmWater
    # Water edges - from the water area in primary_general (around metatiles 256+)
    # In FRLG, water border metatiles are complex. Let me use the ocean area.
    # Ocean tiles are at behavior 0x15: indices 459,460,467,468,475,476,483,484...
    # But those are ocean-style. For ponds/rivers, use the area around 268-310
    place(17, general, 268)        # water rivage haut
    place(18, general, 284)        # water rivage bas
    place(19, general, 276)        # water rivage gauche
    place(20, general, 270)        # water rivage droit
    place(21, general, 256)        # water coin HG
    place(22, general, 257)        # water coin HD
    place(23, general, 272)        # water coin BG
    place(24, general, 273)        # water coin BD
    place(25, general, 264)        # water coin int HG
    place(26, general, 265)        # water coin int HD
    place(27, general, 280)        # water coin int BG
    place(28, general, 281)        # water coin int BD
    # TILE_CHEMIN_COIN_INT_BG (29) / TILE_CHEMIN_COIN_INT_BD (30)
    place(29, general, 14)         # path inner corner BG
    place(30, general, 15)         # path inner corner BD
    # TILE_RESERVE (31)
    place(31, general, 0)          # transparent/empty
    
    # === LIGNE 2 : Arbres, végétation, obstacles (32-47) ===
    # Arbres FRLG : metatiles autour de 40-60 zone (trees with transparency)
    # Wide tree: uses metatiles 11 (left on grass) and 12 (right on grass)
    # Let me use the tree metatiles from the general set
    # In FRLG, tree tops are at 0x00A-0x00F (10-15), bottoms at 0x013 (19), etc.
    # Large tree body metatiles are in the 40-63 range (blue/water area...)
    # Actually, looking at metatile colors, 40-45 = BLUE water, not trees
    # Trees in FRLG are multi-metatile structures
    # Tree rendering: metatiles with palette 3 (green) and behavior impassable (0x411/0x415)
    # Impassable green area: look at 580-620 range (behavior 0x411)
    place(32, general, 11)         # TILE_ARBRE_HG - wide tree top left on grass
    place(33, general, 12)         # TILE_ARBRE_HD - wide tree top right on grass
    place(34, general, 14)         # TILE_ARBRE_BG - tree bottom variants (mowed-base)
    place(35, general, 15)         # TILE_ARBRE_BD
    # TILE_BUISSON (36)
    place(36, general, 35)         # dark green = bush
    # TILE_PETIT_ARBRE (37) - cuttable small tree
    place(37, general, 10)         # thin tree top (0x00A)
    # TILE_ROCHER (38)
    place(38, general, 25)         # rock/stone looking tile
    # TILE_CLOTURE_H (39) - fence horizontal
    place(39, general, 18)         # fence/wall variant
    # TILE_CLOTURE_V (40) - fence vertical
    place(40, general, 34)         # vertical fence variant
    # TILE_PANNEAU (41) - signpost
    place(41, general, 2)          # 0x002 = signpost behavior
    # TILE_BOITE_LETTRES (42)
    place(42, general, 3)          # another signpost variant
    # TILE_REBORD_HAUT (43) - ledge top (jump south)
    place(43, general, 135)        # 0x087 jump_south
    # TILE_REBORD_GAUCHE (44)
    place(44, general, 131)        # jump_west
    # TILE_REBORD_DROIT (45)
    place(45, general, 132)        # jump_east
    # TILE_SOUCHE (46)
    place(46, general, 19)         # tree stump / thin tree on mowed (0x013)
    # TILE_HERBE_RESERVE (47)
    place(47, general, 9)          # grass variant
    
    # === LIGNE 3 : Maisons toit rouge (48-63) ===
    # Depuis Pallet Town secondary metatiles
    # Maison FRLG structure (du map.bin) :
    #   Toit haut :  0x281 0x282 0x282 0x283
    #   Toit bas  :  0x289 0x28A 0x28A 0x28B
    #   Mur haut  :  0x291 0x293 0x292 0x294
    #   Mur milieu:  0x298 0x299 0x29A 0x29B 0x29C
    #   Porte     :  0x2A0 0x2A3(door) 0x2A2 0x2A1 0x2A4
    
    place(48, pallet, sec(0x281))   # TILE_MAISON_TOIT_HG - roof top-left
    place(49, pallet, sec(0x282))   # TILE_MAISON_TOIT_HM - roof top-middle
    place(50, pallet, sec(0x283))   # TILE_MAISON_TOIT_HD - roof top-right
    place(51, pallet, sec(0x289))   # TILE_MAISON_TOIT_BG - roof bottom-left
    place(52, pallet, sec(0x28A))   # TILE_MAISON_TOIT_BM - roof bottom-middle
    place(53, pallet, sec(0x28B))   # TILE_MAISON_TOIT_BD - roof bottom-right
    place(54, pallet, sec(0x291))   # TILE_MAISON_MUR_G - wall left
    place(55, pallet, sec(0x292))   # TILE_MAISON_MUR_M - wall middle
    place(56, pallet, sec(0x294))   # TILE_MAISON_MUR_D - wall right
    place(57, pallet, sec(0x293))   # TILE_MAISON_FENETRE - window
    place(58, pallet, sec(0x2A3))   # TILE_MAISON_PORTE - door!
    # Extra house tiles (59-63)
    place(59, pallet, sec(0x298))   # house wall variant
    place(60, pallet, sec(0x2A0))   # ground level left
    place(61, pallet, sec(0x2A2))   # ground level near door
    place(62, pallet, sec(0x2A5))   # doorstep
    place(63, pallet, sec(0x29E))   # roof/gutter edge (heavily used)
    
    # === LIGNE 4 : Labo Chen / toit bleu (64-79) ===
    # Oak's Lab structure from map.bin:
    #   0x2B0 0x2B1 0x2B1 0x2B1 0x2B1 0x2B3 0x2B4  (lab roof top)
    #   0x2B8 0x2B9 0x2B9 0x2B9 0x2B9 0x2BB 0x2BC  (lab roof bottom)
    #   0x284                                        (lab wall top)
    #   0x2C0 0x2C1 0x2D0 0x2C2 0x2C3 0x2C4 0x2C5  (lab wall)
    #   0x2C8 0x2C9 0x2D8 0x2AC(door) 0x2CB 0x2CC 0x2CD (lab door row)
    
    place(64, pallet, sec(0x2B0))   # TILE_LABO_TOIT_HG
    place(65, pallet, sec(0x2B1))   # TILE_LABO_TOIT_HM
    place(66, pallet, sec(0x2B3))   # TILE_LABO_TOIT_HD
    place(67, pallet, sec(0x2B8))   # TILE_LABO_TOIT_BG
    place(68, pallet, sec(0x2B9))   # TILE_LABO_TOIT_BM
    place(69, pallet, sec(0x2BB))   # TILE_LABO_TOIT_BD
    place(70, pallet, sec(0x2C0))   # TILE_LABO_MUR_G
    place(71, pallet, sec(0x2C2))   # TILE_LABO_MUR_M
    place(72, pallet, sec(0x2C5))   # TILE_LABO_MUR_D
    place(73, pallet, sec(0x2D0))   # TILE_LABO_FENETRE (lab emblem/window)
    place(74, pallet, sec(0x2AC))   # TILE_LABO_PORTE (lab door!)
    # Extra lab tiles (75-79)
    place(75, pallet, sec(0x2B4))   # lab roof right edge
    place(76, pallet, sec(0x2BC))   # lab roof bottom-right
    place(77, pallet, sec(0x2C1))   # lab wall element
    place(78, pallet, sec(0x2C8))   # lab ground left
    place(79, pallet, sec(0x2D8))   # lab entrance area
    
    # === LIGNE 5 : Centre Pokémon + Boutique (80-95) ===
    # Pokémon Center sign: metatile 96, 97 (behavior 0x87 = POKEMON_CENTER_SIGN)
    # PokéMart sign: metatile 64, 65 (behavior 0x88 = POKEMART_SIGN)
    # In FRLG, PokéCenter and PokéMart exterior appearances come from
    # secondary tilesets of cities. Let me use general tiles for now.
    
    # Centre Pokémon exterior (from general primary or Viridian secondary)
    # The red roof of a Pokemon Center uses specific metatiles
    place(80, general, 80)          # TILE_CENTRE_TOIT_G - red element identified
    place(81, general, 112)         # TILE_CENTRE_TOIT_M - building element
    place(82, general, 128)         # TILE_CENTRE_TOIT_D - building element
    place(83, general, 96)          # TILE_CENTRE_MUR_G - pokemon center sign
    place(84, general, 61)          # TILE_CENTRE_PORTE - door (warp_door behavior)
    place(85, general, 97)          # TILE_CENTRE_MUR_D - pokemon center sign 2
    
    # Boutique exterior
    place(86, general, 64)          # TILE_BOUTIQUE_TOIT_G - mart sign
    place(87, general, 160)         # TILE_BOUTIQUE_TOIT_M
    place(88, general, 65)          # TILE_BOUTIQUE_TOIT_D - mart sign 2
    place(89, general, 100)         # TILE_BOUTIQUE_MUR_G
    place(90, general, 98)          # TILE_BOUTIQUE_PORTE - door
    place(91, general, 99)          # TILE_BOUTIQUE_MUR_D
    
    # Arena
    place(92, general, 4)           # TILE_ARENE_SOL - arena ground
    place(93, general, 60)          # TILE_ARENE_STATUE - statue/ornament
    # Fill 94-95
    place(94, general, 62)
    place(95, general, 208)
    
    # === LIGNE 6 : Intérieur base (96-111) ===
    # From primary_building metatiles
    # Building interior metatiles: these are the standard indoor tiles
    # Floor tiles, walls, counter, healing machine, shelf, carpet, etc.
    # Building metatiles are indexed 0-639 in the building sheet
    # Key metatiles from building:
    #   0x062 = Building_PCOff → metatile 98
    #   0x063 = Building_PCOn → metatile 99
    
    place(96, building, 1)          # TILE_SOL_INT - indoor floor
    place(97, building, 8)          # TILE_MUR_INT - indoor wall
    place(98, building, 16)         # TILE_COMPTOIR - counter
    place(99, building, 24)         # TILE_MACHINE_SOIN - healing machine area
    place(100, building, 32)        # TILE_ETAGERE - shelf
    place(101, building, 2)         # TILE_TAPIS - carpet/rug
    place(102, building, 3)         # TILE_SOL_CARRELAGE - tile floor
    place(103, building, 9)         # TILE_MUR_MOTIF - patterned wall
    place(104, building, 40)        # TILE_LIT_TETE - bed head
    place(105, building, 48)        # TILE_LIT_PIED - bed foot
    place(106, building, 56)        # TILE_TV - television
    place(107, building, 98)        # TILE_PC - PC (0x062 = Building_PCOff)
    place(108, building, 64)        # TILE_PLANTE - plant
    place(109, building, 80)        # TILE_ESCALIER_UP - stairs up
    place(110, building, 88)        # TILE_ESCALIER_DOWN - stairs down
    place(111, building, 4)         # TILE_PAILLASSON - doormat
    
    # === LIGNE 7 : Intérieur avancé (112-127) ===
    place(112, building, 96)        # TILE_PORTE_INT - interior door
    place(113, building, 104)       # TILE_FENETRE_INT - interior window
    place(114, building, 5)         # TILE_SOL_BOIS_FONCE - dark wood floor
    place(115, building, 10)        # TILE_MUR_EXT_FENETRE - wall with window
    place(116, building, 112)       # TILE_TABLE - table
    place(117, building, 120)       # TILE_CHAISE - chair
    place(118, building, 128)       # TILE_POSTER - poster
    place(119, building, 136)       # TILE_POUBELLE - trash can
    place(120, building, 6)         # TILE_CARRELAGE_MOTIF - patterned floor
    place(121, building, 0)         # TILE_NOIR - black/dark
    place(122, building, 0)         # TILE_VIDE - empty/void
    
    # === LIGNES 8-15 : Tiles supplémentaires et réserve ===
    # Fill remaining rows with useful additional tiles from various sources
    
    # Row 8 (128-143): More outdoor variants
    for i in range(16):
        meta = 128 + i  # General metatiles 128-143
        place(128 + i, general, meta)
    
    # Row 9 (144-159): More general tiles
    for i in range(16):
        place(144 + i, general, 144 + i)
    
    # Row 10 (160-175): General tiles continuation
    for i in range(16):
        place(160 + i, general, 160 + i)
    
    # Row 11 (176-191): Building variants
    for i in range(16):
        place(176 + i, general, 176 + i)
    
    # Row 12 (192-207): More terrain
    for i in range(16):
        place(192 + i, general, 192 + i)
    
    # Row 13 (208-223): Forest/cave related
    for i in range(16):
        place(208 + i, general, 208 + i)
    
    # Row 14 (224-239): Extended water/cliffs
    for i in range(16):
        place(224 + i, general, 224 + i)
    
    # Row 15 (240-255): Extended buildings
    for i in range(16):
        place(240 + i, general, 240 + i)
    
    # Sauvegarder
    img = Image.fromarray(output, 'RGBA')
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    img.save(OUTPUT)
    print(f"✓ Tileset sauvegardé: {OUTPUT}")
    print(f"  Taille: {img.size[0]}×{img.size[1]} pixels")
    
    # Vérification rapide
    non_empty = 0
    for row in range(ROWS):
        for col in range(COLS):
            tile = output[row*TILE_SIZE:(row+1)*TILE_SIZE, col*TILE_SIZE:(col+1)*TILE_SIZE]
            if tile[:,:,3].any():  # Any non-transparent pixel
                non_empty += 1
    print(f"  Tiles non-vides: {non_empty}/{ROWS*COLS}")


if __name__ == "__main__":
    main()
