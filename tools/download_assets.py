#!/usr/bin/env python3
"""
Télécharge les assets audio + sprites dresseurs depuis pret/pokefirered et Pokémon Showdown.
1) MIDI musicaux FRLG depuis pret/pokefirered
2) Cris Pokémon depuis Pokémon Showdown
3) Sprites dresseurs front pics depuis pret/pokefirered
4) Sprites overworld depuis pret/pokefirered
"""

import os
import json
import subprocess
import urllib.request
import time
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_DIR = os.path.join(BASE_DIR, "assets", "audio", "music")
SFX_DIR = os.path.join(BASE_DIR, "assets", "audio", "sfx")
CRIES_DIR = os.path.join(SFX_DIR, "cries")
TRAINER_SPRITES_DIR = os.path.join(BASE_DIR, "assets", "sprites", "trainers")
OVERWORLD_DIR = os.path.join(BASE_DIR, "assets", "sprites", "characters")
MIDI_TEMP_DIR = os.path.join(BASE_DIR, "tools", "midi_temp")

SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

PRET_BASE = "https://raw.githubusercontent.com/pret/pokefirered/master"
SHOWDOWN_BASE = "https://play.pokemonshowdown.com/audio"

# ============================================================
# 1) MUSIQUES MIDI FRLG
# ============================================================
# Mapping : nom_fichier_local → nom_midi_pret
MUSIC_TRACKS = {
    # Villes (noms corrigés avec les vrais fichiers pret/pokefirered)
    "bourg_palette": "mus_pallet",
    "jadielle": "mus_pewter",           # Viridian = même thème que Pewter
    "argenta": "mus_pewter",
    "azuria": "mus_fuchsia",            # Cerulean = même thème que Fuchsia
    "carmin": "mus_vermillion",
    "lavanville": "mus_lavender",
    "celadopole": "mus_celadon",
    "safrania": "mus_celadon",           # Saffron = même thème que Celadon
    "parmanie": "mus_fuchsia",
    "cramoisile": "mus_cinnabar",
    "plateau_indigo": "mus_poke_center", # Plateau Indigo = Centre Pokémon
    # Routes
    "route_1": "mus_route1",
    "route_2": "mus_route1",
    "route_3": "mus_route3",
    "route_4": "mus_route3",
    "route_5": "mus_route3",
    "route_6": "mus_route3",
    "route_7": "mus_route3",
    "route_8": "mus_route3",
    "route_9": "mus_route3",
    "route_10": "mus_route3",
    "route_11": "mus_route11",
    "route_12": "mus_route11",
    "route_13": "mus_route11",
    "route_14": "mus_route11",
    "route_15": "mus_route11",
    "route_16": "mus_route11",
    "route_17": "mus_route11",
    "route_18": "mus_route11",
    "route_19": "mus_route11",
    "route_20": "mus_route11",
    "route_21": "mus_route11",
    "route_22": "mus_route1",            # Route 22 utilise Route 1
    "route_23": "mus_victory_road",      # Route 23 utilise Victory Road
    "route_24": "mus_route24",
    "route_25": "mus_route24",
    # Combats
    "combat_sauvage": "mus_vs_wild",
    "combat_dresseur": "mus_vs_trainer",
    "combat_champion_arene": "mus_vs_gym_leader",
    "combat_conseil4": "mus_vs_gym_leader",  # E4 = même thème que Gym Leader en Gen 1
    "combat_champion": "mus_vs_champion",
    "combat_legendaire": "mus_vs_legend",
    # Victoire
    "victoire_dresseur": "mus_victory_trainer",
    "victoire_sauvage": "mus_victory_wild",
    "victoire_champion_arene": "mus_victory_gym_leader",
    # Lieux spéciaux
    "centre_pokemon": "mus_poke_center",
    "boutique_pokemon": "mus_poke_center",   # Pas de thème Pokémart séparé, utilise Poké Center
    "arene": "mus_gym",
    "laboratoire_chen": "mus_oak_lab",
    "mont_selenite": "mus_mt_moon",
    "foret_jade": "mus_viridian_forest",
    "grotte": "mus_mt_moon",
    "tour_pokemon": "mus_poke_tower",
    "tour_sylphe": "mus_silph",
    "repaire_rocket": "mus_rocket_hideout",
    "route_victoire": "mus_victory_road",
    "ss_anne": "mus_ss_anne",
    "manoir_pokemon": "mus_poke_mansion",
    "parc_safari": "mus_cycling",            # Pas de Safari Zone dédié, cycling est joyeux
    "casino": "mus_game_corner",
    "grotte_inconnue": "mus_poke_mansion",   # Grotte Inconnue = ambiance sombre
    "iles_ecume": "mus_mt_moon",             # Grottes = Mt Moon
    "tunnel": "mus_mt_moon",
    "grotte_taupiqueur": "mus_mt_moon",
    # Événements
    "titre": "mus_title",
    "intro_chen": "mus_oak",
    "generique": "mus_credits",
    "evolution": "mus_evolution",
    "soin_pokemon": "mus_heal",
    "ligue_champion_salle": "mus_hall_of_fame",
    "dojo_combat": "mus_gym",
    "musee": "mus_school",                   # Musée = école/bâtiment public
    "surf": "mus_surf",
    "velo": "mus_cycling",
    # Rencontres / jingles
    "rencontre_rival": "mus_encounter_rival",
    "rencontre_dresseur": "mus_encounter_boy",
    "rencontre_dresseuse": "mus_encounter_girl",
    "rencontre_champion_arene": "mus_encounter_gym_leader",
    "rencontre_rocket": "mus_encounter_rocket",
    # Fanfares / jingles
    "obtention_badge": "mus_obtain_badge",
    "obtention_objet": "mus_obtain_item",
    "obtention_pokemon": "mus_caught_intro",
    "capture_pokemon": "mus_caught",
    "niveau_up": "mus_level_up",
    "labo_fossiles": "mus_cinnabar",
}

# ============================================================
# 2) CRIS POKÉMON — noms anglais pour Pokémon Showdown
# ============================================================
POKEMON_ENGLISH_NAMES = {
    "001": "bulbasaur", "002": "ivysaur", "003": "venusaur",
    "004": "charmander", "005": "charmeleon", "006": "charizard",
    "007": "squirtle", "008": "wartortle", "009": "blastoise",
    "010": "caterpie", "011": "metapod", "012": "butterfree",
    "013": "weedle", "014": "kakuna", "015": "beedrill",
    "016": "pidgey", "017": "pidgeotto", "018": "pidgeot",
    "019": "rattata", "020": "raticate",
    "021": "spearow", "022": "fearow",
    "023": "ekans", "024": "arbok",
    "025": "pikachu", "026": "raichu",
    "027": "sandshrew", "028": "sandslash",
    "029": "nidoranf", "030": "nidorina", "031": "nidoqueen",
    "032": "nidoranm", "033": "nidorino", "034": "nidoking",
    "035": "clefairy", "036": "clefable",
    "037": "vulpix", "038": "ninetales",
    "039": "jigglypuff", "040": "wigglytuff",
    "041": "zubat", "042": "golbat",
    "043": "oddish", "044": "gloom", "045": "vileplume",
    "046": "paras", "047": "parasect",
    "048": "venonat", "049": "venomoth",
    "050": "diglett", "051": "dugtrio",
    "052": "meowth", "053": "persian",
    "054": "psyduck", "055": "golduck",
    "056": "mankey", "057": "primeape",
    "058": "growlithe", "059": "arcanine",
    "060": "poliwag", "061": "poliwhirl", "062": "poliwrath",
    "063": "abra", "064": "kadabra", "065": "alakazam",
    "066": "machop", "067": "machoke", "068": "machamp",
    "069": "bellsprout", "070": "weepinbell", "071": "victreebel",
    "072": "tentacool", "073": "tentacruel",
    "074": "geodude", "075": "graveler", "076": "golem",
    "077": "ponyta", "078": "rapidash",
    "079": "slowpoke", "080": "slowbro",
    "081": "magnemite", "082": "magneton",
    "083": "farfetchd", "084": "doduo", "085": "dodrio",
    "086": "seel", "087": "dewgong",
    "088": "grimer", "089": "muk",
    "090": "shellder", "091": "cloyster",
    "092": "gastly", "093": "haunter", "094": "gengar",
    "095": "onix",
    "096": "drowzee", "097": "hypno",
    "098": "krabby", "099": "kingler",
    "100": "voltorb", "101": "electrode",
    "102": "exeggcute", "103": "exeggutor",
    "104": "cubone", "105": "marowak",
    "106": "hitmonlee", "107": "hitmonchan",
    "108": "lickitung",
    "109": "koffing", "110": "weezing",
    "111": "rhyhorn", "112": "rhydon",
    "113": "chansey",
    "114": "tangela",
    "115": "kangaskhan",
    "116": "horsea", "117": "seadra",
    "118": "goldeen", "119": "seaking",
    "120": "staryu", "121": "starmie",
    "122": "mrmime",
    "123": "scyther",
    "124": "jynx",
    "125": "electabuzz",
    "126": "magmar",
    "127": "pinsir",
    "128": "tauros",
    "129": "magikarp", "130": "gyarados",
    "131": "lapras",
    "132": "ditto",
    "133": "eevee", "134": "vaporeon", "135": "jolteon", "136": "flareon",
    "137": "porygon",
    "138": "omanyte", "139": "omastar",
    "140": "kabuto", "141": "kabutops",
    "142": "aerodactyl",
    "143": "snorlax",
    "144": "articuno", "145": "zapdos", "146": "moltres",
    "147": "dratini", "148": "dragonair", "149": "dragonite",
    "150": "mewtwo",
    "151": "mew",
}

# ============================================================
# 3) SPRITES DRESSEURS FRONT PICS — mapping classe → fichier pret
# ============================================================
TRAINER_SPRITES = {
    "rival_early": "rival_early_front_pic",
    "rival_late": "rival_late_front_pic",
    "champion_rival": "champion_rival_front_pic",
    "leader_brock": "leader_brock_front_pic",
    "leader_misty": "leader_misty_front_pic",
    "leader_lt_surge": "leader_lt_surge_front_pic",
    "leader_erika": "leader_erika_front_pic",
    "leader_koga": "leader_koga_front_pic",
    "leader_sabrina": "leader_sabrina_front_pic",
    "leader_blaine": "leader_blaine_front_pic",
    "leader_giovanni": "leader_giovanni_front_pic",
    "elite_four_lorelei": "elite_four_lorelei_front_pic",
    "elite_four_bruno": "elite_four_bruno_front_pic",
    "elite_four_agatha": "elite_four_agatha_front_pic",
    "elite_four_lance": "elite_four_lance_front_pic",
    "professor_oak": "professor_oak_front_pic",
    "bug_catcher": "bug_catcher_front_pic",
    "lass": "lass_front_pic",
    "youngster": "youngster_front_pic",
    "hiker": "hiker_front_pic",
    "biker": "biker_front_pic",
    "beauty": "beauty_front_pic",
    "gentleman": "gentleman_front_pic",
    "scientist": "scientist_front_pic",
    "super_nerd": "super_nerd_front_pic",
    "fisherman": "fisherman_front_pic",
    "swimmer_m": "swimmer_m_front_pic",
    "swimmer_f": "swimmer_f_front_pic",
    "sailor": "sailor_front_pic",
    "juggler": "juggler_front_pic",
    "psychic_m": "psychic_m_front_pic",
    "psychic_f": "psychic_f_front_pic",
    "rocker": "rocker_front_pic",
    "engineer": "engineer_front_pic",
    "channeler": "channeler_front_pic",
    "bird_keeper": "bird_keeper_front_pic",
    "black_belt": "black_belt_front_pic",
    "tamer": "tamer_front_pic",
    "camper": "camper_front_pic",
    "picnicker": "picnicker_front_pic",
    "cool_trainer_m": "cool_trainer_m_front_pic",
    "cool_trainer_f": "cool_trainer_f_front_pic",
    "rocket_grunt_m": "rocket_grunt_m_front_pic",
    "rocket_grunt_f": "rocket_grunt_f_front_pic",
    "burglar": "burglar_front_pic",
    "cue_ball": "cue_ball_front_pic",
    "gamer": "gamer_front_pic",
    "pokemaniac": "pokemaniac_front_pic",
    "pokemon_breeder": "pokemon_breeder_front_pic",
    "pokemon_ranger_m": "pokemon_ranger_m_front_pic",
    "pokemon_ranger_f": "pokemon_ranger_f_front_pic",
}

# ============================================================
# 4) SPRITES OVERWORLD
# ============================================================
OVERWORLD_SPRITES = [
    "red_normal",
    "green_normal", 
    "prof_oak",
    "nurse",
    "clerk",
    "gentleman",
    "beauty",
    "brock",
    "misty",
    "lt_surge",
    "erika",
    "koga",
    "sabrina",
    "blaine",
    "giovanni",
    "rocket_m",
    "rocket_f",
    "officer",
    "fisher",
    "youngster",
    "lass",
    "bug_catcher",
    "hiker",
    "biker",
    "sailor",
    "swimmer_m",
    "swimmer_f",
    "super_nerd",
    "scientist",
    "old_man",
    "old_woman",
    "boy",
    "girl",
    "fat_man",
    "medium",
    "channeler",
    "agatha",
    "bruno",
    "lorelei",
    "lance", 
    "bill",
    "mr_fuji",
]


def download_file(url, dest_path, retries=3):
    """Télécharge un fichier avec gestion des erreurs"""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Pokemon fan project asset downloader)'
            })
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, 'wb') as f:
                    f.write(data)
                return True
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                print(f"  ERREUR: {url} → {e}")
                return False
    return False


def download_midi_music():
    """Télécharge les fichiers MIDI depuis pret/pokefirered"""
    print("\n" + "=" * 60)
    print("1) TÉLÉCHARGEMENT DES MUSIQUES MIDI FRLG")
    print("=" * 60)
    
    os.makedirs(MIDI_TEMP_DIR, exist_ok=True)
    
    # Collecter les noms MIDI uniques
    midi_names = set(MUSIC_TRACKS.values())
    
    success = 0
    fail = 0
    for midi_name in sorted(midi_names):
        dest = os.path.join(MIDI_TEMP_DIR, f"{midi_name}.mid")
        if os.path.exists(dest):
            print(f"  [SKIP] {midi_name}.mid (déjà téléchargé)")
            success += 1
            continue
        
        url = f"{PRET_BASE}/sound/songs/midi/{midi_name}.mid"
        print(f"  Téléchargement {midi_name}.mid ...")
        if download_file(url, dest):
            success += 1
        else:
            fail += 1
    
    print(f"\nMIDI: {success} OK, {fail} échoués")
    return success


def convert_midi_to_ogg():
    """Convertit les MIDI en OGG via FluidSynth"""
    print("\n" + "=" * 60)
    print("2) CONVERSION MIDI → OGG VIA FLUIDSYNTH")
    print("=" * 60)
    
    os.makedirs(MUSIC_DIR, exist_ok=True)
    
    # Mapping inverse: pour chaque nom local, on regarde le midi source
    success = 0
    fail = 0
    converted_midis = set()
    
    for local_name, midi_name in sorted(MUSIC_TRACKS.items()):
        ogg_path = os.path.join(MUSIC_DIR, f"{local_name}.ogg")
        if os.path.exists(ogg_path) and os.path.getsize(ogg_path) > 1000:
            print(f"  [SKIP] {local_name}.ogg (déjà converti)")
            success += 1
            continue
        
        midi_path = os.path.join(MIDI_TEMP_DIR, f"{midi_name}.mid")
        if not os.path.exists(midi_path):
            print(f"  [MANQUANT] {midi_name}.mid non trouvé")
            fail += 1
            continue
        
        wav_path = os.path.join(MIDI_TEMP_DIR, f"{local_name}.wav")
        
        # FluidSynth : MIDI → WAV
        print(f"  Conversion {midi_name}.mid → {local_name}.ogg ...")
        try:
            result = subprocess.run(
                ["fluidsynth", "-ni", SOUNDFONT, midi_path, "-F", wav_path, "-r", "44100"],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode != 0:
                print(f"    FluidSynth erreur: {result.stderr[:200]}")
                fail += 1
                continue
            
            # WAV → OGG via Python soundfile
            import soundfile as sf
            data, samplerate = sf.read(wav_path)
            sf.write(ogg_path, data, samplerate, format='OGG', subtype='VORBIS')
            
            # Nettoyage WAV
            os.remove(wav_path)
            
            size_kb = os.path.getsize(ogg_path) / 1024
            print(f"    OK → {size_kb:.0f} KB")
            success += 1
            
        except Exception as e:
            print(f"    Erreur conversion: {e}")
            fail += 1
            if os.path.exists(wav_path):
                os.remove(wav_path)
    
    print(f"\nConversion: {success} OK, {fail} échoués")
    return success


def download_pokemon_cries():
    """Télécharge les cris des 151 Pokémon depuis Pokémon Showdown"""
    print("\n" + "=" * 60)
    print("3) TÉLÉCHARGEMENT DES CRIS POKÉMON")
    print("=" * 60)
    
    os.makedirs(CRIES_DIR, exist_ok=True)
    
    success = 0
    fail = 0
    for num, name in sorted(POKEMON_ENGLISH_NAMES.items()):
        dest = os.path.join(CRIES_DIR, f"{num}.mp3")
        if os.path.exists(dest):
            success += 1
            continue
        
        url = f"{SHOWDOWN_BASE}/cries/{name}.mp3"
        if download_file(url, dest):
            success += 1
        else:
            fail += 1
        
        # Rate limiting
        if (success + fail) % 20 == 0:
            time.sleep(0.5)
    
    print(f"\nCris: {success} OK, {fail} échoués")
    return success


def download_trainer_sprites():
    """Télécharge les sprites dresseurs front pics depuis pret/pokefirered"""
    print("\n" + "=" * 60)
    print("4) TÉLÉCHARGEMENT DES SPRITES DRESSEURS (FRONT PICS)")
    print("=" * 60)
    
    os.makedirs(TRAINER_SPRITES_DIR, exist_ok=True)
    
    success = 0
    fail = 0
    for local_name, pret_name in sorted(TRAINER_SPRITES.items()):
        dest = os.path.join(TRAINER_SPRITES_DIR, f"{local_name}.png")
        if os.path.exists(dest):
            print(f"  [SKIP] {local_name}.png")
            success += 1
            continue
        
        url = f"{PRET_BASE}/graphics/trainers/front_pics/{pret_name}.png"
        print(f"  Téléchargement {local_name}.png ...")
        if download_file(url, dest):
            success += 1
        else:
            fail += 1
    
    print(f"\nSprites dresseurs: {success} OK, {fail} échoués")
    return success


def download_overworld_sprites():
    """Télécharge les sprites overworld depuis pret/pokefirered"""
    print("\n" + "=" * 60)
    print("5) TÉLÉCHARGEMENT DES SPRITES OVERWORLD")
    print("=" * 60)
    
    os.makedirs(OVERWORLD_DIR, exist_ok=True)
    
    success = 0
    fail = 0
    for name in OVERWORLD_SPRITES:
        dest = os.path.join(OVERWORLD_DIR, f"{name}.png")
        if os.path.exists(dest):
            print(f"  [SKIP] {name}.png")
            success += 1
            continue
        
        url = f"{PRET_BASE}/graphics/object_events/pics/people/{name}.png"
        print(f"  Téléchargement {name}.png ...")
        if download_file(url, dest):
            success += 1
        else:
            fail += 1
    
    print(f"\nSprites overworld: {success} OK, {fail} échoués")
    return success


if __name__ == "__main__":
    print("=" * 60)
    print("POKÉMON FRLG — TÉLÉCHARGEMENT ASSETS AUTHENTIQUES")
    print("=" * 60)
    
    steps = sys.argv[1:] if len(sys.argv) > 1 else ["midi", "convert", "cries", "trainers", "overworld"]
    
    if "midi" in steps:
        download_midi_music()
    
    if "convert" in steps:
        convert_midi_to_ogg()
    
    if "cries" in steps:
        download_pokemon_cries()
    
    if "trainers" in steps:
        download_trainer_sprites()
    
    if "overworld" in steps:
        download_overworld_sprites()
    
    print("\n" + "=" * 60)
    print("TERMINÉ !")
    print("=" * 60)
