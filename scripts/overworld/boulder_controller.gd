extends StaticBody2D

# BoulderController — Rocher poussable avec CS Force
# Le rocher peut être poussé d'une case dans la direction du joueur

var position_grille: Vector2i = Vector2i.ZERO
var carte_id: String = ""
var rocher_id: String = ""
var _est_pousse: bool = false

const TAILLE_TILE := 32

func initialiser(data: Dictionary, p_carte_id: String) -> void:
	carte_id = p_carte_id
	rocher_id = data.get("id", "rocher_%d_%d" % [data.get("x", 0), data.get("y", 0)])
	position_grille = Vector2i(data.get("x", 0), data.get("y", 0))
	position = Vector2(position_grille) * TAILLE_TILE
	
	# Vérifier si ce rocher a déjà été poussé (persistant)
	var flag_key := "rocher_%s_%s" % [carte_id, rocher_id]
	if GameManager.get_flag(flag_key):
		# Récupérer la position sauvegardée
		var saved_x = GameManager.get_flag("rocher_%s_%s_x" % [carte_id, rocher_id])
		var saved_y = GameManager.get_flag("rocher_%s_%s_y" % [carte_id, rocher_id])
		if saved_x != null and saved_y != null:
			position_grille = Vector2i(int(saved_x), int(saved_y))
			position = Vector2(position_grille) * TAILLE_TILE

	# Créer le collision shape
	var shape := RectangleShape2D.new()
	shape.size = Vector2(TAILLE_TILE - 2, TAILLE_TILE - 2)
	var col := CollisionShape2D.new()
	col.shape = shape
	col.position = Vector2(TAILLE_TILE / 2, TAILLE_TILE / 2)
	add_child(col)
	
	# Créer le sprite (un rectangle gris foncé représentant un rocher)
	var sprite := ColorRect.new()
	sprite.color = Color(0.45, 0.4, 0.35)
	sprite.size = Vector2(TAILLE_TILE - 4, TAILLE_TILE - 4)
	sprite.position = Vector2(2, 2)
	add_child(sprite)

# Appelée quand le joueur interagit (pousse)
func interagir(joueur: Node) -> void:
	if not StrengthSystem.peut_utiliser_force():
		return
	
	# Direction du joueur
	var dir: Vector2i = joueur.direction_actuelle
	var cible := position_grille + dir
	
	# Vérifier que la case cible est libre
	var carte_data := MapLoader.get_carte(carte_id)
	if not StrengthSystem.case_libre_pour_rocher(carte_data, cible):
		return
	
	# Pousser le rocher
	_est_pousse = true
	position_grille = cible
	
	# Animation de poussée
	var tween := create_tween()
	tween.tween_property(self, "position", Vector2(cible) * TAILLE_TILE, 0.3)
	
	# Sauvegarder la position
	GameManager.set_flag("rocher_%s_%s" % [carte_id, rocher_id], true)
	GameManager.set_flag("rocher_%s_%s_x" % [carte_id, rocher_id], cible.x)
	GameManager.set_flag("rocher_%s_%s_y" % [carte_id, rocher_id], cible.y)
	
	AudioManager.jouer_sfx("res://assets/audio/sfx/boulder.ogg")
