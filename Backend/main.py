# backend/main.py
#!/usr/bin/env python3
"""
FastAPI backend for EMNIST character inference
---------------------------------------------
• Receives a JSON body  {"pixels": [784 floats]}  from the React front‑end  
  – floats already in [0,1], stroke=1, bg=0  
  – orientation already fixed (transpose + horizontal flip)  
• Saves the 28×28 PNG (for auditing)  
• Calls the appropriate *infer script* (cnn_infer.py, rnn_infer.py, lr_infer.py)  
  which prints the top‑1 label to stdout.  
• Appends each request to results.csv and supports feedback updates.
"""

import os, csv, subprocess
from typing import List, Tuple

import numpy as np
from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Configuration ──────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
TMP_DIR         = os.path.join(BASE_DIR, "tmp")
RESULTS_CSV     = os.path.join(BASE_DIR, "results.csv")
ALLOWED_ORIGINS = ["http://localhost:5173", "http://localhost:5174"]

# ── Request / Response Schemas ─────────────────────────────────
class InferenceRequest(BaseModel):
    pixels: List[float]          # length 784, values 0‑1

class InferenceResponse(BaseModel):
    label: str
    img_name: str                # saved PNG filename

class FeedbackRequest(BaseModel):
    img_name: str
    user_feedback: str           # "correct" / "incorrect" / etc.

# ── FastAPI app + CORS ─────────────────────────────────────────
app = FastAPI(
    title       ="EMNIST Inference API",
    description ="pixels → infer → CSV log → feedback",
    version     ="0.2.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ALLOWED_ORIGINS,
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ── Ensure CSV header exists ───────────────────────────────────
if not os.path.exists(RESULTS_CSV) or os.path.getsize(RESULTS_CSV) == 0:
    with open(RESULTS_CSV, "w", newline="") as f:
        csv.writer(f).writerow(
            ["img_name", "model_used", "result_inferred", "user_feedback"]
        )

def _get_next_id() -> int:
    with open(RESULTS_CSV, newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        return sum(1 for _ in reader) + 1

def _run_pipeline(prefix: str, pixels: List[float]) -> Tuple[str, str]:
    run_id   = _get_next_id()
    raw_name = f"raw-img-{run_id}.png"
    in_path  = os.path.join(TMP_DIR, raw_name)

    os.makedirs(TMP_DIR, exist_ok=True)

    # reconstruct & save the 28×28 PNG
    arr = np.array(pixels, dtype=np.float32).reshape((28, 28))
    Image.fromarray((arr * 255).astype(np.uint8)).save(in_path)

    # locate infer script   (e.g., cnn_infer.py)
    infer_script = os.path.join(BASE_DIR, f"{prefix}_infer.py")
    if not os.path.isfile(infer_script):
        raise RuntimeError(f"infer script not found: {infer_script}")

    # run inference
    proc = subprocess.run(
        ["python", infer_script, "--input", in_path],
        capture_output=True,
        text=True
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Inference failed:\n{proc.stderr}")

    label = proc.stdout.strip()

    # log to CSV  (feedback column blank for now)
    with open(RESULTS_CSV, "a", newline="") as f:
        csv.writer(f).writerow([raw_name, prefix, label, ""])

    return label, raw_name

# ── API Endpoints ──────────────────────────────────────────────
@app.get("/", tags=["Info"])
async def root():
    return {"message": "EMNIST Inference API is running"}

@app.post("/cnninfer", response_model=InferenceResponse, tags=["CNN"])
async def cnn_infer(req: InferenceRequest):
    try:
        label, img_name = _run_pipeline("cnn", req.pixels)
        return InferenceResponse(label=label, img_name=img_name)
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rnninfer", response_model=InferenceResponse, tags=["RNN"])
async def rnn_infer(req: InferenceRequest):
    try:
        label, img_name = _run_pipeline("rnn", req.pixels)
        return InferenceResponse(label=label, img_name=img_name)
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/lrinfer", response_model=InferenceResponse, tags=["LogisticRegression"])
async def lr_infer(req: InferenceRequest):
    try:
        label, img_name = _run_pipeline("lr", req.pixels)
        return InferenceResponse(label=label, img_name=img_name)
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback", tags=["Feedback"])
async def feedback(entry: FeedbackRequest):
    # load all rows
    with open(RESULTS_CSV, newline="") as f:
        reader     = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows       = list(reader)

    # update feedback for matching img_name
    for row in rows:
        if row.get("img_name") == entry.img_name:
            row["user_feedback"] = entry.user_feedback

    # rewrite CSV
    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

    return {"status": "feedback recorded"}

# ── Run server manually:  python main.py ------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )
