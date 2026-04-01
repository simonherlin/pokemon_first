#!/usr/bin/env python3
"""
fix_shop_inventories.py — Ajoute les inventaires manquants aux boutiques
"""

import json, os, glob

MAPS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "maps")

# Inventaires correctes pour chaque boutique (fidèles RFVF, progresion)
SHOP_INVENTORIES = {
    "vendeur_jadielle": [
        "pokeball", "potion", "antidote", "anti_para", "reveil"
    ],
    "vendeur_azuria": [
        "pokeball", "superball", "potion", "super_potion", "antidote",
        "anti_para", "reveil", "anti_brule", "corde_sortie", "repousse"
    ],
    "vendeur_carmin": [
        "pokeball", "superball", "potion", "super_potion", "hyper_potion",
        "antidote", "anti_para", "total_soin", "rappel", "corde_sortie", "repousse"
    ],
    "vendeur_lavanville": [
        "pokeball", "superball", "potion", "super_potion", "antidote",
        "anti_para", "reveil", "corde_sortie", "super_repousse"
    ],
    "vendeur_safrania": [
        "pokeball", "superball", "hyperball", "potion", "super_potion",
        "hyper_potion", "max_potion", "total_soin", "rappel", "max_rappel",
        "anti_para", "anti_brule", "anti_gel", "corde_sortie", "super_repousse",
        "max_repousse"
    ],
    "vendeur_parmanie": [
        "pokeball", "superball", "hyperball", "potion", "super_potion",
        "hyper_potion", "antidote", "anti_para", "total_soin", "rappel",
        "corde_sortie", "super_repousse"
    ],
    "vendeur_cramoisile": [
        "pokeball", "superball", "hyperball", "potion", "super_potion",
        "hyper_potion", "max_potion", "total_soin", "rappel", "max_rappel",
        "anti_para", "anti_brule", "anti_gel", "reveil",
        "corde_sortie", "max_repousse"
    ],
    # Grand Magasin 1F — Objets de base + vitamines
    "vendeur_gm_1f": [
        "pokeball", "superball", "hyperball",
        "potion", "super_potion", "hyper_potion", "max_potion",
        "antidote", "anti_para", "anti_brule", "anti_gel", "reveil", "total_soin",
        "rappel", "max_rappel",
        "repousse", "super_repousse", "max_repousse",
        "corde_sortie",
        "proteine", "fer", "calcium", "carbone", "pv_plus"
    ],
    # Grand Magasin 2F — CT
    "vendeur_gm_2f_ct": [
        "ct01", "ct02", "ct03", "ct04", "ct05",
        "ct06", "ct07", "ct08", "ct09", "ct10",
        "ct11", "ct12", "ct13", "ct14", "ct15",
        "ct16", "ct17", "ct18", "ct19", "ct20",
        "ct21", "ct22", "ct23", "ct24", "ct25",
        "ct26", "ct27", "ct28", "ct29", "ct30",
        "ct31", "ct32", "ct33", "ct34", "ct35",
        "ct36", "ct37", "ct38", "ct39", "ct40",
        "ct41", "ct42", "ct43", "ct44", "ct45",
        "ct46", "ct47", "ct48", "ct49", "ct50"
    ],
    # Grand Magasin 2F — Pierres d'évolution
    "vendeur_gm_2f_pierres": [
        "pierre_feu", "pierre_eau", "pierre_foudre", "pierre_plante", "pierre_lune"
    ],
}


def fix_map(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    modified = False
    npcs = data.get("pnj", data.get("pnjs", data.get("npcs", [])))

    for npc in npcs:
        npc_id = npc.get("id", "")

        # Fix "stock" → "inventaire_boutique" (Carmin uses wrong key)
        if "stock" in npc and "inventaire_boutique" not in npc:
            npc["inventaire_boutique"] = npc.pop("stock")
            modified = True

        # Add missing inventories
        if npc_id in SHOP_INVENTORIES:
            old_inv = npc.get("inventaire_boutique", [])
            new_inv = SHOP_INVENTORIES[npc_id]
            if old_inv != new_inv:
                npc["inventaire_boutique"] = new_inv
                modified = True
                print(f"  📦 {npc_id}: {len(old_inv)} → {len(new_inv)} items")

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    return False


def main():
    count = 0
    for filepath in sorted(glob.glob(os.path.join(MAPS_DIR, "*.json"))):
        if fix_map(filepath):
            count += 1
            print(f"✅ {os.path.basename(filepath)}")

    print(f"\n🏪 {count} cartes mises à jour")


if __name__ == "__main__":
    main()
