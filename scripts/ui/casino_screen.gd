extends CanvasLayer

# CasinoScreen — Machine à sous du Casino de Céladopole
# 3 rouleaux, 6 symboles, gains selon combinaisons

signal ecran_ferme()

# --- Symboles et gains ---
const SYMBOLES := ["7", "BAR", "🍒", "⚡", "★", "◆"]
const COULEURS_SYMBOLES := {
	"7": Color(1, 0.2, 0.2),       # Rouge
	"BAR": Color(0.3, 0.3, 0.9),   # Bleu
	"🍒": Color(0.9, 0.2, 0.4),    # Rose
	"⚡": Color(1.0, 0.9, 0.2),    # Jaune
	"★": Color(1.0, 0.7, 0.2),     # Or
	"◆": Color(0.5, 0.9, 0.5),     # Vert
}
const GAINS := {
	"777": 300,
	"BARBARBAR": 100,
	"🍒🍒🍒": 50,
	"⚡⚡⚡": 25,
	"★★★": 15,
	"◆◆◆": 15,
	"🍒🍒": 8,   # 2 cerises (le 3e est différent)
}
const COUT_PARTIE := 3
const MAX_JETONS := 9999

# --- État ---
var _rouleaux: Array[String] = ["7", "7", "7"]
var _en_rotation: bool = false
var _labels_rouleaux: Array[Label] = []
var _label_jetons: Label = null
var _label_message: Label = null
var _label_gain: Label = null
var _timer_rouleaux: Array[float] = [0.0, 0.0, 0.0]
var _vitesse_rouleaux: Array[float] = [0.0, 0.0, 0.0]
var _rouleau_stoppe: Array[bool] = [false, false, false]
var _animation_index: int = 0

func _ready() -> void:
	layer = 90
	_creer_ui()
	_maj_jetons()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.08, 0.1, 0.15, 0.97)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre
	var titre := Label.new()
	titre.text = "🎰 MACHINE À SOUS 🎰"
	titre.position = Vector2(120, 8)
	titre.add_theme_color_override("font_color", Color(1.0, 0.85, 0.2))
	titre.add_theme_font_size_override("font_size", 18)
	add_child(titre)

	# Cadre des rouleaux
	var cadre := Panel.new()
	cadre.position = Vector2(80, 50)
	cadre.size = Vector2(320, 120)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.05, 0.1)
	style.set_border_width_all(3)
	style.border_color = Color(0.8, 0.6, 0.1)
	style.set_corner_radius_all(6)
	cadre.add_theme_stylebox_override("panel", style)
	add_child(cadre)

	# Labels des rouleaux (3)
	for i in range(3):
		var label := Label.new()
		label.position = Vector2(25 + i * 105, 20)
		label.size = Vector2(80, 80)
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		label.add_theme_font_size_override("font_size", 40)
		label.text = SYMBOLES[0]
		cadre.add_child(label)
		_labels_rouleaux.append(label)

	# Séparateurs
	for i in range(2):
		var sep := Label.new()
		sep.text = "│"
		sep.position = Vector2(100 + (i + 1) * 105, 30)
		sep.size = Vector2(10, 60)
		sep.add_theme_font_size_override("font_size", 50)
		sep.add_theme_color_override("font_color", Color(0.5, 0.4, 0.1))
		cadre.add_child(sep)

	# Jetons
	_label_jetons = Label.new()
	_label_jetons.position = Vector2(80, 185)
	_label_jetons.add_theme_color_override("font_color", Color(1.0, 0.9, 0.4))
	_label_jetons.add_theme_font_size_override("font_size", 14)
	add_child(_label_jetons)

	# Message
	_label_message = Label.new()
	_label_message.position = Vector2(80, 210)
	_label_message.size = Vector2(320, 30)
	_label_message.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_message.add_theme_color_override("font_color", Color.WHITE)
	_label_message.add_theme_font_size_override("font_size", 12)
	_label_message.text = "Appuyez sur A pour lancer !"
	add_child(_label_message)

	# Gain
	_label_gain = Label.new()
	_label_gain.position = Vector2(80, 235)
	_label_gain.size = Vector2(320, 30)
	_label_gain.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_gain.add_theme_color_override("font_color", Color(0.3, 1.0, 0.3))
	_label_gain.add_theme_font_size_override("font_size", 14)
	_label_gain.text = ""
	add_child(_label_gain)

	# Table des gains
	var table := Label.new()
	table.text = "777=300  BAR×3=100  🍒×3=50  ⚡×3=25  ★/◆×3=15  🍒×2=8"
	table.position = Vector2(35, 265)
	table.size = Vector2(420, 20)
	table.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	table.add_theme_color_override("font_color", Color(0.5, 0.5, 0.6))
	table.add_theme_font_size_override("font_size", 8)
	add_child(table)

	# Instructions
	var instr := Label.new()
	instr.text = "A: Lancer (3 jetons)   B: Quitter"
	instr.position = Vector2(110, 290)
	instr.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

func _maj_jetons() -> void:
	if _label_jetons:
		_label_jetons.text = "💰 Jetons : %d" % PlayerData.jetons

func _process(delta: float) -> void:
	if _en_rotation:
		_animer_rouleaux(delta)
		return

	if Input.is_action_just_pressed("action_confirmer"):
		_lancer_rouleaux()
	elif Input.is_action_just_pressed("action_annuler"):
		emit_signal("ecran_ferme")
		queue_free()

func _lancer_rouleaux() -> void:
	# Vérifier les jetons
	if not PlayerData.possede_item("jeton_casino"):
		_label_message.text = "Il te faut un Porte-Jetons !"
		return
	if PlayerData.jetons < COUT_PARTIE:
		_label_message.text = "Pas assez de jetons ! (besoin de %d)" % COUT_PARTIE
		return
	PlayerData.jetons -= COUT_PARTIE
	_maj_jetons()
	_label_gain.text = ""
	_label_message.text = "Les rouleaux tournent..."
	# Lancer l'animation
	_en_rotation = true
	_rouleau_stoppe = [false, false, false]
	_timer_rouleaux = [0.0, 0.0, 0.0]
	_vitesse_rouleaux = [12.0, 12.0, 12.0]
	_animation_index = 0
	# Déterminer les résultats finaux à l'avance
	for i in range(3):
		_rouleaux[i] = SYMBOLES[randi() % SYMBOLES.size()]

func _animer_rouleaux(delta: float) -> void:
	for i in range(3):
		if _rouleau_stoppe[i]:
			continue
		_timer_rouleaux[i] += delta
		_vitesse_rouleaux[i] *= 0.995  # Décélération progressive
		# Changer le symbole affiché rapidement
		if fmod(_timer_rouleaux[i], 0.08) < delta:
			_labels_rouleaux[i].text = SYMBOLES[randi() % SYMBOLES.size()]
			_labels_rouleaux[i].add_theme_color_override("font_color", Color.WHITE)
		# Arrêter ce rouleau après un délai (cascade)
		var delai_stop := 0.8 + i * 0.5
		if _timer_rouleaux[i] >= delai_stop:
			_rouleau_stoppe[i] = true
			_labels_rouleaux[i].text = _rouleaux[i]
			var couleur: Color = COULEURS_SYMBOLES.get(_rouleaux[i], Color.WHITE)
			_labels_rouleaux[i].add_theme_color_override("font_color", couleur)
			AudioManager.jouer_sfx("res://assets/audio/sfx/confirm.ogg")
	# Tous arrêtés ?
	if _rouleau_stoppe[0] and _rouleau_stoppe[1] and _rouleau_stoppe[2]:
		_en_rotation = false
		_evaluer_resultat()

func _evaluer_resultat() -> void:
	var r := _rouleaux
	var gain := 0
	# 3 identiques
	if r[0] == r[1] and r[1] == r[2]:
		match r[0]:
			"7":
				gain = 300
				_label_message.text = "🎉 JACKPOT ! 🎉"
			"BAR":
				gain = 100
				_label_message.text = "💰 GROS GAIN !"
			"🍒":
				gain = 50
				_label_message.text = "🍒 Triple cerise !"
			"⚡":
				gain = 25
				_label_message.text = "⚡ Électrisant !"
			_:
				gain = 15
				_label_message.text = "✨ Triple !"
	# 2 cerises
	elif (r[0] == "🍒" and r[1] == "🍒") or (r[1] == "🍒" and r[2] == "🍒") or (r[0] == "🍒" and r[2] == "🍒"):
		gain = 8
		_label_message.text = "🍒 Deux cerises !"
	else:
		_label_message.text = "Pas de chance... Réessaie !"

	if gain > 0:
		PlayerData.jetons = mini(PlayerData.jetons + gain, MAX_JETONS)
		_label_gain.text = "+%d jetons !" % gain
		AudioManager.jouer_sfx("res://assets/audio/sfx/level_up.ogg")
	_maj_jetons()
