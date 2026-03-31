extends CanvasLayer

# SaveScreen — Écran de sauvegarde
# Permet de choisir un slot (1-3) et confirmer la sauvegarde

signal ecran_ferme()

var _index: int = 0
var _labels: Array[Label] = []
var _en_confirmation: bool = false
var _label_confirm: Label = null
var _confirm_index: int = 1  # 0 = Oui, 1 = Non (défaut sur Non)

func _ready() -> void:
	layer = 85
	_creer_ui()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.1, 0.12, 0.2, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre
	var titre := Label.new()
	titre.text = "SAUVEGARDER"
	titre.position = Vector2(170, 8)
	titre.add_theme_color_override("font_color", Color.WHITE)
	titre.add_theme_font_size_override("font_size", 16)
	add_child(titre)

	# Créer les 3 slots
	for i in range(SaveManager.NB_SLOTS):
		_creer_slot(i)

	# Label de confirmation (caché par défaut)
	_label_confirm = Label.new()
	_label_confirm.position = Vector2(120, 260)
	_label_confirm.add_theme_color_override("font_color", Color.YELLOW)
	_label_confirm.add_theme_font_size_override("font_size", 14)
	_label_confirm.visible = false
	add_child(_label_confirm)

	# Instructions
	var instr := Label.new()
	instr.text = "B: Retour"
	instr.position = Vector2(8, 305)
	instr.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

	_maj_selection()

func _creer_slot(index: int) -> void:
	var y_pos := 36 + index * 80
	var panel := Panel.new()
	panel.position = Vector2(40, y_pos)
	panel.size = Vector2(400, 72)
	panel.name = "Slot%d" % index
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.15, 0.2, 0.35, 0.9)
	style.set_border_width_all(2)
	style.border_color = Color(0.4, 0.5, 0.7)
	style.set_corner_radius_all(4)
	panel.add_theme_stylebox_override("panel", style)
	add_child(panel)

	var label := Label.new()
	label.position = Vector2(12, 4)
	label.size = Vector2(376, 64)
	label.add_theme_color_override("font_color", Color.WHITE)
	label.add_theme_font_size_override("font_size", 12)

	var info := SaveManager.info_slot(index)
	if info.is_empty():
		label.text = "  SLOT %d\n  (vide)" % (index + 1)
	else:
		var temps_sec: int = info.get("temps_jeu", 0)
		var h := temps_sec / 3600
		var m := (temps_sec % 3600) / 60
		label.text = "  SLOT %d — %s\n  Badges: %d  Pokédex: %d  Temps: %dh%02d" % [
			index + 1,
			info.get("nom_joueur", "???"),
			info.get("badges", 0),
			info.get("pokedex", 0),
			h, m
		]
	panel.add_child(label)
	_labels.append(label)

func _process(_delta: float) -> void:
	if _en_confirmation:
		_gerer_confirmation()
		return

	if Input.is_action_just_pressed("action_haut"):
		_index = (_index - 1 + SaveManager.NB_SLOTS) % SaveManager.NB_SLOTS
		_maj_selection()
	elif Input.is_action_just_pressed("action_bas"):
		_index = (_index + 1) % SaveManager.NB_SLOTS
		_maj_selection()
	elif Input.is_action_just_pressed("action_confirmer"):
		_demander_confirmation()
	elif Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
		_fermer()

func _gerer_confirmation() -> void:
	if Input.is_action_just_pressed("action_gauche") or Input.is_action_just_pressed("action_droite"):
		_confirm_index = 1 - _confirm_index  # Toggle 0 ↔ 1
		_maj_confirmation()
	elif Input.is_action_just_pressed("action_confirmer"):
		if _confirm_index == 0:  # Oui
			_sauvegarder()
		_en_confirmation = false
		_label_confirm.visible = false
	elif Input.is_action_just_pressed("action_annuler"):
		_en_confirmation = false
		_label_confirm.visible = false

func _demander_confirmation() -> void:
	_en_confirmation = true
	_confirm_index = 1  # Défaut sur "Non" (action irréversible)
	_label_confirm.visible = true
	_maj_confirmation()

func _maj_confirmation() -> void:
	var oui_prefix := "▶ " if _confirm_index == 0 else "  "
	var non_prefix := "▶ " if _confirm_index == 1 else "  "
	_label_confirm.text = "Sauvegarder dans le Slot %d ?   %sOui   %sNon" % [_index + 1, oui_prefix, non_prefix]

func _sauvegarder() -> void:
	var ok := SaveManager.sauvegarder(_index)
	if ok:
		_label_confirm.text = "Sauvegarde réussie !"
		_label_confirm.add_theme_color_override("font_color", Color.GREEN)
	else:
		_label_confirm.text = "Erreur de sauvegarde !"
		_label_confirm.add_theme_color_override("font_color", Color.RED)
	_label_confirm.visible = true
	# Rafraîchir les infos du slot après sauvegarde
	await get_tree().create_timer(1.5).timeout
	_label_confirm.visible = false

func _maj_selection() -> void:
	for i in range(SaveManager.NB_SLOTS):
		var panel = get_node_or_null("Slot%d" % i)
		if panel:
			var style: StyleBoxFlat = panel.get_theme_stylebox("panel") as StyleBoxFlat
			if style:
				if i == _index:
					style.border_color = Color(1, 1, 0.5)
					style.set_border_width_all(3)
				else:
					style.border_color = Color(0.4, 0.5, 0.7)
					style.set_border_width_all(2)

func _fermer() -> void:
	emit_signal("ecran_ferme")
