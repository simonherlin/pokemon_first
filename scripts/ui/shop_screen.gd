extends CanvasLayer

# ShopScreen — Écran de la Boutique Pokémon
# Permet d'acheter des objets avec l'argent du joueur

signal ecran_ferme()

var items_en_vente: Array = []  # IDs des items disponibles
var _items_data: Array = []     # Données complètes [{id, nom, prix, desc}]
var _index: int = 0
var _labels: Array[Label] = []
var _label_argent: Label = null
var _label_desc: Label = null
var _label_message: Label = null
var _en_confirmation: bool = false
var _quantite: int = 1
const MAX_VISIBLE := 7

func _ready() -> void:
	layer = 85
	_charger_items()
	_creer_ui()

func _charger_items() -> void:
	for item_id in items_en_vente:
		var data: Dictionary = ItemsData.get_item(item_id)
		if not data.is_empty():
			_items_data.append({
				"id": item_id,
				"nom": data.get("nom", item_id),
				"prix": data.get("prix", 0),
				"description": data.get("description", "")
			})

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.1, 0.2, 0.15, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre
	var titre := Label.new()
	titre.text = "BOUTIQUE POKÉMON"
	titre.position = Vector2(150, 4)
	titre.add_theme_color_override("font_color", Color.WHITE)
	titre.add_theme_font_size_override("font_size", 16)
	add_child(titre)

	# Argent du joueur
	_label_argent = Label.new()
	_label_argent.text = "₽ %d" % PlayerData.argent
	_label_argent.position = Vector2(380, 4)
	_label_argent.add_theme_color_override("font_color", Color(1, 0.9, 0.3))
	_label_argent.add_theme_font_size_override("font_size", 14)
	add_child(_label_argent)

	# Panel liste
	var panel := Panel.new()
	panel.position = Vector2(16, 28)
	panel.size = Vector2(448, MAX_VISIBLE * 28 + 8)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.15, 0.25, 0.2, 0.9)
	style.set_border_width_all(2)
	style.border_color = Color(0.3, 0.6, 0.4)
	style.set_corner_radius_all(4)
	panel.add_theme_stylebox_override("panel", style)
	add_child(panel)

	# Labels des items
	for i in range(MAX_VISIBLE):
		var label := Label.new()
		label.position = Vector2(8, 4 + i * 28)
		label.size = Vector2(432, 26)
		label.add_theme_color_override("font_color", Color.WHITE)
		label.add_theme_font_size_override("font_size", 12)
		panel.add_child(label)
		_labels.append(label)

	# Description
	_label_desc = Label.new()
	_label_desc.position = Vector2(24, 240)
	_label_desc.size = Vector2(440, 40)
	_label_desc.autowrap_mode = TextServer.AUTOWRAP_WORD
	_label_desc.add_theme_color_override("font_color", Color(0.8, 0.9, 0.8))
	_label_desc.add_theme_font_size_override("font_size", 11)
	add_child(_label_desc)

	# Message (achat réussi, pas assez d'argent, etc.)
	_label_message = Label.new()
	_label_message.position = Vector2(120, 280)
	_label_message.add_theme_color_override("font_color", Color.GREEN)
	_label_message.add_theme_font_size_override("font_size", 13)
	_label_message.visible = false
	add_child(_label_message)

	# Instructions
	var instr := Label.new()
	instr.text = "A: Acheter  B: Retour"
	instr.position = Vector2(8, 305)
	instr.add_theme_color_override("font_color", Color(0.5, 0.6, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

	_maj_affichage()

func _process(_delta: float) -> void:
	if _en_confirmation:
		_gerer_confirmation()
		return

	if Input.is_action_just_pressed("action_haut") and _items_data.size() > 0:
		_index = (_index - 1 + _items_data.size()) % _items_data.size()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_bas") and _items_data.size() > 0:
		_index = (_index + 1) % _items_data.size()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_confirmer") and _items_data.size() > 0:
		_demarrer_achat()
	elif Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
		_fermer()

func _maj_affichage() -> void:
	for i in range(MAX_VISIBLE):
		if i < _items_data.size():
			var item: Dictionary = _items_data[i]
			var prefix := "▶ " if i == _index else "  "
			_labels[i].text = prefix + "%s   %d ₽" % [item["nom"], item["prix"]]
			_labels[i].visible = true
		else:
			if i == 0 and _items_data.is_empty():
				_labels[i].text = "  (Aucun article en vente)"
			else:
				_labels[i].text = ""
			_labels[i].visible = i == 0

	# Description
	if _index < _items_data.size():
		_label_desc.text = _items_data[_index].get("description", "")
	else:
		_label_desc.text = ""

func _demarrer_achat() -> void:
	_en_confirmation = true
	_quantite = 1
	_label_message.visible = true
	_maj_message_achat()

func _gerer_confirmation() -> void:
	if Input.is_action_just_pressed("action_haut"):
		_quantite = mini(_quantite + 1, 99)
		_maj_message_achat()
	elif Input.is_action_just_pressed("action_bas"):
		_quantite = maxi(_quantite - 1, 1)
		_maj_message_achat()
	elif Input.is_action_just_pressed("action_confirmer"):
		_confirmer_achat()
	elif Input.is_action_just_pressed("action_annuler"):
		_en_confirmation = false
		_label_message.visible = false

func _maj_message_achat() -> void:
	var item: Dictionary = _items_data[_index]
	var cout: int = item["prix"] * _quantite
	_label_message.text = "%s ×%d = %d ₽  (▲▼ quantité, A: acheter, B: annuler)" % [item["nom"], _quantite, cout]
	if cout > PlayerData.argent:
		_label_message.add_theme_color_override("font_color", Color.RED)
	else:
		_label_message.add_theme_color_override("font_color", Color.YELLOW)

func _confirmer_achat() -> void:
	var item: Dictionary = _items_data[_index]
	var cout: int = item["prix"] * _quantite
	if PlayerData.depenser_argent(cout):
		PlayerData.ajouter_item(item["id"], _quantite)
		_label_message.text = "%s ×%d acheté !" % [item["nom"], _quantite]
		_label_message.add_theme_color_override("font_color", Color.GREEN)
		_label_argent.text = "₽ %d" % PlayerData.argent
	else:
		_label_message.text = "Pas assez d'argent !"
		_label_message.add_theme_color_override("font_color", Color.RED)
	_en_confirmation = false
	# Cacher le message après un délai
	await get_tree().create_timer(1.5).timeout
	_label_message.visible = false

func _fermer() -> void:
	emit_signal("ecran_ferme")
