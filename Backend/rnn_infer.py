#!/usr/bin/env python3
import os; os.environ["CUDA_VISIBLE_DEVICES"] = "-1"   # CPU only
import argparse, sys, traceback, numpy as np, tensorflow as tf
from pathlib import Path
from PIL import Image

# ── load model ─────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_PATH = SCRIPT_DIR / "SavedModels" / "RNN" / "RNN-Model.keras"
if not MODEL_PATH.exists():
    sys.exit(f"[ERROR] model file not found at {MODEL_PATH}")

model = tf.keras.models.load_model(MODEL_PATH)
print(f"[INFO] loaded RNN model '{MODEL_PATH}'", file=sys.stderr)

# ── 47 EMNIST labels ──────────────────────────────────────────
LABELS = [
    '0','1','2','3','4','5','6','7','8','9',
    'A','B','C','D','E','F','G','H','I','J',
    'K','L','M','N','O','P','Q','R','S','T',
    'U','V','W','X','Y','Z',
    'a','b','d','e','f','g','h','n','q','r','t'
]

# ── preprocessing (same as CNN) ────────────────────────────────
def preprocess(path: Path) -> np.ndarray:
    img = Image.open(path).convert("L")
    arr = np.array(img, dtype=np.uint8)

    # 1. threshold (white ink assumed)
    ys, xs = np.where(arr > 128)
    if len(xs) == 0:
        crop = np.zeros((28,28), dtype=np.uint8)
    else:
        crop = arr[ys.min():ys.max()+1, xs.min():xs.max()+1]

    # 2. resize longest side → 20 px
    h, w = crop.shape
    scale = 20.0 / max(h, w)
    crop = Image.fromarray(crop).resize(
        (int(round(w*scale)), int(round(h*scale))),
        Image.Resampling.LANCZOS
    )
    crop = np.asarray(crop, dtype=np.uint8)

    # 3. center on 28×28 canvas
    canvas = np.zeros((28,28), dtype=np.uint8)
    y_off = (28 - crop.shape[0]) // 2
    x_off = (28 - crop.shape[1]) // 2
    canvas[y_off:y_off+crop.shape[0], x_off:x_off+crop.shape[1]] = crop

    # 4. transpose + horizontal flip
    canvas = canvas.T[:, ::-1]

    # 5. normalize and add channel
    return (canvas.astype("float32") / 255.0).reshape(1,28,28,1)

# ── CLI ───────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="RNN inference for EMNIST PNG")
    ap.add_argument("-i", "--input", required=True, help="28×28 PNG file")
    args = ap.parse_args()

    try:
        x     = preprocess(Path(args.input))
        probs = model.predict(x, verbose=0)[0]
        top2  = probs.argsort()[-2:][::-1]
        a, b  = LABELS[top2[0]], LABELS[top2[1]]
        print(f"{a} or {b}?")
    except Exception:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
