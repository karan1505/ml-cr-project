#!/usr/bin/env python3
"""
Logistic Regression inference script for EMNIST
– loads a saved joblib model
– reads a 28×28 PNG, scales to [0,1], flattens
– prints the predicted class label to stdout
"""

import sys
import argparse
from pathlib import Path

import joblib
import numpy as np
from PIL import Image

# ── locate & load model ───────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_PATH = SCRIPT_DIR / "SavedModels" / "LR" / "LogReg-Model.joblib"

if not MODEL_PATH.exists():
    sys.exit(f"[ERROR] model file not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
print(f"[INFO] loaded model '{MODEL_PATH}'", file=sys.stderr)

# ── main entrypoint ────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="EMNIST Logistic Regression inference")
    parser.add_argument(
        "--input",
        required=True,
        help="path to input 28×28 PNG"
    )
    args = parser.parse_args()
    img_path = Path(args.input)
    if not img_path.exists():
        sys.exit(f"[ERROR] input file not found: {img_path}")

    # load & preprocess image
    img = Image.open(img_path).convert("L")
    if img.size != (28, 28):
        img = img.resize((28, 28))
    arr = np.array(img, dtype=np.float32) / 255.0    # shape (28,28), values in [0,1]
    flat = arr.reshape(1, -1)                       # shape (1, 784)

    # predict
    pred = model.predict(flat)
    label = pred[0]

    # output
    print(label)

if __name__ == "__main__":
    main()
