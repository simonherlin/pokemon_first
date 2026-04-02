extends Node

# TileSetBuilder — Crée le TileSet Godot 4 à partir de l'atlas tileset_outdoor.png
# Utilisé par MapScene pour construire les TileMaps au runtime

# --- Constantes ---
const TAILLE_TILE := 32
const COLONNES_ATLAS := 8

# Indices des tiles (correspondance avec l'atlas)
# Ligne 0 : Terrain de base
const TILE_HERBE := 0
const TILE_HERBE_HAUTE := 1
const TILE_CHEMIN := 2
const TILE_SABLE := 3
const TILE_EAU := 4
const TILE_FLEUR := 5
# Ligne 1 : Arbres et végétation
const TILE_ARBRE_HAUT := 8
const TILE_ARBRE_BAS := 9
const TILE_ARBRE_HAUT_R := 10
const TILE_ARBRE_BAS_R := 11
const TILE_FENCE_H := 12
const TILE_FENCE_V := 13
const TILE_BUISSON := 14
const TILE_HERBE_DETAIL := 15
# Ligne 2 : Maisons
const TILE_TOIT_G := 16
const TILE_TOIT_M := 17
const TILE_TOIT_D := 18
const TILE_MUR_G := 19
const TILE_MUR_M := 20
const TILE_MUR_D := 21
const TILE_PORTE := 22
const TILE_FENETRE := 23
# Ligne 3 : Intérieur
const TILE_SOL_INT := 24
const TILE_MUR_INT := 25
const TILE_COMPTOIR := 26
const TILE_MACHINE_SOIN := 27
const TILE_ETAGERE := 28
const TILE_TAPIS := 29
const TILE_SOL_CARRELAGE := 30
const TILE_MUR_MOTIF := 31

# Ligne 4 : Chambre / Salon
const TILE_LIT_TETE := 32
const TILE_LIT_PIED := 33
const TILE_TV := 34
const TILE_PC := 35
const TILE_PLANTE := 36
const TILE_ESCALIER_UP := 37
const TILE_ESCALIER_DOWN := 38
const TILE_PAILLASSON := 39

# Ligne 5 : Intérieur avancé
const TILE_PORTE_INT := 40
const TILE_FENETRE_INT := 41
const TILE_SOL_BOIS_FONCE := 42
const TILE_MUR_EXT_FENETRE := 43
const TILE_TABLE := 44
const TILE_CHAISE := 45
const TILE_POSTER := 46
const TILE_POUBELLE := 47

# --- Tiles avec collision (murs, obstacles, mobilier) ---
const TILES_COLLISION := [
	TILE_EAU, TILE_ARBRE_HAUT, TILE_ARBRE_BAS,
	TILE_ARBRE_HAUT_R, TILE_ARBRE_BAS_R,
	TILE_FENCE_H, TILE_FENCE_V, TILE_BUISSON,
	TILE_TOIT_G, TILE_TOIT_M, TILE_TOIT_D,
	TILE_MUR_G, TILE_MUR_M, TILE_MUR_D, TILE_FENETRE,
	TILE_MUR_INT, TILE_COMPTOIR, TILE_MACHINE_SOIN,
	TILE_ETAGERE, TILE_MUR_MOTIF,
	# Mobilier intérieur (bloquant)
	TILE_LIT_TETE, TILE_LIT_PIED, TILE_TV, TILE_PC,
	TILE_PLANTE, TILE_FENETRE_INT, TILE_MUR_EXT_FENETRE,
	TILE_TABLE, TILE_CHAISE, TILE_POSTER, TILE_POUBELLE
	# Note : TILE_ESCALIER_UP/DOWN, TILE_PORTE_INT, TILE_PAILLASSON = traversables (warps)
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
