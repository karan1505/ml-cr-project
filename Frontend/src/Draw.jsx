// src/App.js
import React, { useRef, useState, useEffect } from 'react';
import './App.css';

const API_BASE   = 'http://localhost:8000';
const CANVAS_SZ  = 280;    // 10 × 28 px
const BRUSH_SIZE = 12;     // ≈3‑4 px stroke after down‑sample

function Draw() {
  const bigCanvasRef   = useRef(null);
  const smallCanvasRef = useRef(null);

  const [isDrawing, setIsDrawing]   = useState(false);
  const [lastPos,   setLastPos]     = useState({ x: 0, y: 0 });
  const [endpoint,  setEndpoint]    = useState('cnninfer');

  const [showModal, setShowModal]           = useState(false);
  const [predictedLabel, setPredictedLabel] = useState('');
  const [imgName, setImgName]               = useState('');

  /* ------------ initialise 280×280 black canvas ------------ */
  useEffect(() => {
    const c = bigCanvasRef.current;
    c.width  = CANVAS_SZ;
    c.height = CANVAS_SZ;
    const ctx = c.getContext('2d');
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, CANVAS_SZ, CANVAS_SZ);
  }, []);

  /* ------------ pointer helpers ------------ */
  const getPointerPos = e => {
    const rect = bigCanvasRef.current.getBoundingClientRect();
    const x = e.touches ? e.touches[0].clientX : e.clientX;
    const y = e.touches ? e.touches[0].clientY : e.clientY;
    return { x: x - rect.left, y: y - rect.top };
  };

  const startDrawing = e => {
    setLastPos(getPointerPos(e));
    setIsDrawing(true);
  };
  const draw = e => {
    if (!isDrawing) return;
    const ctx = bigCanvasRef.current.getContext('2d');
    const pos = getPointerPos(e);
    ctx.strokeStyle = 'white';
    ctx.lineWidth   = BRUSH_SIZE;
    ctx.lineCap     = 'round';
    ctx.beginPath();
    ctx.moveTo(lastPos.x, lastPos.y);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    setLastPos(pos);
  };
  const stopDrawing = () => setIsDrawing(false);

  const clearCanvas = () => {
    const ctx = bigCanvasRef.current.getContext('2d');
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, CANVAS_SZ, CANVAS_SZ);
  };

  /* ------------  down‑sample, orient & infer  ------------ */
  const infer = async () => {
    // 1. shrink 280×280 → 28×28
    const small = smallCanvasRef.current;
    small.width = 28; small.height = 28;
    const sctx = small.getContext('2d');
    sctx.fillStyle = 'black';
    sctx.fillRect(0, 0, 28, 28);
    sctx.drawImage(bigCanvasRef.current, 0, 0, 28, 28);

    // 2. RGBA → float32 stroke=1, bg=0
    const rgba = sctx.getImageData(0, 0, 28, 28).data;
    const tmp = new Float32Array(28 * 28);
    for (let i = 0, j = 0; i < rgba.length; i += 4, ++j) {
      tmp[j] = rgba[i] / 255;
    }

    // 3. transpose + horizontal flip (EMNIST orientation)
    const pixels = new Float32Array(28 * 28);
    for (let y = 0; y < 28; y++) {
      for (let x = 0; x < 28; x++) {
        const src = y * 28 + x;
        const dst = x * 28 + (27 - y);
        pixels[dst] = tmp[src];
      }
    }

    // 4. send to backend
    try {
      const res = await fetch(`${API_BASE}/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pixels: Array.from(pixels) })
      });
      if (!res.ok) throw new Error(res.statusText);
      const { label, img_name } = await res.json();
      setPredictedLabel(label);
      setImgName(img_name);
      setShowModal(true);
    } catch (err) {
      console.error('Inference error:', err);
      alert('Inference failed; see console.');
    }
  };

  /* ------------ feedback endpoint ------------ */
  const submitFeedback = async decision => {
    try {
      const res = await fetch(`${API_BASE}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ img_name: imgName, user_feedback: decision })
      });
      if (!res.ok) throw new Error(res.statusText);
      setShowModal(false);
    } catch (err) {
      console.error('Feedback error:', err);
      alert('Failed to submit feedback; see console.');
    }
  };

  /* ------------ UI ------------ */
  return (
    <div style={{ display:'flex', flexDirection:'column', alignItems:'center', padding:'2rem', fontFamily:'sans-serif' }}>
      <h1>Drawing Canvas</h1>
      <p>Draw a character (white on black) then click <b>Infer</b>.</p>

      <div style={{ marginBottom:'1rem' }}>
        <label htmlFor="model-select" style={{ marginRight:'0.5rem' }}>Model:</label>
        <select id="model-select" value={endpoint} onChange={e => setEndpoint(e.target.value)}>
          <option value="cnninfer">CNN</option>
          <option value="rnninfer">RNN</option>
          <option value="lrinfer">Logistic Regression</option>
        </select>
      </div>

      <canvas
        ref={bigCanvasRef}
        style={{ border:'2px solid #555', touchAction:'none', cursor:'crosshair' }}
        onMouseDown={startDrawing} onMouseMove={draw}
        onMouseUp={stopDrawing}   onMouseLeave={stopDrawing}
        onTouchStart={startDrawing} onTouchMove={draw}
        onTouchEnd={stopDrawing}
      />

      <div style={{ marginTop:'1rem' }}>
        <button onClick={clearCanvas}>Clear</button>
        <button onClick={infer} style={{ marginLeft:'1rem' }}>Infer</button>
      </div>

      <canvas ref={smallCanvasRef} style={{ display:'none' }} />

      {showModal && (
        <div style={{
          position:'fixed', top:0, left:0, width:'100%', height:'100%',
          background:'rgba(0,0,0,0.5)',
          display:'flex', alignItems:'center', justifyContent:'center'
        }}>
          <div style={{
            background:'#fff', color:'#000',
            padding:'1.5rem', borderRadius:'8px',
            width:'90%', maxWidth:'360px', textAlign:'center',
            boxShadow:'0 2px 10px rgba(0,0,0,0.2)'
          }}>
            <h2 style={{ marginBottom:'1rem' }}>Prediction</h2>
            <p style={{ fontSize:'1.75rem', margin:'1rem 0' }}>{predictedLabel}</p>
            <p>Was this correct?</p>
            <div style={{ display:'flex', justifyContent:'space-around', marginTop:'1rem' }}>
              <button onClick={() => submitFeedback('correct')} style={{ padding:'0.5rem 1rem' }}>Yes</button>
              <button onClick={() => submitFeedback('incorrect')} style={{ padding:'0.5rem 1rem' }}>No</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Draw;
