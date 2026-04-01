extends Node
class_name FishingSystem

# FishingSystem — Gère la pêche (Canne, Super Canne, Méga Canne)
# Déclenche des combats aquatiques depuis les cases d'eau adjacentes

# Vérifie si le joueur a une canne
static func a_canne() -> bool:
	return PlayerData.inventaire.has("canne_a_peche") or \
		PlayerData.inventaire.has("super_canne") or \
		PlayerData.inventaire.has("mega_canne")

# Obtenir la meilleure canne disponible
static func meilleure_canne() -> String:
	if PlayerData.inventaire.has("mega_canne"):
		return "mega_canne"
	elif PlayerData.inventaire.has("super_canne"):
		return "super_canne"
	elif PlayerData.inventaire.has("canne_a_peche"):
		return "canne_a_peche"
	return ""

# Vérifie si la case devant le joueur est de l'eau
static func peut_pecher(tilemap: TileMap, position_grille: Vector2i, direction: Vector2i) -> bool:
	if not a_canne():
		return false
	var cible := position_grille + direction
	# Vérifier si la case est de l'eau
	if tilemap == null:
		return false
	var atlas_coords := tilemap.get_cell_atlas_coords(0, cible)
	return atlas_coords == Vector2i(4, 0)  # TILE_EAU

# Lancer la pêche — retourne les données du Pokémon pêché ou {} si rien mordu
static func pecher(zone_id: String) -> Dictionary:
	var canne := meilleure_canne()
	if canne.is_empty() or zone_id.is_empty():
		return {}
	
	# Charger les tables de rencontres
	var tables: Dictionary = EncounterSystem._tables
	var zone: Dictionary = tables.get(zone_id, {})
	if zone.is_empty():
		return {}
	
	var peche_table: Array = zone.get("peche", [])
	if peche_table.is_empty():
		return {}
	
	# Probabilité de morsure selon la canne
	var taux_morsure: float = 0.5  # 50% par défaut
	match canne:
		"canne_a_peche":
			taux_morsure = 0.5
		"super_canne":
			taux_morsure = 0.75
		"mega_canne":
			taux_morsure = 1.0
	
	if randf() > taux_morsure:
		return {}  # Rien n'a mordu
	
	# Tirage pondéré dans la table de pêche
	var total_taux := 0
	for entree in peche_table:
		total_taux += entree.get("taux", 10)
	
	var tirage := randi() % maxi(1, total_taux)
	var cumul := 0
	for entree in peche_table:
		cumul += entree.get("taux", 10)
		if tirage < cumul:
			return entree
	
	return peche_table[peche_table.size() - 1]

# Filtrer les Pokémon pêchés par niveau de canne
static func ajuster_niveau_peche(pokemon_data: Dictionary) -> Dictionary:
	var canne := meilleure_canne()
	var result := pokemon_data.duplicate()
	var niv_min: int = result.get("niveau_min", 5)
	var niv_max: int = result.get("niveau_max", 15)
	
	match canne:
		"canne_a_peche":
			# Canne basique : niveaux bas
			result["niveau_min"] = niv_min
			result["niveau_max"] = mini(niv_max, niv_min + 5)
		"super_canne":
			# Super Canne : niveaux moyens
			result["niveau_min"] = maxi(niv_min, int((niv_min + niv_max) / 2) - 3)
			result["niveau_max"] = niv_max
		"mega_canne":
			# Méga Canne : niveaux hauts
			result["niveau_min"] = maxi(niv_min, niv_max - 5)
			result["niveau_max"] = niv_max
	
	return result
