extends RefCounted
class_name Pokemon

# Pokemon — Représente un Pokémon en jeu (instance, pas une espèce)
# Contient toutes les données d'un Pokémon individuel de l'équipe

# --- Constantes ---
const MAX_ATTAQUES := 4
const NIVEAU_MAX := 100
const GROUPES_EXP := {
	"rapide":       func(n): return int(4.0 * pow(n, 3) / 5.0),
	"moyen_rapide": func(n): return int(pow(n, 3)),
	"lent_moyen":   func(n): return int(6.0 * pow(n, 3) / 5.0 - 15 * pow(n, 2) + 100 * n - 140),
	"lent":         func(n): return int(5.0 * pow(n, 3) / 4.0)
}

# --- Identité ---
var espece_id: String = ""             # ex: "001"
var surnom: String = ""                # modifiable par le joueur
var id_combat: int = 0                 # ID unique pour identifier en combat
var id_dresseur: int = 0               # ID du dresseur original (0 = joueur)

# --- Niveau et EXP ---
var niveau: int = 1
var exp: int = 0
var groupe_exp: String = "moyen_rapide"

# --- PV ---
var pv_actuels: int = 0
var pv_max: int = 0                    # calculé depuis stats

# --- Stats calculées ---
var stats: Dictionary = {
	"pv": 0, "attaque": 0, "defense": 0,
	"special": 0, "vitesse": 0
}

# --- Modificateurs de stats en combat (remis à zéro hors combat) ---
var modificateurs_stats: Dictionary = {
	"attaque": 0, "defense": 0,
	"special": 0, "vitesse": 0, "esquive": 0, "precision": 0
}

# --- Attaques (max 4) ---
# Chaque attaque: {"id": "charge", "pp_actuels": 35, "pp_max": 35}
var attaques: Array = []

# --- Statut ---
var statut: String = ""                # "", "brulure", "gel", "paralysie", "poison", "poison_grave", "sommeil"
var tours_sommeil: int = 0             # compteur tours de sommeil restants
var compteur_poison_grave: int = 0     # multiplicateur dégâts poison grave

# --- Données espèce (chargées depuis SpeciesData) ---
var stats_base: Dictionary = {}
var types: Array = []
var nom_espece: String = ""

# --- Initialisation depuis données espèce ---
func initialiser(espece_data: Dictionary, niv: int) -> void:
	espece_id = str(espece_data.get("id", 1)).lpad(3, "0")
	nom_espece = espece_data.get("nom", "???")
	surnom = nom_espece
	groupe_exp = espece_data.get("groupe_exp", "moyen_rapide")
	types = espece_data.get("types", ["normal"])
	stats_base = espece_data.get("stats_base", {})
	niveau = clampi(niv, 1, NIVEAU_MAX)
	exp = _exp_pour_niveau(niveau)
	id_combat = randi() % 65536

	_calculer_stats()
	pv_actuels = pv_max

	# Apprendre les attaques disponibles au niveau donné
	var learnset: Dictionary = espece_data.get("learnset", {})
	var attaques_apprises := []
	for niveau_str in learnset:
		if int(niveau_str) <= niveau:
			for move_id in learnset[niveau_str]:
				if not move_id in attaques_apprises:
					attaques_apprises.append(move_id)

	# Garder uniquement les 4 dernières
	var dernieres := attaques_apprises.slice(max(0, attaques_apprises.size() - MAX_ATTAQUES))
	for move_id in dernieres:
		var move_data = MoveData.get_move(move_id)
		if move_data:
			attaques.append({
				"id": move_id,
				"pp_actuels": move_data.get("pp", 10),
				"pp_max": move_data.get("pp", 10)
			})

# Calculer les stats depuis les stats de base et le niveau (formule Gen 1)
func _calculer_stats() -> void:
	for stat_nom in ["pv", "attaque", "defense", "special", "vitesse"]:
		var base: int = stats_base.get(stat_nom, 50)
		var stat_calc: int
		if stat_nom == "pv":
			stat_calc = int((base * 2.0 * niveau) / 100.0) + niveau + 10
		else:
			stat_calc = int((base * 2.0 * niveau) / 100.0) + 5
		stats[stat_nom] = stat_calc
	pv_max = stats["pv"]

# Obtenir la stat en combat (avec modificateurs)
func get_stat_combat(stat_nom: String) -> int:
	var valeur_base := stats.get(stat_nom, 1)
	var modif := modificateurs_stats.get(stat_nom, 0)
	return _appliquer_modificateur(valeur_base, modif)

# Table des multiplicateurs Gen 1 (-6 à +6)
func _appliquer_modificateur(valeur: int, etape: int) -> int:
	var multi := [2.0/8, 2.0/7, 2.0/6, 2.0/5, 2.0/4, 2.0/3,
				  1.0,
				  3.0/2, 4.0/2, 5.0/2, 6.0/2, 7.0/2, 8.0/2]
	var index := clampi(etape + 6, 0, 12)
	return maxi(1, int(valeur * multi[index]))

# Modifier un modificateur de stat en combat
func modifier_stat(stat_nom: String, etapes: int) -> int:
	# Retourne le changement réel appliqué
	var avant := modificateurs_stats.get(stat_nom, 0)
	var apres := clampi(avant + etapes, -6, 6)
	modificateurs_stats[stat_nom] = apres
	return apres - avant

func reinitialiser_modificateurs() -> void:
	for stat in modificateurs_stats:
		modificateurs_stats[stat] = 0

# Infliger des dégâts
func infliger_degats(degats: int) -> void:
	pv_actuels = maxi(0, pv_actuels - degats)

# Soigner des PV
func soigner(montant: int) -> void:
	pv_actuels = mini(pv_max, pv_actuels + montant)

func soigner_complet() -> void:
	pv_actuels = pv_max
	statut = ""
	tours_sommeil = 0
	compteur_poison_grave = 0

func est_ko() -> bool:
	return pv_actuels <= 0

# Gestion statuts
func appliquer_statut(nouveau_statut: String) -> bool:
	if not statut.is_empty():
		return false  # Déjà un statut
	statut = nouveau_statut
	if nouveau_statut == "sommeil":
		tours_sommeil = randi_range(1, 7)
	return true

func guerir_statut() -> void:
	statut = ""
	tours_sommeil = 0
	compteur_poison_grave = 0

# Calculer les dégâts de statut en fin de tour
func degats_statut_fin_tour() -> int:
	match statut:
		"brulure":
			return maxi(1, pv_max / 16)
		"poison":
			return maxi(1, pv_max / 16)
		"poison_grave":
			compteur_poison_grave += 1
			return maxi(1, pv_max * compteur_poison_grave / 16)
	return 0

# Utiliser les PP d'une attaque
func utiliser_pp(index_attaque: int) -> void:
	if index_attaque < 0 or index_attaque >= attaques.size():
		return
	attaques[index_attaque]["pp_actuels"] = maxi(0, attaques[index_attaque]["pp_actuels"] - 1)

# Apprendre une nouvelle attaque (remplace si 4 déjà)
func apprendre_attaque(move_id: String, remplacer_index: int = -1) -> bool:
	var move_data = MoveData.get_move(move_id)
	if move_data == null:
		return false
	var nouvelle_attaque := {
		"id": move_id,
		"pp_actuels": move_data.get("pp", 10),
		"pp_max": move_data.get("pp", 10)
	}
	if attaques.size() < MAX_ATTAQUES:
		attaques.append(nouvelle_attaque)
		return true
	if remplacer_index >= 0 and remplacer_index < MAX_ATTAQUES:
		attaques[remplacer_index] = nouvelle_attaque
		return true
	return false

# Gagner de l'expérience et monter de niveau si nécessaire
# Retourne la liste des niveaux gagnés
func gagner_exp(montant: int) -> Array[int]:
	exp += montant
	var niveaux_gagnes: Array[int] = []
	while niveau < NIVEAU_MAX and exp >= _exp_pour_niveau(niveau + 1):
		niveau += 1
		niveaux_gagnes.append(niveau)
		var ancien_pv_max := pv_max
		_calculer_stats()
		# Bonus PV lors du level up
		pv_actuels += pv_max - ancien_pv_max
	return niveaux_gagnes

# Attaques apprenables au niveau actuel (pour affichage)
func attaques_a_apprendre(espece_data: Dictionary) -> Array[String]:
	var learnset: Dictionary = espece_data.get("learnset", {})
	var a_apprendre: Array[String] = []
	for niveau_str in learnset:
		if int(niveau_str) == niveau:
			for move_id in learnset[niveau_str]:
				a_apprendre.append(move_id)
	return a_apprendre

# EXP nécessaire pour atteindre un niveau
func _exp_pour_niveau(niv: int) -> int:
	if niv <= 1:
		return 0
	if groupe_exp in GROUPES_EXP:
		return GROUPES_EXP[groupe_exp].call(niv)
	return int(pow(niv, 3))

# EXP gagnée à la défaite de ce Pokémon (Gen 1)
func exp_a_la_mort(sauvage: bool) -> int:
	var exp_base: int = 64  # valeur par défaut
	# À récupérer depuis SpeciesData si besoin
	var a := 1 if sauvage else 1.5
	return int(a * exp_base * niveau / 7.0)

# Sérialisation pour sauvegarde
func to_dict() -> Dictionary:
	return {
		"espece_id": espece_id,
		"surnom": surnom,
		"id_combat": id_combat,
		"id_dresseur": id_dresseur,
		"niveau": niveau,
		"exp": exp,
		"groupe_exp": groupe_exp,
		"pv_actuels": pv_actuels,
		"stats": stats,
		"stats_base": stats_base,
		"types": types,
		"nom_espece": nom_espece,
		"attaques": attaques,
		"statut": statut,
		"tours_sommeil": tours_sommeil,
		"compteur_poison_grave": compteur_poison_grave
	}

# Désérialisation depuis sauvegarde
static func from_dict(data: Dictionary) -> Pokemon:
	var p := Pokemon.new()
	p.espece_id = data.get("espece_id", "001")
	p.surnom = data.get("surnom", "???")
	p.id_combat = data.get("id_combat", 0)
	p.id_dresseur = data.get("id_dresseur", 0)
	p.niveau = data.get("niveau", 1)
	p.exp = data.get("exp", 0)
	p.groupe_exp = data.get("groupe_exp", "moyen_rapide")
	p.pv_actuels = data.get("pv_actuels", 1)
	p.stats = data.get("stats", {})
	p.stats_base = data.get("stats_base", {})
	p.types = data.get("types", ["normal"])
	p.nom_espece = data.get("nom_espece", "???")
	p.attaques = data.get("attaques", [])
	p.statut = data.get("statut", "")
	p.tours_sommeil = data.get("tours_sommeil", 0)
	p.compteur_poison_grave = data.get("compteur_poison_grave", 0)
	p.pv_max = p.stats.get("pv", 1)
	return p
