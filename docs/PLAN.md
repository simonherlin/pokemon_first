# Plan de développement — Pokémon Rouge/Bleu HD (Version Familiale)

> Recréer l'intégralité de Pokémon Rouge/Bleu en tant que RPG 2D moderne  
> **Moteur** : Godot 4 + GDScript  
> **Visuel** : Pixel art HD modernisé (sprites 64×96, tiles 32×32)  
> **Langue** : Français  
> **Pokémon** : 151 dans un seul jeu, pas d'exclusivités de version  
> **Usage** : Personnel / Familial — non commercial  

---

## Décisions techniques

| Choix | Décision |
|---|---|
| Moteur | Godot 4 + GDScript |
| Style visuel | Pixel art HD modernisé |
| Langue | Français |
| Pokémon | 151 attrapables dans un seul jeu |
| Résolution | 480×320 → upscale × 3 → 1440×960 (pixelperfect) |
| Architecture | 100 % data-driven (JSON pour Pokémon, attaques, cartes, dresseurs) |
| Éditeur de cartes | Tiled Map Editor → export JSON → import Godot |
| Pixel art | Aseprite ou Pixelorama |
| Versioning | Git + GitHub |

---

## Outils à installer

| Outil | Usage | Lien |
|---|---|---|
| Godot 4.x | Moteur / éditeur | https://godotengine.org |
| Tiled Map Editor | Édition des tilemaps | https://mapeditor.org |
| Aseprite ou Pixelorama | Pixel art | https://libresprite.github.io (libre) |
| Git | Versioning | natif Linux |
| GitHub CLI (`gh`) | Gestion repo | https://cli.github.com |

---

## Structure des dossiers

```
pokemon_first/
├── project.godot
├── assets/
│   ├── sprites/
│   │   ├── pokemon/
│   │   │   ├── front/          # sprite face (combat ennemi) — 151 sprites
│   │   │   ├── back/           # sprite dos (combat allié) — 151 sprites
│   │   │   └── icons/          # icônes miniatures (menu équipe/PC) — 151
│   │   ├── characters/         # joueur, PNJ, dresseurs — overworld
│   │   ├── tilesets/           # outdoor, indoor, grottes, arènes...
│   │   └── ui/                 # frames menus, boutons, icônes, HP bars
│   ├── audio/
│   │   ├── music/              # ~30 morceaux (villes, routes, combats...)
│   │   └── sfx/                # sons de menu, attaques, capture, soin...
│   └── fonts/                  # polices pixel art
├── data/                       # DONNÉES DU JEU (JSON)
│   ├── pokemon/
│   │   ├── species.json        # 151 Pokémon : stats, types, learnset, évolution
│   │   └── moves.json          # ~165 attaques Gen 1 : puissance, précision, effets
│   ├── maps/                   # une entrée par carte (~250 cartes)
│   │   ├── bourg_palette.json  # tiles, PNJ, warps, encounters, scripts
│   │   └── ...
│   ├── trainers.json           # équipes des dresseurs, dialogue, récompense
│   ├── items.json              # objets : effet, prix, description
│   ├── type_chart.json         # matrice 15×15 des efficacités de types
│   ├── encounter_tables.json   # Pokémon par zone, niveaux, probabilités
│   └── pokedex.json            # descriptions, taille, poids par Pokémon
├── scenes/
│   ├── maps/                   # .tscn par zone (~250 scènes)
│   ├── battle/
│   │   ├── battle_scene.tscn
│   │   └── battle_hud.tscn
│   ├── ui/
│   │   ├── dialog_box.tscn
│   │   ├── start_menu.tscn
│   │   ├── party_screen.tscn
│   │   ├── bag_screen.tscn
│   │   ├── pokedex_screen.tscn
│   │   └── shop_screen.tscn
│   ├── entities/
│   │   ├── player.tscn
│   │   ├── npc.tscn
│   │   └── trainer.tscn
│   └── title_screen.tscn
├── scripts/
│   ├── autoload/               # Singletons globaux (chargés automatiquement)
│   │   ├── game_manager.gd     # état du jeu, flags de progression, badges
│   │   ├── player_data.gd      # équipe, inventaire, Pokédex, position
│   │   ├── scene_manager.gd    # transitions de scènes, chargement cartes
│   │   ├── audio_manager.gd    # lecture musique/SFX
│   │   └── save_manager.gd     # sauvegarde / chargement
│   ├── battle/
│   │   ├── battle_controller.gd    # machine à états du tour par tour
│   │   ├── battle_calculator.gd    # formule dégâts, efficacité, critique
│   │   ├── move_effects.gd         # statuts, modifs de stats, effets spéciaux
│   │   └── ai_controller.gd        # IA des dresseurs et Pokémon sauvages
│   ├── overworld/
│   │   ├── player_controller.gd    # déplacement grille, input, interactions
│   │   ├── npc_controller.gd       # déplacement PNJ, patterns, dialogue
│   │   ├── encounter_system.gd     # déclenchement rencontres sauvages
│   │   └── event_system.gd         # cutscenes, events scénaristiques
│   ├── pokemon/
│   │   ├── pokemon.gd              # instance Pokémon (stats, attaques, statut)
│   │   ├── species_data.gd         # chargeur des espèces depuis JSON
│   │   └── evolution.gd            # logique de vérification d'évolution
│   └── ui/
│       ├── dialog_controller.gd
│       ├── menu_controller.gd
│       └── battle_hud_controller.gd
├── shaders/
│   ├── battle_transition.gdshader  # effet spirale/flash entrée en combat
│   └── flash_white.gdshader        # flash blanc (évolution, capture)
└── docs/
    └── PLAN.md                     # ce fichier
```

---

## Phase 0 — Mise en place du projet *(~2-3 jours)*

### Tâches

- [ ] Installer Godot 4.x (AppImage Linux)
- [ ] Installer Tiled Map Editor
- [ ] Installer Aseprite / Pixelorama / LibreSprite
- [ ] Créer le projet Godot dans ce dossier
- [ ] Configurer la résolution : 480×320 de base, upscale pixel-perfect
- [ ] Créer les 5 Autoloads (singletons globaux) :
  - `GameManager` — état du jeu, flags, badges
  - `PlayerData` — équipe, inventaire, Pokédex, position sauvegardée
  - `SceneManager` — transitions, chargement de cartes, stack de scènes
  - `AudioManager` — lecture musique/SFX avec crossfade
  - `SaveManager` — sérialisation/désérialisation JSON
- [ ] Mettre en place la structure complète de dossiers
- [ ] Initialiser le repo git, créer le `.gitignore`

---

## Phase 1 — Prototype jouable "Core Loop" *(~6-8 semaines)*

**Objectif** : Marcher dans Bourg Palette, aller Route 1, combattre un Pokémon sauvage, le capturer, soigner au Centre Pokémon. La boucle de base doit être fun.

### Modules

#### 1.1 Déplacement joueur sur grille
- Mouvement tile-par-tile (32px de grille)
- 4 directions + animation de marche (4 frames/direction)
- Collision avec murs, obstacles, PNJ
- Interaction (touche A devant PNJ / panneau / porte)
- **Script** : `scripts/overworld/player_controller.gd`

#### 1.2 Système de cartes
- Tiles 32×32, importer depuis Tiled → Godot TileMap
- Premier tileset outdoor (herbe, chemin, arbres, maisons, hautes herbes, eau)
- Construire **Bourg Palette** : maison joueur, maison rival, Labo Chen
- Construire **Route 1** : chemin simple avec hautes herbes
- Construire **Jadielle** (simplifié) : Centre Pokémon + Boutique
- Warps / portes fonctionnelles entre les cartes

#### 1.3 Système de dialogues
- Boîte de texte bas d'écran, effet machine à écrire
- Support Oui/Non  
- **Script** : `scripts/ui/dialog_controller.gd`

#### 1.4 Chargement des données JSON
- Parser `species.json` : 3 starters + leurs évolutions (9 Pokémon)
- Parser `moves.json` : ~20 premières attaques
- Parser `type_chart.json` : matrice 15×15

#### 1.5 Système de combat — cœur du jeu
- **Machine à états** : INTRO → CHOIX_ACTION → CHOIX_ATTAQUE → EXÉCUTION → VÉRIF_KO → TOUR_SUIVANT → FIN
- **Formule dégâts Gen 1** :
  ```
  Dmg = ((2*Lvl/5+2) * Puissance * Attaque/Defense) / 50 + 2
       × STAB × TypeEfficacité × Aléatoire(0.85–1.0)
  ```
- Efficacité des types (super / pas très / aucun effet / normal)
- Coups critiques, précision/esquive
- Statuts : brûlure, gel, paralysie, poison, sommeil
- Gain d'EXP après victoire, montée de niveau, apprentissage d'attaques

#### 1.6 Interface de combat
- Sprite Pokémon ennemi (face) haut-droite, allié (dos) bas-gauche
- Barres PV animées (vert → jaune → rouge selon %)
- Barre EXP
- Menu : Combat / Sac / Pokémon / Fuite
- Sous-menu attaques : nom, type, PP restants / PP max
- Messages de combat typés (machine à écrire)

#### 1.7 Rencontres sauvages
- Hautes herbes → compteur de pas → déclenchement aléatoire
- Table de rencontres : Route 1 = Rattata niv.2-5 (45%), Roucool niv.2-5 (45%), Rattata niv.4-7 (10%)
- Transition visuelle vers le combat (fondu + effet spirale)

#### 1.8 Capture
- Lancer Poké Ball depuis le Sac en combat
- Formule : `TauxCapture = (3*PVmax - 2*PVcourant) * TauxBase * ModificateurBall * ModificateurStatut / (3*PVmax)`
- Animation Ball (1-3 secousses → capture ou échec)
- Pokémon ajouté à l'équipe (ou PC si 6 déjà)

#### 1.9 Centre Pokémon
- Parler à l'infirmière Joëlle → soin complet (PV + PP + statuts)
- Animation + musique de soin

#### 1.10 Sprites placeholder
- Rectangles colorés avec nom du Pokémon pour les 10-15 premiers nécessaires

---

## Phase 2 — Systèmes RPG complets *(~4-6 semaines)*

- [ ] **Gestion d'équipe** — voir 6 Pokémon, échanger l'ordre, voir le résumé détaillé
- [ ] **Sac / Inventaire** — catégories (Objets/Balls/Objets Clés/CT-CS), utiliser en et hors combat
- [ ] **Boutique Pokémon** — acheter/vendre, stock variable par ville, Pokédollars
- [ ] **Combats de dresseurs** — ligne de vue, combat forcé, IA basique, récompense argent, flag "déjà battu"
- [ ] **Évolution** — par niveau (flash + animation), par pierre, par échange (PNJ dédié)
- [ ] **Système PC** (Bill's PC) — déposer/retirer Pokémon, boîtes de 30
- [ ] **Pokédex** — 151 entrées, vu/capturé, fiche détaillée (sprite, type, taille, poids, description)
- [ ] **Sauvegarde / Chargement** — JSON, 1 emplacement, via menu Start

---

## Phase 3 — Premier arc : Bourg Palette → Argenta *(~4-6 semaines)*

### Séquence scénaristique

1. Écran titre → Nouvelle Partie / Continuer
2. Intro Prof Chen → choix du nom joueur + rival
3. Chambre du joueur → sortie → Bourg Palette
4. Tente de partir → Chen t'arrête → Labo
5. **Choix du starter** (Bulbizarre / Salamèche / Carapuce) — rival prend l'avantage de type
6. **Combat Rival #1** (dans le Labo)
7. Route 1 (Rattata, Roucool), PNJ qui donne une Potion
8. **Jadielle** — Centre Pokémon, Boutique
9. Vieil homme → bloqué → retourner à Bourg Palette chercher le Colis Chen
10. Livrer le Colis → obtenir le Pokédex + 5 Pokéballs → départ officiel
11. Route 2 (Nord + Sud)
12. **Forêt de Jade** — labyrinthe, dresseurs Insectes, Pikachu rare, Chenipan, Aspicot, Coconfort
13. **Argenta** — ville, Musée (fossiles), Centre, Boutique
14. **Arène d'Argenta** — dresseur préliminaire + **Pierre** (Racaillou niv.12, Onix niv.14)
15. Obtention Badge Roche + CT Tomberoche
16. Route 3 → entrée Mont Sélénite

---

## Phase 4 — Contenu complet : tout le jeu *(~12-20 semaines)*

### Zone par zone dans l'ordre du scénario

| # | Zone | Événement clé |
|---|---|---|
| 1 | Mont Sélénite | 3 étages, fossiles (Amonita/Kabuto), Team Rocket, Pedro |
| 2 | Route 4 → Azuria | Arrivée en ville |
| 3 | Azuria | Arène #2 Ondine (Eau : Staross niv.18, Stari niv.21) — CS Coupe nécessaire |
| 4 | Routes 24-25 | Bill (accès PC), combat Rival #2 |
| 5 | Routes 5-6-7 | Tunnel Souterrain, accès Carmin |
| 6 | Carmin sur Mer | Arène #3 Maj. Bob (Électrik), S.S. Anne, CS01 Coupe |
| 7 | Grotte Taupiqueur | Connexion Carmin ↔ Lavanville |
| 8 | Routes 9-10 | Tunnel Roche (Fossil Pokémon) |
| 9 | Lavanville | Tour Pokémon (6 étages, fantômes, Scope Sylphe nécessaire), sauver M. Fuji |
| 10 | Route 8 + Tunnel Souterrain | Accès Céladopole |
| 11 | Céladopole | Arène #4 Érika (Plante), Grand Magasin (5 étages), Casino + **Repaire Team Rocket sous-sol** |
| 12 | Obtenir Scope Sylphe | Récompense de M. Fuji → retour Tour Pokémon, Fantominus, Ectoplasma |
| 13 | Piste Cyclable (Routes 16-17-18) | Accès Parmanie |
| 14 | Parmanie | Arène #5 Koga (Poison), Parc Safari (CS03 Surf + Dent d'Or → CS04 Force), Zoo |
| 15 | Routes 12-15 | Zones de pêche, accès maritime |
| 16 | Safrania | Arène #6 Morgane (Psy : Alakazam niv.43), Dojo de Combat **(choix Tygnon/Kicklee)**, Tour Sylphe (11 étages), **Combat Rival #4**, **Giovanni** → libération Safrania, CS05 Vole |
| 17 | Routes 19-20-21 | Navigation maritime (Surf requis) |
| 18 | Cramois'Île | Manoir Pokémon (clé Arène), **Arène #7 Auguste** (Feu), résurrection fossiles |
| 19 | Îles Écume | Puzzle Surf + Force (4 étages, boulders), **Artikodin** niv.50 |
| 20 | Centrale | **Électhor** niv.50 |
| 21 | Jadielle (retour) | **Arène #8 Giovanni** (Sol), Badge Terre |
| 22 | Routes 22-23 | Montée vers la Ligue |
| 23 | Route Victoire | Donjon final (3 étages, Force + Surf + Flash requis), **Sulfura** niv.50 |
| 24 | Plateau Indigo — Ligue | **Olga** (Glace), **Aldo** (Combat), **Agatha** (Spectre), **Peter** (Dragon), **Champion : le Rival** |
| 25 | Générique | Fin du jeu principal |
| 26 | Post-game | Grotte Inconnue → **Mewtwo** niv.70 |

---

## Les 151 Pokémon (Phase 5, en parallèle des Phases 3-4)

### Priorité de production des sprites

| Priorité | Pokémon | Raison |
|---|---|---|
| 🔴 Critique | Bulbizarre, Salamèche, Carapuce + évolutions | Starters dès le début |
| 🔴 Critique | Rattata, Roucool | Route 1, premier Pokémon sauvage |
| 🟡 Haute | Pikachu, Chenipan, Aspicot, Chrysacier, Coconfort, Ronflex | Forêt de Jade + tôt dans le jeu |
| 🟡 Haute | Racaillou, Onix (Pierre), Staross, Stari (Ondine) | Premières arènes |
| 🟢 Normale | Tous les autres, par ordre d'apparition scénaristique | |

### Exemple d'entrée `species.json`

```json
{
  "001": {
    "id": 1,
    "nom": "Bulbizarre",
    "nom_en": "Bulbasaur",
    "types": ["plante", "poison"],
    "stats_base": {
      "pv": 45, "attaque": 49, "defense": 49,
      "special": 65, "vitesse": 45
    },
    "evolution": { "methode": "niveau", "niveau": 16, "vers": "002" },
    "learnset": {
      "1": ["charge", "rugissement"],
      "7": ["vampigraine"],
      "13": ["fouet_lianes"],
      "20": ["poudre_toxik"],
      "22": ["poudre_dodo"],
      "29": ["tranche"],
      "38": ["jackpot"],
      "44": ["laser_plante"],
      "46": ["synthese"]
    },
    "groupe_exp": "lent_moyen",
    "taux_capture": 45,
    "exp_base": 64,
    "description_pokedex": "Une étrange graine est plantée sur son dos. Elle absorbe les rayons du soleil et grossit peu à peu.",
    "taille_m": 0.7,
    "poids_kg": 6.9
  }
}
```

---

## Phase 6 — Audio *(~3-4 semaines)*

### Musiques (~30 morceaux)

| Thème | Usage |
|---|---|
| Titre | Écran titre |
| Bourg Palette | Village de départ, ambiance paisible |
| Labo Chen | Scène d'introduction |
| Route 1 / 2 | Premiers pas dans le monde |
| Jadielle / Argenta | Villes du début |
| Forêt de Jade | Zone forêt mystérieuse |
| Mont Sélénite | Zone de grotte |
| Route régionale | Thème générique pour routes intermédiaires |
| Lavanville | Thème inquiétant, ville fantôme |
| Céladopole / Safrania | Grandes villes modernes |
| Parmanie / Cramois'Île | Villes spéciales |
| Centre Pokémon | Soin, repos |
| Combat sauvage | Rencontre Pokémon sauvage |
| Combat dresseur | Combat normal |
| Combat champion d'arène | Moment de tension |
| Combat rival | Thème du rival (épique) |
| Combat Team Rocket | Musique antagoniste |
| Conseil des 4 | Combat final |
| Champion | Combat du champion |
| Victoire (sauvage) | Court jingle |
| Victoire (dresseur) | Court jingle |
| Victoire (arène) | Fanfare badge |
| Évolution | Mélodie d'évolution |
| Capture | Jingle de capture |
| Générique | Fin du jeu |
| S.S. Anne | Thème bateau |
| Tour Sylphe | Zone d'infiltration |
| Route Victoire | Zone finale |
| Ligue Pokémon | Couloir de la Ligue |

### Effets sonores
- Sélection menu, validation, annulation, ouverture/fermeture menu
- Attaques physiques, attaques spéciales, super efficace, pas très efficace, immunité
- Montée de niveau, apprentissage d'attaque, évolution
- Rencontre sauvage, lancer de Ball, secousse Ball, capture réussie, échec capture
- Soin Centre Pokémon, dépense en boutique
- Bruit des pas, bruits d'ambiance (vent, eau)

---

## Phase 7 — Polish *(~4-6 semaines)*

### Transitions visuelles
- [ ] Entrée en combat : effet spirale + flash (shader)
- [ ] Fondu au noir entre les cartes
- [ ] Flash blanc à l'évolution et à la capture
- [ ] Effet de téléportation (Vol CS05)
- [ ] Ondulation de l'eau en overworld
- [ ] Balancement de l'herbe

### Animations de combat
- [ ] ~15-20 effets d'attaque groupés par type (Feu, Eau, Électrik, Plante, etc.)
- [ ] Shake d'écran sur impacts puissants
- [ ] Animation de fuite (Pokémon ennemi s'éloigne)
- [ ] Particules pour statuts (flammes brûlure, étincelles paralysie, ZZZ sommeil)

### Améliorations de confort (modernes, non intrusives)
- [ ] Texte accélérable (maintenir A ou Space)
- [ ] Affichage de l'efficacité du type dans le menu d'attaque (après avoir vu le Pokémon)
- [ ] Curseur mémorisant la dernière attaque utilisée
- [ ] Sprint (tenir Shift)
- [ ] Indicateur de Pokémon déjà capturé dans l'interface de combat

### Corrections Gen 1 (au choix : corriger ou conserver pour l'authenticité)
- Focus Energy (buggé à l'original : augmentait les critiques x2 au lieu de /2)
- Blizzard avait 90% de précision (trop élevé)
- Le type Spectre n'affectait pas Psychic (bug célèbre)
- Le poison s'estompait à 0 PV hors combat (bug lié à la marche)

---

## Checklist de validation finale

| Test | Critère |
|---|---|
| ✅ Déplacement | Joueur se déplace sur grille, no clip impossible |
| ✅ Combats | Dégâts corrects selon la table des types à chaque type |
| ✅ Capture | Pokémon capturables, rejoignent l'équipe ou le PC |
| ✅ Sauvegarde | Fermer + relancer → reprise exacte |
| ✅ Scénario | Bourg Palette → Ligue sans blocage |
| ✅ 151 Pokémon | Chaque Pokémon a au moins un lieu de capture |
| ✅ Évolutions | Niveau + pierre + échange fonctionnels |
| ✅ 8 Arènes | Battre les 8 champions dans l'ordre, badges octroyés |
| ✅ CS overworld | Coupe / Surf / Force / Vole fonctionnels |
| ✅ Performance | 60 FPS constant sur toutes les cartes |

---

## Estimation des délais

| Scénario | Durée estimée |
|---|---|
| Solo, temps partiel (10-15h/semaine) | **12-18 mois** |
| Solo, temps plein | **5-8 mois** |
| Petite équipe (2-3 personnes) | **3-5 mois** |

*La production des sprites (302+ sprites de combat + 151 icônes) est généralement le plus gros goulot d'étranglement.*

---

*Dernière mise à jour : Mars 2026*
