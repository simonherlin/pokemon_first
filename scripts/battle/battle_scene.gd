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

func _ready() -> void:
	menu_action.visible = false
	menu_attaque.visible = false
	# Charger le fond de combat
	var bg_texture := load("res://assets/sprites/ui/battle_bg.png") as Texture2D
	if bg_texture and background:
		background.color = Color(0.75, 0.85, 0.65, 1)
	# Charger le mapping des sprites de dresseurs
	_charger_trainer_sprites_data()

func recevoir_params(params: Dictionary) -> void:
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
	if PlayerData.equipe.is_empty():
		push_error("BattleScene: équipe du joueur vide !")
		return
	var pokemon_joueur := Pokemon.from_dict(PlayerData.equipe[pokemon_index])

	# Initialiser le BattleController
	_controller = BattleController
	_connecter_signaux()

	if _type_combat == "sauvage":
		var espece_id: String = params.get("espece_id", "019")
		var niveau: int = params.get("niveau", 5)
		_controller.demarrer_sauvage(pokemon_joueur, espece_id, niveau, pokemon_index)
	else:
		# Afficher le sprite du dresseur pendant l'intro
		_afficher_sprite_trainer()
		_controller.demarrer_dresseur(pokemon_joueur, _dresseur_data, pokemon_index)
	
	# Charger les sprites des Pokémon
	_charger_sprites_pokemon()
	
	# Si combat dresseur, montrer la transition trainer → Pokémon après un délai
	if _type_combat != "sauvage" and sprite_trainer_ennemi.visible:
		await get_tree().create_timer(1.8).timeout
		_transition_trainer_vers_pokemon()
		_charger_sprites_pokemon()
	
	# Jouer le cri du Pokémon ennemi à l'entrée en combat
	if _controller.pokemon_ennemi:
		_jouer_cri_pokemon(_controller.pokemon_ennemi.espece_id)

# Charger les textures front/back des Pokémon en combat
func _charger_sprites_pokemon() -> void:
	if not _controller:
		return
	# Sprite du joueur (dos)
	if _controller.pokemon_joueur:
		var back_path := "res://assets/sprites/pokemon/back/%s.png" % _controller.pokemon_joueur.espece_id
		var back_tex := load(back_path) as Texture2D
		if back_tex:
			sprite_joueur.texture = back_tex
			# Adapter l'échelle pour que ce soit visible (64×96 → agrandi ×2)
			sprite_joueur.scale = Vector2(2.0, 2.0)
	# Sprite de l'ennemi (face)
	if _controller.pokemon_ennemi:
		var front_path := "res://assets/sprites/pokemon/front/%s.png" % _controller.pokemon_ennemi.espece_id
		var front_tex := load(front_path) as Texture2D
		if front_tex:
			sprite_ennemi.texture = front_tex
			sprite_ennemi.scale = Vector2(1.5, 1.5)

func _connecter_signaux() -> void:
	if not _controller:
		return
	_controller.message_affiche.connect(_on_message)
	_controller.action_requise.connect(_on_action_requise)
	_controller.attaque_requise.connect(_on_attaque_requise)
	_controller.pv_mis_a_jour.connect(_on_pv_mis_a_jour)
	_controller.statut_mis_a_jour.connect(_on_statut_mis_a_jour)
	_controller.combat_termine.connect(_on_combat_termine)
	_controller.evolution_proposee.connect(_on_evolution_proposee)
	_controller.attaque_a_apprendre.connect(_on_attaque_a_apprendre)
	_controller.pokemon_change.connect(_on_pokemon_change)

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
	if joueur:
		barre_pv_joueur.max_value = pv_max
		barre_pv_joueur.value = pv
		label_pv_joueur.text = "%d/%d" % [pv, pv_max]
	else:
		barre_pv_ennemi.max_value = pv_max
		barre_pv_ennemi.value = pv

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
			_charger_sprites_pokemon()
			_afficher_info_pokemon()
			# Sauvegarder l'état du KO
			PlayerData.equipe[_controller.index_pokemon_joueur] = _controller.pokemon_joueur.to_dict()
			_ouvrir_switch_combat(true)
			return
		# Switch normal (joueur_change_pokemon déjà appelé)
		_charger_sprites_pokemon()
		_afficher_info_pokemon()
		_jouer_cri_pokemon(_controller.pokemon_joueur.espece_id)
	else:
		_charger_sprites_pokemon()
		_afficher_info_pokemon()
		if _controller.pokemon_ennemi:
			_jouer_cri_pokemon(_controller.pokemon_ennemi.espece_id)

func _on_combat_termine(victoire: bool) -> void:
	if _controller:
		_controller.message_affiche.disconnect(_on_message)
		_controller.action_requise.disconnect(_on_action_requise)
		_controller.attaque_requise.disconnect(_on_attaque_requise)
		_controller.pv_mis_a_jour.disconnect(_on_pv_mis_a_jour)
		_controller.statut_mis_a_jour.disconnect(_on_statut_mis_a_jour)
		_controller.combat_termine.disconnect(_on_combat_termine)
		if _controller.evolution_proposee.is_connected(_on_evolution_proposee):
			_controller.evolution_proposee.disconnect(_on_evolution_proposee)
		if _controller.attaque_a_apprendre.is_connected(_on_attaque_a_apprendre):
			_controller.attaque_a_apprendre.disconnect(_on_attaque_a_apprendre)
		if _controller.pokemon_change.is_connected(_on_pokemon_change):
			_controller.pokemon_change.disconnect(_on_pokemon_change)
	
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
		SceneManager.charger_scene("res://scenes/maps/map_scene.tscn", {
			"carte_id": "centre_pokemon_plateau",
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
		await get_tree().create_timer(2.0).timeout
		SceneManager.charger_scene("res://scenes/maps/map_scene.tscn", {
			"carte_id": dc.get("carte_id", "bourg_palette"),
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
	var pj := _controller.pokemon_joueur
	var pe := _controller.pokemon_ennemi
	if pj:
		label_nom_joueur.text = pj.surnom
		label_niveau_joueur.text = "N.%d" % pj.niveau
		barre_pv_joueur.max_value = pj.pv_max
		barre_pv_joueur.value = pj.pv_actuels
		label_pv_joueur.text = "%d/%d" % [pj.pv_actuels, pj.pv_max]
	if pe:
		label_nom_ennemi.text = pe.surnom
		label_niveau_ennemi.text = "N.%d" % pe.niveau
		barre_pv_ennemi.max_value = pe.pv_max
		barre_pv_ennemi.value = pe.pv_actuels

func _process(_delta: float) -> void:
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
		AudioManager.jouer_sfx(SFX_CONFIRM)
		_menu_actif = ""
		menu_action.visible = false
		_executer_action(_actions[_index_action])

func _gerer_input_attaque() -> void:
	if Input.is_action_just_pressed("action_haut"):
		_index_attaque = (_index_attaque - 1 + _nb_attaques) % _nb_attaques
		AudioManager.jouer_sfx(SFX_CURSOR)
		_maj_curseur_attaque()
	elif Input.is_action_just_pressed("action_bas"):
		_index_attaque = (_index_attaque + 1) % _nb_attaques
		AudioManager.jouer_sfx(SFX_CURSOR)
		_maj_curseur_attaque()
	elif Input.is_action_just_pressed("action_confirmer"):
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
	var bag_screen := load("res://scripts/ui/battle_bag_screen.gd").new()
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
	var switch_screen := load("res://scripts/ui/battle_switch_screen.gd").new()
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
			emit_signal("pv_mis_a_jour", true, _controller.pokemon_joueur.pv_actuels, _controller.pokemon_joueur.pv_max) if _controller.pv_mis_a_jour else null
			_controller.emit_signal("pv_mis_a_jour", true, _controller.pokemon_joueur.pv_actuels, _controller.pokemon_joueur.pv_max)
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
	var switch_screen := load("res://scripts/ui/battle_switch_screen.gd").new()
	switch_screen.index_actif = _controller.index_pokemon_joueur
	switch_screen.forcer_choix = forcer
	add_child(switch_screen)
	switch_screen.pokemon_choisi.connect(func(index: int):
		switch_screen.queue_free()
		# Sauvegarder l'état du Pokémon actuel
		PlayerData.equipe[_controller.index_pokemon_joueur] = _controller.pokemon_joueur.to_dict()
		_controller.joueur_change_pokemon(index)
		_charger_sprites_pokemon()
		if not forcer:
			# Switch volontaire = l'ennemi attaque
			_controller.action_joueur = "change"
			_controller.attaque_ennemi_index = AIController.choisir_attaque(_controller.pokemon_ennemi, _controller.pokemon_joueur)
			await get_tree().create_timer(0.5).timeout
			await _controller._pokemon_attaque(_controller.pokemon_ennemi, _controller.pokemon_joueur, _controller.attaque_ennemi_index, false)
			_controller._changer_etat(BattleController.Etat.VERIF_KO)
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
	var attaques := _controller.pokemon_joueur.attaques
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
	var attaques := _controller.pokemon_joueur.attaques
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
	var evo_screen := load("res://scripts/ui/evolution_screen.gd").new()
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
	var learn_screen := load("res://scripts/ui/move_learn_screen.gd").new()
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
			var classe := _dresseur_data.get("classe", "")
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
			var classe := _dresseur_data.get("classe", "")
			if classe in ["Champion d'Arène", "Champion d'arène"]:
				chemin = "res://assets/audio/music/victoire_champion_arene.ogg"
			else:
				chemin = "res://assets/audio/music/victoire_dresseur.ogg"
	if not chemin.is_empty():
		AudioManager.jouer_musique(chemin, false)
