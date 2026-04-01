extends Node

# EncounterSystem — Système de rencontres Pokémon sauvages dans les herbes
# Se déclenche à chaque pas dans les zones d'herbes hautes

const CHEMIN_JSON := "res://data/encounter_tables.json"
const TAUX_RENCONTRE_BASE := 0.10  # 10% de chance par pas dans les herbes

var _tables: Dictionary = {}
var _charge: bool = false

func _ready() -> void:
	_charger_tables()

func _charger_tables() -> void:
	if _charge:
		return
	if not FileAccess.file_exists(CHEMIN_JSON):
		push_error("EncounterSystem: encounter_tables.json introuvable")
		return
	var fichier := FileAccess.open(CHEMIN_JSON, FileAccess.READ)
	var data = JSON.parse_string(fichier.get_as_text())
	fichier.close()
	if data == null:
		push_error("EncounterSystem: JSON invalide")
		return
	_tables = data
	_charge = true

# Vérifier si une rencontre se déclenche à cette position
func verifier_rencontre(position_grille: Vector2i, joueur_node: Node) -> void:
	# Vérifier si la case est une herbe haute
	var zone_id := _obtenir_zone_herbe(position_grille, joueur_node)
	if zone_id.is_empty():
		return

	# Décrémenter le compteur Repousse si actif
	if GameManager.repousse_restant > 0:
		GameManager.repousse_restant -= 1
		# Repousse bloque les rencontres avec des Pokémon de niveau <= leader
		var niveau_leader := _obtenir_niveau_leader()
		# On doit quand même tirer le Pokémon pour vérifier son niveau
		var pokemon_test := _choisir_pokemon(zone_id)
		if not pokemon_test.is_empty():
			var niv_max_test: int = pokemon_test.get("niveau_max", 5)
			if niv_max_test <= niveau_leader:
				return  # Repousse bloque cette rencontre
		else:
			return  # Pas de Pokémon dans cette zone

	# Taux de rencontre
	if randf() > TAUX_RENCONTRE_BASE:
		return

	# Choisir le Pokémon selon la table
	var pokemon_data := _choisir_pokemon(zone_id)
	if pokemon_data.is_empty():
		return

	# Déclencher le combat
	var espece_id: String = pokemon_data.get("pokemon_id", "019")
	var niveau_min: int = pokemon_data.get("niveau_min", 2)
	var niveau_max: int = pokemon_data.get("niveau_max", 5)
	var niveau := randi_range(niveau_min, niveau_max)

	# === Équilibrage dynamique ===
	# Les Pokémon sauvages s'adaptent au niveau du joueur
	var avg_joueur := _calculer_niveau_moyen_equipe()
	if avg_joueur > 0 and avg_joueur > niveau_max:
		# Le sauvage monte au minimum à 85% du niveau moyen du joueur
		var plancher := int(avg_joueur * 0.85)
		niveau = maxi(niveau, plancher)
		# Mais pas plus de 3 niveaux au-dessus du joueur
		niveau = mini(niveau, avg_joueur + 3)
		# Et jamais en-dessous de niveau_min d'origine
		niveau = maxi(niveau, niveau_min)

	# SFX de rencontre sauvage
	AudioManager.jouer_sfx("res://assets/audio/sfx/encounter.ogg")
	# Passer en mode combat
	if joueur_node.has_method("set_peut_bouger"):
		joueur_node.set_peut_bouger(false)

	# Obtenir le Pokémon de tête de l'équipe joueur
	if PlayerData.equipe.is_empty():
		push_warning("EncounterSystem: équipe du joueur vide !")
		return
	var premier_pokemon := Pokemon.from_dict(PlayerData.equipe[0])

	# Charger la scène de combat avec les paramètres
	SceneManager.charger_scene("res://scenes/battle/battle_scene.tscn", {
		"type_combat": "sauvage",
		"espece_id": espece_id,
		"niveau": niveau,
		"pokemon_joueur_index": 0,
		"carte_retour": PlayerData.carte_actuelle,
		"musique_carte": MapLoader.get_carte(PlayerData.carte_actuelle).get("musique", "")
	})

# Identifier si la case courante est dans une zone d'herbes
func _obtenir_zone_herbe(position_grille: Vector2i, joueur_node: Node) -> String:
	# Lire les données de la carte pour trouver les zones d'herbes
	var carte_data := MapLoader.get_carte(PlayerData.carte_actuelle)
	for zone in carte_data.get("zones_herbes", []):
		var x1: int = zone.get("x1", 0)
		var y1: int = zone.get("y1", 0)
		var x2: int = zone.get("x2", 0)
		var y2: int = zone.get("y2", 0)
		if position_grille.x >= x1 and position_grille.x <= x2 and \
		   position_grille.y >= y1 and position_grille.y <= y2:
			return zone.get("table", "")
	return ""

# Choisir un Pokémon depuis la table de rencontres (tirage pondéré)
func _choisir_pokemon(zone_id: String) -> Dictionary:
	if not _charge:
		_charger_tables()
	var table: Dictionary = _tables.get(zone_id, {})
	if table.is_empty():
		return {}
	var herbes: Array = table.get("herbes", [])
	if herbes.is_empty():
		return {}

	# Tirage pondéré
	var total_taux := 0
	for entree in herbes:
		total_taux += entree.get("taux", 0)
	var tirage := randi() % maxi(1, total_taux)
	var cumul := 0
	for entree in herbes:
		cumul += entree.get("taux", 0)
		if tirage < cumul:
			return entree
	return herbes[herbes.size() - 1]

# Obtenir toutes les zones pour le débogage
func get_zones() -> Array:
	return _tables.keys()

# Calculer le niveau moyen de l'équipe du joueur
func _calculer_niveau_moyen_equipe() -> int:
	if PlayerData.equipe.is_empty():
		return 0
	var total := 0
	var count := 0
	for poke_dict in PlayerData.equipe:
		var niv: int = poke_dict.get("niveau", 0)
		if niv > 0:
			total += niv
			count += 1
	if count == 0:
		return 0
	return int(total / count)

# Obtenir le niveau du premier Pokémon non-KO de l'équipe (pour Repousse)
func _obtenir_niveau_leader() -> int:
	for poke_dict in PlayerData.equipe:
		var pv: int = poke_dict.get("pv_actuels", 0)
		if pv > 0:
			return poke_dict.get("niveau", 1)
	return 1
