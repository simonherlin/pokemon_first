extends Node

# MoveData — Singleton (ou autoload) pour charger les données des attaques
# Lit moves.json une seule fois et expose les données via get_move()

const CHEMIN_JSON := "res://data/pokemon/moves.json"

var _donnees: Dictionary = {}
var _charge: bool = false

func _ready() -> void:
	_charger()

func _charger() -> void:
	if _charge:
		return
	if not FileAccess.file_exists(CHEMIN_JSON):
		push_error("MoveData: fichier introuvable: %s" % CHEMIN_JSON)
		return
	var fichier := FileAccess.open(CHEMIN_JSON, FileAccess.READ)
	var data = JSON.parse_string(fichier.get_as_text())
	fichier.close()
	if data == null or not data is Dictionary:
		push_error("MoveData: JSON invalide dans %s" % CHEMIN_JSON)
		return
	_donnees = data
	_charge = true

# Obtenir les données d'une attaque par son ID
func get_move(move_id: String) -> Dictionary:
	if not _charge:
		_charger()
	return _donnees.get(move_id, {})

# Obtenir la liste de tous les IDs d'attaques
func tous_les_ids() -> Array:
	return _donnees.keys()

# Vérifier si une attaque existe
func existe(move_id: String) -> bool:
	return move_id in _donnees
