#!/usr/bin/env python3
"""
Logistic Regression inference script for EMNIST
– loads a saved joblib model
– reads a 28×28 PNG, scales to [0,1], flattens
– maps the predicted class index to the corresponding character
– prints that character to stdout
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

# ── EMNIST Balanced mapping (class index → ASCII code) ───────
#   indices 0–9   → '0'–'9'
#   indices 10–35 → 'A'–'Z'
#   indices 36–46 → 'a'–'k'
ASCII_MAP = [
    48, 49, 50, 51, 52, 53, 54, 55, 56, 57,            # '0'–'9'
    65, 66, 67, 68, 69, 70, 71, 72, 73, 74,            # 'A'–'J'
    75, 76, 77, 78, 79, 80, 81, 82, 83, 84,            # 'K'–'T'
    85, 86, 87, 88, 89, 90,                            # 'U'–'Z'
    97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107 # 'a'–'k'
]

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
    label_idx = int(pred[0])

    # map to character
    try:
        char = chr(ASCII_MAP[label_idx])
    except IndexError:
        sys.exit(f"[ERROR] unexpected label index: {label_idx}")

    # output
    print(char)

if __name__ == "__main__":
    main()
