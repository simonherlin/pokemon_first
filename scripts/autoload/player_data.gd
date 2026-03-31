extends Node

# PlayerData — Singleton global
# Données persistantes du joueur : équipe, inventaire, Pokédex, position

# --- Constantes ---
const MAX_EQUIPE := 6
const MAX_BOITE_TAILLE := 30
const MAX_BOITES := 12

# --- Identité joueur ---
var nom_joueur: String = "Joueur"
var argent: int = 3000
var id_joueur: int = 0  # ID dresseur aléatoire (0-65535)

# --- Position ---
var carte_actuelle: String = "bourg_palette"
var position_x: int = 7
var position_y: int = 12
var direction: String = "bas"

# --- Équipe (max 6 Pokémon) ---
# Chaque entrée est un Dictionary représentant un Pokémon en jeu
var equipe: Array = []

# --- Boîtes PC ---
var boites: Array = []  # Array de Array de pokemon

# --- Inventaire ---
# Structure: {"item_id": quantite}
var inventaire: Dictionary = {}

# --- Pokédex ---
var pokedex_vu: Array[String] = []      # IDs des Pokémon vus
var pokedex_capture: Array[String] = [] # IDs des Pokémon capturés

# --- Dresseurs battus (pour ne pas les refaire) ---
var dresseurs_battus: Array[String] = []

# --- Objets ramassés au sol ---
var objets_ramasses: Array[String] = []  # IDs d'objets sol ramassés

# --- Signaux ---
signal argent_modifie(nouveau_montant: int)
signal equipe_modifiee()
signal inventaire_modifie(item_id: String, quantite: int)
signal pokemon_vu(espece_id: String)
signal pokemon_capture(espece_id: String)

func _ready() -> void:
	# Initialiser les boîtes vides
	for _i in range(MAX_BOITES):
		boites.append([])

# --- Argent ---
func ajouter_argent(montant: int) -> void:
	argent = max(0, argent + montant)
	emit_signal("argent_modifie", argent)

func depenser_argent(montant: int) -> bool:
	if argent < montant:
		return false
	argent -= montant
	emit_signal("argent_modifie", argent)
	return true

# --- Équipe ---
func ajouter_pokemon(pokemon_data: Dictionary) -> bool:
	if equipe.size() >= MAX_EQUIPE:
		return false
	equipe.append(pokemon_data)
	emit_signal("equipe_modifiee")
	return true

func retirer_pokemon(index: int) -> Dictionary:
	if index < 0 or index >= equipe.size():
		return {}
	var pokemon = equipe.pop_at(index)
	emit_signal("equipe_modifiee")
	return pokemon

# --- Boîtes PC ---
func deposer_pokemon(index_equipe: int, boite_index: int = -1) -> bool:
	# Impossible de déposer si un seul Pokémon reste
	if equipe.size() <= 1:
		return false
	if index_equipe < 0 or index_equipe >= equipe.size():
		return false
	# Trouver la première boîte avec de la place si non spécifié
	if boite_index < 0:
		boite_index = _trouver_boite_libre()
	if boite_index < 0 or boite_index >= MAX_BOITES:
		return false
	if boites[boite_index].size() >= MAX_BOITE_TAILLE:
		return false
	var pokemon = equipe.pop_at(index_equipe)
	boites[boite_index].append(pokemon)
	emit_signal("equipe_modifiee")
	return true

func retirer_boite_pokemon(boite_index: int, index_pokemon: int) -> bool:
	if equipe.size() >= MAX_EQUIPE:
		return false
	if boite_index < 0 or boite_index >= MAX_BOITES:
		return false
	if index_pokemon < 0 or index_pokemon >= boites[boite_index].size():
		return false
	var pokemon = boites[boite_index].pop_at(index_pokemon)
	equipe.append(pokemon)
	emit_signal("equipe_modifiee")
	return true

func _trouver_boite_libre() -> int:
	for i in range(MAX_BOITES):
		if boites[i].size() < MAX_BOITE_TAILLE:
			return i
	return -1

func compter_pokemon_boites() -> int:
	var total := 0
	for boite in boites:
		total += boite.size()
	return total

func pokemon_equipe_vivant() -> Array:
	var vivants := []
	for p in equipe:
		if p.get("pv_actuels", 0) > 0:
			vivants.append(p)
	return vivants

func equipe_ko() -> bool:
	for p in equipe:
		if p.get("pv_actuels", 0) > 0:
			return false
	return true

# --- Inventaire ---
func ajouter_item(item_id: String, quantite: int = 1) -> void:
	if item_id in inventaire:
		inventaire[item_id] += quantite
	else:
		inventaire[item_id] = quantite
	emit_signal("inventaire_modifie", item_id, inventaire[item_id])

func retirer_item(item_id: String, quantite: int = 1) -> bool:
	if not item_id in inventaire or inventaire[item_id] < quantite:
		return false
	inventaire[item_id] -= quantite
	if inventaire[item_id] <= 0:
		inventaire.erase(item_id)
	var qte = inventaire.get(item_id, 0)
	emit_signal("inventaire_modifie", item_id, qte)
	return true

func quantite_item(item_id: String) -> int:
	return inventaire.get(item_id, 0)

func possede_item(item_id: String) -> bool:
	return inventaire.get(item_id, 0) > 0

# --- Pokédex ---
func enregistrer_vu(espece_id: String) -> void:
	if not espece_id in pokedex_vu:
		pokedex_vu.append(espece_id)
		emit_signal("pokemon_vu", espece_id)

func enregistrer_capture(espece_id: String) -> void:
	enregistrer_vu(espece_id)
	if not espece_id in pokedex_capture:
		pokedex_capture.append(espece_id)
		emit_signal("pokemon_capture", espece_id)

func a_vu(espece_id: String) -> bool:
	return espece_id in pokedex_vu

func a_capture(espece_id: String) -> bool:
	return espece_id in pokedex_capture

# --- Dresseurs ---
func marquer_dresseur_battu(dresseur_id: String) -> void:
	if not dresseur_id in dresseurs_battus:
		dresseurs_battus.append(dresseur_id)

func dresseur_est_battu(dresseur_id: String) -> bool:
	return dresseur_id in dresseurs_battus

# --- Objets sol ---
func marquer_objet_ramasse(objet_id: String) -> void:
	if not objet_id in objets_ramasses:
		objets_ramasses.append(objet_id)

func objet_est_ramasse(objet_id: String) -> bool:
	return objet_id in objets_ramasses

# --- Position ---
func sauvegarder_position(carte: String, x: int, y: int, dir: String = "bas") -> void:
	carte_actuelle = carte
	position_x = x
	position_y = y
	direction = dir

# --- Réinitialisation nouvelle partie ---
func nouvelle_partie(nom: String) -> void:
	nom_joueur = nom
	argent = 3000
	id_joueur = randi() % 65536
	carte_actuelle = "bourg_palette"
	position_x = 7
	position_y = 12
	direction = "bas"
	equipe = []
	inventaire = {}
	pokedex_vu = []
	pokedex_capture = []
	dresseurs_battus = []
	objets_ramasses = []
	boites = []
	for _i in range(MAX_BOITES):
		boites.append([])
