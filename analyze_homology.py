#!/usr/bin/env python3
import os
import sys
import argparse
import numpy as np
import gudhi
import itertools
from tqdm import tqdm
import matplotlib.pyplot as plt

def analyze_persistence(infile, step=1, max_dim=2, min_dist=0.0):
    if not os.path.isfile(infile):
        sys.exit(f"Error: {infile} not found")

    data = np.loadtxt(infile)
    if data.ndim != 2 or data.shape[1] != 3:
        sys.exit("Error: input must have 3 columns (x y z)")

    pts = data[::step, :2]
    filtr = data[::step, 2]
    print(f"[INFO] {len(pts)} punktów (krok: {step})")

    dc = gudhi.DelaunayComplex(points=pts)
    st = dc.create_simplex_tree()

    for i, z in enumerate(filtr):
        st.assign_filtration([i], z)

    for dim in range(1, st.dimension() + 1):
        for simplex, _ in st.get_skeleton(dim):
            if len(simplex) != dim + 1:
                continue
            f = [st.filtration(list(face)) for face in itertools.combinations(simplex, dim)]
            st.assign_filtration(simplex, max(f))
    st.initialize_filtration()

    pers = st.persistence()
    pers_f = [(d, (b, de)) for d, (b, de) in pers if d <= max_dim and abs(de - b) >= min_dist]
    out = os.path.splitext(infile)[0] + f"_pers_dim{max_dim}_dist{min_dist}.txt"

    with open(out, 'w') as f:
        f.write("# dim birth death\n")
        for d, (b, de) in pers_f:
            f.write(f"{d} {b:.6f} {de:.6f}\n")

    print(f"[INFO] zapisano: {out}")
    gudhi.plot_persistence_diagram(pers_f)
    plt.title(f"Persistence diagram ({os.path.basename(infile)})")
    plt.show()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('infile', help='plik chmury punktów (TXT)')
    p.add_argument('step', type=int, nargs='?', default=1)
    p.add_argument('max_dim', type=int, nargs='?', default=2)
    p.add_argument('-k', '--min_dist', type=float, default=0.0)
    args = p.parse_args()
    analyze_persistence(args.infile, args.step, args.max_dim, args.min_dist)

if __name__ == "__main__":
    main()
