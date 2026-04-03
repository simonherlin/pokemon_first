extends Node

# TimeManager — Singleton global
# Gère le cycle jour/nuit basé sur l'horloge système
# Affecte la teinte visuelle des cartes extérieures

# --- Phases du jour ---
enum Phase {
	AUBE,         # 6h-8h
	JOUR,         # 8h-18h
	CREPUSCULE,   # 18h-20h
	NUIT          # 20h-6h
}

# --- Teintes par phase ---
const TEINTES := {
	Phase.AUBE:        Color(1.0, 0.85, 0.7, 0.15),    # Orange chaud léger
	Phase.JOUR:        Color(1.0, 1.0, 1.0, 0.0),       # Pas de teinte
	Phase.CREPUSCULE:  Color(1.0, 0.6, 0.4, 0.2),       # Orange-rouge
	Phase.NUIT:        Color(0.3, 0.3, 0.6, 0.35),       # Bleu foncé
}

# --- Noms français des phases ---
const NOMS_PHASES := {
	Phase.AUBE: "Aube",
	Phase.JOUR: "Jour",
	Phase.CREPUSCULE: "Crépuscule",
	Phase.NUIT: "Nuit",
}

# --- État ---
var phase_actuelle: Phase = Phase.JOUR
var heure_actuelle: int = 12
var minute_actuelle: int = 0

# --- Signaux ---
signal phase_changee(nouvelle_phase: Phase)

func _ready() -> void:
	_mettre_a_jour_heure()

func _process(_delta: float) -> void:
	_mettre_a_jour_heure()

# Mettre à jour l'heure depuis l'horloge système
func _mettre_a_jour_heure() -> void:
	var temps := Time.get_time_dict_from_system()
	heure_actuelle = temps.get("hour", 12)
	minute_actuelle = temps.get("minute", 0)
	var nouvelle_phase := _calculer_phase(heure_actuelle)
	if nouvelle_phase != phase_actuelle:
		phase_actuelle = nouvelle_phase
		emit_signal("phase_changee", phase_actuelle)

# Déterminer la phase selon l'heure
func _calculer_phase(heure: int) -> Phase:
	if heure >= 6 and heure < 8:
		return Phase.AUBE
	elif heure >= 8 and heure < 18:
		return Phase.JOUR
	elif heure >= 18 and heure < 20:
		return Phase.CREPUSCULE
	else:
		return Phase.NUIT

# Obtenir la teinte actuelle (Color avec alpha)
func get_teinte_actuelle() -> Color:
	return TEINTES.get(phase_actuelle, TEINTES[Phase.JOUR])

# Obtenir le nom de la phase
func get_nom_phase() -> String:
	return NOMS_PHASES.get(phase_actuelle, "Jour")

# Vérifier si une carte est extérieure (affectée par le cycle jour/nuit)
func est_carte_exterieure(carte_data: Dictionary) -> bool:
	if carte_data.get("sombre", false):
		return false  # Les grottes sombres ne sont pas affectées
	# Les cartes marquées intérieur ne sont pas affectées
	if carte_data.get("interieur", false):
		return false
	# Détection automatique des intérieurs par le nom de la carte
	var carte_id: String = carte_data.get("id", "")
	var prefixes_interieur := [
		"maison_", "centre_pokemon_", "boutique_", "arene_",
		"laboratoire", "labo_", "tour_pokemon_", "tour_sylphe_",
		"ss_anne_", "repaire_rocket_", "casino_", "grand_magasin_",
		"grotte_", "tunnel_", "mont_selenite_", "iles_ecume_",
		"manoir_pokemon_", "route_victoire_", "grotte_inconnue_",
		"ligue_", "dojo_", "musee_", "cabane_", "centrale",
		"parc_safari_entree", "sevii_ile1_", "sevii_ile2_",
		"sevii_ile3_", "sevii_grotte_"
	]
	for prefixe in prefixes_interieur:
		if carte_id.begins_with(prefixe):
			return false
	var tileset: String = carte_data.get("tileset", "")
	return tileset in ["outdoor", "exterieur"]

# Modificateur de taux de rencontre selon l'heure
# La nuit : +20% de rencontres, À l'aube : -10%
func get_modificateur_rencontre() -> float:
	match phase_actuelle:
		Phase.NUIT:
			return 1.2
		Phase.AUBE:
			return 0.9
		Phase.CREPUSCULE:
			return 1.1
	return 1.0
