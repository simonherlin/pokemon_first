#!/usr/bin/env python3
"""
Convertit tous les MIDI téléchargés en OGG en deux passes:
1) FluidSynth : MIDI → WAV (appel subprocess séparé par fichier)
2) soundfile : WAV → OGG (dans le même processus)
"""
import os
import sys
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIDI_TEMP_DIR = os.path.join(BASE_DIR, "tools", "midi_temp")
MUSIC_DIR = os.path.join(BASE_DIR, "assets", "audio", "music")
SOUNDFONT = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

# Mapping identique au download_assets.py — nom_local → nom_midi
MUSIC_TRACKS = {
    "bourg_palette": "mus_pallet",
    "jadielle": "mus_pewter",
    "argenta": "mus_pewter",
    "azuria": "mus_fuchsia",
    "carmin": "mus_vermillion",
    "lavanville": "mus_lavender",
    "celadopole": "mus_celadon",
    "safrania": "mus_celadon",
    "parmanie": "mus_fuchsia",
    "cramoisile": "mus_cinnabar",
    "plateau_indigo": "mus_poke_center",
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
    "route_22": "mus_route1",
    "route_23": "mus_victory_road",
    "route_24": "mus_route24",
    "route_25": "mus_route24",
    "combat_sauvage": "mus_vs_wild",
    "combat_dresseur": "mus_vs_trainer",
    "combat_champion_arene": "mus_vs_gym_leader",
    "combat_conseil4": "mus_vs_gym_leader",
    "combat_champion": "mus_vs_champion",
    "combat_legendaire": "mus_vs_legend",
    "victoire_dresseur": "mus_victory_trainer",
    "victoire_sauvage": "mus_victory_wild",
    "victoire_champion_arene": "mus_victory_gym_leader",
    "centre_pokemon": "mus_poke_center",
    "boutique_pokemon": "mus_poke_center",
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
    "parc_safari": "mus_cycling",
    "casino": "mus_game_corner",
    "grotte_inconnue": "mus_poke_mansion",
    "iles_ecume": "mus_mt_moon",
    "tunnel": "mus_mt_moon",
    "grotte_taupiqueur": "mus_mt_moon",
    "titre": "mus_title",
    "intro_chen": "mus_oak",
    "generique": "mus_credits",
    "evolution": "mus_evolution",
    "soin_pokemon": "mus_heal",
    "ligue_champion_salle": "mus_hall_of_fame",
    "dojo_combat": "mus_gym",
    "musee": "mus_school",
    "surf": "mus_surf",
    "velo": "mus_cycling",
    "rencontre_rival": "mus_encounter_rival",
    "rencontre_dresseur": "mus_encounter_boy",
    "rencontre_dresseuse": "mus_encounter_girl",
    "rencontre_champion_arene": "mus_encounter_gym_leader",
    "rencontre_rocket": "mus_encounter_rocket",
    "obtention_badge": "mus_obtain_badge",
    "obtention_objet": "mus_obtain_item",
    "obtention_pokemon": "mus_caught_intro",
    "capture_pokemon": "mus_caught",
    "niveau_up": "mus_level_up",
    "labo_fossiles": "mus_cinnabar",
}

def main():
    os.makedirs(MUSIC_DIR, exist_ok=True)
    
    # Phase 1: FluidSynth MIDI → WAV (un par un pour éviter les segfaults)
    # On ne convertit que les MIDI uniques
    unique_midis = set(MUSIC_TRACKS.values())
    wav_cache = {}  # midi_name → wav_path
    
    print("=" * 60)
    print("PHASE 1: MIDI → WAV (FluidSynth)")
    print("=" * 60)
    
    for midi_name in sorted(unique_midis):
        midi_path = os.path.join(MIDI_TEMP_DIR, f"{midi_name}.mid")
        wav_path = os.path.join(MIDI_TEMP_DIR, f"{midi_name}.wav")
        
        if not os.path.exists(midi_path):
            print(f"  [MANQUANT] {midi_name}.mid")
            continue
        
        if os.path.exists(wav_path) and os.path.getsize(wav_path) > 1000:
            print(f"  [SKIP] {midi_name}.wav (déjà converti)")
            wav_cache[midi_name] = wav_path
            continue
        
        print(f"  Conversion {midi_name}.mid → WAV ...", end=" ", flush=True)
        result = subprocess.run(
            ["fluidsynth", "-ni", SOUNDFONT, midi_path, "-F", wav_path, "-r", "22050", "-g", "0.5"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and os.path.exists(wav_path):
            size_kb = os.path.getsize(wav_path) / 1024
            print(f"OK ({size_kb:.0f} KB)")
            wav_cache[midi_name] = wav_path
        else:
            print(f"ERREUR: {result.stderr[:100]}")
    
    print(f"\nWAV convertis: {len(wav_cache)}/{len(unique_midis)}")
    
    # Phase 2: WAV → OGG (soundfile)
    print("\n" + "=" * 60)
    print("PHASE 2: WAV → OGG (soundfile)")
    print("=" * 60)
    
    import soundfile as sf
    
    success = 0
    fail = 0
    for local_name, midi_name in sorted(MUSIC_TRACKS.items()):
        ogg_path = os.path.join(MUSIC_DIR, f"{local_name}.ogg")
        
        if os.path.exists(ogg_path) and os.path.getsize(ogg_path) > 500:
            print(f"  [SKIP] {local_name}.ogg")
            success += 1
            continue
        
        wav_path = wav_cache.get(midi_name)
        if not wav_path or not os.path.exists(wav_path):
            print(f"  [MANQUANT] WAV pour {local_name} ({midi_name})")
            fail += 1
            continue
        
        try:
            data, samplerate = sf.read(wav_path)
            sf.write(ogg_path, data, samplerate, format='OGG', subtype='VORBIS')
            size_kb = os.path.getsize(ogg_path) / 1024
            print(f"  {local_name}.ogg → {size_kb:.0f} KB")
            success += 1
        except Exception as e:
            print(f"  ERREUR {local_name}: {e}")
            fail += 1
    
    print(f"\nOGG: {success} OK, {fail} échoués")
    
    # Nettoyage des WAV
    print("\nNettoyage des WAV temporaires...")
    for wav_path in wav_cache.values():
        if os.path.exists(wav_path):
            os.remove(wav_path)
    
    print("Terminé !")

if __name__ == "__main__":
    main()
