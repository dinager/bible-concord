import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPhrases, addPhrase, parseErrorResponse } from '../../services/api';
import AddPhrase from './AddPhrase';
import AddPhraseFromText from './AddPhraseFromText';
import './css/PhrasesList.css'; // Make sure to import the CSS file

const PhrasesList = () => {
    const [phrases, setPhrases] = useState([]);
    const [showAddPhrase, setShowAddPhrase] = useState(false);
    const [showAddPhraseFromText, setShowAddPhraseFromText] = useState(false);
    const navigate = useNavigate();

    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    useEffect(() => {
        fetchPhrases();
    }, []);

    const fetchPhrases = async () => {
        const response = await getPhrases();
        setPhrases(response.phrases);
    };

    const handleAddPhrase = async (phraseName) => {
        try {
            await addPhrase(phraseName);
            setMessage(`Phrase "${phraseName}" added successfully!`);
            setMessageType('success');
        } catch (error) {
            setMessage(`Failed to add phrase "${phraseName}". ${parseErrorResponse(error)}`);
            setMessageType('error');
        }
        fetchPhrases();
        setShowAddPhrase(false);
    };

    const handleAddPhraseFromText = async (phraseName) => {
        setMessage(`Phrase "${phraseName}" added successfully!`);
        setMessageType('success');
        fetchPhrases();
        setShowAddPhraseFromText(false);
    };

    const handleShowAddPhrase = () => {
        setShowAddPhrase(true);
        setShowAddPhraseFromText(false);
    };

    const handleShowAddPhraseFromText = () => {
        setShowAddPhraseFromText(true);
        setShowAddPhrase(false);
    };

    const handleCancelAddPhraseFromText = () => {
        setShowAddPhraseFromText(false);
    };

    const handleCancelAddPhrase = () => {
        setShowAddPhrase(false);
    };

    return (
        <div>
            <h1>Phrases</h1>
            <div style={{ display: 'flex', gap: '10px' }}>
                <button 
                    onClick={handleShowAddPhrase} 
                    disabled={showAddPhrase || showAddPhraseFromText}
                    className={showAddPhrase || showAddPhraseFromText ? 'disabled-button' : ''}
                >
                    Add Phrase
                </button>
                <button 
                    onClick={handleShowAddPhraseFromText} 
                    disabled={showAddPhrase || showAddPhraseFromText}
                    className={showAddPhrase || showAddPhraseFromText ? 'disabled-button' : ''}
                >
                    Add Phrase from Text
                </button>
            </div>
            {showAddPhrase && <AddPhrase onAddPhrase={handleAddPhrase} onCancel={handleCancelAddPhrase} />}
            {showAddPhraseFromText && <AddPhraseFromText onAddPhrase={handleAddPhraseFromText} onCancel={handleCancelAddPhraseFromText} />}
            {message && <p className={`n-message ${messageType}`}>{message}</p>}

            <table>
                <thead>
                    <tr>
                        <th>Phrase Name</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {phrases.map((phrase, index) => (
                        <tr className={index % 2 === 0 ? 'even-row' : 'odd-row'} key={phrase}>
                            <td>{phrase}</td>
                            <td>
                                <button onClick={() => navigate(`/phrase/${phrase}/context`)}>See Reference</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default PhrasesList;
