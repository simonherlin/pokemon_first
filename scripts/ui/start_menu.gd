extends CanvasLayer

# StartMenu — Menu principal en jeu (ouvert avec Entrée / Start)
# Affiche : Pokédex, Pokémon, Sac, Carte Dresseur, Sauvegarder, Quitter

signal menu_ferme()

const OPTIONS := ["POKÉDEX", "POKÉMON", "SAC", "DRESSEUR", "SAUVEGARDER", "QUITTER"]

var _index: int = 0
var _actif: bool = true
var _sous_ecran: Node = null  # Référence au sous-écran actif

# --- Nœuds UI ---
var _panel: Panel = null
var _labels: Array[Label] = []

func _ready() -> void:
	layer = 80
	_creer_ui()
	_maj_curseur()

func _creer_ui() -> void:
	# Fond semi-transparent pour assombrir le jeu
	var fond := ColorRect.new()
	fond.color = Color(0, 0, 0, 0.3)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Panel du menu (côté droit, style Pokémon)
	_panel = Panel.new()
	_panel.position = Vector2(300, 16)
	_panel.size = Vector2(164, OPTIONS.size() * 28 + 16)
	# Style du panel
	var style := StyleBoxFlat.new()
	style.bg_color = Color(1, 1, 1, 0.95)
	style.border_color = Color(0.2, 0.2, 0.2)
	style.set_border_width_all(3)
	style.set_corner_radius_all(4)
	_panel.add_theme_stylebox_override("panel", style)
	add_child(_panel)

	# Labels des options
	for i in range(OPTIONS.size()):
		var label := Label.new()
		label.text = "  " + OPTIONS[i]
		label.position = Vector2(8, 8 + i * 28)
		label.size = Vector2(148, 26)
		label.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
		label.add_theme_font_size_override("font_size", 14)
		_labels.append(label)
		_panel.add_child(label)

func _process(_delta: float) -> void:
	if not _actif or _sous_ecran != null:
		return

	if Input.is_action_just_pressed("action_haut"):
		_index = (_index - 1 + OPTIONS.size()) % OPTIONS.size()
		_maj_curseur()
	elif Input.is_action_just_pressed("action_bas"):
		_index = (_index + 1) % OPTIONS.size()
		_maj_curseur()
	elif Input.is_action_just_pressed("action_confirmer"):
		_selectionner_option()
	elif Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
		_fermer()

func _maj_curseur() -> void:
	for i in range(_labels.size()):
		var prefix := "▶ " if i == _index else "  "
		_labels[i].text = prefix + OPTIONS[i]

func _selectionner_option() -> void:
	match _index:
		0:  # Pokédex
			_ouvrir_sous_ecran("pokedex")
		1:  # Pokémon
			_ouvrir_sous_ecran("pokemon")
		2:  # Sac
			_ouvrir_sous_ecran("sac")
		3:  # Dresseur
			_ouvrir_sous_ecran("dresseur")
		4:  # Sauvegarder
			_ouvrir_sous_ecran("sauvegarder")
		5:  # Quitter
			_fermer()

func _ouvrir_sous_ecran(ecran: String) -> void:
	var script_path := ""
	match ecran:
		"pokedex":
			script_path = "res://scripts/ui/pokedex_screen.gd"
		"pokemon":
			script_path = "res://scripts/ui/pokemon_team_screen.gd"
		"sac":
			script_path = "res://scripts/ui/bag_screen.gd"
		"dresseur":
			script_path = "res://scripts/ui/player_card_screen.gd"
		"sauvegarder":
			script_path = "res://scripts/ui/save_screen.gd"

	if script_path.is_empty() or not ResourceLoader.exists(script_path):
		return

	var scr = load(script_path)
	_sous_ecran = CanvasLayer.new()
	_sous_ecran.layer = 85
	_sous_ecran.set_script(scr)
	add_child(_sous_ecran)
	# Connecter le signal de fermeture
	if _sous_ecran.has_signal("ecran_ferme"):
		_sous_ecran.ecran_ferme.connect(_on_sous_ecran_ferme)

func _on_sous_ecran_ferme() -> void:
	if _sous_ecran:
		_sous_ecran.queue_free()
		_sous_ecran = null

func _fermer() -> void:
	_actif = false
	emit_signal("menu_ferme")
	queue_free()
