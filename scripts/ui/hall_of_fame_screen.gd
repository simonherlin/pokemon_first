# hall_of_fame_screen.gd — Écran du Panthéon (Hall of Fame)
# Affiché après la victoire contre le Champion de la Ligue Pokémon
# Montre chaque Pokémon de l'équipe du joueur avec une animation
extends CanvasLayer

signal ecran_ferme()

# --- État ---
var _index_pokemon: int = 0
var _phase: String = "intro"  # "intro", "affichage", "fin"
var _timer: float = 0.0

# --- Nœuds UI ---
var _fond: ColorRect = null
var _panel: Panel = null
var _titre: Label = null
var _sprite_pokemon: Sprite2D = null
var _label_nom: Label = null
var _label_espece: Label = null
var _label_niveau: Label = null
var _label_id: Label = null
var _label_congratulations: Label = null
var _particules: Array[ColorRect] = []

func _ready() -> void:
	layer = 95

	# Fond noir
	_fond = ColorRect.new()
	_fond.color = Color(0, 0, 0, 1)
	_fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_fond)

	# Titre
	_titre = Label.new()
	_titre.text = "✦ PANTHÉON ✦"
	_titre.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_titre.position = Vector2(0, 12)
	_titre.size = Vector2(480, 30)
	_titre.add_theme_color_override("font_color", Color(1, 0.85, 0.2))
	_titre.add_theme_font_size_override("font_size", 20)
	add_child(_titre)

	# Panel central pour le Pokémon
	_panel = Panel.new()
	_panel.position = Vector2(120, 50)
	_panel.size = Vector2(240, 200)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.05, 0.15, 0.9)
	style.border_color = Color(1, 0.85, 0.2)
	style.set_border_width_all(2)
	style.set_corner_radius_all(8)
	_panel.add_theme_stylebox_override("panel", style)
	add_child(_panel)

	# Sprite du Pokémon (placeholder — sera rempli)
	_sprite_pokemon = Sprite2D.new()
	_sprite_pokemon.position = Vector2(120, 70)
	_sprite_pokemon.scale = Vector2(2.0, 2.0)
	_panel.add_child(_sprite_pokemon)

	# Labels d'info
	_label_nom = Label.new()
	_label_nom.position = Vector2(10, 130)
	_label_nom.size = Vector2(220, 20)
	_label_nom.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_nom.add_theme_color_override("font_color", Color.WHITE)
	_label_nom.add_theme_font_size_override("font_size", 16)
	_panel.add_child(_label_nom)

	_label_espece = Label.new()
	_label_espece.position = Vector2(10, 152)
	_label_espece.size = Vector2(220, 18)
	_label_espece.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_espece.add_theme_color_override("font_color", Color(0.7, 0.7, 0.9))
	_label_espece.add_theme_font_size_override("font_size", 12)
	_panel.add_child(_label_espece)

	_label_niveau = Label.new()
	_label_niveau.position = Vector2(10, 172)
	_label_niveau.size = Vector2(220, 18)
	_label_niveau.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_niveau.add_theme_color_override("font_color", Color(0.9, 0.9, 0.5))
	_label_niveau.add_theme_font_size_override("font_size", 13)
	_panel.add_child(_label_niveau)

	_label_id = Label.new()
	_label_id.position = Vector2(0, 270)
	_label_id.size = Vector2(480, 20)
	_label_id.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_id.add_theme_color_override("font_color", Color(0.5, 0.5, 0.6))
	_label_id.add_theme_font_size_override("font_size", 11)
	add_child(_label_id)

	# Label congratulations (affiché à la fin)
	_label_congratulations = Label.new()
	_label_congratulations.text = ""
	_label_congratulations.position = Vector2(0, 290)
	_label_congratulations.size = Vector2(480, 30)
	_label_congratulations.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_congratulations.add_theme_color_override("font_color", Color(1, 1, 1))
	_label_congratulations.add_theme_font_size_override("font_size", 12)
	add_child(_label_congratulations)

	# Créer quelques "particules" décoratives (étoiles)
	for i in range(12):
		var star := ColorRect.new()
		star.color = Color(1, 0.85, 0.2, randf_range(0.3, 0.8))
		star.size = Vector2(3, 3)
		star.position = Vector2(randi_range(20, 460), randi_range(20, 300))
		star.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(star)
		_particules.append(star)

	# Jouer la musique du panthéon (fallback : musique de victoire champion)
	var musique_hof := "res://assets/audio/music/hall_of_fame.ogg"
	if not ResourceLoader.exists(musique_hof):
		musique_hof = "res://assets/audio/music/victoire_champion_arene.ogg"
	AudioManager.jouer_musique(musique_hof, false)

	# Sauvegarder l'entrée au Hall of Fame
	_sauvegarder_hall_of_fame()

	# Commencer l'affichage après un court délai
	_phase = "intro"
	_timer = 0.0

func _process(delta: float) -> void:
	_timer += delta
	# Animer les étoiles
	for star in _particules:
		star.color.a = 0.3 + 0.5 * sin(_timer * 2.0 + star.position.x * 0.1)

	match _phase:
		"intro":
			if _timer >= 1.5:
				_afficher_pokemon_suivant()
				_phase = "affichage"
				_timer = 0.0
		"affichage":
			if Input.is_action_just_pressed("action_confirmer") or _timer >= 4.0:
				_index_pokemon += 1
				if _index_pokemon >= PlayerData.equipe.size():
					_phase = "fin"
					_timer = 0.0
					_afficher_fin()
				else:
					_afficher_pokemon_suivant()
					_timer = 0.0
		"fin":
			if Input.is_action_just_pressed("action_confirmer") or _timer >= 5.0:
				_fermer()

func _afficher_pokemon_suivant() -> void:
	if _index_pokemon >= PlayerData.equipe.size():
		return
	var p: Dictionary = PlayerData.equipe[_index_pokemon]
	var espece_id: String = p.get("espece_id", "001")
	var espece_data: Dictionary = SpeciesData.get_espece(espece_id)

	# Charger le sprite front
	var front_path := "res://assets/sprites/pokemon/front/%s.png" % espece_id
	var tex := load(front_path) as Texture2D
	if tex:
		_sprite_pokemon.texture = tex

	# Jouer le cri
	AudioManager.jouer_sfx("res://assets/audio/sfx/cries/%s.mp3" % espece_id)

	# Remplir les labels
	var surnom: String = p.get("surnom", espece_data.get("nom", "???"))
	var nom_espece: String = espece_data.get("nom", "???")
	_label_nom.text = surnom
	_label_espece.text = nom_espece if surnom != nom_espece else ""
	_label_niveau.text = "Niv. %d" % p.get("niveau", 1)
	_label_id.text = "%d / %d" % [_index_pokemon + 1, PlayerData.equipe.size()]

func _afficher_fin() -> void:
	_sprite_pokemon.texture = null
	_label_nom.text = ""
	_label_espece.text = ""
	_label_niveau.text = ""
	_label_id.text = ""
	_label_congratulations.text = "Tu es inscrit au Panthéon !\nAppuie sur A pour continuer..."
	_titre.text = "✦ FÉLICITATIONS ✦"

func _sauvegarder_hall_of_fame() -> void:
	# Enregistrer l'équipe du joueur au moment de la victoire
	var entree := {
		"date": Time.get_datetime_string_from_system(),
		"temps_jeu": GameManager.get_temps_formate(),
		"equipe": []
	}
	for p in PlayerData.equipe:
		entree["equipe"].append({
			"espece_id": p.get("espece_id", "001"),
			"surnom": p.get("surnom", "???"),
			"niveau": p.get("niveau", 1)
		})
	# Stocker dans GameManager (sera sauvegardé avec le save)
	var hall: Array = GameManager.get_flag("hall_of_fame") if GameManager.get_flag("hall_of_fame") is Array else []
	hall.append(entree)
	GameManager.set_flag("hall_of_fame", hall)

func _fermer() -> void:
	emit_signal("ecran_ferme")
	queue_free()
