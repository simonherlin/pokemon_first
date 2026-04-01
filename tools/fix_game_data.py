#!/usr/bin/env python3
"""
fix_game_data.py — Corrige et complète items.json et moves.json
- Supprime les doublons
- Normalise les structures d'effets
- Ajoute les 50 CT RFVF
- Ajoute les attaques manquantes Gen 1
- Corrige les catégories ('type' → 'categorie')
"""

import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===================================================================
# MOVES.JSON — Attaques complètes Gen 1 (165 attaques uniques)
# ===================================================================

MOVES = {
    # --- NORMAL ---
    "charge": {"id":"charge","nom":"Charge","nom_en":"Tackle","type":"normal","categorie":"physique","puissance":35,"precision":95,"pp":35,"priorite":0,"effet":None},
    "griffe": {"id":"griffe","nom":"Griffe","nom_en":"Scratch","type":"normal","categorie":"physique","puissance":40,"precision":100,"pp":35,"priorite":0,"effet":None},
    "ecras_face": {"id":"ecras_face","nom":"Écras'Face","nom_en":"Pound","type":"normal","categorie":"physique","puissance":40,"precision":100,"pp":35,"priorite":0,"effet":None},
    "vive_attaque": {"id":"vive_attaque","nom":"Vive-Attaque","nom_en":"Quick Attack","type":"normal","categorie":"physique","puissance":40,"precision":100,"pp":30,"priorite":1,"effet":None},
    "tranche": {"id":"tranche","nom":"Tranche","nom_en":"Slash","type":"normal","categorie":"physique","puissance":70,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"critique_eleve"}},
    "souplesse": {"id":"souplesse","nom":"Souplesse","nom_en":"Slam","type":"normal","categorie":"physique","puissance":80,"precision":75,"pp":20,"priorite":0,"effet":None},
    "plaquage": {"id":"plaquage","nom":"Plaquage","nom_en":"Body Slam","type":"normal","categorie":"physique","puissance":85,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":30}},
    "belier": {"id":"belier","nom":"Bélier","nom_en":"Take Down","type":"normal","categorie":"physique","puissance":90,"precision":85,"pp":20,"priorite":0,"effet":{"type_effet":"recul","pourcentage":25}},
    "damocles": {"id":"damocles","nom":"Damoclès","nom_en":"Double-Edge","type":"normal","categorie":"physique","puissance":100,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"recul","pourcentage":25}},
    "hyper_faisceau": {"id":"hyper_faisceau","nom":"Ultralaser","nom_en":"Hyper Beam","type":"normal","categorie":"special","puissance":150,"precision":90,"pp":5,"priorite":0,"effet":{"type_effet":"recharge"}},
    "force": {"id":"force","nom":"Force","nom_en":"Strength","type":"normal","categorie":"physique","puissance":80,"precision":100,"pp":15,"priorite":0,"effet":None},
    "coupe": {"id":"coupe","nom":"Coupe","nom_en":"Cut","type":"normal","categorie":"physique","puissance":50,"precision":95,"pp":30,"priorite":0,"effet":None},
    "mega_poing": {"id":"mega_poing","nom":"Méga Poing","nom_en":"Mega Punch","type":"normal","categorie":"physique","puissance":80,"precision":85,"pp":20,"priorite":0,"effet":None},
    "mega_pied": {"id":"mega_pied","nom":"Méga Pied","nom_en":"Mega Kick","type":"normal","categorie":"physique","puissance":120,"precision":75,"pp":5,"priorite":0,"effet":None},
    "etreinte": {"id":"etreinte","nom":"Étreinte","nom_en":"Vice Grip","type":"normal","categorie":"physique","puissance":55,"precision":100,"pp":30,"priorite":0,"effet":None},
    "poing_comete": {"id":"poing_comete","nom":"Poing Comète","nom_en":"Comet Punch","type":"normal","categorie":"physique","puissance":18,"precision":85,"pp":15,"priorite":0,"effet":{"type_effet":"multi_coups","min":2,"max":5}},
    "furie": {"id":"furie","nom":"Furie","nom_en":"Fury Attack","type":"normal","categorie":"physique","puissance":15,"precision":85,"pp":20,"priorite":0,"effet":{"type_effet":"multi_coups","min":2,"max":5}},
    "pilonnage": {"id":"pilonnage","nom":"Pilonnage","nom_en":"Barrage","type":"normal","categorie":"physique","puissance":15,"precision":85,"pp":20,"priorite":0,"effet":{"type_effet":"multi_coups","min":2,"max":5}},
    "double_gifle": {"id":"double_gifle","nom":"Double Gifle","nom_en":"Double Slap","type":"normal","categorie":"physique","puissance":15,"precision":85,"pp":10,"priorite":0,"effet":{"type_effet":"multi_coups","min":2,"max":5}},
    "craquement": {"id":"craquement","nom":"Ligotage","nom_en":"Wrap","type":"normal","categorie":"physique","puissance":15,"precision":85,"pp":20,"priorite":0,"effet":{"type_effet":"immobilisation","tours_min":2,"tours_max":5}},
    "morsure": {"id":"morsure","nom":"Morsure","nom_en":"Bite","type":"normal","categorie":"physique","puissance":60,"precision":100,"pp":25,"priorite":0,"effet":{"type_effet":"flinch","probabilite":30}},
    "super_croc": {"id":"super_croc","nom":"Croc de Mort","nom_en":"Super Fang","type":"normal","categorie":"physique","puissance":0,"precision":90,"pp":10,"priorite":0,"effet":{"type_effet":"demi_pv"}},
    "hyper_croc": {"id":"hyper_croc","nom":"Hyper Croc","nom_en":"Hyper Fang","type":"normal","categorie":"physique","puissance":80,"precision":90,"pp":15,"priorite":0,"effet":{"type_effet":"flinch","probabilite":10}},
    "jackpot": {"id":"jackpot","nom":"Jackpot","nom_en":"Pay Day","type":"normal","categorie":"physique","puissance":40,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"argent"}},
    "destruction": {"id":"destruction","nom":"Explosion","nom_en":"Explosion","type":"normal","categorie":"physique","puissance":170,"precision":100,"pp":5,"priorite":0,"effet":{"type_effet":"auto_ko"}},
    "auto_destruction": {"id":"auto_destruction","nom":"Destruction","nom_en":"Self-Destruct","type":"normal","categorie":"physique","puissance":130,"precision":100,"pp":5,"priorite":0,"effet":{"type_effet":"auto_ko"}},
    "triplattaque": {"id":"triplattaque","nom":"Triplattaque","nom_en":"Tri Attack","type":"normal","categorie":"special","puissance":80,"precision":100,"pp":10,"priorite":0,"effet":None},
    "eclaboussure": {"id":"eclaboussure","nom":"Trempette","nom_en":"Splash","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":40,"priorite":0,"effet":None},
    "morphing": {"id":"morphing","nom":"Morphing","nom_en":"Transform","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"morphing"}},
    "guillotine": {"id":"guillotine","nom":"Guillotine","nom_en":"Guillotine","type":"normal","categorie":"physique","puissance":0,"precision":30,"pp":5,"priorite":0,"effet":{"type_effet":"ohko"}},
    "rugissement": {"id":"rugissement","nom":"Rugissement","nom_en":"Growl","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":40,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"attaque","cible":"ennemi","stages":-1}},
    "groz_yeux": {"id":"groz_yeux","nom":"Groz'Yeux","nom_en":"Leer","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"ennemi","stages":-1}},
    "queue_fouet": {"id":"queue_fouet","nom":"Mimi-Queue","nom_en":"Tail Whip","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"ennemi","stages":-1}},
    "danse_lames": {"id":"danse_lames","nom":"Danse-Lames","nom_en":"Swords Dance","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"attaque","cible":"lanceur","stages":2}},
    "armure": {"id":"armure","nom":"Armure","nom_en":"Harden","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"lanceur","stages":1}},
    "defense_curl": {"id":"defense_curl","nom":"Boul'Armure","nom_en":"Defense Curl","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":40,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"lanceur","stages":1}},
    "affutage": {"id":"affutage","nom":"Affûtage","nom_en":"Sharpen","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"attaque","cible":"lanceur","stages":1}},
    "adaptation": {"id":"adaptation","nom":"Adaptation","nom_en":"Conversion","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":None},
    "tourbillon": {"id":"tourbillon","nom":"Cyclone","nom_en":"Whirlwind","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":-6,"effet":{"type_effet":"fuite_forcee"}},
    "entrave": {"id":"entrave","nom":"Entrave","nom_en":"Disable","type":"normal","categorie":"statut","puissance":0,"precision":55,"pp":20,"priorite":0,"effet":{"type_effet":"entrave"}},
    "ultrason": {"id":"ultrason","nom":"Ultrason","nom_en":"Supersonic","type":"normal","categorie":"statut","puissance":0,"precision":55,"pp":20,"priorite":0,"effet":{"type_effet":"statut","statut":"confusion","probabilite":100}},
    "berceuse": {"id":"berceuse","nom":"Berceuse","nom_en":"Sing","type":"normal","categorie":"statut","puissance":0,"precision":55,"pp":15,"priorite":0,"effet":{"type_effet":"statut","statut":"sommeil","probabilite":100}},
    "meteores": {"id":"meteores","nom":"Météores","nom_en":"Swift","type":"normal","categorie":"special","puissance":60,"precision":100,"pp":20,"priorite":0,"effet":None},
    "tornade": {"id":"tornade","nom":"Tornade","nom_en":"Gust","type":"normal","categorie":"special","puissance":40,"precision":100,"pp":35,"priorite":0,"effet":None},
    "ronflements": {"id":"ronflements","nom":"Ronflement","nom_en":"Snore","type":"normal","categorie":"special","puissance":40,"precision":100,"pp":15,"priorite":0,"effet":None},
    "e_coque": {"id":"e_coque","nom":"E-Coque","nom_en":"Softboiled","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"soin_pv","pourcentage":50}},
    "reflet": {"id":"reflet","nom":"Reflet","nom_en":"Double Team","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"esquive","cible":"lanceur","stages":1}},
    "puissance_cachee": {"id":"puissance_cachee","nom":"Puissance Cachée","nom_en":"Hidden Power","type":"normal","categorie":"special","puissance":60,"precision":100,"pp":15,"priorite":0,"effet":None},
    "retour": {"id":"retour","nom":"Retour","nom_en":"Return","type":"normal","categorie":"physique","puissance":102,"precision":100,"pp":20,"priorite":0,"effet":None},
    "frustration": {"id":"frustration","nom":"Frustration","nom_en":"Frustration","type":"normal","categorie":"physique","puissance":102,"precision":100,"pp":20,"priorite":0,"effet":None},
    "facade": {"id":"facade","nom":"Façade","nom_en":"Facade","type":"normal","categorie":"physique","puissance":70,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"double_si_statut"}},
    "force_cachee": {"id":"force_cachee","nom":"Force Cachée","nom_en":"Secret Power","type":"normal","categorie":"physique","puissance":70,"precision":100,"pp":20,"priorite":0,"effet":None},
    "attraction": {"id":"attraction","nom":"Attraction","nom_en":"Attract","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":15,"priorite":0,"effet":None},
    "provoc": {"id":"provoc","nom":"Provoc","nom_en":"Taunt","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":None},
    "larcin": {"id":"larcin","nom":"Larcin","nom_en":"Thief","type":"normal","categorie":"physique","puissance":40,"precision":100,"pp":10,"priorite":0,"effet":None},
    "hurlement": {"id":"hurlement","nom":"Hurlement","nom_en":"Roar","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":-6,"effet":{"type_effet":"fuite_forcee"}},

    # --- FEU ---
    "flammeche": {"id":"flammeche","nom":"Flammèche","nom_en":"Ember","type":"feu","categorie":"special","puissance":40,"precision":100,"pp":25,"priorite":0,"effet":{"type_effet":"statut","statut":"brulure","probabilite":10}},
    "lance_flamme": {"id":"lance_flamme","nom":"Lance-Flamme","nom_en":"Flamethrower","type":"feu","categorie":"special","puissance":95,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"statut","statut":"brulure","probabilite":10}},
    "deflagration": {"id":"deflagration","nom":"Déflagration","nom_en":"Fire Blast","type":"feu","categorie":"special","puissance":120,"precision":85,"pp":5,"priorite":0,"effet":{"type_effet":"statut","statut":"brulure","probabilite":10}},
    "surchauffe": {"id":"surchauffe","nom":"Surchauffe","nom_en":"Overheat","type":"feu","categorie":"special","puissance":140,"precision":90,"pp":5,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"special","cible":"lanceur","stages":-2}},
    "poing_de_feu": {"id":"poing_de_feu","nom":"Poing de Feu","nom_en":"Fire Punch","type":"feu","categorie":"physique","puissance":75,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"statut","statut":"brulure","probabilite":10}},
    "danse_flamme": {"id":"danse_flamme","nom":"Danse Flamme","nom_en":"Fire Spin","type":"feu","categorie":"special","puissance":15,"precision":70,"pp":15,"priorite":0,"effet":{"type_effet":"immobilisation","tours_min":2,"tours_max":5}},

    # --- EAU ---
    "pistolet_a_o": {"id":"pistolet_a_o","nom":"Pistolet à O","nom_en":"Water Gun","type":"eau","categorie":"special","puissance":40,"precision":100,"pp":25,"priorite":0,"effet":None},
    "bulles": {"id":"bulles","nom":"Écume","nom_en":"Bubble","type":"eau","categorie":"special","puissance":20,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"vitesse","cible":"ennemi","stages":-1,"probabilite":10}},
    "bulles_d_o": {"id":"bulles_d_o","nom":"Bulles d'O","nom_en":"Bubble Beam","type":"eau","categorie":"special","puissance":65,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"vitesse","cible":"ennemi","stages":-1,"probabilite":10}},
    "surf": {"id":"surf","nom":"Surf","nom_en":"Surf","type":"eau","categorie":"special","puissance":95,"precision":100,"pp":15,"priorite":0,"effet":None},
    "hydrocanon": {"id":"hydrocanon","nom":"Hydrocanon","nom_en":"Hydro Pump","type":"eau","categorie":"special","puissance":120,"precision":80,"pp":5,"priorite":0,"effet":None},
    "cascade": {"id":"cascade","nom":"Cascade","nom_en":"Waterfall","type":"eau","categorie":"physique","puissance":80,"precision":100,"pp":15,"priorite":0,"effet":None},
    "repli": {"id":"repli","nom":"Repli","nom_en":"Withdraw","type":"eau","categorie":"statut","puissance":0,"precision":100,"pp":40,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"lanceur","stages":1}},
    "crabe_marteau": {"id":"crabe_marteau","nom":"Pince-Masse","nom_en":"Crabhammer","type":"eau","categorie":"physique","puissance":90,"precision":85,"pp":10,"priorite":0,"effet":{"type_effet":"critique_eleve"}},
    "claquoir": {"id":"claquoir","nom":"Claquoir","nom_en":"Clamp","type":"eau","categorie":"physique","puissance":35,"precision":75,"pp":10,"priorite":0,"effet":{"type_effet":"immobilisation","tours_min":2,"tours_max":5}},
    "vibraqua": {"id":"vibraqua","nom":"Vibraqua","nom_en":"Water Pulse","type":"eau","categorie":"special","puissance":60,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"statut","statut":"confusion","probabilite":20}},
    "danse_pluie": {"id":"danse_pluie","nom":"Danse Pluie","nom_en":"Rain Dance","type":"eau","categorie":"statut","puissance":0,"precision":100,"pp":5,"priorite":0,"effet":None},

    # --- ELECTRIK ---
    "eclair": {"id":"eclair","nom":"Éclair","nom_en":"ThunderShock","type":"electrik","categorie":"special","puissance":40,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":10}},
    "tonnerre": {"id":"tonnerre","nom":"Tonnerre","nom_en":"Thunderbolt","type":"electrik","categorie":"special","puissance":95,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":10}},
    "foudre": {"id":"foudre","nom":"Fatal-Foudre","nom_en":"Thunder","type":"electrik","categorie":"special","puissance":120,"precision":70,"pp":10,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":30}},
    "onde_choc": {"id":"onde_choc","nom":"Cage-Éclair","nom_en":"Thunder Wave","type":"electrik","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":100}},
    "poing_eclair": {"id":"poing_eclair","nom":"Poing-Éclair","nom_en":"Thunder Punch","type":"electrik","categorie":"physique","puissance":75,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":10}},
    "onde_de_choc": {"id":"onde_de_choc","nom":"Onde de Choc","nom_en":"Shock Wave","type":"electrik","categorie":"special","puissance":60,"precision":100,"pp":20,"priorite":0,"effet":None},

    # --- PLANTE ---
    "fouet_lianes": {"id":"fouet_lianes","nom":"Fouet Lianes","nom_en":"Vine Whip","type":"plante","categorie":"physique","puissance":45,"precision":100,"pp":25,"priorite":0,"effet":None},
    "vampigraine": {"id":"vampigraine","nom":"Vampigraine","nom_en":"Leech Seed","type":"plante","categorie":"statut","puissance":0,"precision":90,"pp":10,"priorite":0,"effet":{"type_effet":"vampigraine"}},
    "mega_sangsue": {"id":"mega_sangsue","nom":"Méga-Sangsue","nom_en":"Mega Drain","type":"plante","categorie":"special","puissance":40,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"drain","pourcentage":50}},
    "giga_sangsue": {"id":"giga_sangsue","nom":"Giga-Sangsue","nom_en":"Giga Drain","type":"plante","categorie":"special","puissance":60,"precision":100,"pp":5,"priorite":0,"effet":{"type_effet":"drain","pourcentage":50}},
    "lance_soleil": {"id":"lance_soleil","nom":"Lance-Soleil","nom_en":"Solar Beam","type":"plante","categorie":"special","puissance":120,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"charge_tour","message":"absorbe la lumière !"}},
    "poudre_toxik": {"id":"poudre_toxik","nom":"Poudre Toxik","nom_en":"Poison Powder","type":"plante","categorie":"statut","puissance":0,"precision":75,"pp":35,"priorite":0,"effet":{"type_effet":"statut","statut":"poison","probabilite":100}},
    "poudre_dodo": {"id":"poudre_dodo","nom":"Poudre Dodo","nom_en":"Sleep Powder","type":"plante","categorie":"statut","puissance":0,"precision":75,"pp":15,"priorite":0,"effet":{"type_effet":"statut","statut":"sommeil","probabilite":100}},
    "danse_fleur": {"id":"danse_fleur","nom":"Danse-Fleur","nom_en":"Petal Dance","type":"plante","categorie":"special","puissance":70,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"multi_tour","tours":3,"confusion_apres":True}},
    "para_spore": {"id":"para_spore","nom":"Para-Spore","nom_en":"Stun Spore","type":"plante","categorie":"statut","puissance":0,"precision":75,"pp":30,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":100}},
    "tranch_herbe": {"id":"tranch_herbe","nom":"Tranch'Herbe","nom_en":"Razor Leaf","type":"plante","categorie":"physique","puissance":55,"precision":95,"pp":25,"priorite":0,"effet":{"type_effet":"critique_eleve"}},
    "balle_graine": {"id":"balle_graine","nom":"Balle Graine","nom_en":"Bullet Seed","type":"plante","categorie":"physique","puissance":10,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"multi_coups","min":2,"max":5}},

    # --- GLACE ---
    "laser_glace": {"id":"laser_glace","nom":"Laser Glace","nom_en":"Ice Beam","type":"glace","categorie":"special","puissance":95,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"statut","statut":"gel","probabilite":10}},
    "blizzard": {"id":"blizzard","nom":"Blizzard","nom_en":"Blizzard","type":"glace","categorie":"special","puissance":120,"precision":70,"pp":5,"priorite":0,"effet":{"type_effet":"statut","statut":"gel","probabilite":10}},
    "poing_glace": {"id":"poing_glace","nom":"Poing Glace","nom_en":"Ice Punch","type":"glace","categorie":"physique","puissance":75,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"statut","statut":"gel","probabilite":10}},
    "aurora": {"id":"aurora","nom":"Onde Boréale","nom_en":"Aurora Beam","type":"glace","categorie":"special","puissance":65,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"attaque","cible":"ennemi","stages":-1,"probabilite":10}},
    "brume": {"id":"brume","nom":"Brume","nom_en":"Mist","type":"glace","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":None},
    "buee_noire": {"id":"buee_noire","nom":"Buée Noire","nom_en":"Haze","type":"glace","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"reset_stats"}},
    "grele": {"id":"grele","nom":"Grêle","nom_en":"Hail","type":"glace","categorie":"statut","puissance":0,"precision":100,"pp":10,"priorite":0,"effet":None},

    # --- COMBAT ---
    "poing_karate": {"id":"poing_karate","nom":"Poing Karaté","nom_en":"Karate Chop","type":"combat","categorie":"physique","puissance":50,"precision":100,"pp":25,"priorite":0,"effet":{"type_effet":"critique_eleve"}},
    "double_pied": {"id":"double_pied","nom":"Double Pied","nom_en":"Double Kick","type":"combat","categorie":"physique","puissance":30,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"multi_frappe","nombre":2}},
    "balayage": {"id":"balayage","nom":"Balayage","nom_en":"Low Kick","type":"combat","categorie":"physique","puissance":50,"precision":100,"pp":20,"priorite":0,"effet":None},
    "sacrifice": {"id":"sacrifice","nom":"Sacrifice","nom_en":"Submission","type":"combat","categorie":"physique","puissance":80,"precision":80,"pp":25,"priorite":0,"effet":{"type_effet":"recul","pourcentage":25}},
    "pied_saute": {"id":"pied_saute","nom":"Pied Sauté","nom_en":"Jump Kick","type":"combat","categorie":"physique","puissance":70,"precision":95,"pp":25,"priorite":0,"effet":None},
    "pied_voltige": {"id":"pied_voltige","nom":"Pied Voltige","nom_en":"Hi Jump Kick","type":"combat","categorie":"physique","puissance":85,"precision":90,"pp":20,"priorite":0,"effet":{"type_effet":"recul_si_rate"}},
    "mawashi_geri": {"id":"mawashi_geri","nom":"Mawashi Geri","nom_en":"Rolling Kick","type":"combat","categorie":"physique","puissance":60,"precision":85,"pp":15,"priorite":0,"effet":None},
    "mitra_poing": {"id":"mitra_poing","nom":"Mitra-Poing","nom_en":"Focus Punch","type":"combat","categorie":"physique","puissance":150,"precision":100,"pp":20,"priorite":-3,"effet":None},
    "casse_brique": {"id":"casse_brique","nom":"Casse-Brique","nom_en":"Brick Break","type":"combat","categorie":"physique","puissance":75,"precision":100,"pp":15,"priorite":0,"effet":None},
    "gonflette": {"id":"gonflette","nom":"Gonflette","nom_en":"Bulk Up","type":"combat","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"attaque","cible":"lanceur","stages":1}},
    "plenitude": {"id":"plenitude","nom":"Plénitude","nom_en":"Calm Mind","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"special","cible":"lanceur","stages":1}},
    "riposte": {"id":"riposte","nom":"Riposte","nom_en":"Counter","type":"combat","categorie":"physique","puissance":0,"precision":100,"pp":20,"priorite":-5,"effet":{"type_effet":"riposte"}},

    # --- POISON ---
    "dard_venin": {"id":"dard_venin","nom":"Dard-Venin","nom_en":"Poison Sting","type":"poison","categorie":"physique","puissance":15,"precision":100,"pp":35,"priorite":0,"effet":{"type_effet":"statut","statut":"poison","probabilite":30}},
    "acide": {"id":"acide","nom":"Acide","nom_en":"Acid","type":"poison","categorie":"special","puissance":40,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"ennemi","stages":-1,"probabilite":10}},
    "detritus": {"id":"detritus","nom":"Détritus","nom_en":"Sludge","type":"poison","categorie":"special","puissance":65,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"statut","statut":"poison","probabilite":30}},
    "bombe_beurk": {"id":"bombe_beurk","nom":"Bombe Beurk","nom_en":"Sludge Bomb","type":"poison","categorie":"special","puissance":90,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"statut","statut":"poison","probabilite":30}},
    "smog": {"id":"smog","nom":"Smog","nom_en":"Smog","type":"poison","categorie":"special","puissance":20,"precision":70,"pp":20,"priorite":0,"effet":{"type_effet":"statut","statut":"poison","probabilite":40}},
    "toxik": {"id":"toxik","nom":"Toxik","nom_en":"Toxic","type":"poison","categorie":"statut","puissance":0,"precision":85,"pp":10,"priorite":0,"effet":{"type_effet":"statut","statut":"poison_grave","probabilite":100}},

    # --- SOL ---
    "seisme": {"id":"seisme","nom":"Séisme","nom_en":"Earthquake","type":"sol","categorie":"physique","puissance":100,"precision":100,"pp":10,"priorite":0,"effet":None},
    "tunnel": {"id":"tunnel","nom":"Tunnel","nom_en":"Dig","type":"sol","categorie":"physique","puissance":60,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"semi_invulnerable"}},
    "coup_de_boue": {"id":"coup_de_boue","nom":"Jet de Sable","nom_en":"Sand Attack","type":"sol","categorie":"statut","puissance":0,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"precision","cible":"ennemi","stages":-1}},
    "ossclub": {"id":"ossclub","nom":"Ossclub","nom_en":"Bone Club","type":"sol","categorie":"physique","puissance":65,"precision":85,"pp":20,"priorite":0,"effet":{"type_effet":"flinch","probabilite":10}},
    "osmerang": {"id":"osmerang","nom":"Osmerang","nom_en":"Bonemerang","type":"sol","categorie":"physique","puissance":50,"precision":90,"pp":10,"priorite":0,"effet":{"type_effet":"multi_frappe","nombre":2}},
    "fissure": {"id":"fissure","nom":"Fissure","nom_en":"Fissure","type":"sol","categorie":"physique","puissance":0,"precision":30,"pp":5,"priorite":0,"effet":{"type_effet":"ohko"}},
    "tempete_sable": {"id":"tempete_sable","nom":"Tempête de Sable","nom_en":"Sandstorm","type":"sol","categorie":"statut","puissance":0,"precision":100,"pp":10,"priorite":0,"effet":None},

    # --- VOL ---
    "vol": {"id":"vol","nom":"Vol","nom_en":"Fly","type":"vol","categorie":"physique","puissance":70,"precision":95,"pp":15,"priorite":0,"effet":{"type_effet":"semi_invulnerable"}},
    "aile_dacier": {"id":"aile_dacier","nom":"Cru-Aile","nom_en":"Wing Attack","type":"vol","categorie":"physique","puissance":60,"precision":100,"pp":35,"priorite":0,"effet":None},
    "bec_vrille": {"id":"bec_vrille","nom":"Bec Vrille","nom_en":"Drill Peck","type":"vol","categorie":"physique","puissance":80,"precision":100,"pp":20,"priorite":0,"effet":None},
    "picpic": {"id":"picpic","nom":"Picpic","nom_en":"Peck","type":"vol","categorie":"physique","puissance":35,"precision":100,"pp":35,"priorite":0,"effet":None},
    "brise_ciel": {"id":"brise_ciel","nom":"Piqué","nom_en":"Sky Attack","type":"vol","categorie":"physique","puissance":140,"precision":90,"pp":5,"priorite":0,"effet":{"type_effet":"charge_tour","message":"se prépare à attaquer !"}},
    "aeropique": {"id":"aeropique","nom":"Aéropique","nom_en":"Aerial Ace","type":"vol","categorie":"physique","puissance":60,"precision":100,"pp":20,"priorite":0,"effet":None},

    # --- PSY ---
    "choc_mental": {"id":"choc_mental","nom":"Choc Mental","nom_en":"Confusion","type":"psy","categorie":"special","puissance":50,"precision":100,"pp":25,"priorite":0,"effet":{"type_effet":"statut","statut":"confusion","probabilite":10}},
    "rafale_psy": {"id":"rafale_psy","nom":"Rafale Psy","nom_en":"Psybeam","type":"psy","categorie":"special","puissance":65,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"statut","statut":"confusion","probabilite":10}},
    "psyko": {"id":"psyko","nom":"Psyko","nom_en":"Psychic","type":"psy","categorie":"special","puissance":90,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"special","cible":"ennemi","stages":-1,"probabilite":33}},
    "devoreve": {"id":"devoreve","nom":"Dévorêve","nom_en":"Dream Eater","type":"psy","categorie":"special","puissance":100,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"drain","pourcentage":50}},
    "hypnose": {"id":"hypnose","nom":"Hypnose","nom_en":"Hypnosis","type":"psy","categorie":"statut","puissance":0,"precision":60,"pp":20,"priorite":0,"effet":{"type_effet":"statut","statut":"sommeil","probabilite":100}},
    "teleport": {"id":"teleport","nom":"Téléport","nom_en":"Teleport","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"fuite"}},
    "hate": {"id":"hate","nom":"Hâte","nom_en":"Agility","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"vitesse","cible":"lanceur","stages":2}},
    "protection": {"id":"protection","nom":"Protection","nom_en":"Barrier","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"lanceur","stages":2}},
    "amnesia": {"id":"amnesia","nom":"Amnésie","nom_en":"Amnesia","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"special","cible":"lanceur","stages":2}},
    "repos": {"id":"repos","nom":"Repos","nom_en":"Rest","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"soin_total_sommeil"}},
    "meditation": {"id":"meditation","nom":"Yoga","nom_en":"Meditate","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":40,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"attaque","cible":"lanceur","stages":1}},
    "mur_lumiere": {"id":"mur_lumiere","nom":"Mur Lumière","nom_en":"Light Screen","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":None},
    "reflet_psy": {"id":"reflet_psy","nom":"Protection","nom_en":"Reflect","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":None},
    "paranormale": {"id":"paranormale","nom":"Vague Psy","nom_en":"Psywave","type":"psy","categorie":"special","puissance":0,"precision":80,"pp":15,"priorite":0,"effet":{"type_effet":"degats_variables"}},
    "echange": {"id":"echange","nom":"Échange","nom_en":"Skill Swap","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":10,"priorite":0,"effet":None},

    # --- INSECTE ---
    "fil_venin": {"id":"fil_venin","nom":"Sécrétion","nom_en":"String Shot","type":"insecte","categorie":"statut","puissance":0,"precision":95,"pp":40,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"vitesse","cible":"ennemi","stages":-1}},
    "taillade": {"id":"taillade","nom":"Taillade","nom_en":"Fury Cutter","type":"insecte","categorie":"physique","puissance":10,"precision":95,"pp":20,"priorite":0,"effet":None},
    "agrippage": {"id":"agrippage","nom":"Dard-Nuée","nom_en":"Pin Missile","type":"insecte","categorie":"physique","puissance":14,"precision":85,"pp":20,"priorite":0,"effet":{"type_effet":"multi_coups","min":2,"max":5}},
    "double_dard": {"id":"double_dard","nom":"Double-Dard","nom_en":"Twineedle","type":"insecte","categorie":"physique","puissance":25,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"multi_frappe","nombre":2}},

    # --- ROCHE ---
    "tomberoche": {"id":"tomberoche","nom":"Tomberoche","nom_en":"Rock Tomb","type":"roche","categorie":"physique","puissance":50,"precision":80,"pp":10,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"vitesse","cible":"ennemi","stages":-1}},
    "eboulement": {"id":"eboulement","nom":"Éboulement","nom_en":"Rock Slide","type":"roche","categorie":"physique","puissance":75,"precision":90,"pp":10,"priorite":0,"effet":{"type_effet":"flinch","probabilite":30}},

    # --- SPECTRE ---
    "ombre_nocturne": {"id":"ombre_nocturne","nom":"Ombre Nocturne","nom_en":"Night Shade","type":"spectre","categorie":"special","puissance":0,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"degats_niveau"}},
    "lechouille": {"id":"lechouille","nom":"Léchouille","nom_en":"Lick","type":"spectre","categorie":"physique","puissance":20,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":30}},
    "onde_folie": {"id":"onde_folie","nom":"Onde Folie","nom_en":"Confuse Ray","type":"spectre","categorie":"statut","puissance":0,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"statut","statut":"confusion","probabilite":100}},
    "ball_ombre": {"id":"ball_ombre","nom":"Ball'Ombre","nom_en":"Shadow Ball","type":"spectre","categorie":"special","puissance":80,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"special","cible":"ennemi","stages":-1,"probabilite":20}},

    # --- DRAGON ---
    "draco_rage": {"id":"draco_rage","nom":"Draco-Rage","nom_en":"Dragon Rage","type":"dragon","categorie":"special","puissance":0,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"degats_fixes","valeur":40}},
    "danse_draco": {"id":"danse_draco","nom":"Danse Draco","nom_en":"Dragon Dance","type":"dragon","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"attaque","cible":"lanceur","stages":1}},
    "draco_griffe": {"id":"draco_griffe","nom":"Draco-Griffe","nom_en":"Dragon Claw","type":"dragon","categorie":"physique","puissance":80,"precision":100,"pp":15,"priorite":0,"effet":None},
    "colere": {"id":"colere","nom":"Colère","nom_en":"Outrage","type":"dragon","categorie":"physique","puissance":90,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"multi_tour","tours":3,"confusion_apres":True}},

    # --- Statuts utilitaires ---
    "encore": {"id":"encore","nom":"Encore","nom_en":"Encore","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":5,"priorite":0,"effet":None},
    "rune_protect": {"id":"rune_protect","nom":"Rune Protect","nom_en":"Safeguard","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":25,"priorite":0,"effet":None},
    "abri": {"id":"abri","nom":"Abri","nom_en":"Protect","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":10,"priorite":3,"effet":None},
    "tourment": {"id":"tourment","nom":"Tourment","nom_en":"Torment","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":15,"priorite":0,"effet":None},
    "zenith": {"id":"zenith","nom":"Zénith","nom_en":"Sunny Day","type":"feu","categorie":"statut","puissance":0,"precision":100,"pp":5,"priorite":0,"effet":None},
    "queue_de_fer": {"id":"queue_de_fer","nom":"Queue de Fer","nom_en":"Iron Tail","type":"normal","categorie":"physique","puissance":100,"precision":75,"pp":15,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"ennemi","stages":-1,"probabilite":30}},
    "aile_acier": {"id":"aile_acier","nom":"Aile d'Acier","nom_en":"Steel Wing","type":"normal","categorie":"physique","puissance":70,"precision":90,"pp":25,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"lanceur","stages":1,"probabilite":10}},
    # --- Aliases et attaques manquantes (référencées par les learnsets) ---
    # Alias pour les learnsets qui utilisent des IDs différents
    "avalanche": {"id":"avalanche","nom":"Avalanche","nom_en":"Avalanche","type":"glace","categorie":"physique","puissance":60,"precision":100,"pp":10,"priorite":-4,"effet":{"type_effet":"double_si_touche_avant"}},
    "ballonnade": {"id":"ballonnade","nom":"Pistolet à O","nom_en":"Water Gun","type":"eau","categorie":"special","puissance":40,"precision":100,"pp":25,"priorite":0,"effet":None},
    "bouclier": {"id":"bouclier","nom":"Protection","nom_en":"Barrier","type":"psy","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"lanceur","stages":2}},
    "brouillard": {"id":"brouillard","nom":"Brouillard","nom_en":"Smokescreen","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"precision","cible":"ennemi","stages":-1}},
    "bulles_do": {"id":"bulles_do","nom":"Bulles d'O","nom_en":"Bubble Beam","type":"eau","categorie":"special","puissance":65,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"vitesse","cible":"ennemi","stages":-1,"probabilite":10}},
    "cage_eclair": {"id":"cage_eclair","nom":"Cage-Éclair","nom_en":"Thunder Wave","type":"electrik","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":100}},
    "chant": {"id":"chant","nom":"Berceuse","nom_en":"Sing","type":"normal","categorie":"statut","puissance":0,"precision":55,"pp":15,"priorite":0,"effet":{"type_effet":"statut","statut":"sommeil","probabilite":100}},
    "confusion": {"id":"confusion","nom":"Choc Mental","nom_en":"Confusion","type":"psy","categorie":"special","puissance":50,"precision":100,"pp":25,"priorite":0,"effet":{"type_effet":"statut","statut":"confusion","probabilite":10}},
    "coup_bas": {"id":"coup_bas","nom":"Vive-Attaque","nom_en":"Quick Attack","type":"normal","categorie":"physique","puissance":40,"precision":100,"pp":30,"priorite":1,"effet":None},
    "cru_aile": {"id":"cru_aile","nom":"Cru-Aile","nom_en":"Wing Attack","type":"vol","categorie":"physique","puissance":60,"precision":100,"pp":35,"priorite":0,"effet":None},
    "dragon_rage": {"id":"dragon_rage","nom":"Draco-Rage","nom_en":"Dragon Rage","type":"dragon","categorie":"special","puissance":0,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"degats_fixes","valeur":40}},
    "ecrasement": {"id":"ecrasement","nom":"Écrasement","nom_en":"Stomp","type":"normal","categorie":"physique","puissance":65,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"flinch","probabilite":30}},
    "explosion_roc": {"id":"explosion_roc","nom":"Éboulement","nom_en":"Rock Slide","type":"roche","categorie":"physique","puissance":75,"precision":90,"pp":10,"priorite":0,"effet":{"type_effet":"flinch","probabilite":30}},
    "fatal_foudre": {"id":"fatal_foudre","nom":"Fatal-Foudre","nom_en":"Thunder","type":"electrik","categorie":"special","puissance":120,"precision":70,"pp":10,"priorite":0,"effet":{"type_effet":"statut","statut":"paralysie","probabilite":30}},
    "fil_vénin": {"id":"fil_vénin","nom":"Sécrétion","nom_en":"String Shot","type":"insecte","categorie":"statut","puissance":0,"precision":95,"pp":40,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"vitesse","cible":"ennemi","stages":-1}},
    "flammèche": {"id":"flammèche","nom":"Flammèche","nom_en":"Ember","type":"feu","categorie":"special","puissance":40,"precision":100,"pp":25,"priorite":0,"effet":{"type_effet":"statut","statut":"brulure","probabilite":10}},
    "grincement": {"id":"grincement","nom":"Grincement","nom_en":"Screech","type":"normal","categorie":"statut","puissance":0,"precision":85,"pp":40,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"ennemi","stages":-2}},
    "hyper_beam": {"id":"hyper_beam","nom":"Ultralaser","nom_en":"Hyper Beam","type":"normal","categorie":"special","puissance":150,"precision":90,"pp":5,"priorite":0,"effet":{"type_effet":"recharge"}},
    "jet_de_sable": {"id":"jet_de_sable","nom":"Jet de Sable","nom_en":"Sand Attack","type":"sol","categorie":"statut","puissance":0,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"precision","cible":"ennemi","stages":-1}},
    "lance_pierre": {"id":"lance_pierre","nom":"Jet-Pierres","nom_en":"Rock Throw","type":"roche","categorie":"physique","puissance":50,"precision":90,"pp":15,"priorite":0,"effet":None},
    "laser_plante": {"id":"laser_plante","nom":"Lance-Soleil","nom_en":"Solar Beam","type":"plante","categorie":"special","puissance":120,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"charge_tour","message":"absorbe la lumière !"}},
    "lier": {"id":"lier","nom":"Ligotage","nom_en":"Bind","type":"normal","categorie":"physique","puissance":15,"precision":75,"pp":20,"priorite":0,"effet":{"type_effet":"immobilisation","tours_min":2,"tours_max":5}},
    "ligotage": {"id":"ligotage","nom":"Ligotage","nom_en":"Wrap","type":"normal","categorie":"physique","puissance":15,"precision":85,"pp":20,"priorite":0,"effet":{"type_effet":"immobilisation","tours_min":2,"tours_max":5}},
    "lire_esprit": {"id":"lire_esprit","nom":"Dévorêve","nom_en":"Dream Eater","type":"psy","categorie":"special","puissance":100,"precision":100,"pp":15,"priorite":0,"effet":{"type_effet":"drain","pourcentage":50}},
    "mega_drain": {"id":"mega_drain","nom":"Méga-Sangsue","nom_en":"Mega Drain","type":"plante","categorie":"special","puissance":40,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"drain","pourcentage":50}},
    "mimi_queue": {"id":"mimi_queue","nom":"Mimi-Queue","nom_en":"Tail Whip","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":30,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"defense","cible":"ennemi","stages":-1}},
    "ouragan": {"id":"ouragan","nom":"Ouragan","nom_en":"Gust","type":"vol","categorie":"special","puissance":40,"precision":100,"pp":35,"priorite":0,"effet":None},
    "soin": {"id":"soin","nom":"Soin","nom_en":"Recover","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":20,"priorite":0,"effet":{"type_effet":"soin_pv","pourcentage":50}},
    "synthese": {"id":"synthese","nom":"Synthèse","nom_en":"Synthesis","type":"plante","categorie":"statut","puissance":0,"precision":100,"pp":5,"priorite":0,"effet":{"type_effet":"soin_pv","pourcentage":50}},
    "séisme": {"id":"séisme","nom":"Séisme","nom_en":"Earthquake","type":"sol","categorie":"physique","puissance":100,"precision":100,"pp":10,"priorite":0,"effet":None},
    "trempette": {"id":"trempette","nom":"Trempette","nom_en":"Splash","type":"normal","categorie":"statut","puissance":0,"precision":100,"pp":40,"priorite":0,"effet":None},
    "ultimapoing": {"id":"ultimapoing","nom":"Ultimapoing","nom_en":"Dizzy Punch","type":"normal","categorie":"physique","puissance":70,"precision":100,"pp":10,"priorite":0,"effet":{"type_effet":"statut","statut":"confusion","probabilite":20}},
    "ultralaser": {"id":"ultralaser","nom":"Ultralaser","nom_en":"Hyper Beam","type":"normal","categorie":"special","puissance":150,"precision":90,"pp":5,"priorite":0,"effet":{"type_effet":"recharge"}},
    "flash": {"id":"flash","nom":"Flash","nom_en":"Flash","type":"normal","categorie":"statut","puissance":0,"precision":70,"pp":20,"priorite":0,"effet":{"type_effet":"modif_stat","stat":"precision","cible":"ennemi","stages":-1}},
}


# ===================================================================
# ITEMS.JSON — Tous les objets + 50 CT RFVF
# ===================================================================

# 50 CT RFVF avec les IDs d'attaque correspondants et prix au Grand Magasin
TMS = {
    "ct01": {"num":1,"nom":"CT01 Mitra-Poing","attaque":"mitra_poing","prix":3000},
    "ct02": {"num":2,"nom":"CT02 Draco-Griffe","attaque":"draco_griffe","prix":3000},
    "ct03": {"num":3,"nom":"CT03 Vibraqua","attaque":"vibraqua","prix":3000},
    "ct04": {"num":4,"nom":"CT04 Plénitude","attaque":"plenitude","prix":3000},
    "ct05": {"num":5,"nom":"CT05 Hurlement","attaque":"hurlement","prix":1000},
    "ct06": {"num":6,"nom":"CT06 Toxik","attaque":"toxik","prix":3000},
    "ct07": {"num":7,"nom":"CT07 Grêle","attaque":"grele","prix":3000},
    "ct08": {"num":8,"nom":"CT08 Gonflette","attaque":"gonflette","prix":3000},
    "ct09": {"num":9,"nom":"CT09 Balle Graine","attaque":"balle_graine","prix":3000},
    "ct10": {"num":10,"nom":"CT10 Puissance Cachée","attaque":"puissance_cachee","prix":3000},
    "ct11": {"num":11,"nom":"CT11 Zénith","attaque":"zenith","prix":2000},
    "ct12": {"num":12,"nom":"CT12 Provoc","attaque":"provoc","prix":3000},
    "ct13": {"num":13,"nom":"CT13 Laser Glace","attaque":"laser_glace","prix":5500},
    "ct14": {"num":14,"nom":"CT14 Blizzard","attaque":"blizzard","prix":5500},
    "ct15": {"num":15,"nom":"CT15 Ultralaser","attaque":"hyper_faisceau","prix":7500},
    "ct16": {"num":16,"nom":"CT16 Mur Lumière","attaque":"mur_lumiere","prix":3000},
    "ct17": {"num":17,"nom":"CT17 Abri","attaque":"abri","prix":3000},
    "ct18": {"num":18,"nom":"CT18 Danse Pluie","attaque":"danse_pluie","prix":2000},
    "ct19": {"num":19,"nom":"CT19 Giga-Sangsue","attaque":"giga_sangsue","prix":3000},
    "ct20": {"num":20,"nom":"CT20 Rune Protect","attaque":"rune_protect","prix":3000},
    "ct21": {"num":21,"nom":"CT21 Frustration","attaque":"frustration","prix":1000},
    "ct22": {"num":22,"nom":"CT22 Lance-Soleil","attaque":"lance_soleil","prix":3000},
    "ct23": {"num":23,"nom":"CT23 Queue de Fer","attaque":"queue_de_fer","prix":3000},
    "ct24": {"num":24,"nom":"CT24 Tonnerre","attaque":"tonnerre","prix":4000},
    "ct25": {"num":25,"nom":"CT25 Fatal-Foudre","attaque":"foudre","prix":5500},
    "ct26": {"num":26,"nom":"CT26 Séisme","attaque":"seisme","prix":6000},
    "ct27": {"num":27,"nom":"CT27 Retour","attaque":"retour","prix":1000},
    "ct28": {"num":28,"nom":"CT28 Tunnel","attaque":"tunnel","prix":2000},
    "ct29": {"num":29,"nom":"CT29 Psyko","attaque":"psyko","prix":4000},
    "ct30": {"num":30,"nom":"CT30 Ball'Ombre","attaque":"ball_ombre","prix":3000},
    "ct31": {"num":31,"nom":"CT31 Casse-Brique","attaque":"casse_brique","prix":3000},
    "ct32": {"num":32,"nom":"CT32 Reflet","attaque":"reflet","prix":2000},
    "ct33": {"num":33,"nom":"CT33 Protection","attaque":"reflet_psy","prix":3000},
    "ct34": {"num":34,"nom":"CT34 Onde de Choc","attaque":"onde_de_choc","prix":3000},
    "ct35": {"num":35,"nom":"CT35 Lance-Flamme","attaque":"lance_flamme","prix":4000},
    "ct36": {"num":36,"nom":"CT36 Bombe Beurk","attaque":"bombe_beurk","prix":3000},
    "ct37": {"num":37,"nom":"CT37 Tempête de Sable","attaque":"tempete_sable","prix":2000},
    "ct38": {"num":38,"nom":"CT38 Déflagration","attaque":"deflagration","prix":5500},
    "ct39": {"num":39,"nom":"CT39 Tomberoche","attaque":"tomberoche","prix":3000},
    "ct40": {"num":40,"nom":"CT40 Aéropique","attaque":"aeropique","prix":3000},
    "ct41": {"num":41,"nom":"CT41 Tourment","attaque":"tourment","prix":1500},
    "ct42": {"num":42,"nom":"CT42 Façade","attaque":"facade","prix":3000},
    "ct43": {"num":43,"nom":"CT43 Force Cachée","attaque":"force_cachee","prix":3000},
    "ct44": {"num":44,"nom":"CT44 Repos","attaque":"repos","prix":3000},
    "ct45": {"num":45,"nom":"CT45 Attraction","attaque":"attraction","prix":3000},
    "ct46": {"num":46,"nom":"CT46 Larcin","attaque":"larcin","prix":3000},
    "ct47": {"num":47,"nom":"CT47 Aile d'Acier","attaque":"aile_acier","prix":3000},
    "ct48": {"num":48,"nom":"CT48 Échange","attaque":"echange","prix":3000},
    "ct49": {"num":49,"nom":"CT49 Surchauffe","attaque":"surchauffe","prix":5500},
    "ct50": {"num":50,"nom":"CT50 Surchauffe","attaque":"surchauffe","prix":5500},
}

# Objets de base (nettoyés / normalisés)
BASE_ITEMS = {
    # --- SOINS ---
    "potion": {"id":"potion","nom":"Potion","categorie":"objets","prix":300,"description":"Restaure 20 PV à un Pokémon.","effet":{"type":"soin_pv","montant":20},"utilisable_combat":True},
    "super_potion": {"id":"super_potion","nom":"Super Potion","categorie":"objets","prix":700,"description":"Restaure 50 PV à un Pokémon.","effet":{"type":"soin_pv","montant":50},"utilisable_combat":True},
    "hyper_potion": {"id":"hyper_potion","nom":"Hyper Potion","categorie":"objets","prix":1200,"description":"Restaure 200 PV à un Pokémon.","effet":{"type":"soin_pv","montant":200},"utilisable_combat":True},
    "max_potion": {"id":"max_potion","nom":"Potion Max","categorie":"objets","prix":2500,"description":"Restaure tous les PV d'un Pokémon.","effet":{"type":"soin_pv","montant":9999},"utilisable_combat":True},
    "eau_fraiche": {"id":"eau_fraiche","nom":"Eau Fraîche","categorie":"objets","prix":200,"description":"Restaure 50 PV à un Pokémon.","effet":{"type":"soin_pv","montant":50},"utilisable_combat":True},
    "soda_cool": {"id":"soda_cool","nom":"Soda Cool","categorie":"objets","prix":300,"description":"Restaure 60 PV à un Pokémon.","effet":{"type":"soin_pv","montant":60},"utilisable_combat":True},
    "limonade": {"id":"limonade","nom":"Limonade","categorie":"objets","prix":350,"description":"Restaure 80 PV à un Pokémon.","effet":{"type":"soin_pv","montant":80},"utilisable_combat":True},
    "lait_meumeu": {"id":"lait_meumeu","nom":"Lait Meumeu","categorie":"objets","prix":500,"description":"Restaure 100 PV à un Pokémon.","effet":{"type":"soin_pv","montant":100},"utilisable_combat":True},

    # --- ANTIDOTES ---
    "antidote": {"id":"antidote","nom":"Antidote","categorie":"objets","prix":100,"description":"Guérit un Pokémon empoisonné.","effet":{"type":"guerison_statut","statut":"poison"},"utilisable_combat":True},
    "anti_brulure": {"id":"anti_brulure","nom":"Anti-Brûle","categorie":"objets","prix":250,"description":"Guérit un Pokémon brûlé.","effet":{"type":"guerison_statut","statut":"brulure"},"utilisable_combat":True},
    "anti_gel": {"id":"anti_gel","nom":"Antigel","categorie":"objets","prix":250,"description":"Décongèle un Pokémon gelé.","effet":{"type":"guerison_statut","statut":"gel"},"utilisable_combat":True},
    "anti_para": {"id":"anti_para","nom":"Anti-Para","categorie":"objets","prix":200,"description":"Guérit un Pokémon paralysé.","effet":{"type":"guerison_statut","statut":"paralysie"},"utilisable_combat":True},
    "reveil": {"id":"reveil","nom":"Réveil","categorie":"objets","prix":250,"description":"Réveille un Pokémon endormi.","effet":{"type":"guerison_statut","statut":"sommeil"},"utilisable_combat":True},
    "total_soin": {"id":"total_soin","nom":"Total Soin","categorie":"objets","prix":600,"description":"Guérit tous les problèmes de statut d'un Pokémon.","effet":{"type":"soin_total"},"utilisable_combat":True},

    # --- RAPPEL ---
    "rappel": {"id":"rappel","nom":"Rappel","categorie":"objets","prix":1500,"description":"Ranime un Pokémon KO avec la moitié de ses PV.","effet":{"type":"rappel","montant":50},"utilisable_combat":True},
    "max_rappel": {"id":"max_rappel","nom":"Rappel Max","categorie":"objets","prix":4000,"description":"Ranime un Pokémon KO avec tous ses PV.","effet":{"type":"rappel","montant":100},"utilisable_combat":True},

    # --- PP ---
    "huile": {"id":"huile","nom":"Huile","categorie":"objets","prix":0,"description":"Restaure 10 PP d'une attaque d'un Pokémon.","effet":{"type":"soin_pp","montant":10},"utilisable_combat":True},
    "elixir": {"id":"elixir","nom":"Élixir","categorie":"objets","prix":0,"description":"Restaure 10 PP de toutes les attaques d'un Pokémon.","effet":{"type":"soin_pp_all","montant":10},"utilisable_combat":True},
    "huile_max": {"id":"huile_max","nom":"Huile Max","categorie":"objets","prix":0,"description":"Restaure tous les PP d'une attaque.","effet":{"type":"soin_pp","montant":999},"utilisable_combat":True},
    "max_elixir": {"id":"max_elixir","nom":"Max Élixir","categorie":"objets","prix":0,"description":"Restaure tous les PP de toutes les attaques.","effet":{"type":"soin_pp_all","montant":999},"utilisable_combat":True},

    # --- REPOUSSE ---
    "repousse": {"id":"repousse","nom":"Repousse","categorie":"objets","prix":350,"description":"Éloigne les Pokémon sauvages faibles pendant 100 pas.","effet":{"type":"repousse","pas":100},"utilisable_combat":False},
    "super_repousse": {"id":"super_repousse","nom":"Super Repousse","categorie":"objets","prix":500,"description":"Éloigne les Pokémon sauvages faibles pendant 200 pas.","effet":{"type":"repousse","pas":200},"utilisable_combat":False},
    "max_repousse": {"id":"max_repousse","nom":"Max Repousse","categorie":"objets","prix":700,"description":"Éloigne les Pokémon sauvages faibles pendant 250 pas.","effet":{"type":"repousse","pas":250},"utilisable_combat":False},

    # --- DIVERS ---
    "corde_sortie": {"id":"corde_sortie","nom":"Corde Sortie","categorie":"objets","prix":550,"description":"Permet de fuir instantanément d'une grotte.","effet":{"type":"fuite_donjon"},"utilisable_combat":False},
    "pepite": {"id":"pepite","nom":"Pépite","categorie":"objets","prix":5000,"description":"Une pépite d'or pur. Peut être vendue à bon prix.","effet":None,"utilisable_combat":False},
    "super_bonbon": {"id":"super_bonbon","nom":"Super Bonbon","categorie":"objets","prix":0,"description":"Monte le niveau du Pokémon d'un cran.","effet":{"type":"niveau_plus_1"},"utilisable_combat":False},
    "pp_plus": {"id":"pp_plus","nom":"PP Plus","categorie":"objets","prix":0,"description":"Augmente les PP max d'une attaque d'un Pokémon.","effet":{"type":"pp_plus"},"utilisable_combat":False},
    "calcium": {"id":"calcium","nom":"Calcium","categorie":"objets","prix":9800,"description":"Augmente le Spécial d'un Pokémon.","effet":{"type":"ev_boost","stat":"special"},"utilisable_combat":False},
    "fer": {"id":"fer","nom":"Fer","categorie":"objets","prix":9800,"description":"Augmente la Défense d'un Pokémon.","effet":{"type":"ev_boost","stat":"defense"},"utilisable_combat":False},
    "proteine": {"id":"proteine","nom":"Protéine","categorie":"objets","prix":9800,"description":"Augmente l'Attaque d'un Pokémon.","effet":{"type":"ev_boost","stat":"attaque"},"utilisable_combat":False},
    "carbone": {"id":"carbone","nom":"Carbone","categorie":"objets","prix":9800,"description":"Augmente la Vitesse d'un Pokémon.","effet":{"type":"ev_boost","stat":"vitesse"},"utilisable_combat":False},
    "pv_plus": {"id":"pv_plus","nom":"PV Plus","categorie":"objets","prix":9800,"description":"Augmente les PV max d'un Pokémon.","effet":{"type":"ev_boost","stat":"pv"},"utilisable_combat":False},

    # --- BALLS ---
    "pokeball": {"id":"pokeball","nom":"Poké Ball","categorie":"balls","prix":200,"description":"Une Ball pour attraper les Pokémon sauvages.","effet":{"type":"capture","multiplicateur":1.0},"utilisable_combat":True},
    "superball": {"id":"superball","nom":"Super Ball","categorie":"balls","prix":600,"description":"Une Ball plus performante qu'une Poké Ball.","effet":{"type":"capture","multiplicateur":1.5},"utilisable_combat":True},
    "hyperball": {"id":"hyperball","nom":"Hyper Ball","categorie":"balls","prix":1200,"description":"Une Ball très performante.","effet":{"type":"capture","multiplicateur":2.0},"utilisable_combat":True},
    "masterball": {"id":"masterball","nom":"Master Ball","categorie":"balls","prix":0,"description":"La meilleure Ball. Capture à coup sûr.","effet":{"type":"capture","multiplicateur":999.0},"utilisable_combat":True},
    "safari_ball": {"id":"safari_ball","nom":"Safari Ball","categorie":"balls","prix":0,"description":"Une Ball spéciale du Parc Safari.","effet":{"type":"capture","multiplicateur":1.5},"utilisable_combat":True},

    # --- PIERRES D'ÉVOLUTION ---
    "pierre_feu": {"id":"pierre_feu","nom":"Pierre Feu","categorie":"objets","prix":2100,"description":"Fait évoluer certains Pokémon de type Feu.","effet":{"type":"pierre_evolution","pierre":"pierre_feu"},"utilisable_combat":False},
    "pierre_eau": {"id":"pierre_eau","nom":"Pierre Eau","categorie":"objets","prix":2100,"description":"Fait évoluer certains Pokémon de type Eau.","effet":{"type":"pierre_evolution","pierre":"pierre_eau"},"utilisable_combat":False},
    "pierre_foudre": {"id":"pierre_foudre","nom":"Pierre Foudre","categorie":"objets","prix":2100,"description":"Fait évoluer certains Pokémon de type Électrik.","effet":{"type":"pierre_evolution","pierre":"pierre_foudre"},"utilisable_combat":False},
    "pierre_plante": {"id":"pierre_plante","nom":"Pierre Plante","categorie":"objets","prix":2100,"description":"Fait évoluer certains Pokémon de type Plante.","effet":{"type":"pierre_evolution","pierre":"pierre_plante"},"utilisable_combat":False},
    "pierre_lune": {"id":"pierre_lune","nom":"Pierre Lune","categorie":"objets","prix":0,"description":"Fait évoluer certains Pokémon spéciaux.","effet":{"type":"pierre_evolution","pierre":"pierre_lune"},"utilisable_combat":False},

    # --- OBJETS CLÉS ---
    "colis_chen": {"id":"colis_chen","nom":"Colis du Prof. Chen","categorie":"objets_cles","prix":0,"description":"Un colis pour le Professeur Chen.","effet":None,"utilisable_combat":False},
    "pokedex": {"id":"pokedex","nom":"Pokédex","categorie":"objets_cles","prix":0,"description":"Un appareil high-tech du Professeur Chen.","effet":None,"utilisable_combat":False},
    "ticket_oceane": {"id":"ticket_oceane","nom":"Ticket Océane","categorie":"objets_cles","prix":0,"description":"Un billet pour le luxueux navire Océane.","effet":None,"utilisable_combat":False},
    "scope_sylphe": {"id":"scope_sylphe","nom":"Scope Sylphe","categorie":"objets_cles","prix":0,"description":"Permet d'identifier les spectres.","effet":None,"utilisable_combat":False},
    "poke_flute": {"id":"poke_flute","nom":"Poké Flûte","categorie":"objets_cles","prix":0,"description":"Réveille les Pokémon endormis.","effet":{"type":"guerison_statut","statut":"sommeil"},"utilisable_combat":True},
    "dent_or": {"id":"dent_or","nom":"Dent d'Or","categorie":"objets_cles","prix":0,"description":"La prothèse dentaire du gardien du Parc Safari.","effet":None,"utilisable_combat":False},
    "cle_ascenseur": {"id":"cle_ascenseur","nom":"Clé Ascenseur","categorie":"objets_cles","prix":0,"description":"Clé de l'ascenseur du repaire Rocket.","effet":None,"utilisable_combat":False},
    "cle_arene_cramoisile": {"id":"cle_arene_cramoisile","nom":"Clé Secrète","categorie":"objets_cles","prix":0,"description":"Ouvre l'Arène de Cramois'Île.","effet":None,"utilisable_combat":False},
    "jeton_casino": {"id":"jeton_casino","nom":"Porte-Jetons","categorie":"objets_cles","prix":0,"description":"Un étui pour les jetons du Casino.","effet":None,"utilisable_combat":False},
    "fossile_dome": {"id":"fossile_dome","nom":"Fossile Dôme","categorie":"objets_cles","prix":0,"description":"Fossile d'un ancien Pokémon (Kabuto).","effet":None,"utilisable_combat":False},
    "fossile_helix": {"id":"fossile_helix","nom":"Fossile Nautile","categorie":"objets_cles","prix":0,"description":"Fossile d'un ancien Pokémon (Amonita).","effet":None,"utilisable_combat":False},
    "fossile_ambre": {"id":"fossile_ambre","nom":"Vieil Ambre","categorie":"objets_cles","prix":0,"description":"Ambre contenant l'ADN d'un Pokémon ancien (Ptéra).","effet":None,"utilisable_combat":False},
    "canne_a_peche": {"id":"canne_a_peche","nom":"Canne","categorie":"objets_cles","prix":0,"description":"Une vieille canne pour pêcher des Pokémon.","effet":None,"utilisable_combat":False},
    "super_canne": {"id":"super_canne","nom":"Super Canne","categorie":"objets_cles","prix":0,"description":"Une bonne canne pour pêcher.","effet":None,"utilisable_combat":False},
    "mega_canne": {"id":"mega_canne","nom":"Méga Canne","categorie":"objets_cles","prix":0,"description":"La meilleure canne à pêche.","effet":None,"utilisable_combat":False},

    # --- CS ---
    "cs01_coupe": {"id":"cs01_coupe","nom":"CS01 Coupe","categorie":"ct_cs","prix":0,"description":"Apprend Coupe. Coupe les arbustes hors combat.","effet":{"type":"apprendre_attaque","attaque_id":"coupe"},"utilisable_combat":False},
    "cs02_vol": {"id":"cs02_vol","nom":"CS02 Vol","categorie":"ct_cs","prix":0,"description":"Apprend Vol. Permet de voler vers une ville visitée.","effet":{"type":"apprendre_attaque","attaque_id":"vol"},"utilisable_combat":False},
    "cs03_surf": {"id":"cs03_surf","nom":"CS03 Surf","categorie":"ct_cs","prix":0,"description":"Apprend Surf. Permet de naviguer sur l'eau.","effet":{"type":"apprendre_attaque","attaque_id":"surf"},"utilisable_combat":False},
    "cs04_force": {"id":"cs04_force","nom":"CS04 Force","categorie":"ct_cs","prix":0,"description":"Apprend Force. Permet de pousser les rochers.","effet":{"type":"apprendre_attaque","attaque_id":"force"},"utilisable_combat":False},
    "cs05_flash": {"id":"cs05_flash","nom":"CS05 Flash","categorie":"ct_cs","prix":0,"description":"Apprend Flash. Éclaire les grottes sombres.","effet":{"type":"apprendre_attaque","attaque_id":"flash"},"utilisable_combat":False},
}


def main():
    # === ÉCRIRE MOVES.JSON ===
    moves_path = os.path.join(BASE, "data", "pokemon", "moves.json")
    with open(moves_path, "w", encoding="utf-8") as f:
        json.dump(MOVES, f, ensure_ascii=False, indent=2)
    print(f"✅ moves.json : {len(MOVES)} attaques (doublons supprimés, effets normalisés)")

    # === CONSTRUIRE ITEMS.JSON ===
    items = dict(BASE_ITEMS)

    # Ajouter les 50 CT
    for ct_id, ct_data in TMS.items():
        items[ct_id] = {
            "id": ct_id,
            "nom": ct_data["nom"],
            "categorie": "ct_cs",
            "prix": ct_data["prix"],
            "description": f"Apprend l'attaque {MOVES[ct_data['attaque']]['nom']} à un Pokémon.",
            "effet": {
                "type": "apprendre_attaque",
                "attaque_id": ct_data["attaque"]
            },
            "utilisable_combat": False
        }

    items_path = os.path.join(BASE, "data", "items.json")
    with open(items_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    ct_count = sum(1 for k in items if k.startswith("ct"))
    cs_count = sum(1 for k in items if k.startswith("cs"))
    obj_count = sum(1 for k, v in items.items() if v.get("categorie") == "objets")
    ball_count = sum(1 for k, v in items.items() if v.get("categorie") == "balls")
    key_count = sum(1 for k, v in items.items() if v.get("categorie") == "objets_cles")
    print(f"✅ items.json : {len(items)} objets total")
    print(f"   {ct_count} CT + {cs_count} CS, {obj_count} objets, {ball_count} balls, {key_count} objets clés")
    print(f"   Doublons supprimés : master_ball, total_soin/soin_total, cs_coupe, ct_* duplicates")


if __name__ == "__main__":
    main()
