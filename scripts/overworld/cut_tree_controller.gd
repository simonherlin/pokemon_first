extends StaticBody2D

# CutTreeController — Arbuste coupable avec CS Coupe
# Apparaît sur la carte, disparaît si le joueur utilise Coupe (avec badge Foudre)

const TAILLE_TILE := 32

var arbre_id: String = ""
var carte_id: String = ""
var _coupe: bool = false

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision: CollisionShape2D = $CollisionShape2D

signal arbre_coupe(arbre_id: String)

func _ready() -> void:
	# Vérifier si cet arbre a déjà été coupé (flag dans GameManager)
	var flag_id := "arbre_%s_%s" % [carte_id, arbre_id]
	if GameManager.flags.get(flag_id, false):
		_retirer_arbre()

func initialiser(data: Dictionary, id_carte: String) -> void:
	arbre_id = data.get("id", "")
	carte_id = id_carte
	position = Vector2(data.get("x", 0), data.get("y", 0)) * TAILLE_TILE
	# Vérifier si déjà coupé
	var flag_id := "arbre_%s_%s" % [carte_id, arbre_id]
	if GameManager.flags.get(flag_id, false):
		_retirer_arbre()

func interagir(_joueur: Node) -> Array:
	# Le joueur interagit face à l'arbre
	if _coupe:
		return []
	# Vérifier si le joueur a CS Coupe et le badge Foudre
	var a_cs_coupe: bool = PlayerData.possede_item("cs_coupe")
	var a_badge_foudre: bool = GameManager.possede_badge(2)  # Badge index 2 = Foudre
	if not a_cs_coupe:
		return ["Cet arbre peut être coupé.", "Mais tu n'as pas la CS COUPE..."]
	if not a_badge_foudre:
		return ["Cet arbre peut être coupé.", "Tu as besoin du BADGE FOUDRE pour utiliser COUPE !"]
	# Couper l'arbre !
	return ["Tu utilises COUPE !", "L'arbuste a été coupé !"]

func couper() -> void:
	_coupe = true
	var flag_id := "arbre_%s_%s" % [carte_id, arbre_id]
	GameManager.flags[flag_id] = true
	_retirer_arbre()
	arbre_coupe.emit(arbre_id)

func _retirer_arbre() -> void:
	_coupe = true
	visible = false
	if collision:
		collision.set_deferred("disabled", true)
