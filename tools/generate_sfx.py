#!/usr/bin/env python3
"""Génère des effets sonores rétro style Game Boy pour le projet Pokémon.
Utilise numpy + soundfile pour créer des SFX authentiques en .ogg."""

import numpy as np
import soundfile as sf
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "audio", "sfx")
SAMPLE_RATE = 22050

def save_ogg(name: str, samples: np.ndarray):
    """Sauvegarde un tableau numpy en fichier OGG."""
    path = os.path.join(OUTPUT_DIR, f"{name}.ogg")
    # Normaliser entre -1 et 1
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.8
    sf.write(path, samples.astype(np.float32), SAMPLE_RATE, format='OGG', subtype='VORBIS')
    print(f"  ✓ {name}.ogg ({len(samples)/SAMPLE_RATE*1000:.0f}ms)")

def square_wave(freq: float, duration: float, duty: float = 0.5) -> np.ndarray:
    """Onde carrée style Game Boy."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return np.sign(np.sin(2 * np.pi * freq * t) - (1 - 2 * duty))

def noise_burst(duration: float) -> np.ndarray:
    """Bruit blanc (style canal noise GB)."""
    return np.random.uniform(-1, 1, int(SAMPLE_RATE * duration))

def envelope(samples: np.ndarray, attack: float = 0.005, decay: float = 0.0, release: float = 0.05) -> np.ndarray:
    """Applique une enveloppe ADSR simplifiée."""
    n = len(samples)
    env = np.ones(n)
    a_samples = int(attack * SAMPLE_RATE)
    r_samples = int(release * SAMPLE_RATE)
    if a_samples > 0:
        env[:a_samples] = np.linspace(0, 1, a_samples)
    if r_samples > 0:
        env[-r_samples:] = np.linspace(1, 0, r_samples)
    return samples * env

def pitch_sweep(start_freq: float, end_freq: float, duration: float) -> np.ndarray:
    """Balayage de fréquence (montant ou descendant)."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    freqs = np.linspace(start_freq, end_freq, len(t))
    phase = np.cumsum(freqs / SAMPLE_RATE) * 2 * np.pi
    return np.sign(np.sin(phase))

# === GÉNÉRATION DES SFX ===

def gen_cursor_move():
    """Blip court pour déplacement curseur."""
    s = square_wave(1200, 0.04, 0.25)
    return envelope(s, attack=0.002, release=0.015)

def gen_confirm():
    """Double bip ascendant pour confirmation."""
    s1 = square_wave(800, 0.06, 0.25)
    gap = np.zeros(int(SAMPLE_RATE * 0.02))
    s2 = square_wave(1200, 0.08, 0.25)
    s = np.concatenate([s1, gap, s2])
    return envelope(s, attack=0.003, release=0.03)

def gen_cancel():
    """Bip descendant pour annulation."""
    s1 = square_wave(900, 0.05, 0.25)
    gap = np.zeros(int(SAMPLE_RATE * 0.015))
    s2 = square_wave(500, 0.07, 0.25)
    s = np.concatenate([s1, gap, s2])
    return envelope(s, attack=0.003, release=0.03)

def gen_hit_normal():
    """Bruit d'impact normal."""
    n = noise_burst(0.08)
    # Filtrer grossièrement (atténuer les hautes fréquences)
    from scipy.signal import lfilter
    try:
        b = [0.3, 0.3, 0.4]
        n = lfilter(b, 1, n)
    except:
        pass
    return envelope(n, attack=0.002, release=0.04)

def gen_hit_super_effective():
    """Impact puissant — plus long et plus fort."""
    n1 = noise_burst(0.05) * 1.0
    s = square_wave(200, 0.05, 0.5) * 0.5
    n2 = noise_burst(0.08) * 0.7
    combined = np.concatenate([n1 + s[:len(n1)], n2])
    return envelope(combined, attack=0.002, release=0.05)

def gen_hit_not_effective():
    """Impact faible — court et sourd."""
    n = noise_burst(0.04) * 0.5
    s = square_wave(150, 0.04, 0.5) * 0.3
    combined = n + s
    return envelope(combined, attack=0.002, release=0.02)

def gen_miss():
    """Swoosh pour attaque ratée."""
    s = pitch_sweep(1500, 300, 0.15)
    n = noise_burst(0.15) * 0.3
    combined = s * 0.5 + n
    return envelope(combined, attack=0.01, release=0.06)

def gen_critical():
    """Son de coup critique — impact sec."""
    n = noise_burst(0.03)
    s = square_wave(800, 0.02, 0.125)
    gap = np.zeros(int(SAMPLE_RATE * 0.03))
    n2 = noise_burst(0.06)
    combined = np.concatenate([n, s, gap, n2])
    return envelope(combined, attack=0.001, release=0.03)

def gen_faint():
    """Son de KO — descente de fréquence."""
    s = pitch_sweep(800, 80, 0.5)
    return envelope(s, attack=0.01, release=0.15)

def gen_exp_gain():
    """Ticking d'expérience qui monte."""
    parts = []
    for i in range(8):
        freq = 600 + i * 50
        tick = square_wave(freq, 0.03, 0.25)
        gap = np.zeros(int(SAMPLE_RATE * 0.02))
        parts.extend([tick, gap])
    s = np.concatenate(parts)
    return envelope(s, attack=0.002, release=0.02)

def gen_level_up():
    """Arpège ascendant pour niveau gagné."""
    notes = [523, 659, 784, 1047]  # Do, Mi, Sol, Do (octave)
    parts = []
    for freq in notes:
        note = square_wave(freq, 0.1, 0.25)
        parts.append(note)
    # Note finale tenue
    final = square_wave(1047, 0.2, 0.25)
    parts.append(final)
    s = np.concatenate(parts)
    return envelope(s, attack=0.005, release=0.1)

def gen_ball_throw():
    """Whoosh de lancer de ball."""
    s = pitch_sweep(200, 1200, 0.15)
    n = noise_burst(0.15) * 0.4
    combined = s * 0.5 + n
    return envelope(combined, attack=0.01, release=0.05)

def gen_ball_shake():
    """Tremblement de ball."""
    parts = []
    for _ in range(3):
        tick = noise_burst(0.03)
        gap = np.zeros(int(SAMPLE_RATE * 0.08))
        parts.extend([tick, gap])
    s = np.concatenate(parts)
    return envelope(s, attack=0.002, release=0.01)

def gen_ball_click():
    """Clic de capture réussie."""
    s1 = square_wave(1500, 0.03, 0.125)
    gap = np.zeros(int(SAMPLE_RATE * 0.02))
    s2 = square_wave(2000, 0.05, 0.125)
    s = np.concatenate([s1, gap, s2])
    return envelope(s, attack=0.002, release=0.02)

def gen_low_hp():
    """Bip-bip d'alerte PV bas (3 bips)."""
    parts = []
    for _ in range(3):
        beep = square_wave(880, 0.08, 0.5)
        gap = np.zeros(int(SAMPLE_RATE * 0.12))
        parts.extend([beep, gap])
    s = np.concatenate(parts)
    return envelope(s, attack=0.003, release=0.02)

def gen_door():
    """Son de porte coulissante."""
    s = pitch_sweep(400, 800, 0.12)
    n = noise_burst(0.12) * 0.2
    combined = s * 0.4 + n
    return envelope(combined, attack=0.005, release=0.04)

def gen_wall_hit():
    """Thump contre un mur."""
    n = noise_burst(0.04)
    s = square_wave(100, 0.04, 0.5) * 0.5
    combined = n * 0.6 + s
    return envelope(combined, attack=0.001, release=0.02)

def gen_text_advance():
    """Clic doux pour avancer le texte."""
    s = square_wave(1000, 0.025, 0.125)
    return envelope(s, attack=0.002, release=0.01)

def gen_ledge():
    """Son de saut depuis un rebord."""
    s1 = square_wave(400, 0.05, 0.25)
    gap = np.zeros(int(SAMPLE_RATE * 0.03))
    s2 = pitch_sweep(600, 300, 0.1)
    combined = np.concatenate([s1, gap, s2])
    return envelope(combined, attack=0.005, release=0.04)

def gen_flee():
    """Son de fuite — montée rapide."""
    s = pitch_sweep(300, 1500, 0.2)
    return envelope(s, attack=0.01, release=0.08)

def gen_poison_field():
    """Dégât de poison sur le terrain."""
    s = square_wave(200, 0.08, 0.5)
    gap = np.zeros(int(SAMPLE_RATE * 0.05))
    s2 = square_wave(150, 0.1, 0.5)
    combined = np.concatenate([s, gap, s2])
    return envelope(combined, attack=0.005, release=0.05)

def gen_heal():
    """Son de soin — arpège doux ascendant."""
    notes = [440, 554, 659, 880]
    parts = []
    for freq in notes:
        note = square_wave(freq, 0.12, 0.125)
        note = envelope(note, attack=0.01, release=0.04)
        parts.append(note)
    return np.concatenate(parts)

def gen_stat_up():
    """Montée de stat — bip ascendant rapide."""
    s = pitch_sweep(400, 1200, 0.15)
    return envelope(s, attack=0.005, release=0.05)

def gen_stat_down():
    """Baisse de stat — bip descendant."""
    s = pitch_sweep(1200, 400, 0.15)
    return envelope(s, attack=0.005, release=0.05)

def gen_status_applied():
    """Statut appliqué (poison, paralysie, etc.)."""
    s1 = square_wave(300, 0.1, 0.5)
    gap = np.zeros(int(SAMPLE_RATE * 0.05))
    s2 = square_wave(250, 0.15, 0.5)
    combined = np.concatenate([s1, gap, s2])
    return envelope(combined, attack=0.005, release=0.08)

def gen_item_get():
    """Obtention d'objet — jingle court."""
    notes = [659, 784, 1047, 1319]  # Mi, Sol, Do, Mi (octave+)
    parts = []
    for i, freq in enumerate(notes):
        dur = 0.08 if i < 3 else 0.15
        note = square_wave(freq, dur, 0.25)
        parts.append(note)
    return envelope(np.concatenate(parts), attack=0.005, release=0.08)

def gen_save():
    """Son de sauvegarde."""
    s1 = square_wave(880, 0.1, 0.25)
    gap = np.zeros(int(SAMPLE_RATE * 0.05))
    s2 = square_wave(1100, 0.15, 0.25)
    combined = np.concatenate([s1, gap, s2])
    return envelope(combined, attack=0.005, release=0.06)

def gen_encounter():
    """Exclamation de rencontre (!)."""
    s = square_wave(1500, 0.06, 0.25)
    gap = np.zeros(int(SAMPLE_RATE * 0.03))
    s2 = square_wave(1800, 0.04, 0.25)
    combined = np.concatenate([s, gap, s2])
    return envelope(combined, attack=0.001, release=0.02)

# === MAIN ===
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    sfx_map = {
        # Menu / UI
        "cursor_move": gen_cursor_move,
        "confirm": gen_confirm,
        "cancel": gen_cancel,
        "text_advance": gen_text_advance,
        "save": gen_save,
        # Combat — impacts
        "hit_normal": gen_hit_normal,
        "hit_super_effective": gen_hit_super_effective,
        "hit_not_effective": gen_hit_not_effective,
        "miss": gen_miss,
        "critical": gen_critical,
        "faint": gen_faint,
        # Combat — progression
        "exp_gain": gen_exp_gain,
        "level_up": gen_level_up,
        "stat_up": gen_stat_up,
        "stat_down": gen_stat_down,
        "status_applied": gen_status_applied,
        # Capture
        "ball_throw": gen_ball_throw,
        "ball_shake": gen_ball_shake,
        "ball_click": gen_ball_click,
        # Alerte
        "low_hp": gen_low_hp,
        # Overworld
        "door": gen_door,
        "wall_hit": gen_wall_hit,
        "ledge": gen_ledge,
        "flee": gen_flee,
        "poison_field": gen_poison_field,
        "encounter": gen_encounter,
        # Items / soin
        "heal": gen_heal,
        "item_get": gen_item_get,
    }
    
    print(f"Génération de {len(sfx_map)} effets sonores...")
    ok = 0
    for name, generator in sfx_map.items():
        try:
            samples = generator()
            save_ogg(name, samples)
            ok += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
    
    print(f"\nTerminé: {ok}/{len(sfx_map)} SFX générés dans {OUTPUT_DIR}")
