extends Node

# MapLoader — Utilitaire pour charger les données JSON des cartes

const DOSSIER_MAPS := "res://data/maps/"

var _cartes: Dictionary = {}

func _ready() -> void:
	pass

# Charger une carte par son ID
func get_carte(carte_id: String) -> Dictionary:
	if carte_id in _cartes:
		return _cartes[carte_id]
	var chemin := DOSSIER_MAPS + carte_id + ".json"
	if not FileAccess.file_exists(chemin):
		push_warning("MapLoader: carte introuvable: %s" % chemin)
		return {}
	var fichier := FileAccess.open(chemin, FileAccess.READ)
	var data = JSON.parse_string(fichier.get_as_text())
	fichier.close()
	if data == null:
		push_error("MapLoader: JSON invalide: %s" % chemin)
		return {}
	_cartes[carte_id] = data
	return data
