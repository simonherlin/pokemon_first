extends Node
class_name StrengthSystem

# StrengthSystem — Gère les rochers poussables (CS04 Force)
# Les rochers peuvent être poussés d'une case dans la direction du joueur

# Vérifie si le joueur peut utiliser Force
static func peut_utiliser_force() -> bool:
	# Badge Arc-en-ciel (index 3) requis
	if not GameManager.badges[3]:
		return false
	if not GameManager.get_flag("cs_force_obtenu"):
		return false
	return _equipe_a_cs("cs04_force", "force")

# Vérifier si on peut pousser un rocher vers la position cible
static func case_libre_pour_rocher(carte_data: Dictionary, cible: Vector2i) -> bool:
	var largeur: int = carte_data.get("largeur", 20)
	var hauteur: int = carte_data.get("hauteur", 18)
	# Hors limites ?
	if cible.x < 0 or cible.x >= largeur or cible.y < 0 or cible.y >= hauteur:
		return false
	# Vérifier collision avec les tiles
	var tiles_sol: Array = carte_data.get("tiles_sol", [])
	var tiles_objets: Array = carte_data.get("tiles_objets", [])
	# Eau bloque
	if cible.y < tiles_sol.size():
		var row: Array = tiles_sol[cible.y]
		if cible.x < row.size() and row[cible.x] == 4:  # TILE_EAU
			return false
	# Mur/obstacle sur layer objets
	if cible.y < tiles_objets.size():
		var row: Array = tiles_objets[cible.y]
		if cible.x < row.size() and row[cible.x] >= 0:
			return false
	return true

static func _equipe_a_cs(item_id: String, attaque_id: String) -> bool:
	for poke in PlayerData.equipe:
		if poke.get("pv_actuels", 0) <= 0:
			continue
		for atk in poke.get("attaques", []):
			if atk.get("id", "") == attaque_id:
				return true
	if PlayerData.inventaire.has(item_id):
		return true
	return false
