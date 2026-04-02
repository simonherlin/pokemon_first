# town_map_screen.gd — Carte du Kanto (Town Map)
# Affiche les villes/routes visitées avec un curseur mobile
extends CanvasLayer

signal ecran_ferme()

# Données des villes (positions approximatives sur une carte 480×320)
const VILLES := [
	{"id": "bourg_palette", "nom": "Bourg Palette", "x": 90, "y": 260, "flag": ""},
	{"id": "jadielle", "nom": "Jadielle", "x": 90, "y": 200, "flag": "visite_jadielle"},
	{"id": "argenta", "nom": "Argenta", "x": 90, "y": 130, "flag": "visite_argenta"},
	{"id": "azuria", "nom": "Azuria", "x": 180, "y": 80, "flag": "visite_azuria"},
	{"id": "carmin_sur_mer", "nom": "Carmin sur Mer", "x": 180, "y": 220, "flag": "visite_carmin"},
	{"id": "lavanville", "nom": "Lavanville", "x": 270, "y": 170, "flag": "visite_lavanville"},
	{"id": "celadopole", "nom": "Céladopole", "x": 180, "y": 130, "flag": "visite_celadopole"},
	{"id": "safrania", "nom": "Safrania", "x": 180, "y": 170, "flag": "visite_safrania"},
	{"id": "parmanie", "nom": "Parmanie", "x": 180, "y": 260, "flag": "visite_parmanie"},
	{"id": "cramoisile", "nom": "Cramois'Île", "x": 90, "y": 290, "flag": "visite_cramoisile"},
	{"id": "plateau_indigo", "nom": "Plateau Indigo", "x": 30, "y": 80, "flag": "visite_plateau_indigo"},
]

var _index: int = 0
var _actif: bool = true

# UI
var _panel: Panel = null
var _carte_rect: ColorRect = null
var _curseur: ColorRect = null
var _label_nom: Label = null
var _points: Array[ColorRect] = []

func _ready() -> void:
	layer = 90
	_creer_ui()
	_maj_affichage()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0, 0, 0, 0.6)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Panel carte
	_panel = Panel.new()
	_panel.position = Vector2(40, 20)
	_panel.size = Vector2(400, 280)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.85, 0.92, 0.85, 0.98)
	style.border_color = Color(0.2, 0.4, 0.2)
	style.set_border_width_all(3)
	style.set_corner_radius_all(6)
	_panel.add_theme_stylebox_override("panel", style)
	add_child(_panel)

	# Titre
	var titre := Label.new()
	titre.text = "CARTE DU KANTO"
	titre.position = Vector2(140, 4)
	titre.add_theme_color_override("font_color", Color(0.15, 0.3, 0.15))
	titre.add_theme_font_size_override("font_size", 14)
	_panel.add_child(titre)

	# Points des villes
	for ville in VILLES:
		var point := ColorRect.new()
		var visible_ville: bool = str(ville["flag"]) == "" or GameManager.get_flag(str(ville["flag"])) == true
		point.color = Color(0.8, 0.2, 0.2) if visible_ville else Color(0.5, 0.5, 0.5, 0.3)
		point.size = Vector2(8, 8)
		point.position = Vector2(ville["x"] - 4, ville["y"] - 4)
		_points.append(point)
		_panel.add_child(point)

	# Curseur (cercle autour de la ville sélectionnée)
	_curseur = ColorRect.new()
	_curseur.color = Color(1, 0.8, 0, 0.6)
	_curseur.size = Vector2(14, 14)
	_panel.add_child(_curseur)

	# Label du nom de la ville
	_label_nom = Label.new()
	_label_nom.position = Vector2(10, 256)
	_label_nom.size = Vector2(380, 20)
	_label_nom.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_nom.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
	_label_nom.add_theme_font_size_override("font_size", 13)
	_panel.add_child(_label_nom)

func _process(_delta: float) -> void:
	if not _actif:
		return
	# Faire clignoter le curseur
	_curseur.visible = fmod(Time.get_ticks_msec() / 500.0, 1.0) > 0.3

	if Input.is_action_just_pressed("action_gauche") or Input.is_action_just_pressed("action_haut"):
		_index = (_index - 1 + VILLES.size()) % VILLES.size()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_droite") or Input.is_action_just_pressed("action_bas"):
		_index = (_index + 1) % VILLES.size()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_confirmer"):
		_fermer()

func _maj_affichage() -> void:
	var ville: Dictionary = VILLES[_index]
	_curseur.position = Vector2(ville["x"] - 7, ville["y"] - 7)
	_label_nom.text = ville["nom"]

func _fermer() -> void:
	_actif = false
	emit_signal("ecran_ferme")
	queue_free()
