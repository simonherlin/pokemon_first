extends CharacterBody2D

# PlayerController — Déplacement du joueur sur la grille 32×32px
# Gère les déplacements, le sprint, les interactions, les transitions de carte

# --- Constantes ---
const TAILLE_TILE := 32
const VITESSE_MARCHE := 4.0    # tiles/seconde
const VITESSE_SPRINT := 7.0    # tiles/seconde (avec Shift)

# --- Nœuds ---
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var ray_interaction: RayCast2D = $RayInteraction
@onready var camera: Camera2D = null

# --- État ---
var en_deplacement: bool = false
var position_grille: Vector2i = Vector2i(7, 12)
var direction_actuelle: Vector2i = Vector2i(0, 1)  # bas par défaut
var peut_bouger: bool = true  # désactivé pendant les dialogues/combats

# --- Déplacement ---
var cible_monde: Vector2 = Vector2.ZERO
var vitesse_courante: float = VITESSE_MARCHE

func _ready() -> void:
	position = Vector2(position_grille) * TAILLE_TILE
	cible_monde = position
	# Créer une Camera2D qui suit le joueur
	camera = Camera2D.new()
	camera.position = Vector2(TAILLE_TILE / 2, TAILLE_TILE / 2)
	camera.zoom = Vector2(1, 1)
	camera.enabled = true
	camera.position_smoothing_enabled = true
	camera.position_smoothing_speed = 8.0
	add_child(camera)
	camera.make_current()
	# Sauvegarder la position initiale
	PlayerData.sauvegarder_position(PlayerData.carte_actuelle, position_grille.x, position_grille.y, "bas")
	_mettre_a_jour_animation("bas", false)

func _process(delta: float) -> void:
	if not peut_bouger:
		return

	if en_deplacement:
		_continuer_deplacement(delta)
	else:
		_lire_input()

func _lire_input() -> void:
	# Vérifier sprint
	vitesse_courante = VITESSE_SPRINT if Input.is_action_pressed("action_sprint") else VITESSE_MARCHE

	# Direction demandée
	var dir := Vector2i.ZERO
	if Input.is_action_pressed("action_haut"):
		dir = Vector2i(0, -1)
	elif Input.is_action_pressed("action_bas"):
		dir = Vector2i(0, 1)
	elif Input.is_action_pressed("action_gauche"):
		dir = Vector2i(-1, 0)
	elif Input.is_action_pressed("action_droite"):
		dir = Vector2i(1, 0)

	# Interaction (bouton A)
	if Input.is_action_just_pressed("action_confirmer"):
		_interagir()
		return

	if dir == Vector2i.ZERO:
		_mettre_a_jour_animation(_vec_vers_direction(direction_actuelle), false)
		return

	# Tourner si direction différente
	direction_actuelle = dir
	_mettre_a_jour_animation(_vec_vers_direction(dir), false)

	# Vérifier si la case cible est accessible
	var cible_grille := position_grille + dir
	if not _case_accessible(cible_grille):
		return

	# Démarrer le déplacement
	position_grille = cible_grille
	cible_monde = Vector2(position_grille) * TAILLE_TILE
	en_deplacement = true
	_mettre_a_jour_animation(_vec_vers_direction(dir), true)

func _continuer_deplacement(delta: float) -> void:
	var pas := vitesse_courante * TAILLE_TILE * delta
	var diff := cible_monde - position
	if diff.length() <= pas:
		position = cible_monde
		en_deplacement = false
		_mettre_a_jour_animation(_vec_vers_direction(direction_actuelle), false)
		_arrivee_nouvelle_case()
	else:
		position += diff.normalized() * pas

func _arrivee_nouvelle_case() -> void:
	PlayerData.sauvegarder_position(
		PlayerData.carte_actuelle,
		position_grille.x, position_grille.y,
		_vec_vers_direction(direction_actuelle)
	)
	# Vérifier warp
	if _verifier_warp():
		return
	# Vérifier herbes sauvages
	EncounterSystem.verifier_rencontre(position_grille, self)

func _case_accessible(cible: Vector2i) -> bool:
	# Vérifier les limites de la carte (permet de sortir pour les connexions)
	var carte_data := MapLoader.get_carte(PlayerData.carte_actuelle)
	var largeur: int = carte_data.get("largeur", 20) if not carte_data.is_empty() else 20
	var hauteur: int = carte_data.get("hauteur", 18) if not carte_data.is_empty() else 18
	
	# Permettre de sortir si une connexion existe dans cette direction
	var a_connexion := false
	for connexion in carte_data.get("connexions", []):
		var dir: String = connexion.get("direction", "")
		if dir == "nord" and cible.y < 0:
			a_connexion = true
		elif dir == "sud" and cible.y >= hauteur:
			a_connexion = true
		elif dir == "ouest" and cible.x < 0:
			a_connexion = true
		elif dir == "est" and cible.x >= largeur:
			a_connexion = true
	
	if not a_connexion:
		if cible.x < 0 or cible.x >= largeur or cible.y < 0 or cible.y >= hauteur:
			return false
	elif cible.x < -1 or cible.x > largeur or cible.y < -1 or cible.y > hauteur:
		return false
	
	# Vérifier collision avec le TileMap via le RayCast
	ray_interaction.target_position = Vector2(direction_actuelle) * TAILLE_TILE
	ray_interaction.force_raycast_update()
	if ray_interaction.is_colliding():
		var collider = ray_interaction.get_collider()
		if collider != null:
			return false
	return true

func _verifier_warp() -> bool:
	# Chercher un warp à la position actuelle dans les données de la carte
	var carte_data := MapLoader.get_carte(PlayerData.carte_actuelle)
	if carte_data.is_empty():
		return false
	for warp in carte_data.get("warps", []):
		if warp.get("x", -1) == position_grille.x and warp.get("y", -1) == position_grille.y:
			_entrer_warp(warp)
			return true
	# Vérifier les connexions de carte (bord de la carte)
	var largeur: int = carte_data.get("largeur", 20)
	var hauteur: int = carte_data.get("hauteur", 18)
	for connexion in carte_data.get("connexions", []):
		var dir: String = connexion.get("direction", "")
		var vers: String = connexion.get("vers", "")
		var decalage: int = connexion.get("decalage", 0)
		if dir == "nord" and position_grille.y < 0:
			var vers_data := MapLoader.get_carte(vers)
			var vers_h: int = vers_data.get("hauteur", 18) if not vers_data.is_empty() else 18
			_changer_carte(vers, position_grille.x + decalage, vers_h - 1)
			return true
		elif dir == "sud" and position_grille.y >= hauteur:
			_changer_carte(vers, position_grille.x + decalage, 0)
			return true
		elif dir == "ouest" and position_grille.x < 0:
			var vers_data := MapLoader.get_carte(vers)
			var vers_l: int = vers_data.get("largeur", 20) if not vers_data.is_empty() else 20
			_changer_carte(vers, vers_l - 1, position_grille.y + decalage)
			return true
		elif dir == "est" and position_grille.x >= largeur:
			_changer_carte(vers, 0, position_grille.y + decalage)
			return true
	return false

func _entrer_warp(warp: Dictionary) -> void:
	peut_bouger = false
	var vers_map: String = warp.get("vers_map", "")
	var vers_warp: String = warp.get("vers_warp", "")
	SceneManager.charger_scene("res://scenes/maps/%s.tscn" % vers_map, {
		"warp_entree": vers_warp,
		"carte_id": vers_map
	})

func _changer_carte(vers_carte: String, x: int, y: int) -> void:
	peut_bouger = false
	PlayerData.sauvegarder_position(vers_carte, x, y, _vec_vers_direction(direction_actuelle))
	SceneManager.charger_scene("res://scenes/maps/%s.tscn" % vers_carte, {
		"carte_id": vers_carte
	})

func _interagir() -> void:
	# Orienter le RayCast vers la direction du joueur et détecter
	ray_interaction.target_position = Vector2(direction_actuelle) * TAILLE_TILE
	ray_interaction.force_raycast_update()
	if ray_interaction.is_colliding():
		var collider = ray_interaction.get_collider()
		if collider and collider.has_method("interagir"):
			collider.interagir(self)

func _vec_vers_direction(v: Vector2i) -> String:
	if v == Vector2i(0, -1): return "haut"
	if v == Vector2i(0, 1):  return "bas"
	if v == Vector2i(-1, 0): return "gauche"
	if v == Vector2i(1, 0):  return "droite"
	return "bas"

func _mettre_a_jour_animation(direction: String, marche: bool) -> void:
	if sprite == null:
		return
	var suffix := "_marche" if marche else "_idle"
	var anim := direction + suffix
	if sprite.sprite_frames and sprite.sprite_frames.has_animation(anim):
		sprite.play(anim)
	else:
		# Fallback : animation de base
		if sprite.sprite_frames and sprite.sprite_frames.has_animation(direction):
			sprite.play(direction)

# Bloquer/débloquer les déplacements (appelé par DialogController, BattleScene, etc.)
func set_peut_bouger(valeur: bool) -> void:
	peut_bouger = valeur
	if not valeur:
		_mettre_a_jour_animation(_vec_vers_direction(direction_actuelle), false)

# Téléporter le joueur à une position de grille
func teleporter(x: int, y: int, direction: String = "bas") -> void:
	position_grille = Vector2i(x, y)
	position = Vector2(position_grille) * TAILLE_TILE
	cible_monde = position
	en_deplacement = false
	var dirs := {"haut": Vector2i(0,-1), "bas": Vector2i(0,1), "gauche": Vector2i(-1,0), "droite": Vector2i(1,0)}
	direction_actuelle = dirs.get(direction, Vector2i(0,1))
	_mettre_a_jour_animation(direction, false)
