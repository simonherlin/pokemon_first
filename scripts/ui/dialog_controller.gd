extends Control

# DialogController — Système de dialogue typewriter
# Affiche du texte lettre par lettre, gère les choix Oui/Non

# --- Constantes ---
const VITESSE_TEXTE := 30.0  # caractères/seconde
const VITESSE_RAPIDE := 120.0  # quand le joueur maintient A

# --- Nœuds ---
@onready var label_texte: RichTextLabel = $PanelContainer/MarginContainer/LabelTexte
@onready var indicateur_suite: TextureRect = $PanelContainer/IndicateurSuite
@onready var panel: PanelContainer = $PanelContainer

# Choix Oui/Non
@onready var panel_choix: VBoxContainer = $PanelChoix
@onready var label_oui: Label = $PanelChoix/LabelOui
@onready var label_non: Label = $PanelChoix/LabelNon

# --- État ---
var _lignes_en_attente: Array = []
var _texte_actuel: String = ""
var _index_char: float = 0.0
var _texte_complet: bool = false
var _en_attente_input: bool = false
var _choix_actif: bool = false
var _choix_index: int = 1  # 0=Oui, 1=Non (default sur Non)
var _visible_dialog: bool = false

# --- Signaux ---
signal dialogue_termine()
signal choix_fait(oui: bool)

func _ready() -> void:
	visible = false
	if panel_choix:
		panel_choix.visible = false

func _process(delta: float) -> void:
	if not _visible_dialog:
		return

	if _choix_actif:
		_gerer_choix()
		return

	if _en_attente_input:
		_gerer_attente_input()
		return

	if not _texte_complet:
		_animer_texte(delta)

func afficher_dialogue(lignes: Array) -> void:
	_lignes_en_attente = lignes.duplicate()
	_visible_dialog = true
	visible = true
	if panel_choix:
		panel_choix.visible = false
	_afficher_prochaine_ligne()

func afficher_choix(question: String) -> void:
	_lignes_en_attente = []
	_texte_actuel = question
	_index_char = question.length()
	_texte_complet = true
	_visible_dialog = true
	visible = true
	label_texte.text = question
	_choix_actif = true
	_choix_index = 1  # Non par défaut
	if panel_choix:
		panel_choix.visible = true
		_mettre_a_jour_choix()

func _afficher_prochaine_ligne() -> void:
	if _lignes_en_attente.is_empty():
		_fermer()
		return
	_texte_actuel = _lignes_en_attente.pop_front()
	_index_char = 0.0
	_texte_complet = false
	_en_attente_input = false
	label_texte.text = ""
	if indicateur_suite:
		indicateur_suite.visible = false

func _animer_texte(delta: float) -> void:
	var vitesse := VITESSE_RAPIDE if Input.is_action_pressed("action_confirmer") else VITESSE_TEXTE
	var ancien_nb := int(_index_char)
	_index_char += vitesse * delta

	var nb_chars := mini(int(_index_char), _texte_actuel.length())
	label_texte.text = _texte_actuel.substr(0, nb_chars)
	# Son de texte toutes les 3 lettres
	if nb_chars > ancien_nb and nb_chars % 3 == 0 and nb_chars < _texte_actuel.length():
		AudioManager.jouer_sfx("res://assets/audio/sfx/text_advance.ogg")

	if nb_chars >= _texte_actuel.length():
		_texte_complet = true
		_en_attente_input = true
		if indicateur_suite:
			indicateur_suite.visible = true

func _gerer_attente_input() -> void:
	if Input.is_action_just_pressed("action_confirmer"):
		AudioManager.jouer_sfx("res://assets/audio/sfx/confirm.ogg")
		_en_attente_input = false
		if indicateur_suite:
			indicateur_suite.visible = false
		_afficher_prochaine_ligne()

func _gerer_choix() -> void:
	if Input.is_action_just_pressed("action_haut"):
		_choix_index = 0
		AudioManager.jouer_sfx("res://assets/audio/sfx/cursor_move.ogg")
		_mettre_a_jour_choix()
	elif Input.is_action_just_pressed("action_bas"):
		_choix_index = 1
		AudioManager.jouer_sfx("res://assets/audio/sfx/cursor_move.ogg")
		_mettre_a_jour_choix()
	elif Input.is_action_just_pressed("action_confirmer"):
		AudioManager.jouer_sfx("res://assets/audio/sfx/confirm.ogg")
		_choix_actif = false
		if panel_choix:
			panel_choix.visible = false
		emit_signal("choix_fait", _choix_index == 0)
		_fermer()
	elif Input.is_action_just_pressed("action_annuler"):
		AudioManager.jouer_sfx("res://assets/audio/sfx/cancel.ogg")
		_choix_actif = false
		if panel_choix:
			panel_choix.visible = false
		emit_signal("choix_fait", false)
		_fermer()

func _mettre_a_jour_choix() -> void:
	if label_oui:
		label_oui.text = "▶ Oui" if _choix_index == 0 else "  Oui"
	if label_non:
		label_non.text = "▶ Non" if _choix_index == 1 else "  Non"

func _fermer() -> void:
	_visible_dialog = false
	visible = false
	emit_signal("dialogue_termine")

# Vérifier si un dialogue est en cours
func est_actif() -> bool:
	return _visible_dialog
