extends Control

# credits_screen.gd — Écran de générique après la victoire à la Ligue Pokémon
# Défile les crédits puis ramène au menu / Bourg Palette

const VITESSE_DEFILEMENT := 40.0  # pixels par seconde
const DELAI_FIN := 3.0  # secondes après la fin du défilement

var _texte_credits: Array[String] = [
	"",
	"",
	"FÉLICITATIONS !",
	"",
	"Tu es devenu le nouveau",
	"MAÎTRE POKÉMON !",
	"",
	"",
	"━━━━━━━━━━━━━━━━━━━━━",
	"",
	"POKÉMON ROUGE / BLEU HD",
	"",
	"Recréation familiale",
	"",
	"━━━━━━━━━━━━━━━━━━━━━",
	"",
	"",
	"— DIRECTION —",
	"",
	"Satoshi Tajiri",
	"(Concept original)",
	"",
	"",
	"— CONCEPTION DU JEU —",
	"",
	"Game Freak",
	"(Jeu original, 1996)",
	"",
	"",
	"— RECRÉATION HD —",
	"",
	"Projet familial",
	"avec Godot Engine 4",
	"",
	"",
	"— POKÉMON —",
	"",
	"151 Pokémon de la",
	"première génération",
	"",
	"De Bulbizarre (#001)",
	"à Mew (#151)",
	"",
	"",
	"— RÉGIONS —",
	"",
	"Bourg Palette",
	"Jadielle",
	"Argenta",
	"Azuria",
	"Carmin sur Mer",
	"Lavanville",
	"Céladopole",
	"Safrania",
	"Parmanie",
	"Cramois'Île",
	"Plateau Indigo",
	"",
	"",
	"— CHAMPIONS D'ARÈNE —",
	"",
	"Pierre — Badge Roche",
	"Ondine — Badge Cascade",
	"Major Bob — Badge Foudre",
	"Érika — Badge Prisme",
	"Koga — Badge Âme",
	"Morgane — Badge Marais",
	"Auguste — Badge Volcan",
	"Giovanni — Badge Terre",
	"",
	"",
	"— CONSEIL DES 4 —",
	"",
	"Olga — Glace",
	"Aldo — Combat",
	"Agatha — Spectre",
	"Peter — Dragon",
	"",
	"",
	"— CHAMPION —",
	"",
	"Régis",
	"",
	"",
	"— POKÉMON LÉGENDAIRES —",
	"",
	"Artikodin — Îles Écume",
	"Électhor — Centrale",
	"Sulfura — Route Victoire",
	"Mewtwo — Grotte Inconnue",
	"Mew — ???",
	"",
	"",
	"— MOTEUR —",
	"",
	"Godot Engine 4",
	"GDScript",
	"",
	"",
	"— MUSIQUE ET SON —",
	"",
	"Inspiré de l'œuvre originale",
	"de Junichi Masuda",
	"",
	"",
	"━━━━━━━━━━━━━━━━━━━━━",
	"",
	"Ce jeu est un projet",
	"familial non commercial.",
	"",
	"Pokémon est une marque",
	"de The Pokémon Company,",
	"Nintendo et Game Freak.",
	"",
	"━━━━━━━━━━━━━━━━━━━━━",
	"",
	"",
	"Merci d'avoir joué !",
	"",
	"",
	"— FIN —",
	"",
	"",
	"",
	"Appuie sur A pour continuer...",
	"",
	"",
]

var _label_credits: RichTextLabel = null
var _defilement_actif: bool = true
var _position_y: float = 0.0
var _hauteur_totale: float = 0.0
var _timer_fin: float = 0.0
var _termine: bool = false

func _ready() -> void:
	# Fond noir
	var fond := ColorRect.new()
	fond.color = Color.BLACK
	fond.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(fond)
	
	# Label des crédits
	_label_credits = RichTextLabel.new()
	_label_credits.bbcode_enabled = true
	_label_credits.scroll_active = false
	_label_credits.fit_content = true
	_label_credits.set_anchors_preset(Control.PRESET_FULL_RECT)
	_label_credits.add_theme_color_override("default_color", Color.WHITE)
	
	# Construire le texte centré
	var texte := "[center]"
	for ligne in _texte_credits:
		if ligne.begins_with("—") or ligne.begins_with("━"):
			texte += "[color=gold]%s[/color]\n" % ligne
		elif ligne == ligne.to_upper() and ligne.length() > 2:
			texte += "[b][color=yellow]%s[/color][/b]\n" % ligne
		else:
			texte += "%s\n" % ligne
	texte += "[/center]"
	
	_label_credits.text = texte
	add_child(_label_credits)
	
	# Positionner en bas de l'écran
	_position_y = get_viewport_rect().size.y
	_label_credits.position.y = _position_y
	
	# Flag générique
	GameManager.set_flag("generique_vu", true)
	
	# Musique
	if ResourceLoader.exists("res://assets/audio/music/generique.ogg"):
		AudioManager.jouer_musique("res://assets/audio/music/generique.ogg")

func _process(delta: float) -> void:
	if _termine:
		return
	
	# Accélérer avec A/Espace
	var vitesse := VITESSE_DEFILEMENT
	if Input.is_action_pressed("ui_accept") or Input.is_key_pressed(KEY_SPACE):
		vitesse *= 4.0
	
	if _defilement_actif:
		_position_y -= vitesse * delta
		_label_credits.position.y = _position_y
		
		# Calculer la hauteur totale du contenu
		_hauteur_totale = _label_credits.get_content_height()
		
		# Fin du défilement
		if _position_y + _hauteur_totale < 0:
			_defilement_actif = false
			_timer_fin = DELAI_FIN
	else:
		_timer_fin -= delta
		if _timer_fin <= 0:
			_termine = true
			_retour_jeu()
	
	# Skip avec Échap
	if Input.is_action_just_pressed("ui_cancel"):
		_termine = true
		_retour_jeu()

func _retour_jeu() -> void:
	# Soigner toute l'équipe
	for i in range(PlayerData.equipe.size()):
		var p := Pokemon.from_dict(PlayerData.equipe[i])
		p.soigner_complet()
		PlayerData.equipe[i] = p.to_dict()
	# Réinitialiser les flags E4 (pour pouvoir recommencer)
	GameManager.set_flag("ligue_en_cours", false)
	GameManager.set_flag("conseil_olga_battu", false)
	GameManager.set_flag("conseil_aldo_battu", false)
	GameManager.set_flag("conseil_agatha_battu", false)
	GameManager.set_flag("conseil_peter_battu", false)
	# Retour à Bourg Palette après les crédits
	SceneManager.charger_scene("res://scenes/maps/bourg_palette.tscn", {
		"warp_entree": ""
	})
