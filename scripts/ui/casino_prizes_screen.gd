extends CanvasLayer

# CasinoPrizesScreen — Échange de jetons contre des prix
# Pokémon et CT disponibles au comptoir du Casino de Céladopole

signal ecran_ferme()

# --- Liste des prix ---
# {nom, type ("pokemon"/"ct"), id, niveau (pour pokémon), cout}
const PRIX := [
	{"nom": "Abra", "type": "pokemon", "id": "063", "niveau": 9, "cout": 180},
	{"nom": "Mélofée", "type": "pokemon", "id": "035", "niveau": 8, "cout": 500},
	{"nom": "Nidorina", "type": "pokemon", "id": "030", "niveau": 17, "cout": 1200},
	{"nom": "Minidraco", "type": "pokemon", "id": "147", "niveau": 18, "cout": 2800},
	{"nom": "Porygon", "type": "pokemon", "id": "137", "niveau": 26, "cout": 9999},
	{"nom": "CT15 Ultralaser", "type": "ct", "id": "ct15", "cout": 5500},
	{"nom": "CT23 Draco-Rage", "type": "ct", "id": "ct23", "cout": 3300},
	{"nom": "CT50 Clonage", "type": "ct", "id": "ct50", "cout": 6500},
]

var _index_selection: int = 0
var _labels_prix: Array[Label] = []
var _label_jetons: Label = null
var _label_message: Label = null
var _curseur: Label = null
var _scroll_offset: int = 0
const MAX_VISIBLE := 6

func _ready() -> void:
	layer = 90
	_creer_ui()
	_maj_affichage()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.08, 0.1, 0.15, 0.97)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre
	var titre := Label.new()
	titre.text = "🏆 COMPTOIR DES PRIX 🏆"
	titre.position = Vector2(110, 8)
	titre.add_theme_color_override("font_color", Color(1.0, 0.85, 0.2))
	titre.add_theme_font_size_override("font_size", 16)
	add_child(titre)

	# Compteur jetons
	_label_jetons = Label.new()
	_label_jetons.position = Vector2(300, 30)
	_label_jetons.add_theme_color_override("font_color", Color(1.0, 0.9, 0.4))
	_label_jetons.add_theme_font_size_override("font_size", 12)
	add_child(_label_jetons)

	# Curseur
	_curseur = Label.new()
	_curseur.text = "▶"
	_curseur.add_theme_font_size_override("font_size", 14)
	_curseur.add_theme_color_override("font_color", Color.WHITE)
	add_child(_curseur)

	# Labels pour chaque ligne visible
	for i in range(MAX_VISIBLE):
		var label := Label.new()
		label.position = Vector2(60, 50 + i * 30)
		label.size = Vector2(380, 28)
		label.add_theme_font_size_override("font_size", 13)
		add_child(label)
		_labels_prix.append(label)

	# Ajouter option "Quitter" en fin de liste — sera affichée dynamiquement

	# Message en bas
	_label_message = Label.new()
	_label_message.position = Vector2(50, 250)
	_label_message.size = Vector2(380, 30)
	_label_message.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label_message.add_theme_font_size_override("font_size", 11)
	_label_message.add_theme_color_override("font_color", Color(0.6, 0.6, 0.7))
	add_child(_label_message)

	# Instructions
	var instr := Label.new()
	instr.text = "↑↓: Choisir   A: Échanger   B: Quitter"
	instr.position = Vector2(90, 290)
	instr.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

func _maj_affichage() -> void:
	# Jetons
	_label_jetons.text = "💰 %d J" % PlayerData.jetons

	# Scroll : ajuster si nécessaire
	var total_items := PRIX.size() + 1  # +1 pour "Quitter"
	if _index_selection < _scroll_offset:
		_scroll_offset = _index_selection
	elif _index_selection >= _scroll_offset + MAX_VISIBLE:
		_scroll_offset = _index_selection - MAX_VISIBLE + 1

	# Afficher les éléments visibles
	for i in range(MAX_VISIBLE):
		var idx := _scroll_offset + i
		if idx < PRIX.size():
			var prix_data: Dictionary = PRIX[idx]
			var peut_acheter := PlayerData.jetons >= prix_data["cout"]
			var couleur := Color(1, 1, 1) if peut_acheter else Color(0.4, 0.4, 0.4)
			_labels_prix[i].text = "%s   —   %d jetons" % [prix_data["nom"], prix_data["cout"]]
			_labels_prix[i].add_theme_color_override("font_color", couleur)
			_labels_prix[i].visible = true
		elif idx == PRIX.size():
			_labels_prix[i].text = "Quitter"
			_labels_prix[i].add_theme_color_override("font_color", Color(0.8, 0.6, 0.6))
			_labels_prix[i].visible = true
		else:
			_labels_prix[i].visible = false

	# Curseur
	var pos_y := _index_selection - _scroll_offset
	_curseur.position = Vector2(40, 50 + pos_y * 30)

	# Message d'info
	if _index_selection < PRIX.size():
		var prix_data: Dictionary = PRIX[_index_selection]
		if prix_data["type"] == "pokemon":
			_label_message.text = "%s Nv.%d — Coût : %d jetons" % [prix_data["nom"], prix_data.get("niveau", 5), prix_data["cout"]]
		else:
			_label_message.text = "%s — Coût : %d jetons" % [prix_data["nom"], prix_data["cout"]]
	else:
		_label_message.text = "Revenir au casino"

func _process(_delta: float) -> void:
	var total_items := PRIX.size() + 1
	if Input.is_action_just_pressed("ui_up"):
		_index_selection = (_index_selection - 1 + total_items) % total_items
		AudioManager.jouer_sfx("res://assets/audio/sfx/select.ogg")
		_maj_affichage()
	elif Input.is_action_just_pressed("ui_down"):
		_index_selection = (_index_selection + 1) % total_items
		AudioManager.jouer_sfx("res://assets/audio/sfx/select.ogg")
		_maj_affichage()
	elif Input.is_action_just_pressed("action_confirmer"):
		_confirmer_selection()
	elif Input.is_action_just_pressed("action_annuler"):
		_fermer()

func _confirmer_selection() -> void:
	# Option "Quitter"
	if _index_selection >= PRIX.size():
		_fermer()
		return

	var prix_data: Dictionary = PRIX[_index_selection]
	var cout: int = prix_data["cout"]

	# Vérifier jetons suffisants
	if PlayerData.jetons < cout:
		_label_message.text = "Pas assez de jetons !"
		_label_message.add_theme_color_override("font_color", Color(1, 0.3, 0.3))
		AudioManager.jouer_sfx("res://assets/audio/sfx/cancel.ogg")
		return

	# Vérifier place dans l'équipe (pour les Pokémon)
	if prix_data["type"] == "pokemon":
		# Créer le Pokémon et l'ajouter
		var pokemon = SpeciesData.creer_pokemon(prix_data["id"], prix_data.get("niveau", 5))
		if pokemon:
			PlayerData.jetons -= cout
			var p_dict: Dictionary = pokemon.to_dict() if pokemon.has_method("to_dict") else {}
			if p_dict.is_empty():
				# Fallback : utiliser directement comme Dictionary
				p_dict = pokemon if pokemon is Dictionary else {}
			if not PlayerData.ajouter_pokemon(p_dict):
				PlayerData.boites[0].append(p_dict)
				_label_message.text = "%s envoyé dans la boîte !" % prix_data["nom"]
			else:
				_label_message.text = "%s rejoint ton équipe !" % prix_data["nom"]
			_label_message.add_theme_color_override("font_color", Color(0.3, 1, 0.3))
			AudioManager.jouer_sfx("res://assets/audio/sfx/level_up.ogg")
		else:
			_label_message.text = "Erreur lors de l'obtention..."
			return
	elif prix_data["type"] == "ct":
		# Ajouter CT à l'inventaire
		PlayerData.jetons -= cout
		PlayerData.ajouter_item(prix_data["id"], 1)
		_label_message.text = "%s obtenu !" % prix_data["nom"]
		_label_message.add_theme_color_override("font_color", Color(0.3, 1, 0.3))
		AudioManager.jouer_sfx("res://assets/audio/sfx/level_up.ogg")

	_maj_affichage()

func _fermer() -> void:
	AudioManager.jouer_sfx("res://assets/audio/sfx/cancel.ogg")
	emit_signal("ecran_ferme")
	queue_free()
