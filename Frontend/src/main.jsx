import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import './index.css';
import LandingPage from './LandingPage.jsx';
import Draw from './Draw.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/welcome" replace />} />
        <Route path="/welcome" element={<LandingPage />} />
        <Route path="/draw" element={<Draw />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
