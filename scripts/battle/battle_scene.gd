extends Node2D

# BattleScene — Scène de combat qui connecte BattleController ↔ BattleHUD
# Reçoit les paramètres de SceneManager et orchestre le combat

# --- Nœuds ---
@onready var hud := $BattleHUD
@onready var sprite_joueur: Sprite2D = $SpriteJoueur
@onready var sprite_ennemi: Sprite2D = $SpriteEnnemi
@onready var sprite_trainer_ennemi: Sprite2D = $SpriteTrainerEnnemi
@onready var background: ColorRect = $Background

# --- Labels HUD ---
@onready var label_nom_joueur: Label = $BattleHUD/PanelJoueur/LabelNom
@onready var label_niveau_joueur: Label = $BattleHUD/PanelJoueur/LabelNiveau
@onready var barre_pv_joueur: ProgressBar = $BattleHUD/PanelJoueur/BarrePV
@onready var label_pv_joueur: Label = $BattleHUD/PanelJoueur/LabelPV
@onready var label_statut_joueur: Label = $BattleHUD/PanelJoueur/LabelStatut

@onready var label_nom_ennemi: Label = $BattleHUD/PanelEnnemi/LabelNom
@onready var label_niveau_ennemi: Label = $BattleHUD/PanelEnnemi/LabelNiveau
@onready var barre_pv_ennemi: ProgressBar = $BattleHUD/PanelEnnemi/BarrePV
@onready var label_statut_ennemi: Label = $BattleHUD/PanelEnnemi/LabelStatut

@onready var label_capture: Label = $BattleHUD/PanelEnnemi/LabelCapture
@onready var barre_exp: ProgressBar = $BattleHUD/PanelJoueur/BarreEXP
@onready var label_exp: Label = $BattleHUD/PanelJoueur/LabelEXP

@onready var label_message: RichTextLabel = $BattleHUD/PanelMessage/LabelMessage
@onready var menu_action: VBoxContainer = $BattleHUD/MenuAction
@onready var menu_attaque: VBoxContainer = $BattleHUD/MenuAttaque

# --- Paramètres reçus ---
var _type_combat: String = "sauvage"
var _carte_retour: String = "bourg_palette"
var _dresseur_data: Dictionary = {}
var _params_retour: Dictionary = {}  # Paramètres supplémentaires à renvoyer à la carte

# --- Sprites dresseurs ---
var _trainer_sprites_data: Dictionary = {}

# --- Battle Controller ---
var _controller: Node = null

# Chemins SFX pour l'UI
const SFX_CURSOR := "res://assets/audio/sfx/cursor_move.ogg"
const SFX_CONFIRM := "res://assets/audio/sfx/confirm.ogg"
const SFX_CANCEL := "res://assets/audio/sfx/cancel.ogg"

# --- État menu ---
var _index_action: int = 0
var _index_attaque: int = 0
var _nb_attaques: int = 0
var _menu_actif: String = ""
var _actions := ["attaque", "sac", "pokemon", "fuite"]

# --- Timer intro (remplacement du await dans _phase_intro) ---
var _intro_timer: float = 0.0
var _intro_en_cours: bool = false
const INTRO_AUTO_AVANCE := 3.0  # secondes avant auto-avancement

# --- Timer de sécurité : récupération si recevoir_params meurt ---
var _scene_timer: float = 0.0
var _combat_demarre: bool = false
var _debug_timer: float = 0.0  # timer pour logs périodiques

# --- Positions de base des sprites (pour animations) ---
var _pos_joueur_base: Vector2 = Vector2.ZERO
var _pos_ennemi_base: Vector2 = Vector2.ZERO
var _tween_pv_joueur: Tween = null
var _tween_pv_ennemi: Tween = null
var _tween_exp: Tween = null

func _ready() -> void:
	menu_action.visible = false
	menu_attaque.visible = false
	# Charger le fond de combat
	var bg_texture := load("res://assets/sprites/ui/battle_bg.png") as Texture2D
	if bg_texture and background:
		background.color = Color(0.75, 0.85, 0.65, 1)
	# Fallback : si recevoir_params n'est jamais appelé, s'auto-initialiser
	call_deferred("_auto_init_fallback")
	# Charger le mapping des sprites de dresseurs
	_charger_trainer_sprites_data()
	# Sauvegarder les positions de base des sprites pour les animations
	if sprite_joueur:
		_pos_joueur_base = sprite_joueur.position
	if sprite_ennemi:
		_pos_ennemi_base = sprite_ennemi.position
	# Initialiser le style de la barre d'EXP
	if barre_exp:
		var fill_style := StyleBoxFlat.new()
		fill_style.bg_color = Color(0.3, 0.5, 1.0)
		fill_style.set_corner_radius_all(2)
		barre_exp.add_theme_stylebox_override("fill", fill_style)
		var bg_style := StyleBoxFlat.new()
		bg_style.bg_color = Color(0.15, 0.15, 0.2)
		bg_style.set_corner_radius_all(2)
		barre_exp.add_theme_stylebox_override("background", bg_style)
	# Cacher l'indicateur de capture par défaut
	if label_capture:
		label_capture.visible = false

# Fallback : appelé via call_deferred depuis _ready
# Si après 2 frames recevoir_params n'a toujours pas été appelé,
# on récupère les params depuis SceneManager.derniers_params_scene
func _auto_init_fallback() -> void:
	# Attendre 2 frames pour laisser SceneManager appeler recevoir_params
	await get_tree().process_frame
	await get_tree().process_frame
	if _controller != null:
		# recevoir_params a déjà été appelé — tout va bien
		return
	# recevoir_params n'a PAS été appelé — fallback
	print("[BattleScene] ⚠ FALLBACK: recevoir_params jamais appelé — récupération params depuis SceneManager")
	var params: Dictionary = SceneManager.derniers_params_scene
	if params.is_empty():
		push_error("[BattleScene] FALLBACK: aucun paramètre disponible — retour carte")
		SceneManager.charger_scene("res://scenes/maps/bourg_palette.tscn", {})
		return
	recevoir_params(params)

func recevoir_params(params: Dictionary) -> void:
	print("[BattleScene] recevoir_params: type=%s, carte_retour=%s" % [params.get("type_combat", "sauvage"), params.get("carte_retour", "?")])
	_type_combat = params.get("type_combat", "sauvage")
	_carte_retour = params.get("carte_retour", "bourg_palette")
	_dresseur_data = params.get("dresseur_data", {})
	# Conserver les paramètres supplémentaires pour les renvoyer à la carte
	if params.get("champion_battu", false):
		_params_retour["champion_battu"] = true

	# --- Lancer la musique de combat ---
	_jouer_musique_combat()

	# Obtenir le Pokémon du joueur
	var pokemon_index: int = params.get("pokemon_joueur_index", 0)
	print("[BattleScene] Equipe joueur: %d pokemon" % PlayerData.equipe.size())
	if PlayerData.equipe.is_empty():
		push_error("BattleScene: équipe du joueur vide !")
		# Retourner à la carte au lieu de rester bloqué
		await get_tree().create_timer(0.5).timeout
		SceneManager.charger_scene("res://scenes/maps/%s.tscn" % _carte_retour, {})
		return
	var pokemon_joueur := Pokemon.from_dict(PlayerData.equipe[pokemon_index])
	if pokemon_joueur == null:
		push_error("[BattleScene] Impossible de créer le Pokémon joueur depuis l'équipe — retour à la carte")
		await get_tree().create_timer(0.5).timeout
		SceneManager.charger_scene("res://scenes/maps/%s.tscn" % _carte_retour, {})
		return
	print("[BattleScene] Pokemon joueur: %s N.%d PV=%d/%d, %d attaques" % [pokemon_joueur.surnom, pokemon_joueur.niveau, pokemon_joueur.pv_actuels, pokemon_joueur.pv_max, pokemon_joueur.attaques.size()])

	# Initialiser le BattleController
	_controller = BattleController
	# Réinitialiser l'état de la machine à états (sécurité entre combats)
	_controller._traitement_etat_en_cours = false
	_controller._etat_en_attente = -1
	_connecter_signaux()

	# Préparer le combat AVANT de démarrer la machine à états
	if _type_combat == "sauvage":
		var espece_id: String = params.get("espece_id", "019")
		var niveau: int = params.get("niveau", 5)
		# Préparer les données sans démarrer la machine à états
		_controller.type_combat = BattleController.TypeCombat.SAUVAGE
		_controller.pokemon_joueur = pokemon_joueur
		_controller.index_pokemon_joueur = pokemon_index
		_controller.pokemon_ennemi = SpeciesData.creer_sauvage(espece_id, niveau)
		if _controller.pokemon_ennemi == null:
			_controller.pokemon_ennemi = SpeciesData.creer_sauvage("001", niveau)
		_controller.tour = 0
	else:
		# Afficher le sprite du dresseur pendant l'intro
		_afficher_sprite_trainer()
		_controller.type_combat = BattleController.TypeCombat.DRESSEUR
		_controller.dresseur_ennemi = _dresseur_data
		_controller.index_pokemon_joueur = pokemon_index
		_controller.equipe_ennemi = []
		for p_data in _dresseur_data.get("equipe", []):
			var p: Pokemon = null
			# Utiliser from_dict si les données sont complètes (to_dict), sinon recréer
			if p_data.has("stats") and p_data.has("attaques"):
				p = Pokemon.from_dict(p_data)
			else:
				p = SpeciesData.creer_pokemon(p_data.get("espece_id", "001"), p_data.get("niveau", 5))
			if p:
				_controller.equipe_ennemi.append(p)
		_controller.index_pokemon_ennemi = 0
		_controller.pokemon_du_joueur_ref = pokemon_joueur
		if _controller.equipe_ennemi.is_empty():
			var p_default := SpeciesData.creer_pokemon("001", 5)
			if p_default:
				_controller.equipe_ennemi.append(p_default)
		_controller.pokemon_ennemi = _controller.equipe_ennemi[0]
		_controller.pokemon_joueur = pokemon_joueur
		_controller.tour = 0

	# Charger les sprites et afficher les infos AVANT l'animation
	_charger_sprites_pokemon()
	_afficher_info_pokemon()
	# Si combat dresseur avec sprite trainer, cacher le sprite Pokémon ennemi pendant l'intro
	if _type_combat != "sauvage" and sprite_trainer_ennemi.visible:
		sprite_ennemi.visible = false

	# Animation d'entrée : slide-in des sprites
	print("[BattleScene] Début animation entrée combat...")
	await _animer_entree_combat()
	print("[BattleScene] Animation entrée terminée")

	# Si combat dresseur, montrer la transition trainer → Pokémon après un délai
	if _type_combat != "sauvage" and sprite_trainer_ennemi.visible:
		print("[BattleScene] Transition trainer → pokémon (1.8s)")
		await get_tree().create_timer(1.8).timeout
		_transition_trainer_vers_pokemon()
		_charger_sprites_pokemon()

	# Jouer le cri du Pokémon ennemi à l'entrée
	if _controller.pokemon_ennemi:
		_jouer_cri_pokemon(_controller.pokemon_ennemi.espece_id)

	# MAINTENANT démarrer la machine à états (après que l'UI est prête)
	print("[BattleScene] Démarrage machine à états → INTRO (combat_demarre=%s)" % _combat_demarre)
	PlayerData.enregistrer_vu(_controller.pokemon_ennemi.espece_id)
	# GARDE : si le timer de sécurité a déjà tiré pendant les await,
	# ne pas revenir en INTRO — le combat est déjà en CHOIX_ACTION
	if _combat_demarre:
		print("[BattleScene] Combat déjà démarré (sécurité a tiré) — skip INTRO, on reste en CHOIX_ACTION")
		return
	_controller._changer_etat(BattleController.Etat.INTRO)
	# Activer le timer d'intro — _process() gère l'avancement
	_intro_en_cours = true
	_intro_timer = 0.0
	print("[BattleScene] Intro activée — en attente input (max %.1fs)" % INTRO_AUTO_AVANCE)

# Charger les textures front/back des Pokémon en combat
func _charger_sprites_pokemon() -> void:
	if not _controller:
		return
	# Sprite du joueur (dos) — sprites 96×96 depuis PokeAPI Gen V
	if _controller.pokemon_joueur:
		var back_path := "res://assets/sprites/pokemon/back/%s.png" % _controller.pokemon_joueur.espece_id
		var back_tex := load(back_path) as Texture2D
		if back_tex:
			sprite_joueur.texture = back_tex
			sprite_joueur.scale = Vector2(1.8, 1.8)
			# Réinitialiser position, visibilité et alpha (après KO ou transition)
			sprite_joueur.position = _pos_joueur_base
			sprite_joueur.modulate = Color.WHITE
			sprite_joueur.visible = true
	# Sprite de l'ennemi (face)
	if _controller.pokemon_ennemi:
		var front_path := "res://assets/sprites/pokemon/front/%s.png" % _controller.pokemon_ennemi.espece_id
		var front_tex := load(front_path) as Texture2D
		if front_tex:
			sprite_ennemi.texture = front_tex
			sprite_ennemi.scale = Vector2(1.5, 1.5)
			# Réinitialiser position, visibilité et alpha (après KO ou transition)
			sprite_ennemi.position = _pos_ennemi_base
			sprite_ennemi.modulate = Color.WHITE
			sprite_ennemi.visible = true

func _connecter_signaux() -> void:
	if not _controller:
		return
	# Déconnecter les anciens signaux s'ils existent (sécurité singleton)
	_deconnecter_signaux()
	_controller.message_affiche.connect(_on_message)
	_controller.action_requise.connect(_on_action_requise)
	_controller.attaque_requise.connect(_on_attaque_requise)
	_controller.pv_mis_a_jour.connect(_on_pv_mis_a_jour)
	_controller.statut_mis_a_jour.connect(_on_statut_mis_a_jour)
	_controller.combat_termine.connect(_on_combat_termine)
	_controller.evolution_proposee.connect(_on_evolution_proposee)
	_controller.attaque_a_apprendre.connect(_on_attaque_a_apprendre)
	_controller.pokemon_change.connect(_on_pokemon_change)
	_controller.animation_attaque.connect(_on_animation_attaque)
	_controller.exp_gagnee.connect(_on_exp_gagnee)
	_controller.animation_capture.connect(_on_animation_capture)


func _deconnecter_signaux() -> void:
	if not _controller:
		return
	var signaux := [
		[_controller.message_affiche, _on_message],
		[_controller.action_requise, _on_action_requise],
		[_controller.attaque_requise, _on_attaque_requise],
		[_controller.pv_mis_a_jour, _on_pv_mis_a_jour],
		[_controller.statut_mis_a_jour, _on_statut_mis_a_jour],
		[_controller.combat_termine, _on_combat_termine],
		[_controller.evolution_proposee, _on_evolution_proposee],
		[_controller.attaque_a_apprendre, _on_attaque_a_apprendre],
		[_controller.pokemon_change, _on_pokemon_change],
		[_controller.animation_attaque, _on_animation_attaque],
		[_controller.exp_gagnee, _on_exp_gagnee],
		[_controller.animation_capture, _on_animation_capture],
	]
	for s in signaux:
		if s[0].is_connected(s[1]):
			s[0].disconnect(s[1])


func _exit_tree() -> void:
	# Nettoyage des signaux quand la scène est détruite
	_deconnecter_signaux()

func _on_message(texte: String) -> void:
	label_message.text = texte

func _on_action_requise() -> void:
	label_message.text = "Que faire ?"
	_afficher_info_pokemon()
	_index_action = 0
	menu_action.visible = true
	menu_attaque.visible = false
	_menu_actif = "action"
	_maj_curseur_action()

func _on_attaque_requise() -> void:
	_index_attaque = 0
	menu_action.visible = false
	menu_attaque.visible = true
	_menu_actif = "attaque"
	_nb_attaques = _controller.pokemon_joueur.attaques.size()
	_maj_menu_attaque()
	_maj_curseur_attaque()

func _on_pv_mis_a_jour(joueur: bool, pv: int, pv_max: int) -> void:
	# Animation fluide de la barre de PV via tween
	if joueur:
		barre_pv_joueur.max_value = pv_max
		if _tween_pv_joueur:
			_tween_pv_joueur.kill()
		_tween_pv_joueur = create_tween()
		_tween_pv_joueur.tween_property(barre_pv_joueur, "value", float(pv), 0.5).set_ease(Tween.EASE_OUT)
		label_pv_joueur.text = "%d/%d" % [pv, pv_max]
		# Colorer la barre selon le pourcentage de PV
		var pct := float(pv) / float(maxi(pv_max, 1))
		if pct <= 0.2:
			barre_pv_joueur.modulate = Color(1.0, 0.3, 0.3)
		elif pct <= 0.5:
			barre_pv_joueur.modulate = Color(1.0, 0.85, 0.2)
		else:
			barre_pv_joueur.modulate = Color(0.3, 0.9, 0.3)
	else:
		barre_pv_ennemi.max_value = pv_max
		if _tween_pv_ennemi:
			_tween_pv_ennemi.kill()
		_tween_pv_ennemi = create_tween()
		_tween_pv_ennemi.tween_property(barre_pv_ennemi, "value", float(pv), 0.5).set_ease(Tween.EASE_OUT)
		var pct := float(pv) / float(maxi(pv_max, 1))
		if pct <= 0.2:
			barre_pv_ennemi.modulate = Color(1.0, 0.3, 0.3)
		elif pct <= 0.5:
			barre_pv_ennemi.modulate = Color(1.0, 0.85, 0.2)
		else:
			barre_pv_ennemi.modulate = Color(0.3, 0.9, 0.3)

func _on_statut_mis_a_jour(joueur: bool, statut: String) -> void:
	var abrev := _abreger_statut(statut)
	if joueur:
		label_statut_joueur.text = abrev
		label_statut_joueur.visible = not statut.is_empty()
	else:
		label_statut_ennemi.text = abrev
		label_statut_ennemi.visible = not statut.is_empty()

# Gérer le changement de Pokémon (envoi du suivant par le dresseur, ou échange joueur)
func _on_pokemon_change(joueur: bool) -> void:
	if joueur:
		# Pokémon joueur KO → forcer le choix d'un remplaçant
		if _controller.pokemon_joueur and _controller.pokemon_joueur.est_ko():
			await _animer_ko(sprite_joueur)
			_charger_sprites_pokemon()
			_afficher_info_pokemon()
			# Sauvegarder l'état du KO
			PlayerData.equipe[_controller.index_pokemon_joueur] = _controller.pokemon_joueur.to_dict()
			_ouvrir_switch_combat(true)
			return
		# Switch normal (joueur_change_pokemon déjà appelé)
		_charger_sprites_pokemon()
		await _animer_apparition(sprite_joueur)
		_afficher_info_pokemon()
		_jouer_cri_pokemon(_controller.pokemon_joueur.espece_id)
	else:
		# Pokémon ennemi KO → animer la chute
		if _controller.pokemon_ennemi and _controller.pokemon_ennemi.est_ko():
			await _animer_ko(sprite_ennemi)
		_charger_sprites_pokemon()
		if _controller.pokemon_ennemi and not _controller.pokemon_ennemi.est_ko():
			await _animer_apparition(sprite_ennemi)
		_afficher_info_pokemon()
		if _controller.pokemon_ennemi:
			_jouer_cri_pokemon(_controller.pokemon_ennemi.espece_id)

func _on_combat_termine(victoire: bool) -> void:
	_deconnecter_signaux()
	
	# Jouer la musique de victoire ou arrêter la musique de combat
	if victoire:
		_jouer_musique_victoire()
	else:
		AudioManager.arreter_musique()
	
	# Sauvegarder l'état des PV dans l'équipe
	if _controller.pokemon_joueur:
		PlayerData.equipe[_controller.index_pokemon_joueur] = _controller.pokemon_joueur.to_dict()
	# Défaite pendant le Conseil 4 → KO total → retour au Centre Pokémon du Plateau
	if not victoire and GameManager.get_flag("ligue_en_cours"):
		GameManager.set_flag("ligue_en_cours", false)
		# Réinitialiser les flags E4 pour recommencer
		GameManager.set_flag("conseil_olga_battu", false)
		GameManager.set_flag("conseil_aldo_battu", false)
		GameManager.set_flag("conseil_agatha_battu", false)
		GameManager.set_flag("conseil_peter_battu", false)
		# Soigner l'équipe et téléporter au Centre Pokémon
		for i in range(PlayerData.equipe.size()):
			var p := Pokemon.from_dict(PlayerData.equipe[i])
			p.soigner_complet()
			PlayerData.equipe[i] = p.to_dict()
		await get_tree().create_timer(2.0).timeout
		SceneManager.charger_scene("res://scenes/maps/centre_pokemon_plateau.tscn", {
			"warp_entree": "sortie"
		})
		return
	# Vérifier si c'est la victoire contre le champion de la Ligue → Hall of Fame → crédits
	if victoire and _carte_retour == "ligue_champion" and _params_retour.get("champion_battu", false):
		GameManager.set_flag("champion_ligue_battu", true)
		GameManager.set_flag("generique_vu", true)
		GameManager.set_flag("grotte_inconnue_ouverte", true)
		PlayerData.marquer_dresseur_battu("champion_rival_ligue")
		await get_tree().create_timer(2.0).timeout
		# Afficher le Hall of Fame avant les crédits
		var hof_scr = load("res://scripts/ui/hall_of_fame_screen.gd")
		var hof := CanvasLayer.new()
		hof.set_script(hof_scr)
		add_child(hof)
		await hof.ecran_ferme
		SceneManager.charger_scene("res://scenes/ui/credits_screen.tscn", {})
		return
	# Défaite hors E4 → soigner + retour au dernier Centre Pokémon (whiteout)
	if not victoire:
		for i in range(PlayerData.equipe.size()):
			var p := Pokemon.from_dict(PlayerData.equipe[i])
			p.soigner_complet()
			PlayerData.equipe[i] = p.to_dict()
		var dc: Dictionary = GameManager.dernier_centre
		var carte_retour_id: String = dc.get("carte_id", "bourg_palette")
		await get_tree().create_timer(2.0).timeout
		SceneManager.charger_scene("res://scenes/maps/%s.tscn" % carte_retour_id, {
			"warp_entree": ""
		})
		return
	# Retour à la carte
	await get_tree().create_timer(2.0).timeout
	var retour_params := {"carte_id": _carte_retour}
	retour_params.merge(_params_retour)
	SceneManager.charger_scene("res://scenes/maps/%s.tscn" % _carte_retour, retour_params)

func _afficher_info_pokemon() -> void:
	if not _controller:
		return
	var pj: Pokemon = _controller.pokemon_joueur
	var pe: Pokemon = _controller.pokemon_ennemi
	if pj:
		label_nom_joueur.text = pj.surnom
		label_niveau_joueur.text = "N.%d" % pj.niveau
		barre_pv_joueur.max_value = pj.pv_max
		barre_pv_joueur.value = pj.pv_actuels
		label_pv_joueur.text = "%d/%d" % [pj.pv_actuels, pj.pv_max]
		_maj_barre_exp(pj)
	if pe:
		label_nom_ennemi.text = pe.surnom
		label_niveau_ennemi.text = "N.%d" % pe.niveau
		barre_pv_ennemi.max_value = pe.pv_max
		barre_pv_ennemi.value = pe.pv_actuels
		_maj_indicateur_capture(pe)

func _process(delta: float) -> void:
	# Log périodique toutes les 3 secondes pour diagnostic
	_debug_timer += delta
	if _debug_timer >= 3.0:
		_debug_timer = 0.0
		var etat_ctrl := "null"
		if _controller:
			etat_ctrl = BattleController.Etat.keys()[_controller.etat_actuel] if _controller.etat_actuel < BattleController.Etat.size() else str(_controller.etat_actuel)
		print("[BattleScene] ÉTAT: menu=%s, intro=%s, demarre=%s, ctrl=%s" % [_menu_actif, _intro_en_cours, _combat_demarre, etat_ctrl])
	# Timer de sécurité : si après 5 secondes le combat n'a pas démarré correctement
	if not _combat_demarre:
		_scene_timer += delta
		if _scene_timer >= 5.0:
			if _controller:
				print("[BattleScene] SÉCURITÉ: combat pas démarré après 5s — forçage CHOIX_ACTION")
				_combat_demarre = true
				_intro_en_cours = false
				if _controller.pokemon_joueur and _controller.pokemon_ennemi:
					_controller._changer_etat(BattleController.Etat.CHOIX_ACTION)
				else:
					push_error("[BattleScene] SÉCURITÉ: pokemon null — retour à la carte")
					SceneManager.charger_scene("res://scenes/maps/%s.tscn" % _carte_retour, {})
				return
			elif _scene_timer >= 10.0:
				# 10 secondes et toujours pas de controller — abandon total
				push_error("[BattleScene] CRITIQUE: 10s sans controller — retour carte")
				SceneManager.charger_scene("res://scenes/maps/%s.tscn" % _carte_retour, {})
				return
	# Gérer l'avancement de l'intro (remplace le await timer dans le controller)
	if _intro_en_cours:
		_intro_timer += delta
		if Input.is_action_just_pressed("action_confirmer") or _intro_timer >= INTRO_AUTO_AVANCE:
			print("[BattleScene] Intro avancée (timer=%.1fs, input=%s)" % [_intro_timer, Input.is_action_just_pressed("action_confirmer")])
			_intro_en_cours = false
			_intro_timer = 0.0
			_combat_demarre = true
			if _controller:
				_controller.avancer_intro()
		return
	# Filet de sécurité : si le contrôleur est en CHOIX_ACTION mais le menu n'est pas actif
	if _controller and _controller.etat_actuel == BattleController.Etat.CHOIX_ACTION and _menu_actif == "":
		print("[BattleScene] FILET: CHOIX_ACTION mais menu vide — réactivation menu")
		_on_action_requise()
		return
	match _menu_actif:
		"action":
			_gerer_input_action()
		"attaque":
			_gerer_input_attaque()

func _gerer_input_action() -> void:
	if Input.is_action_just_pressed("action_haut"):
		_index_action = (_index_action - 1 + _actions.size()) % _actions.size()
		AudioManager.jouer_sfx(SFX_CURSOR)
		_maj_curseur_action()
	elif Input.is_action_just_pressed("action_bas"):
		_index_action = (_index_action + 1) % _actions.size()
		AudioManager.jouer_sfx(SFX_CURSOR)
		_maj_curseur_action()
	elif Input.is_action_just_pressed("action_confirmer"):
		print("[BattleScene] ACTION CONFIRMÉE: %s (index=%d)" % [_actions[_index_action], _index_action])
		AudioManager.jouer_sfx(SFX_CONFIRM)
		_menu_actif = ""
		menu_action.visible = false
		_executer_action(_actions[_index_action])

func _gerer_input_attaque() -> void:
	# Sécurité : si aucune attaque, revenir au menu action
	if _nb_attaques <= 0:
		if Input.is_action_just_pressed("action_confirmer") or Input.is_action_just_pressed("action_annuler"):
			AudioManager.jouer_sfx(SFX_CANCEL)
			_menu_actif = ""
			menu_attaque.visible = false
			_on_action_requise()
		return
	if Input.is_action_just_pressed("action_haut"):
		_index_attaque = (_index_attaque - 1 + _nb_attaques) % _nb_attaques
		AudioManager.jouer_sfx(SFX_CURSOR)
		_maj_curseur_attaque()
	elif Input.is_action_just_pressed("action_bas"):
		_index_attaque = (_index_attaque + 1) % _nb_attaques
		AudioManager.jouer_sfx(SFX_CURSOR)
		_maj_curseur_attaque()
	elif Input.is_action_just_pressed("action_confirmer"):
		# Vérifier qu'il y a des attaques disponibles avant de confirmer
		if _nb_attaques <= 0 or _index_attaque >= _nb_attaques:
			AudioManager.jouer_sfx(SFX_CANCEL)
			_menu_actif = ""
			menu_attaque.visible = false
			_on_action_requise()
			return
		AudioManager.jouer_sfx(SFX_CONFIRM)
		_menu_actif = ""
		menu_attaque.visible = false
		_controller.joueur_choisit_attaque(_index_attaque)
	elif Input.is_action_just_pressed("action_annuler"):
		AudioManager.jouer_sfx(SFX_CANCEL)
		_menu_actif = ""
		menu_attaque.visible = false
		_on_action_requise()

func _executer_action(action: String) -> void:
	match action:
		"attaque":
			_on_attaque_requise()
		"sac":
			_ouvrir_sac_combat()
		"pokemon":
			_ouvrir_switch_combat(false)
		"fuite":
			_controller.joueur_tente_fuite()

# --- Sac en combat ---
func _ouvrir_sac_combat() -> void:
	var bag_screen: Node = load("res://scripts/ui/battle_bag_screen.gd").new()
	add_child(bag_screen)
	_menu_actif = ""
	bag_screen.item_choisi.connect(func(item_id: String):
		bag_screen.queue_free()
		_utiliser_item_combat(item_id)
	)
	bag_screen.ecran_ferme.connect(func():
		bag_screen.queue_free()
		_on_action_requise()
	)

func _utiliser_item_combat(item_id: String) -> void:
	var item_data: Dictionary = ItemsData.get_item(item_id)
	var categorie: String = item_data.get("categorie", "")
	if not item_data.get("utilisable_combat", false):
		label_message.text = "Pas utilisable ici !"
		await get_tree().create_timer(1.0).timeout
		_on_action_requise()
		return
	if categorie == "balls":
		_controller.joueur_tente_capture(item_id)
	elif categorie in ["objets"]:
		var effet: Dictionary = item_data.get("effet", {})
		var type_effet: String = effet.get("type", "")
		if type_effet in ["soin_pv", "guerison_statut", "soin_total", "rappel", "soin_pp", "soin_pp_all"]:
			_choisir_cible_soin(item_id, item_data)
		else:
			label_message.text = "Pas utilisable ici !"
			await get_tree().create_timer(1.0).timeout
			_on_action_requise()
	else:
		label_message.text = "Pas utilisable ici !"
		await get_tree().create_timer(1.0).timeout
		_on_action_requise()

func _choisir_cible_soin(item_id: String, item_data: Dictionary) -> void:
	var switch_screen: Node = load("res://scripts/ui/battle_switch_screen.gd").new()
	switch_screen.index_actif = -1  # Tous sélectionnables pour le soin
	add_child(switch_screen)
	switch_screen.pokemon_choisi.connect(func(index: int):
		switch_screen.queue_free()
		_appliquer_soin_combat(item_id, item_data, index)
	)
	switch_screen.ecran_ferme.connect(func():
		switch_screen.queue_free()
		_on_action_requise()
	)

func _appliquer_soin_combat(item_id: String, item_data: Dictionary, index_cible: int) -> void:
	var p_data: Dictionary = PlayerData.equipe[index_cible]
	var effet: Dictionary = item_data.get("effet", {})
	var type_effet: String = effet.get("type", "")
	var nom_item: String = item_data.get("nom", item_id)
	var surnom: String = p_data.get("surnom", "???")
	var pv_act: int = p_data.get("pv_actuels", 0)
	var pv_max: int = p_data.get("stats", {}).get("pv", 1)
	var applique := false

	match type_effet:
		"soin_pv":
			if pv_act <= 0 or pv_act >= pv_max:
				label_message.text = "Ça n'aura aucun effet !"
				await get_tree().create_timer(1.0).timeout
				_on_action_requise()
				return
			var soin: int = effet.get("montant", 20)
			p_data["pv_actuels"] = mini(pv_act + soin, pv_max)
			applique = true
		"soin_total":
			if pv_act <= 0:
				label_message.text = "Ça n'aura aucun effet !"
				await get_tree().create_timer(1.0).timeout
				_on_action_requise()
				return
			p_data["pv_actuels"] = pv_max
			p_data["statut"] = ""
			applique = true
		"guerison_statut":
			var statut_soigne: String = effet.get("statut", "")
			var statut_actuel: String = p_data.get("statut", "")
			if statut_actuel.is_empty() or (not statut_soigne.is_empty() and statut_actuel != statut_soigne):
				label_message.text = "Ça n'aura aucun effet !"
				await get_tree().create_timer(1.0).timeout
				_on_action_requise()
				return
			p_data["statut"] = ""
			applique = true
		"rappel":
			if pv_act > 0:
				label_message.text = "Ça n'aura aucun effet !"
				await get_tree().create_timer(1.0).timeout
				_on_action_requise()
				return
			var pct_rappel: int = effet.get("montant", 50)
			var soin_rappel: int = maxi(1, int(pv_max * pct_rappel / 100.0))
			p_data["pv_actuels"] = mini(soin_rappel, pv_max)
			p_data["statut"] = ""
			applique = true

	if applique:
		PlayerData.retirer_item(item_id)
		PlayerData.equipe[index_cible] = p_data
		# Synchroniser le Pokémon actif en combat si c'est celui qui est soigné
		if index_cible == _controller.index_pokemon_joueur and _controller.pokemon_joueur:
			_controller.pokemon_joueur.pv_actuels = p_data["pv_actuels"]
			_controller.pokemon_joueur.statut = p_data.get("statut", "")
			_on_pv_mis_a_jour(true, _controller.pokemon_joueur.pv_actuels, _controller.pokemon_joueur.pv_max)
			_controller.emit_signal("statut_mis_a_jour", true, _controller.pokemon_joueur.statut)
		label_message.text = "Tu utilises %s sur %s !" % [nom_item, surnom]
		await get_tree().create_timer(1.0).timeout
		# L'ennemi attaque ensuite (c'est un tour)
		_controller.action_joueur = "item"
		_controller.item_utilise = item_id
		_controller.attaque_ennemi_index = AIController.choisir_attaque(_controller.pokemon_ennemi, _controller.pokemon_joueur)
		_controller._changer_etat(BattleController.Etat.EXECUTION)
	else:
		label_message.text = "Ça n'aura aucun effet !"
		await get_tree().create_timer(1.0).timeout
		_on_action_requise()

# --- Switch Pokémon en combat ---
func _ouvrir_switch_combat(forcer: bool) -> void:
	var switch_screen: Node = load("res://scripts/ui/battle_switch_screen.gd").new()
	switch_screen.index_actif = _controller.index_pokemon_joueur
	switch_screen.forcer_choix = forcer
	add_child(switch_screen)
	switch_screen.pokemon_choisi.connect(func(index: int):
		switch_screen.queue_free()
		# Sauvegarder l'état du Pokémon actuel
		PlayerData.equipe[_controller.index_pokemon_joueur] = _controller.pokemon_joueur.to_dict()
		_controller.joueur_change_pokemon(index)
		_charger_sprites_pokemon()
		_afficher_info_pokemon()
		if not forcer:
			# Switch volontaire = l'ennemi attaque ensuite via la machine à états
			_controller.action_joueur = "change"
			_controller.attaque_ennemi_index = AIController.choisir_attaque(_controller.pokemon_ennemi, _controller.pokemon_joueur)
			_controller._changer_etat(BattleController.Etat.EXECUTION)
	)
	switch_screen.ecran_ferme.connect(func():
		switch_screen.queue_free()
		if forcer:
			# Obligé de choisir, pas d'annulation
			_ouvrir_switch_combat(true)
		else:
			_on_action_requise()
	)

func _maj_curseur_action() -> void:
	var labels := menu_action.get_children()
	var noms := ["Attaque", "Sac", "Pokémon", "Fuite"]
	for i in range(labels.size()):
		if i < noms.size():
			labels[i].text = ("▶ " if i == _index_action else "  ") + noms[i]

func _maj_menu_attaque() -> void:
	var labels := menu_attaque.get_children()
	var attaques: Array = _controller.pokemon_joueur.attaques
	for i in range(labels.size()):
		if i < attaques.size():
			var md := MoveData.get_move(attaques[i]["id"])
			var type_atk: String = md.get("type", "normal").to_upper().left(3)
			labels[i].text = "%s  %s  %d/%d" % [md.get("nom", "???"), type_atk, attaques[i]["pp_actuels"], attaques[i]["pp_max"]]
			labels[i].visible = true
		else:
			labels[i].visible = false

func _maj_curseur_attaque() -> void:
	var labels := menu_attaque.get_children()
	var attaques: Array = _controller.pokemon_joueur.attaques
	for i in range(labels.size()):
		if i < attaques.size():
			var md := MoveData.get_move(attaques[i]["id"])
			var type_atk: String = md.get("type", "normal").to_upper().left(3)
			var prefix := "▶ " if i == _index_attaque else "  "
			labels[i].text = prefix + "%s  %s  %d/%d" % [md.get("nom", "???"), type_atk, attaques[i]["pp_actuels"], attaques[i]["pp_max"]]

func _abreger_statut(statut: String) -> String:
	match statut:
		"brulure": return "BRL"
		"gel": return "GEL"
		"paralysie": return "PAR"
		"poison", "poison_grave": return "PSN"
		"sommeil": return "SOM"
	return ""

# --- Gestion des évolutions ---
func _on_evolution_proposee(pokemon: Pokemon, vers_id: String) -> void:
	var evo_screen: Node = load("res://scripts/ui/evolution_screen.gd").new()
	evo_screen.pokemon = pokemon
	evo_screen.vers_id = vers_id
	add_child(evo_screen)
	evo_screen.evolution_terminee.connect(func(accepte: bool):
		_controller.confirmer_evolution(accepte)
		# Recharger le sprite si évolué
		if accepte:
			_charger_sprites_pokemon()
			_afficher_info_pokemon()
	)

# --- Gestion de l'apprentissage d'attaques ---
func _on_attaque_a_apprendre(pokemon: Pokemon, move_id: String) -> void:
	var learn_screen: Node = load("res://scripts/ui/move_learn_screen.gd").new()
	learn_screen.pokemon = pokemon
	learn_screen.move_id = move_id
	add_child(learn_screen)
	learn_screen.choix_fait.connect(func(index_remplacement: int):
		_controller.confirmer_apprentissage(index_remplacement)
	)

# === SYSTÈME SPRITES DRESSEURS ===

# Charger le fichier JSON de mapping classe → sprite
func _charger_trainer_sprites_data() -> void:
	var chemin := "res://data/trainer_sprites.json"
	if not FileAccess.file_exists(chemin):
		return
	var file := FileAccess.open(chemin, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) == OK:
		_trainer_sprites_data = json.data

func _get_trainer_sprite_name() -> String:
	# Vérifier d'abord le mapping par carte (arène / ligue)
	var arene_map: Dictionary = _trainer_sprites_data.get("_arene_mapping", {})
	var ligue_map: Dictionary = _trainer_sprites_data.get("_ligue_mapping", {})
	if _carte_retour in arene_map:
		return arene_map[_carte_retour]
	if _carte_retour in ligue_map:
		return ligue_map[_carte_retour]
	# Sinon, utiliser la classe du dresseur
	var classe: String = _dresseur_data.get("classe", "")
	if classe in _trainer_sprites_data:
		return _trainer_sprites_data[classe]
	# Fallback par défaut
	return ""

# Afficher le sprite du dresseur ennemi (pendant l'intro)
func _afficher_sprite_trainer() -> void:
	var sprite_name := _get_trainer_sprite_name()
	if sprite_name.is_empty():
		return
	var chemin := "res://assets/sprites/trainers/%s.png" % sprite_name
	var tex := load(chemin) as Texture2D
	if tex:
		sprite_trainer_ennemi.texture = tex
		sprite_trainer_ennemi.scale = Vector2(2.5, 2.5)
		sprite_trainer_ennemi.visible = true
		sprite_ennemi.visible = false

# Transition : cacher le sprite dresseur, afficher le sprite Pokémon ennemi
func _transition_trainer_vers_pokemon() -> void:
	if sprite_trainer_ennemi.visible:
		sprite_trainer_ennemi.visible = false
	sprite_ennemi.visible = true

# === SYSTÈME AUDIO DE COMBAT ===

# Détermine et lance la musique de combat appropriée
func _jouer_musique_combat() -> void:
	var chemin_musique: String = ""
	match _type_combat:
		"sauvage":
			chemin_musique = "res://assets/audio/music/combat_sauvage.ogg"
		"dresseur":
			# Vérifier si c'est un champion d'arène, le conseil 4, ou le champion
			var classe: String = _dresseur_data.get("classe", "")
			if classe in ["Champion d'Arène", "Champion d'arène"]:
				chemin_musique = "res://assets/audio/music/combat_champion_arene.ogg"
			elif classe in ["conseil_4", "Maître"]:
				chemin_musique = "res://assets/audio/music/combat_conseil4.ogg"
			elif classe in ["Champion", "champion_ligue"]:
				chemin_musique = "res://assets/audio/music/combat_champion.ogg"
			elif classe in ["Rival"]:
				chemin_musique = "res://assets/audio/music/combat_dresseur.ogg"
			else:
				chemin_musique = "res://assets/audio/music/combat_dresseur.ogg"
	
	if not chemin_musique.is_empty():
		AudioManager.jouer_musique(chemin_musique)

# Joue le cri d'un Pokémon par son espece_id
func _jouer_cri_pokemon(espece_id: String) -> void:
	var cri_path := "res://assets/audio/sfx/cries/%s.mp3" % espece_id
	AudioManager.jouer_sfx(cri_path)

# Joue la musique de victoire adaptée au type de combat
func _jouer_musique_victoire() -> void:
	var chemin: String = ""
	match _type_combat:
		"sauvage":
			chemin = "res://assets/audio/music/victoire_sauvage.ogg"
		"dresseur":
			var classe: String = _dresseur_data.get("classe", "")
			if classe in ["Champion d'Arène", "Champion d'arène"]:
				chemin = "res://assets/audio/music/victoire_champion_arene.ogg"
			else:
				chemin = "res://assets/audio/music/victoire_dresseur.ogg"
	if not chemin.is_empty():
		AudioManager.jouer_musique(chemin, false)

# =============================================================================
# ANIMATIONS DE COMBAT
# =============================================================================

# Couleurs associées aux types pour le flash d'attaque
const TYPE_COULEURS := {
	"normal": Color(0.66, 0.66, 0.56),
	"feu": Color(0.93, 0.51, 0.19),
	"eau": Color(0.39, 0.56, 0.94),
	"electrik": Color(0.97, 0.82, 0.17),
	"plante": Color(0.48, 0.78, 0.30),
	"glace": Color(0.59, 0.85, 0.84),
	"combat": Color(0.76, 0.18, 0.16),
	"poison": Color(0.64, 0.24, 0.63),
	"sol": Color(0.88, 0.75, 0.40),
	"vol": Color(0.66, 0.56, 0.95),
	"psy": Color(0.98, 0.33, 0.53),
	"insecte": Color(0.65, 0.72, 0.10),
	"roche": Color(0.72, 0.63, 0.21),
	"spectre": Color(0.45, 0.34, 0.59),
	"dragon": Color(0.44, 0.21, 0.98),
}

# Animation d'entrée en combat : les sprites glissent depuis les bords
func _animer_entree_combat() -> void:
	if not sprite_joueur or not sprite_ennemi:
		return
	# Positionner le sprite joueur hors écran à gauche
	sprite_joueur.position = Vector2(_pos_joueur_base.x - 300, _pos_joueur_base.y)
	sprite_joueur.modulate.a = 0.0
	sprite_joueur.visible = true
	# Positionner le sprite ennemi hors écran à droite
	sprite_ennemi.position = Vector2(_pos_ennemi_base.x + 300, _pos_ennemi_base.y)
	sprite_ennemi.modulate.a = 0.0
	sprite_ennemi.visible = true
	# Animer le slide-in du joueur
	var tween_joueur := create_tween().set_parallel(true)
	tween_joueur.tween_property(sprite_joueur, "position", _pos_joueur_base, 0.6)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	tween_joueur.tween_property(sprite_joueur, "modulate:a", 1.0, 0.4)
	# Animer le slide-in de l'ennemi avec un léger décalage
	await get_tree().create_timer(0.15).timeout
	var tween_ennemi := create_tween().set_parallel(true)
	tween_ennemi.tween_property(sprite_ennemi, "position", _pos_ennemi_base, 0.6)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	tween_ennemi.tween_property(sprite_ennemi, "modulate:a", 1.0, 0.4)
	# Attendre que les deux animations soient terminées
	await tween_ennemi.finished

# Callback quand une attaque est jouée — animer l'attaquant et le défenseur
func _on_animation_attaque(attaquant_joueur: bool, attaque_id: String) -> void:
	# Récupérer le type de l'attaque pour la couleur du flash
	var move_data := MoveData.get_move(attaque_id) if attaque_id else {}
	var type_attaque: String = move_data.get("type", "normal")
	var couleur_flash: Color = TYPE_COULEURS.get(type_attaque, Color.WHITE)
	
	if attaquant_joueur:
		# Le sprite joueur avance légèrement, puis le sprite ennemi flashe
		await _secouer_sprite(sprite_joueur, Vector2(16, -4))
		await _flash_sprite(sprite_ennemi, couleur_flash)
	else:
		# Le sprite ennemi avance, puis le sprite joueur flashe
		await _secouer_sprite(sprite_ennemi, Vector2(-16, 4))
		await _flash_sprite(sprite_joueur, couleur_flash)

# Secouer un sprite dans une direction puis le ramener à sa position
func _secouer_sprite(sprite: Sprite2D, decalage: Vector2) -> void:
	if not sprite or not is_instance_valid(sprite):
		return
	var pos_depart := sprite.position
	var tween := create_tween()
	# Aller vers la cible (avance rapide)
	tween.tween_property(sprite, "position", pos_depart + decalage, 0.08)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUAD)
	# Revenir à la position de départ
	tween.tween_property(sprite, "position", pos_depart, 0.12)\
		.set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_QUAD)
	await tween.finished

# Faire flasher un sprite dans une couleur (impact d'attaque)
func _flash_sprite(sprite: Sprite2D, couleur: Color) -> void:
	if not sprite or not is_instance_valid(sprite):
		return
	var couleur_originale := sprite.modulate
	var tween := create_tween()
	# Flash blanc puis coloré puis retour
	tween.tween_property(sprite, "modulate", Color.WHITE * 2.0, 0.05)
	tween.tween_property(sprite, "modulate", couleur, 0.08)
	tween.tween_property(sprite, "modulate", Color.WHITE * 1.5, 0.05)
	tween.tween_property(sprite, "modulate", couleur_originale, 0.1)
	# Petit tremblement pendant le flash
	var pos_depart := sprite.position
	var shake_tween := create_tween()
	shake_tween.tween_property(sprite, "position", pos_depart + Vector2(-3, 0), 0.03)
	shake_tween.tween_property(sprite, "position", pos_depart + Vector2(3, 0), 0.03)
	shake_tween.tween_property(sprite, "position", pos_depart + Vector2(-2, 0), 0.03)
	shake_tween.tween_property(sprite, "position", pos_depart + Vector2(2, 0), 0.03)
	shake_tween.tween_property(sprite, "position", pos_depart, 0.03)
	await tween.finished

# Animation de KO : le sprite descend et disparaît
func _animer_ko(sprite: Sprite2D) -> void:
	if not sprite or not is_instance_valid(sprite):
		return
	var tween := create_tween().set_parallel(true)
	tween.tween_property(sprite, "position:y", sprite.position.y + 40, 0.5)\
		.set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_QUAD)
	tween.tween_property(sprite, "modulate:a", 0.0, 0.5)
	await tween.finished

# Animation d'apparition d'un Pokémon (switch ou nouveau)
func _animer_apparition(sprite: Sprite2D) -> void:
	if not sprite or not is_instance_valid(sprite):
		return
	# Réinitialiser la position (après un KO qui déplace le sprite vers le bas)
	if sprite == sprite_joueur:
		sprite.position = _pos_joueur_base
	else:
		sprite.position = _pos_ennemi_base
	# Commencer petit et transparent
	sprite.scale = Vector2(0.1, 0.1)
	sprite.modulate = Color(1, 1, 1, 0)
	sprite.visible = true
	var scale_finale: Vector2
	if sprite == sprite_joueur:
		scale_finale = Vector2(1.8, 1.8)
	else:
		scale_finale = Vector2(1.5, 1.5)
	var tween := create_tween().set_parallel(true)
	tween.tween_property(sprite, "scale", scale_finale, 0.4)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	tween.tween_property(sprite, "modulate:a", 1.0, 0.3)
	await tween.finished

# =============================================================================
# BARRE D'EXP ANIMÉE
# =============================================================================

# Mettre à jour la barre d'EXP (sans animation)
func _maj_barre_exp(pokemon: Pokemon) -> void:
	if not barre_exp or not pokemon:
		return
	var info := pokemon.get_exp_info()
	var exp_niv: int = info.get("exp_niv_actuel", 0)
	var exp_next: int = info.get("exp_niv_suivant", 1)
	var exp_act: int = info.get("exp_actuel", 0)
	var range_exp: int = maxi(exp_next - exp_niv, 1)
	barre_exp.max_value = range_exp
	barre_exp.value = exp_act - exp_niv
	# Couleur bleue pour EXP
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.3, 0.5, 1.0)
	style.set_corner_radius_all(2)
	barre_exp.add_theme_stylebox_override("fill", style)
	var bg_style := StyleBoxFlat.new()
	bg_style.bg_color = Color(0.15, 0.15, 0.2)
	bg_style.set_corner_radius_all(2)
	barre_exp.add_theme_stylebox_override("background", bg_style)

# Callback quand de l'EXP est gagné — animer la barre
func _on_exp_gagnee(pokemon: Pokemon, montant: int, exp_avant: int, exp_apres: int, niveaux: Array) -> void:
	if not barre_exp or not pokemon:
		return
	# Animer le remplissage de la barre d'EXP
	# Si des niveaux sont gagnés, on remplit la barre par étapes
	if niveaux.is_empty():
		# Pas de level-up : simple tween de remplissage
		var info := pokemon.get_exp_info()
		var exp_niv: int = info.get("exp_niv_actuel", 0)
		var exp_next: int = info.get("exp_niv_suivant", 1)
		var range_exp: int = maxi(exp_next - exp_niv, 1)
		barre_exp.max_value = range_exp
		if _tween_exp:
			_tween_exp.kill()
		_tween_exp = create_tween()
		_tween_exp.tween_property(barre_exp, "value", float(exp_apres - exp_niv), 0.8)\
			.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUAD)
	else:
		# Level-up : remplir la barre → reset → remplir par étape
		await _animer_exp_level_up(pokemon)

# Animation d'EXP avec level-up : remplir → flash → reset
func _animer_exp_level_up(pokemon: Pokemon) -> void:
	# Remplir la barre complètement
	if _tween_exp:
		_tween_exp.kill()
	_tween_exp = create_tween()
	_tween_exp.tween_property(barre_exp, "value", barre_exp.max_value, 0.4)\
		.set_ease(Tween.EASE_OUT)
	await _tween_exp.finished
	await get_tree().create_timer(0.2).timeout
	# Mettre à jour pour le nouveau niveau
	_maj_barre_exp(pokemon)

# =============================================================================
# INDICATEUR DE CAPTURE
# =============================================================================

# Afficher la difficulté de capture pour les combats sauvages
func _maj_indicateur_capture(pokemon_ennemi_ref: Pokemon) -> void:
	if not label_capture:
		return
	# N'afficher que pour les combats sauvages et si le joueur a un Pokédex
	if _type_combat != "sauvage" or not GameManager.get_flag("pokedex_recu"):
		label_capture.text = ""
		label_capture.visible = false
		return
	# Vérifier si le joueur a déjà capturé cette espèce
	if PlayerData.a_capture(pokemon_ennemi_ref.espece_id):
		label_capture.text = "●"
		label_capture.add_theme_color_override("font_color", Color(0.3, 0.8, 0.3))
		label_capture.visible = true
		return
	# Afficher les étoiles de difficulté basées sur le taux de capture
	var taux := BattleCalculator.get_taux_capture(pokemon_ennemi_ref.espece_id)
	var etoiles := ""
	var couleur := Color.WHITE
	if taux >= 200:
		etoiles = "★★★★★"
		couleur = Color(0.3, 0.9, 0.3)  # Vert — très facile
	elif taux >= 150:
		etoiles = "★★★★☆"
		couleur = Color(0.5, 0.8, 0.3)  # Vert clair
	elif taux >= 100:
		etoiles = "★★★☆☆"
		couleur = Color(0.9, 0.8, 0.2)  # Jaune — moyen
	elif taux >= 45:
		etoiles = "★★☆☆☆"
		couleur = Color(0.9, 0.5, 0.2)  # Orange — difficile
	elif taux >= 3:
		etoiles = "★☆☆☆☆"
		couleur = Color(0.9, 0.2, 0.2)  # Rouge — très difficile
	else:
		etoiles = "☆☆☆☆☆"
		couleur = Color(0.6, 0.1, 0.1)  # Rouge foncé — quasi impossible
	label_capture.text = etoiles
	label_capture.add_theme_color_override("font_color", couleur)
	label_capture.visible = true

# =============================================================================
# ANIMATION DE CAPTURE (SECOUSSES DE BALL)
# =============================================================================

# Callback d'animation de capture : affiche les secousses de la Ball
func _on_animation_capture(nb_secousses: int, succes: bool) -> void:
	# Cacher le sprite ennemi quand la ball est lancée
	if sprite_ennemi:
		var tween_hide := create_tween()
		tween_hide.tween_property(sprite_ennemi, "modulate:a", 0.0, 0.3)
		await tween_hide.finished
	# Créer un sprite de Ball au centre
	var ball_sprite := Sprite2D.new()
	ball_sprite.position = _pos_ennemi_base
	# Utiliser un cercle coloré comme placeholder si pas de texture
	var ball_tex := load("res://assets/sprites/ui/pokeball_item.png") as Texture2D
	if ball_tex:
		ball_sprite.texture = ball_tex
		ball_sprite.scale = Vector2(1.5, 1.5)
	else:
		# Fallback : créer une représentation visuelle simple
		var placeholder := ColorRect.new()
		placeholder.color = Color(0.9, 0.2, 0.2)
		placeholder.size = Vector2(16, 16)
		placeholder.position = Vector2(-8, -8)
		ball_sprite.add_child(placeholder)
	add_child(ball_sprite)
	# Animer les secousses
	for i in range(nb_secousses):
		await _secouer_ball(ball_sprite)
		await get_tree().create_timer(0.2).timeout
	if succes:
		# Ball clique — petit flash blanc
		var flash := ColorRect.new()
		flash.color = Color(1, 1, 1, 0.4)
		flash.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(flash)
		await get_tree().create_timer(0.15).timeout
		flash.queue_free()
	else:
		# Ball s'ouvre — le Pokémon réapparaît
		ball_sprite.queue_free()
		if sprite_ennemi:
			sprite_ennemi.modulate.a = 1.0
			await _animer_apparition(sprite_ennemi)
		return
	ball_sprite.queue_free()

# Animation d'une secousse de Ball (gauche-droite)
func _secouer_ball(ball: Sprite2D) -> void:
	if not ball or not is_instance_valid(ball):
		return
	var pos_base := ball.position
	var tween := create_tween()
	tween.tween_property(ball, "position:x", pos_base.x - 8, 0.07)
	tween.tween_property(ball, "position:x", pos_base.x + 8, 0.14)
	tween.tween_property(ball, "position:x", pos_base.x - 4, 0.1)
	tween.tween_property(ball, "position:x", pos_base.x, 0.07)
	AudioManager.jouer_sfx(BattleController.SFX_BALL_SHAKE)
	await tween.finished
