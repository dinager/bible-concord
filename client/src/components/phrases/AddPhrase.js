import React, { useState } from 'react';
import './css/AddPhrase.css'; // Import the CSS file

const AddPhrase = ({ onAddPhrase, onCancel }) => {
    const [phraseName, setPhraseName] = useState('');

    const handleAddPhrase = () => {
        if (phraseName.split(' ').length < 3) {
            alert('Phrase name must be at least 3 characters long');
            return;
        }
        // allow only characters, and spaces
        if (!/^[a-zA-Z ]+$/.test(phraseName)) {
            alert('Phrase name can only contain letters and spaces');
            return;
        }
        onAddPhrase(phraseName);
        setPhraseName('');
    };

    return (
        <div className="add-phrase-container">
            <h2 className="add-phrase-header">Add New Phrase</h2>
            <div className="add-phrase-form-group">
                <label className="add-phrase-label">Phrase Name:</label>
                <input
                    className="add-phrase-input"
                    type="text"
                    value={phraseName}
                    onChange={(e) => setPhraseName(e.target.value)}
                />
            </div>
            <button className="add-phrase-button" onClick={handleAddPhrase}>Add Phrase</button>
            <button className="add-phrase-back-button" onClick={onCancel}>Back</button>
        </div>
    );
};

export default AddPhrase;
