import React from 'react';

function LandingPage() {
  return (
    <div style={{
      fontFamily: 'Inter, sans-serif',
      backgroundColor: '#1a202c', // Darker background
      color: '#edf2f7',         // Lighter text
      minHeight: '60vh',
      width: '50vw',         // Ensure full viewport width
      overflow: 'hidden',       // Prevent scrolling
      boxSizing: 'border-box',
      padding: '2rem',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundImage: 'radial-gradient(circle, rgba(26,32,44,1) 0%, rgba(0,0,0,1) 100%)', // Gradient background
    }}>
      <h1 style={{
        fontSize: 'clamp(2.5rem, 6vw, 4rem)', // Responsive font size
        marginBottom: '1.5rem',
        lineHeight: 1.1,
        fontWeight: 700,      // Bold font
        textAlign: 'center',
      }}>
        EMNIST Character Recognition
      </h1>
      <p style={{
        fontSize: 'clamp(1.1rem, 3vw, 1.3rem)',
        color: '#cbd5e0',         // Lighter secondary text
        textAlign: 'center',
        maxWidth: '700px',       // Wider text container
        marginBottom: '2rem',
        lineHeight: 1.6,          // Improved line height for readability
      }}>
        Unleash the power of machine learning to recognize your handwritten characters. Simply draw letters or digits, and our intelligent model, trained on the extensive EMNIST dataset, will instantly provide its prediction. Experience the magic of AI in your browser!
      </p>
      <a
        href="/draw"
        style={{
          padding: '1rem 2rem',
          fontSize: 'clamp(1.1rem, 3vw, 1.2rem)',
          fontWeight: 600,      // Semi-bold font
          textDecoration: 'none',
          backgroundColor: '#4a5568', // Muted button color
          color: '#f7fafc',         // Light button text
          borderRadius: '0.75rem',  // More rounded corners
          boxShadow: '0 6px 15px rgba(0,0,0,0.2)', // Subtle shadow
          transition: 'background-color 0.3s ease', // Smooth transition
          '&:hover': {
            backgroundColor: '#718096', // Darker shade on hover
          },
        }}
      >
        Start Drawing
      </a>
    </div>
  );
}

export default LandingPage;
