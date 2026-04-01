extends CanvasLayer

# BagScreen — Écran du sac (inventaire)
# Affiche les objets par catégorie avec navigation et utilisation

signal ecran_ferme()

const CATEGORIES := ["objets", "balls", "objets_cles", "ct_cs"]
const NOMS_CATEGORIES := ["OBJETS", "BALLS", "OBJETS CLÉS", "CT/CS"]

var _index_cat: int = 0
var _index_item: int = 0
var _items_affiches: Array = []  # [{id, nom, quantite, description}]
var _labels_items: Array[Label] = []
var _label_cat: Label = null
var _label_desc: Label = null
var _label_message: Label = null
var _instr_label: Label = null
var _scroll_offset: int = 0
const MAX_VISIBLE := 8

# Sous-écran de choix du Pokémon cible
var _choix_pokemon_actif: bool = false
var _choix_pokemon_index: int = 0
var _choix_item_id: String = ""
var _choix_item_data: Dictionary = {}
var _choix_pokemon_nodes: Array = []

func _ready() -> void:
	layer = 85
	_creer_ui()
	_rafraichir_items()

func _creer_ui() -> void:
	# Fond
	var fond := ColorRect.new()
	fond.color = Color(0.12, 0.18, 0.28, 0.95)
	fond.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fond.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(fond)

	# Titre catégorie
	_label_cat = Label.new()
	_label_cat.text = NOMS_CATEGORIES[0]
	_label_cat.position = Vector2(180, 4)
	_label_cat.add_theme_color_override("font_color", Color.WHITE)
	_label_cat.add_theme_font_size_override("font_size", 16)
	add_child(_label_cat)

	# Navigation catégories
	var nav := Label.new()
	nav.text = "◄ ► Catégorie"
	nav.position = Vector2(12, 4)
	nav.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
	nav.add_theme_font_size_override("font_size", 10)
	add_child(nav)

	# Panel liste items
	var panel := Panel.new()
	panel.position = Vector2(16, 28)
	panel.size = Vector2(448, MAX_VISIBLE * 26 + 8)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.18, 0.22, 0.35, 0.9)
	style.set_border_width_all(2)
	style.border_color = Color(0.4, 0.5, 0.7)
	style.set_corner_radius_all(4)
	panel.add_theme_stylebox_override("panel", style)
	add_child(panel)

	# Labels items (pool de MAX_VISIBLE labels)
	for i in range(MAX_VISIBLE):
		var label := Label.new()
		label.position = Vector2(8, 4 + i * 26)
		label.size = Vector2(432, 24)
		label.add_theme_color_override("font_color", Color.WHITE)
		label.add_theme_font_size_override("font_size", 12)
		panel.add_child(label)
		_labels_items.append(label)

	# Description en bas
	_label_desc = Label.new()
	_label_desc.text = ""
	_label_desc.position = Vector2(24, 248)
	_label_desc.size = Vector2(440, 36)
	_label_desc.autowrap_mode = TextServer.AUTOWRAP_WORD
	_label_desc.add_theme_color_override("font_color", Color(0.8, 0.8, 0.8))
	_label_desc.add_theme_font_size_override("font_size", 11)
	add_child(_label_desc)

	# Message (résultat d'utilisation)
	_label_message = Label.new()
	_label_message.text = ""
	_label_message.position = Vector2(24, 284)
	_label_message.size = Vector2(440, 20)
	_label_message.add_theme_color_override("font_color", Color.GREEN)
	_label_message.add_theme_font_size_override("font_size", 12)
	_label_message.visible = false
	add_child(_label_message)

	# Instructions
	_instr_label = Label.new()
	_instr_label.text = "A: Utiliser  B: Retour"
	_instr_label.position = Vector2(8, 305)
	_instr_label.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
	_instr_label.add_theme_font_size_override("font_size", 10)
	add_child(_instr_label)

func _rafraichir_items() -> void:
	_items_affiches.clear()
	_index_item = 0
	_scroll_offset = 0

	var categorie: String = CATEGORIES[_index_cat]
	_label_cat.text = NOMS_CATEGORIES[_index_cat]

	# Parcourir l'inventaire et filtrer par catégorie
	for item_id in PlayerData.inventaire:
		var quantite: int = PlayerData.inventaire[item_id]
		if quantite <= 0:
			continue
		var item_data: Dictionary = ItemsData.get_item(item_id)
		if item_data.is_empty():
			continue
		if item_data.get("categorie", "") == categorie:
			_items_affiches.append({
				"id": item_id,
				"nom": item_data.get("nom", item_id),
				"quantite": quantite,
				"description": item_data.get("description", "")
			})

	_maj_affichage()

func _maj_affichage() -> void:
	for i in range(MAX_VISIBLE):
		var idx := _scroll_offset + i
		if idx < _items_affiches.size():
			var item: Dictionary = _items_affiches[idx]
			var prefix := "▶ " if idx == _index_item else "  "
			_labels_items[i].text = prefix + "%s  ×%d" % [item["nom"], item["quantite"]]
			_labels_items[i].visible = true
		else:
			if i == 0 and _items_affiches.is_empty():
				_labels_items[i].text = "  (vide)"
				_labels_items[i].visible = true
			else:
				_labels_items[i].text = ""
				_labels_items[i].visible = false

	# Description de l'item sélectionné
	if _index_item < _items_affiches.size():
		_label_desc.text = _items_affiches[_index_item].get("description", "")
	else:
		_label_desc.text = ""

func _process(_delta: float) -> void:
	if _choix_pokemon_actif:
		_process_choix_pokemon()
		return

	# Navigation catégories (gauche/droite)
	if Input.is_action_just_pressed("action_gauche"):
		_index_cat = (_index_cat - 1 + CATEGORIES.size()) % CATEGORIES.size()
		_rafraichir_items()
	elif Input.is_action_just_pressed("action_droite"):
		_index_cat = (_index_cat + 1) % CATEGORIES.size()
		_rafraichir_items()

	# Navigation items (haut/bas)
	if Input.is_action_just_pressed("action_haut") and _items_affiches.size() > 0:
		_index_item = (_index_item - 1 + _items_affiches.size()) % _items_affiches.size()
		_ajuster_scroll()
		_maj_affichage()
	elif Input.is_action_just_pressed("action_bas") and _items_affiches.size() > 0:
		_index_item = (_index_item + 1) % _items_affiches.size()
		_ajuster_scroll()
		_maj_affichage()

	# Utiliser
	if Input.is_action_just_pressed("action_confirmer") and _items_affiches.size() > 0:
		_tenter_utiliser_item()

	# Fermer
	if Input.is_action_just_pressed("action_annuler") or Input.is_action_just_pressed("action_menu"):
		_fermer()

func _ajuster_scroll() -> void:
	if _index_item < _scroll_offset:
		_scroll_offset = _index_item
	elif _index_item >= _scroll_offset + MAX_VISIBLE:
		_scroll_offset = _index_item - MAX_VISIBLE + 1

# --- Utilisation des objets hors combat ---

func _tenter_utiliser_item() -> void:
	if _index_item >= _items_affiches.size():
		return
	var item_id: String = _items_affiches[_index_item]["id"]
	var item_data: Dictionary = ItemsData.get_item(item_id)
	if item_data.is_empty():
		return
	var effet: Dictionary = item_data.get("effet", {})
	if effet.is_empty():
		_afficher_message("Cet objet ne peut pas être utilisé ici.", Color.RED)
		return

	var type_effet: String = effet.get("type", "")

	# Objets qui ciblent un Pokémon de l'équipe
	if type_effet in ["soin_pv", "guerison_statut", "soin_total", "rappel",
	                   "soin_pp", "soin_pp_all", "niveau_plus_1", "pp_plus",
	                   "ev_boost", "apprendre_attaque", "pierre_evolution"]:
		_choix_item_id = item_id
		_choix_item_data = item_data
		_ouvrir_choix_pokemon()
		return

	# Objets qui s'appliquent directement (repousse, corde sortie)
	match type_effet:
		"repousse":
			var pas: int = effet.get("pas", 100)
			GameManager.repousse_restant = pas
			PlayerData.retirer_item(item_id)
			_afficher_message("La Repousse fait effet !", Color.GREEN)
			_rafraichir_items()
		"fuite_donjon":
			# Téléporter au dernier Centre Pokémon
			PlayerData.retirer_item(item_id)
			_afficher_message("Tu t'échappes de la grotte !", Color.GREEN)
			_rafraichir_items()
			# Téléporter après un court délai
			await get_tree().create_timer(0.8).timeout
			var centre: Dictionary = GameManager.dernier_centre
			PlayerData.sauvegarder_position(
				centre.get("carte_id", "bourg_palette"),
				centre.get("x", 7),
				centre.get("y", 12),
				centre.get("direction", "bas")
			)
			SceneManager.charger_scene(
				"res://scenes/maps/%s.tscn" % centre.get("carte_id", "bourg_palette"),
				{"carte_id": centre.get("carte_id", "bourg_palette")}
			)
		"toggle_velo":
			# Activer/désactiver le vélo — fermer le sac d'abord
			emit_signal("ecran_ferme")
			# Trouver le joueur dans la scène et toggler le vélo
			var tree := get_tree()
			if tree:
				var joueurs := tree.get_nodes_in_group("joueur")
				if joueurs.is_empty():
					# Fallback: chercher par arbre de scènes
					var scene_root = tree.current_scene
					if scene_root and scene_root.has_node("Entities/Player"):
						var player = scene_root.get_node("Entities/Player")
						player.sur_velo = not player.sur_velo
				else:
					joueurs[0].sur_velo = not joueurs[0].sur_velo
		_:
			_afficher_message("Pas utilisable ici.", Color.RED)

func _ouvrir_choix_pokemon() -> void:
	_choix_pokemon_actif = true
	_choix_pokemon_index = 0
	_choix_pokemon_nodes.clear()

	# Overlay pour le choix du Pokémon
	var overlay := ColorRect.new()
	overlay.name = "ChoixPokemonOverlay"
	overlay.color = Color(0.1, 0.15, 0.3, 0.95)
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(overlay)

	var titre := Label.new()
	titre.text = "Utiliser %s sur quel Pokémon ?" % _choix_item_data.get("nom", "")
	titre.position = Vector2(40, 6)
	titre.add_theme_color_override("font_color", Color.YELLOW)
	titre.add_theme_font_size_override("font_size", 13)
	overlay.add_child(titre)

	for i in range(PlayerData.equipe.size()):
		var p: Dictionary = PlayerData.equipe[i]
		var y_pos := 30 + i * 44
		var lbl := Label.new()
		var pv_act: int = p.get("pv_actuels", 0)
		var pv_max: int = p.get("stats", {}).get("pv", 1)
		var statut: String = p.get("statut", "")
		var statut_txt := (" [%s]" % statut.to_upper()) if not statut.is_empty() else ""
		var ko_txt := " [KO]" if pv_act <= 0 else ""
		lbl.text = "  %s  N.%d  PV %d/%d%s%s" % [
			p.get("surnom", "???"), p.get("niveau", 1), pv_act, pv_max, statut_txt, ko_txt
		]
		lbl.position = Vector2(20, y_pos)
		lbl.size = Vector2(440, 40)
		lbl.add_theme_color_override("font_color", Color.WHITE if pv_act > 0 else Color(0.5, 0.5, 0.5))
		lbl.add_theme_font_size_override("font_size", 12)
		overlay.add_child(lbl)
		_choix_pokemon_nodes.append(lbl)

	var instr := Label.new()
	instr.text = "A: Confirmer  B: Retour"
	instr.position = Vector2(8, 305)
	instr.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
	instr.add_theme_font_size_override("font_size", 10)
	overlay.add_child(instr)

	_maj_choix_pokemon()

func _process_choix_pokemon() -> void:
	var nb := PlayerData.equipe.size()
	if nb == 0:
		_fermer_choix_pokemon()
		return

	if Input.is_action_just_pressed("action_haut"):
		_choix_pokemon_index = (_choix_pokemon_index - 1 + nb) % nb
		_maj_choix_pokemon()
	elif Input.is_action_just_pressed("action_bas"):
		_choix_pokemon_index = (_choix_pokemon_index + 1) % nb
		_maj_choix_pokemon()
	elif Input.is_action_just_pressed("action_confirmer"):
		_appliquer_item_hors_combat(_choix_item_id, _choix_item_data, _choix_pokemon_index)
	elif Input.is_action_just_pressed("action_annuler"):
		_fermer_choix_pokemon()

func _maj_choix_pokemon() -> void:
	for i in range(_choix_pokemon_nodes.size()):
		var lbl: Label = _choix_pokemon_nodes[i]
		var txt: String = lbl.text
		if txt.begins_with("▶ "):
			txt = "  " + txt.substr(2)
		if i == _choix_pokemon_index:
			txt = "▶ " + txt.substr(2)
		lbl.text = txt

func _fermer_choix_pokemon() -> void:
	_choix_pokemon_actif = false
	_choix_pokemon_nodes.clear()
	var overlay = get_node_or_null("ChoixPokemonOverlay")
	if overlay:
		overlay.queue_free()

# --- Application des effets hors combat ---

func _appliquer_item_hors_combat(item_id: String, item_data: Dictionary, index: int) -> void:
	var p: Dictionary = PlayerData.equipe[index]
	var effet: Dictionary = item_data.get("effet", {})
	var type_effet: String = effet.get("type", "")
	var nom_item: String = item_data.get("nom", item_id)
	var surnom: String = p.get("surnom", "???")
	var pv_act: int = p.get("pv_actuels", 0)
	var pv_max: int = p.get("stats", {}).get("pv", 1)

	match type_effet:
		"soin_pv":
			if pv_act <= 0:
				_afficher_message("%s est KO !" % surnom, Color.RED)
				return
			if pv_act >= pv_max:
				_afficher_message("Les PV de %s sont déjà au max !" % surnom, Color.RED)
				return
			var soin: int = mini(effet.get("montant", 20), pv_max - pv_act)
			p["pv_actuels"] = pv_act + soin
			PlayerData.retirer_item(item_id)
			_afficher_message("%s récupère %d PV !" % [surnom, soin], Color.GREEN)

		"guerison_statut":
			var statut_cible: String = effet.get("statut", "")
			var statut_actuel: String = p.get("statut", "")
			if statut_actuel.is_empty():
				_afficher_message("%s n'a pas de problème de statut !" % surnom, Color.RED)
				return
			if not statut_cible.is_empty() and statut_actuel != statut_cible:
				_afficher_message("Ça n'aura aucun effet !", Color.RED)
				return
			p["statut"] = ""
			PlayerData.retirer_item(item_id)
			_afficher_message("%s est guéri !" % surnom, Color.GREEN)

		"soin_total":
			if pv_act <= 0:
				_afficher_message("%s est KO !" % surnom, Color.RED)
				return
			p["pv_actuels"] = pv_max
			p["statut"] = ""
			PlayerData.retirer_item(item_id)
			_afficher_message("%s est complètement soigné !" % surnom, Color.GREEN)

		"rappel":
			if pv_act > 0:
				_afficher_message("%s n'est pas KO !" % surnom, Color.RED)
				return
			var pct: int = effet.get("montant", 50)
			var soin_rappel: int = maxi(1, int(pv_max * pct / 100.0))
			p["pv_actuels"] = mini(soin_rappel, pv_max)
			p["statut"] = ""
			PlayerData.retirer_item(item_id)
			_afficher_message("%s est ranimé !" % surnom, Color.GREEN)

		"niveau_plus_1":
			if p.get("niveau", 1) >= 100:
				_afficher_message("%s est déjà au niveau max !" % surnom, Color.RED)
				return
			p["niveau"] = p.get("niveau", 1) + 1
			# Recalculer les stats avec la nouvelle valeur
			var espece: Dictionary = SpeciesData.get_espece(p.get("espece_id", "001"))
			if not espece.is_empty():
				var stats_base: Dictionary = espece.get("stats_base", {})
				var niv: int = p["niveau"]
				for stat_nom in ["pv", "attaque", "defense", "special", "vitesse"]:
					var base: int = stats_base.get(stat_nom, 50)
					if stat_nom == "pv":
						p["stats"]["pv"] = int((2.0 * base * niv) / 100.0) + niv + 10
					else:
						p["stats"][stat_nom] = int((2.0 * base * niv) / 100.0) + 5
				# Restaurer les PV au max (bonus du Super Bonbon)
				p["pv_actuels"] = p["stats"]["pv"]
			PlayerData.retirer_item(item_id)
			_afficher_message("%s monte au niveau %d !" % [surnom, p["niveau"]], Color.GREEN)

		"apprendre_attaque":
			var attaque_id: String = effet.get("attaque_id", "")
			if attaque_id.is_empty():
				_afficher_message("CT défectueuse !", Color.RED)
				return
			# Vérifier que le Pokémon n'a pas déjà cette attaque
			var attaques: Array = p.get("attaques", [])
			for atk in attaques:
				if atk.get("id", "") == attaque_id:
					_afficher_message("%s connaît déjà cette attaque !" % surnom, Color.RED)
					return
			var move_data: Dictionary = MoveData.get_move(attaque_id)
			var nom_attaque: String = move_data.get("nom", attaque_id)
			if attaques.size() < 4:
				# Apprendre directement
				attaques.append({"id": attaque_id, "pp_actuels": move_data.get("pp", 10), "pp_max": move_data.get("pp", 10)})
				p["attaques"] = attaques
				PlayerData.retirer_item(item_id)
				_afficher_message("%s apprend %s !" % [surnom, nom_attaque], Color.GREEN)
			else:
				# Pour l'instant : remplacer la dernière attaque (simplifié)
				# TODO: écran de choix de remplacement
				var old_atk: String = attaques[3].get("id", "")
				var old_name: String = MoveData.get_move(old_atk).get("nom", old_atk)
				attaques[3] = {"id": attaque_id, "pp_actuels": move_data.get("pp", 10), "pp_max": move_data.get("pp", 10)}
				p["attaques"] = attaques
				PlayerData.retirer_item(item_id)
				_afficher_message("%s oublie %s et apprend %s !" % [surnom, old_name, nom_attaque], Color.GREEN)

		"pierre_evolution":
			var pierre: String = effet.get("pierre", "")
			var espece_id: String = p.get("espece_id", "")
			# Utiliser la méthode de SpeciesData qui gère pierre + pierre_multiple
			var nouvel_id: String = SpeciesData.peut_evoluer_pierre(espece_id, pierre)
			if nouvel_id.is_empty():
				_afficher_message("Ça n'a aucun effet sur %s !" % surnom, Color.RED)
				return
			var espece: Dictionary = SpeciesData.get_espece(espece_id)
			var nouvelle_espece: Dictionary = SpeciesData.get_espece(nouvel_id)
			if nouvelle_espece.is_empty():
				_afficher_message("Erreur d'évolution !", Color.RED)
				return
			var ancien_nom: String = surnom
			p["espece_id"] = nouvel_id
			if p.get("surnom", "") == espece.get("nom", ""):
				p["surnom"] = nouvelle_espece.get("nom", surnom)
			p["types"] = nouvelle_espece.get("types", p.get("types", []))
			# Recalculer les stats avec les nouvelles stats de base
			var stats_base: Dictionary = nouvelle_espece.get("stats_base", {})
			var niv: int = p.get("niveau", 1)
			for stat_nom in ["pv", "attaque", "defense", "special", "vitesse"]:
				var base: int = stats_base.get(stat_nom, 50)
				if stat_nom == "pv":
					p["stats"]["pv"] = int((2.0 * base * niv) / 100.0) + niv + 10
				else:
					p["stats"][stat_nom] = int((2.0 * base * niv) / 100.0) + 5
			p["pv_actuels"] = p["stats"]["pv"]
			PlayerData.retirer_item(item_id)
			PlayerData.enregistrer_vu(nouvel_id)
			PlayerData.enregistrer_capture(nouvel_id)
			_afficher_message("%s évolue en %s !" % [ancien_nom, p.get("surnom", "???")], Color.YELLOW)

		"ev_boost":
			# Vitamines — augmentent un EV (simplifié : +1 à la stat de base effective)
			var stat_cible: String = effet.get("stat", "attaque")
			p["stats"][stat_cible] = p.get("stats", {}).get(stat_cible, 10) + 2
			if stat_cible == "pv":
				p["pv_actuels"] = p.get("pv_actuels", 0) + 2
			PlayerData.retirer_item(item_id)
			var noms_stats := {"pv":"PV","attaque":"Attaque","defense":"Défense","special":"Spécial","vitesse":"Vitesse"}
			_afficher_message("%s de %s augmente !" % [noms_stats.get(stat_cible, stat_cible), surnom], Color.GREEN)

		_:
			_afficher_message("Cet objet ne peut pas être utilisé ici.", Color.RED)
			return

	# Mise à jour de la donnée dans l'équipe
	PlayerData.equipe[index] = p
	_fermer_choix_pokemon()
	_rafraichir_items()

func _afficher_message(texte: String, couleur: Color) -> void:
	_label_message.text = texte
	_label_message.add_theme_color_override("font_color", couleur)
	_label_message.visible = true
	# Cacher après un délai
	var timer := get_tree().create_timer(2.0)
	timer.timeout.connect(func(): _label_message.visible = false)

func _fermer() -> void:
	emit_signal("ecran_ferme")
