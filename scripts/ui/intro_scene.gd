extends Control

# IntroScene — Séquence d'introduction du Professeur Chen
# 1. Discours du Professeur Chen (bienvenue dans le monde des Pokémon)
# 2. Choix du nom du joueur
# 3. Choix du nom du rival
# 4. Transition vers le jeu (chambre du joueur → Bourg Palette)

enum Phase {
	DISCOURS_CHEN,
	NOM_JOUEUR,
	NOM_RIVAL,
	TRANSITION
}

var _phase: Phase = Phase.DISCOURS_CHEN
var _index_dialogue: int = 0
var _nom_joueur: String = ""
var _nom_rival: String = ""

# --- Dialogues du Professeur Chen ---
var _dialogues_chen := [
	"Bonjour ! Bienvenue dans le monde des POKÉMON !",
	"Mon nom est CHEN. Les gens m'appellent le PROF. POKÉMON.",
	"Ce monde est peuplé de créatures appelées POKÉMON.",
	"Certains les utilisent comme animaux domestiques,\nd'autres les font combattre.",
	"Moi, j'étudie les POKÉMON.\nJ'en ai fait ma profession.",
	"Mais d'abord, dis-moi comment tu t'appelles."
]

# --- Nœuds UI ---
var _fond: ColorRect = null
var _label_dialogue: Label = null
var _label_instruction: Label = null
var _panel_nom: Panel = null
var _input_nom: LineEdit = null
var _label_titre_nom: Label = null
var _en_attente_input: bool = false
var _noms_predefs_joueur := ["Red", "Sacha", "Pierre", "Max"]
var _noms_predefs_rival := ["Régis", "Blue", "Paul", "Hugo"]
var _labels_predefs: Array[Label] = []
var _index_predef: int = 0
var _mode_predef: bool = true  # true = choix prédéfini, false = saisie libre

func _ready() -> void:
	_creer_ui()
	_afficher_dialogue()

func _creer_ui() -> void:
	# Fond sombre
	_fond = ColorRect.new()
	_fond.color = Color(0.05, 0.05, 0.15, 1.0)
	_fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(_fond)

	# Zone de dialogue
	var panel_dialogue := Panel.new()
	panel_dialogue.position = Vector2(24, 200)
	panel_dialogue.size = Vector2(432, 100)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.1, 0.1, 0.2, 0.95)
	style.set_border_width_all(2)
	style.border_color = Color(0.4, 0.45, 0.9)
	style.set_corner_radius_all(6)
	panel_dialogue.add_theme_stylebox_override("panel", style)
	add_child(panel_dialogue)

	_label_dialogue = Label.new()
	_label_dialogue.position = Vector2(12, 8)
	_label_dialogue.size = Vector2(408, 80)
	_label_dialogue.autowrap_mode = TextServer.AUTOWRAP_WORD
	_label_dialogue.add_theme_color_override("font_color", Color.WHITE)
	_label_dialogue.add_theme_font_size_override("font_size", 13)
	panel_dialogue.add_child(_label_dialogue)

	# Instruction (bas d'écran)
	_label_instruction = Label.new()
	_label_instruction.position = Vector2(160, 310)
	_label_instruction.add_theme_color_override("font_color", Color(0.5, 0.5, 0.7))
	_label_instruction.add_theme_font_size_override("font_size", 10)
	_label_instruction.text = "Appuie sur A pour continuer"
	add_child(_label_instruction)

	# Titre (Prof Chen)
	var label_chen := Label.new()
	label_chen.text = "PROF. CHEN"
	label_chen.position = Vector2(180, 20)
	label_chen.add_theme_color_override("font_color", Color(0.9, 0.8, 0.4))
	label_chen.add_theme_font_size_override("font_size", 16)
	add_child(label_chen)

	# Panel de choix de nom (initialement caché)
	_panel_nom = Panel.new()
	_panel_nom.position = Vector2(60, 50)
	_panel_nom.size = Vector2(360, 140)
	var style_nom := StyleBoxFlat.new()
	style_nom.bg_color = Color(0.15, 0.15, 0.25, 0.95)
	style_nom.set_border_width_all(2)
	style_nom.border_color = Color(0.5, 0.5, 0.8)
	style_nom.set_corner_radius_all(8)
	_panel_nom.add_theme_stylebox_override("panel", style_nom)
	_panel_nom.visible = false
	add_child(_panel_nom)

	_label_titre_nom = Label.new()
	_label_titre_nom.position = Vector2(80, 8)
	_label_titre_nom.add_theme_color_override("font_color", Color.YELLOW)
	_label_titre_nom.add_theme_font_size_override("font_size", 14)
	_panel_nom.add_child(_label_titre_nom)

	# Noms prédéfinis
	for i in range(4):
		var label := Label.new()
		label.position = Vector2(20 + (i % 2) * 160, 40 + (i / 2) * 30)
		label.add_theme_color_override("font_color", Color.WHITE)
		label.add_theme_font_size_override("font_size", 12)
		_labels_predefs.append(label)
		_panel_nom.add_child(label)

	# Saisie libre
	_input_nom = LineEdit.new()
	_input_nom.position = Vector2(60, 104)
	_input_nom.size = Vector2(200, 28)
	_input_nom.max_length = 10
	_input_nom.placeholder_text = "Tape ton nom..."
	_input_nom.visible = false
	_panel_nom.add_child(_input_nom)

func _afficher_dialogue() -> void:
	if _index_dialogue < _dialogues_chen.size():
		_label_dialogue.text = _dialogues_chen[_index_dialogue]

func _process(_delta: float) -> void:
	match _phase:
		Phase.DISCOURS_CHEN:
			_gerer_discours()
		Phase.NOM_JOUEUR:
			_gerer_choix_nom(true)
		Phase.NOM_RIVAL:
			_gerer_choix_nom(false)
		Phase.TRANSITION:
			pass

func _gerer_discours() -> void:
	if Input.is_action_just_pressed("action_confirmer"):
		_index_dialogue += 1
		if _index_dialogue < _dialogues_chen.size():
			_afficher_dialogue()
		else:
			# Passer au choix du nom
			_phase = Phase.NOM_JOUEUR
			_afficher_choix_nom("Quel est ton nom ?", _noms_predefs_joueur)

func _afficher_choix_nom(titre: String, noms: Array) -> void:
	_panel_nom.visible = true
	_label_titre_nom.text = titre
	_label_instruction.text = "▲▼◀▶: Choisir   A: Confirmer"
	_label_dialogue.text = titre
	_index_predef = 0
	_mode_predef = true
	_input_nom.visible = false
	for i in range(4):
		if i < noms.size():
			_labels_predefs[i].text = noms[i]
			_labels_predefs[i].visible = true
		else:
			_labels_predefs[i].visible = false
	_maj_curseur_nom()

func _maj_curseur_nom() -> void:
	var noms: Array = _noms_predefs_joueur if _phase == Phase.NOM_JOUEUR else _noms_predefs_rival
	for i in range(_labels_predefs.size()):
		if i < noms.size():
			_labels_predefs[i].text = ("▶ " if i == _index_predef else "  ") + noms[i]

func _gerer_choix_nom(est_joueur: bool) -> void:
	var noms: Array = _noms_predefs_joueur if est_joueur else _noms_predefs_rival
	if Input.is_action_just_pressed("action_haut"):
		if _index_predef >= 2:
			_index_predef -= 2
			_maj_curseur_nom()
	elif Input.is_action_just_pressed("action_bas"):
		if _index_predef + 2 < noms.size():
			_index_predef += 2
			_maj_curseur_nom()
	elif Input.is_action_just_pressed("action_gauche"):
		if _index_predef % 2 > 0:
			_index_predef -= 1
			_maj_curseur_nom()
	elif Input.is_action_just_pressed("action_droite"):
		if _index_predef % 2 < 1 and _index_predef + 1 < noms.size():
			_index_predef += 1
			_maj_curseur_nom()
	elif Input.is_action_just_pressed("action_confirmer"):
		var nom_choisi: String = noms[_index_predef]
		if est_joueur:
			_nom_joueur = nom_choisi
			_label_dialogue.text = "Donc ton nom est %s !" % nom_choisi
			_panel_nom.visible = false
			await get_tree().create_timer(1.5).timeout
			_label_dialogue.text = "Et quel est le nom de ton rival ?"
			await get_tree().create_timer(1.0).timeout
			_phase = Phase.NOM_RIVAL
			_afficher_choix_nom("Nom du rival ?", _noms_predefs_rival)
		else:
			_nom_rival = nom_choisi
			_label_dialogue.text = "Ah oui ! Je me souviens ! Son nom est %s !" % nom_choisi
			_panel_nom.visible = false
			await get_tree().create_timer(1.5).timeout
			_lancer_jeu()

func _lancer_jeu() -> void:
	_phase = Phase.TRANSITION
	_label_dialogue.text = "%s ! Ton aventure POKÉMON commence maintenant !" % _nom_joueur
	_label_instruction.text = ""
	await get_tree().create_timer(2.0).timeout

	# Initialiser la partie
	GameManager.nouvelle_partie()
	GameManager.nom_rival = _nom_rival
	GameManager.set_flag("rival_nomme", true)
	GameManager.set_flag("intro_terminee", true)
	PlayerData.nouvelle_partie(_nom_joueur)

	# Donner quelques items de départ
	PlayerData.ajouter_item("potion", 5)
	PlayerData.ajouter_item("pokeball", 5)

	# Position initiale : devant la porte du labo
	PlayerData.sauvegarder_position("laboratoire_chen", 5, 8, "haut")

	# Charger le laboratoire pour la séquence du choix du starter
	SceneManager.charger_scene("res://scenes/maps/laboratoire_chen.tscn", {
		"carte_id": "laboratoire_chen"
	})
