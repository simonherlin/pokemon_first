extends Node

# WeatherManager — Singleton global
# Gère les effets météo visuels sur les cartes extérieures

# --- Types de météo ---
enum Meteo {
	AUCUNE,
	PLUIE,
	SOLEIL,
	NEIGE,
	TEMPETE_SABLE
}

# --- Noms français ---
const NOMS_METEO := {
	Meteo.AUCUNE: "",
	Meteo.PLUIE: "Pluie",
	Meteo.SOLEIL: "Soleil intense",
	Meteo.NEIGE: "Neige",
	Meteo.TEMPETE_SABLE: "Tempête de sable",
}

# --- Teintes par météo (s'ajoutent à la teinte jour/nuit) ---
const TEINTES_METEO := {
	Meteo.AUCUNE:         Color(1, 1, 1, 0),
	Meteo.PLUIE:          Color(0.4, 0.4, 0.6, 0.15),     # Bleuté léger
	Meteo.SOLEIL:         Color(1.0, 0.9, 0.6, 0.1),       # Jaune chaud
	Meteo.NEIGE:          Color(0.8, 0.85, 1.0, 0.12),     # Blanc-bleu
	Meteo.TEMPETE_SABLE:  Color(0.8, 0.7, 0.4, 0.2),       # Brun-jaune
}

# --- Météo par défaut pour certaines cartes ---
const METEO_CARTES := {
	# Routes souvent pluvieuses (ambiance)
	"route_14": Meteo.PLUIE,
	"route_15": Meteo.PLUIE,
	# Îles Écume — neige/vent
	"iles_ecume_b1f": Meteo.NEIGE,
	"iles_ecume_b2f": Meteo.NEIGE,
	"iles_ecume_b3f": Meteo.NEIGE,
	"iles_ecume_b4f": Meteo.NEIGE,
	# Sevii volcanique — soleil intense
	"sevii_volcan_ext": Meteo.SOLEIL,
	"sevii_sentier_braise": Meteo.SOLEIL,
}

# --- État ---
var meteo_actuelle: Meteo = Meteo.AUCUNE
var _carte_actuelle_id: String = ""
var _overlay: CanvasLayer = null
var _particules_pluie: Array[Label] = []
var _particules_neige: Array[Label] = []
var _overlay_teinte: ColorRect = null

# --- Signaux ---
signal meteo_changee(nouvelle_meteo: Meteo)

func _ready() -> void:
	set_process(false)

# Définir la météo pour une carte donnée
func configurer_meteo_carte(carte_id: String, carte_data: Dictionary) -> void:
	_carte_actuelle_id = carte_id
	# Vérifier si la carte a une météo fixée dans les données
	var meteo_json: String = carte_data.get("meteo", "")
	if not meteo_json.is_empty():
		meteo_actuelle = _string_to_meteo(meteo_json)
	elif carte_id in METEO_CARTES:
		meteo_actuelle = METEO_CARTES[carte_id]
	else:
		# Météo aléatoire pour les cartes extérieures (10% de chance de pluie)
		if TimeManager.est_carte_exterieure(carte_data):
			if randf() < 0.10:
				meteo_actuelle = Meteo.PLUIE
			else:
				meteo_actuelle = Meteo.AUCUNE
		else:
			meteo_actuelle = Meteo.AUCUNE
	emit_signal("meteo_changee", meteo_actuelle)

# Convertir une chaîne en Meteo
func _string_to_meteo(nom: String) -> Meteo:
	match nom.to_lower():
		"pluie": return Meteo.PLUIE
		"soleil": return Meteo.SOLEIL
		"neige": return Meteo.NEIGE
		"tempete_sable": return Meteo.TEMPETE_SABLE
	return Meteo.AUCUNE

# Obtenir le nom de la météo actuelle
func get_nom_meteo() -> String:
	return NOMS_METEO.get(meteo_actuelle, "")

# Obtenir la teinte météo
func get_teinte_meteo() -> Color:
	return TEINTES_METEO.get(meteo_actuelle, TEINTES_METEO[Meteo.AUCUNE])

# Créer l'overlay météo sur une scène (précipitations visuelles)
func creer_overlay_meteo(parent: Node2D) -> void:
	supprimer_overlay()
	if meteo_actuelle == Meteo.AUCUNE:
		return
	_overlay = CanvasLayer.new()
	_overlay.layer = 55  # Entre les entités et le HUD
	_overlay.name = "WeatherOverlay"
	parent.add_child(_overlay)
	match meteo_actuelle:
		Meteo.PLUIE:
			_creer_pluie()
		Meteo.NEIGE:
			_creer_neige()
		Meteo.TEMPETE_SABLE:
			_creer_sable()
		Meteo.SOLEIL:
			_creer_soleil()
	set_process(true)

# Supprimer l'overlay météo existant
func supprimer_overlay() -> void:
	set_process(false)
	_particules_pluie.clear()
	_particules_neige.clear()
	if _overlay and is_instance_valid(_overlay):
		_overlay.queue_free()
	_overlay = null
	_overlay_teinte = null

# --- Effets de particules ---

func _creer_pluie() -> void:
	if not _overlay:
		return
	# Teinte bleutée
	_overlay_teinte = ColorRect.new()
	_overlay_teinte.color = Color(0.3, 0.35, 0.5, 0.1)
	_overlay_teinte.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_overlay_teinte.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_overlay.add_child(_overlay_teinte)
	# Gouttes de pluie (labels avec caractère |)
	for i in range(30):
		var goutte := Label.new()
		goutte.text = "|"
		goutte.add_theme_font_size_override("font_size", 8)
		goutte.add_theme_color_override("font_color", Color(0.6, 0.7, 0.9, 0.5))
		goutte.position = Vector2(randf() * 480, randf() * 320)
		goutte.rotation = 0.15  # Légère inclinaison pour la pluie
		_overlay.add_child(goutte)
		_particules_pluie.append(goutte)

func _creer_neige() -> void:
	if not _overlay:
		return
	_overlay_teinte = ColorRect.new()
	_overlay_teinte.color = Color(0.8, 0.85, 0.95, 0.08)
	_overlay_teinte.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_overlay_teinte.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_overlay.add_child(_overlay_teinte)
	# Flocons de neige
	for i in range(20):
		var flocon := Label.new()
		flocon.text = "•"
		flocon.add_theme_font_size_override("font_size", randi_range(6, 12))
		flocon.add_theme_color_override("font_color", Color(1, 1, 1, 0.6))
		flocon.position = Vector2(randf() * 480, randf() * 320)
		_overlay.add_child(flocon)
		_particules_neige.append(flocon)

func _creer_sable() -> void:
	if not _overlay:
		return
	_overlay_teinte = ColorRect.new()
	_overlay_teinte.color = Color(0.7, 0.6, 0.3, 0.15)
	_overlay_teinte.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_overlay_teinte.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_overlay.add_child(_overlay_teinte)
	# Grains de sable
	for i in range(25):
		var grain := Label.new()
		grain.text = "·"
		grain.add_theme_font_size_override("font_size", randi_range(6, 10))
		grain.add_theme_color_override("font_color", Color(0.9, 0.8, 0.5, 0.5))
		grain.position = Vector2(randf() * 480, randf() * 320)
		_overlay.add_child(grain)
		_particules_pluie.append(grain)  # Réutiliser le tableau pour l'animation

func _creer_soleil() -> void:
	if not _overlay:
		return
	_overlay_teinte = ColorRect.new()
	_overlay_teinte.color = Color(1.0, 0.95, 0.7, 0.08)
	_overlay_teinte.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_overlay_teinte.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_overlay.add_child(_overlay_teinte)

# --- Animation des particules ---
func _process(delta: float) -> void:
	match meteo_actuelle:
		Meteo.PLUIE:
			_animer_pluie(delta)
		Meteo.NEIGE:
			_animer_neige(delta)
		Meteo.TEMPETE_SABLE:
			_animer_sable(delta)

func _animer_pluie(delta: float) -> void:
	for goutte in _particules_pluie:
		if not is_instance_valid(goutte):
			continue
		goutte.position.y += 280 * delta
		goutte.position.x += 40 * delta
		if goutte.position.y > 330:
			goutte.position.y = -10
			goutte.position.x = randf() * 480

func _animer_neige(delta: float) -> void:
	for flocon in _particules_neige:
		if not is_instance_valid(flocon):
			continue
		flocon.position.y += 30 * delta
		flocon.position.x += sin(flocon.position.y * 0.02) * 20 * delta
		if flocon.position.y > 330:
			flocon.position.y = -10
			flocon.position.x = randf() * 480

func _animer_sable(delta: float) -> void:
	for grain in _particules_pluie:
		if not is_instance_valid(grain):
			continue
		grain.position.x += 200 * delta
		grain.position.y += 30 * delta
		if grain.position.x > 490 or grain.position.y > 330:
			grain.position.x = -10
			grain.position.y = randf() * 320

# Modificateur de rencontre selon la météo
# Pluie : +10%, Tempête : -20%
func get_modificateur_rencontre() -> float:
	match meteo_actuelle:
		Meteo.PLUIE:
			return 1.1
		Meteo.TEMPETE_SABLE:
			return 0.8
	return 1.0
