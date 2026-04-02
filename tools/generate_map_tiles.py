#!/usr/bin/env python3
"""
Génère tiles_sol et tiles_objets pour toutes les cartes qui n'en ont pas.
Catégorise automatiquement chaque carte et génère un layout approprié.
"""

import json, os, random

random.seed(42)

DATA_DIR = "data/maps"

# Tile indices (matching tileset_builder.gd)
HERBE = 0; HERBE_HAUTE = 1; CHEMIN = 2; SABLE = 3; EAU = 4; FLEUR = 5
ARBRE_H = 8; ARBRE_B = 9; ARBRE_HR = 10; ARBRE_BR = 11
FENCE_H = 12; FENCE_V = 13; BUISSON = 14; HERBE_D = 15
TOIT_G = 16; TOIT_M = 17; TOIT_D = 18
MUR_G = 19; MUR_M = 20; MUR_D = 21; PORTE = 22; FENETRE = 23
SOL_INT = 24; MUR_INT = 25; COMPTOIR = 26; MACHINE = 27
ETAGERE = 28; TAPIS = 29; SOL_CARR = 30; MUR_MOTIF = 31
LIT_T = 32; LIT_P = 33; TV = 34; PC = 35
PLANTE = 36; ESC_UP = 37; ESC_DOWN = 38; PAILLASSON = 39
PORTE_INT = 40; FENETRE_INT = 41; SOL_BOIS = 42; MUR_EXT_F = 43
TABLE = 44; CHAISE = 45; POSTER = 46; POUBELLE = 47


def make_grid(w, h, fill=0):
    return [[fill]*w for _ in range(h)]


def make_empty_grid(w, h):
    return [[-1]*w for _ in range(h)]


# ── Générateurs par type de carte ──

def gen_centre_pokemon(w, h):
    """Centre Pokémon classique."""
    sol = make_grid(w, h, SOL_INT)
    obj = make_empty_grid(w, h)
    # Murs en haut
    for x in range(w):
        sol[0][x] = MUR_INT
        sol[1][x] = MUR_INT
    # Machine de soin en haut au centre
    cx = w // 2
    obj[1][cx] = MACHINE
    obj[1][cx-1] = COMPTOIR
    obj[1][cx+1] = COMPTOIR
    # Plantes décoratives
    obj[1][1] = PLANTE
    obj[1][w-2] = PLANTE
    # PC à gauche
    if w > 4:
        obj[1][2] = PC
    # Paillasson en bas au centre
    sol[h-1][cx] = PAILLASSON
    # Tapis central
    for y in range(3, h-1):
        sol[y][cx] = TAPIS
    return sol, obj


def gen_boutique(w, h):
    """Boutique Pokémon."""
    sol = make_grid(w, h, SOL_INT)
    obj = make_empty_grid(w, h)
    # Murs en haut
    for x in range(w):
        sol[0][x] = MUR_INT
        sol[1][x] = MUR_INT
    # Comptoir vendeur
    for x in range(2, w//2 + 2):
        obj[2][x] = COMPTOIR
    # Étagères à droite
    for y in range(2, h-2):
        obj[y][w-2] = ETAGERE
    # Paillasson
    sol[h-1][w//2] = PAILLASSON
    return sol, obj


def gen_arene(w, h):
    """Arène Pokémon."""
    sol = make_grid(w, h, SOL_CARR)
    obj = make_empty_grid(w, h)
    # Murs sur les bords
    for x in range(w):
        sol[0][x] = MUR_MOTIF
        sol[1][x] = MUR_INT
    for y in range(h):
        sol[y][0] = MUR_INT
        sol[y][w-1] = MUR_INT
    # Zone de combat au centre (tapis)
    cy, cx = h//2, w//2
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            ny, nx = cy+dy, cx+dx
            if 0 <= ny < h and 0 <= nx < w:
                sol[ny][nx] = TAPIS
    # Champion en haut au centre
    # Paillasson en bas
    sol[h-1][cx] = PAILLASSON
    # Statues
    obj[2][2] = PLANTE
    obj[2][w-3] = PLANTE
    return sol, obj


def gen_maison(w, h):
    """Petite maison / cabane."""
    sol = make_grid(w, h, SOL_BOIS)
    obj = make_empty_grid(w, h)
    # Murs en haut
    for x in range(w):
        sol[0][x] = MUR_INT
    # Meuble
    if w >= 6 and h >= 4:
        obj[1][1] = TV
        obj[1][w-2] = PC
        if h >= 5:
            obj[2][1] = TABLE
            obj[2][2] = CHAISE
    # Paillasson
    sol[h-1][w//2] = PAILLASSON
    return sol, obj


def gen_grotte(w, h):
    """Grotte / caverne."""
    # Murs de grotte partout, sol de grotte au milieu
    sol = make_grid(w, h, SOL_CARR)  # sol grotte = 30 (réutilise sol_carrelage gris)
    obj = make_empty_grid(w, h)
    
    # Utiliser MUR_MOTIF (31) pour les murs de grotte
    # Bordure
    for x in range(w):
        sol[0][x] = MUR_MOTIF
        sol[h-1][x] = MUR_MOTIF
    for y in range(h):
        sol[y][0] = MUR_MOTIF
        sol[y][w-1] = MUR_MOTIF
    
    # Intérieur = sol de grotte (on utilise SOL_INT varié)
    for y in range(1, h-1):
        for x in range(1, w-1):
            sol[y][x] = SOL_INT
    
    # Quelques rochers aléatoires
    random.seed(hash(f"grotte_{w}_{h}") & 0xFFFFFFFF)
    for _ in range(w * h // 20):
        rx = random.randint(2, w-3)
        ry = random.randint(2, h-3)
        obj[ry][rx] = BUISSON  # obstacle
    
    return sol, obj


def gen_route(w, h, map_id=""):
    """Route extérieure."""
    sol = make_grid(w, h, HERBE)
    obj = make_empty_grid(w, h)
    
    random.seed(hash(f"route_{map_id}") & 0xFFFFFFFF)
    
    is_water_route = "19" in map_id or "20" in map_id or "21" in map_id or "surf" in map_id
    is_cycling = "17" in map_id
    
    if is_water_route:
        # Route maritime
        sol = make_grid(w, h, EAU)
        # Chemin au milieu
        mid = w // 2
        for y in range(h):
            for dx in range(-1, 2):
                nx = mid + dx
                if 0 <= nx < w:
                    sol[y][nx] = CHEMIN
        return sol, obj
    
    # Route terrestre standard
    # Arbres sur les bords
    for y in range(0, h, 2):
        if y+1 < h:
            obj[y][0] = ARBRE_H
            obj[y+1][0] = ARBRE_B
            obj[y][w-1] = ARBRE_HR
            obj[y+1][w-1] = ARBRE_BR
    
    # Chemin au milieu (vertical ou horizontal selon les dimensions)
    if h > w:  # route verticale
        mid = w // 2
        for y in range(h):
            for dx in range(-1, 2):
                nx = mid + dx
                if 0 <= nx < w:
                    sol[y][nx] = CHEMIN
    else:  # route horizontale
        mid = h // 2
        for x in range(w):
            for dy in range(-1, 2):
                ny = mid + dy
                if 0 <= ny < h:
                    sol[ny][x] = CHEMIN
    
    # Hautes herbes aléatoires
    for _ in range(w * h // 10):
        rx = random.randint(1, w-2)
        ry = random.randint(1, h-2)
        if sol[ry][rx] == HERBE and obj[ry][rx] == -1:
            sol[ry][rx] = HERBE_HAUTE
    
    # Fleurs
    for _ in range(w * h // 30):
        rx = random.randint(1, w-2)
        ry = random.randint(1, h-2)
        if sol[ry][rx] == HERBE and obj[ry][rx] == -1:
            sol[ry][rx] = FLEUR
    
    return sol, obj


def gen_ville(w, h, map_id=""):
    """Ville extérieure avec bâtiments."""
    sol = make_grid(w, h, HERBE)
    obj = make_empty_grid(w, h)
    
    random.seed(hash(f"ville_{map_id}") & 0xFFFFFFFF)
    
    # Routes principales
    mid_h = h // 2
    mid_w = w // 2
    
    # Route horizontale
    for x in range(w):
        for dy in [-1, 0, 1]:
            ny = mid_h + dy
            if 0 <= ny < h:
                sol[ny][x] = CHEMIN
    
    # Route verticale
    for y in range(h):
        for dx in [-1, 0, 1]:
            nx = mid_w + dx
            if 0 <= nx < w:
                sol[y][nx] = CHEMIN
    
    # Bâtiments (3 tuiles de large: toit_g, toit_m, toit_d en haut, murs en bas)
    buildings = []
    for _ in range(min(6, w * h // 40)):
        bx = random.randint(1, w-5)
        by = random.randint(1, h-5)
        # Vérifier pas de chevauchement
        ok = True
        for bb in buildings:
            if abs(bx - bb[0]) < 5 and abs(by - bb[1]) < 4:
                ok = False
                break
        # Pas sur le chemin principal
        if abs(by - mid_h) <= 2 or abs(bx - mid_w) <= 2:
            ok = False
        
        if ok:
            buildings.append((bx, by))
            # Toit
            obj[by][bx] = TOIT_G
            obj[by][bx+1] = TOIT_M
            obj[by][bx+2] = TOIT_D
            # Mur
            obj[by+1][bx] = MUR_G
            obj[by+1][bx+1] = FENETRE
            obj[by+1][bx+2] = MUR_D
            # Porte
            sol[by+2][bx+1] = PORTE
    
    # Arbres décoratifs
    for y in range(0, h, 2):
        if y+1 < h and obj[y][0] == -1 and obj[y+1][0] == -1:
            obj[y][0] = ARBRE_H
            obj[y+1][0] = ARBRE_B
        if y+1 < h and obj[y][w-1] == -1 and obj[y+1][w-1] == -1:
            obj[y][w-1] = ARBRE_HR
            obj[y+1][w-1] = ARBRE_BR
    
    # Fleurs
    for _ in range(w * h // 20):
        rx = random.randint(1, w-2)
        ry = random.randint(1, h-2)
        if sol[ry][rx] == HERBE and obj[ry][rx] == -1:
            sol[ry][rx] = FLEUR
    
    return sol, obj


def gen_safari(w, h, map_id=""):
    """Zone de parc safari."""
    sol = make_grid(w, h, HERBE)
    obj = make_empty_grid(w, h)
    
    random.seed(hash(f"safari_{map_id}") & 0xFFFFFFFF)
    
    # Beaucoup d'herbe haute
    for y in range(h):
        for x in range(w):
            r = random.random()
            if r < 0.25:
                sol[y][x] = HERBE_HAUTE
            elif r < 0.05:
                sol[y][x] = FLEUR
    
    # Chemin serpentin
    px = w // 2
    for y in range(h):
        px += random.randint(-1, 1)
        px = max(1, min(w-2, px))
        for dx in range(-1, 2):
            nx = px + dx
            if 0 <= nx < w:
                sol[y][nx] = CHEMIN
    
    # Un peu d'eau
    wx = random.randint(2, w-4)
    wy = random.randint(2, h-4)
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            ny, nx = wy+dy, wx+dx
            if 0 <= ny < h and 0 <= nx < w:
                sol[ny][nx] = EAU
    
    # Clôtures en bordure
    for x in range(w):
        obj[0][x] = FENCE_H
        obj[h-1][x] = FENCE_H
    
    return sol, obj


def gen_tour_sylphe(w, h, floor=""):
    """Étage de la Tour Sylphe (bureau)."""
    sol = make_grid(w, h, SOL_CARR)
    obj = make_empty_grid(w, h)
    
    # Murs
    for x in range(w):
        sol[0][x] = MUR_INT
    for y in range(h):
        sol[y][0] = MUR_INT
        sol[y][w-1] = MUR_INT
    
    # Tables et chaises de bureau
    random.seed(hash(f"sylphe_{floor}") & 0xFFFFFFFF)
    for _ in range(w * h // 15):
        rx = random.randint(2, w-3)
        ry = random.randint(2, h-3)
        if obj[ry][rx] == -1:
            obj[ry][rx] = TABLE
    
    # Escalier montant/descendant
    obj[1][1] = ESC_UP
    obj[1][w-2] = ESC_DOWN
    
    # Plantes décoratives
    obj[1][w//2] = PLANTE
    
    return sol, obj


def gen_repaire_rocket(w, h, floor=""):
    """Repaire Rocket souterrain."""
    sol = make_grid(w, h, SOL_CARR)
    obj = make_empty_grid(w, h)
    
    # Murs sombres
    for x in range(w):
        sol[0][x] = MUR_MOTIF
    for y in range(h):
        sol[y][0] = MUR_MOTIF
        sol[y][w-1] = MUR_MOTIF
    
    # Sol intérieur
    for y in range(1, h):
        for x in range(1, w-1):
            sol[y][x] = SOL_CARR
    
    # Escaliers
    obj[1][1] = ESC_UP
    if floor != "b4f":
        obj[1][w-2] = ESC_DOWN
    
    return sol, obj


def gen_manoir(w, h, floor=""):
    """Manoir Pokémon (intérieur sombre)."""
    sol = make_grid(w, h, SOL_BOIS)
    obj = make_empty_grid(w, h)
    
    # Murs
    for x in range(w):
        sol[0][x] = MUR_MOTIF
    for y in range(h):
        sol[y][0] = MUR_MOTIF
        sol[y][w-1] = MUR_MOTIF
    
    random.seed(hash(f"manoir_{floor}") & 0xFFFFFFFF)
    
    # Mobilier cassé épars
    for _ in range(w * h // 20):
        rx = random.randint(2, w-3)
        ry = random.randint(2, h-3)
        if obj[ry][rx] == -1:
            item = random.choice([TABLE, POUBELLE, PLANTE])
            obj[ry][rx] = item
    
    # Escaliers
    obj[1][1] = ESC_UP
    if "b1f" not in floor:
        obj[1][w-2] = ESC_DOWN
    
    return sol, obj


def gen_ligue(w, h, map_id=""):
    """Salle de la Ligue Pokémon."""
    sol = make_grid(w, h, SOL_CARR)
    obj = make_empty_grid(w, h)
    
    # Murs
    for x in range(w):
        sol[0][x] = MUR_MOTIF
        sol[1][x] = MUR_INT
    for y in range(h):
        sol[y][0] = MUR_INT
        sol[y][w-1] = MUR_INT
    
    # Tapis rouge central menant au champion
    cx = w // 2
    for y in range(2, h-1):
        sol[y][cx] = TAPIS
    
    # Statues
    obj[2][2] = PLANTE
    obj[2][w-3] = PLANTE
    
    # Paillasson entrée/sortie
    sol[h-1][cx] = PAILLASSON
    sol[2][cx] = PORTE_INT
    
    return sol, obj


def gen_grand_magasin(w, h, floor=""):
    """Grand magasin de Céladopole."""
    sol = make_grid(w, h, SOL_CARR)
    obj = make_empty_grid(w, h)
    
    # Murs
    for x in range(w):
        sol[0][x] = MUR_INT
    
    # Comptoirs vendeurs
    for x in range(2, w//2):
        obj[2][x] = COMPTOIR
    
    # Étagères
    for y in range(4, h-2, 2):
        for x in range(w//2 + 1, w-2):
            obj[y][x] = ETAGERE
    
    # Escalier
    obj[1][w-2] = ESC_UP if floor == "1f" else ESC_DOWN
    obj[1][1] = ESC_DOWN if floor == "2f" else ESC_UP
    
    return sol, obj


def gen_casino(w, h):
    """Casino de Céladopole."""
    sol = make_grid(w, h, SOL_CARR)
    obj = make_empty_grid(w, h)
    
    # Murs
    for x in range(w):
        sol[0][x] = MUR_MOTIF
    
    # Rangées de machines (tables)
    for y in range(3, h-2, 2):
        for x in range(2, w-2, 3):
            obj[y][x] = TABLE
    
    # Comptoir en fond
    for x in range(2, w//2):
        obj[1][x] = COMPTOIR
    
    # Paillasson
    sol[h-1][w//2] = PAILLASSON
    
    return sol, obj


def gen_safari_entree(w, h):
    """Entrée du parc safari."""
    sol = make_grid(w, h, SOL_INT)
    obj = make_empty_grid(w, h)
    for x in range(w):
        sol[0][x] = MUR_INT
    obj[1][w//2] = COMPTOIR
    sol[h-1][w//2] = PAILLASSON
    return sol, obj


def gen_labo_fossiles(w, h):
    """Laboratoire fossiles de Cramois'Île."""
    sol = make_grid(w, h, SOL_CARR)
    obj = make_empty_grid(w, h)
    for x in range(w):
        sol[0][x] = MUR_INT
    # Machines de recherche
    obj[1][2] = MACHINE
    obj[1][3] = PC
    obj[1][w-3] = PC
    obj[1][w-2] = MACHINE
    # Tables
    for x in range(3, w-3):
        obj[3][x] = TABLE
    sol[h-1][w//2] = PAILLASSON
    return sol, obj


def gen_dojo(w, h):
    """Dojo de combat."""
    sol = make_grid(w, h, SOL_BOIS)
    obj = make_empty_grid(w, h)
    for x in range(w):
        sol[0][x] = MUR_MOTIF
    for y in range(h):
        sol[y][0] = MUR_MOTIF
        sol[y][w-1] = MUR_MOTIF
    # Tapis central
    cy, cx = h//2, w//2
    for dy in range(-2, 3):
        for dx in range(-3, 4):
            ny, nx = cy+dy, cx+dx
            if 0 < ny < h and 0 < nx < w-1:
                sol[ny][nx] = TAPIS
    sol[h-1][cx] = PAILLASSON
    return sol, obj


def gen_centrale(w, h):
    """Centrale électrique."""
    sol = make_grid(w, h, SOL_CARR)
    obj = make_empty_grid(w, h)
    for x in range(w):
        sol[0][x] = MUR_MOTIF
    for y in range(h):
        sol[y][0] = MUR_MOTIF
        sol[y][w-1] = MUR_MOTIF
    # Machines
    random.seed(42)
    for _ in range(w * h // 12):
        rx = random.randint(2, w-3)
        ry = random.randint(2, h-3)
        if obj[ry][rx] == -1:
            obj[ry][rx] = random.choice([MACHINE, PC, TABLE])
    return sol, obj


def gen_route_victoire(w, h, floor=""):
    """Route victoire (grotte)."""
    return gen_grotte(w, h)


# ── Catégorisation et exécution ──

def categorize_and_generate(map_id, data):
    """Catégorise une carte et génère ses tiles."""
    w = data.get("largeur", 20)
    h = data.get("hauteur", 18)
    
    if "centre_pokemon" in map_id:
        return gen_centre_pokemon(w, h)
    elif "boutique" in map_id:
        return gen_boutique(w, h)
    elif "arene_" in map_id:
        return gen_arene(w, h)
    elif "ligue_" in map_id:
        return gen_ligue(w, h, map_id)
    elif "tour_sylphe" in map_id:
        floor = map_id.split("_")[-1]
        return gen_tour_sylphe(w, h, floor)
    elif "repaire_rocket" in map_id:
        floor = map_id.split("_")[-1]
        return gen_repaire_rocket(w, h, floor)
    elif "manoir_pokemon" in map_id:
        floor = map_id.split("_")[-1]
        return gen_manoir(w, h, floor)
    elif "grotte_inconnue" in map_id or "iles_ecume" in map_id:
        return gen_grotte(w, h)
    elif "route_victoire" in map_id:
        floor = map_id.split("_")[-1]
        return gen_route_victoire(w, h, floor)
    elif "parc_safari_entree" in map_id:
        return gen_safari_entree(w, h)
    elif "parc_safari_zone" in map_id:
        return gen_safari(w, h, map_id)
    elif "grand_magasin" in map_id:
        floor = map_id.split("_")[-1]
        return gen_grand_magasin(w, h, floor)
    elif "casino" in map_id:
        return gen_casino(w, h)
    elif "dojo_combat" in map_id:
        return gen_dojo(w, h)
    elif "centrale" in map_id:
        return gen_centrale(w, h)
    elif "labo_fossiles" in map_id:
        return gen_labo_fossiles(w, h)
    elif map_id.startswith("route_"):
        return gen_route(w, h, map_id)
    elif any(v in map_id for v in ["celadopole", "cramoisile", "parmanie", "safrania", "plateau_indigo"]):
        return gen_ville(w, h, map_id)
    elif any(v in map_id for v in ["maison_", "cabane_", "sevii_ile"]) and any(v in map_id for v in ["maison", "boutique", "centre"]):
        if "boutique" in map_id:
            return gen_boutique(w, h)
        elif "centre_pokemon" in map_id:
            return gen_centre_pokemon(w, h)
        return gen_maison(w, h)
    elif any(v in map_id for v in ["maison", "cabane"]):
        return gen_maison(w, h)
    elif "sevii" in map_id:
        if "grotte" in map_id or "foret" in map_id:
            return gen_grotte(w, h)
        elif "route" in map_id:
            return gen_route(w, h, map_id)
        else:
            return gen_ville(w, h, map_id)
    else:
        # Fallback : sol intérieur basique
        return gen_maison(w, h)


def main():
    updated = 0
    for f in sorted(os.listdir(DATA_DIR)):
        if not f.endswith(".json"):
            continue
        path = os.path.join(DATA_DIR, f)
        data = json.loads(open(path, "r", encoding="utf-8").read())
        
        if data.get("tiles_sol"):
            continue  # Already has tiles
        
        map_id = f.replace(".json", "")
        w = data.get("largeur", 20)
        h = data.get("hauteur", 18)
        
        if w == 0 or h == 0:
            print(f"  ⚠ {map_id} — dimensions 0, skip")
            continue
        
        sol, obj = categorize_and_generate(map_id, data)
        data["tiles_sol"] = sol
        data["tiles_objets"] = obj
        
        with open(path, "w", encoding="utf-8") as fout:
            json.dump(data, fout, indent=2, ensure_ascii=False)
        
        updated += 1
        print(f"  ✓ {map_id} ({w}×{h})")
    
    print(f"\n{updated} cartes mises à jour avec tiles_sol/tiles_objets.")


if __name__ == "__main__":
    main()
