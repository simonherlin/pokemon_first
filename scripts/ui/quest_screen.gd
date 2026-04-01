extends CanvasLayer

# QuestScreen — Écran de journal de quêtes
# Affiche les quêtes principales et secondaires avec leur progression

signal ecran_ferme()

# --- État ---
var _actif: bool = true
var _index: int = 0
var _onglet: int = 0  # 0 = principales, 1 = secondaires
var _quetes_affichees: Array = []
var _scroll_offset: int = 0
const MAX_VISIBLE := 6

# --- Nœuds UI ---
var _fond: ColorRect = null
var _panel_liste: Panel = null
var _panel_detail: Panel = null
var _labels_quetes: Array[Label] = []
var _label_onglet: Label = null
var _label_titre_detail: Label = null
var _label_desc_detail: RichTextLabel = null
var _labels_etapes: Array[Label] = []
var _label_compteur: Label = null
var _label_instructions: Label = null

func _ready() -> void:
	layer = 90
	_creer_ui()
	_charger_onglet()
	_maj_affichage()

func _creer_ui() -> void:
	# --- Fond sombre ---
	_fond = ColorRect.new()
	_fond.color = Color(0, 0, 0, 0.7)
	_fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_fond)

	# --- En-tête avec onglets ---
	_label_onglet = Label.new()
	_label_onglet.position = Vector2(16, 8)
	_label_onglet.size = Vector2(448, 24)
	_label_onglet.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_onglet.add_theme_color_override("font_color", Color(1.0, 0.9, 0.4))
	_label_onglet.add_theme_font_size_override("font_size", 15)
	add_child(_label_onglet)

	# --- Panel liste des quêtes (gauche) ---
	_panel_liste = Panel.new()
	_panel_liste.position = Vector2(8, 36)
	_panel_liste.size = Vector2(200, MAX_VISIBLE * 32 + 16)
	var style_liste := StyleBoxFlat.new()
	style_liste.bg_color = Color(0.12, 0.15, 0.25, 0.95)
	style_liste.border_color = Color(0.5, 0.55, 0.7)
	style_liste.set_border_width_all(2)
	style_liste.set_corner_radius_all(4)
	_panel_liste.add_theme_stylebox_override("panel", style_liste)
	add_child(_panel_liste)

	# Labels de la liste
	for i in range(MAX_VISIBLE):
		var label := Label.new()
		label.position = Vector2(8, 8 + i * 32)
		label.size = Vector2(184, 28)
		label.add_theme_font_size_override("font_size", 12)
		label.clip_text = true
		_labels_quetes.append(label)
		_panel_liste.add_child(label)

	# --- Panel détail (droite) ---
	_panel_detail = Panel.new()
	_panel_detail.position = Vector2(216, 36)
	_panel_detail.size = Vector2(256, MAX_VISIBLE * 32 + 16)
	var style_detail := StyleBoxFlat.new()
	style_detail.bg_color = Color(0.15, 0.12, 0.22, 0.95)
	style_detail.border_color = Color(0.5, 0.45, 0.65)
	style_detail.set_border_width_all(2)
	style_detail.set_corner_radius_all(4)
	_panel_detail.add_theme_stylebox_override("panel", style_detail)
	add_child(_panel_detail)

	# Titre de la quête sélectionnée
	_label_titre_detail = Label.new()
	_label_titre_detail.position = Vector2(8, 4)
	_label_titre_detail.size = Vector2(240, 22)
	_label_titre_detail.add_theme_color_override("font_color", Color(1.0, 0.85, 0.3))
	_label_titre_detail.add_theme_font_size_override("font_size", 13)
	_label_titre_detail.clip_text = true
	_panel_detail.add_child(_label_titre_detail)

	# Description
	_label_desc_detail = RichTextLabel.new()
	_label_desc_detail.position = Vector2(8, 26)
	_label_desc_detail.size = Vector2(240, 44)
	_label_desc_detail.bbcode_enabled = false
	_label_desc_detail.scroll_active = false
	_label_desc_detail.add_theme_color_override("default_color", Color(0.8, 0.8, 0.85))
	_label_desc_detail.add_theme_font_size_override("normal_font_size", 10)
	_panel_detail.add_child(_label_desc_detail)

	# Étapes (jusqu'à 5)
	for i in range(5):
		var label := Label.new()
		label.position = Vector2(12, 74 + i * 22)
		label.size = Vector2(232, 20)
		label.add_theme_font_size_override("font_size", 11)
		label.clip_text = true
		_labels_etapes.append(label)
		_panel_detail.add_child(label)

	# Compteur en bas
	_label_compteur = Label.new()
	_label_compteur.position = Vector2(8, MAX_VISIBLE * 32 - 4)
	_label_compteur.size = Vector2(240, 18)
	_label_compteur.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_label_compteur.add_theme_color_override("font_color", Color(0.6, 0.6, 0.65))
	_label_compteur.add_theme_font_size_override("font_size", 10)
	_panel_detail.add_child(_label_compteur)

	# Instructions en bas de l'écran
	_label_instructions = Label.new()
	_label_instructions.position = Vector2(8, 36 + MAX_VISIBLE * 32 + 20)
	_label_instructions.size = Vector2(464, 20)
	_label_instructions.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_instructions.add_theme_color_override("font_color", Color(0.5, 0.5, 0.55))
	_label_instructions.add_theme_font_size_override("font_size", 10)
	_label_instructions.text = "◄► Onglets   ▲▼ Navigation   B Retour"
	add_child(_label_instructions)

func _process(_delta: float) -> void:
	if not _actif:
		return

	if Input.is_action_just_pressed("action_haut"):
		if _quetes_affichees.size() > 0:
			_index = (_index - 1 + _quetes_affichees.size()) % _quetes_affichees.size()
			_ajuster_scroll()
			_maj_affichage()
	elif Input.is_action_just_pressed("action_bas"):
		if _quetes_affichees.size() > 0:
			_index = (_index + 1) % _quetes_affichees.size()
			_ajuster_scroll()
			_maj_affichage()
	elif Input.is_action_just_pressed("action_gauche") or Input.is_action_just_pressed("action_droite"):
		_onglet = 1 - _onglet
		_index = 0
		_scroll_offset = 0
		_charger_onglet()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_annuler"):
		_fermer()

func _charger_onglet() -> void:
	if _onglet == 0:
		_quetes_affichees = QuestManager.get_quetes_principales()
	else:
		_quetes_affichees = QuestManager.get_quetes_secondaires()
	# Trier : actives en premier, terminées ensuite, verrouillées en dernier
	_quetes_affichees.sort_custom(func(a, b):
		return a.get("etat", 0) < b.get("etat", 0) or \
			(a.get("etat", 0) == b.get("etat", 0) and \
			 a.get("etapes_terminees", 0) > b.get("etapes_terminees", 0))
	)

func _ajuster_scroll() -> void:
	if _index < _scroll_offset:
		_scroll_offset = _index
	elif _index >= _scroll_offset + MAX_VISIBLE:
		_scroll_offset = _index - MAX_VISIBLE + 1

func _maj_affichage() -> void:
	# --- Onglets ---
	var onglet_main := "▶ PRINCIPALES ◀" if _onglet == 0 else "  PRINCIPALES  "
	var onglet_side := "▶ SECONDAIRES ◀" if _onglet == 1 else "  SECONDAIRES  "
	_label_onglet.text = onglet_main + "    " + onglet_side

	# --- Liste des quêtes ---
	for i in range(MAX_VISIBLE):
		var idx_quete := _scroll_offset + i
		if idx_quete >= _quetes_affichees.size():
			_labels_quetes[i].text = ""
			_labels_quetes[i].visible = false
			continue
		_labels_quetes[i].visible = true
		var q: Dictionary = _quetes_affichees[idx_quete]
		var etat: int = q.get("etat", 0)
		var prefix := "▶ " if idx_quete == _index else "  "
		var marqueur := ""
		match etat:
			QuestManager.EtatQuete.TERMINEE:
				marqueur = "✓ "
				_labels_quetes[i].add_theme_color_override("font_color", Color(0.4, 0.8, 0.4))
			QuestManager.EtatQuete.ACTIVE:
				marqueur = "● "
				_labels_quetes[i].add_theme_color_override("font_color", Color(1.0, 1.0, 1.0))
			QuestManager.EtatQuete.VERROUILLEE:
				marqueur = "🔒 "
				_labels_quetes[i].add_theme_color_override("font_color", Color(0.45, 0.45, 0.5))
		_labels_quetes[i].text = prefix + marqueur + q.get("nom", "???")

	# --- Détail de la quête sélectionnée ---
	if _quetes_affichees.is_empty():
		_label_titre_detail.text = "Aucune quête"
		_label_desc_detail.text = ""
		for label in _labels_etapes:
			label.text = ""
		_label_compteur.text = ""
		return

	var quete: Dictionary = _quetes_affichees[clampi(_index, 0, _quetes_affichees.size() - 1)]
	var etat_q: int = quete.get("etat", 0)

	# Titre
	_label_titre_detail.text = quete.get("nom", "???")

	# Description
	if etat_q == QuestManager.EtatQuete.VERROUILLEE:
		_label_desc_detail.text = "???"
	else:
		_label_desc_detail.text = quete.get("description", "")

	# Étapes
	var etapes: Array = quete.get("etapes", [])
	for i in range(5):
		if i >= etapes.size():
			_labels_etapes[i].text = ""
			_labels_etapes[i].visible = false
			continue
		_labels_etapes[i].visible = true
		var etape: Dictionary = etapes[i]
		if etat_q == QuestManager.EtatQuete.VERROUILLEE:
			_labels_etapes[i].text = "  ???"
			_labels_etapes[i].add_theme_color_override("font_color", Color(0.4, 0.4, 0.45))
		elif etape.get("terminee", false):
			_labels_etapes[i].text = "  ✓ " + etape.get("description", "")
			_labels_etapes[i].add_theme_color_override("font_color", Color(0.4, 0.8, 0.4))
		else:
			_labels_etapes[i].text = "  ○ " + etape.get("description", "")
			_labels_etapes[i].add_theme_color_override("font_color", Color(0.85, 0.85, 0.9))

	# Compteur de progression
	var terminees: int = quete.get("etapes_terminees", 0)
	var total: int = quete.get("etapes_total", 0)
	if etat_q == QuestManager.EtatQuete.TERMINEE:
		_label_compteur.text = "✓ Terminée"
		_label_compteur.add_theme_color_override("font_color", Color(0.4, 0.8, 0.4))
	elif etat_q == QuestManager.EtatQuete.VERROUILLEE:
		_label_compteur.text = "Verrouillée"
		_label_compteur.add_theme_color_override("font_color", Color(0.5, 0.5, 0.55))
	else:
		_label_compteur.text = "%d/%d" % [terminees, total]
		_label_compteur.add_theme_color_override("font_color", Color(0.7, 0.7, 0.75))

func _fermer() -> void:
	_actif = false
	emit_signal("ecran_ferme")
	queue_free()
