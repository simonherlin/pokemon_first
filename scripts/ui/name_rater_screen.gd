# name_rater_screen.gd — Écran du Juge des Noms (renommer un Pokémon)
# Étape 1 : sélectionner un Pokémon de l'équipe
# Étape 2 : saisir un nouveau surnom (clavier virtuel)
extends CanvasLayer

signal ecran_ferme()

# --- État ---
enum Phase { SELECTION_POKEMON, SAISIE_NOM }
var _phase: Phase = Phase.SELECTION_POKEMON
var _index_pokemon: int = 0
var _index_clavier: int = 0
var _nouveau_nom: String = ""
var _actif: bool = true

# Clavier virtuel (grille 10×5 + effacer + valider)
const CLAVIER := [
	"A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
	"K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
	"U", "V", "W", "X", "Y", "Z", " ", "-", "'", ".",
	"a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
	"k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
]
const CLAVIER_COLONNES := 10
const NOM_MAX := 10

# --- UI ---
var _panel: Panel = null
var _label_info: Label = null
var _label_nom: Label = null
var _labels_equipe: Array[Label] = []
var _labels_clavier: Array[Label] = []
var _label_effacer: Label = null
var _label_valider: Label = null

func _ready() -> void:
	layer = 90
	_creer_ui_selection()

func _creer_ui_selection() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0, 0, 0, 0.5)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	_panel = Panel.new()
	_panel.position = Vector2(60, 30)
	_panel.size = Vector2(360, 260)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(1, 1, 1, 0.97)
	style.border_color = Color(0.2, 0.2, 0.2)
	style.set_border_width_all(3)
	style.set_corner_radius_all(6)
	_panel.add_theme_stylebox_override("panel", style)
	add_child(_panel)

	_label_info = Label.new()
	_label_info.text = "Quel Pokémon veux-tu renommer ?"
	_label_info.position = Vector2(10, 8)
	_label_info.size = Vector2(340, 24)
	_label_info.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
	_label_info.add_theme_font_size_override("font_size", 13)
	_panel.add_child(_label_info)

	# Liste des Pokémon de l'équipe
	for i in range(PlayerData.equipe.size()):
		var p: Dictionary = PlayerData.equipe[i]
		var espece_data: Dictionary = SpeciesData.get_espece(p.get("espece_id", "001"))
		var nom_espece: String = espece_data.get("nom", "???")
		var surnom: String = p.get("surnom", nom_espece)
		var label := Label.new()
		label.text = "  %s (Nv.%d)" % [surnom, p.get("niveau", 1)]
		label.position = Vector2(20, 40 + i * 28)
		label.size = Vector2(300, 24)
		label.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
		label.add_theme_font_size_override("font_size", 12)
		_labels_equipe.append(label)
		_panel.add_child(label)
	_maj_curseur_equipe()

func _process(_delta: float) -> void:
	if not _actif:
		return
	match _phase:
		Phase.SELECTION_POKEMON:
			_process_selection()
		Phase.SAISIE_NOM:
			_process_saisie()

func _process_selection() -> void:
	var nb := PlayerData.equipe.size()
	if nb == 0:
		_fermer()
		return
	if Input.is_action_just_pressed("action_haut"):
		_index_pokemon = (_index_pokemon - 1 + nb) % nb
		_maj_curseur_equipe()
	elif Input.is_action_just_pressed("action_bas"):
		_index_pokemon = (_index_pokemon + 1) % nb
		_maj_curseur_equipe()
	elif Input.is_action_just_pressed("action_confirmer"):
		_passer_a_saisie()
	elif Input.is_action_just_pressed("action_annuler"):
		_fermer()

func _maj_curseur_equipe() -> void:
	for i in range(_labels_equipe.size()):
		var p: Dictionary = PlayerData.equipe[i]
		var espece_data: Dictionary = SpeciesData.get_espece(p.get("espece_id", "001"))
		var nom_espece: String = espece_data.get("nom", "???")
		var surnom: String = p.get("surnom", nom_espece)
		var prefix := "▶ " if i == _index_pokemon else "  "
		_labels_equipe[i].text = "%s%s (Nv.%d)" % [prefix, surnom, p.get("niveau", 1)]

func _passer_a_saisie() -> void:
	_phase = Phase.SAISIE_NOM
	_nouveau_nom = ""
	_index_clavier = 0
	# Vider le panel
	for child in _panel.get_children():
		child.queue_free()
	_labels_equipe.clear()
	_labels_clavier.clear()

	# Recréer l'UI pour le clavier
	_label_info = Label.new()
	var p: Dictionary = PlayerData.equipe[_index_pokemon]
	var espece_data: Dictionary = SpeciesData.get_espece(p.get("espece_id", "001"))
	_label_info.text = "Nouveau nom pour %s :" % espece_data.get("nom", "???")
	_label_info.position = Vector2(10, 4)
	_label_info.size = Vector2(340, 20)
	_label_info.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
	_label_info.add_theme_font_size_override("font_size", 12)
	_panel.add_child(_label_info)

	_label_nom = Label.new()
	_label_nom.text = "_"
	_label_nom.position = Vector2(100, 28)
	_label_nom.size = Vector2(200, 24)
	_label_nom.add_theme_color_override("font_color", Color(0.2, 0.2, 0.8))
	_label_nom.add_theme_font_size_override("font_size", 16)
	_panel.add_child(_label_nom)

	# Grille du clavier
	for i in range(CLAVIER.size()):
		var col := i % CLAVIER_COLONNES
		var row := i / CLAVIER_COLONNES
		var label := Label.new()
		label.text = "  %s" % CLAVIER[i]
		label.position = Vector2(10 + col * 32, 58 + row * 24)
		label.size = Vector2(30, 22)
		label.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
		label.add_theme_font_size_override("font_size", 12)
		_labels_clavier.append(label)
		_panel.add_child(label)

	# Boutons Effacer / Valider
	_label_effacer = Label.new()
	_label_effacer.text = "  [EFFACER]"
	_label_effacer.position = Vector2(10, 190)
	_label_effacer.size = Vector2(120, 22)
	_label_effacer.add_theme_color_override("font_color", Color(0.6, 0.1, 0.1))
	_label_effacer.add_theme_font_size_override("font_size", 12)
	_panel.add_child(_label_effacer)

	_label_valider = Label.new()
	_label_valider.text = "  [VALIDER]"
	_label_valider.position = Vector2(180, 190)
	_label_valider.size = Vector2(120, 22)
	_label_valider.add_theme_color_override("font_color", Color(0.1, 0.5, 0.1))
	_label_valider.add_theme_font_size_override("font_size", 12)
	_panel.add_child(_label_valider)

	_maj_curseur_clavier()

func _process_saisie() -> void:
	var total := CLAVIER.size() + 2  # +effacer +valider
	if Input.is_action_just_pressed("action_gauche"):
		if _index_clavier < CLAVIER.size():
			if _index_clavier % CLAVIER_COLONNES > 0:
				_index_clavier -= 1
		elif _index_clavier == CLAVIER.size() + 1:
			_index_clavier = CLAVIER.size()
		_maj_curseur_clavier()
	elif Input.is_action_just_pressed("action_droite"):
		if _index_clavier < CLAVIER.size():
			if _index_clavier % CLAVIER_COLONNES < CLAVIER_COLONNES - 1:
				_index_clavier += 1
		elif _index_clavier == CLAVIER.size():
			_index_clavier = CLAVIER.size() + 1
		_maj_curseur_clavier()
	elif Input.is_action_just_pressed("action_haut"):
		if _index_clavier >= CLAVIER.size():
			_index_clavier = CLAVIER.size() - CLAVIER_COLONNES
		elif _index_clavier >= CLAVIER_COLONNES:
			_index_clavier -= CLAVIER_COLONNES
		_maj_curseur_clavier()
	elif Input.is_action_just_pressed("action_bas"):
		if _index_clavier < CLAVIER.size() - CLAVIER_COLONNES:
			_index_clavier += CLAVIER_COLONNES
		elif _index_clavier < CLAVIER.size():
			_index_clavier = CLAVIER.size()
		_maj_curseur_clavier()
	elif Input.is_action_just_pressed("action_confirmer"):
		if _index_clavier < CLAVIER.size():
			# Ajouter un caractère
			if _nouveau_nom.length() < NOM_MAX:
				_nouveau_nom += CLAVIER[_index_clavier]
				_maj_nom_affiche()
		elif _index_clavier == CLAVIER.size():
			# Effacer
			if _nouveau_nom.length() > 0:
				_nouveau_nom = _nouveau_nom.substr(0, _nouveau_nom.length() - 1)
				_maj_nom_affiche()
		else:
			# Valider
			_appliquer_nom()
	elif Input.is_action_just_pressed("action_annuler"):
		if _nouveau_nom.length() > 0:
			_nouveau_nom = _nouveau_nom.substr(0, _nouveau_nom.length() - 1)
			_maj_nom_affiche()
		else:
			_phase = Phase.SELECTION_POKEMON
			# Recréer l'UI de sélection
			for child in _panel.get_children():
				child.queue_free()
			_labels_clavier.clear()
			_creer_contenu_selection()

func _creer_contenu_selection() -> void:
	_label_info = Label.new()
	_label_info.text = "Quel Pokémon veux-tu renommer ?"
	_label_info.position = Vector2(10, 8)
	_label_info.size = Vector2(340, 24)
	_label_info.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
	_label_info.add_theme_font_size_override("font_size", 13)
	_panel.add_child(_label_info)
	_labels_equipe.clear()
	for i in range(PlayerData.equipe.size()):
		var p: Dictionary = PlayerData.equipe[i]
		var espece_data: Dictionary = SpeciesData.get_espece(p.get("espece_id", "001"))
		var nom_espece: String = espece_data.get("nom", "???")
		var surnom: String = p.get("surnom", nom_espece)
		var label := Label.new()
		label.text = "  %s (Nv.%d)" % [surnom, p.get("niveau", 1)]
		label.position = Vector2(20, 40 + i * 28)
		label.size = Vector2(300, 24)
		label.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
		label.add_theme_font_size_override("font_size", 12)
		_labels_equipe.append(label)
		_panel.add_child(label)
	_maj_curseur_equipe()

func _maj_curseur_clavier() -> void:
	for i in range(_labels_clavier.size()):
		var prefix := "▶" if i == _index_clavier else "  "
		_labels_clavier[i].text = "%s%s" % [prefix, CLAVIER[i]]
	if _label_effacer:
		var prefix_e := "▶" if _index_clavier == CLAVIER.size() else "  "
		_label_effacer.text = "%s[EFFACER]" % prefix_e
	if _label_valider:
		var prefix_v := "▶" if _index_clavier == CLAVIER.size() + 1 else "  "
		_label_valider.text = "%s[VALIDER]" % prefix_v

func _maj_nom_affiche() -> void:
	if _label_nom:
		_label_nom.text = _nouveau_nom + "_" if _nouveau_nom.length() < NOM_MAX else _nouveau_nom

func _appliquer_nom() -> void:
	if _nouveau_nom.strip_edges().is_empty():
		# Si vide, utiliser le nom de l'espèce
		var p: Dictionary = PlayerData.equipe[_index_pokemon]
		var espece_data: Dictionary = SpeciesData.get_espece(p.get("espece_id", "001"))
		_nouveau_nom = espece_data.get("nom", "Pokémon")
	PlayerData.equipe[_index_pokemon]["surnom"] = _nouveau_nom
	_fermer()

func _fermer() -> void:
	_actif = false
	emit_signal("ecran_ferme")
	queue_free()
