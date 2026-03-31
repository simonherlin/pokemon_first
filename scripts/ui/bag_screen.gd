extends CanvasLayer

# BagScreen — Écran du sac (inventaire)
# Affiche les objets par catégorie avec navigation

signal ecran_ferme()

const CATEGORIES := ["objets", "balls", "objets_cles", "ct_cs"]
const NOMS_CATEGORIES := ["OBJETS", "BALLS", "OBJETS CLÉS", "CT/CS"]

var _index_cat: int = 0
var _index_item: int = 0
var _items_affiches: Array = []  # [{id, nom, quantite}]
var _labels_items: Array[Label] = []
var _label_cat: Label = null
var _label_desc: Label = null
var _scroll_offset: int = 0
const MAX_VISIBLE := 8

func _ready() -> void:
	layer = 85
	_creer_ui()
	_rafraichir_items()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.12, 0.18, 0.28, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre catégorie
	_label_cat = Label.new()
	_label_cat.text = NOMS_CATEGORIES[0]
	_label_cat.position = Vector2(180, 4)
	_label_cat.add_theme_color_override("font_color", Color.WHITE)
	_label_cat.add_theme_font_size_override("font_size", 16)
	add_child(_label_cat)

	# Navigation catégories
	var nav := Label.new()
	nav.text = "◄ ► Catégorie"
	nav.position = Vector2(12, 4)
	nav.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
	nav.add_theme_font_size_override("font_size", 10)
	add_child(nav)

	# Panel liste items
	var panel := Panel.new()
	panel.position = Vector2(16, 28)
	panel.size = Vector2(448, MAX_VISIBLE * 26 + 8)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.18, 0.22, 0.35, 0.9)
	style.set_border_width_all(2)
	style.border_color = Color(0.4, 0.5, 0.7)
	style.set_corner_radius_all(4)
	panel.add_theme_stylebox_override("panel", style)
	add_child(panel)

	# Labels items (pool de MAX_VISIBLE labels)
	for i in range(MAX_VISIBLE):
		var label := Label.new()
		label.position = Vector2(8, 4 + i * 26)
		label.size = Vector2(432, 24)
		label.add_theme_color_override("font_color", Color.WHITE)
		label.add_theme_font_size_override("font_size", 12)
		panel.add_child(label)
		_labels_items.append(label)

	# Description en bas
	_label_desc = Label.new()
	_label_desc.text = ""
	_label_desc.position = Vector2(24, 248)
	_label_desc.size = Vector2(440, 60)
	_label_desc.autowrap_mode = TextServer.AUTOWRAP_WORD
	_label_desc.add_theme_color_override("font_color", Color(0.8, 0.8, 0.8))
	_label_desc.add_theme_font_size_override("font_size", 11)
	add_child(_label_desc)

	# Instructions
	var instr := Label.new()
	instr.text = "B: Retour"
	instr.position = Vector2(8, 305)
	instr.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

func _rafraichir_items() -> void:
	_items_affiches.clear()
	_index_item = 0
	_scroll_offset = 0

	var categorie: String = CATEGORIES[_index_cat]
	_label_cat.text = NOMS_CATEGORIES[_index_cat]

	# Parcourir l'inventaire et filtrer par catégorie
	for item_id in PlayerData.inventaire:
		var quantite: int = PlayerData.inventaire[item_id]
		if quantite <= 0:
			continue
		var item_data: Dictionary = ItemsData.get_item(item_id)
		if item_data.is_empty():
			continue
		if item_data.get("categorie", "") == categorie:
			_items_affiches.append({
				"id": item_id,
				"nom": item_data.get("nom", item_id),
				"quantite": quantite,
				"description": item_data.get("description", "")
			})

	_maj_affichage()

func _maj_affichage() -> void:
	for i in range(MAX_VISIBLE):
		var idx := _scroll_offset + i
		if idx < _items_affiches.size():
			var item: Dictionary = _items_affiches[idx]
			var prefix := "▶ " if idx == _index_item else "  "
			_labels_items[i].text = prefix + "%s  ×%d" % [item["nom"], item["quantite"]]
			_labels_items[i].visible = true
		else:
			if i == 0 and _items_affiches.is_empty():
				_labels_items[i].text = "  (vide)"
				_labels_items[i].visible = true
			else:
				_labels_items[i].text = ""
				_labels_items[i].visible = false

	# Description de l'item sélectionné
	if _index_item < _items_affiches.size():
		_label_desc.text = _items_affiches[_index_item].get("description", "")
	else:
		_label_desc.text = ""

func _process(_delta: float) -> void:
	# Navigation catégories (gauche/droite)
	if Input.is_action_just_pressed("action_gauche"):
		_index_cat = (_index_cat - 1 + CATEGORIES.size()) % CATEGORIES.size()
		_rafraichir_items()
	elif Input.is_action_just_pressed("action_droite"):
		_index_cat = (_index_cat + 1) % CATEGORIES.size()
		_rafraichir_items()

	# Navigation items (haut/bas)
	if Input.is_action_just_pressed("action_haut") and _items_affiches.size() > 0:
		_index_item = (_index_item - 1 + _items_affiches.size()) % _items_affiches.size()
		_ajuster_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_bas") and _items_affiches.size() > 0:
		_index_item = (_index_item + 1) % _items_affiches.size()
		_ajuster_scroll()
		_maj_affichage()

	# Fermer
	if Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
		_fermer()

func _ajuster_scroll() -> void:
	if _index_item < _scroll_offset:
		_scroll_offset = _index_item
	elif _index_item >= _scroll_offset + MAX_VISIBLE:
		_scroll_offset = _index_item - MAX_VISIBLE + 1

func _fermer() -> void:
	emit_signal("ecran_ferme")
