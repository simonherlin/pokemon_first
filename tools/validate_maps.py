#!/usr/bin/env python3
"""Validate map data: check reciprocal warps and connexions."""
import json
import os
import sys

MAPS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'maps')

def load_all_maps():
    maps = {}
    for fname in sorted(os.listdir(MAPS_DIR)):
        if not fname.endswith('.json'):
            continue
        map_id = fname.replace('.json', '')
        with open(os.path.join(MAPS_DIR, fname), 'r', encoding='utf-8') as f:
            maps[map_id] = json.load(f)
    return maps

def get_opposite_direction(direction):
    opposites = {
        'nord': 'sud',
        'sud': 'nord',
        'est': 'ouest',
        'ouest': 'est',
    }
    return opposites.get(direction)

def validate(maps):
    issues = []
    all_map_ids = set(maps.keys())

    for map_id, data in sorted(maps.items()):
        # --- Validate warps ---
        warps = data.get('warps', [])
        for i, warp in enumerate(warps):
            dest_map = (warp.get('destination_map') or warp.get('carte_destination')
                       or warp.get('dest_map') or warp.get('vers_map'))
            if not dest_map:
                # Try other common keys
                for k in warp:
                    if 'dest' in k or 'carte' in k or 'vers' in k:
                        val = warp[k]
                        if isinstance(val, str) and val in all_map_ids:
                            dest_map = val
                            break
            if not dest_map:
                issues.append({
                    'type': 'WARP_NO_DEST',
                    'map': map_id,
                    'warp_index': i,
                    'warp': warp,
                    'message': f"Warp #{i} in '{map_id}' has no destination map field"
                })
                continue

            # Check destination map exists
            if dest_map not in all_map_ids:
                issues.append({
                    'type': 'WARP_DEST_NOT_FOUND',
                    'map': map_id,
                    'warp_index': i,
                    'dest_map': dest_map,
                    'warp': warp,
                    'message': f"Warp #{i} in '{map_id}' -> '{dest_map}' but map '{dest_map}' does not exist"
                })
                continue

            # Check for reciprocal warp
            dest_data = maps[dest_map]
            dest_warps = dest_data.get('warps', [])
            has_reciprocal = False
            for dw in dest_warps:
                dw_dest = (dw.get('destination_map') or dw.get('carte_destination')
                          or dw.get('dest_map') or dw.get('vers_map'))
                if not dw_dest:
                    for k in dw:
                        if 'dest' in k or 'carte' in k or 'vers' in k:
                            val = dw[k]
                            if isinstance(val, str) and val in all_map_ids:
                                dw_dest = val
                                break
                if dw_dest == map_id:
                    has_reciprocal = True
                    break

            if not has_reciprocal:
                issues.append({
                    'type': 'WARP_NO_RECIPROCAL',
                    'map': map_id,
                    'warp_index': i,
                    'dest_map': dest_map,
                    'warp': warp,
                    'message': f"Warp #{i} in '{map_id}' -> '{dest_map}' but '{dest_map}' has NO warp back to '{map_id}'"
                })

        # --- Validate connexions ---
        connexions = data.get('connexions', [])
        for i, conn in enumerate(connexions):
            dest_map = conn.get('carte') or conn.get('map') or conn.get('destination') or conn.get('vers')
            direction = conn.get('direction')

            if not dest_map:
                issues.append({
                    'type': 'CONN_NO_DEST',
                    'map': map_id,
                    'conn_index': i,
                    'conn': conn,
                    'message': f"Connexion #{i} in '{map_id}' has no destination map field"
                })
                continue

            if not direction:
                issues.append({
                    'type': 'CONN_NO_DIRECTION',
                    'map': map_id,
                    'conn_index': i,
                    'conn': conn,
                    'message': f"Connexion #{i} in '{map_id}' has no direction"
                })
                continue

            # Check destination map exists
            if dest_map not in all_map_ids:
                issues.append({
                    'type': 'CONN_DEST_NOT_FOUND',
                    'map': map_id,
                    'conn_index': i,
                    'dest_map': dest_map,
                    'conn': conn,
                    'message': f"Connexion #{i} in '{map_id}' direction '{direction}' -> '{dest_map}' but map '{dest_map}' does not exist"
                })
                continue

            # Check for reciprocal connexion
            opposite = get_opposite_direction(direction)
            if not opposite:
                issues.append({
                    'type': 'CONN_UNKNOWN_DIRECTION',
                    'map': map_id,
                    'conn_index': i,
                    'direction': direction,
                    'conn': conn,
                    'message': f"Connexion #{i} in '{map_id}' has unknown direction '{direction}'"
                })
                continue

            dest_data = maps[dest_map]
            dest_conns = dest_data.get('connexions', [])
            has_reciprocal = False
            for dc in dest_conns:
                dc_dest = dc.get('carte') or dc.get('map') or dc.get('destination') or dc.get('vers')
                dc_dir = dc.get('direction')
                if dc_dest == map_id and dc_dir == opposite:
                    has_reciprocal = True
                    break

            if not has_reciprocal:
                issues.append({
                    'type': 'CONN_NO_RECIPROCAL',
                    'map': map_id,
                    'conn_index': i,
                    'dest_map': dest_map,
                    'direction': direction,
                    'opposite': opposite,
                    'conn': conn,
                    'message': f"Connexion #{i} in '{map_id}' direction '{direction}' -> '{dest_map}' but '{dest_map}' has NO connexion '{opposite}' back to '{map_id}'"
                })

    return issues

def main():
    maps = load_all_maps()
    print(f"Loaded {len(maps)} maps: {', '.join(sorted(maps.keys()))}\n")

    # Print summary of warps and connexions per map
    print("=" * 80)
    print("MAP SUMMARY")
    print("=" * 80)
    for map_id, data in sorted(maps.items()):
        warps = data.get('warps', [])
        conns = data.get('connexions', [])
        if warps or conns:
            warp_dests = []
            for w in warps:
                d = w.get('destination_map') or w.get('carte_destination') or w.get('dest_map') or w.get('vers_map') or '???'
                warp_dests.append(d)
            conn_dests = []
            for c in conns:
                d = c.get('carte') or c.get('map') or c.get('destination') or c.get('vers') or '???'
                dr = c.get('direction', '?')
                conn_dests.append(f"{dr}->{d}")
            print(f"  {map_id}: warps=[{', '.join(warp_dests)}] connexions=[{', '.join(conn_dests)}]")

    print()
    issues = validate(maps)

    if not issues:
        print("✅ No issues found! All warps and connexions are reciprocal.")
        return

    # Group by type
    print("=" * 80)
    print(f"ISSUES FOUND: {len(issues)}")
    print("=" * 80)

    # Sprint 5 maps
    sprint5 = {'route_5', 'route_6', 'tunnel_souterrain', 'carmin_sur_mer',
                'centre_pokemon_carmin', 'boutique_carmin', 'ss_anne_pont',
                'ss_anne_cabines', 'ss_anne_cuisine', 'ss_anne_capitaine',
                'arene_carmin', 'route_7', 'grotte_taupiqueur'}

    sprint5_issues = [i for i in issues if i['map'] in sprint5 or i.get('dest_map') in sprint5]
    other_issues = [i for i in issues if i not in sprint5_issues]

    if sprint5_issues:
        print(f"\n--- SPRINT 5 ISSUES ({len(sprint5_issues)}) ---")
        for iss in sprint5_issues:
            print(f"  [{iss['type']}] {iss['message']}")

    if other_issues:
        print(f"\n--- OTHER ISSUES ({len(other_issues)}) ---")
        for iss in other_issues:
            print(f"  [{iss['type']}] {iss['message']}")

    # Print detailed warp data for problematic maps
    problem_maps = set()
    for iss in issues:
        problem_maps.add(iss['map'])
        if 'dest_map' in iss:
            problem_maps.add(iss['dest_map'])

    print(f"\n{'=' * 80}")
    print("DETAILED WARP/CONNEXION DATA FOR PROBLEMATIC MAPS")
    print("=" * 80)
    for map_id in sorted(problem_maps):
        if map_id not in maps:
            print(f"\n  {map_id}: *** DOES NOT EXIST ***")
            continue
        data = maps[map_id]
        print(f"\n  {map_id}:")
        warps = data.get('warps', [])
        if warps:
            print(f"    warps:")
            for j, w in enumerate(warps):
                print(f"      [{j}] {json.dumps(w, ensure_ascii=False)}")
        conns = data.get('connexions', [])
        if conns:
            print(f"    connexions:")
            for j, c in enumerate(conns):
                print(f"      [{j}] {json.dumps(c, ensure_ascii=False)}")

if __name__ == '__main__':
    main()
