#!/usr/bin/env python3
import sys
import os
import argparse
import gudhi
import numpy as np

def read_diagram(filename, dim):
    pairs = []
    with open(filename) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            d, b, de = line.split()
            if int(d) == dim:
                pairs.append((float(b), float(de)))
    return pairs

def main():
    p = argparse.ArgumentParser(description="Porównanie diagramów persystentnych")
    p.add_argument('a_files', nargs='+')
    p.add_argument('-b', '--b_file', required=True)
    p.add_argument('-d', '--dim', type=int, required=True)
    args = p.parse_args()

    if not os.path.isfile(args.b_file):
        sys.exit(f"B-file not found: {args.b_file}")

    diag_b = read_diagram(args.b_file, args.dim)
    best_file, best_dist = None, float('inf')

    for f in args.a_files:
        if not os.path.isfile(f): 
            print(f"[WARN] Missing: {f}")
            continue
        diag_a = read_diagram(f, args.dim)
        if not diag_a:
            continue
        dist = gudhi.bottleneck_distance(diag_a, diag_b)
        print(f"{os.path.basename(f)} → distance = {dist:.6f}")
        if dist < best_dist:
            best_dist, best_file = dist, f

    if best_file:
        print(f"\n[RESULT] Najbliższy diagram: {best_file} (distance={best_dist:.6f})")
    else:
        print("Brak porównywalnych diagramów.")

if __name__ == "__main__":
    main()
