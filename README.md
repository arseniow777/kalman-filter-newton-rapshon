# Komputasi Numerik — Battery Cycle Life Prediction

Prediksi cycle life lithium-ion battery menggunakan Extended Kalman Filter (EKF) dan Newton Raphson, dibandingkan dengan baseline Linear Regression (ElasticNet).

**Referensi**: Fahmy et al. (2025)

## Deskripsi Project

Sistem ini mengimplementasikan pipeline prediksi cycle life battery:

1. **EKF (Extended Kalman Filter)** — Melakukan tracking degradasi kapasitas per cycle
   - State: `[Q, dQ]` (kapasitas dan laju degradasi)
   - Menghaluskan noise dari raw QDischarge measurement
2. **Newton Raphson** — Mencari cycle number saat kapasitas mencapai EOL threshold (80%)
   - Fit polynomial degree-2 pada smoothed capacity curve
   - Root finding untuk prediksi end-of-life
3. **Linear Regression Baseline** — ElasticNet untuk comparison
   - Feature engineering dari first 100 cycles
   - Hyperparameter tuning via cross-validation

## Dataset

- **Sumber**: NASA PCoE Battery Dataset
- **File**: 3 batch files `.mat` (MATLAB format)
  - `2017-05-12_batchdata_updated_struct_errorcorrect.mat`
  - `2017-06-30_batchdata_updated_struct_errorcorrect.mat`
  - `2018-04-12_batchdata_updated_struct_errorcorrect.mat`
- **Total cells**: 124 lithium-ion batteries (41 train, 43 val, 40 test)

## Struktur Project

```
komputasiNumerik-battery/
├── README.md                          # File ini
├── requirements.txt                   # Python dependencies
├── explore.py                         # Script explorasi data format
├── dataset/
│   ├── 2017-05-12_batchdata_updated_struct_errorcorrect.mat
│   ├── 2017-06-30_batchdata_updated_struct_errorcorrect.mat
│   └── 2018-04-12_batchdata_updated_struct_errorcorrect.mat
├── notebooks/
│   ├── eda/
│   │   └── 01_eda (1).ipynb           # Exploratory Data Analysis
│   └── v1/
│       ├── config_v1.py               # Konfigurasi & parameter
│       ├── 02_preprocessing_v1.ipynb  # Data preprocessing & train-val-test split
│       └── 03_modelling_v1 (1).ipynb  # EKF + NR & Linear Regression
└── outputs/
    └── v1/
        ├── figures/                   # Hasil visualisasi
        │   ├── actual_vs_predicted_v1.png
        │   └── per_cell_comparison_v1.png
        └── results/
            └── results_v1.pkl         # Metrik evaluasi (RMSE, APE)
```

## Prerequisites

- **Python**: 3.8+ (3.10+ recommended)
- **Git**: Untuk clone repository
- **pip**: Python package manager
- **Jupyter Notebook/Lab**: Untuk menjalankan notebook

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-username/komputasiNumerik-battery.git
cd komputasiNumerik-battery
```

### 2. Setup Python Environment

**Opsi A: Menggunakan venv (Recommended)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**Opsi B: Menggunakan conda**

```bash
conda create -n battery python=3.10
conda activate battery
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verifikasi instalasi:**

```bash
python -c "import h5py, numpy, pandas; print('✓ All dependencies installed')"
```

### 4. Dataset Setup

Dataset `.mat` files sudah ada di folder `dataset/`. Jika belum:

1. Download dari [NASA PCoE Battery Dataset](https://data.nasa.gov/)
2. Letakkan di folder `dataset/`
3. File harus: `*_batchdata_updated_struct_errorcorrect.mat`

### 5. Jalankan Notebooks (Urutan)

#### Langkah 1: Exploratory Data Analysis

```bash
jupyter notebook notebooks/eda/01_eda\ \(1\).ipynb
```

- Eksplorasi struktur data `.mat`
- Visualisasi QDischarge, IR, temperature per cell
- Identifikasi outliers

#### Langkah 2: Preprocessing & Train-Val-Test Split

```bash
jupyter notebook notebooks/v1/02_preprocessing_v1.ipynb
```

- Load 3 batch files
- Extract cycle life labels
- Split: 41 train, 43 val, 40 test
- Simpan ke `outputs/v1/preprocessed_v1.pkl`

#### Langkah 3: Modelling — EKF + NR vs Linear Regression

```bash
jupyter notebook notebooks/v1/03_modelling_v1\ \(1\).ipynb
```

- Run EKF untuk tracking degradasi
- Run Newton Raphson untuk prediksi cycle life
- Train ElasticNet baseline
- Generate figures dan results

## Konfigurasi

File `notebooks/v1/config_v1.py` berisi parameter:

```python
# EKF Parameters (Table 2, Fahmy et al.)
EKF_P0 = [2.0, 0.0]              # Initial covariance [Q, dQ]
EKF_R  = 0.01                    # Measurement noise (QDischarge)
EKF_Q  = [0.8, 0.2]              # Process noise [Q, dQ]

# Battery Parameters
BATTERY_Q_NOMINAL = 1.1 Ah       # Nominal capacity
EOL_THRESHOLD = 0.88             # EOL = 80% of nominal

# Newton Raphson
NR_TOL      = 1e-6               # Tolerance
NR_MAX_ITER = 100                # Max iterations

# Data Split
TRAIN_SIZE = 41
VAL_SIZE   = 43
TEST_SIZE  = 40
```

Edit di sini jika ingin tuning hyperparameter.

## Hasil & Metrics

Setelah menjalankan semua notebook, hasil akan tersimpan di:

- **Figures**: `outputs/v1/figures/`
  - `actual_vs_predicted_v1.png` — Scatter plot actual vs predicted
  - `per_cell_comparison_v1.png` — Per-cell comparison all methods
- **Results**: `outputs/v1/results/results_v1.pkl`
  - RMSE dan Average Percentage Error untuk setiap method

**Target Performance (Paper)**:

- EKF + NR: RMSE = 10.93, Avg%Error = 3.26%
- Linear Regression: RMSE = 211.6, Avg%Error = 9.98%

## Explorasi Data

Untuk melihat format data `.mat`:

```bash
python explore.py
```

Output: struktur dan sample data dari setiap field (QDischarge, IR, temperature, dll)

## Troubleshooting

### Error: "No module named 'h5py'"

```bash
pip install h5py
```

### Error: "File not found: dataset/\*.mat"

Pastikan file `.mat` sudah ada di folder `dataset/`. Download dari NASA jika belum ada.

### Error: "ImportError in notebook"

Pastikan virtual environment sudah activate:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Jupyter kernel tidak terdeteksi

Install ipykernel di virtual environment:

```bash
pip install ipykernel
python -m ipykernel install --user --name battery --display-name "Python (Battery)"
```

## Dependencies Breakdown

| Package        | Versi       | Kegunaan                            |
| -------------- | ----------- | ----------------------------------- |
| `numpy`        | -           | Numerical computation               |
| `pandas`       | -           | Data manipulation                   |
| `scipy`        | -           | Scientific computing (optimization) |
| `h5py`         | -           | Read MATLAB `.mat` files            |
| `matplotlib`   | -           | Plotting & visualization            |
| `seaborn`      | -           | Statistical data visualization      |
| `scikit-learn` | (via scipy) | Machine learning (ElasticNet)       |
| `jupyter`      | -           | Notebook environment                |
| `ipykernel`    | -           | Jupyter kernel                      |

## Catatan Penting

1. **Virtual Environment**: Selalu gunakan virtual environment untuk menghindari dependency conflicts
2. **Dataset Size**: File `.mat` cukup besar (~500MB+). Pastikan space disk cukup
3. **Notebook Order**: Jangan skip preprocessing — output-nya diperlukan oleh modelling notebook
4. **Random Seed**: `RANDOM_SEED = 42` untuk reproducibility

## Contributing

Jika ada improvement atau bug:

1. Fork repository
2. Buat branch: `git checkout -b feature/improvement`
3. Commit: `git commit -m "Add improvement"`
4. Push: `git push origin feature/improvement`
5. Create Pull Request

## Referensi

- Fahmy et al. (2025) — EKF + Newton Raphson untuk battery RUL prediction
- NASA PCoE Battery Dataset — https://data.nasa.gov/
- Extended Kalman Filter — Standard state estimation technique
- Newton Raphson Method — Root finding algorithm

## License

[Sesuaikan dengan lisensi project Anda]

## Author

Dikerjakan sebagai tugas Komputasi Numerik

---

**Last Updated**: Juni 2, 2026
