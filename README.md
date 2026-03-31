# Pokémon Rouge/Bleu HD 🎮

Recréation familiale et personnelle de Pokémon Rouge/Bleu en version modernisée.  
**Non commercial — usage personnel uniquement.**

## Description

Recréation complète de Pokémon Rouge/Bleu (Génération I) en tant que RPG 2D moderne :

- **151 Pokémon** attrapables dans un seul jeu
- **Pixel art HD** modernisé (sprites 96×96, tiles 32×32)
- **Mécaniques Gen 1 authentiques** (formule de dégâts, un seul stat Spécial, etc.)
- **En français** (noms officiels FR de tous les Pokémon, attaques, lieux)
- Tout le scénario original : Bourg Palette → Ligue Pokémon → Mewtwo

## Stack technique

| Composant | Technologie |
|---|---|
| Moteur | [Godot 4](https://godotengine.org) + GDScript |
| Éditeur de cartes | [Tiled Map Editor](https://www.mapeditor.org) |
| Pixel art | Aseprite / [Pixelorama](https://github.com/Orama-Interactive/Pixelorama) |
| Données | JSON (data-driven) |
| Versioning | Git + GitHub |

## Prérequis

- Godot 4.x (télécharger sur [godotengine.org](https://godotengine.org/download))
- Git

## Lancer le projet

```bash
git clone https://github.com/simonherlin/pokemon_first.git
cd pokemon_first
# Ouvrir Godot 4 → Import → sélectionner ce dossier
```

## Structure du projet

```
pokemon_first/
├── assets/          # Sprites, audio, polices
├── data/            # Données JSON (Pokémon, attaques, cartes, dresseurs)
├── docs/            # Documentation et plan de développement
├── scenes/          # Scènes Godot (.tscn)
├── scripts/         # Scripts GDScript (.gd)
└── shaders/         # Shaders visuels (.gdshader)
```

## Plan de développement

Voir [docs/PLAN.md](docs/PLAN.md) pour le plan complet en 7 phases.

### Phases

| Phase | Description | Statut |
|---|---|---|
| 0 | Mise en place du projet | 🔄 En cours |
| 1 | Prototype jouable (Core Loop) | ⏳ À faire |
| 2 | Systèmes RPG complets | ⏳ À faire |
| 3 | Premier arc : Bourg Palette → Argenta | ⏳ À faire |
| 4 | Contenu complet (tout le jeu) | ⏳ À faire |
| 5 | 151 Pokémon (art + données) | ⏳ À faire |
| 6 | Audio complet | ⏳ À faire |
| 7 | Polish & finitions | ⏳ À faire |

## Avertissement légal

Ce projet est une recréation **non commerciale** à usage **strictement familial et personnel**.  
Tous les droits sur Pokémon appartiennent à Nintendo / Game Freak / The Pokémon Company.  
Ce projet n'est pas affilié, sponsorisé ou approuvé par ces entités.  
**Aucune distribution commerciale ne sera effectuée.**
