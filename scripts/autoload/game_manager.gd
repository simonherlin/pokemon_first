extends Node

# GameManager — Singleton global
# Gère l'état général du jeu : progression, badges, flags de scénario

# --- Constantes ---
const MAX_BADGES := 8
const VERSION_JEU := "0.1.0"

# --- Badges ---
var badges: Array[bool] = [false, false, false, false, false, false, false, false]
# 0=Arène1(Pierre Grise) 1=Arène2(Cascade) 2=Arène3(Foudre) 3=Arène4(Arc-en-ciel)
# 4=Arène5(Âme) 5=Arène6(Carapuce) 6=Arène7(Volcani) 7=Arène8(Viridien)

# --- Flags scénario ---
var flags: Dictionary = {
	"colis_chen_livre": false,
	"pokedex_recu": false,
	"rival_nomme": false,
	"fossile_choisi": "",
	"mewtwo_vaincu": false
}

# --- État de jeu ---
var partie_en_cours: bool = false
var temps_jeu_secondes: int = 0
var _temps_accum: float = 0.0
var nom_rival: String = "Régis"

# --- Signal ---
signal badge_obtenu(index: int)
signal flag_modifie(cle: String, valeur)

func _ready() -> void:
	set_process(true)

func _process(delta: float) -> void:
	if partie_en_cours:
		_temps_accum += delta
		temps_jeu_secondes = int(_temps_accum)

# Accorder un badge (0-7)
func donner_badge(index: int) -> void:
	if index < 0 or index >= MAX_BADGES:
		return
	badges[index] = true
	emit_signal("badge_obtenu", index)

func possede_badge(index: int) -> bool:
	if index < 0 or index >= MAX_BADGES:
		return false
	return badges[index]

func nombre_badges() -> int:
	var count := 0
	for b in badges:
		if b:
			count += 1
	return count

# Lire/écrire un flag de scénario
func set_flag(cle: String, valeur) -> void:
	flags[cle] = valeur
	emit_signal("flag_modifie", cle, valeur)

func get_flag(cle: String):
	return flags.get(cle, null)

# Temps de jeu formaté (HH:MM:SS)
func get_temps_formate() -> String:
	var h := temps_jeu_secondes / 3600
	var m := (temps_jeu_secondes % 3600) / 60
	var s := temps_jeu_secondes % 60
	return "%02d:%02d:%02d" % [h, m, s]

# Réinitialisation pour nouvelle partie
func nouvelle_partie() -> void:
	badges = [false, false, false, false, false, false, false, false]
	flags = {
		"colis_chen_livre": false,
		"pokedex_recu": false,
		"rival_nomme": false,
		"fossile_choisi": "",
		"mewtwo_vaincu": false
	}
	temps_jeu_secondes = 0
	partie_en_cours = true
	nom_rival = "Régis"
