import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPhrases, addPhrase, deletePhrase, parseErrorResponse } from '../../services/api'; // Make sure deletePhrase is imported
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

    const handleDelete = async (phrase) => {
        const confirmDelete = window.confirm(`Are you sure you want to delete the phrase: ${phrase}?`);
        if (confirmDelete) {
            try {
                await deletePhrase(phrase);
                setPhrases((prevPhrases) => prevPhrases.filter(p => p !== phrase));
                setMessage(`Phrase "${phrase}" deleted successfully!`);
                setMessageType('success');
            } catch (error) {
                setMessage(`Failed to delete phrase "${phrase}". ${parseErrorResponse(error)}`);
                setMessageType('error');
            }
        }
    };

    return (
        <div>
            <h1>Phrases</h1>
            <div style={{ display: 'flex', gap: '10px' }}>
                <button 
                    onClick={() => setShowAddPhrase(true)} 
                    disabled={showAddPhrase || showAddPhraseFromText}
                    className={showAddPhrase || showAddPhraseFromText ? 'disabled-button' : 'button-add-phrase'}
                >
                    Add Phrase
                </button>
                <button 
                    onClick={() => setShowAddPhraseFromText(true)} 
                    disabled={showAddPhrase || showAddPhraseFromText}
                    className={showAddPhrase || showAddPhraseFromText ? 'disabled-button' : 'button-add-phrase-from-text'}
                >
                    Add Phrase From Text
                </button>
            </div>
            {showAddPhrase && <AddPhrase onAddPhrase={handleAddPhrase} onCancel={() => setShowAddPhrase(false)} />}
            {showAddPhraseFromText && <AddPhraseFromText onAddPhrase={handleAddPhraseFromText} onCancel={() => setShowAddPhraseFromText(false)} />}
            {message && <p className={`n-message ${messageType}`}>{message}</p>}

            <table>
                <thead>
                    <tr>
                        <th>Phrase Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {phrases.map((phrase, index) => (
                        <tr className={index % 2 === 0 ? 'even-row' : 'odd-row'} key={phrase}>
                            <td>{phrase}</td>
                            <td>
                                <button
                                    onClick={() => navigate(`/phrase/${phrase}/context`)}
                                    className="button-view-words"
                                >
                                    See Reference
                                </button>
                                <button
                                    onClick={(e) => { e.stopPropagation(); handleDelete(phrase); }}
                                    className="button-delete"
                                >
                                    Delete Phrase
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default PhrasesList;
