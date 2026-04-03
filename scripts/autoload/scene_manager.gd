extends Node

# SceneManager — Singleton global
# Gestion des transitions de scènes avec fondu au noir

# --- Constantes ---
const DUREE_FONDU := 0.3  # secondes

# --- Nœuds ---
var _canvas_layer: CanvasLayer = null
var _rect_fondu: ColorRect = null
var _tween: Tween = null

# --- État ---
var _en_transition: bool = false
var _scene_en_attente: String = ""
var _params_en_attente: Dictionary = {}

# Params publics pour que les scènes puissent se self-initialiser
# si recevoir_params n'est pas appelé (fallback robuste)
var derniers_params_scene: Dictionary = {}
var _params_appliques: bool = false

# --- Signaux ---
signal transition_debut()
signal transition_fin()
signal scene_chargee(chemin: String)

func _ready() -> void:
	_creer_couche_fondu()

func _creer_couche_fondu() -> void:
	_canvas_layer = CanvasLayer.new()
	_canvas_layer.layer = 100
	add_child(_canvas_layer)

	_rect_fondu = ColorRect.new()
	_rect_fondu.color = Color(0, 0, 0, 0)
	_rect_fondu.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_rect_fondu.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_canvas_layer.add_child(_rect_fondu)

# Charger une nouvelle scène avec fondu
func charger_scene(chemin: String, params: Dictionary = {}) -> void:
	if _en_transition:
		return
	_en_transition = true
	_scene_en_attente = chemin
	_params_en_attente = params
	emit_signal("transition_debut")
	_fondu_vers(1.0, _charger_scene_apres_fondu)

# Retourner à la scène précédente (ex: fin de combat → overworld)
func retour_scene(chemin: String, params: Dictionary = {}) -> void:
	charger_scene(chemin, params)

# Fondu vers une opacité cible puis callback
func _fondu_vers(opacite_cible: float, callback: Callable) -> void:
	if _tween:
		_tween.kill()
	_tween = create_tween()
	_tween.tween_property(_rect_fondu, "color:a", opacite_cible, DUREE_FONDU)
	_tween.tween_callback(callback)

func _charger_scene_apres_fondu() -> void:
	# Stocker les params AVANT le changement de scène (pour fallback)
	derniers_params_scene = _params_en_attente.duplicate()
	_params_appliques = false
	print("[SceneManager] Changement scène → %s (params=%d clés)" % [_scene_en_attente, _params_en_attente.size()])
	var err = get_tree().change_scene_to_file(_scene_en_attente)
	if err != OK:
		push_error("SceneManager: impossible de charger la scène %s" % _scene_en_attente)
		_en_transition = false
		return
	emit_signal("scene_chargee", _scene_en_attente)
	# Attendre un frame pour que la scène soit initialisée
	await get_tree().process_frame
	print("[SceneManager] process_frame OK — appliquer params")
	_appliquer_params(_params_en_attente)
	_fondu_vers(0.0, _fin_transition)

func _appliquer_params(params: Dictionary) -> void:
	# Transmettre les paramètres à la scène active si besoin
	var racine = get_tree().current_scene
	print("[SceneManager] _appliquer_params: racine=%s, params=%d clés" % [racine.name if racine else "NULL", params.size()])
	if racine and params.size() > 0:
		if racine.has_method("recevoir_params"):
			print("[SceneManager] → racine.recevoir_params() appelé")
			_params_appliques = true
			racine.recevoir_params(params)
		else:
			print("[SceneManager] ⚠ racine n'a pas recevoir_params()")

func _fin_transition() -> void:
	_en_transition = false
	_params_en_attente = {}
	emit_signal("transition_fin")

func est_en_transition() -> bool:
	return _en_transition
