extends CharacterBody2D

# NPCController — Contrôleur de PNJ (personnage non-joueur)
# Gère les dialogues, les combats de dresseurs, la détection du joueur

# --- Constantes ---
const TAILLE_TILE := 32

# --- Données du PNJ (chargées depuis la carte JSON) ---
var npc_id: String = ""
var dialogues: Array = []           # Liste de lignes de dialogue
var dialogue_apres: Array = []       # Dialogue après avoir été battu (dresseur)
var est_dresseur: bool = false
var equipe_dresseur: Array = []      # Liste de {espece_id, niveau}
var recompense: int = 0
var champ_vision: int = 3           # Cases devant le PNJ (dresseur)
var direction_initiale: String = "bas"
var mobile: bool = false
var type_pnj: String = ""           # "", "infirmiere", "vendeur", "pc", "champion"
var inventaire_boutique: Array = [] # IDs des items en vente (si type=vendeur)
var trainer_id: String = ""          # Référence vers trainers.json (si présent)
var _trainer_nom: String = ""        # Nom du dresseur chargé depuis trainers.json
var _trainer_classe: String = ""     # Classe du dresseur (pour choisir la musique de combat)

# --- Nœuds ---
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var ray_vision: RayCast2D = $RayVision

# --- État ---
var joueur_detecte: bool = false
var battu: bool = false

signal dialogue_demarre(lignes: Array)
signal combat_dresseur_demarre(npc_id: String, equipe: Array, recompense: int, nom: String)
signal soin_demande()
signal boutique_demandee(items: Array)

func _ready() -> void:
	battu = PlayerData.dresseur_est_battu(npc_id)
	_appliquer_direction(direction_initiale)

func _process(_delta: float) -> void:
	if est_dresseur and not battu:
		_verifier_champ_vision()

# Initialiser depuis les données JSON de la carte
func initialiser_depuis_json(data: Dictionary) -> void:
	npc_id = data.get("id", "")
	dialogues = data.get("dialogue", data.get("dialogue_avant", []))
	dialogue_apres = data.get("dialogue_apres", [])
	est_dresseur = data.has("equipe")
	equipe_dresseur = data.get("equipe", [])
	recompense = data.get("recompense", 0)
	mobile = data.get("mobile", false)
	direction_initiale = data.get("direction", "bas")
	type_pnj = data.get("type", "")
	inventaire_boutique = data.get("inventaire_boutique", [])
	trainer_id = data.get("trainer_id", "")
	battu = PlayerData.dresseur_est_battu(npc_id)
	# Charger le sprite du PNJ
	_charger_sprite(data.get("sprite", "pnj_homme"))
	# Si trainer_id est défini, charger l'équipe depuis trainers.json
	if not trainer_id.is_empty() and not est_dresseur:
		_charger_trainer_data()

# Interaction déclenché par le joueur (touche A face au PNJ)
func interagir(joueur: Node) -> void:
	# Tourner vers le joueur
	var dir_vers_joueur := _direction_vers(joueur)
	_appliquer_direction(dir_vers_joueur)

	# PNJ spéciaux
	match type_pnj:
		"infirmiere":
			_interagir_infirmiere(joueur)
			return
		"vendeur":
			_interagir_vendeur(joueur)
			return
		"pc":
			_interagir_pc(joueur)
			return

	if est_dresseur and not battu:
		# Démarrer un combat
		emit_signal("combat_dresseur_demarre", npc_id, equipe_dresseur, recompense, npc_id)
		_demarrer_combat(joueur)
	else:
		# Dialogue simple
		var lignes := dialogue_apres if (est_dresseur and battu) else dialogues
		if lignes.is_empty():
			lignes = ["..."]
		emit_signal("dialogue_demarre", lignes)

# Infirmière : soigne toute l'équipe
func _interagir_infirmiere(joueur: Node) -> void:
	# Dialogue d'accueil
	var lignes_soin := ["Bienvenue au Centre Pokémon !", "Je vais soigner vos Pokémon."]
	emit_signal("dialogue_demarre", lignes_soin)
	# Jouer le jingle de soin
	AudioManager.jouer_musique("res://assets/audio/music/soin_pokemon.ogg", false)
	# Soigner tous les Pokémon de l'équipe
	_soigner_equipe()
	# Émettre le signal de soin (pour animations futures)
	emit_signal("soin_demande")

# Soigner tous les Pokémon du joueur
func _soigner_equipe() -> void:
	for i in range(PlayerData.equipe.size()):
		var p: Dictionary = PlayerData.equipe[i]
		# Restaurer les PV au max (pv_max est dans stats.pv)
		p["pv_actuels"] = p.get("stats", {}).get("pv", p.get("pv_actuels", 1))
		# Supprimer le statut
		p["statut"] = ""
		# Restaurer les PP de toutes les attaques
		if p.has("attaques"):
			for atk in p["attaques"]:
				atk["pp_actuels"] = atk.get("pp_max", atk.get("pp_actuels", 0))
		PlayerData.equipe[i] = p

# Vendeur : affiche le dialogue puis ouvre la boutique
func _interagir_vendeur(joueur: Node) -> void:
	emit_signal("dialogue_demarre", dialogues if not dialogues.is_empty() else ["Bienvenue !"])
	emit_signal("boutique_demandee", inventaire_boutique)
# PC : ouvre le système de stockage Pokémon de Bill
func _interagir_pc(joueur: Node) -> void:
	if not GameManager.get_flag("bill_pc_active"):
		emit_signal("dialogue_demarre", ["Le PC s'allume...", "Mais le système de stockage\nn'est pas encore activé."])
		return
	# Ouvrir l'écran PC
	if joueur.has_method("set_peut_bouger"):
		joueur.set_peut_bouger(false)
	var pc_scene = preload("res://scenes/ui/pc_screen.tscn")
	var pc_ecran = pc_scene.instantiate()
	get_tree().current_scene.add_child(pc_ecran)
	pc_ecran.pc_ferme.connect(func():
		if joueur.has_method("set_peut_bouger"):
			joueur.set_peut_bouger(true)
	)
# Vérifier si le joueur entre dans le champ de vision du dresseur
# === Équilibrage dynamique ===
# Ajuste le niveau de l'équipe du dresseur en fonction du joueur
func _equilibrer_equipe_dresseur(equipe_base: Array) -> Array:
	if equipe_base.is_empty() or PlayerData.equipe.is_empty():
		return equipe_base
	# Calculer le niveau moyen du joueur
	var total_joueur := 0
	var count_joueur := 0
	for poke in PlayerData.equipe:
		var niv: int = poke.get("niveau", 0)
		if niv > 0:
			total_joueur += niv
			count_joueur += 1
	if count_joueur == 0:
		return equipe_base
	var avg_joueur := int(total_joueur / count_joueur)
	# Calculer le niveau moyen du dresseur
	var total_dresseur := 0
	var count_dresseur := 0
	for poke in equipe_base:
		var niv: int = poke.get("niveau", 0)
		if niv > 0:
			total_dresseur += niv
			count_dresseur += 1
	if count_dresseur == 0:
		return equipe_base
	var avg_dresseur := int(total_dresseur / count_dresseur)
	# Si le joueur est significativement plus fort (> 3 niveaux d'avance),
	# on remonte les niveaux du dresseur proportionnellement
	if avg_joueur <= avg_dresseur + 3:
		return equipe_base
	var boost := avg_joueur - avg_dresseur - 2  # On garde le joueur 2 niveaux au-dessus
	var equipe_ajustee := []
	for poke in equipe_base:
		var copie := poke.duplicate(true)
		var niv_base: int = copie.get("niveau", 5)
		var nouveau_niv := mini(niv_base + boost, 100)
		copie["niveau"] = nouveau_niv
		# Recalculer les stats pour le nouveau niveau
		var espece_id_poke: String = copie.get("espece_id", "")
		if not espece_id_poke.is_empty():
			var pokemon_recalcule = SpeciesData.creer_pokemon(espece_id_poke, nouveau_niv)
			if pokemon_recalcule:
				copie = pokemon_recalcule.to_dict()
		equipe_ajustee.append(copie)
	return equipe_ajustee

# Vérifier si le joueur entre dans le champ de vision du dresseur
func _verifier_champ_vision() -> void:
	if ray_vision == null:
		return
	ray_vision.target_position = _direction_vers_vec(direction_initiale) * TAILLE_TILE * champ_vision
	ray_vision.force_raycast_update()
	if ray_vision.is_colliding():
		var collider = ray_vision.get_collider()
		if collider and collider.is_in_group("joueur") and not joueur_detecte:
			joueur_detecte = true
			_reagir_joueur_vu(collider)

func _reagir_joueur_vu(joueur: Node) -> void:
	# Exclamation mark (TODO: anim) puis dialoguer/combattre
	_demarrer_combat(joueur)

func _demarrer_combat(joueur: Node) -> void:
	if joueur.has_method("set_peut_bouger"):
		joueur.set_peut_bouger(false)
	# === Équilibrage dynamique des dresseurs ===
	var equipe_equilibree := _equilibrer_equipe_dresseur(equipe_dresseur)
	# Construire les données du dresseur pour BattleController
	var dresseur_data := {
		"id": npc_id,
		"nom": _trainer_nom if not _trainer_nom.is_empty() else npc_id,
		"classe": _trainer_classe if not _trainer_classe.is_empty() else "",
		"equipe": equipe_equilibree,
		"recompense": recompense
	}
	# Paramètres de combat
	var params := {
		"type_combat": "dresseur",
		"dresseur_data": dresseur_data,
		"pokemon_joueur_index": 0,
		"carte_retour": PlayerData.carte_actuelle,
		"musique_carte": MapLoader.get_carte(PlayerData.carte_actuelle).get("musique", "")
	}
	# Si type champion, signaler pour le traitement post-victoire
	if type_pnj == "champion":
		params["champion_battu"] = true
	# Charger de la scène de combat
	SceneManager.charger_scene("res://scenes/battle/battle_scene.tscn", params)

# Charger les données du dresseur depuis trainers.json via trainer_id
func _charger_trainer_data() -> void:
	var chemin := "res://data/trainers.json"
	if not FileAccess.file_exists(chemin):
		push_error("NPCController: trainers.json introuvable")
		return
	var fichier := FileAccess.open(chemin, FileAccess.READ)
	var all_trainers = JSON.parse_string(fichier.get_as_text())
	fichier.close()
	if not all_trainers or not all_trainers.has(trainer_id):
		push_error("NPCController: dresseur %s introuvable dans trainers.json" % trainer_id)
		return
	var trainer_raw: Dictionary = all_trainers[trainer_id]
	# Construire l'équipe de Pokémon
	var equipe_combat := []
	for pkmn in trainer_raw.get("equipe", []):
		var pokemon = SpeciesData.creer_pokemon(pkmn.get("espece_id", "019"), pkmn.get("niveau", 5))
		if pokemon:
			equipe_combat.append(pokemon.to_dict())
	if not equipe_combat.is_empty():
		equipe_dresseur = equipe_combat
		est_dresseur = true
	recompense = trainer_raw.get("recompense", 0)
	_trainer_nom = trainer_raw.get("nom", trainer_id)
	_trainer_classe = trainer_raw.get("classe", "")
	# Charger les dialogues du dresseur si pas définis dans la carte
	if dialogues.is_empty():
		var dial_avant: String = trainer_raw.get("dialogue_avant", "")
		if not dial_avant.is_empty():
			dialogues = [dial_avant]
	if dialogue_apres.is_empty():
		var dial_defaite: String = trainer_raw.get("dialogue_defaite", "")
		if not dial_defaite.is_empty():
			dialogue_apres = [dial_defaite]
	# Mettre à jour le statut battu avec le trainer_id
	battu = PlayerData.dresseur_est_battu(trainer_id) or PlayerData.dresseur_est_battu(npc_id)

# Calculer la direction pour faire face au joueur
func _direction_vers(cible: Node) -> String:
	var delta := cible.position - position
	if abs(delta.x) > abs(delta.y):
		return "droite" if delta.x > 0 else "gauche"
	return "bas" if delta.y > 0 else "haut"

func _direction_vers_vec(dir: String) -> Vector2:
	match dir:
		"haut":    return Vector2(0, -1)
		"bas":     return Vector2(0, 1)
		"gauche":  return Vector2(-1, 0)
		"droite":  return Vector2(1, 0)
	return Vector2(0, 1)

func _appliquer_direction(dir: String) -> void:
	direction_initiale = dir
	if sprite and sprite.sprite_frames:
		var anim := dir + "_idle"
		if sprite.sprite_frames.has_animation(anim):
			sprite.play(anim)
		elif sprite.sprite_frames.has_animation(dir):
			sprite.play(dir)
		elif sprite.sprite_frames.has_animation("default"):
			sprite.play("default")

# Charger le sprite du PNJ depuis le dossier characters
func _charger_sprite(sprite_id: String) -> void:
	var chemin := "res://assets/sprites/characters/%s_bas_0.png" % sprite_id
	var texture := load(chemin) as Texture2D
	if texture == null:
		# Fallback : utiliser le sprite homme par défaut
		texture = load("res://assets/sprites/characters/pnj_homme_bas_0.png") as Texture2D
	if texture == null:
		return
	# Créer un SpriteFrames basique avec une seule frame
	var frames := SpriteFrames.new()
	frames.add_animation("default")
	frames.set_animation_speed("default", 1.0)
	frames.set_animation_loop("default", false)
	frames.add_frame("default", texture)
	# Ajouter les animations directionnelles (même texture pour le MVP)
	for dir_name in ["bas_idle", "haut_idle", "gauche_idle", "droite_idle"]:
		frames.add_animation(dir_name)
		frames.set_animation_speed(dir_name, 1.0)
		frames.set_animation_loop(dir_name, false)
		frames.add_frame(dir_name, texture)
	# Supprimer l'animation "default" auto-créée si elle est vide
	if frames.has_animation("default") and frames.get_frame_count("default") == 0:
		frames.remove_animation("default")
	sprite.sprite_frames = frames
	sprite.play("bas_idle")
