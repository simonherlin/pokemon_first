extends Node
class_name FlySystem

# FlySystem — Gère le voyage rapide par Vol (CS02)
# Permet au joueur de se téléporter dans une ville déjà visitée

# Destinations de vol disponibles (id_carte → données)
const DESTINATIONS := {
	"bourg_palette": {"nom": "Bourg Palette", "x": 7, "y": 12},
	"jadielle_ville": {"nom": "Jadielle", "x": 10, "y": 8},
	"argenta_ville": {"nom": "Argenta", "x": 10, "y": 8},
	"azuria_ville": {"nom": "Azuria", "x": 10, "y": 10},
	"carmin_sur_mer": {"nom": "Carmin-sur-Mer", "x": 10, "y": 8},
	"celadopole": {"nom": "Céladopole", "x": 10, "y": 10},
	"safrania": {"nom": "Safrania", "x": 10, "y": 10},
	"lavanville": {"nom": "Lavanville", "x": 10, "y": 8},
	"parmanie": {"nom": "Parmanie", "x": 10, "y": 10},
	"cramoisile": {"nom": "Cramois'Île", "x": 8, "y": 8},
	"plateau_indigo": {"nom": "Plateau Indigo", "x": 8, "y": 8}
}

# Vérifie si le joueur peut utiliser Vol
static func peut_voler() -> bool:
	# Badge Foudre (index 2) requis pour Vol en RFVF... mais en Gen 1 c'est badge Terre
	# On utilise le badge Foudre (index 2) comme dans RFVF
	if not GameManager.badges[2]:
		return false
	if not GameManager.get_flag("cs_vol_obtenu"):
		return false
	# Un Pokémon connaît Vol ou le joueur a la CS
	return _equipe_connait_attaque("vol") or PlayerData.inventaire.has("cs02_vol")

# Obtenir la liste des destinations débloquées (villes visitées)
static func get_destinations_disponibles() -> Array:
	var result: Array = []
	for carte_id in DESTINATIONS:
		# Le joueur y est allé si la carte apparaît dans ses données
		# On utilise un test simplifié : centre pokémon visité ou flag ville
		if _ville_visitee(carte_id):
			var d: Dictionary = DESTINATIONS[carte_id].duplicate()
			d["carte_id"] = carte_id
			result.append(d)
	return result

# Voler vers une destination
static func voler_vers(carte_id: String) -> void:
	if not carte_id in DESTINATIONS:
		return
	var dest: Dictionary = DESTINATIONS[carte_id]
	PlayerData.sauvegarder_position(carte_id, dest["x"], dest["y"], "bas")
	AudioManager.jouer_sfx("res://assets/audio/sfx/fly.ogg")
	SceneManager.charger_scene("res://scenes/maps/%s.tscn" % carte_id, {
		"carte_id": carte_id
	})

static func _ville_visitee(carte_id: String) -> bool:
	# On considère Bourg Palette toujours débloqué
	if carte_id == "bourg_palette":
		return true
	# Sinon, on vérifie si le joueur a une infirmière de la ville dans les flags
	# ou s'il a simplement visité la zone (simplifié : flag existe OU dresseur battu dans la zone)
	match carte_id:
		"jadielle_ville":
			return GameManager.get_flag("vieil_homme_vu") or GameManager.get_flag("badge_terre")
		"argenta_ville":
			return GameManager.get_flag("badge_roche")
		"azuria_ville":
			return GameManager.get_flag("badge_cascade")
		"carmin_sur_mer":
			return GameManager.get_flag("ticket_oceane_recu") or GameManager.get_flag("badge_foudre")
		"celadopole":
			return GameManager.get_flag("badge_prisme") or GameManager.get_flag("scope_sylphe_obtenu")
		"safrania":
			return GameManager.get_flag("badge_ame") or GameManager.get_flag("safrania_liberee")
		"lavanville":
			return GameManager.get_flag("m_fuji_sauve") or GameManager.get_flag("tour_pokemon_terminee")
		"parmanie":
			return GameManager.get_flag("badge_marais") or GameManager.get_flag("parc_safari_visite")
		"cramoisile":
			return GameManager.get_flag("badge_volcan") or GameManager.get_flag("cle_arene_cramoisile_obtenu")
		"plateau_indigo":
			return GameManager.get_flag("route_victoire_terminee")
	return false

static func _equipe_connait_attaque(attaque_id: String) -> bool:
	for poke in PlayerData.equipe:
		if poke.get("pv_actuels", 0) <= 0:
			continue
		for atk in poke.get("attaques", []):
			if atk.get("id", "") == attaque_id:
				return true
	return false
