# Robust Fingerprint Matching under Distortions

## Overview
This project implements a complete pipeline for **fingerprint matching under challenging conditions**, such as altered fingerprints (Obliteration, Central Rotation, Z-cut) with varying difficulty levels (Easy, Medium, Hard).  
The goal is to compare **classical fingerprint recognition methods** (minutiae-based and ORB-based) with **deep learning models** (CNN + metric learning).  

The project is designed to be:  
- **Reproducible**: all splits and pairs are pre-generated and stored as CSV files.  
- **Transparent**: baseline vs DL comparisons are evaluated with standard biometric metrics (ROC, AUC, EER).  
- **Practical**: includes both Jupyter notebooks for analysis and a CLI tool for direct fingerprint comparison.  

---

## Dataset Structure
The dataset is assumed to follow this folder structure:

```
data/raw/
    person_<id>/
        original/
            <id>__M_Left_index_finger.bmp
            ...
        Altered_Easy/
            Obl/
            CR/
            Zcut/
        Altered_Medium/
            Obl/
            CR/
            Zcut/
        Altered_Hard/
            Obl/
            CR/
            Zcut/
```

- **original/**: clean fingerprint samples.  
- **Altered_X/**: distorted samples with difficulty level Easy/Medium/Hard.  
- **Obl / CR / Zcut**: specific alteration types.  
- File names encode: `person_id`, gender (M/F), hand, and finger. Example:  
  ```
  001__M_Left_index_finger.bmp
  ```

---

## Project File Structure

```
repo/
│
├── data/
│   ├── raw/                # Original dataset (as provided)
│   ├── index/
│   │    └── metadata.csv   # path, person_id, finger, level, type
│   ├── splits/
│   │    ├── train_ids.txt
│   │    ├── val_ids.txt
│   │    ├── test_ids.txt
│   └── pairs/
│        ├── train_pairs.csv
│        ├── val_pairs.csv
│        ├── test_pairs_easy.csv
│        ├── test_pairs_medium.csv
│        └──test_pairs_hard.csv
│         
│
├── src/
│   ├── dataio/
│   │    ├── indexer.py        # Traverse raw dataset → metadata.csv
│   │    ├── pairs_builder.py  # Generate pairs from metadata & splits
│   │    └── dataset.py        # PyTorch dataset class
│   │
│   ├── classic/
│   │    ├── enhancement.py
│   │    ├── matcher_minutiae.py
│   │    ├── matcher_orb.py
│   │
│   ├── dl/
│   │    ├── models.py
│   │    ├── losses.py
│   │    ├── train.py
│   │    ├── eval.py
│   │
│   ├── eval/
│   │    ├── metrics.py
│   │    ├── plots.py
│   │
│   └── api/
│        └── matcher.py   # Unified API for classical & DL models
│
├── notebooks/
│   ├── 01_explore_data.ipynb
│   ├── 02_pairs_stats.ipynb
│   ├── 03_baseline_eval.ipynb
│   ├── 04_dl_training.ipynb
│
├── models/                 # Trained weights
├── results/                # Evaluation outputs (ROC/DET plots, confusion matrices, CSVs)
├── match.py                # CLI tool for fingerprint comparison
├── pyproject.toml
└── README.md
```

---

## Features
- **Indexing**: automatically parse dataset and generate `metadata.csv` with all file paths and attributes.  
- **Pair Generation**: build genuine and impostor pairs for training, validation, and testing.  
- **Classical Baselines**:  
  - Minutiae-based matcher (extraction + skeletonization + RANSAC alignment).  
  - ORB/SIFT-based matcher with descriptor verification.  
- **Deep Learning**:  
  - ResNet18/MobileNetV3 backbone → 128-D embeddings.  
  - Metric learning (Contrastive loss, Triplet loss).  
- **Evaluation Metrics**: ROC, AUC, EER, FAR/FRR.  
- **Visualization**: ROC/DET plots, confusion matrices, error case visualization.  
- **CLI Tool**:  
  ```bash
  python match.py --img1 path_a.bmp --img2 path_b.bmp --method dl --weights models/resnet18.pt
  ```
  Output example:  
  ```json
  {"score": 0.842, "decision": "match", "threshold": 0.79, "method": "dl"}
  ```

---

## Development Process
1. **Index dataset** → create `metadata.csv`.  
2. **Generate splits** (train/val/test with subject-disjoint IDs).  
3. **Generate pairs** for each subset.  
4. **Run baselines** (ORB, minutiae).  
5. **Train DL models** with metric learning.  
6. **Evaluate** across difficulty levels and alteration types.  
7. **Document** results with plots and reports.  

---

## Evaluation Plan
- **Metrics**: ROC, AUC, EER, FAR/FRR.  
- **Scenarios**: Original vs {Easy, Medium, Hard}.  
- **Alteration types**: Obl, CR, Zcut.  
- **Error analysis**: visualize False Accepts and False Rejects.  

---

## Tech Stack
- **Language**: Python 3.12+  
- **Libraries**: PyTorch, Torchvision, OpenCV, NumPy, Matplotlib, Scikit-learn, Pandas  
- **Environment**: Jupyter for analysis, CLI for demos  
- **Hardware**: training on GPU (Colab/Kaggle), inference CPU/GPU  

---

## How to Use
1. Place dataset under `data/raw/` in the described format.  
2. Run indexer:  
   ```bash
   python src/dataio/indexer.py --input data/raw --output data/index/metadata.csv
   ```
3. Generate pairs:  
   ```bash
   python src/dataio/pairs_builder.py --metadata data/index/metadata.csv --split data/splits/train_ids.txt
   ```
4. Train DL model:  
   ```bash
   python src/dl/train.py --config configs/resnet18.yaml
   ```
5. Evaluate:  
   ```bash
   python src/dl/eval.py --weights models/resnet18_metric.pt --pairs data/pairs/test_pairs_easy.csv
   ```
6. CLI demo:  
   ```bash
   python match.py --img1 a.bmp --img2 b.bmp --method orb --enhance
   ```

---

## License
MIT License

---

## Author
Prepared as a research/resume project to demonstrate expertise in biometric fingerprint recognition, classical vision methods, and deep learning for robust matching under distortions.
