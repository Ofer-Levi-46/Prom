import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <div
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: '100vh',
            }}
        >
            <div
                style={{
                    width: '100%',
                    backgroundColor: '#f0f0f0',
                    maxWidth: '480px',
                    boxSizing: 'border-box',
                    border: '1px solid #ccc',
                    borderRadius: '8px',
                }}
            >
                <App />
            </div>
        </div>
    </StrictMode>
);
