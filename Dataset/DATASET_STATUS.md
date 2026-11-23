# 📊 Dataset Status Report

This document reports the live download, verification, and preparation status of all datasets in the **AI-Virtual-Fitting-Room** repository.

---

## 📋 Summary Table

| Dataset Name | Official Source | Target Directory | Download Status | Verified Count / Size | Category Coverage | License |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Fashion Product Images Small** | [HuggingFace: ashraq/fashion-product-images-small](https://huggingface.co/datasets/ashraq/fashion-product-images-small) | `Dataset/Catalog/` | **Downloaded & Verified** | 200 catalog items (images + metadata CSV/JSON) | Men (60), Women (60), Boys (40), Girls (40) | CC BY-SA 4.0 |
| **CURVTON-205K (Sample Split)** | [HuggingFace: curvton2/curvton2](https://huggingface.co/datasets/curvton2/curvton2) | `Dataset/Virtual_TryOn/CURVTON/sample/` | **Downloaded & Verified** | 30 paired images (person, garment, ground truth try-on) | Men & Women (Easy pairs) | CC BY-NC 4.0 |
| **CURVTON-205K (Full Split)** | [HuggingFace: curvton2/curvton2](https://huggingface.co/datasets/curvton2/curvton2) | `Dataset/Virtual_TryOn/CURVTON/` | **Not Downloaded (Safety Guard)** | ~108–126 GB (Requires explicit confirmation) | Adult Male & Female | CC BY-NC 4.0 |
| **VITON-HD** | [GitHub: shadow2496/VITON-HD](https://github.com/shadow2496/VITON-HD) | `Dataset/Virtual_TryOn/VITON_HD/` | **Requires Registration / Agreement** | Directory structure ready (`train/`, `test/`) | Adult Women Upper-Body | Research Non-Commercial |
| **DeepFashion2** | [GitHub: switchablenorms/DeepFashion2](https://github.com/switchablenorms/DeepFashion2) | `Dataset/Image_Processing/DeepFashion2/` | **Requires Agreement / Manual Download** | Directory structure ready (`train/`, `validation/`, `test/`) | Clothing Segmentation & Landmarks | Academic Research Only |

---

## 🔍 Detailed Dataset Reports

### 1. Catalog Dataset: Fashion Product Images Small
- **Location:** `Dataset/Catalog/`
- **Metadata files:** `catalog_metadata.csv`, `catalog_metadata.json`
- **Breakdown:**
  - `Dataset/Catalog/Men/`: Tops, Bottoms, Outerwear (60 products)
  - `Dataset/Catalog/Women/`: Tops, Bottoms, Dresses, Outerwear (60 products)
  - `Dataset/Catalog/Boys/`: Tops, Bottoms, Outerwear (40 products)
  - `Dataset/Catalog/Girls/`: Tops, Bottoms, Dresses, Outerwear (40 products)
- **Status:** **Verified** and ready for the Frontend catalog and Try-On engine.

### 2. Virtual Try-On Dataset: CURVTON-205K
- **Sample Location:** `Dataset/Virtual_TryOn/CURVTON/sample/`
- **Contents:**
  - `easy/female/`: `cloth_image/`, `initial_person_image/`, `tryon_image/`
  - `easy/male/`: `cloth_image/`, `initial_person_image/`, `tryon_image/`
- **Status:** **Verified**. Used for benchmark evaluation and pipeline testing.

---

## ⚠️ Storage Safety Note
The complete CURVTON-205K dataset requires more than 108 GB of storage. As per project guidelines, only the curated sample split has been downloaded to keep disk space optimal while providing full test coverage.
