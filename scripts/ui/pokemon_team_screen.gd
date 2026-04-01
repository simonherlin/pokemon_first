extends CanvasLayer

# PokemonTeamScreen — Affiche l'équipe du joueur (6 slots max)
# Chaque slot : icône, surnom, niveau, barre PV, PV texte, statut
# Supporte : sélection, sous-menu CS (Vol, Surf, Flash), réorganisation

signal ecran_ferme()
signal action_cs(action: String)  # Signal pour les CS overworld

# Constantes pour les CS overworld
const CS_OVERWORLD := {
	"vol": "VOL",
	"surf": "SURF",
	"coupe": "COUPE",
	"force": "FORCE",
	"flash": "FLASH"
}

var _index: int = 0
var _slots: Array[Dictionary] = []
var _sous_menu: Control = null
var _sous_menu_index: int = 0
var _sous_menu_options: Array[String] = []
var _sous_menu_labels: Array[Label] = []
var _mode_swap: bool = false
var _swap_source: int = -1

func _ready() -> void:
	layer = 85
	_creer_ui()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.15, 0.25, 0.45, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre
	var titre := Label.new()
	titre.text = "POKÉMON"
	titre.position = Vector2(180, 4)
	titre.add_theme_color_override("font_color", Color.WHITE)
	titre.add_theme_font_size_override("font_size", 16)
	add_child(titre)

	# Créer les 6 slots
	var equipe := PlayerData.equipe
	for i in range(6):
		var slot := _creer_slot(i, equipe[i] if i < equipe.size() else {})
		_slots.append(slot)

	# Instruction en bas
	var instr := Label.new()
	instr.text = "B: Retour"
	instr.position = Vector2(8, 300)
	instr.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

	_maj_selection()

func _creer_slot(index: int, pokemon_data: Dictionary) -> Dictionary:
	var y_pos := 24 + index * 46
	var slot_data := {}

	# Panel de fond du slot
	var panel := Panel.new()
	panel.position = Vector2(16, y_pos)
	panel.size = Vector2(448, 42)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.2, 0.35, 0.55, 0.8)
	style.set_border_width_all(1)
	style.border_color = Color(0.4, 0.5, 0.7)
	style.set_corner_radius_all(3)
	panel.add_theme_stylebox_override("panel", style)
	add_child(panel)
	slot_data["panel"] = panel
	slot_data["style"] = style

	if pokemon_data.is_empty():
		# Slot vide
		var label_vide := Label.new()
		label_vide.text = "---"
		label_vide.position = Vector2(48, 10)
		label_vide.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
		label_vide.add_theme_font_size_override("font_size", 12)
		panel.add_child(label_vide)
		slot_data["vide"] = true
		return slot_data

	slot_data["vide"] = false
	var espece_id: String = pokemon_data.get("espece_id", "001")

	# Icône du Pokémon
	var icon := TextureRect.new()
	var icon_path := "res://assets/sprites/pokemon/icons/%s.png" % espece_id
	if ResourceLoader.exists(icon_path):
		icon.texture = load(icon_path) as Texture2D
	icon.position = Vector2(4, 4)
	icon.size = Vector2(32, 32)
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	panel.add_child(icon)
	slot_data["icon"] = icon

	# Nom / surnom
	var label_nom := Label.new()
	label_nom.text = pokemon_data.get("surnom", "???")
	label_nom.position = Vector2(42, 2)
	label_nom.add_theme_color_override("font_color", Color.WHITE)
	label_nom.add_theme_font_size_override("font_size", 13)
	panel.add_child(label_nom)
	slot_data["label_nom"] = label_nom

	# Niveau
	var label_niv := Label.new()
	label_niv.text = "N.%d" % pokemon_data.get("niveau", 1)
	label_niv.position = Vector2(180, 2)
	label_niv.add_theme_color_override("font_color", Color(0.9, 0.9, 0.6))
	label_niv.add_theme_font_size_override("font_size", 12)
	panel.add_child(label_niv)
	slot_data["label_niv"] = label_niv

	# Barre PV
	var pv_act: int = pokemon_data.get("pv_actuels", 0)
	var pv_max: int = pokemon_data.get("stats", {}).get("pv", maxi(pv_act, 1))
	var barre := ProgressBar.new()
	barre.min_value = 0
	barre.max_value = pv_max
	barre.value = pv_act
	barre.show_percentage = false
	barre.position = Vector2(42, 22)
	barre.size = Vector2(160, 12)
	# Couleur selon ratio PV
	var ratio: float = float(pv_act) / float(maxi(pv_max, 1))
	var fill_style := StyleBoxFlat.new()
	if ratio > 0.5:
		fill_style.bg_color = Color(0.2, 0.8, 0.2)
	elif ratio > 0.2:
		fill_style.bg_color = Color(0.9, 0.7, 0.1)
	else:
		fill_style.bg_color = Color(0.9, 0.2, 0.2)
	fill_style.set_corner_radius_all(2)
	barre.add_theme_stylebox_override("fill", fill_style)
	var bg_style := StyleBoxFlat.new()
	bg_style.bg_color = Color(0.15, 0.15, 0.15)
	bg_style.set_corner_radius_all(2)
	barre.add_theme_stylebox_override("background", bg_style)
	panel.add_child(barre)
	slot_data["barre"] = barre

	# Texte PV
	var label_pv := Label.new()
	label_pv.text = "%d/%d" % [pv_act, pv_max]
	label_pv.position = Vector2(210, 20)
	label_pv.add_theme_color_override("font_color", Color.WHITE)
	label_pv.add_theme_font_size_override("font_size", 11)
	panel.add_child(label_pv)
	slot_data["label_pv"] = label_pv

	# Statut
	var statut: String = pokemon_data.get("statut", "")
	if not statut.is_empty():
		var label_statut := Label.new()
		label_statut.text = _abreger_statut(statut)
		label_statut.position = Vector2(280, 12)
		label_statut.add_theme_color_override("font_color", Color(1.0, 0.5, 0.3))
		label_statut.add_theme_font_size_override("font_size", 11)
		panel.add_child(label_statut)

	# Types
	var types: Array = pokemon_data.get("types", [])
	if not types.is_empty():
		var label_types := Label.new()
		label_types.text = "/".join(types).to_upper()
		label_types.position = Vector2(330, 12)
		label_types.add_theme_color_override("font_color", Color(0.7, 0.8, 1.0))
		label_types.add_theme_font_size_override("font_size", 10)
		panel.add_child(label_types)

	return slot_data

func _process(_delta: float) -> void:
	var nb_pokemon := PlayerData.equipe.size()
	if nb_pokemon == 0:
		if Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
			_fermer()
		return

	# Sous-menu actif
	if _sous_menu != null:
		_process_sous_menu()
		return

	# Mode échange
	if _mode_swap:
		if Input.is_action_just_pressed("action_haut"):
			_index = (_index - 1 + nb_pokemon) % nb_pokemon
			_maj_selection()
		elif Input.is_action_just_pressed("action_bas"):
			_index = (_index + 1) % nb_pokemon
			_maj_selection()
		elif Input.is_action_just_pressed("action_confirmer"):
			_executer_swap()
		elif Input.is_action_just_pressed("action_annuler"):
			_mode_swap = false
			_swap_source = -1
			_maj_selection()
		return

	if Input.is_action_just_pressed("action_haut"):
		_index = (_index - 1 + nb_pokemon) % nb_pokemon
		_maj_selection()
	elif Input.is_action_just_pressed("action_bas"):
		_index = (_index + 1) % nb_pokemon
		_maj_selection()
	elif Input.is_action_just_pressed("action_confirmer"):
		_ouvrir_sous_menu()
	elif Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
		_fermer()

func _maj_selection() -> void:
	for i in range(_slots.size()):
		if _slots[i].has("style"):
			var style: StyleBoxFlat = _slots[i]["style"]
			if i == _index:
				style.bg_color = Color(0.3, 0.5, 0.8, 0.9)
				style.border_color = Color(1, 1, 0.5)
				style.set_border_width_all(2)
			elif _mode_swap and i == _swap_source:
				# Source de l'échange en surbrillance verte
				style.bg_color = Color(0.2, 0.55, 0.3, 0.9)
				style.border_color = Color(0.5, 1, 0.5)
				style.set_border_width_all(2)
			else:
				style.bg_color = Color(0.2, 0.35, 0.55, 0.8)
				style.border_color = Color(0.4, 0.5, 0.7)
				style.set_border_width_all(1)

func _abreger_statut(statut: String) -> String:
	match statut:
		"brulure": return "BRL"
		"gel": return "GEL"
		"paralysie": return "PAR"
		"poison", "poison_grave": return "PSN"
		"sommeil": return "SOM"
	return ""

# --- Sous-menu d'actions ---
func _ouvrir_sous_menu() -> void:
	if _index >= PlayerData.equipe.size():
		return
	var poke_data: Dictionary = PlayerData.equipe[_index]
	var attaques: Array = poke_data.get("attaques", [])

	_sous_menu_options.clear()
	# Vérifier les CS overworld
	for att in attaques:
		var move_id: String = att.get("id", "")
		if CS_OVERWORLD.has(move_id):
			_sous_menu_options.append(move_id)
	# Options de base
	_sous_menu_options.append("ordre")
	_sous_menu_options.append("retour")

	_sous_menu_index = 0
	_sous_menu_labels.clear()

	# Créer le panel du sous-menu
	_sous_menu = Panel.new()
	_sous_menu.position = Vector2(300, 24 + _index * 46)
	_sous_menu.size = Vector2(140, _sous_menu_options.size() * 24 + 12)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(1, 1, 1, 0.95)
	style.border_color = Color(0.2, 0.2, 0.2)
	style.set_border_width_all(2)
	style.set_corner_radius_all(3)
	_sous_menu.add_theme_stylebox_override("panel", style)
	add_child(_sous_menu)

	for i in range(_sous_menu_options.size()):
		var lbl := Label.new()
		lbl.position = Vector2(8, 6 + i * 24)
		lbl.size = Vector2(124, 22)
		lbl.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
		lbl.add_theme_font_size_override("font_size", 12)
		_sous_menu.add_child(lbl)
		_sous_menu_labels.append(lbl)

	_maj_sous_menu()

func _process_sous_menu() -> void:
	if Input.is_action_just_pressed("action_haut"):
		_sous_menu_index = (_sous_menu_index - 1 + _sous_menu_options.size()) % _sous_menu_options.size()
		_maj_sous_menu()
	elif Input.is_action_just_pressed("action_bas"):
		_sous_menu_index = (_sous_menu_index + 1) % _sous_menu_options.size()
		_maj_sous_menu()
	elif Input.is_action_just_pressed("action_confirmer"):
		_selectionner_sous_menu()
	elif Input.is_action_just_pressed("action_annuler"):
		_fermer_sous_menu()

func _maj_sous_menu() -> void:
	for i in range(_sous_menu_labels.size()):
		var option: String = _sous_menu_options[i]
		var prefix := "▶ " if i == _sous_menu_index else "  "
		var texte := ""
		match option:
			"vol": texte = "VOL"
			"surf": texte = "SURF"
			"coupe": texte = "COUPE"
			"force": texte = "FORCE"
			"flash": texte = "FLASH"
			"ordre": texte = "ORDRE"
			"retour": texte = "RETOUR"
		_sous_menu_labels[i].text = prefix + texte

func _selectionner_sous_menu() -> void:
	var option: String = _sous_menu_options[_sous_menu_index]
	_fermer_sous_menu()

	match option:
		"vol":
			if FlySystem.peut_voler():
				_ouvrir_ecran_vol()
			else:
				pass  # TODO: afficher message "Impossible d'utiliser Vol ici"
		"surf":
			# Surf est géré par l'overworld, on ferme tout
			if SurfSystem.peut_surfer():
				emit_signal("action_cs", "surf")
				_fermer()
		"coupe":
			emit_signal("action_cs", "coupe")
			_fermer()
		"force":
			if StrengthSystem.peut_utiliser_force():
				emit_signal("action_cs", "force")
				_fermer()
		"flash":
			emit_signal("action_cs", "flash")
			_fermer()
		"ordre":
			_mode_swap = true
			_swap_source = _index
			_maj_selection()
		"retour":
			pass

func _fermer_sous_menu() -> void:
	if _sous_menu:
		_sous_menu.queue_free()
		_sous_menu = null
	_sous_menu_labels.clear()
	_sous_menu_options.clear()

func _ouvrir_ecran_vol() -> void:
	var fly_screen := CanvasLayer.new()
	fly_screen.set_script(load("res://scripts/ui/fly_screen.gd"))
	add_child(fly_screen)
	if fly_screen.has_signal("destination_choisie"):
		fly_screen.destination_choisie.connect(_on_vol_destination)
	if fly_screen.has_signal("ecran_ferme"):
		fly_screen.ecran_ferme.connect(_on_vol_annule)

func _on_vol_destination(carte_id: String) -> void:
	FlySystem.voler_vers(carte_id)

func _on_vol_annule() -> void:
	pass  # Retour au sous-menu, rien à faire

# --- Échange de Pokémon dans l'équipe ---
func _executer_swap() -> void:
	if _swap_source == _index:
		_mode_swap = false
		_swap_source = -1
		_maj_selection()
		return
	# Échanger les Pokémon
	var temp = PlayerData.equipe[_swap_source]
	PlayerData.equipe[_swap_source] = PlayerData.equipe[_index]
	PlayerData.equipe[_index] = temp
	_mode_swap = false
	_swap_source = -1
	# Rafraîchir l'affichage complet
	_rafraichir_slots()
	_maj_selection()

func _rafraichir_slots() -> void:
	# Supprimer les anciens slots visuels
	for slot in _slots:
		if slot.has("panel") and is_instance_valid(slot["panel"]):
			slot["panel"].queue_free()
	_slots.clear()
	# Recréer
	var equipe := PlayerData.equipe
	for i in range(6):
		var slot := _creer_slot(i, equipe[i] if i < equipe.size() else {})
		_slots.append(slot)

func _fermer() -> void:
	_fermer_sous_menu()
	emit_signal("ecran_ferme")
