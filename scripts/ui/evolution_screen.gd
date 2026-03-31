extends CanvasLayer

# EvolutionScreen — Écran d'animation d'évolution
# Affiche l'ancien sprite, flash, puis le nouveau sprite

signal evolution_terminee(accepte: bool)

var pokemon: Pokemon = null
var vers_id: String = ""

var _label_message: Label = null
var _sprite_pokemon: TextureRect = null
var _choix_fait: bool = false
var _en_confirmation: bool = false
var _index_choix: int = 1  # 0=Oui, 1=Non (défaut Non)
var _labels_choix: Array[Label] = []

func _ready() -> void:
	layer = 90
	_creer_ui()
	_demarrer_sequence()

func _creer_ui() -> void:
	# Fond noir
	var fond := ColorRect.new()
	fond.color = Color(0.05, 0.05, 0.1, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Sprite Pokémon (centre)
	_sprite_pokemon = TextureRect.new()
	_sprite_pokemon.position = Vector2(176, 60)
	_sprite_pokemon.size = Vector2(128, 192)
	_sprite_pokemon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	# Charger le sprite actuel
	var front_path := "res://assets/sprites/pokemon/front/%s.png" % pokemon.espece_id
	var tex := load(front_path) as Texture2D
	if tex:
		_sprite_pokemon.texture = tex
	add_child(_sprite_pokemon)

	# Message
	_label_message = Label.new()
	_label_message.position = Vector2(40, 260)
	_label_message.size = Vector2(400, 50)
	_label_message.autowrap_mode = TextServer.AUTOWRAP_WORD
	_label_message.add_theme_color_override("font_color", Color.WHITE)
	_label_message.add_theme_font_size_override("font_size", 14)
	add_child(_label_message)

func _demarrer_sequence() -> void:
	_label_message.text = "Hein ? %s évolue !" % pokemon.surnom
	await get_tree().create_timer(2.0).timeout

	# Flash blanc rapide
	var flash := ColorRect.new()
	flash.color = Color(1, 1, 1, 0.9)
	flash.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(flash)
	await get_tree().create_timer(0.5).timeout

	# Changer le sprite pour le nouveau Pokémon
	var new_path := "res://assets/sprites/pokemon/front/%s.png" % vers_id
	var new_tex := load(new_path) as Texture2D
	if new_tex:
		_sprite_pokemon.texture = new_tex

	# Retirer le flash
	flash.queue_free()
	await get_tree().create_timer(0.5).timeout

	# Demander confirmation
	var espece_data := SpeciesData.get_espece(vers_id)
	var nouveau_nom: String = espece_data.get("nom", "???")
	_label_message.text = "%s veut évoluer en %s !\nAccepter l'évolution ?" % [pokemon.surnom, nouveau_nom]
	_afficher_choix()

func _afficher_choix() -> void:
	_en_confirmation = true
	var y_base := 290
	var noms := ["Oui", "Non"]
	for i in range(2):
		var label := Label.new()
		label.position = Vector2(160 + i * 80, y_base)
		label.add_theme_color_override("font_color", Color.WHITE)
		label.add_theme_font_size_override("font_size", 14)
		_labels_choix.append(label)
		add_child(label)
	_maj_curseur_choix()

func _maj_curseur_choix() -> void:
	var noms := ["Oui", "Non"]
	for i in range(_labels_choix.size()):
		_labels_choix[i].text = ("▶ " if i == _index_choix else "  ") + noms[i]

func _process(_delta: float) -> void:
	if not _en_confirmation:
		return
	if Input.is_action_just_pressed("action_gauche") or Input.is_action_just_pressed("action_droite"):
		_index_choix = 1 - _index_choix
		_maj_curseur_choix()
	elif Input.is_action_just_pressed("action_confirmer"):
		_en_confirmation = false
		emit_signal("evolution_terminee", _index_choix == 0)
		await get_tree().create_timer(0.5).timeout
		queue_free()
