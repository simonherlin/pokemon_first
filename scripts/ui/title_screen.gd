extends Control

# TitleScreen — Écran titre animé avec sélection Nouvelle Partie / Continuer

var _index: int = 0
var _options := ["nouvelle", "continuer"]
var _pret: bool = false
var _timer_intro: float = 0.0
var _timer_press_start: float = 0.0
var _etoiles: Array[Dictionary] = []
var _label_press_start: Label = null
var _label_version: Label = null
var _labels_etoiles: Array[Label] = []

@onready var label_nouvelle: Label = $VBox/LabelNouvelle
@onready var label_continuer: Label = $VBox/LabelContinuer

func _ready() -> void:
	_index = 0
	# Cacher le menu au début
	$VBox/LabelNouvelle.visible = false
	$VBox/LabelContinuer.visible = false
	# Jouer la musique du titre
	AudioManager.jouer_musique("res://assets/audio/music/titre.ogg", true)
	# Créer les étoiles de fond animées
	_creer_etoiles()
	# Créer le texte "Appuie sur A"
	_creer_press_start()
	# Créer le label version
	_creer_version()
	# Animation d'entrée du titre
	_animer_entree()

func _creer_etoiles() -> void:
	for i in range(30):
		var etoile := Label.new()
		etoile.text = ["·", "•", "✦", "✧", "★"][randi() % 5]
		var px := randf() * 480.0
		var py := randf() * 320.0
		etoile.position = Vector2(px, py)
		etoile.add_theme_font_size_override("font_size", randi_range(6, 12))
		var alpha := randf_range(0.1, 0.5)
		etoile.add_theme_color_override("font_color", Color(0.6, 0.7, 1.0, alpha))
		etoile.z_index = -1
		add_child(etoile)
		_labels_etoiles.append(etoile)
		_etoiles.append({
			"label": etoile,
			"phase": randf() * TAU,
			"vitesse": randf_range(1.5, 3.5),
			"alpha_base": alpha,
		})

func _creer_press_start() -> void:
	_label_press_start = Label.new()
	_label_press_start.text = "— Appuie sur A pour commencer —"
	_label_press_start.position = Vector2(100, 270)
	_label_press_start.add_theme_color_override("font_color", Color(0.7, 0.7, 0.8, 0.0))
	_label_press_start.add_theme_font_size_override("font_size", 11)
	add_child(_label_press_start)

func _creer_version() -> void:
	_label_version = Label.new()
	_label_version.text = "v1.0 — Fan Game Gen 1"
	_label_version.position = Vector2(155, 305)
	_label_version.add_theme_color_override("font_color", Color(0.3, 0.3, 0.4))
	_label_version.add_theme_font_size_override("font_size", 8)
	add_child(_label_version)

func _animer_entree() -> void:
	# Titre : slide depuis le haut + fondu
	var titre_node := $VBox/Title
	var subtitle_node := $VBox/Subtitle
	titre_node.modulate = Color(1, 1, 1, 0)
	subtitle_node.modulate = Color(1, 1, 1, 0)
	var pos_orig_titre := titre_node.position
	titre_node.position.y -= 30
	var tween := create_tween()
	tween.set_parallel(true)
	tween.tween_property(titre_node, "modulate:a", 1.0, 1.5).set_ease(Tween.EASE_OUT)
	tween.tween_property(titre_node, "position:y", pos_orig_titre.y, 1.2).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	tween.tween_property(subtitle_node, "modulate:a", 1.0, 1.5).set_delay(0.8)
	# Après l'animation, afficher "Press Start"
	tween.chain().tween_callback(_afficher_press_start).set_delay(0.5)

func _afficher_press_start() -> void:
	_pret = false
	var tween := create_tween()
	tween.tween_property(_label_press_start, "theme_override_colors/font_color:a", 0.8, 0.8)
	tween.tween_callback(func(): _pret = true)

func _process(delta: float) -> void:
	_timer_intro += delta
	# Animer les étoiles (scintillement)
	for data in _etoiles:
		data["phase"] += delta * data["vitesse"]
		var alpha := data["alpha_base"] + sin(data["phase"]) * 0.3
		var label: Label = data["label"]
		label.add_theme_color_override("font_color", Color(0.6, 0.7, 1.0, clampf(alpha, 0.05, 0.8)))
	# Animer le titre (couleur cyclique subtile)
	if has_node("VBox/Title"):
		var hue := fmod(_timer_intro * 0.03, 1.0)
		var titre_col := Color.from_hsv(hue, 0.15, 1.0)
		$VBox/Title.add_theme_color_override("font_color", titre_col)
	# Animer "Press Start" clignotant
	if _pret and not $VBox/LabelNouvelle.visible:
		_timer_press_start += delta
		var alpha := 0.4 + sin(_timer_press_start * 3.0) * 0.4
		_label_press_start.add_theme_color_override("font_color", Color(0.7, 0.7, 0.8, alpha))
		if Input.is_action_just_pressed("action_confirmer"):
			AudioManager.jouer_sfx("res://assets/audio/sfx/confirm.ogg")
			_label_press_start.visible = false
			$VBox/LabelNouvelle.visible = true
			$VBox/LabelContinuer.visible = true
			_mettre_a_jour_curseur()
			# Animation d'apparition du menu
			$VBox/LabelNouvelle.modulate = Color(1, 1, 1, 0)
			$VBox/LabelContinuer.modulate = Color(1, 1, 1, 0)
			var tw := create_tween()
			tw.set_parallel(true)
			tw.tween_property($VBox/LabelNouvelle, "modulate:a", 1.0, 0.4)
			tw.tween_property($VBox/LabelContinuer, "modulate:a", 1.0, 0.4).set_delay(0.15)
		return
	# Menu actif
	if not $VBox/LabelNouvelle.visible:
		return
	if Input.is_action_just_pressed("action_haut"):
		_index = (_index - 1 + _options.size()) % _options.size()
		AudioManager.jouer_sfx("res://assets/audio/sfx/cursor_move.ogg")
		_mettre_a_jour_curseur()
	elif Input.is_action_just_pressed("action_bas"):
		_index = (_index + 1) % _options.size()
		AudioManager.jouer_sfx("res://assets/audio/sfx/cursor_move.ogg")
		_mettre_a_jour_curseur()
	elif Input.is_action_just_pressed("action_confirmer"):
		AudioManager.jouer_sfx("res://assets/audio/sfx/confirm.ogg")
		_selectionner()

func _mettre_a_jour_curseur() -> void:
	label_nouvelle.text = ("▶ " if _index == 0 else "  ") + "Nouvelle Partie"
	label_continuer.text = ("▶ " if _index == 1 else "  ") + "Continuer"

func _selectionner() -> void:
	match _options[_index]:
		"nouvelle":
			SceneManager.charger_scene("res://scenes/ui/intro_scene.tscn")
		"continuer":
			if SaveManager.slot_existe(0):
				SaveManager.charger(0)
				var carte: String = PlayerData.carte_actuelle
				SceneManager.charger_scene("res://scenes/maps/%s.tscn" % carte)
			else:
				# Pas de sauvegarde — feedback visuel
				label_continuer.add_theme_color_override("font_color", Color(0.5, 0.3, 0.3))
				var tw := create_tween()
				tw.tween_property(label_continuer, "position:x", label_continuer.position.x + 4, 0.05)
				tw.tween_property(label_continuer, "position:x", label_continuer.position.x - 4, 0.05)
				tw.tween_property(label_continuer, "position:x", label_continuer.position.x, 0.05)
				AudioManager.jouer_sfx("res://assets/audio/sfx/cancel.ogg")
