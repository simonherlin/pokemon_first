#!/bin/bash
# Convertit les WAV en OGG un par un via des processus Python séparés
# Évite les segfaults de soundfile

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MIDI_DIR="$BASE_DIR/tools/midi_temp"
MUSIC_DIR="$BASE_DIR/assets/audio/music"
SOUNDFONT="/usr/share/sounds/sf2/FluidR3_GM.sf2"

mkdir -p "$MUSIC_DIR"

# Tableau associatif: nom_local=nom_midi
declare -A TRACKS
TRACKS[bourg_palette]=mus_pallet
TRACKS[jadielle]=mus_pewter
TRACKS[argenta]=mus_pewter
TRACKS[azuria]=mus_fuchsia
TRACKS[carmin]=mus_vermillion
TRACKS[lavanville]=mus_lavender
TRACKS[celadopole]=mus_celadon
TRACKS[safrania]=mus_celadon
TRACKS[parmanie]=mus_fuchsia
TRACKS[cramoisile]=mus_cinnabar
TRACKS[plateau_indigo]=mus_poke_center
TRACKS[route_1]=mus_route1
TRACKS[route_2]=mus_route1
TRACKS[route_3]=mus_route3
TRACKS[route_4]=mus_route3
TRACKS[route_5]=mus_route3
TRACKS[route_6]=mus_route3
TRACKS[route_7]=mus_route3
TRACKS[route_8]=mus_route3
TRACKS[route_9]=mus_route3
TRACKS[route_10]=mus_route3
TRACKS[route_11]=mus_route11
TRACKS[route_12]=mus_route11
TRACKS[route_13]=mus_route11
TRACKS[route_14]=mus_route11
TRACKS[route_15]=mus_route11
TRACKS[route_16]=mus_route11
TRACKS[route_17]=mus_route11
TRACKS[route_18]=mus_route11
TRACKS[route_19]=mus_route11
TRACKS[route_20]=mus_route11
TRACKS[route_21]=mus_route11
TRACKS[route_22]=mus_route1
TRACKS[route_23]=mus_victory_road
TRACKS[route_24]=mus_route24
TRACKS[route_25]=mus_route24
TRACKS[combat_sauvage]=mus_vs_wild
TRACKS[combat_dresseur]=mus_vs_trainer
TRACKS[combat_champion_arene]=mus_vs_gym_leader
TRACKS[combat_conseil4]=mus_vs_gym_leader
TRACKS[combat_champion]=mus_vs_champion
TRACKS[combat_legendaire]=mus_vs_legend
TRACKS[victoire_dresseur]=mus_victory_trainer
TRACKS[victoire_sauvage]=mus_victory_wild
TRACKS[victoire_champion_arene]=mus_victory_gym_leader
TRACKS[centre_pokemon]=mus_poke_center
TRACKS[boutique_pokemon]=mus_poke_center
TRACKS[arene]=mus_gym
TRACKS[laboratoire_chen]=mus_oak_lab
TRACKS[mont_selenite]=mus_mt_moon
TRACKS[foret_jade]=mus_viridian_forest
TRACKS[grotte]=mus_mt_moon
TRACKS[tour_pokemon]=mus_poke_tower
TRACKS[tour_sylphe]=mus_silph
TRACKS[repaire_rocket]=mus_rocket_hideout
TRACKS[route_victoire]=mus_victory_road
TRACKS[ss_anne]=mus_ss_anne
TRACKS[manoir_pokemon]=mus_poke_mansion
TRACKS[parc_safari]=mus_cycling
TRACKS[casino]=mus_game_corner
TRACKS[grotte_inconnue]=mus_poke_mansion
TRACKS[iles_ecume]=mus_mt_moon
TRACKS[tunnel]=mus_mt_moon
TRACKS[grotte_taupiqueur]=mus_mt_moon
TRACKS[titre]=mus_title
TRACKS[intro_chen]=mus_oak
TRACKS[generique]=mus_credits
TRACKS[evolution]=mus_evolution
TRACKS[soin_pokemon]=mus_heal
TRACKS[ligue_champion_salle]=mus_hall_of_fame
TRACKS[dojo_combat]=mus_gym
TRACKS[musee]=mus_school
TRACKS[surf]=mus_surf
TRACKS[velo]=mus_cycling
TRACKS[rencontre_rival]=mus_encounter_rival
TRACKS[rencontre_dresseur]=mus_encounter_boy
TRACKS[rencontre_dresseuse]=mus_encounter_girl
TRACKS[rencontre_champion_arene]=mus_encounter_gym_leader
TRACKS[rencontre_rocket]=mus_encounter_rocket
TRACKS[obtention_badge]=mus_obtain_badge
TRACKS[obtention_objet]=mus_obtain_item
TRACKS[obtention_pokemon]=mus_caught_intro
TRACKS[capture_pokemon]=mus_caught
TRACKS[niveau_up]=mus_level_up
TRACKS[labo_fossiles]=mus_cinnabar

echo "============================================"
echo "PHASE 1: MIDI → WAV (FluidSynth)"
echo "============================================"

# Convertir les MIDI uniques en WAV
declare -A DONE_MIDI
for local in "${!TRACKS[@]}"; do
    midi="${TRACKS[$local]}"
    if [[ -n "${DONE_MIDI[$midi]}" ]]; then continue; fi
    DONE_MIDI[$midi]=1
    
    wav="$MIDI_DIR/${midi}.wav"
    mid="$MIDI_DIR/${midi}.mid"
    
    if [[ ! -f "$mid" ]]; then
        echo "  [MANQUANT] $midi.mid"
        continue
    fi
    
    if [[ -f "$wav" && $(stat -c%s "$wav") -gt 1000 ]]; then
        echo "  [SKIP] $midi.wav"
        continue
    fi
    
    echo -n "  $midi.mid → WAV ... "
    fluidsynth -ni "$SOUNDFONT" "$mid" -F "$wav" -r 22050 -g 0.5 2>/dev/null
    if [[ $? -eq 0 && -f "$wav" ]]; then
        echo "OK ($(du -h "$wav" | cut -f1))"
    else
        echo "ERREUR"
    fi
done

echo ""
echo "============================================"
echo "PHASE 2: WAV → OGG (processus Python séparés)"
echo "============================================"

SUCCESS=0
FAIL=0

for local in $(echo "${!TRACKS[@]}" | tr ' ' '\n' | sort); do
    midi="${TRACKS[$local]}"
    ogg="$MUSIC_DIR/${local}.ogg"
    wav="$MIDI_DIR/${midi}.wav"
    
    if [[ -f "$ogg" && $(stat -c%s "$ogg") -gt 500 ]]; then
        echo "  [SKIP] ${local}.ogg"
        SUCCESS=$((SUCCESS + 1))
        continue
    fi
    
    if [[ ! -f "$wav" ]]; then
        echo "  [MANQUANT WAV] $local ($midi)"
        FAIL=$((FAIL + 1))
        continue
    fi
    
    # Processus Python séparé pour chaque fichier (évite les segfaults)
    python3 -c "
import soundfile as sf
data, sr = sf.read('$wav')
sf.write('$ogg', data, sr, format='OGG', subtype='VORBIS')
import os
print(f'  ${local}.ogg → {os.path.getsize(\"$ogg\") // 1024} KB')
" 2>/dev/null
    
    if [[ $? -eq 0 && -f "$ogg" ]]; then
        SUCCESS=$((SUCCESS + 1))
    else
        echo "  ERREUR: ${local}.ogg"
        FAIL=$((FAIL + 1))
    fi
done

echo ""
echo "OGG: $SUCCESS OK, $FAIL échoués"
echo ""
echo "Nettoyage des WAV..."
rm -f "$MIDI_DIR"/*.wav
echo "Terminé !"
