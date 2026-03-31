extends Node

# ItemsData — Autoload pour charger les données des objets
# Lit items.json et les expose via get_item()

const CHEMIN_JSON := "res://data/items.json"

var _donnees: Dictionary = {}
var _charge: bool = false

func _ready() -> void:
	_charger()

func _charger() -> void:
	if _charge:
		return
	if not FileAccess.file_exists(CHEMIN_JSON):
		push_error("ItemsData: fichier introuvable: %s" % CHEMIN_JSON)
		return
	var fichier := FileAccess.open(CHEMIN_JSON, FileAccess.READ)
	var data = JSON.parse_string(fichier.get_as_text())
	fichier.close()
	if data == null or not data is Dictionary:
		push_error("ItemsData: JSON invalide dans %s" % CHEMIN_JSON)
		return
	_donnees = data
	_charge = true

func get_item(item_id: String) -> Dictionary:
	if not _charge:
		_charger()
	return _donnees.get(item_id, {})

func tous_les_ids() -> Array:
	return _donnees.keys()

func existe(item_id: String) -> bool:
	return item_id in _donnees
