import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/app.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);


// client side rendered app: react (cra)
  // -> db which is Firebase
  // -> react-loading-skeleton
  // tailwind

// architecture(folder structure)
  // src
    // componenets,
    // constants,
    // context,
    // helpers,
    // lib(firebase is gointo live in here)
    // services(firebase functions in here)
    // styles(tailwind's folder(app/tailwind))