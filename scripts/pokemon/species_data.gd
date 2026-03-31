extends Node

# SpeciesData — Autoload pour charger les données des espèces Pokémon
# Lit species.json une seule fois et fournit les données par ID

const CHEMIN_JSON := "res://data/pokemon/species.json"

var _donnees: Dictionary = {}
var _charge: bool = false

func _ready() -> void:
	_charger()

func _charger() -> void:
	if _charge:
		return
	if not FileAccess.file_exists(CHEMIN_JSON):
		push_error("SpeciesData: fichier introuvable: %s" % CHEMIN_JSON)
		return
	var fichier := FileAccess.open(CHEMIN_JSON, FileAccess.READ)
	var data = JSON.parse_string(fichier.get_as_text())
	fichier.close()
	if data == null or not data is Dictionary:
		push_error("SpeciesData: JSON invalide dans %s" % CHEMIN_JSON)
		return
	_donnees = data
	_charge = true

# Obtenir les données d'une espèce par son ID (ex: "001", "025")
func get_espece(espece_id: String) -> Dictionary:
	if not _charge:
		_charger()
	# Normaliser l'ID en 3 chiffres
	var id_norm := _normaliser_id(espece_id)
	return _donnees.get(id_norm, {})

# Obtenir les données par numéro entier
func get_espece_par_numero(numero: int) -> Dictionary:
	return get_espece(str(numero).lpad(3, "0"))

# Créer une instance Pokemon depuis un espece_id et un niveau
func creer_pokemon(espece_id: String, niveau: int) -> Pokemon:
	var espece_data := get_espece(espece_id)
	if espece_data.is_empty():
		push_error("SpeciesData: espèce introuvable: %s" % espece_id)
		return null
	var p := Pokemon.new()
	p.initialiser(espece_data, niveau)
	return p

# Créer un Pokémon sauvage aléatoire pour la capture
func creer_sauvage(espece_id: String, niveau: int) -> Pokemon:
	var p := creer_pokemon(espece_id, niveau)
	if p:
		p.id_dresseur = -1  # -1 = sauvage
	return p

# Nombre total d'espèces chargées
func nombre_especes() -> int:
	return _donnees.size()

# Obtenir tous les IDs d'espèces
func tous_les_ids() -> Array:
	return _donnees.keys()

# --- Évolution ---
# Vérifier si un Pokémon peut évoluer au niveau actuel
func peut_evoluer_niveau(espece_id: String, niveau: int) -> String:
	var data := get_espece(espece_id)
	if data.is_empty():
		return ""
	var evo: Dictionary = data.get("evolution", {})
	if evo.is_empty():
		return ""
	if evo.get("methode", "") == "niveau" and niveau >= evo.get("niveau", 999):
		return evo.get("vers", "")
	return ""

# Vérifier si un Pokémon peut évoluer avec une pierre
func peut_evoluer_pierre(espece_id: String, pierre_id: String) -> String:
	var data := get_espece(espece_id)
	if data.is_empty():
		return ""
	var evo: Dictionary = data.get("evolution", {})
	if evo.is_empty():
		return ""
	if evo.get("methode", "") == "pierre" and evo.get("pierre", "") == pierre_id:
		return evo.get("vers", "")
	return ""

# Faire évoluer un Pokémon (retourne la nouvelle espèce_id ou "" si impossible)
func evoluer(pokemon: Pokemon) -> String:
	var vers := peut_evoluer_niveau(pokemon.espece_id, pokemon.niveau)
	if vers.is_empty():
		return ""
	var ancienne_espece := get_espece(pokemon.espece_id)
	var nouvelle_espece := get_espece(vers)
	if nouvelle_espece.is_empty():
		return ""

	# Appliquer les nouvelles données d'espèce
	pokemon.espece_id = vers
	pokemon.nom_espece = nouvelle_espece.get("nom", "???")
	pokemon.types = nouvelle_espece.get("types", pokemon.types)
	pokemon.stats_base = nouvelle_espece.get("stats_base", pokemon.stats_base)
	pokemon.groupe_exp = nouvelle_espece.get("groupe_exp", pokemon.groupe_exp)
	# Recalculer les stats mais conserver les PV actuels (ratio)
	var ratio_pv := float(pokemon.pv_actuels) / float(pokemon.pv_max)
	pokemon._calculer_stats()
	pokemon.pv_actuels = maxi(1, int(pokemon.pv_max * ratio_pv))
	# Si surnom = ancien nom d'espèce → mettre à jour
	if pokemon.surnom == ancienne_espece.get("nom", ""):
		pokemon.surnom = pokemon.nom_espece
	return vers

# Normaliser un ID en 3 chiffres
func _normaliser_id(espece_id: String) -> String:
	if espece_id.length() >= 3:
		return espece_id
	return espece_id.lpad(3, "0")
