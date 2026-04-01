extends Node
class_name SurfSystem

# SurfSystem — Gère le déplacement sur l'eau (CS03 Surf)
# Le joueur peut surfer si : badge Cascade obtenu + CS Surf obtenu + Pokémon connaissant Surf

# Vérifie si le joueur peut utiliser Surf
static func peut_surfer() -> bool:
	# Badge Cascade (index 1) requis
	if not GameManager.badges[1]:
		return false
	# Flag CS obtenu
	if not GameManager.get_flag("cs_surf_obtenu"):
		return false
	# Un Pokémon de l'équipe connaît Surf (ou possède la CS)
	return _equipe_connait_attaque("surf")

# Vérifie si une case est de l'eau (tile index 4)
static func est_case_eau(tilemap: TileMap, pos: Vector2i) -> bool:
	if tilemap == null:
		return false
	# Vérifier couche 0 (sol)
	var data := tilemap.get_cell_source_id(0, pos)
	if data < 0:
		return false
	var atlas_coords := tilemap.get_cell_atlas_coords(0, pos)
	# TILE_EAU = index 4 → atlas (4, 0)
	return atlas_coords == Vector2i(4, 0)

# Vérifier si l'équipe possède une attaque spécifique
static func _equipe_connait_attaque(attaque_id: String) -> bool:
	for poke in PlayerData.equipe:
		if poke.get("pv_actuels", 0) <= 0:
			continue
		for atk in poke.get("attaques", []):
			if atk.get("id", "") == attaque_id:
				return true
	# En mode simplifié : si le joueur a la CS dans l'inventaire, ça suffit
	if PlayerData.inventaire.has("cs03_surf"):
		return true
	return false
