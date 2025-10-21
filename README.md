# Prostate cancer Topological Analysis

This project converts medical images (e.g., prostate tissue) into point clouds, 
computes persistent homology diagrams, and compares them using bottleneck distance.

## Usage

1. **Convert images:**
   ```bash
   python convert_image_to_point_cloud.py /path/to/*.tiff --threshold 200 --out-dir results
