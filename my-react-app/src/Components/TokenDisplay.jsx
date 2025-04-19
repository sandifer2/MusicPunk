import React from 'react';
import '../CSS/TokenDisplay.css';

function TokenDisplay({ tokenCount }) {
    return (
        <div className="token-display">
            <span className="token-icon">🪙</span>
            <span className="token-count">{tokenCount}</span>
        </div>
    );
}

export default TokenDisplay;