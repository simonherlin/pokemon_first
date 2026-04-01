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
	# Afficher le nom de la carte en haut
	_afficher_nom_carte()
	# Lancer la musique de la carte
	var musique: String = carte_data.get("musique", "")
	if not musique.is_empty() and ResourceLoader.exists(musique):
		AudioManager.jouer_musique(musique)
	PlayerData.carte_actuelle = carte_id

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
	# Marquer les dresseurs PNJ comme battus
	for pnj_data in carte_data.get("pnj", []):
		if pnj_data.get("type", "") == "champion":
			var tid: String = pnj_data.get("trainer_id", pnj_data.get("id", ""))
			PlayerData.marquer_dresseur_battu(tid)
			PlayerData.marquer_dresseur_battu(pnj_data.get("id", ""))

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
	_start_menu = null
	if joueur:
		joueur.set_peut_bouger(true)

