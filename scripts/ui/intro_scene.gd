extends Control

# IntroScene — Séquence d'introduction du Professeur Chen
# Reproduction fidèle de l'intro de Pokémon Rouge/Bleu FRLG
# 1. Discours du Professeur Chen avec portrait + Pokémon
# 2. Choix du nom du joueur
# 3. Choix du nom du rival
# 4. Transition vers le jeu (chambre du joueur à Bourg Palette)

enum Phase {
	DISCOURS_CHEN,
	NOM_JOUEUR,
	NOM_RIVAL,
	TRANSITION
}

var _phase: Phase = Phase.DISCOURS_CHEN
var _index_dialogue: int = 0
var _nom_joueur: String = ""
var _nom_rival: String = ""

# --- Dialogues du Professeur Chen ---
var _dialogues_chen := [
	"Bonjour ! Bienvenue dans le\nmonde des POKÉMON !",
	"Mon nom est CHEN.\nLes gens m'appellent le PROF. POKÉMON.",
	"Ce monde est peuplé de créatures\nappelées POKÉMON.",
	"Certains les utilisent comme\nanimaux domestiques, d'autres\nles font combattre.",
	"Moi, j'étudie les POKÉMON.\nJ'en ai fait ma profession.",
	"Mais d'abord, dis-moi\ncomment tu t'appelles."
]

# --- Nœuds UI ---
var _fond: ColorRect = null
var _sprite_chen: Sprite2D = null
var _sprite_pokemon: Sprite2D = null
var _sprite_joueur_preview: Sprite2D = null
var _sprite_rival_preview: Sprite2D = null
var _label_dialogue: Label = null
var _label_instruction: Label = null
var _panel_nom: Panel = null
var _label_titre_nom: Label = null
var _labels_predefs: Array[Label] = []
var _index_predef: int = 0
var _noms_predefs_joueur := ["Red", "Sacha", "Pierre", "Max"]
var _noms_predefs_rival := ["Régis", "Blue", "Paul", "Hugo"]

# --- Typewriter ---
var _typewriter_timer: float = 0.0
var _typewriter_texte_complet: String = ""
var _typewriter_index: int = 0
var _typewriter_actif: bool = false

# --- Animation ---
var _anim_timer: float = 0.0
var _stars: Array[Dictionary] = []
var _panel_dialogue: Panel = null


func _ready() -> void:
	_creer_ui()
	# Lancer la musique d'intro
	AudioManager.jouer_musique("res://assets/audio/music/intro_chen.ogg")
	# Fondu d'entrée depuis noir
	modulate = Color(1, 1, 1, 0)
	var tween_entree := create_tween()
	tween_entree.tween_property(self, "modulate:a", 1.0, 1.5)
	tween_entree.tween_callback(_demarrer_dialogue).set_delay(0.5)


func _demarrer_dialogue() -> void:
	_afficher_dialogue_typewriter()


func _creer_ui() -> void:
	# --- Fond sombre ---
	_fond = ColorRect.new()
	_fond.color = Color(0.02, 0.02, 0.08, 1.0)
	_fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(_fond)

	# --- Étoiles décoratives ---
	_creer_etoiles()

	# --- Portrait du Prof. Chen (sprite dresseur HD Scale3x) ---
	_sprite_chen = Sprite2D.new()
	var chen_tex := load("res://assets/sprites/trainers/professor_oak_hd.png") as Texture2D
	if chen_tex:
		_sprite_chen.texture = chen_tex
		_sprite_chen.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_sprite_chen.position = Vector2(240, 100)
	_sprite_chen.scale = Vector2(1.0, 1.0)
	add_child(_sprite_chen)

	# --- Sprite Pokémon (Nidorino — apparaît pendant le dialogue) ---
	_sprite_pokemon = Sprite2D.new()
	var nido_tex := load("res://assets/sprites/pokemon/front/034.png") as Texture2D
	if nido_tex:
		_sprite_pokemon.texture = nido_tex
		_sprite_pokemon.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_sprite_pokemon.position = Vector2(380, 110)
	_sprite_pokemon.scale = Vector2(2.0, 2.0)
	_sprite_pokemon.visible = false
	add_child(_sprite_pokemon)

	# --- Sprite joueur (mini preview — apparaît pendant le nommage) ---
	_sprite_joueur_preview = Sprite2D.new()
	var joueur_tex := load("res://assets/sprites/characters/red_normal_bas_0.png") as Texture2D
	if joueur_tex:
		_sprite_joueur_preview.texture = joueur_tex
		_sprite_joueur_preview.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_sprite_joueur_preview.position = Vector2(240, 90)
	_sprite_joueur_preview.scale = Vector2(2.5, 2.5)
	_sprite_joueur_preview.visible = false
	add_child(_sprite_joueur_preview)

	# --- Sprite rival (mini preview — apparaît pendant le nommage) ---
	_sprite_rival_preview = Sprite2D.new()
	var rival_tex := load("res://assets/sprites/trainers/rival_early.png") as Texture2D
	if rival_tex:
		_sprite_rival_preview.texture = rival_tex
		_sprite_rival_preview.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_sprite_rival_preview.position = Vector2(240, 90)
	_sprite_rival_preview.scale = Vector2(2.5, 2.5)
	_sprite_rival_preview.visible = false
	add_child(_sprite_rival_preview)

	# --- Cadre de dialogue (style Pokémon classique — fond blanc, bordure noire) ---
	_panel_dialogue = Panel.new()
	_panel_dialogue.position = Vector2(16, 216)
	_panel_dialogue.size = Vector2(448, 96)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(1.0, 1.0, 1.0, 0.95)
	style.set_border_width_all(3)
	style.border_color = Color(0.2, 0.2, 0.3)
	style.set_corner_radius_all(4)
	_panel_dialogue.add_theme_stylebox_override("panel", style)
	add_child(_panel_dialogue)

	_label_dialogue = Label.new()
	_label_dialogue.position = Vector2(14, 10)
	_label_dialogue.size = Vector2(420, 76)
	_label_dialogue.autowrap_mode = TextServer.AUTOWRAP_WORD
	_label_dialogue.add_theme_color_override("font_color", Color(0.1, 0.1, 0.15))
	_label_dialogue.add_theme_font_size_override("font_size", 14)
	_panel_dialogue.add_child(_label_dialogue)

	# Petite flèche clignotante pour indiquer suite
	_label_instruction = Label.new()
	_label_instruction.position = Vector2(426, 70)
	_label_instruction.add_theme_color_override("font_color", Color(0.3, 0.3, 0.4))
	_label_instruction.add_theme_font_size_override("font_size", 12)
	_label_instruction.text = "▼"
	_panel_dialogue.add_child(_label_instruction)

	# --- Panel de choix de nom (initialement caché) ---
	_panel_nom = Panel.new()
	_panel_nom.position = Vector2(80, 20)
	_panel_nom.size = Vector2(320, 140)
	var style_nom := StyleBoxFlat.new()
	style_nom.bg_color = Color(1.0, 1.0, 1.0, 0.95)
	style_nom.set_border_width_all(3)
	style_nom.border_color = Color(0.2, 0.2, 0.3)
	style_nom.set_corner_radius_all(4)
	_panel_nom.add_theme_stylebox_override("panel", style_nom)
	_panel_nom.visible = false
	add_child(_panel_nom)

	_label_titre_nom = Label.new()
	_label_titre_nom.position = Vector2(20, 10)
	_label_titre_nom.add_theme_color_override("font_color", Color(0.1, 0.1, 0.15))
	_label_titre_nom.add_theme_font_size_override("font_size", 14)
	_panel_nom.add_child(_label_titre_nom)

	# Labels pour les noms prédéfinis (grille 2x2)
	for i in range(4):
		var label := Label.new()
		label.position = Vector2(30 + (i % 2) * 140, 45 + (i / 2) * 35)
		label.add_theme_color_override("font_color", Color(0.1, 0.1, 0.15))
		label.add_theme_font_size_override("font_size", 13)
		_labels_predefs.append(label)
		_panel_nom.add_child(label)


func _creer_etoiles() -> void:
	for i in range(30):
		var star := {
			"x": randf() * 480.0,
			"y": randf() * 200.0,
			"speed": randf_range(0.3, 1.0),
			"size": randf_range(1.0, 2.5),
			"phase": randf() * TAU
		}
		_stars.append(star)


func _afficher_dialogue_typewriter() -> void:
	if _index_dialogue < _dialogues_chen.size():
		_typewriter_texte_complet = _dialogues_chen[_index_dialogue]
		_typewriter_index = 0
		_typewriter_actif = true
		_typewriter_timer = 0.0
		_label_dialogue.text = ""
		_maj_sprites_dialogue()


func _maj_sprites_dialogue() -> void:
	match _index_dialogue:
		0, 1:
			_sprite_chen.visible = true
			_sprite_pokemon.visible = false
		2, 3:
			_sprite_chen.visible = true
			_sprite_pokemon.visible = true
			_sprite_pokemon.modulate.a = 0.0
			var tw := create_tween()
			tw.tween_property(_sprite_pokemon, "modulate:a", 1.0, 0.5)
		4:
			_sprite_pokemon.visible = true
		5:
			_sprite_pokemon.visible = false


func _process(delta: float) -> void:
	_anim_timer += delta
	queue_redraw()

	# Clignotement de la flèche
	if _label_instruction:
		_label_instruction.visible = not _typewriter_actif and fmod(_anim_timer, 0.8) < 0.5

	# Typewriter
	if _typewriter_actif:
		_typewriter_timer += delta
		var vitesse := 0.03
		if Input.is_action_pressed("action_confirmer"):
			vitesse = 0.005
		if _typewriter_timer >= vitesse:
			_typewriter_timer = 0.0
			if _typewriter_index < _typewriter_texte_complet.length():
				_typewriter_index += 1
				_label_dialogue.text = _typewriter_texte_complet.substr(0, _typewriter_index)
				if _typewriter_index % 3 == 0:
					AudioManager.jouer_sfx("res://assets/audio/sfx/text_advance.ogg")
			else:
				_typewriter_actif = false
		return

	match _phase:
		Phase.DISCOURS_CHEN:
			_gerer_discours()
		Phase.NOM_JOUEUR:
			_gerer_choix_nom(true)
		Phase.NOM_RIVAL:
			_gerer_choix_nom(false)
		Phase.TRANSITION:
			pass


func _draw() -> void:
	for star in _stars:
		var alpha := 0.3 + sin(_anim_timer * star["speed"] + star["phase"]) * 0.3
		var col := Color(1, 1, 1, alpha)
		var s: float = star["size"]
		draw_rect(Rect2(star["x"] - s * 0.5, star["y"] - s * 0.5, s, s), col)


func _gerer_discours() -> void:
	if Input.is_action_just_pressed("action_confirmer"):
		AudioManager.jouer_sfx("res://assets/audio/sfx/confirm.ogg")
		_index_dialogue += 1
		if _index_dialogue < _dialogues_chen.size():
			_afficher_dialogue_typewriter()
		else:
			_phase = Phase.NOM_JOUEUR
			_sprite_chen.visible = false
			_sprite_pokemon.visible = false
			_sprite_joueur_preview.visible = true
			_afficher_choix_nom("Quel est ton nom ?", _noms_predefs_joueur)


func _afficher_choix_nom(titre: String, noms: Array) -> void:
	_panel_nom.visible = true
	_label_titre_nom.text = titre
	_label_dialogue.text = titre
	_index_predef = 0
	for i in range(4):
		if i < noms.size():
			_labels_predefs[i].text = noms[i]
			_labels_predefs[i].visible = true
		else:
			_labels_predefs[i].visible = false
	_maj_curseur_nom()


func _maj_curseur_nom() -> void:
	var noms: Array = _noms_predefs_joueur if _phase == Phase.NOM_JOUEUR else _noms_predefs_rival
	for i in range(_labels_predefs.size()):
		if i < noms.size():
			_labels_predefs[i].text = ("▶ " if i == _index_predef else "  ") + noms[i]


func _gerer_choix_nom(est_joueur: bool) -> void:
	var noms: Array = _noms_predefs_joueur if est_joueur else _noms_predefs_rival
	if Input.is_action_just_pressed("action_haut"):
		if _index_predef >= 2:
			_index_predef -= 2
			AudioManager.jouer_sfx("res://assets/audio/sfx/cursor_move.ogg")
			_maj_curseur_nom()
	elif Input.is_action_just_pressed("action_bas"):
		if _index_predef + 2 < noms.size():
			_index_predef += 2
			AudioManager.jouer_sfx("res://assets/audio/sfx/cursor_move.ogg")
			_maj_curseur_nom()
	elif Input.is_action_just_pressed("action_gauche"):
		if _index_predef % 2 > 0:
			_index_predef -= 1
			AudioManager.jouer_sfx("res://assets/audio/sfx/cursor_move.ogg")
			_maj_curseur_nom()
	elif Input.is_action_just_pressed("action_droite"):
		if _index_predef % 2 < 1 and _index_predef + 1 < noms.size():
			_index_predef += 1
			AudioManager.jouer_sfx("res://assets/audio/sfx/cursor_move.ogg")
			_maj_curseur_nom()
	elif Input.is_action_just_pressed("action_confirmer"):
		AudioManager.jouer_sfx("res://assets/audio/sfx/confirm.ogg")
		var nom_choisi: String = noms[_index_predef]
		if est_joueur:
			_nom_joueur = nom_choisi
			_panel_nom.visible = false
			_label_dialogue.text = "Donc ton nom est %s !" % nom_choisi
			await get_tree().create_timer(1.5).timeout
			_sprite_joueur_preview.visible = false
			_sprite_rival_preview.visible = true
			_label_dialogue.text = "Et quel est le nom de ton rival ?"
			await get_tree().create_timer(1.0).timeout
			_phase = Phase.NOM_RIVAL
			_afficher_choix_nom("Nom du rival ?", _noms_predefs_rival)
		else:
			_nom_rival = nom_choisi
			_panel_nom.visible = false
			_sprite_rival_preview.visible = false
			_sprite_chen.visible = true
			_label_dialogue.text = "Ah oui ! Je me souviens !\nSon nom est %s !" % nom_choisi
			await get_tree().create_timer(1.5).timeout
			_lancer_jeu()


func _lancer_jeu() -> void:
	_phase = Phase.TRANSITION
	_label_dialogue.text = "%s ! Ton aventure POKÉMON\ncommence maintenant !" % _nom_joueur
	AudioManager.jouer_sfx("res://assets/audio/sfx/confirm.ogg")

	# Fondu de sortie
	var tween_sortie := create_tween()
	tween_sortie.tween_property(self, "modulate:a", 0.0, 1.5).set_delay(2.0)
	await tween_sortie.finished

	# Initialiser la partie
	GameManager.nouvelle_partie()
	GameManager.nom_rival = _nom_rival
	GameManager.set_flag("rival_nomme", true)
	GameManager.set_flag("intro_terminee", true)
	PlayerData.nouvelle_partie(_nom_joueur)

	# Pas d'items de départ : le joueur les recevra du Prof. Chen au labo
	# Position initiale : chambre du joueur à Bourg Palette (2e étage)
	PlayerData.sauvegarder_position("maison_joueur_2f", 4, 4, "bas")

	# Charger la chambre du joueur
	SceneManager.charger_scene("res://scenes/maps/maison_joueur_2f.tscn", {
		"carte_id": "maison_joueur_2f"
	})
