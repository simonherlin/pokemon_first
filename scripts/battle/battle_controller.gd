extends Node

# BattleController — Contrôleur principal du combat Gen 1
# Machine à états : INTRO → CHOIX_ACTION → CHOIX_ATTAQUE → EXECUTION → VERIF_KO → TOUR_SUIVANT → FIN

# ----------------------------------------------------------------
# Énumérations et constantes
# ----------------------------------------------------------------
enum Etat {
	INTRO,
	CHOIX_ACTION,
	CHOIX_ATTAQUE,
	EXECUTION,
	VERIF_KO,
	FIN_TOUR,
	CAPTURE,
	FIN
}

enum TypeCombat {
	SAUVAGE,
	DRESSEUR
}

# ----------------------------------------------------------------
# Références aux systèmes
# ----------------------------------------------------------------
@onready var calculateur := BattleCalculator
@onready var effets := MoveEffects
@onready var ia := AIController

# Chemins SFX
const SFX_HIT := "res://assets/audio/sfx/hit_normal.ogg"
const SFX_SUPER := "res://assets/audio/sfx/hit_super_effective.ogg"
const SFX_RESIST := "res://assets/audio/sfx/hit_not_effective.ogg"
const SFX_MISS := "res://assets/audio/sfx/miss.ogg"
const SFX_CRITICAL := "res://assets/audio/sfx/critical.ogg"
const SFX_FAINT := "res://assets/audio/sfx/faint.ogg"
const SFX_EXP := "res://assets/audio/sfx/exp_gain.ogg"
const SFX_LEVEL_UP := "res://assets/audio/sfx/level_up.ogg"
const SFX_BALL_THROW := "res://assets/audio/sfx/ball_throw.ogg"
const SFX_BALL_SHAKE := "res://assets/audio/sfx/ball_shake.ogg"
const SFX_BALL_CLICK := "res://assets/audio/sfx/ball_click.ogg"
const SFX_FLEE := "res://assets/audio/sfx/flee.ogg"
const SFX_STAT_UP := "res://assets/audio/sfx/stat_up.ogg"
const SFX_STAT_DOWN := "res://assets/audio/sfx/stat_down.ogg"
const SFX_STATUS := "res://assets/audio/sfx/status_applied.ogg"

# ----------------------------------------------------------------
# État du combat
# ----------------------------------------------------------------
var etat_actuel: Etat = Etat.INTRO
var type_combat: TypeCombat = TypeCombat.SAUVAGE

# Pokémon actifs
var pokemon_joueur: Pokemon = null
var pokemon_ennemi: Pokemon = null

# Données dresseur ennemi (si TypeCombat.DRESSEUR)
var dresseur_ennemi: Dictionary = {}
var equipe_ennemi: Array = []
var index_pokemon_ennemi: int = 0
var index_pokemon_joueur: int = 0

# Index d'attaque choisis ce tour
var attaque_joueur_index: int = -1
var attaque_ennemi_index: int = -1

# Sauvegarde du choix d'action (pour l'UI)
var action_joueur: String = ""  # "attaque", "item", "change", "fuite"
var item_utilise: String = ""

# Compteur de tours
var tour: int = 0

# ----------------------------------------------------------------
# Signaux (l'UI s'y connecte)
# ----------------------------------------------------------------
signal message_affiche(texte: String)
signal action_requise()                         # Attendre l'input du joueur
signal attaque_requise()
signal animation_attaque(attaquant_joueur: bool, attaque_id: String)
signal pv_mis_a_jour(joueur: bool, pv_actuels: int, pv_max: int)
signal statut_mis_a_jour(joueur: bool, statut: String)
signal combat_termine(victoire: bool)
signal pokemon_change(joueur: bool)
signal capture_reussie(pokemon: Pokemon)
signal niveau_gagne(pokemon: Pokemon, nouveau_niveau: int)
signal evolution_proposee(pokemon: Pokemon, vers_id: String)
signal attaque_a_apprendre(pokemon: Pokemon, move_id: String)
signal attaque_apprise(pokemon: Pokemon, move_id: String)
signal exp_gagnee(pokemon: Pokemon, montant: int, exp_avant: int, exp_apres: int, niveaux: Array)
signal animation_capture(nb_secousses: int, succes: bool)

# --- État pour apprentissage d'attaque ---
var _attente_apprentissage: bool = false
var _move_en_attente: String = ""

# ----------------------------------------------------------------
# Démarrer un combat sauvage
# ----------------------------------------------------------------
func demarrer_sauvage(pokemon_du_joueur: Pokemon, espece_id: String, niveau: int, idx_joueur: int = 0) -> void:
	type_combat = TypeCombat.SAUVAGE
	pokemon_joueur = pokemon_du_joueur
	index_pokemon_joueur = idx_joueur
	pokemon_ennemi = SpeciesData.creer_sauvage(espece_id, niveau)
	if pokemon_ennemi == null:
		push_error("BattleController: impossible de créer le Pokémon sauvage '%s'" % espece_id)
		# Créer un Pokémon par défaut pour éviter le crash
		pokemon_ennemi = SpeciesData.creer_sauvage("001", niveau)
	if pokemon_ennemi == null:
		push_error("BattleController: impossible de créer un Pokémon, fin du combat.")
		emit_signal("combat_termine", false)
		return
	tour = 0
	etat_actuel = Etat.INTRO
	_changer_etat(Etat.INTRO)

# Démarrer un combat contre un dresseur
func demarrer_dresseur(pokemon_du_joueur: Pokemon, donnees_dresseur: Dictionary, idx_joueur: int = 0) -> void:
	type_combat = TypeCombat.DRESSEUR
	dresseur_ennemi = donnees_dresseur
	index_pokemon_joueur = idx_joueur
	equipe_ennemi = []
	for p_data in donnees_dresseur.get("equipe", []):
		var p := SpeciesData.creer_pokemon(p_data.get("espece_id", "001"), p_data.get("niveau", 5))
		if p:
			equipe_ennemi.append(p)
	index_pokemon_ennemi = 0
	pokemon_du_joueur_ref = pokemon_du_joueur
	if equipe_ennemi.is_empty():
		push_error("BattleController: l'équipe ennemie est vide, création d'un Pokémon par défaut.")
		var p_default := SpeciesData.creer_pokemon("001", 5)
		if p_default:
			equipe_ennemi.append(p_default)
		else:
			emit_signal("combat_termine", false)
			return
	pokemon_ennemi = equipe_ennemi[0]
	pokemon_joueur = pokemon_du_joueur
	tour = 0
	_changer_etat(Etat.INTRO)

var pokemon_du_joueur_ref: Pokemon = null

# ----------------------------------------------------------------
# Machine à états
# ----------------------------------------------------------------
var _traitement_etat_en_cours: bool = false

func _changer_etat(nouvel_etat: Etat) -> void:
	# Garde anti-réentrance : si un état est déjà en traitement, on diffère
	if _traitement_etat_en_cours:
		call_deferred("_changer_etat", nouvel_etat)
		return
	_traitement_etat_en_cours = true
	etat_actuel = nouvel_etat
	match etat_actuel:
		Etat.INTRO:
			await _phase_intro()
		Etat.CHOIX_ACTION:
			emit_signal("action_requise")
		Etat.CHOIX_ATTAQUE:
			emit_signal("attaque_requise")
		Etat.EXECUTION:
			await _executer_tour()
		Etat.VERIF_KO:
			await _verifier_ko()
		Etat.FIN_TOUR:
			await _fin_tour()
		Etat.FIN:
			pass
	_traitement_etat_en_cours = false

# ----------------------------------------------------------------
# Phase INTRO
# ----------------------------------------------------------------
func _phase_intro() -> void:
	if pokemon_ennemi == null:
		push_error("BattleController: pokemon_ennemi est null dans _phase_intro")
		emit_signal("combat_termine", false)
		return
	PlayerData.enregistrer_vu(pokemon_ennemi.espece_id)
	if type_combat == TypeCombat.SAUVAGE:
		var msg := "Un %s sauvage apparaît !" % pokemon_ennemi.surnom
		emit_signal("message_affiche", msg)
	else:
		var nom_dresseur: String = dresseur_ennemi.get("nom", "Dresseur")
		emit_signal("message_affiche", "%s veut se battre !" % nom_dresseur)
	emit_signal("pv_mis_a_jour", false, pokemon_ennemi.pv_actuels, pokemon_ennemi.pv_max)
	emit_signal("pv_mis_a_jour", true, pokemon_joueur.pv_actuels, pokemon_joueur.pv_max)
	await get_tree().create_timer(1.5).timeout
	_changer_etat(Etat.CHOIX_ACTION)

# ----------------------------------------------------------------
# Appel depuis l'UI : le joueur a choisi une action
# ----------------------------------------------------------------
func joueur_choisit_attaque(index: int) -> void:
	if etat_actuel != Etat.CHOIX_ACTION and etat_actuel != Etat.CHOIX_ATTAQUE:
		return
	if index < 0 or index >= pokemon_joueur.attaques.size():
		return
	if pokemon_joueur.attaques[index]["pp_actuels"] <= 0:
		emit_signal("message_affiche", "Il n'y a plus de PP !")
		return
	attaque_joueur_index = index
	action_joueur = "attaque"
	# L'IA choisit son attaque
	attaque_ennemi_index = AIController.choisir_attaque(pokemon_ennemi, pokemon_joueur)
	_changer_etat(Etat.EXECUTION)

func joueur_choisit_item(item_id: String) -> void:
	if etat_actuel != Etat.CHOIX_ACTION:
		return
	action_joueur = "item"
	item_utilise = item_id
	attaque_ennemi_index = AIController.choisir_attaque(pokemon_ennemi, pokemon_joueur)
	_changer_etat(Etat.EXECUTION)

func joueur_tente_fuite() -> void:
	if etat_actuel != Etat.CHOIX_ACTION:
		return
	if type_combat == TypeCombat.DRESSEUR:
		emit_signal("message_affiche", "Impossible de fuir un combat de Dresseur !")
		_changer_etat(Etat.CHOIX_ACTION)
		return
	# Formule de fuite Gen 1
	var vit_joueur := pokemon_joueur.get_stat_combat("vitesse")
	var vit_ennemi := pokemon_ennemi.get_stat_combat("vitesse")
	var taux_fuite := (vit_joueur * 128 / maxi(1, vit_ennemi) + 30 * tour) % 256
	if taux_fuite >= 256 or randf() * 256 < taux_fuite:
		AudioManager.jouer_sfx(SFX_FLEE)
		emit_signal("message_affiche", "Tu prends la fuite !")
		_changer_etat(Etat.FIN)
		emit_signal("combat_termine", false)
	else:
		emit_signal("message_affiche", "Impossible de fuir !")
		attaque_ennemi_index = AIController.choisir_attaque(pokemon_ennemi, pokemon_joueur)
		action_joueur = "fuite_echouee"
		_changer_etat(Etat.EXECUTION)

func joueur_tente_capture(ball_id: String) -> void:
	if etat_actuel != Etat.CHOIX_ACTION:
		return
	if type_combat == TypeCombat.DRESSEUR:
		emit_signal("message_affiche", "Tu ne peux pas capturer le Pokémon d'un dresseur !")
		_changer_etat(Etat.CHOIX_ACTION)
		return
	if not PlayerData.retirer_item(ball_id):
		emit_signal("message_affiche", "Tu n'as plus de %s !" % ball_id)
		_changer_etat(Etat.CHOIX_ACTION)
		return
	var items_data := ItemsData.get_item(ball_id)
	var multi: float = 1.0
	if not items_data.is_empty():
		multi = items_data.get("effet", {}).get("multiplicateur", 1.0)
	_changer_etat(Etat.CAPTURE)
	_resoudre_capture(multi)

func _resoudre_capture(ball_mult: float) -> void:
	AudioManager.jouer_sfx(SFX_BALL_THROW)
	emit_signal("message_affiche", "Tu lances la Ball...")
	await get_tree().create_timer(1.0).timeout
	var resultat := BattleCalculator.calculer_capture(pokemon_ennemi, ball_mult)
	var nb_secousses: int = resultat.get("nb_secousses", 0)
	var succes: bool = resultat.get("succes", false)
	# Émettre le signal d'animation de capture avec les secousses
	emit_signal("animation_capture", nb_secousses, succes)
	# Attendre l'animation des secousses
	await get_tree().create_timer(0.6 * nb_secousses + 0.5).timeout
	if succes:
		AudioManager.jouer_sfx(SFX_BALL_CLICK)
		emit_signal("message_affiche", "Gotcha ! %s a été capturé !" % pokemon_ennemi.surnom)
		PlayerData.enregistrer_capture(pokemon_ennemi.espece_id)
		# Ajouter à l'équipe ou à la boîte
		var p_dict := pokemon_ennemi.to_dict()
		if not PlayerData.ajouter_pokemon(p_dict):
			# Équipe pleine → boîte
			PlayerData.boites[0].append(p_dict)
		emit_signal("capture_reussie", pokemon_ennemi)
		_changer_etat(Etat.FIN)
		emit_signal("combat_termine", true)
	else:
		AudioManager.jouer_sfx(SFX_BALL_SHAKE)
		emit_signal("message_affiche", "%s s'est échappé !" % pokemon_ennemi.surnom)
		# L'ennemi contre-attaque ce tour
		attaque_ennemi_index = AIController.choisir_attaque(pokemon_ennemi, pokemon_joueur)
		await get_tree().create_timer(0.5).timeout
		await _pokemon_attaque(pokemon_ennemi, pokemon_joueur, attaque_ennemi_index, false)
		_changer_etat(Etat.VERIF_KO)

# ----------------------------------------------------------------
# Phase EXECUTION : résoudre les deux attaques
# ----------------------------------------------------------------
func _executer_tour() -> void:
	tour += 1

	# Résoudre l'item si le joueur en a utilisé un
	if action_joueur == "item":
		await _resoudre_item(item_utilise)
		# Puis l'ennemi attaque
		if attaque_ennemi_index >= 0:
			await _pokemon_attaque(pokemon_ennemi, pokemon_joueur, attaque_ennemi_index, false)
		_changer_etat(Etat.VERIF_KO)
		return

	if action_joueur == "fuite_echouee":
		if attaque_ennemi_index >= 0:
			await _pokemon_attaque(pokemon_ennemi, pokemon_joueur, attaque_ennemi_index, false)
		_changer_etat(Etat.VERIF_KO)
		return

	# Déterminer l'ordre (vitesse, Gen 1)
	var joueur_en_premier := _priorite_joueur_en_premier()

	if joueur_en_premier:
		# Vérifier statut joueur avant action
		var msg_statut := MoveEffects.verifier_statut_avant_action(pokemon_joueur)
		if not msg_statut.is_empty():
			emit_signal("message_affiche", msg_statut)
			await get_tree().create_timer(1.0).timeout
			# Si statut bloquant → passer l'attaque joueur
			if pokemon_joueur.statut in ["gel", "sommeil"] or (pokemon_joueur.statut == "paralysie" and "ne peut pas" in msg_statut):
				pass
			else:
				await _pokemon_attaque(pokemon_joueur, pokemon_ennemi, attaque_joueur_index, true)
		else:
			await _pokemon_attaque(pokemon_joueur, pokemon_ennemi, attaque_joueur_index, true)

		if pokemon_ennemi.est_ko():
			_changer_etat(Etat.VERIF_KO)
			return

		# Ennemi attaque
		var msg_statut_ennemi := MoveEffects.verifier_statut_avant_action(pokemon_ennemi)
		if not msg_statut_ennemi.is_empty():
			emit_signal("message_affiche", msg_statut_ennemi)
			await get_tree().create_timer(1.0).timeout
			# Statut bloquant ennemi → pas d'attaque
			if not (pokemon_ennemi.statut in ["gel", "sommeil"] or (pokemon_ennemi.statut == "paralysie" and "ne peut pas" in msg_statut_ennemi)):
				if attaque_ennemi_index >= 0:
					await _pokemon_attaque(pokemon_ennemi, pokemon_joueur, attaque_ennemi_index, false)
		else:
			if attaque_ennemi_index >= 0:
				await _pokemon_attaque(pokemon_ennemi, pokemon_joueur, attaque_ennemi_index, false)
	else:
		# Ennemi en premier
		var msg_statut_ennemi := MoveEffects.verifier_statut_avant_action(pokemon_ennemi)
		if not msg_statut_ennemi.is_empty():
			emit_signal("message_affiche", msg_statut_ennemi)
			await get_tree().create_timer(1.0).timeout
			if not (pokemon_ennemi.statut in ["gel", "sommeil"] or (pokemon_ennemi.statut == "paralysie" and "ne peut pas" in msg_statut_ennemi)):
				if attaque_ennemi_index >= 0:
					await _pokemon_attaque(pokemon_ennemi, pokemon_joueur, attaque_ennemi_index, false)
		else:
			if attaque_ennemi_index >= 0:
				await _pokemon_attaque(pokemon_ennemi, pokemon_joueur, attaque_ennemi_index, false)

		if pokemon_joueur.est_ko():
			_changer_etat(Etat.VERIF_KO)
			return

		var msg_statut := MoveEffects.verifier_statut_avant_action(pokemon_joueur)
		if not msg_statut.is_empty():
			emit_signal("message_affiche", msg_statut)
			await get_tree().create_timer(1.0).timeout
			if not (pokemon_joueur.statut in ["gel", "sommeil"] or (pokemon_joueur.statut == "paralysie" and "ne peut pas" in msg_statut)):
				await _pokemon_attaque(pokemon_joueur, pokemon_ennemi, attaque_joueur_index, true)
		else:
			await _pokemon_attaque(pokemon_joueur, pokemon_ennemi, attaque_joueur_index, true)

	_changer_etat(Etat.VERIF_KO)

# Déterminer qui attaque en premier (vitesse + priorité de l'attaque)
func _priorite_joueur_en_premier() -> bool:
	# Vérifier priorité des attaques (ex: Vive-Attaque = priorité +1)
	var attaque_joueur_data := MoveData.get_move(pokemon_joueur.attaques[attaque_joueur_index]["id"]) if attaque_joueur_index >= 0 else {}
	var attaque_ennemi_data := MoveData.get_move(pokemon_ennemi.attaques[attaque_ennemi_index]["id"]) if attaque_ennemi_index >= 0 else {}

	var priorite_j: int = attaque_joueur_data.get("priorite", 0)
	var priorite_e: int = attaque_ennemi_data.get("priorite", 0)

	if priorite_j != priorite_e:
		return priorite_j > priorite_e

	var vit_j := pokemon_joueur.get_stat_combat("vitesse")
	var vit_e := pokemon_ennemi.get_stat_combat("vitesse")
	if vit_j == vit_e:
		return randf() < 0.5
	return vit_j > vit_e

# Résoudre une attaque
func _pokemon_attaque(attaquant: Pokemon, defenseur: Pokemon, index_attaque: int, joueur_attaque: bool) -> void:
	if index_attaque < 0 or index_attaque >= attaquant.attaques.size():
		return
	var attaque_ref: Dictionary = attaquant.attaques[index_attaque]
	var attaque_data: Dictionary = MoveData.get_move(attaque_ref["id"])
	if attaque_data.is_empty():
		return

	attaquant.utiliser_pp(index_attaque)
	emit_signal("message_affiche", "%s utilise %s !" % [attaquant.surnom, attaque_data.get("nom", "???")])
	await get_tree().create_timer(0.8).timeout
	emit_signal("animation_attaque", joueur_attaque, attaque_ref["id"])

	# Vérifier précision
	if not BattleCalculator.attaque_touche(attaquant, defenseur, attaque_data):
		AudioManager.jouer_sfx(SFX_MISS)
		emit_signal("message_affiche", "L'attaque a raté !")
		await get_tree().create_timer(0.8).timeout
		return

	# Calculer dégâts
	var degats := BattleCalculator.calculer_degats(attaquant, defenseur, attaque_data)
	if degats > 0:
		defenseur.infliger_degats(degats)
		# SFX selon l'efficacité
		var type_mult := BattleCalculator.get_efficacite(attaque_data.get("type", "normal"), defenseur.types)
		if type_mult > 1.0:
			AudioManager.jouer_sfx(SFX_SUPER)
		elif type_mult < 1.0 and type_mult > 0.0:
			AudioManager.jouer_sfx(SFX_RESIST)
		else:
			AudioManager.jouer_sfx(SFX_HIT)
		emit_signal("pv_mis_a_jour", not joueur_attaque, defenseur.pv_actuels, defenseur.pv_max)
		await get_tree().create_timer(0.5).timeout
		# Message d'efficacité
		var msg_eff := BattleCalculator.message_efficacite(type_mult)
		if not msg_eff.is_empty():
			emit_signal("message_affiche", msg_eff)
			await get_tree().create_timer(0.8).timeout

	# Appliquer effets secondaires
	var resultat_effet := MoveEffects.appliquer_effet(attaquant, defenseur, attaque_data)
	if not resultat_effet["message"].is_empty():
		# SFX selon le type d'effet
		if not resultat_effet["statut_applique"].is_empty():
			AudioManager.jouer_sfx(SFX_STATUS)
		emit_signal("message_affiche", resultat_effet["message"])
		await get_tree().create_timer(0.8).timeout
	if not resultat_effet["statut_applique"].is_empty():
		emit_signal("statut_mis_a_jour", not joueur_attaque, defenseur.statut)

# Résoudre l'utilisation d'un item
func _resoudre_item(item_id: String) -> void:
	emit_signal("message_affiche", "Tu utilises %s..." % item_id)
	await get_tree().create_timer(0.5).timeout
	# La logique d'application est dans l'UI, ici on émet juste le message
	# L'item a déjà été consommé dans le menu

# ----------------------------------------------------------------
# Phase VERIF_KO
# ----------------------------------------------------------------
func _verifier_ko() -> void:
	if pokemon_joueur.est_ko():
		AudioManager.jouer_sfx(SFX_FAINT)
		emit_signal("message_affiche", "%s est mis KO !" % pokemon_joueur.surnom)
		await get_tree().create_timer(1.0).timeout
		# Chercher un remplaçant dans l'équipe
		var remplacant_index := _trouver_remplacant_joueur()
		if remplacant_index < 0:
			emit_signal("message_affiche", "Tous tes Pokémon sont KO ! Tu te fais soigner...")
			await get_tree().create_timer(1.0).timeout
			_changer_etat(Etat.FIN)
			emit_signal("combat_termine", false)
			return
		else:
			# L'UI doit afficher la sélection de Pokémon
			emit_signal("pokemon_change", true)
			return

	if pokemon_ennemi.est_ko():
		AudioManager.jouer_sfx(SFX_FAINT)
		emit_signal("message_affiche", "%s est mis KO !" % pokemon_ennemi.surnom)
		await get_tree().create_timer(1.0).timeout
		# Distribuer l'EXP
		await _distribuer_exp()
		# Combat dresseur : chercher un remplaçant ennemi
		if type_combat == TypeCombat.DRESSEUR:
			index_pokemon_ennemi += 1
			if index_pokemon_ennemi < equipe_ennemi.size():
				pokemon_ennemi = equipe_ennemi[index_pokemon_ennemi]
				emit_signal("message_affiche", "%s envoie %s !" % [dresseur_ennemi.get("nom", "Dresseur"), pokemon_ennemi.surnom])
				emit_signal("pokemon_change", false)
				await get_tree().create_timer(1.0).timeout
				_changer_etat(Etat.CHOIX_ACTION)
				return
			else:
				# Dresseur battu
				var argent: int = dresseur_ennemi.get("recompense", 0)
				PlayerData.ajouter_argent(argent)
				PlayerData.marquer_dresseur_battu(dresseur_ennemi.get("id", ""))
				emit_signal("message_affiche", "%s est battu ! Tu gagnes %d ₽ !" % [dresseur_ennemi.get("nom", "Dresseur"), argent])
				await get_tree().create_timer(1.0).timeout
				_changer_etat(Etat.FIN)
				emit_signal("combat_termine", true)
				return
		else:
			# Pokémon sauvage KO
			_changer_etat(Etat.FIN)
			emit_signal("combat_termine", true)
			return

	# Personne KO → fin de tour
	_changer_etat(Etat.FIN_TOUR)

# ----------------------------------------------------------------
# Phase FIN_TOUR : dégâts de statut
# ----------------------------------------------------------------
func _fin_tour() -> void:
	var msg_j := MoveEffects.appliquer_degats_fin_tour(pokemon_joueur)
	if not msg_j.is_empty():
		emit_signal("message_affiche", msg_j)
		emit_signal("pv_mis_a_jour", true, pokemon_joueur.pv_actuels, pokemon_joueur.pv_max)
		await get_tree().create_timer(0.8).timeout
		if pokemon_joueur.est_ko():
			_changer_etat(Etat.VERIF_KO)
			return

	var msg_e := MoveEffects.appliquer_degats_fin_tour(pokemon_ennemi)
	if not msg_e.is_empty():
		emit_signal("message_affiche", msg_e)
		emit_signal("pv_mis_a_jour", false, pokemon_ennemi.pv_actuels, pokemon_ennemi.pv_max)
		await get_tree().create_timer(0.8).timeout
		if pokemon_ennemi.est_ko():
			_changer_etat(Etat.VERIF_KO)
			return

	_changer_etat(Etat.CHOIX_ACTION)

# ----------------------------------------------------------------
# Distribution d'EXP
# ----------------------------------------------------------------
func _distribuer_exp() -> void:
	var exp := BattleCalculator.calculer_exp_gagne(pokemon_ennemi, type_combat == TypeCombat.SAUVAGE)
	AudioManager.jouer_sfx(SFX_EXP)
	emit_signal("message_affiche", "%s gagne %d points d'Expérience !" % [pokemon_joueur.surnom, exp])
	var exp_avant := pokemon_joueur.exp
	await get_tree().create_timer(0.8).timeout
	var niveaux := pokemon_joueur.gagner_exp(exp)
	var exp_apres := pokemon_joueur.exp
	# Émettre le signal pour animer la barre d'EXP
	emit_signal("exp_gagnee", pokemon_joueur, exp, exp_avant, exp_apres, niveaux)
	for niv in niveaux:
		AudioManager.jouer_sfx(SFX_LEVEL_UP)
		emit_signal("message_affiche", "%s monte au niveau %d !" % [pokemon_joueur.surnom, niv])
		emit_signal("niveau_gagne", pokemon_joueur, niv)
		emit_signal("pv_mis_a_jour", true, pokemon_joueur.pv_actuels, pokemon_joueur.pv_max)
		await get_tree().create_timer(1.0).timeout
		# Vérifier attaques à apprendre
		var espece_data := SpeciesData.get_espece(pokemon_joueur.espece_id)
		var nouvelles_attaques := pokemon_joueur.attaques_a_apprendre(espece_data)
		for move_id in nouvelles_attaques:
			# Vérifier si déjà connue
			var deja_connue := false
			for a in pokemon_joueur.attaques:
				if a.get("id", "") == move_id:
					deja_connue = true
					break
			if deja_connue:
				continue
			var move_data := MoveData.get_move(move_id)
			var move_nom: String = move_data.get("nom", move_id) if move_data else move_id
			if pokemon_joueur.attaques.size() < Pokemon.MAX_ATTAQUES:
				# Place libre — apprentissage automatique
				pokemon_joueur.apprendre_attaque(move_id)
				emit_signal("message_affiche", "%s apprend %s !" % [pokemon_joueur.surnom, move_nom])
				emit_signal("attaque_apprise", pokemon_joueur, move_id)
				await get_tree().create_timer(1.2).timeout
			else:
				# 4 attaques déjà — proposer le remplacement
				emit_signal("message_affiche", "%s veut apprendre %s, mais il connaît déjà 4 attaques." % [pokemon_joueur.surnom, move_nom])
				await get_tree().create_timer(1.5).timeout
				_attente_apprentissage = true
				_move_en_attente = move_id
				emit_signal("attaque_a_apprendre", pokemon_joueur, move_id)
				# Attendre que l'UI réponde via confirmer_apprentissage()
				while _attente_apprentissage:
					await get_tree().create_timer(0.1).timeout
		# Vérifier évolution
		var vers := SpeciesData.peut_evoluer_niveau(pokemon_joueur.espece_id, niv)
		if not vers.is_empty():
			emit_signal("evolution_proposee", pokemon_joueur, vers)
			# Attendre un peu pour l'UI d'évolution
			await get_tree().create_timer(0.5).timeout
	# Mettre à jour l'équipe du joueur
	PlayerData.equipe[index_pokemon_joueur] = pokemon_joueur.to_dict()

# Trouver un Pokémon vivant dans l'équipe du joueur
func _trouver_remplacant_joueur() -> int:
	for i in range(PlayerData.equipe.size()):
		if i == index_pokemon_joueur:
			continue
		var p_data: Dictionary = PlayerData.equipe[i]
		if p_data.get("pv_actuels", 0) > 0:
			return i
	return -1

# Appeler depuis l'UI après la sélection du Pokémon remplaçant
func joueur_change_pokemon(index_equipe: int) -> void:
	index_pokemon_joueur = index_equipe
	var p_data: Dictionary = PlayerData.equipe[index_equipe]
	pokemon_joueur = Pokemon.from_dict(p_data)
	emit_signal("pokemon_change", true)
	emit_signal("pv_mis_a_jour", true, pokemon_joueur.pv_actuels, pokemon_joueur.pv_max)
	emit_signal("message_affiche", "Vas-y, %s !" % pokemon_joueur.surnom)
	_changer_etat(Etat.CHOIX_ACTION)

# --- Gestion apprentissage d'attaque ---
# Appeler depuis l'UI : index_remplacement = 0-3 pour remplacer, -1 pour abandonner
func confirmer_apprentissage(index_remplacement: int) -> void:
	if not _attente_apprentissage:
		return
	if index_remplacement >= 0 and index_remplacement < Pokemon.MAX_ATTAQUES:
		var move_data := MoveData.get_move(_move_en_attente)
		var move_nom: String = move_data.get("nom", _move_en_attente) if move_data else _move_en_attente
		var ancienne: Dictionary = pokemon_joueur.attaques[index_remplacement]
		var anc_data: Dictionary = MoveData.get_move(ancienne.get("id", ""))
		var anc_nom: String = anc_data.get("nom", "???") if anc_data else "???"
		pokemon_joueur.apprendre_attaque(_move_en_attente, index_remplacement)
		emit_signal("message_affiche", "1, 2, 3 et... Hop !\n%s oublie %s et apprend %s !" % [pokemon_joueur.surnom, anc_nom, move_nom])
	else:
		var move_data := MoveData.get_move(_move_en_attente)
		var move_nom: String = move_data.get("nom", _move_en_attente) if move_data else _move_en_attente
		emit_signal("message_affiche", "%s n'apprend pas %s." % [pokemon_joueur.surnom, move_nom])
	_move_en_attente = ""
	_attente_apprentissage = false

# --- Gestion évolution ---
# Appeler depuis l'UI après confirmation d'évolution
func confirmer_evolution(accepte: bool) -> void:
	if not accepte:
		emit_signal("message_affiche", "%s n'évolue pas." % pokemon_joueur.surnom)
		return
	var vers := SpeciesData.peut_evoluer_niveau(pokemon_joueur.espece_id, pokemon_joueur.niveau)
	if vers.is_empty():
		return
	var ancien_nom := pokemon_joueur.surnom
	SpeciesData.evoluer(pokemon_joueur)
	emit_signal("message_affiche", "Félicitations ! %s évolue en %s !" % [ancien_nom, pokemon_joueur.surnom])
	emit_signal("pv_mis_a_jour", true, pokemon_joueur.pv_actuels, pokemon_joueur.pv_max)
	# Enregistrer dans le Pokédex
	PlayerData.enregistrer_vu(pokemon_joueur.espece_id)
	PlayerData.enregistrer_capture(pokemon_joueur.espece_id)
	# Mettre à jour l'équipe
	PlayerData.equipe[index_pokemon_joueur] = pokemon_joueur.to_dict()
