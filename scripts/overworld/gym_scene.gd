extends Node2D

# GymScene — Script spécialisé pour les arènes Pokémon
# Gère les combats de dresseurs d'arène et l'obtention de badges
# Utilisé par l'arène d'Argenta (Pierre)

const TAILLE_TILE := 32
const PLAYER_SCENE := preload("res://scenes/entities/player.tscn")
const NPC_SCENE := preload("res://scenes/entities/npc.tscn")

var carte_id: String = ""
var carte_data: Dictionary = {}
var joueur: CharacterBody2D = null
var _menu_ouvert: bool = false
var _start_menu: Node = null

# Données d'arène
var _badge_index: int = 0  # Index du badge (0 = Badge Roche)
var _badge_flag: String = "badge_roche"
var _champion_id: String = "champion_pierre"
var _ct_recompense: String = "ct_tomberoche"
var _badge_nom: String = "BADGE ROCHE"
var _ct_nom: String = "CT TOMBEROCHE"
var _ct_description: String = "TOMBEROCHE inflige des dégâts et peut\nréduire la Vitesse adverse."
var _badge_desc: String = "Ce badge augmente l'Attaque de tes Pokémon."

@onready var tilemap: TileMap = $TileMap
@onready var entities: Node2D = $Entities
@onready var dialog_box: Control = $DialogBox

func _ready() -> void:
	if carte_id.is_empty():
		carte_id = _deviner_carte_id()
	_configurer_arene()
	_charger_carte()
	_peindre_tilemap()
	_instancier_joueur()
	_instancier_pnj()
	PlayerData.carte_actuelle = carte_id
	var musique: String = carte_data.get("musique", "")
	if not musique.is_empty() and ResourceLoader.exists(musique):
		AudioManager.jouer_musique(musique)

func _configurer_arene() -> void:
	# Configurer selon l'arène
	match carte_id:
		"arene_argenta":
			_badge_index = 0
			_badge_flag = "badge_roche"
			_champion_id = "champion_pierre"
			_ct_recompense = "ct_tomberoche"
			_badge_nom = "BADGE ROCHE"
			_ct_nom = "CT TOMBEROCHE"
			_ct_description = "TOMBEROCHE inflige des dégâts et peut\nréduire la Vitesse adverse."
			_badge_desc = "Ce badge augmente l'Attaque de tes Pokémon."
		"arene_azuria":
			_badge_index = 1
			_badge_flag = "badge_cascade"
			_champion_id = "champion_ondine"
			_ct_recompense = "ct_cascade"
			_badge_nom = "BADGE CASCADE"
			_ct_nom = "CT CASCADE"
			_ct_description = "CASCADE est une puissante attaque Eau."
			_badge_desc = "Ce badge permet aux Pokémon jusqu'au N.30\nd'obéir sans condition."
		"arene_carmin":
			_badge_index = 2
			_badge_flag = "badge_foudre"
			_champion_id = "champion_major_bob"
			_ct_recompense = "ct_tonnerre"
			_badge_nom = "BADGE FOUDRE"
			_ct_nom = "CT TONNERRE"
			_ct_description = "TONNERRE est une puissante attaque Électrik\nqui peut paralyser l'adversaire."
			_badge_desc = "Ce badge permet d'utiliser COUPE\nhors des combats."
		"arene_celadopole":
			_badge_index = 3
			_badge_flag = "badge_prisme"
			_champion_id = "champion_erika"
			_ct_recompense = "ct_mega_drain"
			_badge_nom = "BADGE PRISME"
			_ct_nom = "CT MÉGA-SANGSUE"
			_ct_description = "MÉGA-SANGSUE absorbe la moitié des\ndégâts infligés pour restaurer vos PV."
			_badge_desc = "Ce badge permet aux Pokémon jusqu'au N.50\nd'obéir sans condition."
		"arene_parmanie":
			_badge_index = 4
			_badge_flag = "badge_ame"
			_champion_id = "champion_koga"
			_ct_recompense = "ct_toxik"
			_badge_nom = "BADGE ÂME"
			_ct_nom = "CT TOXIK"
			_ct_description = "TOXIK empoisonne gravement l'adversaire.\nLes dégâts augmentent chaque tour."
			_badge_desc = "Ce badge permet d'utiliser SURF\nhors des combats."
		"arene_safrania":
			_badge_index = 5
			_badge_flag = "badge_marais"
			_champion_id = "champion_morgane"
			_ct_recompense = "ct_psyko"
			_badge_nom = "BADGE MARAIS"
			_ct_nom = "CT PSYKO"
			_ct_description = "PSYKO est une puissante attaque Psy\nqui peut baisser le Spécial adverse."
			_badge_desc = "Ce badge permet aux Pokémon jusqu'au N.70\nd'obéir sans condition."
		"arene_cramoisile":
			_badge_index = 6
			_badge_flag = "badge_volcan"
			_champion_id = "champion_auguste"
			_ct_recompense = "ct_deflagration"
			_badge_nom = "BADGE VOLCAN"
			_ct_nom = "CT DÉFLAGRATION"
			_ct_description = "DÉFLAGRATION est une puissante attaque Feu\nqui peut brûler l'adversaire."
			_badge_desc = "Ce badge permet aux Pokémon jusqu'au N.80\nd'obéir sans condition."
		"arene_jadielle":
			_badge_index = 7
			_badge_flag = "badge_terre"
			_champion_id = "champion_giovanni_arene"
			_ct_recompense = "ct_seisme"
			_badge_nom = "BADGE TERRE"
			_ct_nom = "CT SÉISME"
			_ct_description = "SÉISME est une puissante attaque Sol\nqui touche tous les Pokémon au sol."
			_badge_desc = "Ce badge permet à tous les Pokémon\nd'obéir sans condition."

func recevoir_params(params: Dictionary) -> void:
	carte_id = params.get("carte_id", carte_id)
	var warp_id: String = params.get("warp_entree", "")
	if not warp_id.is_empty() and joueur:
		_teleporter_sur_warp(warp_id)
	# Vérifier si on revient d'un combat gagné contre le champion
	if params.get("champion_battu", false):
		await get_tree().create_timer(0.5).timeout
		_sequence_badge()

func _charger_carte() -> void:
	carte_data = MapLoader.get_carte(carte_id)
	if carte_data.is_empty():
		push_warning("GymScene: données de carte introuvables pour %s" % carte_id)

func _peindre_tilemap() -> void:
	if carte_data.is_empty():
		return
	TileSetBuilder.peindre_carte(tilemap, carte_data)

func _instancier_joueur() -> void:
	joueur = PLAYER_SCENE.instantiate()
	var px: int = PlayerData.position_x
	var py: int = PlayerData.position_y
	joueur.position_grille = Vector2i(px, py)
	joueur.position = Vector2(px, py) * TAILLE_TILE
	entities.add_child(joueur)

func _instancier_pnj() -> void:
	for pnj_data in carte_data.get("pnj", []):
		var npc := NPC_SCENE.instantiate()
		npc.position = Vector2(pnj_data.get("x", 0), pnj_data.get("y", 0)) * TAILLE_TILE
		npc.initialiser_depuis_json(pnj_data)
		if npc.has_signal("dialogue_demarre"):
			npc.dialogue_demarre.connect(_on_dialogue_demarre)
		if npc.has_signal("combat_dresseur_demarre"):
			npc.combat_dresseur_demarre.connect(_on_combat_dresseur)
		entities.add_child(npc)

func _teleporter_sur_warp(warp_id: String) -> void:
	for warp in carte_data.get("warps", []):
		if warp.get("id", "") == warp_id or warp.get("vers_warp", "") == warp_id:
			var x: int = warp.get("x", 0)
			var y: int = warp.get("y", 0)
			joueur.teleporter(x, y + 1, "bas")
			return

func _on_dialogue_demarre(lignes: Array) -> void:
	if joueur:
		joueur.set_peut_bouger(false)
	dialog_box.afficher_dialogue(lignes)
	if not dialog_box.dialogue_termine.is_connected(_on_dialogue_termine):
		dialog_box.dialogue_termine.connect(_on_dialogue_termine)

func _on_dialogue_termine() -> void:
	if joueur:
		joueur.set_peut_bouger(true)

func _on_combat_dresseur(dresseur_id: String, _equipe: Array, _recompense_npc: int, _nom: String) -> void:
	# Vérifier si déjà battu
	if PlayerData.dresseur_est_battu(dresseur_id):
		return
	# Charger les données du dresseur
	var chemin := "res://data/trainers.json"
	if not FileAccess.file_exists(chemin):
		push_error("GymScene: trainers.json introuvable")
		return
	var fichier := FileAccess.open(chemin, FileAccess.READ)
	var all_trainers = JSON.parse_string(fichier.get_as_text())
	fichier.close()
	if not all_trainers or not all_trainers.has(dresseur_id):
		push_error("GymScene: dresseur %s introuvable" % dresseur_id)
		return

	var trainer_raw: Dictionary = all_trainers[dresseur_id]
	# Construire l'équipe
	var equipe_combat := []
	for pkmn in trainer_raw.get("equipe", []):
		var pokemon = SpeciesData.creer_pokemon(pkmn.get("espece_id", "074"), pkmn.get("niveau", 10))
		if pokemon:
			equipe_combat.append(pokemon.to_dict())
	if equipe_combat.is_empty():
		return

	var trainer_data := {
		"id": dresseur_id,
		"nom": trainer_raw.get("nom", "Dresseur"),
		"classe": trainer_raw.get("classe", ""),
		"dialogue_avant": trainer_raw.get("dialogue_avant", ""),
		"dialogue_defaite": trainer_raw.get("dialogue_defaite", ""),
		"recompense": trainer_raw.get("recompense", 100),
		"equipe": equipe_combat
	}

	PlayerData.sauvegarder_position(carte_id, joueur.position_grille.x, joueur.position_grille.y, "haut")

	# Déterminer si c'est le champion
	var est_champion: bool = (dresseur_id == _champion_id)

	SceneManager.charger_scene("res://scenes/battle/battle_scene.tscn", {
		"type_combat": "dresseur",
		"carte_retour": carte_id,
		"dresseur_data": trainer_data,
		"pokemon_joueur_index": 0,
		"champion_battu": est_champion
	})

# --- Séquence d'obtention de badge ---
func _sequence_badge() -> void:
	if GameManager.get_flag(_badge_flag):
		return  # Badge déjà obtenu

	if joueur:
		joueur.set_peut_bouger(false)

	# Donner le badge
	GameManager.donner_badge(_badge_index)
	GameManager.set_flag(_badge_flag, true)

	# Donner la CT récompense
	if not _ct_recompense.is_empty():
		PlayerData.ajouter_item(_ct_recompense, 1)

	# Marquer le champion comme battu
	PlayerData.marquer_dresseur_battu(_champion_id)

	# Dialogue de victoire (dynamique selon l'arène)
	var messages := [
		"Bravo ! Tu m'as vaincu !",
		"%s a obtenu le %s !" % [PlayerData.nom_joueur, _badge_nom],
		_badge_desc,
		"Tiens, prends aussi cette CT.",
		"%s a obtenu %s !" % [PlayerData.nom_joueur, _ct_nom],
		_ct_description,
		"Bonne chance pour la suite de ton aventure !"
	]

	dialog_box.afficher_dialogue(messages)
	if not dialog_box.dialogue_termine.is_connected(_fin_sequence_badge):
		dialog_box.dialogue_termine.connect(_fin_sequence_badge, CONNECT_ONE_SHOT)

func _fin_sequence_badge() -> void:
	if joueur:
		joueur.set_peut_bouger(true)

func _deviner_carte_id() -> String:
	return get_scene_file_path().get_file().get_basename()

# --- Gestion du Start Menu ---
func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("action_menu") and not _menu_ouvert:
		_ouvrir_menu()

func _ouvrir_menu() -> void:
	if _menu_ouvert or SceneManager.est_en_transition():
		return
	_menu_ouvert = true
	if joueur:
		joueur.set_peut_bouger(false)
	var scr = load("res://scripts/ui/start_menu.gd")
	_start_menu = CanvasLayer.new()
	_start_menu.set_script(scr)
	add_child(_start_menu)
	_start_menu.menu_ferme.connect(_on_menu_ferme)

func _on_menu_ferme() -> void:
	_menu_ouvert = false
	_start_menu = null
	if joueur:
		joueur.set_peut_bouger(true)
