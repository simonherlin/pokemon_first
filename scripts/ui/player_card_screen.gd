extends CanvasLayer

# PlayerCardScreen — Carte du dresseur
# Affiche : nom, argent, badges, temps de jeu, Pokédex stats

signal ecran_ferme()

func _ready() -> void:
	layer = 85
	_creer_ui()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.1, 0.15, 0.3, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre
	var titre := Label.new()
	titre.text = "CARTE DRESSEUR"
	titre.position = Vector2(160, 8)
	titre.add_theme_color_override("font_color", Color.WHITE)
	titre.add_theme_font_size_override("font_size", 16)
	add_child(titre)

	# Panel principal
	var panel := Panel.new()
	panel.position = Vector2(40, 36)
	panel.size = Vector2(400, 250)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.2, 0.25, 0.45, 0.9)
	style.set_border_width_all(3)
	style.border_color = Color(0.5, 0.6, 0.9)
	style.set_corner_radius_all(6)
	panel.add_theme_stylebox_override("panel", style)
	add_child(panel)

	# Nom du joueur
	_ajouter_ligne(panel, "NOM:", PlayerData.nom_joueur, 12)
	# ID Dresseur
	_ajouter_ligne(panel, "ID N°:", str(PlayerData.id_joueur).lpad(5, "0"), 38)
	# Argent
	_ajouter_ligne(panel, "ARGENT:", "%d ₽" % PlayerData.argent, 64)
	# Temps de jeu
	var total_sec := GameManager.temps_jeu_secondes
	var heures := total_sec / 3600
	var minutes := (total_sec % 3600) / 60
	_ajouter_ligne(panel, "TEMPS:", "%dh %02dmin" % [heures, minutes], 90)
	# Pokédex
	_ajouter_ligne(panel, "POKÉDEX:", "Vus: %d  Capturés: %d" % [PlayerData.pokedex_vu.size(), PlayerData.pokedex_capture.size()], 116)

	# Badges
	var label_badges := Label.new()
	label_badges.text = "BADGES:"
	label_badges.position = Vector2(16, 148)
	label_badges.add_theme_color_override("font_color", Color(0.7, 0.8, 1.0))
	label_badges.add_theme_font_size_override("font_size", 13)
	panel.add_child(label_badges)

	# Afficher les 8 badges
	var noms_badges := ["Pierre", "Cascade", "Foudre", "Arc-en-ciel", "Âme", "Marais", "Volcan", "Terre"]
	for i in range(8):
		var badge_label := Label.new()
		var col := i % 4
		var row := i / 4
		badge_label.position = Vector2(16 + col * 95, 172 + row * 30)
		if GameManager.badges[i]:
			badge_label.text = "★ %s" % noms_badges[i]
			badge_label.add_theme_color_override("font_color", Color(1, 0.85, 0.2))
		else:
			badge_label.text = "☆ %s" % noms_badges[i]
			badge_label.add_theme_color_override("font_color", Color(0.4, 0.4, 0.4))
		badge_label.add_theme_font_size_override("font_size", 11)
		panel.add_child(badge_label)

	# Instructions
	var instr := Label.new()
	instr.text = "B: Retour"
	instr.position = Vector2(8, 305)
	instr.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

func _ajouter_ligne(parent: Control, key: String, value: String, y: float) -> void:
	var label_key := Label.new()
	label_key.text = key
	label_key.position = Vector2(16, y)
	label_key.add_theme_color_override("font_color", Color(0.7, 0.8, 1.0))
	label_key.add_theme_font_size_override("font_size", 13)
	parent.add_child(label_key)

	var label_val := Label.new()
	label_val.text = value
	label_val.position = Vector2(140, y)
	label_val.add_theme_color_override("font_color", Color.WHITE)
	label_val.add_theme_font_size_override("font_size", 13)
	parent.add_child(label_val)

func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
		_fermer()

func _fermer() -> void:
	emit_signal("ecran_ferme")
