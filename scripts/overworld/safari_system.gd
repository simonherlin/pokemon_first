# safari_system.gd — Gestion du Parc Safari (état, pas, Balls)
# Mécaniques Gen 1 : 500 pas, 30 Safari Balls, entrée 500₽
class_name SafariSystem
extends Node

# --- Constantes ---
const PAS_MAX := 500
const BALLS_INITIALES := 30
const PRIX_ENTREE := 500

# --- État du Safari ---
var actif: bool = false
var pas_restants: int = 0
var balls_restantes: int = 0

# --- Signaux ---
signal safari_termine()
signal pas_mis_a_jour(restants: int)
signal balls_mis_a_jour(restantes: int)

# ----------------------------------------------------------------
# Entrée / Sortie du Safari
# ----------------------------------------------------------------

## Tente d'entrer dans le Safari. Retourne true si le joueur a assez d'argent.
func entrer_safari() -> bool:
	if actif:
		return true  # Déjà dedans
	if PlayerData.argent < PRIX_ENTREE:
		return false
	PlayerData.retirer_argent(PRIX_ENTREE)
	actif = true
	pas_restants = PAS_MAX
	balls_restantes = BALLS_INITIALES
	GameManager.set_flag("parc_safari_visite", true)
	emit_signal("pas_mis_a_jour", pas_restants)
	emit_signal("balls_mis_a_jour", balls_restantes)
	return true

## Quitter le Safari (volontairement ou forcé)
func quitter_safari() -> void:
	actif = false
	pas_restants = 0
	balls_restantes = 0
	emit_signal("safari_termine")

# ----------------------------------------------------------------
# Gestion des pas
# ----------------------------------------------------------------

## Appelé à chaque pas du joueur dans le Safari. Retourne true si le Safari est toujours actif.
func decompter_pas() -> bool:
	if not actif:
		return false
	pas_restants -= 1
	emit_signal("pas_mis_a_jour", pas_restants)
	if pas_restants <= 0:
		quitter_safari()
		return false
	return true

# ----------------------------------------------------------------
# Gestion des Safari Balls
# ----------------------------------------------------------------

## Utilise une Safari Ball. Retourne true si encore des balls.
func utiliser_ball() -> bool:
	if balls_restantes <= 0:
		return false
	balls_restantes -= 1
	emit_signal("balls_mis_a_jour", balls_restantes)
	if balls_restantes <= 0:
		quitter_safari()
		return false
	return true

# ----------------------------------------------------------------
# Formule de capture Safari (Gen 1)
# ----------------------------------------------------------------
# En Gen 1, le taux de capture Safari dépend du taux_capture de l'espèce,
# modifié par les cailloux (colère) et l'appât.
# colere_compteur augmente le catch rate mais aussi le flee rate
# appat_compteur diminue le flee rate mais aussi le catch rate

## Calculer si la capture réussit
## colere : nombre de tours de colère restants (lancé caillou)
## appat : nombre de tours d'appât restants
static func calculer_capture_safari(pokemon: Pokemon, colere: int, appat: int) -> bool:
	var espece_data := SpeciesData.get_espece(pokemon.espece_id)
	var taux_base: int = espece_data.get("taux_capture", 255)

	# Modificateur selon état (colère double le taux, appât le divise par 2)
	var taux_modifie: float = float(taux_base)
	if colere > 0:
		taux_modifie *= 2.0
	if appat > 0:
		taux_modifie /= 2.0

	taux_modifie = clampf(taux_modifie, 1.0, 255.0)

	# Formula Gen 1 Safari: random(0, 255) < taux_modifie
	var tirage := randi() % 256
	return tirage < int(taux_modifie)

## Calculer si le Pokémon fuit
## colere : le caillou augmente la fuite
## appat : l'appât diminue la fuite
static func calculer_fuite_safari(pokemon: Pokemon, colere: int, appat: int) -> bool:
	var espece_data := SpeciesData.get_espece(pokemon.espece_id)
	var vitesse_base: int = espece_data.get("stats_base", {}).get("vitesse", 50)

	# Taux de fuite basé sur la vitesse de base
	var taux_fuite: float = float(vitesse_base)
	if colere > 0:
		taux_fuite *= 2.0
	if appat > 0:
		taux_fuite /= 2.0

	taux_fuite = clampf(taux_fuite, 1.0, 255.0)

	# Random(0, 255) < taux_fuite → le Pokémon fuit
	var tirage := randi() % 256
	return tirage < int(taux_fuite)

# ----------------------------------------------------------------
# Vérification de zone Safari
# ----------------------------------------------------------------

## Vérifie si la carte actuelle est dans le Parc Safari
static func est_zone_safari() -> bool:
	var carte_id: String = PlayerData.carte_actuelle
	return carte_id.begins_with("parc_safari_zone")

## Les cartes du Safari
static func est_carte_safari(carte_id: String) -> bool:
	return carte_id.begins_with("parc_safari")
