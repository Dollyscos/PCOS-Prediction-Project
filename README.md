# PCOS Prediction System Streamlit Webpage

This project is a browser-based Streamlit application for predicting Polycystic Ovary Syndrome (PCOS) using:
- structured clinical data
- ovarian ultrasound images
- a combined review page that compares both results side by side

## Pages
- Home
- Clinical Prediction
- Ultrasound Prediction
- Combined Review

## Project structure
```text
pcos_streamlit_webpage/
├── app.py
├── artifacts/
├── assets/
├── pages/
├── utils/
├── requirements.txt
├── environment.yml
└── README.md
```
## Recommended Python Version
This project is best run with Python 3.11.

## Setup option 1: Conda (recommended)
Use this option if you already have Conda installed. It is the most reliable setup, especially on macOS.

### Create and activate the environment
```bash
conda env create -f environment.yml
conda activate pcos_env
```

### Install `llvm-openmp` or `libomp` (macOS only)
On macOS, install `llvm-openmp` with Conda or `libomp` with Homebrew.
```bash
conda activate pcos_env
conda install -c conda-forge llvm-openmp xgboost -y
```
```bash
brew install libomp
```

### Run the app
From inside the pcos_streamlit_webpage folder:
```bash
streamlit run app.py
```

## Setup option 2: Standard Python virtual environment
Use this option if you do not use Conda.

### Create and activate a virtual environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### Run the app
From inside the pcos_streamlit_webpage folder:
```bash
streamlit run app.py
```

## Required artifacts
Make sure these files are inside the `artifacts/` folder before running the app:

- `clinical_feature_order.json`
- `clinical_categories.json`
- `clinical_preprocessor.joblib`
- `clinical_xgb_model.json`
- `ultrasound_resnet50.keras`
- `ultrasound_metadata.json`
- `shap_background.csv`

## Notes
- Use **relative paths only** in the project files.
- If you replace model files in `artifacts/`, clear the Streamlit cache and restart the app:
  ```bash
  streamlit cache clear
  ```
- On macOS, XGBoost may require `libomp`. The Conda setup handles this more reliably than the pip-only setup.

## Troubleshooting

### 1. `ImportError: numpy.core.multiarray failed to import`
This usually means the wrong Python environment is being used. Make sure the app is running inside the correct environment and reinstall dependencies if needed.

### 2. `XGBoost library could not be loaded`
This usually happens when `llvm-openmp` is missing on macOS. Use the Conda setup if possible.
- On macOS, install llvm-openmp with Conda or libomp with Homebrew.
```bash
conda activate pcos_env
conda install -c conda-forge llvm-openmp xgboost -y
```
```bash
brew install libomp
```

### 3. Streamlit does not run model results properly
Clear the cache and restart the app:
```bash
streamlit cache clear
```

## Recommendation
- Use **Conda** if available, especially on macOS.
- Use the **venv + requirements.txt** option if Conda is not installed.
