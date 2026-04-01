# safari_battle.gd — Contrôleur de combat Safari (séparé du BattleController)
# Actions possibles : Safari Ball, Caillou, Appât, Fuite
# Pas de Pokémon du joueur impliqué — juste un Pokémon sauvage
extends Node

class_name SafariBattle

# --- Signaux (l'UI s'y connecte) ---
signal message_affiche(texte: String)
signal action_requise()
signal pv_mis_a_jour(pv_actuels: int, pv_max: int)
signal capture_reussie(pokemon: Pokemon)
signal pokemon_fuit()
signal combat_termine(capture: bool)

# --- Constantes SFX ---
const SFX_BALL_THROW := "res://assets/audio/sfx/ball_throw.ogg"
const SFX_BALL_SHAKE := "res://assets/audio/sfx/ball_shake.ogg"
const SFX_BALL_CLICK := "res://assets/audio/sfx/ball_click.ogg"
const SFX_ROCK := "res://assets/audio/sfx/hit_normal.ogg"
const SFX_BAIT := "res://assets/audio/sfx/stat_down.ogg"
const SFX_FLEE := "res://assets/audio/sfx/flee.ogg"

# --- État du combat ---
var pokemon_sauvage: Pokemon = null
var colere_compteur: int = 0    # Tours de colère restants (caillou)
var appat_compteur: int = 0     # Tours d'appât restants
var tour: int = 0
var safari_system: SafariSystem = null

# ----------------------------------------------------------------
# Démarrer le combat Safari
# ----------------------------------------------------------------
func demarrer(espece_id: String, niveau: int, safari_sys: SafariSystem) -> void:
	pokemon_sauvage = SpeciesData.creer_sauvage(espece_id, niveau)
	safari_system = safari_sys
	colere_compteur = 0
	appat_compteur = 0
	tour = 0

	PlayerData.enregistrer_vu(pokemon_sauvage.espece_id)
	emit_signal("message_affiche", "Un %s sauvage apparaît !" % pokemon_sauvage.surnom)
	emit_signal("pv_mis_a_jour", pokemon_sauvage.pv_actuels, pokemon_sauvage.pv_max)
	await get_tree().create_timer(1.5).timeout
	emit_signal("action_requise")

# ----------------------------------------------------------------
# Action : Lancer une Safari Ball
# ----------------------------------------------------------------
func lancer_safari_ball() -> void:
	tour += 1

	# Utiliser une ball du stock safari
	if safari_system and not safari_system.utiliser_ball():
		emit_signal("message_affiche", "Plus de Safari Balls !")
		await get_tree().create_timer(1.0).timeout
		_fin_combat(false)
		return

	AudioManager.jouer_sfx(SFX_BALL_THROW)
	emit_signal("message_affiche", "Tu lances une Safari Ball !")
	await get_tree().create_timer(1.0).timeout

	# Calcul de la capture
	var succes := SafariSystem.calculer_capture_safari(pokemon_sauvage, colere_compteur, appat_compteur)

	if succes:
		AudioManager.jouer_sfx(SFX_BALL_CLICK)
		emit_signal("message_affiche", "Gotcha ! %s a été capturé !" % pokemon_sauvage.surnom)
		PlayerData.enregistrer_capture(pokemon_sauvage.espece_id)
		var p_dict := pokemon_sauvage.to_dict()
		if not PlayerData.ajouter_pokemon(p_dict):
			PlayerData.boites[0].append(p_dict)
		emit_signal("capture_reussie", pokemon_sauvage)
		await get_tree().create_timer(1.5).timeout
		_fin_combat(true)
	else:
		AudioManager.jouer_sfx(SFX_BALL_SHAKE)
		emit_signal("message_affiche", "%s s'est échappé de la Ball !" % pokemon_sauvage.surnom)
		await get_tree().create_timer(1.0).timeout
		_tour_pokemon_sauvage()

# ----------------------------------------------------------------
# Action : Lancer un Caillou (augmente capture + fuite)
# ----------------------------------------------------------------
func lancer_caillou() -> void:
	tour += 1
	AudioManager.jouer_sfx(SFX_ROCK)
	emit_signal("message_affiche", "Tu lances un Caillou sur %s !" % pokemon_sauvage.surnom)
	await get_tree().create_timer(0.8).timeout

	# Le caillou met en colère : +capture, +fuite (1-5 tours de colère)
	colere_compteur = randi_range(1, 5)
	appat_compteur = 0  # Annule l'appât

	emit_signal("message_affiche", "%s est en colère !" % pokemon_sauvage.surnom)
	await get_tree().create_timer(0.8).timeout
	_tour_pokemon_sauvage()

# ----------------------------------------------------------------
# Action : Lancer de l'Appât (diminue fuite + capture)
# ----------------------------------------------------------------
func lancer_appat() -> void:
	tour += 1
	AudioManager.jouer_sfx(SFX_BAIT)
	emit_signal("message_affiche", "Tu lances de l'Appât à %s !" % pokemon_sauvage.surnom)
	await get_tree().create_timer(0.8).timeout

	# L'appât attire : -fuite, -capture (1-5 tours d'appât)
	appat_compteur = randi_range(1, 5)
	colere_compteur = 0  # Annule la colère

	emit_signal("message_affiche", "%s observe l'Appât..." % pokemon_sauvage.surnom)
	await get_tree().create_timer(0.8).timeout
	_tour_pokemon_sauvage()

# ----------------------------------------------------------------
# Action : Fuir
# ----------------------------------------------------------------
func fuir() -> void:
	AudioManager.jouer_sfx(SFX_FLEE)
	emit_signal("message_affiche", "Tu prends la fuite !")
	await get_tree().create_timer(1.0).timeout
	_fin_combat(false)

# ----------------------------------------------------------------
# Tour du Pokémon sauvage
# ----------------------------------------------------------------
func _tour_pokemon_sauvage() -> void:
	# Décrémenter les compteurs
	if colere_compteur > 0:
		colere_compteur -= 1
	if appat_compteur > 0:
		appat_compteur -= 1

	# Vérifier si le Pokémon fuit
	var fuit := SafariSystem.calculer_fuite_safari(pokemon_sauvage, colere_compteur, appat_compteur)
	if fuit:
		emit_signal("message_affiche", "%s a pris la fuite !" % pokemon_sauvage.surnom)
		emit_signal("pokemon_fuit")
		await get_tree().create_timer(1.2).timeout
		_fin_combat(false)
		return

	# Le Pokémon ne fuit pas — observer
	emit_signal("message_affiche", "%s observe attentivement..." % pokemon_sauvage.surnom)
	await get_tree().create_timer(0.8).timeout
	emit_signal("action_requise")

# ----------------------------------------------------------------
# Fin du combat
# ----------------------------------------------------------------
func _fin_combat(capture: bool) -> void:
	emit_signal("combat_termine", capture)
