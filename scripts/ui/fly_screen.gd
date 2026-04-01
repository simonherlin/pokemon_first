extends CanvasLayer

# FlyScreen — Écran de sélection de destination pour Vol (CS02)
# Affiche la liste des villes visitées, le joueur choisit et se téléporte

signal ecran_ferme()
signal destination_choisie(carte_id: String)

var _index: int = 0
var _destinations: Array = []
var _labels: Array[Label] = []
var _scroll_offset: int = 0
const MAX_VISIBLE := 8

func _ready() -> void:
	layer = 90
	_destinations = FlySystem.get_destinations_disponibles()
	if _destinations.is_empty():
		_fermer()
		return
	_creer_ui()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.05, 0.1, 0.25, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre
	var titre := Label.new()
	titre.text = "VOL — Choisir une destination"
	titre.position = Vector2(80, 10)
	titre.add_theme_color_override("font_color", Color.YELLOW)
	titre.add_theme_font_size_override("font_size", 14)
	fond.add_child(titre)

	# Destinations
	for i in range(mini(_destinations.size(), MAX_VISIBLE)):
		var lbl := Label.new()
		lbl.position = Vector2(60, 40 + i * 30)
		lbl.size = Vector2(360, 28)
		lbl.add_theme_color_override("font_color", Color.WHITE)
		lbl.add_theme_font_size_override("font_size", 13)
		_labels.append(lbl)
		fond.add_child(lbl)

	# Instructions
	var instr := Label.new()
	instr.text = "A: Voler  B: Retour"
	instr.position = Vector2(120, 300)
	instr.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	fond.add_child(instr)

	_maj_affichage()

func _process(_delta: float) -> void:
	if _destinations.is_empty():
		return

	if Input.is_action_just_pressed("action_haut"):
		_index = (_index - 1 + _destinations.size()) % _destinations.size()
		_ajuster_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_bas"):
		_index = (_index + 1) % _destinations.size()
		_ajuster_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_confirmer"):
		_choisir()
	elif Input.is_action_just_pressed("action_annuler"):
		_fermer()

func _ajuster_scroll() -> void:
	if _index < _scroll_offset:
		_scroll_offset = _index
	elif _index >= _scroll_offset + MAX_VISIBLE:
		_scroll_offset = _index - MAX_VISIBLE + 1

func _maj_affichage() -> void:
	for i in range(_labels.size()):
		var idx := _scroll_offset + i
		if idx >= _destinations.size():
			_labels[i].text = ""
			continue
		var dest: Dictionary = _destinations[idx]
		var prefix := "▶ " if idx == _index else "  "
		_labels[i].text = prefix + dest.get("nom", "???")

func _choisir() -> void:
	if _index >= _destinations.size():
		return
	var dest: Dictionary = _destinations[_index]
	emit_signal("destination_choisie", dest.get("carte_id", ""))
	queue_free()

func _fermer() -> void:
	emit_signal("ecran_ferme")
	queue_free()
