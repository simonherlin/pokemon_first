extends CanvasLayer

# PokedexScreen — Écran du Pokédex
# Affiche la liste des 151 Pokémon avec statut vu/capturé

signal ecran_ferme()

var _index: int = 0
var _labels: Array[Label] = []
var _label_info: Label = null
var _sprite: TextureRect = null
var _scroll_offset: int = 0
const MAX_VISIBLE := 10
const NB_POKEMON := 151

func _ready() -> void:
	layer = 85
	_creer_ui()
	_maj_affichage()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.85, 0.3, 0.3, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre
	var titre := Label.new()
	titre.text = "POKÉDEX"
	titre.position = Vector2(190, 4)
	titre.add_theme_color_override("font_color", Color.WHITE)
	titre.add_theme_font_size_override("font_size", 16)
	add_child(titre)

	# Compteurs
	var compteur := Label.new()
	compteur.name = "LabelCompteur"
	compteur.position = Vector2(12, 4)
	compteur.add_theme_color_override("font_color", Color(1, 1, 0.8))
	compteur.add_theme_font_size_override("font_size", 11)
	compteur.text = "Vus: %d  Capturés: %d" % [PlayerData.pokedex_vu.size(), PlayerData.pokedex_capture.size()]
	add_child(compteur)

	# Panel liste (gauche)
	var panel_liste := Panel.new()
	panel_liste.position = Vector2(8, 26)
	panel_liste.size = Vector2(280, MAX_VISIBLE * 26 + 8)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.7, 0.2, 0.2, 0.8)
	style.set_border_width_all(2)
	style.border_color = Color(0.9, 0.4, 0.4)
	style.set_corner_radius_all(4)
	panel_liste.add_theme_stylebox_override("panel", style)
	add_child(panel_liste)

	# Labels de la liste
	for i in range(MAX_VISIBLE):
		var label := Label.new()
		label.position = Vector2(4, 4 + i * 26)
		label.size = Vector2(272, 24)
		label.add_theme_color_override("font_color", Color.WHITE)
		label.add_theme_font_size_override("font_size", 12)
		panel_liste.add_child(label)
		_labels.append(label)

	# Panel info (droite)
	var panel_info := Panel.new()
	panel_info.position = Vector2(296, 26)
	panel_info.size = Vector2(176, 284)
	var style_info := StyleBoxFlat.new()
	style_info.bg_color = Color(0.6, 0.15, 0.15, 0.8)
	style_info.set_border_width_all(2)
	style_info.border_color = Color(0.9, 0.4, 0.4)
	style_info.set_corner_radius_all(4)
	panel_info.add_theme_stylebox_override("panel", style_info)
	add_child(panel_info)

	# Sprite du Pokémon sélectionné
	_sprite = TextureRect.new()
	_sprite.position = Vector2(40, 8)
	_sprite.size = Vector2(96, 96)
	_sprite.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	panel_info.add_child(_sprite)

	# Info texte
	_label_info = Label.new()
	_label_info.position = Vector2(8, 108)
	_label_info.size = Vector2(160, 168)
	_label_info.autowrap_mode = TextServer.AUTOWRAP_WORD
	_label_info.add_theme_color_override("font_color", Color.WHITE)
	_label_info.add_theme_font_size_override("font_size", 11)
	panel_info.add_child(_label_info)

	# Instructions
	var instr := Label.new()
	instr.text = "B: Retour"
	instr.position = Vector2(8, 305)
	instr.add_theme_color_override("font_color", Color(0.8, 0.6, 0.6))
	instr.add_theme_font_size_override("font_size", 10)
	add_child(instr)

func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("action_haut"):
		_index = maxi(0, _index - 1)
		_ajuster_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_bas"):
		_index = mini(NB_POKEMON - 1, _index + 1)
		_ajuster_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
		_fermer()

func _maj_affichage() -> void:
	# Mettre à jour la liste visible
	for i in range(MAX_VISIBLE):
		var num := _scroll_offset + i + 1  # Pokémon #1 à #151
		if num > NB_POKEMON:
			_labels[i].text = ""
			_labels[i].visible = false
			continue
		_labels[i].visible = true
		var id_str := str(num).lpad(3, "0")
		var prefix := "▶ " if (_scroll_offset + i) == _index else "  "
		var statut_txt := ""
		if PlayerData.a_capture(id_str):
			statut_txt = " ●"
		elif PlayerData.a_vu(id_str):
			statut_txt = " ○"

		# Nom visible seulement si vu
		if PlayerData.a_vu(id_str):
			var espece := SpeciesData.get_espece(id_str)
			_labels[i].text = prefix + "#%s %s%s" % [id_str, espece.get("nom", "???"), statut_txt]
		else:
			_labels[i].text = prefix + "#%s ------%s" % [id_str, statut_txt]

	# Mettre à jour le panel d'info
	var id_sel := str(_index + 1).lpad(3, "0")
	if PlayerData.a_vu(id_sel):
		var espece := SpeciesData.get_espece(id_sel)
		var front_path := "res://assets/sprites/pokemon/front/%s.png" % id_sel
		if ResourceLoader.exists(front_path):
			_sprite.texture = load(front_path) as Texture2D
		else:
			_sprite.texture = null

		var info_text := "%s\n" % espece.get("nom", "???")
		info_text += "Types: %s\n" % "/".join(espece.get("types", []))
		info_text += "Taille: %.1f m\n" % espece.get("taille_m", 0)
		info_text += "Poids: %.1f kg\n" % espece.get("poids_kg", 0)
		if PlayerData.a_capture(id_sel):
			info_text += "\n● Capturé"
		else:
			info_text += "\n○ Vu"
		var desc: String = espece.get("description_pokedex", "")
		if not desc.is_empty():
			info_text += "\n\n%s" % desc
		_label_info.text = info_text
	else:
		_sprite.texture = null
		_label_info.text = "???\n\nPas encore vu."

func _ajuster_scroll() -> void:
	if _index < _scroll_offset:
		_scroll_offset = _index
	elif _index >= _scroll_offset + MAX_VISIBLE:
		_scroll_offset = _index - MAX_VISIBLE + 1

func _fermer() -> void:
	emit_signal("ecran_ferme")
