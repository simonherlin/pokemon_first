extends Node2D

# MapScene — Script de base pour toutes les scènes de carte
# Charge les données JSON, peint le TileMap, instancie joueur + PNJ

const TAILLE_TILE := 32
const PLAYER_SCENE := preload("res://scenes/entities/player.tscn")
const NPC_SCENE := preload("res://scenes/entities/npc.tscn")
const CUT_TREE_SCENE := preload("res://scenes/entities/cut_tree.tscn")
const BOULDER_SCENE_SCRIPT := preload("res://scripts/overworld/boulder_controller.gd")

var carte_id: String = ""
var carte_data: Dictionary = {}

@onready var tilemap: TileMap = $TileMap
@onready var entities: Node2D = $Entities
@onready var dialog_box: Control = $DialogBox

var joueur: CharacterBody2D = null
var _menu_ouvert: bool = false
var _start_menu: Node = null
var _overlay_obscurite: CanvasLayer = null
var _overlay_jour_nuit: CanvasLayer = null

# --- Safari ---
var safari_system: SafariSystem = null

# --- Puzzle Arène ---
var _puzzle_data: Dictionary = {}
var _poubelles_nodes: Array = []
var _premier_interrupteur_trouve: bool = false
var _interrupteur_positions: Array = []  # [index_a, index_b]

func _ready() -> void:
	# Le carte_id peut être défini via recevoir_params ou depuis le nom de la scène
	if carte_id.is_empty():
		carte_id = _deviner_carte_id()
	_charger_carte()
	_peindre_tilemap()
	_instancier_joueur()
	_instancier_pnj()
	_instancier_arbres_coupables()
	_instancier_rochers()
	_instancier_objets_sol()
	# Grotte sombre : ajouter l'overlay de ténèbres
	_initialiser_obscurite()
	# Cycle jour/nuit : tinter les cartes extérieures
	_initialiser_cycle_jour_nuit()
	# Météo : pluie, neige, sable, soleil
	_initialiser_meteo()
	# Puzzle d'arène (poubelles Carmin, téléporteurs Safrania)
	_initialiser_puzzle_arene()
	# Safari : compteur de pas et mécaniques
	_initialiser_safari()
	# Afficher le nom de la carte en haut
	_afficher_nom_carte()
	# Lancer la musique de la carte
	var musique: String = carte_data.get("musique", "")
	if not musique.is_empty() and ResourceLoader.exists(musique):
		AudioManager.jouer_musique(musique)
	PlayerData.carte_actuelle = carte_id
	# Activer le flag ligue_en_cours si on entre dans une salle E4
	if carte_id in ["ligue_olga", "ligue_aldo", "ligue_agatha", "ligue_peter", "ligue_champion"]:
		GameManager.set_flag("ligue_en_cours", true)

# Recevoir les paramètres du SceneManager (warp_entree, carte_id, etc.)
func recevoir_params(params: Dictionary) -> void:
	carte_id = params.get("carte_id", carte_id)
	# Warp d'entrée : téléporter le joueur à la bonne position
	var warp_id: String = params.get("warp_entree", "")
	if not warp_id.is_empty() and joueur:
		_teleporter_sur_warp(warp_id)
	# Gérer le retour d'un combat champion (Conseil 4 / Ligue)
	if params.get("champion_battu", false):
		_on_champion_battu()

func _charger_carte() -> void:
	carte_data = MapLoader.get_carte(carte_id)
	if carte_data.is_empty():
		push_warning("MapScene: données de carte introuvables pour %s" % carte_id)

func _peindre_tilemap() -> void:
	# Utiliser le TileSetBuilder pour peindre les tiles depuis le JSON
	if carte_data.is_empty():
		return
	TileSetBuilder.peindre_carte(tilemap, carte_data)

func _instancier_joueur() -> void:
	joueur = PLAYER_SCENE.instantiate()
	var px: int = PlayerData.position_x
	var py: int = PlayerData.position_y
	joueur.position_grille = Vector2i(px, py)
	joueur.position = Vector2(px, py) * TAILLE_TILE
	entities.add_child(joueur)

func _instancier_pnj() -> void:
	for pnj_data in carte_data.get("pnj", []):
		var npc := NPC_SCENE.instantiate()
		npc.position = Vector2(pnj_data.get("x", 0), pnj_data.get("y", 0)) * TAILLE_TILE
		npc.initialiser_depuis_json(pnj_data)
		if npc.has_signal("dialogue_demarre"):
			npc.dialogue_demarre.connect(_on_dialogue_demarre)
		if npc.has_signal("boutique_demandee"):
			npc.boutique_demandee.connect(_on_boutique_demandee)
		if npc.has_signal("soin_demande"):
			npc.soin_demande.connect(_on_soin_demande)
		entities.add_child(npc)

func _instancier_arbres_coupables() -> void:
	# Instancier les arbres coupables définis dans le JSON de la carte
	for arbre_data in carte_data.get("arbres_coupables", []):
		var arbre := CUT_TREE_SCENE.instantiate()
		arbre.initialiser(arbre_data, carte_id)
		entities.add_child(arbre)

func _instancier_rochers() -> void:
	# Instancier les rochers poussables définis dans le JSON
	for rocher_data in carte_data.get("rochers", []):
		var rocher := StaticBody2D.new()
		rocher.set_script(BOULDER_SCENE_SCRIPT)
		rocher.initialiser(rocher_data, carte_id)
		entities.add_child(rocher)

func _instancier_objets_sol() -> void:
	# Instancier les objets ramassables au sol
	for obj_data in carte_data.get("objets_sol", []):
		var obj_id: String = obj_data.get("id", "")
		# Vérifier si déjà ramassé
		if PlayerData.objet_est_ramasse("%s_%s" % [carte_id, obj_id]):
			continue
		var item_id: String = obj_data.get("item", "")
		var x: int = obj_data.get("x", 0)
		var y: int = obj_data.get("y", 0)
		# Créer un nœud interactable pour l'objet
		var obj_node := StaticBody2D.new()
		obj_node.position = Vector2(x, y) * TAILLE_TILE
		# Collision
		var shape := RectangleShape2D.new()
		shape.size = Vector2(TAILLE_TILE - 2, TAILLE_TILE - 2)
		var col := CollisionShape2D.new()
		col.shape = shape
		col.position = Vector2(TAILLE_TILE / 2, TAILLE_TILE / 2)
		obj_node.add_child(col)
		# Sprite (petit cercle doré représentant une Poké Ball au sol)
		var sprite_obj := ColorRect.new()
		sprite_obj.color = Color(1.0, 0.85, 0.2)
		sprite_obj.size = Vector2(12, 12)
		sprite_obj.position = Vector2(10, 10)
		obj_node.add_child(sprite_obj)
		# Ajouter le script d'interaction inline via metadata
		obj_node.set_meta("item_id", item_id)
		obj_node.set_meta("obj_id", "%s_%s" % [carte_id, obj_id])
		obj_node.set_meta("quantite", obj_data.get("quantite", 1))
		obj_node.set_script(_creer_script_objet_sol())
		entities.add_child(obj_node)

func _creer_script_objet_sol() -> GDScript:
	# Script inline minimaliste pour l'objet au sol
	var code := """extends StaticBody2D

func interagir(joueur: Node) -> void:
	var item_id: String = get_meta("item_id", "")
	var obj_id: String = get_meta("obj_id", "")
	var quantite: int = get_meta("quantite", 1)
	if item_id.is_empty():
		return
	PlayerData.ajouter_item(item_id, quantite)
	PlayerData.marquer_objet_ramasse(obj_id)
	var item_data: Dictionary = ItemsData.get_item(item_id)
	var nom: String = item_data.get("nom", item_id)
	# Trouver le DialogBox pour afficher le message
	var parent = get_parent()
	while parent != null:
		if parent.has_node("DialogBox"):
			parent.get_node("DialogBox").afficher_dialogue(["Tu as trouvé %s !" % nom])
			break
		parent = parent.get_parent()
	AudioManager.jouer_sfx("res://assets/audio/sfx/item_get.ogg")
	queue_free()
"""
	var script := GDScript.new()
	script.source_code = code
	script.reload()
	return script

# --- Grottes sombres (Flash) ---
func _initialiser_obscurite() -> void:
	# Vérifier si la carte est une grotte sombre
	var sombre: bool = carte_data.get("sombre", false)
	if not sombre:
		return
	# Réinitialiser Flash quand on entre dans une nouvelle grotte sombre
	GameManager.flash_actif = false
	# Créer un overlay noir semi-transparent
	_overlay_obscurite = CanvasLayer.new()
	_overlay_obscurite.layer = 60
	var rect := ColorRect.new()
	rect.color = Color(0, 0, 0, 0.92)
	rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_overlay_obscurite.add_child(rect)
	add_child(_overlay_obscurite)

func utiliser_flash() -> void:
	# Appelé quand le joueur utilise Flash depuis le menu Pokémon
	GameManager.flash_actif = true
	if _overlay_obscurite:
		var tween := create_tween()
		for child in _overlay_obscurite.get_children():
			if child is ColorRect:
				tween.tween_property(child, "color:a", 0.0, 0.8)
		tween.tween_callback(_overlay_obscurite.queue_free)
		_overlay_obscurite = null

func _on_dialogue_demarre(lignes: Array) -> void:
	if joueur:
		joueur.set_peut_bouger(false)
	dialog_box.afficher_dialogue(lignes)
	# Reconnecter le signal de fin de dialogue
	if not dialog_box.dialogue_termine.is_connected(_on_dialogue_termine):
		dialog_box.dialogue_termine.connect(_on_dialogue_termine)

func _on_dialogue_termine() -> void:
	if joueur:
		joueur.set_peut_bouger(true)

func _on_soin_demande() -> void:
	# Sauvegarder ce centre comme dernier lieu de soin
	GameManager.dernier_centre = {
		"carte_id": carte_id,
		"x": PlayerData.position_x,
		"y": PlayerData.position_y,
		"direction": PlayerData.direction
	}
	# Petit délai pour laisser le dialogue s'afficher, puis message de confirmation
	await get_tree().create_timer(0.5).timeout
	dialog_box.afficher_dialogue(["...Vos Pokémon sont maintenant en pleine forme !", "Revenez quand vous voulez !"])

func _on_boutique_demandee(items: Array) -> void:
	# Attendre la fin du dialogue d'accueil, puis ouvrir la boutique
	await get_tree().create_timer(0.5).timeout
	_ouvrir_boutique(items)

func _ouvrir_boutique(items: Array) -> void:
	if joueur:
		joueur.set_peut_bouger(false)
	var scr = load("res://scripts/ui/shop_screen.gd")
	var shop := CanvasLayer.new()
	shop.set_script(scr)
	shop.items_en_vente = items
	add_child(shop)
	shop.ecran_ferme.connect(func():
		shop.queue_free()
		if joueur:
			joueur.set_peut_bouger(true)
	)

func _teleporter_sur_warp(warp_id: String) -> void:
	for warp in carte_data.get("warps", []):
		if warp.get("id", "") == warp_id or warp.get("vers_warp", "") == warp_id:
			var x: int = warp.get("x", 0)
			var y: int = warp.get("y", 0)
			joueur.teleporter(x, y + 1, "bas")  # Un tile sous le warp
			return

func _afficher_nom_carte() -> void:
	var nom: String = carte_data.get("nom", carte_id)
	if nom.is_empty():
		return
	# Créer un label temporaire pour afficher le nom de la zone
	var label := Label.new()
	label.text = nom
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_color_override("font_color", Color.WHITE)
	label.add_theme_color_override("font_shadow_color", Color.BLACK)
	label.add_theme_constant_override("shadow_offset_x", 1)
	label.add_theme_constant_override("shadow_offset_y", 1)
	label.position = Vector2(160, 8)
	label.z_index = 100
	# Utiliser un CanvasLayer pour que ce soit au-dessus de tout
	var canvas := CanvasLayer.new()
	canvas.layer = 50
	canvas.add_child(label)
	add_child(canvas)
	# Faire disparaître après 2 secondes
	var tween := create_tween()
	tween.tween_interval(2.0)
	tween.tween_property(label, "modulate:a", 0.0, 0.5)
	tween.tween_callback(canvas.queue_free)

func _deviner_carte_id() -> String:
	var nom_fichier := get_scene_file_path().get_file().get_basename()
	return nom_fichier

# --- Gestion victoire champion (Conseil 4 / Ligue) ---
func _on_champion_battu() -> void:
	# Marquer le dresseur comme battu et poser les flags correspondants
	match carte_id:
		"ligue_olga":
			GameManager.set_flag("conseil_olga_battu", true)
		"ligue_aldo":
			GameManager.set_flag("conseil_aldo_battu", true)
		"ligue_agatha":
			GameManager.set_flag("conseil_agatha_battu", true)
		"ligue_peter":
			GameManager.set_flag("conseil_peter_battu", true)
		"ligue_champion":
			GameManager.set_flag("champion_ligue_battu", true)
			GameManager.set_flag("ligue_en_cours", false)
	# Marquer les dresseurs PNJ comme battus
	for pnj_data in carte_data.get("pnj", []):
		if pnj_data.get("type", "") == "champion":
			var tid: String = pnj_data.get("trainer_id", pnj_data.get("id", ""))
			PlayerData.marquer_dresseur_battu(tid)
			PlayerData.marquer_dresseur_battu(pnj_data.get("id", ""))

# ----------------------------------------------------------------
# Puzzle Arène de Carmin (poubelles / interrupteurs)
# ----------------------------------------------------------------
func _initialiser_puzzle_arene() -> void:
	_puzzle_data = carte_data.get("puzzle", {})
	if _puzzle_data.is_empty():
		return
	match _puzzle_data.get("type", ""):
		"poubelles_carmin":
			_creer_poubelles()
		"teleporteurs_safrania":
			_creer_teleporteurs()

func _creer_poubelles() -> void:
	# Générer 2 positions d'interrupteurs aléatoires parmi les 15 poubelles
	var poubelles_data: Array = _puzzle_data.get("poubelles", [])
	var nb := poubelles_data.size()
	if nb < 2:
		return
	_interrupteur_positions = []
	_interrupteur_positions.append(randi() % nb)
	var second := randi() % (nb - 1)
	if second >= _interrupteur_positions[0]:
		second += 1
	_interrupteur_positions.append(second)
	_premier_interrupteur_trouve = false

	for i in range(nb):
		var pd: Dictionary = poubelles_data[i]
		var poubelle := StaticBody2D.new()
		poubelle.position = Vector2(pd.get("x", 0), pd.get("y", 0)) * TAILLE_TILE
		var shape := RectangleShape2D.new()
		shape.size = Vector2(TAILLE_TILE - 2, TAILLE_TILE - 2)
		var col := CollisionShape2D.new()
		col.shape = shape
		col.position = Vector2(TAILLE_TILE / 2, TAILLE_TILE / 2)
		poubelle.add_child(col)
		# Visuel simple
		var sprite_p := ColorRect.new()
		sprite_p.color = Color(0.4, 0.4, 0.4)
		sprite_p.size = Vector2(24, 24)
		sprite_p.position = Vector2(4, 4)
		poubelle.add_child(sprite_p)
		poubelle.set_meta("poubelle_index", i)
		poubelle.set_meta("type", "poubelle")
		_poubelles_nodes.append(poubelle)
		entities.add_child(poubelle)

## Appelé quand le joueur interagit avec une poubelle
func interagir_poubelle(index: int) -> void:
	if index in _interrupteur_positions:
		if not _premier_interrupteur_trouve:
			_premier_interrupteur_trouve = true
			AudioManager.jouer_sfx("res://assets/audio/sfx/switch.ogg")
			dialog_box.afficher_dialogue(["Tu as trouvé le 1er interrupteur !", "Cherche le 2e dans une poubelle voisine !"])
		else:
			# Vérifier si c'est le bon (doit être le 2e interrupteur)
			AudioManager.jouer_sfx("res://assets/audio/sfx/switch.ogg")
			dialog_box.afficher_dialogue(["Tu as trouvé le 2e interrupteur !", "La porte s'ouvre !"])
			_ouvrir_barriere_carmin()
	else:
		if _premier_interrupteur_trouve:
			# Mauvaise poubelle → reset
			_premier_interrupteur_trouve = false
			# Re-randomiser les positions
			var nb: int = _puzzle_data.get("poubelles", []).size()
			_interrupteur_positions[0] = randi() % nb
			var second: int = randi() % (nb - 1)
			if second >= _interrupteur_positions[0]:
				second += 1
			_interrupteur_positions[1] = second
			dialog_box.afficher_dialogue(["La poubelle est vide...", "Les interrupteurs ont été réinitialisés !"])
		else:
			dialog_box.afficher_dialogue(["La poubelle est vide..."])

func _ouvrir_barriere_carmin() -> void:
	# Retirer les murs de barrière dans le TileMap
	var y_bars: Array = _puzzle_data.get("barriere_y", [])
	var x_min: int = _puzzle_data.get("barriere_x_min", 3)
	var x_max: int = _puzzle_data.get("barriere_x_max", 8)
	for y in y_bars:
		for x in range(x_min, x_max + 1):
			# Remettre le tile à 24 (sol) au lieu de 25 (mur)
			tilemap.set_cell(0, Vector2i(x, y), 0, Vector2i(24 % 8, 24 / 8))
	GameManager.set_flag("puzzle_carmin_resolu", true)

# ----------------------------------------------------------------
# Puzzle Arène de Safrania (téléporteurs)
# ----------------------------------------------------------------
func _creer_teleporteurs() -> void:
	# Les téléporteurs sont gérés via la détection de case dans le joueur
	# On stocke les données pour que le player_controller puisse y accéder
	pass

## Vérifie si la position est un téléporteur et retourne la destination
func verifier_teleporteur(position_grille: Vector2i) -> Dictionary:
	if _puzzle_data.get("type", "") != "teleporteurs_safrania":
		return {}
	for tp in _puzzle_data.get("teleporteurs", []):
		if tp.get("x", -1) == position_grille.x and tp.get("y", -1) == position_grille.y:
			return {"x": tp.get("dest_x", 0), "y": tp.get("dest_y", 0)}
	return {}

# ----------------------------------------------------------------
# Safari Zone — Gestion des pas et mécaniques
# ----------------------------------------------------------------
func _initialiser_safari() -> void:
	if not SafariSystem.est_zone_safari():
		return
	# Chercher le SafariSystem dans les autoloads ou le créer localement
	var safari_nodes := get_tree().get_nodes_in_group("safari_system")
	if safari_nodes.size() > 0:
		safari_system = safari_nodes[0] as SafariSystem
	# Connecter le signal du joueur pour décompter les pas
	if joueur and joueur.has_signal("pas_effectue"):
		joueur.pas_effectue.connect(_on_pas_safari)

func _on_pas_safari() -> void:
	if safari_system and safari_system.actif:
		if not safari_system.decompter_pas():
			# Plus de pas → retour à l'entrée
			dialog_box.afficher_dialogue(["Ding dong ! C'est fini !", "Votre temps au Parc Safari est écoulé !"])
			await dialog_box.dialogue_termine
			SceneManager.charger_scene("res://scenes/maps/map_scene.tscn", {
				"carte_id": "parc_safari_entree",
				"warp_entree": "retour_safari"
			})

# --- Gestion du Start Menu ---
func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("action_menu") and not _menu_ouvert:
		_ouvrir_menu()

func _ouvrir_menu() -> void:
	if _menu_ouvert or SceneManager.est_en_transition():
		return
	_menu_ouvert = true
	if joueur:
		joueur.set_peut_bouger(false)
	var scr = load("res://scripts/ui/start_menu.gd")
	_start_menu = CanvasLayer.new()
	_start_menu.set_script(scr)
	add_child(_start_menu)
	_start_menu.menu_ferme.connect(_on_menu_ferme)

func _on_menu_ferme() -> void:
	_menu_ouvert = false

# =============================================================================
# CYCLE JOUR/NUIT
# =============================================================================

# Appliquer la teinte jour/nuit sur les cartes extérieures
func _initialiser_cycle_jour_nuit() -> void:
	if not TimeManager.est_carte_exterieure(carte_data):
		return
	var teinte := TimeManager.get_teinte_actuelle()
	if teinte.a <= 0.01:
		return  # Pas de teinte en plein jour
	_overlay_jour_nuit = CanvasLayer.new()
	_overlay_jour_nuit.layer = 58  # Au-dessus des entités, sous le HUD
	_overlay_jour_nuit.name = "JourNuitOverlay"
	var rect := ColorRect.new()
	rect.color = teinte
	rect.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_overlay_jour_nuit.add_child(rect)
	add_child(_overlay_jour_nuit)
	# Se connecter au changement de phase pour adapter la teinte en temps réel
	TimeManager.phase_changee.connect(_on_phase_changee)

func _on_phase_changee(_nouvelle_phase) -> void:
	if not TimeManager.est_carte_exterieure(carte_data):
		return
	var teinte := TimeManager.get_teinte_actuelle()
	if _overlay_jour_nuit and is_instance_valid(_overlay_jour_nuit):
		var rect := _overlay_jour_nuit.get_child(0)
		if rect is ColorRect:
			var tween := create_tween()
			tween.tween_property(rect, "color", teinte, 2.0)
	else:
		# Créer l'overlay s'il n'existe pas encore
		if teinte.a > 0.01:
			_initialiser_cycle_jour_nuit()

# =============================================================================
# MÉTÉO
# =============================================================================

func _initialiser_meteo() -> void:
	WeatherManager.configurer_meteo_carte(carte_id, carte_data)
	if WeatherManager.meteo_actuelle != WeatherManager.Meteo.AUCUNE:
		WeatherManager.creer_overlay_meteo(self)
	_start_menu = null
	if joueur:
		joueur.set_peut_bouger(true)

