extends Node

# AIController — Intelligence artificielle des dresseurs et Pokémon sauvages Gen 1
# Logique simple : choisir l'attaque la plus efficace

# Choisir l'index de l'attaque à utiliser pour un Pokémon IA
func choisir_attaque(pokemon: Pokemon, cible: Pokemon) -> int:
	var meilleures: Array = []
	var meilleur_score := -1.0

	for i in range(pokemon.attaques.size()):
		var attaque_ref = pokemon.attaques[i]
		if attaque_ref["pp_actuels"] <= 0:
			continue
		var attaque_data := MoveData.get_move(attaque_ref["id"])
		if attaque_data.is_empty():
			continue

		# Ignorer les attaques sans puissance pour l'IA de base
		var puissance := float(attaque_data.get("puissance", 0))
		if puissance <= 0:
			# Attaques de statut : priorité basse (10% de chance de les utiliser)
			var score_statut := 10.0 if _utile_statut(attaque_data, cible) else 0.0
			if score_statut > meilleur_score:
				meilleur_score = score_statut
				meilleures = [i]
			elif score_statut == meilleur_score:
				meilleures.append(i)
			continue

		var type_attaque: String = attaque_data.get("type", "normal")
		var efficacite := BattleCalculator.get_efficacite(type_attaque, cible.types)

		if efficacite == 0.0:
			continue  # Jamais choisir une attaque inefficace

		# Score = puissance × efficacité × STAB bonus
		var stab := 1.5 if type_attaque in pokemon.types else 1.0
		var score := puissance * efficacite * stab

		if score > meilleur_score:
			meilleur_score = score
			meilleures = [i]
		elif score == meilleur_score:
			meilleures.append(i)

	if meilleures.is_empty():
		# Aucune attaque utilisable → utiliser la première quoi qu'il arrive
		if pokemon.attaques.size() > 0:
			return 0
		return -1

	# Parmi les meilleures, en choisir une aléatoirement
	return meilleures[randi() % meilleures.size()]

# Choisir de changer de Pokémon (retourne l'index dans l'équipe ou -1 si pas de changement)
func choisir_changement(equipe: Array, pokemon_actuel: Pokemon, cible: Pokemon) -> int:
	# IA simple : ne change que si le Pokémon actuel est très désavantagé (x2 de faiblesse)
	var type_cible_principal: String = cible.types[0] if cible.types.size() > 0 else "normal"
	var efficacite_recue := BattleCalculator.get_efficacite(type_cible_principal, pokemon_actuel.types)

	if efficacite_recue < 2.0:
		return -1  # Pas de changement si pas en danger

	# Chercher un Pokémon de remplacement qui résiste à l'adversaire
	var candidats: Array = []
	for i in range(equipe.size()):
		var p_data: Dictionary = equipe[i]
		if p_data.get("pv_actuels", 0) <= 0:
			continue
		if p_data.get("espece_id", "") == pokemon_actuel.espece_id:
			continue
		# Vérifier résistance simple
		candidats.append(i)

	if candidats.is_empty():
		return -1
	return candidats[randi() % candidats.size()]

# Vérifier si une attaque de statut est utile contre la cible
func _utile_statut(attaque_data: Dictionary, cible: Pokemon) -> bool:
	var effet_raw = attaque_data.get("effet", null)
	if effet_raw == null or not (effet_raw is Dictionary):
		return false
	var effet: Dictionary = effet_raw
	if effet.is_empty():
		return false
	var type_effet: String = effet.get("type_effet", "")
	match type_effet:
		"infliger_statut":
			return cible.statut.is_empty()
		"modifier_stat_ennemi":
			return true
	return false
