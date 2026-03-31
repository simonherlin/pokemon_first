extends Node2D

# MapScene — Script de base pour toutes les scènes de carte
# Charge les données JSON, peint le TileMap, instancie joueur + PNJ

const TAILLE_TILE := 32
const PLAYER_SCENE := preload("res://scenes/entities/player.tscn")
const NPC_SCENE := preload("res://scenes/entities/npc.tscn")

var carte_id: String = ""
var carte_data: Dictionary = {}

@onready var tilemap: TileMap = $TileMap
@onready var entities: Node2D = $Entities
@onready var dialog_box: Control = $DialogBox

var joueur: CharacterBody2D = null

func _ready() -> void:
	# Le carte_id peut être défini via recevoir_params ou depuis le nom de la scène
	if carte_id.is_empty():
		carte_id = _deviner_carte_id()
	_charger_carte()
	_peindre_tilemap()
	_instancier_joueur()
	_instancier_pnj()
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
		entities.add_child(npc)

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
