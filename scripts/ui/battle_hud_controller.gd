extends Control

# BattleHUDController — Interface de combat : barres PV, menus, texte
# S'occupe d'afficher les info Pokémon et les menus d'action/attaque

# --- Nœuds — Pokémon Joueur (bas-droite) ---
@onready var label_nom_joueur: Label = $PanelJoueur/LabelNom
@onready var label_niveau_joueur: Label = $PanelJoueur/LabelNiveau
@onready var barre_pv_joueur: ProgressBar = $PanelJoueur/BarrePV
@onready var label_pv_joueur: Label = $PanelJoueur/LabelPV
@onready var label_statut_joueur: Label = $PanelJoueur/LabelStatut

# --- Nœuds — Pokémon Ennemi (haut-gauche) ---
@onready var label_nom_ennemi: Label = $PanelEnnemi/LabelNom
@onready var label_niveau_ennemi: Label = $PanelEnnemi/LabelNiveau
@onready var barre_pv_ennemi: ProgressBar = $PanelEnnemi/BarrePV
@onready var label_statut_ennemi: Label = $PanelEnnemi/LabelStatut

# --- Nœuds — Boîte de texte ---
@onready var label_message: RichTextLabel = $PanelMessage/LabelMessage

# --- Nœuds — Menus ---
@onready var menu_action: VBoxContainer = $MenuAction
@onready var menu_attaque: VBoxContainer = $MenuAttaque
@onready var labels_action: Array = []
@onready var labels_attaque: Array = []

# --- État ---
var _index_action: int = 0
var _index_attaque: int = 0
var _nb_attaques: int = 0
var _actions: Array = ["Attaque", "Sac", "Pokémon", "Fuite"]
var _menu_actif: String = ""  # "", "action", "attaque"

# --- Signaux ---
signal action_selectionnee(action: String)
signal attaque_selectionnee(index: int)
signal retour_menu()

func _ready() -> void:
	_initialiser_menus()
	cacher_menus()

func _initialiser_menus() -> void:
	if menu_action:
		for child in menu_action.get_children():
			labels_action.append(child)
	if menu_attaque:
		for child in menu_attaque.get_children():
			labels_attaque.append(child)

func _process(_delta: float) -> void:
	match _menu_actif:
		"action":
			_gerer_menu_action()
		"attaque":
			_gerer_menu_attaque()

# ----------------------------------------------------------------
# Mise à jour de l'affichage
# ----------------------------------------------------------------
func mettre_a_jour_joueur(pokemon: Pokemon) -> void:
	if label_nom_joueur:
		label_nom_joueur.text = pokemon.surnom
	if label_niveau_joueur:
		label_niveau_joueur.text = "N.%d" % pokemon.niveau
	mettre_a_jour_pv_joueur(pokemon.pv_actuels, pokemon.pv_max)
	mettre_a_jour_statut_joueur(pokemon.statut)

func mettre_a_jour_ennemi(pokemon: Pokemon) -> void:
	if label_nom_ennemi:
		label_nom_ennemi.text = pokemon.surnom
	if label_niveau_ennemi:
		label_niveau_ennemi.text = "N.%d" % pokemon.niveau
	mettre_a_jour_pv_ennemi(pokemon.pv_actuels, pokemon.pv_max)
	mettre_a_jour_statut_ennemi(pokemon.statut)

func mettre_a_jour_pv_joueur(pv: int, pv_max: int) -> void:
	if barre_pv_joueur:
		barre_pv_joueur.max_value = pv_max
		barre_pv_joueur.value = pv
		_colorer_barre(barre_pv_joueur, pv, pv_max)
	if label_pv_joueur:
		label_pv_joueur.text = "%d/%d" % [pv, pv_max]

func mettre_a_jour_pv_ennemi(pv: int, pv_max: int) -> void:
	if barre_pv_ennemi:
		barre_pv_ennemi.max_value = pv_max
		barre_pv_ennemi.value = pv
		_colorer_barre(barre_pv_ennemi, pv, pv_max)

func mettre_a_jour_statut_joueur(statut: String) -> void:
	if label_statut_joueur:
		label_statut_joueur.text = _abreger_statut(statut)
		label_statut_joueur.visible = not statut.is_empty()

func mettre_a_jour_statut_ennemi(statut: String) -> void:
	if label_statut_ennemi:
		label_statut_ennemi.text = _abreger_statut(statut)
		label_statut_ennemi.visible = not statut.is_empty()

# ----------------------------------------------------------------
# Messages
# ----------------------------------------------------------------
func afficher_message(texte: String) -> void:
	if label_message:
		label_message.text = texte

func effacer_message() -> void:
	if label_message:
		label_message.text = ""

# ----------------------------------------------------------------
# Menu d'action (Attaque / Sac / Pokémon / Fuite)
# ----------------------------------------------------------------
func afficher_menu_action() -> void:
	_menu_actif = "action"
	_index_action = 0
	if menu_action:
		menu_action.visible = true
	if menu_attaque:
		menu_attaque.visible = false
	_mettre_a_jour_curseur_action()

func afficher_menu_attaque(attaques: Array) -> void:
	_menu_actif = "attaque"
	_index_attaque = 0
	_nb_attaques = attaques.size()
	if menu_action:
		menu_action.visible = false
	if menu_attaque:
		menu_attaque.visible = true
		for i in range(labels_attaque.size()):
			if i < attaques.size():
				var move_data := MoveData.get_move(attaques[i]["id"])
				var nom: String = move_data.get("nom", "???")
				var pp: int = attaques[i]["pp_actuels"]
				var pp_max: int = attaques[i]["pp_max"]
				labels_attaque[i].text = "%s  %d/%d" % [nom, pp, pp_max]
				labels_attaque[i].visible = true
			else:
				labels_attaque[i].visible = false
	_mettre_a_jour_curseur_attaque()

func cacher_menus() -> void:
	_menu_actif = ""
	if menu_action:
		menu_action.visible = false
	if menu_attaque:
		menu_attaque.visible = false

# ----------------------------------------------------------------
# Gestion input menus
# ----------------------------------------------------------------
func _gerer_menu_action() -> void:
	if Input.is_action_just_pressed("action_haut"):
		_index_action = (_index_action - 1 + _actions.size()) % _actions.size()
		_mettre_a_jour_curseur_action()
	elif Input.is_action_just_pressed("action_bas"):
		_index_action = (_index_action + 1) % _actions.size()
		_mettre_a_jour_curseur_action()
	elif Input.is_action_just_pressed("action_confirmer"):
		cacher_menus()
		emit_signal("action_selectionnee", _actions[_index_action].to_lower())

func _gerer_menu_attaque() -> void:
	if Input.is_action_just_pressed("action_haut"):
		_index_attaque = (_index_attaque - 1 + _nb_attaques) % _nb_attaques
		_mettre_a_jour_curseur_attaque()
	elif Input.is_action_just_pressed("action_bas"):
		_index_attaque = (_index_attaque + 1) % _nb_attaques
		_mettre_a_jour_curseur_attaque()
	elif Input.is_action_just_pressed("action_confirmer"):
		cacher_menus()
		emit_signal("attaque_selectionnee", _index_attaque)
	elif Input.is_action_just_pressed("action_annuler"):
		# Retour au menu action
		afficher_menu_action()
		emit_signal("retour_menu")

# ----------------------------------------------------------------
# Curseur visuel
# ----------------------------------------------------------------
func _mettre_a_jour_curseur_action() -> void:
	for i in range(labels_action.size()):
		if i < _actions.size():
			var prefix := "▶ " if i == _index_action else "  "
			labels_action[i].text = prefix + _actions[i]

func _mettre_a_jour_curseur_attaque() -> void:
	# Géré via le contenu texte, le ▶ est ajouté au label
	pass

# ----------------------------------------------------------------
# Utilitaires
# ----------------------------------------------------------------
func _colorer_barre(barre: ProgressBar, pv: int, pv_max: int) -> void:
	var ratio := float(pv) / float(maxi(1, pv_max))
	var style := StyleBoxFlat.new()
	if ratio > 0.5:
		style.bg_color = Color(0.2, 0.8, 0.2)  # Vert
	elif ratio > 0.2:
		style.bg_color = Color(1.0, 0.8, 0.0)  # Jaune
	else:
		style.bg_color = Color(1.0, 0.2, 0.2)  # Rouge
	barre.add_theme_stylebox_override("fill", style)

func _abreger_statut(statut: String) -> String:
	match statut:
		"brulure": return "BRL"
		"gel": return "GEL"
		"paralysie": return "PAR"
		"poison", "poison_grave": return "PSN"
		"sommeil": return "SOM"
	return ""
