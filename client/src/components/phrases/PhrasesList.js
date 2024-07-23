import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPhrases, addPhrase, parseErrorResponse } from '../../services/api'; // Assuming these functions exist
import AddPhrase from './AddPhrase';

const PhrasesList = () => {
    const [phrases, setPhrases] = useState([]);
    const [showAddPhrase, setShowAddPhrase] = useState(false);
    const navigate = useNavigate();

    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'

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

    return (
        <div>
            <h1>Phrases</h1>
            <button onClick={() => setShowAddPhrase(true)}>Add Phrase</button>
            {showAddPhrase && <AddPhrase onAddPhrase={handleAddPhrase} />}
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
