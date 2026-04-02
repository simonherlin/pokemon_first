#!/usr/bin/env python3
"""Génère des tiles indoor style FRLG pour le tileset outdoor.
Remplace les tiles de la ligne 3 (indices 24-31) par de meilleurs tiles:
  24 = Sol parquet (wooden floor pattern)
  25 = Mur intérieur (wall with baseboard)
  26 = Comptoir/Table
  27 = Machine de soin (pink/white)
  28 = Étagère/Bibliothèque
  29 = Tapis rouge
  30 = Sol carrelé (checkered)
  31 = Mur décoré

Puis ajoute des lignes 4-7 pour plus de tiles indoor:
  32 = Lit (tête) - bleu
  33 = Lit (pied) - bleu
  34 = Console/TV
  35 = PC/Bureau
  36 = Plante verte
  37 = Escalier montée
  38 = Escalier descente
  39 = Paillasson/Tapis porte

  40 = Porte intérieure
  41 = Fenêtre intérieure
  42 = Sol bois foncé
  43 = Mur fenêtre extérieur
  44 = Table ronde
  45 = Chaise
  46 = Poster mur
  47 = Poubelle
"""
from PIL import Image, ImageDraw
import os

TILE = 32
COLS = 8

def draw_rect(draw, x, y, w, h, color):
    draw.rectangle([x, y, x+w-1, y+h-1], fill=color)

def draw_parquet(draw, ox, oy):
    """Tile 24: Sol parquet FRLG - beige/brun avec lignes"""
    base = (216, 200, 168)
    line = (192, 176, 144)
    dark = (176, 160, 128)
    draw_rect(draw, ox, oy, 32, 32, base)
    # Lignes horizontales du parquet
    for y in [0, 8, 16, 24]:
        draw_rect(draw, ox, oy+y, 32, 1, line)
    # Motif décalé
    for y in [0, 16]:
        draw_rect(draw, ox+16, oy+y+4, 1, 4, dark)
    for y in [8, 24]:
        draw_rect(draw, ox, oy+y+4, 1, 4, dark)
        draw_rect(draw, ox+31, oy+y+4, 1, 4, dark)

def draw_mur(draw, ox, oy):
    """Tile 25: Mur intérieur - crème avec plinthe brune"""
    wall = (232, 224, 208)
    wall_shadow = (216, 208, 192)
    baseboard = (152, 120, 88)
    baseboard_top = (168, 136, 104)
    # Mur principal
    draw_rect(draw, ox, oy, 32, 26, wall)
    # Légère ombre
    draw_rect(draw, ox, oy+12, 32, 2, wall_shadow)
    # Plinthe
    draw_rect(draw, ox, oy+26, 32, 2, baseboard_top)
    draw_rect(draw, ox, oy+28, 32, 4, baseboard)

def draw_comptoir(draw, ox, oy):
    """Tile 26: Comptoir/Table brun"""
    top = (168, 128, 88)
    front = (144, 104, 64)
    edge = (120, 88, 56)
    draw_rect(draw, ox, oy, 32, 8, top)
    draw_rect(draw, ox, oy+8, 32, 2, edge)
    draw_rect(draw, ox, oy+10, 32, 22, front)

def draw_machine_soin(draw, ox, oy):
    """Tile 27: Machine centre Pokémon - rose/blanc"""
    body = (248, 208, 224)
    screen = (160, 240, 160)
    base_c = (200, 168, 184)
    draw_rect(draw, ox+4, oy+4, 24, 24, body)
    draw_rect(draw, ox+8, oy+8, 16, 10, screen)
    draw_rect(draw, ox+4, oy+24, 24, 4, base_c)
    # Ball slot
    draw_rect(draw, ox+12, oy+20, 8, 4, (255, 80, 80))

def draw_etagere(draw, ox, oy):
    """Tile 28: Étagère/Bibliothèque - bois avec livres"""
    wood = (160, 120, 80)
    shelf = (144, 104, 64)
    draw_rect(draw, ox, oy, 32, 32, wood)
    # Étagères
    for y in [0, 10, 20]:
        draw_rect(draw, ox, oy+y, 32, 2, shelf)
        # Livres de couleurs variées
        colors = [(200, 60, 60), (60, 100, 200), (60, 160, 60), (200, 180, 60)]
        for i, c in enumerate(colors):
            draw_rect(draw, ox+2+i*7, oy+y+3, 5, 7, c)

def draw_tapis_rouge(draw, ox, oy):
    """Tile 29: Tapis rouge FRLG"""
    red = (192, 48, 48)
    red_l = (216, 72, 72)
    border = (160, 32, 32)
    draw_rect(draw, ox, oy, 32, 32, red)
    draw_rect(draw, ox, oy, 32, 2, border)
    draw_rect(draw, ox, oy+30, 32, 2, border)
    draw_rect(draw, ox, oy, 2, 32, border)
    draw_rect(draw, ox+30, oy, 2, 32, border)
    # Motif central
    draw_rect(draw, ox+12, oy+12, 8, 8, red_l)

def draw_carrelage(draw, ox, oy):
    """Tile 30: Sol carrelé - damier blanc/gris clair"""
    white = (240, 240, 240)
    gray = (208, 216, 224)
    for cy in range(4):
        for cx in range(4):
            c = white if (cx+cy) % 2 == 0 else gray
            draw_rect(draw, ox+cx*8, oy+cy*8, 8, 8, c)

def draw_mur_deco(draw, ox, oy):
    """Tile 31: Mur avec motif/papier peint"""
    wall = (216, 208, 192)
    pattern = (200, 192, 176)
    baseboard = (152, 120, 88)
    draw_rect(draw, ox, oy, 32, 28, wall)
    # Motif losange subtil
    for y in range(0, 24, 8):
        for x in range(0, 32, 8):
            draw_rect(draw, ox+x+3, oy+y+3, 2, 2, pattern)
    draw_rect(draw, ox, oy+28, 32, 4, baseboard)

def draw_lit_tete(draw, ox, oy):
    """Tile 32: Lit (tête) - oreiller blanc, drap bleu"""
    frame = (120, 88, 56)
    pillow = (240, 240, 248)
    sheet = (80, 120, 200)
    draw_rect(draw, ox, oy, 32, 32, sheet)
    draw_rect(draw, ox, oy, 32, 4, frame)
    draw_rect(draw, ox, oy, 4, 32, frame)
    draw_rect(draw, ox+28, oy, 4, 32, frame)
    # Oreiller
    draw_rect(draw, ox+6, oy+6, 20, 10, pillow)
    draw_rect(draw, ox+8, oy+8, 16, 6, (248, 248, 255))

def draw_lit_pied(draw, ox, oy):
    """Tile 33: Lit (pied) - couverture bleue"""
    frame = (120, 88, 56)
    sheet = (80, 120, 200)
    sheet_l = (100, 140, 220)
    draw_rect(draw, ox, oy, 32, 32, sheet)
    draw_rect(draw, ox, oy, 4, 32, frame)
    draw_rect(draw, ox+28, oy, 4, 32, frame)
    draw_rect(draw, ox, oy+28, 32, 4, frame)
    # Motif couverture
    draw_rect(draw, ox+6, oy+4, 20, 4, sheet_l)
    draw_rect(draw, ox+6, oy+16, 20, 4, sheet_l)

def draw_tv(draw, ox, oy):
    """Tile 34: Console/TV"""
    body = (64, 64, 72)
    screen = (80, 120, 80)
    stand = (96, 96, 104)
    draw_rect(draw, ox+4, oy+4, 24, 20, body)
    draw_rect(draw, ox+6, oy+6, 20, 14, screen)
    draw_rect(draw, ox+12, oy+24, 8, 4, stand)
    # Console dessous
    draw_rect(draw, ox+8, oy+28, 16, 4, (40, 40, 48))

def draw_pc(draw, ox, oy):
    """Tile 35: PC/Bureau"""
    desk = (168, 136, 104)
    screen = (160, 200, 240)
    body = (200, 200, 208)
    draw_rect(draw, ox, oy+16, 32, 16, desk)
    draw_rect(draw, ox+8, oy+2, 16, 16, body)
    draw_rect(draw, ox+10, oy+4, 12, 10, screen)
    # Clavier
    draw_rect(draw, ox+8, oy+18, 16, 4, (80, 80, 88))

def draw_plante(draw, ox, oy):
    """Tile 36: Plante verte en pot"""
    pot = (176, 104, 64)
    pot_rim = (192, 120, 80)
    leaf = (56, 152, 56)
    leaf_d = (40, 120, 40)
    # Pot
    draw_rect(draw, ox+10, oy+22, 12, 10, pot)
    draw_rect(draw, ox+8, oy+20, 16, 4, pot_rim)
    # Feuilles
    draw_rect(draw, ox+8, oy+8, 16, 14, leaf)
    draw_rect(draw, ox+4, oy+12, 8, 8, leaf_d)
    draw_rect(draw, ox+20, oy+10, 8, 8, leaf_d)
    draw_rect(draw, ox+12, oy+4, 8, 8, leaf)

def draw_escalier_up(draw, ox, oy):
    """Tile 37: Escalier montée"""
    wood = (144, 112, 80)
    step = (168, 136, 104)
    draw_rect(draw, ox, oy, 32, 32, wood)
    for i in range(4):
        y = i * 8
        draw_rect(draw, ox+2, oy+y, 28, 6, step)
        draw_rect(draw, ox+2, oy+y+6, 28, 2, (120, 88, 56))

def draw_escalier_down(draw, ox, oy):
    """Tile 38: Escalier descente"""
    wood = (144, 112, 80)
    step = (168, 136, 104)
    draw_rect(draw, ox, oy, 32, 32, wood)
    for i in range(4):
        y = (3-i) * 8
        draw_rect(draw, ox+2, oy+y, 28, 6, step)
        draw_rect(draw, ox+2, oy+y+6, 28, 2, (120, 88, 56))

def draw_paillasson(draw, ox, oy):
    """Tile 39: Paillasson devant la porte"""
    mat = (168, 144, 104)
    border = (144, 120, 80)
    draw_rect(draw, ox+4, oy+8, 24, 16, mat)
    draw_rect(draw, ox+4, oy+8, 24, 2, border)
    draw_rect(draw, ox+4, oy+22, 24, 2, border)

def draw_porte(draw, ox, oy):
    """Tile 40: Porte intérieure"""
    frame_c = (120, 88, 56)
    door = (168, 136, 104)
    handle = (208, 192, 64)
    draw_rect(draw, ox+4, oy, 24, 32, door)
    draw_rect(draw, ox+2, oy, 4, 32, frame_c)
    draw_rect(draw, ox+26, oy, 4, 32, frame_c)
    draw_rect(draw, ox+2, oy, 28, 3, frame_c)
    # Poignée
    draw_rect(draw, ox+22, oy+16, 3, 3, handle)

def draw_fenetre_int(draw, ox, oy):
    """Tile 41: Fenêtre vue intérieure"""
    wall = (232, 224, 208)
    frame_c = (120, 88, 56)
    sky = (160, 200, 240)
    draw_rect(draw, ox, oy, 32, 32, wall)
    draw_rect(draw, ox+4, oy+4, 24, 20, frame_c)
    draw_rect(draw, ox+6, oy+6, 20, 16, sky)
    # Croisillons
    draw_rect(draw, ox+15, oy+6, 2, 16, frame_c)
    draw_rect(draw, ox+6, oy+13, 20, 2, frame_c)
    # Plinthe en bas
    draw_rect(draw, ox, oy+28, 32, 4, (152, 120, 88))

def draw_sol_bois_fonce(draw, ox, oy):
    """Tile 42: Sol bois foncé"""
    base = (160, 128, 96)
    line = (136, 104, 72)
    draw_rect(draw, ox, oy, 32, 32, base)
    for y in range(0, 32, 8):
        draw_rect(draw, ox, oy+y, 32, 1, line)

def draw_mur_ext_fenetre(draw, ox, oy):
    """Tile 43: Mur extérieur avec fenêtre (pour vue extérieure maison)"""
    wall = (200, 184, 168)
    frame_c = (120, 88, 56)
    glass = (176, 216, 240)
    draw_rect(draw, ox, oy, 32, 32, wall)
    draw_rect(draw, ox+6, oy+6, 20, 16, frame_c)
    draw_rect(draw, ox+8, oy+8, 16, 12, glass)
    draw_rect(draw, ox+15, oy+8, 2, 12, frame_c)

def draw_table_ronde(draw, ox, oy):
    """Tile 44: Table"""
    top = (176, 144, 112)
    leg = (144, 112, 80)
    draw_rect(draw, ox+4, oy+4, 24, 20, top)
    draw_rect(draw, ox+4, oy+4, 24, 2, (192, 160, 128))
    draw_rect(draw, ox+14, oy+24, 4, 8, leg)

def draw_chaise(draw, ox, oy):
    """Tile 45: Chaise"""
    seat = (168, 136, 104)
    back = (144, 112, 80)
    draw_rect(draw, ox+8, oy+16, 16, 12, seat)
    draw_rect(draw, ox+8, oy+4, 16, 14, back)
    draw_rect(draw, ox+8, oy+28, 4, 4, (120, 88, 56))
    draw_rect(draw, ox+20, oy+28, 4, 4, (120, 88, 56))

def draw_poster(draw, ox, oy):
    """Tile 46: Poster sur le mur"""
    wall = (232, 224, 208)
    draw_rect(draw, ox, oy, 32, 32, wall)
    # Poster frame
    draw_rect(draw, ox+6, oy+4, 20, 16, (80, 80, 88))
    draw_rect(draw, ox+8, oy+6, 16, 12, (200, 80, 80))
    # Pokéball sur le poster
    draw_rect(draw, ox+12, oy+8, 8, 4, (240, 240, 240))
    draw_rect(draw, ox+12, oy+12, 8, 4, (200, 60, 60))
    # Plinthe
    draw_rect(draw, ox, oy+28, 32, 4, (152, 120, 88))

def draw_poubelle(draw, ox, oy):
    """Tile 47: Poubelle"""
    body = (128, 128, 136)
    lid = (144, 144, 152)
    # Base transparente
    draw_rect(draw, ox+10, oy+8, 12, 20, body)
    draw_rect(draw, ox+8, oy+6, 16, 4, lid)
    draw_rect(draw, ox+14, oy+4, 4, 4, (160, 160, 168))

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    tileset_path = os.path.join(project_dir, "assets", "sprites", "tilesets", "tileset_outdoor.png")

    img = Image.open(tileset_path)
    # Expand to 8 rows (256×256) to have room for indoor tiles
    new_img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    new_img.paste(img, (0, 0))
    draw = ImageDraw.Draw(new_img)

    # Row 3: Indoor basics (tiles 24-31)
    funcs_row3 = [draw_parquet, draw_mur, draw_comptoir, draw_machine_soin,
                  draw_etagere, draw_tapis_rouge, draw_carrelage, draw_mur_deco]
    for i, f in enumerate(funcs_row3):
        f(draw, i * TILE, 3 * TILE)

    # Row 4: Bedroom/Living (tiles 32-39)
    funcs_row4 = [draw_lit_tete, draw_lit_pied, draw_tv, draw_pc,
                  draw_plante, draw_escalier_up, draw_escalier_down, draw_paillasson]
    for i, f in enumerate(funcs_row4):
        f(draw, i * TILE, 4 * TILE)

    # Row 5: More indoor (tiles 40-47)
    funcs_row5 = [draw_porte, draw_fenetre_int, draw_sol_bois_fonce, draw_mur_ext_fenetre,
                  draw_table_ronde, draw_chaise, draw_poster, draw_poubelle]
    for i, f in enumerate(funcs_row5):
        f(draw, i * TILE, 5 * TILE)

    new_img.save(tileset_path)
    print(f"Tileset updated: {new_img.size}")

if __name__ == "__main__":
    main()
