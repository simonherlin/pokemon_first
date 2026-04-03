extends Node

# MoveEffects — Gestion des effets secondaires des attaques
# Statuts, modifications de stats, effets spéciaux Gen 1

# Appliquer l'effet d'une attaque après calcul des dégâts
# Retourne un dictionnaire décrivant ce qui s'est passé
func appliquer_effet(attaquant: Pokemon, defenseur: Pokemon, attaque: Dictionary) -> Dictionary:
	var effet_raw = attaque.get("effet", null)
	var resultat := {"message": "", "statut_applique": "", "stat_modifiee": ""}

	if effet_raw == null or not (effet_raw is Dictionary):
		return resultat
	var effet: Dictionary = effet_raw

	if effet.is_empty():
		return resultat

	var type_effet: String = effet.get("type_effet", "")
	var chance: float = effet.get("chance", 1.0)

	# Vérification probabiliste
	if randf() > chance:
		return resultat

	match type_effet:
		"infliger_statut":
			var statut_cible: String = effet.get("statut", "")
			if statut_cible.is_empty():
				return resultat
			# Immunités de type
			if _immune_statut(defenseur, statut_cible):
				resultat["message"] = _message_immunite(statut_cible)
				return resultat
			if defenseur.appliquer_statut(statut_cible):
				resultat["statut_applique"] = statut_cible
				resultat["message"] = _message_statut_applique(defenseur, statut_cible)

		"modifier_stat_ennemi":
			var stat: String = effet.get("stat", "")
			var etapes: int = effet.get("etapes", -1)
			var change := defenseur.modifier_stat(stat, etapes)
			resultat["stat_modifiee"] = stat
			resultat["message"] = _message_modif_stat(defenseur, stat, change, etapes)

		"modifier_stat_soi":
			var stat: String = effet.get("stat", "")
			var etapes: int = effet.get("etapes", 1)
			var change := attaquant.modifier_stat(stat, etapes)
			resultat["stat_modifiee"] = stat
			resultat["message"] = _message_modif_stat(attaquant, stat, change, etapes)

		"soin":
			var pourcentage: float = effet.get("pourcentage", 0.5)
			var soin := maxi(1, int(attaquant.pv_max * pourcentage))
			attaquant.soigner(soin)
			resultat["message"] = "%s récupère %d PV !" % [attaquant.surnom, soin]

		"confusion":
			# Non implémenté en MVP — placeholder
			resultat["message"] = ""

		"critique_eleve":
			pass  # Géré dans BattleCalculator

	return resultat

# Vérifier l'immunité d'un Pokémon à un statut
func _immune_statut(pokemon: Pokemon, statut: String) -> bool:
	match statut:
		"brulure":
			return "feu" in pokemon.types
		"gel":
			return "glace" in pokemon.types
		"paralysie":
			return "electrik" in pokemon.types
		"poison", "poison_grave":
			return "poison" in pokemon.types or "acier" in pokemon.types
	return false

# Messages d'application de statut
func _message_statut_applique(pokemon: Pokemon, statut: String) -> String:
	match statut:
		"brulure":
			return "%s est brûlé !" % pokemon.surnom
		"gel":
			return "%s est gelé !" % pokemon.surnom
		"paralysie":
			return "%s est paralysé !" % pokemon.surnom
		"poison":
			return "%s est empoisonné !" % pokemon.surnom
		"poison_grave":
			return "%s est gravement empoisonné !" % pokemon.surnom
		"sommeil":
			return "%s s'endort !" % pokemon.surnom
	return ""

func _message_immunite(statut: String) -> String:
	match statut:
		"brulure":
			return "Ça n'affecte pas les types Feu !"
		"gel":
			return "Ça n'affecte pas les types Glace !"
		"paralysie":
			return "Ça n'affecte pas les types Électrique !"
		"poison", "poison_grave":
			return "Ça n'affecte pas les types Poison !"
	return ""

# Message de modification de stat
# etapes_visees indique la direction souhaitée (>0 hausse, <0 baisse)
func _message_modif_stat(pokemon: Pokemon, stat: String, changement: int, etapes_visees: int = 0) -> String:
	var noms_stats := {
		"attaque": "l'Attaque", "defense": "la Défense",
		"special": "le Spécial", "vitesse": "la Vitesse",
		"precision": "la Précision", "esquive": "l'Esquive"
	}
	var nom_stat: String = noms_stats.get(stat, stat)
	if changement == 0:
		if etapes_visees > 0:
			return "%s de %s ne peut plus monter !" % [nom_stat, pokemon.surnom]
		else:
			return "%s de %s ne peut plus baisser !" % [nom_stat, pokemon.surnom]
	if changement > 0:
		match changement:
			1: return "%s de %s monte !" % [nom_stat, pokemon.surnom]
			2: return "%s de %s monte fortement !" % [nom_stat, pokemon.surnom]
			_: return "%s de %s monte au maximum !" % [nom_stat, pokemon.surnom]
	else:
		match changement:
			-1: return "%s de %s baisse !" % [nom_stat, pokemon.surnom]
			-2: return "%s de %s baisse fortement !" % [nom_stat, pokemon.surnom]
			_: return "%s de %s baisse au minimum !" % [nom_stat, pokemon.surnom]

# Appliquer les dégâts de statut en fin de tour
# Retourne le message correspondant
func appliquer_degats_fin_tour(pokemon: Pokemon) -> String:
	if pokemon.statut.is_empty() or pokemon.est_ko():
		return ""
	var degats := pokemon.degats_statut_fin_tour()
	if degats <= 0:
		return ""
	pokemon.infliger_degats(degats)
	match pokemon.statut:
		"brulure":
			return "%s souffre de sa brûlure !" % pokemon.surnom
		"poison", "poison_grave":
			return "%s souffre du poison !" % pokemon.surnom
	return ""

# Vérifier si un Pokémon peut agir ce tour (paralysie, sommeil, gel)
# Retourne le message si incapable d'agir, "" si peut agir
func verifier_statut_avant_action(pokemon: Pokemon) -> String:
	match pokemon.statut:
		"sommeil":
			if pokemon.tours_sommeil > 0:
				pokemon.tours_sommeil -= 1
				if pokemon.tours_sommeil == 0:
					pokemon.statut = ""
					return "%s se réveille !" % pokemon.surnom
				return "%s est endormi !" % pokemon.surnom
		"gel":
			if randf() < 0.25:  # 25% de chance de se dégeler chaque tour
				pokemon.statut = ""
				return "%s n'est plus gelé !" % pokemon.surnom
			return "%s est gelé, il ne peut pas attaquer !" % pokemon.surnom
		"paralysie":
			if randf() < 0.25:  # 25% de chance de ne pas agir
				return "%s est paralysé ! Il ne peut pas attaquer !" % pokemon.surnom
	return ""
