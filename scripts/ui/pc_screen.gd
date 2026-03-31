extends CanvasLayer

# PCScreen — Écran du système de Stockage Pokémon de Bill
# Permet de déposer et retirer des Pokémon des boîtes PC

signal pc_ferme()

const TAILLE_BOITE := 30

var _boite_actuelle: int = 0
var _mode: String = "menu"  # "menu", "deposer", "retirer"
var _curseur: int = 0
var _boite_curseur: int = 0

@onready var fond: ColorRect = $Fond
@onready var titre_label: Label = $Fond/TitreLabel
@onready var liste_container: VBoxContainer = $Fond/ListeContainer
@onready var info_label: Label = $Fond/InfoLabel
@onready var instructions_label: Label = $Fond/InstructionsLabel

func _ready() -> void:
	_afficher_menu_principal()

func _afficher_menu_principal() -> void:
	_mode = "menu"
	_curseur = 0
	titre_label.text = "PC de BILL"
	_nettoyer_liste()
	
	var options := ["DÉPOSER un Pokémon", "RETIRER un Pokémon", "CHANGER de BOÎTE", "FERMER"]
	for i in range(options.size()):
		var label := Label.new()
		label.text = ("▶ " if i == _curseur else "   ") + options[i]
		label.add_theme_font_size_override("font_size", 14)
		liste_container.add_child(label)
	
	info_label.text = "Équipe : %d/%d | Boîte %d : %d/%d" % [
		PlayerData.equipe.size(), PlayerData.MAX_EQUIPE,
		_boite_actuelle + 1, PlayerData.boites[_boite_actuelle].size(), TAILLE_BOITE
	]
	instructions_label.text = "Z : Confirmer | X : Annuler"

func _afficher_liste_equipe() -> void:
	_mode = "deposer"
	_curseur = 0
	titre_label.text = "DÉPOSER un Pokémon"
	_nettoyer_liste()
	
	if PlayerData.equipe.size() <= 1:
		var label := Label.new()
		label.text = "Il faut garder au moins 1 Pokémon !"
		label.add_theme_font_size_override("font_size", 14)
		liste_container.add_child(label)
		info_label.text = ""
		instructions_label.text = "X : Retour"
		return
	
	for i in range(PlayerData.equipe.size()):
		var pkmn: Dictionary = PlayerData.equipe[i]
		var label := Label.new()
		var nom: String = pkmn.get("surnom", "???")
		var niv: int = pkmn.get("niveau", 1)
		var pv: int = pkmn.get("pv_actuels", 0)
		var pv_max: int = pkmn.get("stats", {}).get("pv", 1)
		label.text = ("▶ " if i == _curseur else "   ") + "%s  N.%d  PV %d/%d" % [nom, niv, pv, pv_max]
		label.add_theme_font_size_override("font_size", 14)
		liste_container.add_child(label)
	
	info_label.text = "Boîte %d : %d/%d places" % [
		_boite_actuelle + 1,
		PlayerData.boites[_boite_actuelle].size(), TAILLE_BOITE
	]
	instructions_label.text = "Z : Déposer | X : Retour"

func _afficher_liste_boite() -> void:
	_mode = "retirer"
	_boite_curseur = 0
	titre_label.text = "BOÎTE %d — RETIRER" % (_boite_actuelle + 1)
	_nettoyer_liste()
	
	var boite: Array = PlayerData.boites[_boite_actuelle]
	if boite.is_empty():
		var label := Label.new()
		label.text = "Cette boîte est vide."
		label.add_theme_font_size_override("font_size", 14)
		liste_container.add_child(label)
		info_label.text = ""
		instructions_label.text = "X : Retour"
		return
	
	for i in range(boite.size()):
		var pkmn: Dictionary = boite[i]
		var label := Label.new()
		var nom: String = pkmn.get("surnom", "???")
		var niv: int = pkmn.get("niveau", 1)
		label.text = ("▶ " if i == _boite_curseur else "   ") + "%s  N.%d" % [nom, niv]
		label.add_theme_font_size_override("font_size", 14)
		liste_container.add_child(label)
	
	info_label.text = "Équipe : %d/%d" % [PlayerData.equipe.size(), PlayerData.MAX_EQUIPE]
	instructions_label.text = "Z : Retirer | X : Retour"

func _nettoyer_liste() -> void:
	for child in liste_container.get_children():
		child.queue_free()

func _process(_delta: float) -> void:
	match _mode:
		"menu":
			_traiter_input_menu()
		"deposer":
			_traiter_input_deposer()
		"retirer":
			_traiter_input_retirer()

func _traiter_input_menu() -> void:
	if Input.is_action_just_pressed("ui_down"):
		_curseur = mini(_curseur + 1, 3)
		_afficher_menu_principal()
	elif Input.is_action_just_pressed("ui_up"):
		_curseur = maxi(_curseur - 1, 0)
		_afficher_menu_principal()
	elif Input.is_action_just_pressed("confirmer"):
		match _curseur:
			0:  # Déposer
				_afficher_liste_equipe()
			1:  # Retirer
				_afficher_liste_boite()
			2:  # Changer boîte
				_boite_actuelle = (_boite_actuelle + 1) % PlayerData.MAX_BOITES
				_afficher_menu_principal()
			3:  # Fermer
				_fermer()
	elif Input.is_action_just_pressed("annuler"):
		_fermer()

func _traiter_input_deposer() -> void:
	if PlayerData.equipe.size() <= 1:
		if Input.is_action_just_pressed("annuler") or Input.is_action_just_pressed("confirmer"):
			_afficher_menu_principal()
		return
	
	if Input.is_action_just_pressed("ui_down"):
		_curseur = mini(_curseur + 1, PlayerData.equipe.size() - 1)
		_afficher_liste_equipe()
	elif Input.is_action_just_pressed("ui_up"):
		_curseur = maxi(_curseur - 1, 0)
		_afficher_liste_equipe()
	elif Input.is_action_just_pressed("confirmer"):
		if PlayerData.deposer_pokemon(_curseur, _boite_actuelle):
			_curseur = maxi(_curseur - 1, 0)
			_afficher_liste_equipe()
		else:
			info_label.text = "Impossible de déposer ce Pokémon !"
	elif Input.is_action_just_pressed("annuler"):
		_afficher_menu_principal()

func _traiter_input_retirer() -> void:
	var boite: Array = PlayerData.boites[_boite_actuelle]
	if boite.is_empty():
		if Input.is_action_just_pressed("annuler") or Input.is_action_just_pressed("confirmer"):
			_afficher_menu_principal()
		return
	
	if Input.is_action_just_pressed("ui_down"):
		_boite_curseur = mini(_boite_curseur + 1, boite.size() - 1)
		_afficher_liste_boite()
	elif Input.is_action_just_pressed("ui_up"):
		_boite_curseur = maxi(_boite_curseur - 1, 0)
		_afficher_liste_boite()
	elif Input.is_action_just_pressed("confirmer"):
		if PlayerData.retirer_boite_pokemon(_boite_actuelle, _boite_curseur):
			_boite_curseur = maxi(_boite_curseur - 1, 0)
			_afficher_liste_boite()
		else:
			info_label.text = "Équipe pleine !"
	elif Input.is_action_just_pressed("annuler"):
		_afficher_menu_principal()

func _fermer() -> void:
	emit_signal("pc_ferme")
	queue_free()
