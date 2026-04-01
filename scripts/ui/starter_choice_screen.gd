extends Control

# StarterChoiceScreen — Écran de choix du Pokémon de départ
# Affiché dans le laboratoire du Prof. Chen
# Le joueur choisit entre Bulbizarre, Salamèche et Carapuce

signal starter_choisi(espece_id: String)

const STARTERS := [
	{"id": "001", "nom": "Bulbizarre", "type": "Plante/Poison", "description": "Un Pokémon graine qui porte\nune bulbe sur son dos depuis\nsa naissance."},
	{"id": "004", "nom": "Salamèche", "type": "Feu", "description": "La flamme au bout de sa queue\nindique son état de santé.\nElle brûle vivement quand il va bien."},
	{"id": "007", "nom": "Carapuce", "type": "Eau", "description": "Sa carapace ne sert pas\nqu'à le protéger. Sa forme ronde\nréduit la résistance dans l'eau."},
	{"id": "151", "nom": "Mew", "type": "Psy", "description": "Un Pokémon très rare et mythique.\nOn dit qu'il possède le code\ngénétique de tous les Pokémon."}
]

var _index: int = 0
var _labels_noms: Array[Label] = []
var _label_description: Label = null
var _label_type: Label = null
var _label_instruction: Label = null
var _confirme: bool = false
var _curseur_oui_non: int = 1  # 0 = Oui, 1 = Non (défaut Non)
var _labels_oui_non: Array[Label] = []

func _ready() -> void:
	_creer_ui()
	_mettre_a_jour_selection()

func _creer_ui() -> void:
	# Fond semi-transparent
	var fond := ColorRect.new()
	fond.color = Color(0.05, 0.1, 0.05, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(fond)

	# Titre
	var titre := Label.new()
	titre.text = "Choisis ton Pokémon !"
	titre.position = Vector2(120, 12)
	titre.add_theme_color_override("font_color", Color.YELLOW)
	titre.add_theme_font_size_override("font_size", 16)
	add_child(titre)

	# Les 4 starters côte à côte (3 classiques + Mew)
	var nb_starters := STARTERS.size()
	var panel_largeur := 105
	var espacement := 6
	var total_w := nb_starters * panel_largeur + (nb_starters - 1) * espacement
	var offset_x := (480 - total_w) / 2
	for i in range(nb_starters):
		var panel := Panel.new()
		panel.position = Vector2(offset_x + i * (panel_largeur + espacement), 50)
		panel.size = Vector2(panel_largeur, 100)
		var style := StyleBoxFlat.new()
		style.bg_color = Color(0.15, 0.2, 0.15, 0.9)
		style.set_border_width_all(2)
		style.border_color = Color(0.3, 0.4, 0.3)
		style.set_corner_radius_all(6)
		panel.add_theme_stylebox_override("panel", style)
		panel.name = "PanelStarter%d" % i
		add_child(panel)

		var nom := Label.new()
		nom.text = STARTERS[i].nom
		nom.position = Vector2(8, 8)
		nom.add_theme_color_override("font_color", Color.WHITE)
		nom.add_theme_font_size_override("font_size", 12)
		panel.add_child(nom)
		_labels_noms.append(nom)

		var type_label := Label.new()
		type_label.text = "Type: %s" % STARTERS[i].type
		type_label.position = Vector2(8, 28)
		type_label.add_theme_color_override("font_color", Color(0.6, 0.8, 0.6))
		type_label.add_theme_font_size_override("font_size", 9)
		panel.add_child(type_label)

		# Sprite du Pokémon (image réelle depuis assets)
		var sprite_path := "res://assets/sprites/pokemon/front/%s.png" % STARTERS[i].id
		if ResourceLoader.exists(sprite_path):
			var tex := load(sprite_path)
			var sprite := TextureRect.new()
			sprite.texture = tex
			sprite.position = Vector2(22, 48)
			sprite.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			sprite.custom_minimum_size = Vector2(60, 48)
			sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			panel.add_child(sprite)
		else:
			# Fallback : carré coloré
			var sprite_rect := ColorRect.new()
			sprite_rect.position = Vector2(22, 55)
			sprite_rect.size = Vector2(60, 40)
			match i:
				0: sprite_rect.color = Color(0.2, 0.6, 0.3, 0.8)
				1: sprite_rect.color = Color(0.8, 0.3, 0.2, 0.8)
				2: sprite_rect.color = Color(0.2, 0.4, 0.8, 0.8)
				3: sprite_rect.color = Color(0.8, 0.4, 0.8, 0.8)  # Rose (Psy)
			panel.add_child(sprite_rect)

	# Description en bas
	var panel_desc := Panel.new()
	panel_desc.position = Vector2(24, 170)
	panel_desc.size = Vector2(432, 60)
	var style_desc := StyleBoxFlat.new()
	style_desc.bg_color = Color(0.1, 0.12, 0.1, 0.9)
	style_desc.set_border_width_all(2)
	style_desc.border_color = Color(0.3, 0.4, 0.3)
	style_desc.set_corner_radius_all(4)
	panel_desc.add_theme_stylebox_override("panel", style_desc)
	add_child(panel_desc)

	_label_description = Label.new()
	_label_description.position = Vector2(12, 8)
	_label_description.size = Vector2(408, 50)
	_label_description.autowrap_mode = TextServer.AUTOWRAP_WORD
	_label_description.add_theme_color_override("font_color", Color.WHITE)
	_label_description.add_theme_font_size_override("font_size", 11)
	panel_desc.add_child(_label_description)

	# Zone Oui/Non (cachée par défaut)
	for j in range(2):
		var lbl := Label.new()
		lbl.position = Vector2(170 + j * 80, 250)
		lbl.add_theme_color_override("font_color", Color.WHITE)
		lbl.add_theme_font_size_override("font_size", 12)
		lbl.visible = false
		add_child(lbl)
		_labels_oui_non.append(lbl)

	# Instruction
	_label_instruction = Label.new()
	_label_instruction.position = Vector2(110, 300)
	_label_instruction.add_theme_color_override("font_color", Color(0.5, 0.6, 0.5))
	_label_instruction.add_theme_font_size_override("font_size", 10)
	_label_instruction.text = "◀ ▶ : Choisir     A : Confirmer"
	add_child(_label_instruction)

func _mettre_a_jour_selection() -> void:
	var nb := STARTERS.size()
	for i in range(nb):
		var panel: Panel = get_node("PanelStarter%d" % i)
		var style: StyleBoxFlat = panel.get_theme_stylebox("panel").duplicate()
		if i == _index:
			style.border_color = Color.YELLOW
			style.set_border_width_all(3)
			_labels_noms[i].add_theme_color_override("font_color", Color.YELLOW)
		else:
			style.border_color = Color(0.3, 0.4, 0.3)
			style.set_border_width_all(2)
			_labels_noms[i].add_theme_color_override("font_color", Color.WHITE)
		panel.add_theme_stylebox_override("panel", style)
	_label_description.text = STARTERS[_index].description

func _maj_oui_non() -> void:
	_labels_oui_non[0].text = ("▶ " if _curseur_oui_non == 0 else "  ") + "Oui"
	_labels_oui_non[1].text = ("▶ " if _curseur_oui_non == 1 else "  ") + "Non"

func _process(_delta: float) -> void:
	if _confirme:
		_gerer_confirmation()
	else:
		_gerer_selection()

func _gerer_selection() -> void:
	var nb := STARTERS.size()
	if Input.is_action_just_pressed("action_gauche"):
		_index = (_index - 1 + nb) % nb
		_mettre_a_jour_selection()
	elif Input.is_action_just_pressed("action_droite"):
		_index = (_index + 1) % nb
		_mettre_a_jour_selection()
	elif Input.is_action_just_pressed("action_confirmer"):
		_confirme = true
		_label_description.text = "Tu veux %s ?" % STARTERS[_index].nom
		_label_instruction.text = ""
		_curseur_oui_non = 1  # Par défaut sur Non (action irréversible)
		for lbl in _labels_oui_non:
			lbl.visible = true
		_maj_oui_non()

func _gerer_confirmation() -> void:
	if Input.is_action_just_pressed("action_gauche") or Input.is_action_just_pressed("action_droite"):
		_curseur_oui_non = 1 - _curseur_oui_non
		_maj_oui_non()
	elif Input.is_action_just_pressed("action_confirmer"):
		if _curseur_oui_non == 0:
			# Oui — choix confirmé
			emit_signal("starter_choisi", STARTERS[_index].id)
		else:
			# Non — revenir à la sélection
			_confirme = false
			for lbl in _labels_oui_non:
				lbl.visible = false
			_label_instruction.text = "◀ ▶ : Choisir     A : Confirmer"
			_mettre_a_jour_selection()
	elif Input.is_action_just_pressed("action_annuler"):
		_confirme = false
		for lbl in _labels_oui_non:
			lbl.visible = false
		_label_instruction.text = "◀ ▶ : Choisir     A : Confirmer"
		_mettre_a_jour_selection()
