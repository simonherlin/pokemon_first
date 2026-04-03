extends Node2D

# LabScene — Script spécialisé pour le Laboratoire du Prof. Chen
# Gère la séquence de choix du starter et le combat rival #1
# Hérite la logique de map_scene.gd mais avec un scénario scriptée

const TAILLE_TILE := 32
const PLAYER_SCENE := preload("res://scenes/entities/player.tscn")
const NPC_SCENE := preload("res://scenes/entities/npc.tscn")

var carte_id: String = "laboratoire_chen"
var carte_data: Dictionary = {}
var joueur: CharacterBody2D = null
var _menu_ouvert: bool = false
var _start_menu: Node = null
var _cutscene_active: bool = false
var _starter_screen: Control = null

@onready var tilemap: TileMap = $TileMap
@onready var entities: Node2D = $Entities
@onready var dialog_box: Control = $DialogBox

func _ready() -> void:
	_charger_carte()
	_peindre_tilemap()
	_instancier_joueur()
	_instancier_pnj()
	PlayerData.carte_actuelle = carte_id
	# Lancer la musique du labo
	var musique: String = carte_data.get("musique", "")
	if not musique.is_empty() and ResourceLoader.exists(musique):
		AudioManager.jouer_musique(musique)
	# Réconcilier le flag rival_labo_battu depuis PlayerData
	# (car _on_combat_rival_termine est appelé sur une instance détruite lors du changement de scène)
	if PlayerData.dresseur_est_battu("rival_labo_001") and not GameManager.get_flag("rival_labo_battu"):
		GameManager.set_flag("rival_labo_battu", true)
		print("[LabScene] Flag rival_labo_battu réconcilié depuis PlayerData")

	# Vérifier si on doit lancer la séquence du starter
	if not GameManager.get_flag("premier_pokemon_recu"):
		# Petite pause avant d'afficher le dialogue
		await get_tree().create_timer(0.5).timeout
		_lancer_sequence_starter()
	elif GameManager.get_flag("premier_pokemon_recu") and not GameManager.get_flag("rival_labo_battu"):
		# Le joueur a un starter mais n'a pas encore battu le rival (cas improbable)
		pass
	elif GameManager.get_flag("rival_labo_battu") and not GameManager.get_flag("pokedex_recu"):
		# Retour du combat rival — dialogue post-combat du Prof. Chen
		await get_tree().create_timer(0.5).timeout
		_sequence_post_rival()

func recevoir_params(params: Dictionary) -> void:
	carte_id = params.get("carte_id", carte_id)
	var warp_id: String = params.get("warp_entree", "")
	if not warp_id.is_empty() and joueur:
		_teleporter_sur_warp(warp_id)

# --- Chargement carte ---
func _charger_carte() -> void:
	carte_data = MapLoader.get_carte(carte_id)
	if carte_data.is_empty():
		push_warning("LabScene: données de carte introuvables pour %s" % carte_id)

func _peindre_tilemap() -> void:
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

func _teleporter_sur_warp(warp_id: String) -> void:
	var map_h: int = carte_data.get("hauteur", 10)
	for warp in carte_data.get("warps", []):
		if warp.get("id", "") == warp_id or warp.get("vers_warp", "") == warp_id:
			var x: int = warp.get("x", 0)
			var y: int = warp.get("y", 0)
			var final_y: int = y + 1 if y + 1 < map_h else y
			joueur.teleporter(x, final_y, "bas")
			return

# --- Dialogues ---
func _on_dialogue_demarre(lignes: Array) -> void:
	if joueur:
		joueur.set_peut_bouger(false)
	dialog_box.afficher_dialogue(lignes)
	if not dialog_box.dialogue_termine.is_connected(_on_dialogue_termine):
		dialog_box.dialogue_termine.connect(_on_dialogue_termine)

func _on_dialogue_termine() -> void:
	if not _cutscene_active and joueur:
		joueur.set_peut_bouger(true)

# --- Séquence de choix du starter ---
func _lancer_sequence_starter() -> void:
	print("[LabScene] Lancement séquence starter")
	_cutscene_active = true
	if joueur:
		joueur.set_peut_bouger(false)

	# Dialogue du Prof. Chen
	dialog_box.afficher_dialogue([
		"PROF. CHEN : Ah, %s ! Te voilà enfin !" % PlayerData.nom_joueur,
		"PROF. CHEN : J'ai ici des POKÉMON pour toi.",
		"PROF. CHEN : Il y a aussi un Pokémon très spécial...",
		"PROF. CHEN : Choisis celui qui te plaît."
	])
	if not dialog_box.dialogue_termine.is_connected(_apres_dialogue_chen):
		dialog_box.dialogue_termine.connect(_apres_dialogue_chen, CONNECT_ONE_SHOT)

func _apres_dialogue_chen() -> void:
	# Afficher l'écran de choix du starter
	var scr := load("res://scripts/ui/starter_choice_screen.gd")
	_starter_screen = Control.new()
	_starter_screen.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_starter_screen.set_script(scr)
	add_child(_starter_screen)
	_starter_screen.starter_choisi.connect(_on_starter_choisi)

func _on_starter_choisi(espece_id: String) -> void:
	print("[LabScene] Starter choisi: %s" % espece_id)
	# Fermer l'écran de choix
	if _starter_screen:
		_starter_screen.queue_free()
		_starter_screen = null

	# Créer le starter et l'ajouter à l'équipe
	var pokemon = SpeciesData.creer_pokemon(espece_id, 5)
	if pokemon:
		PlayerData.ajouter_pokemon(pokemon.to_dict())
		PlayerData.enregistrer_capture(espece_id)
		PlayerData.enregistrer_vu(espece_id)
		print("[LabScene] Pokémon ajouté: %s N.%d, équipe=%d" % [pokemon.surnom, pokemon.niveau, PlayerData.equipe.size()])

	# Mettre à jour les flags
	GameManager.set_flag("starter_choisi", espece_id)
	GameManager.set_flag("premier_pokemon_recu", true)

	# Récupérer le nom du Pokémon choisi
	var espece_data: Dictionary = SpeciesData.get_espece(espece_id)
	var nom_pokemon: String = espece_data.get("nom", "Pokémon")

	# Dialogue de réaction
	dialog_box.afficher_dialogue([
		"Tu as choisi %s !" % nom_pokemon,
		"C'est un excellent choix !"
	])
	if not dialog_box.dialogue_termine.is_connected(_apres_choix_starter):
		dialog_box.dialogue_termine.connect(_apres_choix_starter, CONNECT_ONE_SHOT)

func _apres_choix_starter() -> void:
	# Le rival choisit le Pokémon avec avantage de type
	var rival_starter := _determiner_starter_rival()
	var rival_espece: Dictionary = SpeciesData.get_espece(rival_starter)
	var nom_rival: String = GameManager.nom_rival
	var nom_rival_pokemon: String = rival_espece.get("nom", "Pokémon")

	PlayerData.enregistrer_vu(rival_starter)

	dialog_box.afficher_dialogue([
		"%s : Quoi ? Tu as choisi avant moi ?!" % nom_rival,
		"%s : Alors je prends %s !" % [nom_rival, nom_rival_pokemon],
		"%s : Maintenant battons-nous !" % nom_rival,
		"%s veut se battre !" % nom_rival
	])
	if not dialog_box.dialogue_termine.is_connected(_lancer_combat_rival):
		dialog_box.dialogue_termine.connect(_lancer_combat_rival, CONNECT_ONE_SHOT)

func _determiner_starter_rival() -> String:
	# Le rival prend le Pokémon avec avantage de type sur le joueur
	var starter_joueur: String = GameManager.get_flag("starter_choisi")
	match starter_joueur:
		"001":  # Bulbizarre → rival prend Salamèche (feu > plante)
			return "004"
		"004":  # Salamèche → rival prend Carapuce (eau > feu)
			return "007"
		"007":  # Carapuce → rival prend Bulbizarre (plante > eau)
			return "001"
		"151":  # Mew (psy) → rival prend Salamèche (le plus polyvalent)
			return "004"
		_:
			return "004"

func _lancer_combat_rival() -> void:
	print("[LabScene] Lancement combat rival")
	# Construire l'équipe du rival
	var rival_starter := _determiner_starter_rival()
	var rival_pokemon = SpeciesData.creer_pokemon(rival_starter, 5)
	if not rival_pokemon:
		push_error("LabScene: impossible de créer le Pokémon rival")
		_fin_cutscene()
		return

	var nom_rival: String = GameManager.nom_rival
	var trainer_data := {
		"id": "rival_labo_001",
		"nom": nom_rival,
		"classe": "Rival",
		"dialogue_avant": "",
		"dialogue_defaite": "Quoi ?! Impossible !",
		"recompense": 175,
		"equipe": [rival_pokemon.to_dict()]
	}

	# Sauvegarder la position avant combat
	PlayerData.sauvegarder_position(carte_id, 5, 5, "haut")

	# Charger la scène de combat avec les paramètres
	SceneManager.charger_scene("res://scenes/battle/battle_scene.tscn", {
		"type_combat": "dresseur",
		"carte_retour": "laboratoire_chen",
		"dresseur_data": trainer_data,
		"pokemon_joueur_index": 0,
		"musique_carte": "res://assets/audio/music/laboratoire_chen.ogg"
	})

func _on_combat_rival_termine(resultat: Dictionary) -> void:
	# Marquer le rival comme battu
	GameManager.set_flag("rival_labo_battu", true)
	PlayerData.marquer_dresseur_battu("rival_labo_001")

func _sequence_post_rival() -> void:
	_cutscene_active = true
	if joueur:
		joueur.set_peut_bouger(false)
	var nom_rival: String = GameManager.nom_rival
	dialog_box.afficher_dialogue([
		"%s : Pfff... C'est pas possible..." % nom_rival,
		"%s est parti en courant !" % nom_rival,
		"PROF. CHEN : Bravo, %s !" % PlayerData.nom_joueur,
		"PROF. CHEN : Tu as le talent d'un grand dresseur.",
		"PROF. CHEN : J'aimerais te demander un service.",
		"PROF. CHEN : Peux-tu aller chercher un colis pour moi\nà la Boutique de Jadielle ?",
		"PROF. CHEN : Quand tu reviendras,\nje te donnerai quelque chose de spécial.",
		"%s a reçu 5 POKÉ BALL !" % PlayerData.nom_joueur
	])
	if not dialog_box.dialogue_termine.is_connected(_apres_dialogue_post_rival):
		dialog_box.dialogue_termine.connect(_apres_dialogue_post_rival, CONNECT_ONE_SHOT)

func _apres_dialogue_post_rival() -> void:
	# Donner des Poké Balls supplémentaires
	PlayerData.ajouter_item("pokeball", 5)
	# Fin de la cutscene — le joueur peut explorer librement
	_fin_cutscene()

func _fin_cutscene() -> void:
	_cutscene_active = false
	if joueur:
		joueur.set_peut_bouger(true)

# --- Gestion du Start Menu ---
func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("action_menu") and not _menu_ouvert and not _cutscene_active:
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
