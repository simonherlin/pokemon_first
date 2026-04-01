extends Node

# QuestManager — Singleton de gestion des quêtes
# Charge les quêtes depuis data/quetes.json et détermine leur état
# à partir des flags de GameManager (aucun état supplémentaire à sauvegarder)

# --- Types d'état de quête ---
enum EtatQuete { VERROUILLEE, ACTIVE, TERMINEE }

# --- Données chargées depuis JSON ---
var _quetes_principales: Array = []
var _quetes_secondaires: Array = []
var _toutes_quetes: Dictionary = {}  # id → données de la quête

# --- Signal émis quand une quête change d'état ---
signal quete_mise_a_jour(quete_id: String, nouvel_etat: int)
signal quete_terminee(quete_id: String)

func _ready() -> void:
	_charger_quetes()
	# Écouter les changements de flags pour mettre à jour les quêtes
	if GameManager.flag_modifie.is_connected(_on_flag_modifie):
		return
	GameManager.flag_modifie.connect(_on_flag_modifie)

# Charger les quêtes depuis le fichier JSON
func _charger_quetes() -> void:
	var fichier := FileAccess.open("res://data/quetes.json", FileAccess.READ)
	if not fichier:
		push_error("QuestManager: impossible de charger data/quetes.json")
		return
	var json := JSON.new()
	var err := json.parse(fichier.get_as_text())
	fichier.close()
	if err != OK:
		push_error("QuestManager: erreur de parsing JSON — %s" % json.get_error_message())
		return
	var data: Dictionary = json.data
	_quetes_principales = data.get("principales", [])
	_quetes_secondaires = data.get("secondaires", [])
	# Indexer par ID
	for q in _quetes_principales:
		_toutes_quetes[q["id"]] = q
		q["categorie"] = "principale"
	for q in _quetes_secondaires:
		_toutes_quetes[q["id"]] = q
		q["categorie"] = "secondaire"

# --- Accès public ---

# Obtenir l'état d'une quête par son ID
func get_etat(quete_id: String) -> int:
	if not _toutes_quetes.has(quete_id):
		return EtatQuete.VERROUILLEE
	var q: Dictionary = _toutes_quetes[quete_id]
	# Vérifier le prérequis
	if not _prerequis_rempli(q):
		return EtatQuete.VERROUILLEE
	# Vérifier si toutes les étapes sont terminées
	if _toutes_etapes_terminees(q):
		return EtatQuete.TERMINEE
	return EtatQuete.ACTIVE

# Obtenir la progression d'une quête (étapes terminées / total)
func get_progression(quete_id: String) -> Dictionary:
	if not _toutes_quetes.has(quete_id):
		return {"terminees": 0, "total": 0}
	var q: Dictionary = _toutes_quetes[quete_id]
	var etapes: Array = q.get("etapes", [])
	var terminees := 0
	for etape in etapes:
		if _etape_terminee(etape):
			terminees += 1
	return {"terminees": terminees, "total": etapes.size()}

# Obtenir les détails d'une quête enrichis avec l'état et la progression
func get_quete_details(quete_id: String) -> Dictionary:
	if not _toutes_quetes.has(quete_id):
		return {}
	var q: Dictionary = _toutes_quetes[quete_id].duplicate(true)
	q["etat"] = get_etat(quete_id)
	var prog := get_progression(quete_id)
	q["etapes_terminees"] = prog.terminees
	q["etapes_total"] = prog.total
	# Enrichir chaque étape avec son statut
	for i in range(q["etapes"].size()):
		q["etapes"][i]["terminee"] = _etape_terminee(q["etapes"][i])
	return q

# Obtenir toutes les quêtes principales avec leur état
func get_quetes_principales() -> Array:
	var resultat := []
	for q in _quetes_principales:
		resultat.append(get_quete_details(q["id"]))
	return resultat

# Obtenir toutes les quêtes secondaires avec leur état
func get_quetes_secondaires() -> Array:
	var resultat := []
	for q in _quetes_secondaires:
		resultat.append(get_quete_details(q["id"]))
	return resultat

# Obtenir les quêtes actives (non terminées, non verrouillées)
func get_quetes_actives() -> Array:
	var resultat := []
	for id in _toutes_quetes.keys():
		if get_etat(id) == EtatQuete.ACTIVE:
			resultat.append(get_quete_details(id))
	return resultat

# Obtenir les quêtes terminées
func get_quetes_terminees() -> Array:
	var resultat := []
	for id in _toutes_quetes.keys():
		if get_etat(id) == EtatQuete.TERMINEE:
			resultat.append(get_quete_details(id))
	return resultat

# --- Vérifications internes ---

# Vérifier si le prérequis d'une quête est rempli
func _prerequis_rempli(quete: Dictionary) -> bool:
	var prerequis: String = quete.get("prerequis", "")
	if prerequis.is_empty():
		return true
	var val = GameManager.get_flag(prerequis)
	if val is bool:
		return val
	if val is String:
		return not val.is_empty()
	return val != null

# Vérifier si une étape est terminée
func _etape_terminee(etape: Dictionary) -> bool:
	var flag_cle: String = etape.get("flag", "")
	if flag_cle.is_empty():
		return false
	# Cas spécial : vérification du Pokédex complet
	if flag_cle == "_special_pokedex_complet":
		return PlayerData.pokedex_capture.size() >= 151
	# Cas normal : vérifier le flag dans GameManager
	var val_flag = GameManager.get_flag(flag_cle)
	# Vérification "valeur_non_vide" (pour les flags String comme fossile_choisi)
	if etape.has("valeur_non_vide") and etape["valeur_non_vide"]:
		return val_flag is String and not val_flag.is_empty()
	# Vérification classique avec valeur attendue
	var valeur_attendue = etape.get("valeur", true)
	return val_flag == valeur_attendue

# Vérifier si toutes les étapes d'une quête sont terminées
func _toutes_etapes_terminees(quete: Dictionary) -> bool:
	var etapes: Array = quete.get("etapes", [])
	for etape in etapes:
		if not _etape_terminee(etape):
			return false
	return true

# --- Callback quand un flag change ---
func _on_flag_modifie(_cle: String, _valeur) -> void:
	# Vérifier si des quêtes viennent de se terminer
	for id in _toutes_quetes.keys():
		var ancien_etat := get_etat(id)
		# On ne peut pas comparer directement ancien/nouveau car l'état est dynamique
		# Mais on peut émettre un signal si la quête est maintenant terminée
		if ancien_etat == EtatQuete.TERMINEE:
			continue
		# Recalculer après le changement de flag
		if _toutes_etapes_terminees(_toutes_quetes[id]) and _prerequis_rempli(_toutes_quetes[id]):
			emit_signal("quete_terminee", id)
	# Émettre une mise à jour générale
	emit_signal("quete_mise_a_jour", _cle, 0)
