#!/usr/bin/env python3
import sys
import os
import argparse
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def convert_to_png(image_path):
    if image_path.lower().endswith(".png"):
        return image_path
    png_path = os.path.splitext(image_path)[0] + ".png"
    print(f"[INFO] Konwersja {image_path} → {png_path}")
    with Image.open(image_path) as img:
        img.convert("L").save(png_path)
    return png_path

def image_to_point_cloud(image_path, threshold=None, tile_size=1000):
    with Image.open(image_path) as img:
        w, h = img.size
        print(f"[DEBUG] image size: {w}x{h}, mode: {img.mode}")
        points = []

        for y in range(0, h, tile_size):
            for x in range(0, w, tile_size):
                tile_w = min(tile_size, w - x)
                tile_h = min(tile_size, h - y)
                tile = img.crop((x, y, x + tile_w, y + tile_h))
                arr = np.array(tile, dtype=np.uint8)
                xs, ys = np.meshgrid(np.arange(x, x + tile_w), np.arange(y, y + tile_h), indexing='xy')
                tile_points = np.column_stack((xs.ravel(), ys.ravel(), arr.ravel()))
                if threshold is not None:
                    tile_points = tile_points[tile_points[:, 2] < threshold]
                points.append(tile_points)
                print(f"[INFO] kafelek ({x},{y}) – {len(tile_points)} punktów")

        if not points:
            print("[ERROR] Brak punktów – obraz pusty?")
            sys.exit(1)
        points = np.vstack(points)
        print(f"[INFO] Całkowita liczba punktów: {len(points)}")
    return points

def save_point_cloud_txt(points, out_path):
    np.savetxt(out_path, points, fmt='%d', delimiter=' ', header='x y z')
    print(f"[INFO] Zapisano: {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Konwersja obrazów na chmury punktów")
    parser.add_argument('images', nargs='+', help='Ścieżki do plików (TIFF, PNG, JPG)')
    parser.add_argument('--threshold', type=int, default=None)
    parser.add_argument('--tile-size', type=int, default=1000)
    parser.add_argument('--out-dir', default='results')
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    for img_path in args.images:
        if not os.path.isfile(img_path):
            print(f"[ERROR] Plik nie istnieje: {img_path}")
            continue
        png_path = convert_to_png(img_path)
        points = image_to_point_cloud(png_path, args.threshold, args.tile_size)
        base = os.path.splitext(os.path.basename(png_path))[0]
        out_txt = os.path.join(args.out_dir, base + "_point_cloud.txt")
        save_point_cloud_txt(points, out_txt)

if __name__ == "__main__":
    main()
