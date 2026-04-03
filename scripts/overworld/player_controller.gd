extends CharacterBody2D

# PlayerController — Déplacement du joueur sur la grille 32×32px
# Gère les déplacements, le sprint, les interactions, les transitions de carte

# --- Constantes ---
const TAILLE_TILE := 32
const VITESSE_MARCHE := 4.0    # tiles/seconde
const VITESSE_SPRINT := 7.0    # tiles/seconde (avec Shift)
const VITESSE_VELO := 9.0      # tiles/seconde (avec Vélo)

# --- Nœuds ---
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var ray_interaction: RayCast2D = $RayInteraction
@onready var camera: Camera2D = null

# --- État ---
var en_deplacement: bool = false
var position_grille: Vector2i = Vector2i(7, 12)
var direction_actuelle: Vector2i = Vector2i(0, 1)  # bas par défaut
var peut_bouger: bool = true  # désactivé pendant les dialogues/combats
var est_sur_eau: bool = false  # true si le joueur surfe
var sur_velo: bool = false     # true si le joueur est sur le vélo

# --- Signaux ---
signal pas_effectue()  # émis à chaque pas (utilisé par le Safari)

# --- Déplacement ---
var cible_monde: Vector2 = Vector2.ZERO
var vitesse_courante: float = VITESSE_MARCHE

func _ready() -> void:
	add_to_group("joueur")
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
	# Vérifier sprint / vélo
	if sur_velo:
		vitesse_courante = VITESSE_VELO
	elif Input.is_action_pressed("action_sprint"):
		vitesse_courante = VITESSE_SPRINT
	else:
		vitesse_courante = VITESSE_MARCHE

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
		# Ne relancer l'animation idle que si on ne la joue pas déjà
		var anim_idle := _vec_vers_direction(direction_actuelle) + "_idle"
		if sprite and sprite.sprite_frames and sprite.animation != anim_idle:
			_mettre_a_jour_animation(_vec_vers_direction(direction_actuelle), false)
		return

	# Tourner d'abord si direction différente (comportement Pokémon original)
	if dir != direction_actuelle:
		direction_actuelle = dir
		_mettre_a_jour_animation(_vec_vers_direction(dir), false)
		# Ne pas marcher au premier frame — juste tourner
		return

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
	# Signal de pas (pour Safari, etc.)
	emit_signal("pas_effectue")
	# Décrémenter le compteur Repousse dans GameManager
	# (Le EncounterSystem gère la logique de blocage)
	
	# Vérifier warp
	if _verifier_warp():
		return
	# Vérifier téléporteur d'arène (Safrania)
	_verifier_teleporteur()
	# Rencontres aquatiques si en surf
	if est_sur_eau:
		EncounterSystem.verifier_rencontre_surf(position_grille, self)
		return
	# Rencontres en grotte (chaque pas peut déclencher un combat)
	if EncounterSystem.est_carte_cave():
		EncounterSystem.verifier_rencontre_cave(self)
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
			# Si on surfe, on peut passer les collisions d'eau
			# Mais on ne peut pas aller sur la terre ferme sans descendre du surf
			return false
	
	# Vérifier si la case cible est de l'eau
	var tilemap := _get_tilemap()
	if tilemap:
		var is_water := SurfSystem.est_case_eau(tilemap, cible)
		if is_water and not est_sur_eau:
			# Proposer de surfer si le joueur a la CS
			return false  # L'interaction Surf se fait via _interagir()
		elif not is_water and est_sur_eau:
			# Descendre du surf quand on atteint la terre
			est_sur_eau = false
			sprite.modulate = Color.WHITE
	
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
			# --- Interception Prof. Chen à Bourg Palette ---
			if PlayerData.carte_actuelle == "bourg_palette" and not GameManager.get_flag("premier_pokemon_recu"):
				_intercepter_chen()
				return true
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
	# Bloquer la sortie vers la salle suivante si le membre du Conseil 4 n'est pas battu
	if warp.get("id", "") == "sortie_suivante":
		var flag_requis := _get_flag_ligue_requis(PlayerData.carte_actuelle)
		if not flag_requis.is_empty() and not GameManager.get_flag(flag_requis):
			return  # Warp bloqué : vaincre le champion d'abord

	# Vérifier les conditions d'accès au warp (ex: arène Jadielle = 7 badges)
	var condition: Dictionary = warp.get("condition", {})
	if not condition.is_empty():
		var cond_type: String = condition.get("type", "")
		var autorise: bool = true

		if cond_type == "badges":
			var nb_requis: int = condition.get("nombre", 0)
			if GameManager.nombre_badges() < nb_requis:
				autorise = false
		elif cond_type == "flag":
			var flag_cle: String = condition.get("flag", "")
			var flag_val = condition.get("valeur", true)
			if not flag_cle.is_empty() and GameManager.get_flag(flag_cle) != flag_val:
				autorise = false

		if not autorise:
			# Afficher le message de refus
			var msg_refus: String = condition.get("message_refus", "L'accès est bloqué.")
			var scene_root := get_tree().current_scene
			var dialog_box_node = scene_root.get("dialog_box") if scene_root else null
			if dialog_box_node and dialog_box_node.has_method("afficher_dialogue"):
				dialog_box_node.afficher_dialogue([msg_refus])
			return  # Warp bloqué

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


## Interception du Prof. Chen quand le joueur essaie de quitter Bourg Palette
## sans avoir de Pokémon. Le professeur le ramène au laboratoire.
func _intercepter_chen() -> void:
	peut_bouger = false
	# Faire reculer le joueur d'un pas (il était en train de sortir)
	position_grille.y = 0
	position = Vector2(position_grille) * TAILLE_TILE
	cible_monde = position
	en_deplacement = false
	direction_actuelle = Vector2i(0, -1)
	_mettre_a_jour_animation("haut", false)

	await get_tree().create_timer(0.3).timeout

	# Afficher le message d'avertissement du Prof. Chen via le DialogBox de la scène
	var scene_root := get_tree().current_scene
	var dialog_box = scene_root.get("dialog_box") if scene_root else null
	if dialog_box and dialog_box.has_method("afficher_dialogue"):
		dialog_box.afficher_dialogue([
			"PROF. CHEN : Hé ! Attends !",
			"C'est dangereux de s'aventurer\ndans les hautes herbes sans POKÉMON !",
			"Suis-moi à mon laboratoire !"
		])
		await dialog_box.dialogue_termine
	else:
		# Fallback : simple timer si pas de DialogBox
		await get_tree().create_timer(2.0).timeout

	# Rediriger vers le laboratoire du Prof. Chen
	PlayerData.sauvegarder_position("laboratoire_chen", 5, 8, "haut")
	SceneManager.charger_scene("res://scenes/maps/laboratoire_chen.tscn", {
		"carte_id": "laboratoire_chen",
		"intercepte_par_chen": true
	})

## Retourne le flag requis pour débloquer le warp de sortie de la salle E4
func _get_flag_ligue_requis(carte_id: String) -> String:
	match carte_id:
		"ligue_olga":   return "conseil_olga_battu"
		"ligue_aldo":   return "conseil_aldo_battu"
		"ligue_agatha": return "conseil_agatha_battu"
		"ligue_peter":  return "conseil_peter_battu"
	return ""

## Vérifier si le joueur est sur un téléporteur (puzzle arène Safrania)
func _verifier_teleporteur() -> void:
	var scene_root := get_tree().current_scene
	if scene_root and scene_root.has_method("verifier_teleporteur"):
		var dest: Dictionary = scene_root.verifier_teleporteur(position_grille)
		if not dest.is_empty():
			# Téléporter le joueur à la destination
			AudioManager.jouer_sfx("res://assets/audio/sfx/teleport.ogg")
			peut_bouger = false
			await get_tree().create_timer(0.3).timeout
			teleporter(dest.get("x", 0), dest.get("y", 0), "bas")
			peut_bouger = true

func _interagir() -> void:
	# Orienter le RayCast vers la direction du joueur et détecter
	ray_interaction.target_position = Vector2(direction_actuelle) * TAILLE_TILE
	ray_interaction.force_raycast_update()
	if ray_interaction.is_colliding():
		var collider = ray_interaction.get_collider()
		if collider and collider.has_method("interagir"):
			collider.interagir(self)
			return
		# Vérifier si c'est une poubelle (puzzle arène Carmin)
		if collider and collider.has_meta("type") and collider.get_meta("type") == "poubelle":
			var idx: int = collider.get_meta("poubelle_index", -1)
			if idx >= 0:
				var scene_root := get_tree().current_scene
				if scene_root and scene_root.has_method("interagir_poubelle"):
					scene_root.interagir_poubelle(idx)
				return
	
	# Si la case devant est de l'eau et qu'on n'est pas encore en train de surfer
	var tilemap := _get_tilemap()
	if tilemap and not est_sur_eau:
		var cible := position_grille + direction_actuelle
		if SurfSystem.est_case_eau(tilemap, cible) and SurfSystem.peut_surfer():
			_commencer_surf()
			return
	
	# Pêche : si on est face à l'eau et qu'on a une canne
	if tilemap and not est_sur_eau:
		var cible := position_grille + direction_actuelle
		if FishingSystem.peut_pecher(tilemap, position_grille, direction_actuelle):
			_lancer_peche()
			return

# --- Système de Surf ---
func _commencer_surf() -> void:
	est_sur_eau = true
	sprite.modulate = Color(0.7, 0.85, 1.0)  # Teinte bleutée pour indiquer le surf
	AudioManager.jouer_sfx("res://assets/audio/sfx/surf.ogg")
	# Se déplacer sur la première case d'eau
	var cible := position_grille + direction_actuelle
	position_grille = cible
	cible_monde = Vector2(position_grille) * TAILLE_TILE
	en_deplacement = true
	_mettre_a_jour_animation(_vec_vers_direction(direction_actuelle), true)

# --- Système de Pêche ---
func _lancer_peche() -> void:
	peut_bouger = false
	# Obtenir la zone d'encounter
	var zone_id := _obtenir_zone_encounter()
	if zone_id.is_empty():
		peut_bouger = true
		return
	
	var pokemon_data := FishingSystem.pecher(zone_id)
	if pokemon_data.is_empty():
		# Rien n'a mordu
		AudioManager.jouer_sfx("res://assets/audio/sfx/fishing_fail.ogg")
		# TODO: afficher message "Rien ne mord..."
		await get_tree().create_timer(1.0).timeout
		peut_bouger = true
		return
	
	# Ajuster le niveau selon la canne
	pokemon_data = FishingSystem.ajuster_niveau_peche(pokemon_data)
	var espece_id: String = pokemon_data.get("pokemon_id", "129")  # Magicarpe par défaut
	var niveau := randi_range(pokemon_data.get("niveau_min", 5), pokemon_data.get("niveau_max", 15))
	
	AudioManager.jouer_sfx("res://assets/audio/sfx/encounter.ogg")
	SceneManager.charger_scene("res://scenes/battle/battle_scene.tscn", {
		"type_combat": "sauvage",
		"espece_id": espece_id,
		"niveau": niveau,
		"pokemon_joueur_index": 0,
		"carte_retour": PlayerData.carte_actuelle,
		"musique_carte": MapLoader.get_carte(PlayerData.carte_actuelle).get("musique", "")
	})

func _obtenir_zone_encounter() -> String:
	# Chercher la zone de rencontre pour cette carte (pour la pêche/surf)
	var carte_data := MapLoader.get_carte(PlayerData.carte_actuelle)
	# D'abord chercher dans les zones d'herbes (qui peuvent avoir aussi des données pêche)
	for zone in carte_data.get("zones_herbes", []):
		var x1: int = zone.get("x1", 0)
		var y1: int = zone.get("y1", 0)
		var x2: int = zone.get("x2", 0)
		var y2: int = zone.get("y2", 0)
		if position_grille.x >= x1 and position_grille.x <= x2 and \
		   position_grille.y >= y1 and position_grille.y <= y2:
			return zone.get("table", "")
	# Sinon utiliser l'ID de la carte directement comme zone
	return PlayerData.carte_actuelle

func _get_tilemap() -> TileMap:
	var parent := get_parent()
	if parent == null:
		return null
	var scene := parent.get_parent()
	if scene and scene.has_node("TileMap"):
		return scene.get_node("TileMap") as TileMap
	return null

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
