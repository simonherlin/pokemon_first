extends Node

# AudioManager — Singleton global
# Lecture musique (avec crossfade) et effets sonores (SFX)

# --- Constantes ---
const VOLUME_MUSIQUE_DEFAUT := 0.8
const VOLUME_SFX_DEFAUT := 1.0
const DUREE_CROSSFADE := 1.0  # secondes

# --- Nœuds audio ---
var _joueur_musique_a: AudioStreamPlayer = null
var _joueur_musique_b: AudioStreamPlayer = null
var _joueur_actif: AudioStreamPlayer = null  # Lequel joue en ce moment
var _joueurs_sfx: Array[AudioStreamPlayer] = []
const NB_CANAUX_SFX := 4  # Nombre de canaux SFX simultanés

# --- État ---
var _musique_actuelle: String = ""
var _volume_musique: float = VOLUME_MUSIQUE_DEFAUT
var _volume_sfx: float = VOLUME_SFX_DEFAUT
var _muet: bool = false
var _tween: Tween = null

# --- Cache des ressources audio ---
var _cache_audio: Dictionary = {}

# Seuil de silence en dB — évite -INF et NaN lors des tweens
const SILENCE_DB := -80.0

# Conversion linéaire → dB sécurisée (0.0 → -80 dB au lieu de -INF)
static func _linear_to_db_safe(linear: float) -> float:
	if linear <= 0.0:
		return SILENCE_DB
	return linear_to_db(linear)

func _ready() -> void:
	# Créer les bus audio s'ils n'existent pas
	_assurer_bus("Musique")
	_assurer_bus("SFX")

	_joueur_musique_a = AudioStreamPlayer.new()
	_joueur_musique_a.bus = "Musique"
	add_child(_joueur_musique_a)

	_joueur_musique_b = AudioStreamPlayer.new()
	_joueur_musique_b.bus = "Musique"
	add_child(_joueur_musique_b)

	# Créer plusieurs canaux SFX pour permettre la superposition
	for i in range(NB_CANAUX_SFX):
		var sfx_player := AudioStreamPlayer.new()
		sfx_player.bus = "SFX"
		add_child(sfx_player)
		_joueurs_sfx.append(sfx_player)

	_joueur_actif = _joueur_musique_a

func _assurer_bus(nom_bus: String) -> void:
	if AudioServer.get_bus_index(nom_bus) == -1:
		var idx := AudioServer.bus_count
		AudioServer.add_bus(idx)
		AudioServer.set_bus_name(idx, nom_bus)

# Jouer une musique (avec crossfade si une autre joue déjà)
func jouer_musique(chemin: String, boucle: bool = true) -> void:
	if chemin == _musique_actuelle:
		return
	if chemin.is_empty():
		arreter_musique()
		return

	var stream = _charger_audio(chemin)
	if stream == null:
		return

	_musique_actuelle = chemin

	var nouveau_joueur := _joueur_musique_b if _joueur_actif == _joueur_musique_a else _joueur_musique_a
	nouveau_joueur.stream = stream
	nouveau_joueur.volume_db = SILENCE_DB

	if stream is AudioStreamOggVorbis:
		stream.loop = boucle
	elif stream is AudioStreamMP3:
		stream.loop = boucle

	nouveau_joueur.play()

	# Crossfade
	if _tween:
		_tween.kill()
	_tween = create_tween()
	_tween.set_parallel(true)
	_tween.tween_property(_joueur_actif, "volume_db", SILENCE_DB, DUREE_CROSSFADE)
	_tween.tween_property(nouveau_joueur, "volume_db", _linear_to_db_safe(_volume_musique), DUREE_CROSSFADE)
	_tween.set_parallel(false)
	_tween.tween_callback(func(): _joueur_actif.stop())

	_joueur_actif = nouveau_joueur

func arreter_musique() -> void:
	_musique_actuelle = ""
	_joueur_musique_a.stop()
	_joueur_musique_b.stop()

func pausemusique(en_pause: bool) -> void:
	_joueur_actif.stream_paused = en_pause

# Jouer un effet sonore (utilise le premier canal libre)
func jouer_sfx(chemin: String) -> void:
	if _muet:
		return
	var stream = _charger_audio(chemin)
	if stream == null:
		return
	# Trouver un canal SFX libre
	var joueur: AudioStreamPlayer = null
	for sfx_player in _joueurs_sfx:
		if not sfx_player.playing:
			joueur = sfx_player
			break
	# Si aucun canal libre, utiliser le premier (le plus ancien)
	if joueur == null:
		joueur = _joueurs_sfx[0]
	joueur.stream = stream
	joueur.volume_db = _linear_to_db_safe(_volume_sfx)
	joueur.play()

# Charger et mettre en cache un fichier audio
func _charger_audio(chemin: String) -> AudioStream:
	if chemin in _cache_audio:
		return _cache_audio[chemin]
	if not ResourceLoader.exists(chemin):
		push_warning("AudioManager: fichier audio introuvable: %s" % chemin)
		return null
	var stream = load(chemin) as AudioStream
	_cache_audio[chemin] = stream
	return stream

# Réglage du volume musique (0.0 - 1.0)
func set_volume_musique(volume: float) -> void:
	_volume_musique = clamp(volume, 0.0, 1.0)
	_joueur_actif.volume_db = _linear_to_db_safe(_volume_musique)

# Réglage du volume SFX (0.0 - 1.0)
func set_volume_sfx(volume: float) -> void:
	_volume_sfx = clamp(volume, 0.0, 1.0)

func set_muet(actif: bool) -> void:
	_muet = actif
	AudioServer.set_bus_mute(AudioServer.get_bus_index("Musique"), actif)
	AudioServer.set_bus_mute(AudioServer.get_bus_index("SFX"), actif)
