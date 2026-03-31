extends Control

# TitleScreen — Écran titre avec sélection Nouvelle Partie / Continuer

var _index: int = 0
var _options := ["nouvelle", "continuer"]

@onready var label_nouvelle: Label = $VBox/LabelNouvelle
@onready var label_continuer: Label = $VBox/LabelContinuer

func _ready() -> void:
	_index = 0
	_mettre_a_jour_curseur()

func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("action_haut"):
		_index = (_index - 1 + _options.size()) % _options.size()
		_mettre_a_jour_curseur()
	elif Input.is_action_just_pressed("action_bas"):
		_index = (_index + 1) % _options.size()
		_mettre_a_jour_curseur()
	elif Input.is_action_just_pressed("action_confirmer"):
		_selectionner()

func _mettre_a_jour_curseur() -> void:
	label_nouvelle.text = ("▶ " if _index == 0 else "  ") + "Nouvelle Partie"
	label_continuer.text = ("▶ " if _index == 1 else "  ") + "Continuer"

func _selectionner() -> void:
	match _options[_index]:
		"nouvelle":
			# Lancer la séquence d'introduction du Prof. Chen
			SceneManager.charger_scene("res://scenes/ui/intro_scene.tscn")
		"continuer":
			if SaveManager.slot_existe(0):
				SaveManager.charger(0)
				var carte: String = PlayerData.carte_actuelle
				SceneManager.charger_scene("res://scenes/maps/%s.tscn" % carte)
			else:
				# Pas de sauvegarde disponible
				pass
