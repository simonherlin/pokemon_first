extends Node

# TileSetBuilder — Crée le TileSet Godot 4 à partir de l'atlas tileset_outdoor.png
# Utilisé par MapScene pour construire les TileMaps au runtime
# Version RFVF : tileset 16 colonnes × 16 lignes = 256 tiles à 32×32px

# --- Constantes ---
const TAILLE_TILE := 32
const COLONNES_ATLAS := 16

# ===== INDICES DES TILES (correspondance atlas 16 colonnes) =====

# --- Ligne 0 : Sols extérieurs ---
const TILE_HERBE := 0
const TILE_HERBE_VARIANTE := 1
const TILE_HERBE_FLEURS := 2
const TILE_HERBE_HAUTE := 3
const TILE_CHEMIN := 4
const TILE_CHEMIN_BORD_HAUT := 5
const TILE_CHEMIN_BORD_BAS := 6
const TILE_CHEMIN_BORD_GAUCHE := 7
const TILE_CHEMIN_BORD_DROIT := 8
const TILE_CHEMIN_COIN_HG := 9
const TILE_CHEMIN_COIN_HD := 10
const TILE_CHEMIN_COIN_BG := 11
const TILE_CHEMIN_COIN_BD := 12
const TILE_CHEMIN_COIN_INT_HG := 13
const TILE_CHEMIN_COIN_INT_HD := 14
const TILE_SABLE := 15

# --- Ligne 1 : Eau et rivages ---
const TILE_EAU := 16
const TILE_EAU_RIVAGE_HAUT := 17
const TILE_EAU_RIVAGE_BAS := 18
const TILE_EAU_RIVAGE_GAUCHE := 19
const TILE_EAU_RIVAGE_DROIT := 20
const TILE_EAU_COIN_HG := 21
const TILE_EAU_COIN_HD := 22
const TILE_EAU_COIN_BG := 23
const TILE_EAU_COIN_BD := 24
const TILE_EAU_COIN_INT_HG := 25
const TILE_EAU_COIN_INT_HD := 26
const TILE_EAU_COIN_INT_BG := 27
const TILE_EAU_COIN_INT_BD := 28
const TILE_CHEMIN_COIN_INT_BG := 29
const TILE_CHEMIN_COIN_INT_BD := 30
const TILE_RESERVE := 31

# --- Ligne 2 : Arbres, végétation, obstacles ---
const TILE_ARBRE_HG := 32
const TILE_ARBRE_HD := 33
const TILE_ARBRE_BG := 34
const TILE_ARBRE_BD := 35
const TILE_BUISSON := 36
const TILE_PETIT_ARBRE := 37
const TILE_ROCHER := 38
const TILE_CLOTURE_H := 39
const TILE_CLOTURE_V := 40
const TILE_PANNEAU := 41
const TILE_BOITE_LETTRES := 42
const TILE_REBORD_HAUT := 43
const TILE_REBORD_GAUCHE := 44
const TILE_REBORD_DROIT := 45
const TILE_SOUCHE := 46
const TILE_HERBE_RESERVE := 47

# --- Ligne 3 : Maisons toit rouge ---
const TILE_MAISON_TOIT_HG := 48
const TILE_MAISON_TOIT_HM := 49
const TILE_MAISON_TOIT_HD := 50
const TILE_MAISON_TOIT_BG := 51
const TILE_MAISON_TOIT_BM := 52
const TILE_MAISON_TOIT_BD := 53
const TILE_MAISON_MUR_G := 54
const TILE_MAISON_MUR_M := 55
const TILE_MAISON_MUR_D := 56
const TILE_MAISON_FENETRE := 57
const TILE_MAISON_PORTE := 58

# --- Ligne 4 : Labo Chen (toit bleu) ---
const TILE_LABO_TOIT_HG := 64
const TILE_LABO_TOIT_HM := 65
const TILE_LABO_TOIT_HD := 66
const TILE_LABO_TOIT_BG := 67
const TILE_LABO_TOIT_BM := 68
const TILE_LABO_TOIT_BD := 69
const TILE_LABO_MUR_G := 70
const TILE_LABO_MUR_M := 71
const TILE_LABO_MUR_D := 72
const TILE_LABO_FENETRE := 73
const TILE_LABO_PORTE := 74

# --- Ligne 5 : Centre Pokémon + Boutique ---
const TILE_CENTRE_TOIT_G := 80
const TILE_CENTRE_TOIT_M := 81
const TILE_CENTRE_TOIT_D := 82
const TILE_CENTRE_MUR_G := 83
const TILE_CENTRE_PORTE := 84
const TILE_CENTRE_MUR_D := 85
const TILE_BOUTIQUE_TOIT_G := 86
const TILE_BOUTIQUE_TOIT_M := 87
const TILE_BOUTIQUE_TOIT_D := 88
const TILE_BOUTIQUE_MUR_G := 89
const TILE_BOUTIQUE_PORTE := 90
const TILE_BOUTIQUE_MUR_D := 91
const TILE_ARENE_SOL := 92
const TILE_ARENE_STATUE := 93

# --- Ligne 6 : Intérieur base ---
const TILE_SOL_INT := 96
const TILE_MUR_INT := 97
const TILE_COMPTOIR := 98
const TILE_MACHINE_SOIN := 99
const TILE_ETAGERE := 100
const TILE_TAPIS := 101
const TILE_SOL_CARRELAGE := 102
const TILE_MUR_MOTIF := 103
const TILE_LIT_TETE := 104
const TILE_LIT_PIED := 105
const TILE_TV := 106
const TILE_PC := 107
const TILE_PLANTE := 108
const TILE_ESCALIER_UP := 109
const TILE_ESCALIER_DOWN := 110
const TILE_PAILLASSON := 111

# --- Ligne 7 : Intérieur avancé ---
const TILE_PORTE_INT := 112
const TILE_FENETRE_INT := 113
const TILE_SOL_BOIS_FONCE := 114
const TILE_MUR_EXT_FENETRE := 115
const TILE_TABLE := 116
const TILE_CHAISE := 117
const TILE_POSTER := 118
const TILE_POUBELLE := 119
const TILE_CARRELAGE_MOTIF := 120
const TILE_NOIR := 121
const TILE_VIDE := 122

# Alias de compatibilité (ancien → nouveau)
const TILE_FLEUR := 2            # herbe_fleurs
const TILE_PORTE := 58           # maison_porte
const TILE_FENETRE := 57         # maison_fenetre
const TILE_ARBRE_HAUT := 32      # arbre_hg (compatibilité)
const TILE_ARBRE_BAS := 34       # arbre_bg
const TILE_ARBRE_HAUT_R := 33    # arbre_hd
const TILE_ARBRE_BAS_R := 35     # arbre_bd
const TILE_FENCE_H := 39         # cloture_h
const TILE_FENCE_V := 40         # cloture_v
const TILE_HERBE_DETAIL := 1     # herbe_variante
const TILE_TOIT_G := 48          # maison_toit_hg
const TILE_TOIT_M := 49          # maison_toit_hm
const TILE_TOIT_D := 50          # maison_toit_hd
const TILE_MUR_G := 54           # maison_mur_g
const TILE_MUR_M := 55           # maison_mur_m
const TILE_MUR_D := 56           # maison_mur_d

# --- Tiles avec collision ---
const TILES_COLLISION := [
	# Eau
	TILE_EAU,
	# Arbres (4 quadrants)
	TILE_ARBRE_HG, TILE_ARBRE_HD, TILE_ARBRE_BG, TILE_ARBRE_BD,
	# Obstacles extérieurs
	TILE_BUISSON, TILE_PETIT_ARBRE, TILE_ROCHER,
	TILE_CLOTURE_H, TILE_CLOTURE_V, TILE_PANNEAU, TILE_BOITE_LETTRES,
	# Rebords (sautables vers le bas seulement — pour l'instant bloquant)
	TILE_REBORD_HAUT,
	# Toits maisons rouges
	TILE_MAISON_TOIT_HG, TILE_MAISON_TOIT_HM, TILE_MAISON_TOIT_HD,
	TILE_MAISON_TOIT_BG, TILE_MAISON_TOIT_BM, TILE_MAISON_TOIT_BD,
	# Murs maisons (pas les portes)
	TILE_MAISON_MUR_G, TILE_MAISON_MUR_M, TILE_MAISON_MUR_D, TILE_MAISON_FENETRE,
	# Toits labo
	TILE_LABO_TOIT_HG, TILE_LABO_TOIT_HM, TILE_LABO_TOIT_HD,
	TILE_LABO_TOIT_BG, TILE_LABO_TOIT_BM, TILE_LABO_TOIT_BD,
	# Murs labo
	TILE_LABO_MUR_G, TILE_LABO_MUR_M, TILE_LABO_MUR_D, TILE_LABO_FENETRE,
	# Centre Pokémon toits et murs
	TILE_CENTRE_TOIT_G, TILE_CENTRE_TOIT_M, TILE_CENTRE_TOIT_D,
	TILE_CENTRE_MUR_G, TILE_CENTRE_MUR_D,
	# Boutique toits et murs
	TILE_BOUTIQUE_TOIT_G, TILE_BOUTIQUE_TOIT_M, TILE_BOUTIQUE_TOIT_D,
	TILE_BOUTIQUE_MUR_G, TILE_BOUTIQUE_MUR_D,
	# Mobilier intérieur (bloquant)
	TILE_MUR_INT, TILE_COMPTOIR, TILE_MACHINE_SOIN,
	TILE_ETAGERE, TILE_MUR_MOTIF,
	TILE_LIT_TETE, TILE_LIT_PIED, TILE_TV, TILE_PC,
	TILE_PLANTE, TILE_FENETRE_INT, TILE_MUR_EXT_FENETRE,
	TILE_TABLE, TILE_CHAISE, TILE_POSTER, TILE_POUBELLE,
	TILE_ARENE_STATUE,
	# Note : Portes, escaliers, paillasson = traversables (warps ou libre)
]

# --- Cache ---
var _tileset: TileSet = null

func _ready() -> void:
	_construire_tileset()

func get_tileset() -> TileSet:
	if _tileset == null:
		_construire_tileset()
	return _tileset

func _construire_tileset() -> void:
	_tileset = TileSet.new()
	_tileset.tile_size = Vector2i(TAILLE_TILE, TAILLE_TILE)
	
	# Ajouter une couche physique pour les collisions
	_tileset.add_physics_layer()
	_tileset.set_physics_layer_collision_layer(0, 1)
	_tileset.set_physics_layer_collision_mask(0, 1)
	
	# Charger la texture de l'atlas
	var texture := load("res://assets/sprites/tilesets/tileset_outdoor.png") as Texture2D
	if texture == null:
		push_error("TileSetBuilder: impossible de charger tileset_outdoor.png")
		return
	
	# Créer la source atlas
	var atlas_source := TileSetAtlasSource.new()
	atlas_source.texture = texture
	atlas_source.texture_region_size = Vector2i(TAILLE_TILE, TAILLE_TILE)
	
	# Ajouter la source au TileSet AVANT de créer les tiles,
	# sinon les tile_data ne connaissent pas la couche physique
	var source_id := _tileset.add_source(atlas_source)
	
	# Calculer le nombre de lignes
	var nb_colonnes := texture.get_width() / TAILLE_TILE
	var nb_lignes := texture.get_height() / TAILLE_TILE
	
	# Créer chaque tile dans l'atlas
	for row in range(nb_lignes):
		for col in range(nb_colonnes):
			var atlas_coords := Vector2i(col, row)
			atlas_source.create_tile(atlas_coords)
			
			# Ajouter la collision si nécessaire
			var tile_index := row * COLONNES_ATLAS + col
			if tile_index in TILES_COLLISION:
				var tile_data := atlas_source.get_tile_data(atlas_coords, 0)
				# Polygone de collision centré (coordonnées relatives au centre du tile)
				var half := TAILLE_TILE / 2.0
				var polygon := PackedVector2Array([
					Vector2(-half, -half),
					Vector2(half, -half),
					Vector2(half, half),
					Vector2(-half, half)
				])
				tile_data.add_collision_polygon(0)
				tile_data.set_collision_polygon_points(0, 0, polygon)
	# Le source_id devrait être 0
	if source_id != 0:
		push_warning("TileSetBuilder: source_id = %d (attendu 0)" % source_id)

# Convertir un index de tile (0-31) en coordonnées atlas (col, row)
static func tile_index_to_atlas(index: int) -> Vector2i:
	return Vector2i(index % COLONNES_ATLAS, index / COLONNES_ATLAS)

# Peindre une carte entière sur un TileMap à partir des données JSON
func peindre_carte(tilemap: TileMap, carte_data: Dictionary) -> void:
	# Assigner le TileSet
	tilemap.tile_set = get_tileset()
	
	# Couche 0 = sol (terrain de base)
	# Couche 1 = obstacles/décorations (arbres, maisons, etc.)
	# S'assurer qu'on a 2 couches (Godot 4 crée layer 0 par défaut)
	while tilemap.get_layers_count() < 2:
		tilemap.add_layer(-1)
	
	tilemap.set_layer_name(0, "sol")
	tilemap.set_layer_name(1, "objets")
	
	var largeur: int = carte_data.get("largeur", 20)
	var hauteur: int = carte_data.get("hauteur", 18)
	
	# Couche sol (depuis les données tiles)
	var tiles_sol: Array = carte_data.get("tiles_sol", [])
	for y in range(mini(hauteur, tiles_sol.size())):
		var row: Array = tiles_sol[y] if y < tiles_sol.size() else []
		for x in range(largeur):
			var tile_idx: int = row[x] if x < row.size() else TILE_HERBE
			var atlas_coords := tile_index_to_atlas(tile_idx)
			tilemap.set_cell(0, Vector2i(x, y), 0, atlas_coords)
	
	# Couche objets/décorations
	var tiles_objets: Array = carte_data.get("tiles_objets", [])
	for y in range(mini(hauteur, tiles_objets.size())):
		var row: Array = tiles_objets[y] if y < tiles_objets.size() else []
		for x in range(largeur):
			var tile_idx: int = row[x] if x < row.size() else -1
			if tile_idx >= 0:
				var atlas_coords := tile_index_to_atlas(tile_idx)
				tilemap.set_cell(1, Vector2i(x, y), 0, atlas_coords)
