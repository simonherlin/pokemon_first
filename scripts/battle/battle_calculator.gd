extends Node

# BattleCalculator — Calculs de combat Gen 1
# Dégâts, critiques, précision, efficacité des types, capture

const CHEMIN_TYPE_CHART := "res://data/type_chart.json"

var _type_chart: Dictionary = {}
var _charge: bool = false

func _ready() -> void:
	_charger_type_chart()

func _charger_type_chart() -> void:
	if _charge:
		return
	if not FileAccess.file_exists(CHEMIN_TYPE_CHART):
		push_error("BattleCalculator: type_chart.json introuvable")
		return
	var fichier := FileAccess.open(CHEMIN_TYPE_CHART, FileAccess.READ)
	var data = JSON.parse_string(fichier.get_as_text())
	fichier.close()
	if data == null:
		push_error("BattleCalculator: type_chart.json invalide")
		return
	_type_chart = data
	_charge = true

# ----------------------------------------------------------------
# Formule de dégâts officielle Génération I
# ----------------------------------------------------------------
func calculer_degats(attaquant: Pokemon, defenseur: Pokemon, attaque: Dictionary) -> int:
	var puissance: int = attaque.get("puissance", 0)
	if puissance <= 0:
		return 0

	var level := attaquant.niveau
	var categorie: String = attaque.get("categorie", "physique")
	var atk: int
	var def_val: int

	if categorie == "physique":
		atk = attaquant.get_stat_combat("attaque")
		def_val = defenseur.get_stat_combat("defense")
	else:
		atk = attaquant.get_stat_combat("special")
		def_val = defenseur.get_stat_combat("special")

	# Brûlure divise l'attaque physique par 2
	if attaquant.statut == "brulure" and categorie == "physique":
		atk = maxi(1, atk / 2)

	var stab := 1.5 if attaque.get("type", "normal") in attaquant.types else 1.0
	var type_mult := get_efficacite(attaque.get("type", "normal"), defenseur.types)
	var critique := 1.0
	if _est_critique(attaquant, attaque):
		critique = 2.0
	var aleatoire := randf_range(0.85, 1.0)

	var dmg := int(((2.0 * level / 5.0 + 2.0) * puissance * atk / def_val) / 50.0 + 2.0)
	dmg = int(dmg * stab * type_mult * critique * aleatoire)
	return maxi(1, dmg) if type_mult > 0.0 else 0

# ----------------------------------------------------------------
# Critique (Gen 1 : basé sur vitesse de base)
# ----------------------------------------------------------------
func _est_critique(attaquant: Pokemon, attaque: Dictionary) -> bool:
	# Taux de base Gen 1 = vitesse_base / 512 (environ)
	var vitesse_base: int = int(attaquant.stats_base.get("vitesse", 50))
	var taux: float = vitesse_base / 512.0
	# Attaque à fort taux de critique (ex: Tranche) : ×8
	if attaque.get("effet", {}) != null:
		var effet: Dictionary = attaque.get("effet", {})
		if effet.get("type_effet", "") == "critique_eleve":
			taux *= 8.0
	return randf() < taux

# ----------------------------------------------------------------
# Efficacité des types
# ----------------------------------------------------------------
func get_efficacite(type_attaque: String, types_defenseur: Array) -> float:
	if not _charge:
		_charger_type_chart()
	var mult := 1.0
	for type_def in types_defenseur:
		var ligne: Dictionary = _type_chart.get(type_attaque, {})
		mult *= ligne.get(type_def, 1.0)
	return mult

# Message d'efficacité
func message_efficacite(mult: float) -> String:
	if mult == 0.0:
		return "Ça n'affecte pas..."
	elif mult < 1.0:
		return "Ce n'est pas très efficace..."
	elif mult > 1.0:
		return "C'est super efficace !"
	return ""

# ----------------------------------------------------------------
# Vérification de toucher (précision)
# ----------------------------------------------------------------
func attaque_touche(attaquant: Pokemon, defenseur: Pokemon, attaque: Dictionary) -> bool:
	var precision: int = attaque.get("precision", 100)
	if precision == 0:
		return true  # Attaque qui touche toujours (ex: Tranche Nuit)
	var modif_precision: int = int(attaquant.modificateurs_stats.get("precision", 0))
	var modif_esquive: int = int(defenseur.modificateurs_stats.get("esquive", 0))
	var etape_finale := clampi(modif_precision - modif_esquive, -6, 6)
	var multiplicateurs := [
		33.0/100, 36.0/100, 43.0/100, 50.0/100, 60.0/100, 75.0/100,
		1.0,
		133.0/100, 166.0/100, 200.0/100, 250.0/100, 233.0/100, 300.0/100
	]
	var index := clampi(etape_finale + 6, 0, 12)
	var taux_final: float = float(precision) * float(multiplicateurs[index]) / 100.0
	return randf() < taux_final

# ----------------------------------------------------------------
# Formule de capture Gen 1
# ----------------------------------------------------------------
func calculer_capture(pokemon_sauvage: Pokemon, ball_mult: float) -> Dictionary:
	var taux_capture_espece: int = 45  # Valeur par défaut
	# À récupérer depuis SpeciesData si disponible
	var espece_data := SpeciesData.get_espece(pokemon_sauvage.espece_id)
	taux_capture_espece = espece_data.get("taux_capture", 45)

	# Formule Gen 1 simplifiée
	var pv_max := float(pokemon_sauvage.pv_max)
	var pv_actuels := float(pokemon_sauvage.pv_actuels)
	var statut_bonus := 1.0
	match pokemon_sauvage.statut:
		"sommeil", "gel":
			statut_bonus = 2.0
		"poison", "brulure", "paralysie", "poison_grave":
			statut_bonus = 1.5

	var taux := int((3.0 * pv_max - 2.0 * pv_actuels) * taux_capture_espece * ball_mult * statut_bonus / (3.0 * pv_max))
	taux = clampi(taux, 0, 255)

	# 4 tests de secousse de la Ball — compter les secousses réussies
	var nb_secousses := 0
	for _i in range(4):
		if randi() % 256 >= taux:
			return {"succes": false, "nb_secousses": nb_secousses}
		nb_secousses += 1
	return {"succes": true, "nb_secousses": 3}

# Obtenir le taux de capture brut d'un Pokémon (pour l'indicateur)
func get_taux_capture(espece_id: String) -> int:
	var espece_data := SpeciesData.get_espece(espece_id)
	return espece_data.get("taux_capture", 45)

# Calcul de l'EXP gagnée après un combat
func calculer_exp_gagne(pokemon_vaincu: Pokemon, sauvage: bool) -> int:
	var espece_data := SpeciesData.get_espece(pokemon_vaincu.espece_id)
	var exp_base: int = espece_data.get("exp_base", 64)
	var a: float = 1.0 if sauvage else 1.5
	return maxi(1, int(a * exp_base * pokemon_vaincu.niveau / 7.0))
