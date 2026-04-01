# options_screen.gd — Écran Options (volume musique/SFX, vitesse texte)
extends CanvasLayer

signal ecran_ferme()

# Options disponibles
const LABELS := ["Volume Musique", "Volume SFX", "Vitesse Texte", "Retour"]
const VITESSES_TEXTE := ["Lent", "Normal", "Rapide"]

var _index: int = 0
var _actif: bool = true
var _volume_musique: float = 0.8
var _volume_sfx: float = 1.0
var _vitesse_texte_index: int = 1  # 0=lent, 1=normal, 2=rapide

# UI
var _panel: Panel = null
var _labels: Array[Label] = []
var _valeurs: Array[Label] = []

func _ready() -> void:
	layer = 90
	# Charger les valeurs actuelles
	_volume_musique = AudioManager._volume_musique
	_volume_sfx = AudioManager._volume_sfx
	# Vitesse texte depuis GameManager (flag)
	var vt = GameManager.get_flag("vitesse_texte")
	if vt is int or vt is float:
		_vitesse_texte_index = clampi(int(vt), 0, 2)
	_creer_ui()
	_maj_affichage()

func _creer_ui() -> void:
	# Fond semi-transparent
	var fond := ColorRect.new()
	fond.color = Color(0, 0, 0, 0.5)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Panel central
	_panel = Panel.new()
	_panel.position = Vector2(80, 60)
	_panel.size = Vector2(320, 200)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.95, 0.95, 0.95, 0.98)
	style.border_color = Color(0.2, 0.2, 0.2)
	style.set_border_width_all(3)
	style.set_corner_radius_all(6)
	_panel.add_theme_stylebox_override("panel", style)
	add_child(_panel)

	# Titre
	var titre := Label.new()
	titre.text = "OPTIONS"
	titre.position = Vector2(120, 8)
	titre.add_theme_color_override("font_color", Color(0.15, 0.15, 0.15))
	titre.add_theme_font_size_override("font_size", 16)
	_panel.add_child(titre)

	# Labels et valeurs
	for i in range(LABELS.size()):
		var label := Label.new()
		label.text = "  " + LABELS[i]
		label.position = Vector2(12, 44 + i * 36)
		label.size = Vector2(180, 30)
		label.add_theme_color_override("font_color", Color(0.1, 0.1, 0.1))
		label.add_theme_font_size_override("font_size", 13)
		_labels.append(label)
		_panel.add_child(label)

		# Valeur à droite (sauf Retour)
		var valeur := Label.new()
		valeur.position = Vector2(200, 44 + i * 36)
		valeur.size = Vector2(100, 30)
		valeur.add_theme_color_override("font_color", Color(0.3, 0.3, 0.7))
		valeur.add_theme_font_size_override("font_size", 13)
		_valeurs.append(valeur)
		_panel.add_child(valeur)

func _process(_delta: float) -> void:
	if not _actif:
		return
	if Input.is_action_just_pressed("action_haut"):
		_index = (_index - 1 + LABELS.size()) % LABELS.size()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_bas"):
		_index = (_index + 1) % LABELS.size()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_gauche"):
		_ajuster_valeur(-1)
	elif Input.is_action_just_pressed("action_droite"):
		_ajuster_valeur(1)
	elif Input.is_action_just_pressed("action_confirmer"):
		if _index == LABELS.size() - 1:
			_fermer()
	elif Input.is_action_just_pressed("action_annuler"):
		_fermer()

func _ajuster_valeur(direction: int) -> void:
	match _index:
		0:  # Volume Musique
			_volume_musique = clampf(_volume_musique + direction * 0.1, 0.0, 1.0)
			AudioManager.set_volume_musique(_volume_musique)
		1:  # Volume SFX
			_volume_sfx = clampf(_volume_sfx + direction * 0.1, 0.0, 1.0)
			AudioManager.set_volume_sfx(_volume_sfx)
		2:  # Vitesse Texte
			_vitesse_texte_index = clampi(_vitesse_texte_index + direction, 0, 2)
			GameManager.set_flag("vitesse_texte", _vitesse_texte_index)
	_maj_affichage()

func _maj_affichage() -> void:
	# Curseur
	for i in range(_labels.size()):
		var prefix := "▶ " if i == _index else "  "
		_labels[i].text = prefix + LABELS[i]

	# Valeurs
	_valeurs[0].text = "◀ %d%% ▶" % int(_volume_musique * 100)
	_valeurs[1].text = "◀ %d%% ▶" % int(_volume_sfx * 100)
	_valeurs[2].text = "◀ %s ▶" % VITESSES_TEXTE[_vitesse_texte_index]
	_valeurs[3].text = ""  # Retour n'a pas de valeur

func _fermer() -> void:
	# Sauvegarder les options dans les flags
	GameManager.set_flag("volume_musique", _volume_musique)
	GameManager.set_flag("volume_sfx", _volume_sfx)
	GameManager.set_flag("vitesse_texte", _vitesse_texte_index)
	_actif = false
	emit_signal("ecran_ferme")
	queue_free()
