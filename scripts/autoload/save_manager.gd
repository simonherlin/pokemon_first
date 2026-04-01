extends Node

# SaveManager — Singleton global
# Sauvegarde et chargement de l'état du jeu en JSON

# --- Constantes ---
const DOSSIER_SAVES := "user://saves/"
const NOM_FICHIER_SAVE := "save_%d.json"
const NB_SLOTS := 3

# --- Signaux ---
signal sauvegarde_terminee(slot: int)
signal chargement_termine(slot: int)
signal erreur_sauvegarde(message: String)

func _ready() -> void:
	# Créer le dossier saves s'il n'existe pas
	DirAccess.make_dir_recursive_absolute(DOSSIER_SAVES)

# Sauvegarder dans un slot (0, 1 ou 2)
func sauvegarder(slot: int) -> bool:
	if slot < 0 or slot >= NB_SLOTS:
		emit_signal("erreur_sauvegarde", "Slot invalide: %d" % slot)
		return false

	var data := _collecter_donnees()
	var json_str := JSON.stringify(data, "\t")
	var chemin := DOSSIER_SAVES + NOM_FICHIER_SAVE % slot

	var fichier := FileAccess.open(chemin, FileAccess.WRITE)
	if fichier == null:
		emit_signal("erreur_sauvegarde", "Impossible d'écrire dans %s" % chemin)
		return false

	fichier.store_string(json_str)
	fichier.close()
	emit_signal("sauvegarde_terminee", slot)
	return true

# Charger depuis un slot
func charger(slot: int) -> bool:
	if slot < 0 or slot >= NB_SLOTS:
		emit_signal("erreur_sauvegarde", "Slot invalide: %d" % slot)
		return false

	var chemin := DOSSIER_SAVES + NOM_FICHIER_SAVE % slot
	if not FileAccess.file_exists(chemin):
		emit_signal("erreur_sauvegarde", "Aucune sauvegarde dans le slot %d" % slot)
		return false

	var fichier := FileAccess.open(chemin, FileAccess.READ)
	if fichier == null:
		emit_signal("erreur_sauvegarde", "Impossible de lire %s" % chemin)
		return false

	var json_str := fichier.get_as_text()
	fichier.close()

	var data = JSON.parse_string(json_str)
	if data == null:
		emit_signal("erreur_sauvegarde", "JSON corrompu dans le slot %d" % slot)
		return false

	_appliquer_donnees(data)
	emit_signal("chargement_termine", slot)
	return true

# Vérifier si un slot contient une sauvegarde
func slot_existe(slot: int) -> bool:
	var chemin := DOSSIER_SAVES + NOM_FICHIER_SAVE % slot
	return FileAccess.file_exists(chemin)

# Supprimer une sauvegarde
func supprimer(slot: int) -> void:
	var chemin := DOSSIER_SAVES + NOM_FICHIER_SAVE % slot
	if FileAccess.file_exists(chemin):
		DirAccess.remove_absolute(chemin)

# Obtenir les métadonnées d'un slot (pour l'écran de sélection)
func info_slot(slot: int) -> Dictionary:
	if not slot_existe(slot):
		return {}
	var chemin := DOSSIER_SAVES + NOM_FICHIER_SAVE % slot
	var fichier := FileAccess.open(chemin, FileAccess.READ)
	if fichier == null:
		return {}
	var data = JSON.parse_string(fichier.get_as_text())
	fichier.close()
	if data == null:
		return {}
	return {
		"nom_joueur": data.get("nom_joueur", "???"),
		"temps_jeu": data.get("temps_jeu_secondes", 0),
		"badges": data.get("badges", []).count(true),
		"pokedex": data.get("pokedex_capture", []).size()
	}

# --- Sérialisation ---
func _collecter_donnees() -> Dictionary:
	return {
		# GameManager
		"badges": GameManager.badges,
		"flags": GameManager.flags,
		"temps_jeu_secondes": GameManager.temps_jeu_secondes,
		"nom_rival": GameManager.nom_rival,
		"repousse_restant": GameManager.repousse_restant,
		"dernier_centre": GameManager.dernier_centre,
		# PlayerData
		"nom_joueur": PlayerData.nom_joueur,
		"argent": PlayerData.argent,
		"id_joueur": PlayerData.id_joueur,
		"carte_actuelle": PlayerData.carte_actuelle,
		"position_x": PlayerData.position_x,
		"position_y": PlayerData.position_y,
		"direction": PlayerData.direction,
		"equipe": PlayerData.equipe,
		"inventaire": PlayerData.inventaire,
		"pokedex_vu": PlayerData.pokedex_vu,
		"pokedex_capture": PlayerData.pokedex_capture,
		"dresseurs_battus": PlayerData.dresseurs_battus,
		"objets_ramasses": PlayerData.objets_ramasses,
		"boites": PlayerData.boites,
		"jetons": PlayerData.jetons
	}

func _appliquer_donnees(data: Dictionary) -> void:
	# GameManager
	if "badges" in data:
		var badges_raw: Array = data["badges"]
		var badges_typed: Array[bool] = []
		for b in badges_raw:
			badges_typed.append(bool(b))
		GameManager.badges = badges_typed
	if "flags" in data:
		GameManager.flags = data["flags"]
	if "temps_jeu_secondes" in data:
		GameManager.temps_jeu_secondes = int(data["temps_jeu_secondes"])
		GameManager._temps_accum = float(GameManager.temps_jeu_secondes)
	if "nom_rival" in data:
		GameManager.nom_rival = data["nom_rival"]
	if "repousse_restant" in data:
		GameManager.repousse_restant = int(data["repousse_restant"])
	if "dernier_centre" in data:
		GameManager.dernier_centre = data["dernier_centre"]
	GameManager.partie_en_cours = true

	# PlayerData
	if "nom_joueur" in data:
		PlayerData.nom_joueur = data["nom_joueur"]
	if "argent" in data:
		PlayerData.argent = int(data["argent"])
	if "id_joueur" in data:
		PlayerData.id_joueur = int(data["id_joueur"])
	if "carte_actuelle" in data:
		PlayerData.carte_actuelle = data["carte_actuelle"]
	if "position_x" in data:
		PlayerData.position_x = int(data["position_x"])
	if "position_y" in data:
		PlayerData.position_y = int(data["position_y"])
	if "direction" in data:
		PlayerData.direction = data["direction"]
	if "equipe" in data:
		PlayerData.equipe = data["equipe"]
	if "inventaire" in data:
		PlayerData.inventaire = data["inventaire"]
	if "pokedex_vu" in data:
		var vu_typed: Array[String] = []
		for s in data["pokedex_vu"]:
			vu_typed.append(str(s))
		PlayerData.pokedex_vu = vu_typed
	if "pokedex_capture" in data:
		var cap_typed: Array[String] = []
		for s in data["pokedex_capture"]:
			cap_typed.append(str(s))
		PlayerData.pokedex_capture = cap_typed
	if "dresseurs_battus" in data:
		var bat_typed: Array[String] = []
		for s in data["dresseurs_battus"]:
			bat_typed.append(str(s))
		PlayerData.dresseurs_battus = bat_typed
	if "objets_ramasses" in data:
		var obj_typed: Array[String] = []
		for s in data["objets_ramasses"]:
			obj_typed.append(str(s))
		PlayerData.objets_ramasses = obj_typed
	if "boites" in data:
		PlayerData.boites = []
		for boite in data["boites"]:
			var boite_typed: Array = []
			for pokemon in boite:
				boite_typed.append(pokemon)
			PlayerData.boites.append(boite_typed)
		# Compléter jusqu'à MAX_BOITES si besoin
		while PlayerData.boites.size() < PlayerData.MAX_BOITES:
			PlayerData.boites.append([])
	if "jetons" in data:
		PlayerData.jetons = int(data["jetons"])
