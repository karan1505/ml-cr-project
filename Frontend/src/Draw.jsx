import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function Draw() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '2rem',
      fontFamily: 'sans-serif'
    }}>
      <h1>Drawing Canvas</h1>
      <p>This is where the character drawing and prediction will happen.</p>
    </div>
  );
}

export default Draw;

  