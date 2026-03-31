extends Node2D

# MapScene — Script de base pour toutes les scènes de carte
# Charge les données JSON, instancie joueur + PNJ, gère les dialogues et warps

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
	_instancier_joueur()
	_instancier_pnj()
	# Lancer la musique de la carte
	var musique: String = carte_data.get("musique", "")
	if not musique.is_empty():
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

func _deviner_carte_id() -> String:
	var nom_fichier := get_scene_file_path().get_file().get_basename()
	return nom_fichier
