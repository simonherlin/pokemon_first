extends CanvasLayer

# MoveLearnScreen — Écran pour choisir quelle attaque oublier
# Affiche les 4 attaques actuelles + la nouvelle, le joueur choisit

signal choix_fait(index_remplacement: int)  # -1 = annuler, 0-3 = remplacer

var pokemon: Pokemon = null
var move_id: String = ""

var _labels: Array[Label] = []
var _label_message: Label = null
var _label_nouvelle: Label = null
var _index: int = 0  # 0-3 = attaques actuelles, 4 = annuler
var _nb_options: int = 5  # 4 attaques + annuler

func _ready() -> void:
	layer = 92
	_creer_ui()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.1, 0.1, 0.2, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre
	var move_data := MoveData.get_move(move_id)
	var move_nom: String = move_data.get("nom", move_id) if move_data else move_id

	_label_message = Label.new()
	_label_message.text = "Quelle attaque %s doit-il oublier ?" % pokemon.surnom
	_label_message.position = Vector2(40, 10)
	_label_message.add_theme_color_override("font_color", Color.WHITE)
	_label_message.add_theme_font_size_override("font_size", 14)
	add_child(_label_message)

	# Nouvelle attaque (en bas)
	_label_nouvelle = Label.new()
	var type_str: String = move_data.get("type", "normal") if move_data else "normal"
	var pp_str: String = str(move_data.get("pp", 0)) if move_data else "?"
	var puiss_str: String = str(move_data.get("puissance", 0)) if move_data else "?"
	_label_nouvelle.text = "NOUVELLE → %s  (Type: %s  Puiss: %s  PP: %s)" % [move_nom, type_str.to_upper(), puiss_str, pp_str]
	_label_nouvelle.position = Vector2(40, 40)
	_label_nouvelle.add_theme_color_override("font_color", Color.YELLOW)
	_label_nouvelle.add_theme_font_size_override("font_size", 12)
	add_child(_label_nouvelle)

	# Séparateur
	var sep := Label.new()
	sep.text = "─────────────────────────────"
	sep.position = Vector2(40, 60)
	sep.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
	add_child(sep)

	# Attaques actuelles
	for i in range(4):
		var label := Label.new()
		label.position = Vector2(40, 80 + i * 40)
		label.size = Vector2(400, 36)
		label.add_theme_color_override("font_color", Color.WHITE)
		label.add_theme_font_size_override("font_size", 12)
		_labels.append(label)
		add_child(label)

		if i < pokemon.attaques.size():
			var atk: Dictionary = pokemon.attaques[i]
			var atk_data := MoveData.get_move(atk.get("id", ""))
			var nom: String = atk_data.get("nom", "???") if atk_data else "???"
			var a_type: String = atk_data.get("type", "normal") if atk_data else "normal"
			var a_puiss: String = str(atk_data.get("puissance", 0)) if atk_data else "?"
			var a_pp: String = "%d/%d" % [atk.get("pp_actuels", 0), atk.get("pp_max", 0)]
			label.text = "  %s  (Type: %s  Puiss: %s  PP: %s)" % [nom, a_type.to_upper(), a_puiss, a_pp]
		else:
			label.text = "  ---"

	# Option annuler
	var label_annuler := Label.new()
	label_annuler.position = Vector2(40, 80 + 4 * 40)
	label_annuler.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
	label_annuler.add_theme_font_size_override("font_size", 12)
	label_annuler.text = "  Ne pas apprendre"
	_labels.append(label_annuler)
	add_child(label_annuler)

	# Instructions
	var instr := Label.new()
	instr.text = "▲▼: Choisir   A: Confirmer"
	instr.position = Vector2(120, 300)
	instr.add_theme_color_override("font_color", Color(0.5, 0.6, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

	_maj_curseur()

func _maj_curseur() -> void:
	for i in range(_labels.size()):
		var texte: String = _labels[i].text
		if texte.begins_with("▶ "):
			texte = "  " + texte.substr(2)
		elif texte.begins_with("  "):
			pass
		if i == _index:
			_labels[i].text = "▶ " + texte.strip_edges()
		else:
			_labels[i].text = "  " + texte.strip_edges()

func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("action_haut"):
		_index = (_index - 1 + _nb_options) % _nb_options
		_maj_curseur()
	elif Input.is_action_just_pressed("action_bas"):
		_index = (_index + 1) % _nb_options
		_maj_curseur()
	elif Input.is_action_just_pressed("action_confirmer"):
		var result := _index if _index < 4 else -1
		emit_signal("choix_fait", result)
		queue_free()
	elif Input.is_action_just_pressed("action_annuler"):
		emit_signal("choix_fait", -1)
		queue_free()
