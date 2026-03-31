extends Node2D

# BattleScene — Scène de combat qui connecte BattleController ↔ BattleHUD
# Reçoit les paramètres de SceneManager et orchestre le combat

# --- Nœuds ---
@onready var hud := $BattleHUD
@onready var sprite_joueur: Sprite2D = $SpriteJoueur
@onready var sprite_ennemi: Sprite2D = $SpriteEnnemi
@onready var background: ColorRect = $Background

# --- Labels HUD ---
@onready var label_nom_joueur: Label = $BattleHUD/PanelJoueur/LabelNom
@onready var label_niveau_joueur: Label = $BattleHUD/PanelJoueur/LabelNiveau
@onready var barre_pv_joueur: ProgressBar = $BattleHUD/PanelJoueur/BarrePV
@onready var label_pv_joueur: Label = $BattleHUD/PanelJoueur/LabelPV
@onready var label_statut_joueur: Label = $BattleHUD/PanelJoueur/LabelStatut

@onready var label_nom_ennemi: Label = $BattleHUD/PanelEnnemi/LabelNom
@onready var label_niveau_ennemi: Label = $BattleHUD/PanelEnnemi/LabelNiveau
@onready var barre_pv_ennemi: ProgressBar = $BattleHUD/PanelEnnemi/BarrePV
@onready var label_statut_ennemi: Label = $BattleHUD/PanelEnnemi/LabelStatut

@onready var label_message: RichTextLabel = $BattleHUD/PanelMessage/LabelMessage
@onready var menu_action: VBoxContainer = $BattleHUD/MenuAction
@onready var menu_attaque: VBoxContainer = $BattleHUD/MenuAttaque

# --- Paramètres reçus ---
var _type_combat: String = "sauvage"
var _carte_retour: String = "bourg_palette"
var _dresseur_data: Dictionary = {}

# --- Battle Controller ---
var _controller: Node = null

# --- État menu ---
var _index_action: int = 0
var _index_attaque: int = 0
var _nb_attaques: int = 0
var _menu_actif: String = ""
var _actions := ["attaque", "sac", "pokemon", "fuite"]

func _ready() -> void:
	menu_action.visible = false
	menu_attaque.visible = false
	# Charger le fond de combat
	var bg_texture := load("res://assets/sprites/ui/battle_bg.png") as Texture2D
	if bg_texture and background:
		# Remplacer le ColorRect par un TextureRect ou colorer
		background.color = Color(0.75, 0.85, 0.65, 1)

func recevoir_params(params: Dictionary) -> void:
	_type_combat = params.get("type_combat", "sauvage")
	_carte_retour = params.get("carte_retour", "bourg_palette")
	_dresseur_data = params.get("dresseur_data", {})

	# Obtenir le Pokémon du joueur
	var pokemon_index: int = params.get("pokemon_joueur_index", 0)
	if PlayerData.equipe.is_empty():
		push_error("BattleScene: équipe du joueur vide !")
		return
	var pokemon_joueur := Pokemon.from_dict(PlayerData.equipe[pokemon_index])

	# Initialiser le BattleController
	_controller = BattleController
	_connecter_signaux()

	if _type_combat == "sauvage":
		var espece_id: String = params.get("espece_id", "019")
		var niveau: int = params.get("niveau", 5)
		_controller.demarrer_sauvage(pokemon_joueur, espece_id, niveau, pokemon_index)
	else:
		_controller.demarrer_dresseur(pokemon_joueur, _dresseur_data, pokemon_index)
	
	# Charger les sprites des Pokémon
	_charger_sprites_pokemon()

# Charger les textures front/back des Pokémon en combat
func _charger_sprites_pokemon() -> void:
	if not _controller:
		return
	# Sprite du joueur (dos)
	if _controller.pokemon_joueur:
		var back_path := "res://assets/sprites/pokemon/back/%s.png" % _controller.pokemon_joueur.espece_id
		var back_tex := load(back_path) as Texture2D
		if back_tex:
			sprite_joueur.texture = back_tex
			# Adapter l'échelle pour que ce soit visible (64×96 → agrandi ×2)
			sprite_joueur.scale = Vector2(2.0, 2.0)
	# Sprite de l'ennemi (face)
	if _controller.pokemon_ennemi:
		var front_path := "res://assets/sprites/pokemon/front/%s.png" % _controller.pokemon_ennemi.espece_id
		var front_tex := load(front_path) as Texture2D
		if front_tex:
			sprite_ennemi.texture = front_tex
			sprite_ennemi.scale = Vector2(1.5, 1.5)

func _connecter_signaux() -> void:
	if not _controller:
		return
	_controller.message_affiche.connect(_on_message)
	_controller.action_requise.connect(_on_action_requise)
	_controller.attaque_requise.connect(_on_attaque_requise)
	_controller.pv_mis_a_jour.connect(_on_pv_mis_a_jour)
	_controller.statut_mis_a_jour.connect(_on_statut_mis_a_jour)
	_controller.combat_termine.connect(_on_combat_termine)
	_controller.evolution_proposee.connect(_on_evolution_proposee)
	_controller.attaque_a_apprendre.connect(_on_attaque_a_apprendre)

func _on_message(texte: String) -> void:
	label_message.text = texte

func _on_action_requise() -> void:
	label_message.text = "Que faire ?"
	_afficher_info_pokemon()
	_index_action = 0
	menu_action.visible = true
	menu_attaque.visible = false
	_menu_actif = "action"
	_maj_curseur_action()

func _on_attaque_requise() -> void:
	_index_attaque = 0
	menu_action.visible = false
	menu_attaque.visible = true
	_menu_actif = "attaque"
	_nb_attaques = _controller.pokemon_joueur.attaques.size()
	_maj_menu_attaque()
	_maj_curseur_attaque()

func _on_pv_mis_a_jour(joueur: bool, pv: int, pv_max: int) -> void:
	if joueur:
		barre_pv_joueur.max_value = pv_max
		barre_pv_joueur.value = pv
		label_pv_joueur.text = "%d/%d" % [pv, pv_max]
	else:
		barre_pv_ennemi.max_value = pv_max
		barre_pv_ennemi.value = pv

func _on_statut_mis_a_jour(joueur: bool, statut: String) -> void:
	var abrev := _abreger_statut(statut)
	if joueur:
		label_statut_joueur.text = abrev
		label_statut_joueur.visible = not statut.is_empty()
	else:
		label_statut_ennemi.text = abrev
		label_statut_ennemi.visible = not statut.is_empty()

func _on_combat_termine(victoire: bool) -> void:
	if _controller:
		_controller.message_affiche.disconnect(_on_message)
		_controller.action_requise.disconnect(_on_action_requise)
		_controller.attaque_requise.disconnect(_on_attaque_requise)
		_controller.pv_mis_a_jour.disconnect(_on_pv_mis_a_jour)
		_controller.statut_mis_a_jour.disconnect(_on_statut_mis_a_jour)
		_controller.combat_termine.disconnect(_on_combat_termine)
		if _controller.evolution_proposee.is_connected(_on_evolution_proposee):
			_controller.evolution_proposee.disconnect(_on_evolution_proposee)
		if _controller.attaque_a_apprendre.is_connected(_on_attaque_a_apprendre):
			_controller.attaque_a_apprendre.disconnect(_on_attaque_a_apprendre)
	# Sauvegarder l'état des PV dans l'équipe
	if _controller.pokemon_joueur:
		PlayerData.equipe[_controller.index_pokemon_joueur] = _controller.pokemon_joueur.to_dict()
	# Retour à la carte
	await get_tree().create_timer(2.0).timeout
	SceneManager.charger_scene("res://scenes/maps/%s.tscn" % _carte_retour, {
		"carte_id": _carte_retour
	})

func _afficher_info_pokemon() -> void:
	if not _controller:
		return
	var pj := _controller.pokemon_joueur
	var pe := _controller.pokemon_ennemi
	if pj:
		label_nom_joueur.text = pj.surnom
		label_niveau_joueur.text = "N.%d" % pj.niveau
		barre_pv_joueur.max_value = pj.pv_max
		barre_pv_joueur.value = pj.pv_actuels
		label_pv_joueur.text = "%d/%d" % [pj.pv_actuels, pj.pv_max]
	if pe:
		label_nom_ennemi.text = pe.surnom
		label_niveau_ennemi.text = "N.%d" % pe.niveau
		barre_pv_ennemi.max_value = pe.pv_max
		barre_pv_ennemi.value = pe.pv_actuels

func _process(_delta: float) -> void:
	match _menu_actif:
		"action":
			_gerer_input_action()
		"attaque":
			_gerer_input_attaque()

func _gerer_input_action() -> void:
	if Input.is_action_just_pressed("action_haut"):
		_index_action = (_index_action - 1 + _actions.size()) % _actions.size()
		_maj_curseur_action()
	elif Input.is_action_just_pressed("action_bas"):
		_index_action = (_index_action + 1) % _actions.size()
		_maj_curseur_action()
	elif Input.is_action_just_pressed("action_confirmer"):
		_menu_actif = ""
		menu_action.visible = false
		_executer_action(_actions[_index_action])

func _gerer_input_attaque() -> void:
	if Input.is_action_just_pressed("action_haut"):
		_index_attaque = (_index_attaque - 1 + _nb_attaques) % _nb_attaques
		_maj_curseur_attaque()
	elif Input.is_action_just_pressed("action_bas"):
		_index_attaque = (_index_attaque + 1) % _nb_attaques
		_maj_curseur_attaque()
	elif Input.is_action_just_pressed("action_confirmer"):
		_menu_actif = ""
		menu_attaque.visible = false
		_controller.joueur_choisit_attaque(_index_attaque)
	elif Input.is_action_just_pressed("action_annuler"):
		_menu_actif = ""
		menu_attaque.visible = false
		_on_action_requise()

func _executer_action(action: String) -> void:
	match action:
		"attaque":
			_on_attaque_requise()
		"sac":
			# TODO: ouvrir le sac
			_controller.joueur_tente_capture("pokeball")
		"pokemon":
			# TODO: écran de sélection
			_on_action_requise()
		"fuite":
			_controller.joueur_tente_fuite()

func _maj_curseur_action() -> void:
	var labels := menu_action.get_children()
	var noms := ["Attaque", "Sac", "Pokémon", "Fuite"]
	for i in range(labels.size()):
		if i < noms.size():
			labels[i].text = ("▶ " if i == _index_action else "  ") + noms[i]

func _maj_menu_attaque() -> void:
	var labels := menu_attaque.get_children()
	var attaques := _controller.pokemon_joueur.attaques
	for i in range(labels.size()):
		if i < attaques.size():
			var md := MoveData.get_move(attaques[i]["id"])
			labels[i].text = "%s  %d/%d" % [md.get("nom", "???"), attaques[i]["pp_actuels"], attaques[i]["pp_max"]]
			labels[i].visible = true
		else:
			labels[i].visible = false

func _maj_curseur_attaque() -> void:
	var labels := menu_attaque.get_children()
	var attaques := _controller.pokemon_joueur.attaques
	for i in range(labels.size()):
		if i < attaques.size():
			var md := MoveData.get_move(attaques[i]["id"])
			var prefix := "▶ " if i == _index_attaque else "  "
			labels[i].text = prefix + "%s  %d/%d" % [md.get("nom", "???"), attaques[i]["pp_actuels"], attaques[i]["pp_max"]]

func _abreger_statut(statut: String) -> String:
	match statut:
		"brulure": return "BRL"
		"gel": return "GEL"
		"paralysie": return "PAR"
		"poison", "poison_grave": return "PSN"
		"sommeil": return "SOM"
	return ""

# --- Gestion des évolutions ---
func _on_evolution_proposee(pokemon: Pokemon, vers_id: String) -> void:
	var evo_screen := load("res://scripts/ui/evolution_screen.gd").new()
	evo_screen.pokemon = pokemon
	evo_screen.vers_id = vers_id
	add_child(evo_screen)
	evo_screen.evolution_terminee.connect(func(accepte: bool):
		_controller.confirmer_evolution(accepte)
		# Recharger le sprite si évolué
		if accepte:
			_charger_sprites_pokemon()
			_afficher_info_pokemon()
	)

# --- Gestion de l'apprentissage d'attaques ---
func _on_attaque_a_apprendre(pokemon: Pokemon, move_id: String) -> void:
	var learn_screen := load("res://scripts/ui/move_learn_screen.gd").new()
	learn_screen.pokemon = pokemon
	learn_screen.move_id = move_id
	add_child(learn_screen)
	learn_screen.choix_fait.connect(func(index_remplacement: int):
		_controller.confirmer_apprentissage(index_remplacement)
	)
