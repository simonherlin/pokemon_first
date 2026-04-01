extends CanvasLayer

# BattleBagScreen — Sac utilisable en combat
# Filtré : potions, balls, antidotes (pas d'objets clés, pas de CT)

signal item_choisi(item_id: String)
signal ecran_ferme()

const CATEGORIES_COMBAT := ["objets", "balls"]
const NOMS_CATEGORIES := ["SOINS", "BALLS"]
const MAX_VISIBLE := 7

var _index_cat: int = 0
var _index_item: int = 0
var _items_affiches: Array = []
var _labels: Array[Label] = []
var _label_cat: Label = null
var _label_desc: Label = null
var _scroll_offset: int = 0

func _ready() -> void:
	layer = 90
	_creer_ui()
	_rafraichir_items()

func _creer_ui() -> void:
	var fond := ColorRect.new()
	fond.color = Color(0.12, 0.18, 0.28, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	_label_cat = Label.new()
	_label_cat.text = NOMS_CATEGORIES[0]
	_label_cat.position = Vector2(180, 4)
	_label_cat.add_theme_color_override("font_color", Color.WHITE)
	_label_cat.add_theme_font_size_override("font_size", 16)
	add_child(_label_cat)

	var nav := Label.new()
	nav.text = "◄ ► Catégorie"
	nav.position = Vector2(12, 4)
	nav.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
	nav.add_theme_font_size_override("font_size", 10)
	add_child(nav)

	var panel := Panel.new()
	panel.position = Vector2(16, 28)
	panel.size = Vector2(448, MAX_VISIBLE * 28 + 8)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.18, 0.22, 0.35, 0.9)
	style.set_border_width_all(2)
	style.border_color = Color(0.4, 0.5, 0.7)
	style.set_corner_radius_all(4)
	panel.add_theme_stylebox_override("panel", style)
	add_child(panel)

	for i in range(MAX_VISIBLE):
		var label := Label.new()
		label.position = Vector2(8, 4 + i * 28)
		label.size = Vector2(432, 26)
		label.add_theme_color_override("font_color", Color.WHITE)
		label.add_theme_font_size_override("font_size", 12)
		panel.add_child(label)
		_labels.append(label)

	_label_desc = Label.new()
	_label_desc.position = Vector2(24, 240)
	_label_desc.size = Vector2(440, 40)
	_label_desc.autowrap_mode = TextServer.AUTOWRAP_WORD
	_label_desc.add_theme_color_override("font_color", Color(0.8, 0.9, 0.8))
	_label_desc.add_theme_font_size_override("font_size", 11)
	add_child(_label_desc)

	var instr := Label.new()
	instr.text = "A: Utiliser  B: Retour  ◄►: Catégorie"
	instr.position = Vector2(8, 305)
	instr.add_theme_color_override("font_color", Color(0.5, 0.6, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

func _rafraichir_items() -> void:
	_items_affiches.clear()
	_index_item = 0
	_scroll_offset = 0
	_label_cat.text = NOMS_CATEGORIES[_index_cat]
	var categorie: String = CATEGORIES_COMBAT[_index_cat]
	for item_id in PlayerData.inventaire:
		var quantite: int = PlayerData.inventaire[item_id]
		if quantite <= 0:
			continue
		var item_data: Dictionary = ItemsData.get_item(item_id)
		if item_data.is_empty():
			continue
		var cat_item: String = item_data.get("categorie", "")
		if cat_item == categorie:
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
			_labels[i].text = prefix + "%s  ×%d" % [item["nom"], item["quantite"]]
			_labels[i].visible = true
		else:
			if i == 0 and _items_affiches.is_empty():
				_labels[i].text = "  (vide)"
				_labels[i].visible = true
			else:
				_labels[i].text = ""
				_labels[i].visible = false
	if _index_item < _items_affiches.size():
		_label_desc.text = _items_affiches[_index_item].get("description", "")
	else:
		_label_desc.text = ""

func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("action_gauche"):
		_index_cat = (_index_cat - 1 + CATEGORIES_COMBAT.size()) % CATEGORIES_COMBAT.size()
		_rafraichir_items()
	elif Input.is_action_just_pressed("action_droite"):
		_index_cat = (_index_cat + 1) % CATEGORIES_COMBAT.size()
		_rafraichir_items()
	elif Input.is_action_just_pressed("action_haut") and _items_affiches.size() > 0:
		_index_item = (_index_item - 1 + _items_affiches.size()) % _items_affiches.size()
		_ajuster_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_bas") and _items_affiches.size() > 0:
		_index_item = (_index_item + 1) % _items_affiches.size()
		_ajuster_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_confirmer") and _items_affiches.size() > 0:
		var item: Dictionary = _items_affiches[_index_item]
		emit_signal("item_choisi", item["id"])
	elif Input.is_action_just_pressed("action_annuler"):
		emit_signal("ecran_ferme")

func _ajuster_scroll() -> void:
	if _index_item < _scroll_offset:
		_scroll_offset = _index_item
	elif _index_item >= _scroll_offset + MAX_VISIBLE:
		_scroll_offset = _index_item - MAX_VISIBLE + 1
