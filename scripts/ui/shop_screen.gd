extends CanvasLayer

# ShopScreen — Écran de la Boutique Pokémon
# Permet d'acheter et vendre des objets

signal ecran_ferme()

var items_en_vente: Array = []  # IDs des items disponibles
var _items_data: Array = []     # Données affichées [{id, nom, prix, desc}]
var _index: int = 0
var _scroll_offset: int = 0
var _labels: Array[Label] = []
var _label_argent: Label = null
var _label_desc: Label = null
var _label_message: Label = null
var _label_mode: Label = null
var _instr_label: Label = null
var _en_confirmation: bool = false
var _quantite: int = 1
var _mode: String = "acheter"  # "acheter" ou "vendre"
const MAX_VISIBLE := 7

func _ready() -> void:
	layer = 85
	_charger_items_achat()
	_creer_ui()

func _charger_items_achat() -> void:
	_items_data.clear()
	for item_id in items_en_vente:
		var data: Dictionary = ItemsData.get_item(item_id)
		if not data.is_empty() and data.get("prix", 0) > 0:
			_items_data.append({
				"id": item_id,
				"nom": data.get("nom", item_id),
				"prix": data.get("prix", 0),
				"description": data.get("description", "")
			})

func _charger_items_vente() -> void:
	_items_data.clear()
	for item_id in PlayerData.inventaire:
		var quantite: int = PlayerData.inventaire[item_id]
		if quantite <= 0:
			continue
		var data: Dictionary = ItemsData.get_item(item_id)
		if data.is_empty():
			continue
		var prix_vente: int = int(data.get("prix", 0) / 2)
		if prix_vente <= 0:
			continue
		# Ne pas vendre les objets clés
		if data.get("categorie", "") == "objets_cles":
			continue
		_items_data.append({
			"id": item_id,
			"nom": data.get("nom", item_id),
			"prix": prix_vente,
			"quantite": quantite,
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

	# Mode (Acheter / Vendre)
	_label_mode = Label.new()
	_label_mode.text = "ACHETER"
	_label_mode.position = Vector2(16, 4)
	_label_mode.add_theme_color_override("font_color", Color(0.3, 1.0, 0.3))
	_label_mode.add_theme_font_size_override("font_size", 14)
	add_child(_label_mode)

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

	# Message
	_label_message = Label.new()
	_label_message.position = Vector2(120, 280)
	_label_message.add_theme_color_override("font_color", Color.GREEN)
	_label_message.add_theme_font_size_override("font_size", 13)
	_label_message.visible = false
	add_child(_label_message)

	# Instructions
	_instr_label = Label.new()
	_instr_label.text = "A: Acheter  L/R: Acheter/Vendre  B: Retour"
	_instr_label.position = Vector2(8, 305)
	_instr_label.add_theme_color_override("font_color", Color(0.5, 0.6, 0.5))
	_instr_label.add_theme_font_size_override("font_size", 10)
	add_child(_instr_label)

	_maj_affichage()

func _process(_delta: float) -> void:
	if _en_confirmation:
		_gerer_confirmation()
		return

	# Changer de mode avec ◄ ►
	if Input.is_action_just_pressed("action_gauche") or Input.is_action_just_pressed("action_droite"):
		_basculer_mode()
		return

	if Input.is_action_just_pressed("action_haut") and _items_data.size() > 0:
		_index = (_index - 1 + _items_data.size()) % _items_data.size()
		_maj_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_bas") and _items_data.size() > 0:
		_index = (_index + 1) % _items_data.size()
		_maj_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_confirmer") and _items_data.size() > 0:
		_demarrer_transaction()
	elif Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
		_fermer()

func _basculer_mode() -> void:
	if _mode == "acheter":
		_mode = "vendre"
		_label_mode.text = "VENDRE"
		_label_mode.add_theme_color_override("font_color", Color(1.0, 0.6, 0.3))
		_charger_items_vente()
	else:
		_mode = "acheter"
		_label_mode.text = "ACHETER"
		_label_mode.add_theme_color_override("font_color", Color(0.3, 1.0, 0.3))
		_charger_items_achat()
	_index = 0
	_scroll_offset = 0
	_maj_affichage()

func _maj_scroll() -> void:
	if _index < _scroll_offset:
		_scroll_offset = _index
	elif _index >= _scroll_offset + MAX_VISIBLE:
		_scroll_offset = _index - MAX_VISIBLE + 1

func _maj_affichage() -> void:
	for i in range(MAX_VISIBLE):
		var data_idx := _scroll_offset + i
		if data_idx < _items_data.size():
			var item: Dictionary = _items_data[data_idx]
			var prefix := "▶ " if data_idx == _index else "  "
			if _mode == "vendre":
				_labels[i].text = prefix + "%s  ×%d  %d ₽" % [item["nom"], item.get("quantite", 1), item["prix"]]
			else:
				_labels[i].text = prefix + "%s   %d ₽" % [item["nom"], item["prix"]]
			_labels[i].visible = true
		else:
			if i == 0 and _items_data.is_empty():
				_labels[i].text = "  (Rien à %s)" % ("vendre" if _mode == "vendre" else "acheter")
			else:
				_labels[i].text = ""
			_labels[i].visible = i == 0

	if _index < _items_data.size():
		_label_desc.text = _items_data[_index].get("description", "")
	else:
		_label_desc.text = ""

func _demarrer_transaction() -> void:
	_en_confirmation = true
	_quantite = 1
	_label_message.visible = true
	_maj_message_transaction()

func _gerer_confirmation() -> void:
	if Input.is_action_just_pressed("action_haut"):
		var max_q := 99
		if _mode == "vendre":
			max_q = _items_data[_index].get("quantite", 1)
		_quantite = mini(_quantite + 1, max_q)
		_maj_message_transaction()
	elif Input.is_action_just_pressed("action_bas"):
		_quantite = maxi(_quantite - 1, 1)
		_maj_message_transaction()
	elif Input.is_action_just_pressed("action_confirmer"):
		_confirmer_transaction()
	elif Input.is_action_just_pressed("action_annuler"):
		_en_confirmation = false
		_label_message.visible = false

func _maj_message_transaction() -> void:
	var item: Dictionary = _items_data[_index]
	var cout: int = item["prix"] * _quantite
	if _mode == "acheter":
		_label_message.text = "%s ×%d = %d ₽  (▲▼ quantité, A: acheter, B: annuler)" % [item["nom"], _quantite, cout]
		if cout > PlayerData.argent:
			_label_message.add_theme_color_override("font_color", Color.RED)
		else:
			_label_message.add_theme_color_override("font_color", Color.YELLOW)
	else:
		_label_message.text = "Vendre %s ×%d = %d ₽  (▲▼ quantité, A: vendre, B: annuler)" % [item["nom"], _quantite, cout]
		_label_message.add_theme_color_override("font_color", Color.YELLOW)

func _confirmer_transaction() -> void:
	var item: Dictionary = _items_data[_index]
	var cout: int = item["prix"] * _quantite

	if _mode == "acheter":
		if PlayerData.depenser_argent(cout):
			PlayerData.ajouter_item(item["id"], _quantite)
			_label_message.text = "%s ×%d acheté !" % [item["nom"], _quantite]
			_label_message.add_theme_color_override("font_color", Color.GREEN)
		else:
			_label_message.text = "Pas assez d'argent !"
			_label_message.add_theme_color_override("font_color", Color.RED)
	else:
		# Vendre
		if PlayerData.retirer_item(item["id"], _quantite):
			PlayerData.ajouter_argent(cout)
			_label_message.text = "%s ×%d vendu pour %d ₽ !" % [item["nom"], _quantite, cout]
			_label_message.add_theme_color_override("font_color", Color.GREEN)
			# Rafraîchir la liste de vente
			_charger_items_vente()
			_index = mini(_index, maxi(0, _items_data.size() - 1))
			_scroll_offset = mini(_scroll_offset, maxi(0, _items_data.size() - MAX_VISIBLE))
		else:
			_label_message.text = "Erreur de vente !"
			_label_message.add_theme_color_override("font_color", Color.RED)

	_en_confirmation = false
	_label_argent.text = "₽ %d" % PlayerData.argent
	_maj_affichage()
	# Cacher le message après un délai
	await get_tree().create_timer(1.5).timeout
	_label_message.visible = false

func _fermer() -> void:
	emit_signal("ecran_ferme")
