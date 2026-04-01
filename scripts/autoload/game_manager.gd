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
	"mewtwo_vaincu": false,
	"starter_choisi": "",
	"intro_terminee": false,
	"rival_labo_battu": false,
	"vieil_homme_vu": false,
	"premier_pokemon_recu": false,
	"badge_roche": false,
	"badge_cascade": false,
	"mont_selenite_termine": false,
	"fossile_mont_selenite_pris": false,
	"rival_route24_battu": false,
	"pont_pepite_termine": false,
	"bill_rencontre": false,
	"bill_pc_active": false,
	"ticket_oceane_recu": false,
	"rival_ss_anne_battu": false,
	"ss_anne_termine": false,
	"cs_coupe_obtenu": false,
	"badge_foudre": false,
	"arbre_coupe_route9": false,
	"badge_prisme": false,
	"scope_sylphe_obtenu": false,
	"m_fuji_sauve": false,
	"poke_flute_obtenu": false,
	"tour_pokemon_terminee": false,
	"giovanni_repaire_battu": false,
	"repaire_rocket_termine": false,
	"cle_ascenseur_obtenu": false,
	"evoli_celadopole_recu": false,
	"jeton_casino_recu": false,
	# Sprint 7 — Piste Cyclable, Parmanie, Safari, Routes 12-15, Safrania
	"ronflex_route12_battu": false,
	"ronflex_route16_battu": false,
	"badge_ame": false,
	"parc_safari_visite": false,
	"dent_or_obtenu": false,
	"cs_surf_obtenu": false,
	"cs_force_obtenu": false,
	"cs_vol_obtenu": false,
	"canne_a_peche_obtenu": false,
	"super_canne_obtenu": false,
	"badge_marais": false,
	"dojo_termine": false,
	"tygnon_ou_kicklee_choisi": "",
	"lokhlass_recu": false,
	"master_ball_recue": false,
	"tour_sylphe_terminee": false,
	"giovanni_sylphe_battu": false,
	"rival_sylphe_battu": false,
	"safrania_liberee": false,
	# Sprint 8 — Routes 19-21, Cramois'Île, Îles Écume, Centrale, Jadielle Arène
	"badge_volcan": false,
	"badge_terre": false,
	"cle_arene_cramoisile_obtenu": false,
	"manoir_pokemon_termine": false,
	"fossile_ambre_obtenu": false,
	"artikodin_battu": false,
	"electhor_battu": false,
	"iles_ecume_termine": false,
	"centrale_visite": false,
	"giovanni_arene_battu": false,
	"ptéra_ressuscite": false
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
	for key in flags.keys():
		if flags[key] is bool:
			flags[key] = false
		elif flags[key] is String:
			flags[key] = ""
	temps_jeu_secondes = 0
	partie_en_cours = true
	nom_rival = "Régis"
