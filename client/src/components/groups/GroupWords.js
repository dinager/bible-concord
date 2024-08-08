import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
    getWordsInGroup,
    addWordToGroup,
    parseErrorResponse,
    getGroupWordAppearancesIndex
} from '../../services/api';
import AddWord from './AddWord';
import { FaArrowLeft } from 'react-icons/fa';

const GroupWords = () => {
    const navigate = useNavigate();

    const { groupName } = useParams();
    const [words, setWords] = useState([]);
    const [showAddWord, setShowAddWord] = useState(false);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'

    const fetchWords = useCallback(async () => {
        const response = await getWordsInGroup(groupName);
        setWords(response.words);
    }, [groupName]);

    useEffect(() => {
        fetchWords();
    }, [fetchWords]);

    const handleAddWord = async (word) => {
        try {
            await addWordToGroup(groupName, word);
            setMessage(`Word "${word}" added successfully to ${groupName}!`);
            setMessageType('success');
        } catch (error) {
            setMessage(`Failed to add word "${word}" to ${groupName}. ${parseErrorResponse(error)}`);
            setMessageType('error');
        }
        fetchWords();
        setShowAddWord(false);
    };

    const handleAddWordFromIndex = () => {
        navigate(`/groups/${groupName}/add-word-from-list`);
    };

    const handleSearchWordFromIndex = () => {
        navigate(`/search-words/${groupName}`);
    };

    const exportToCSV = async () => {
        let csvContent = 'data:text/csv;charset=utf-8,Word,Book,Chapter,Verse,Word Position,Verse Text\n';
        const wordAppearancesIndex = await getGroupWordAppearancesIndex(groupName);
    
        // Generate CSV content from the aggregated data
        for (const entry of wordAppearancesIndex.values()) {
            const row = [
                entry.word,
                entry.book,
                entry.chapter,
                entry.verse,
                entry.word_position,
                entry.verse_text,
            ];
    
            csvContent += row.join(',') + '\n';
        }
    
        // Encode CSV content for download
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', `group-name_${groupName}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={() => navigate('/groups')} className="return-arrow" />
                <h1>Words in
                    <span style={{ textTransform: 'uppercase', color: 'blue', fontStyle: 'italic' }}> {groupName} </span>
                </h1>
            </div>
            <div className="div-line-wrapper">
                <button onClick={() => setShowAddWord(true)}>Add Word</button>
                <button onClick={handleAddWordFromIndex}>Add Word From Index</button>
                <button onClick={handleSearchWordFromIndex}>Search Words In Group</button>
                <button onClick={exportToCSV}>Export to CSV</button>
            </div>
            {showAddWord && <AddWord onAddWord={handleAddWord} />}
            {message && <p className={`n-message ${messageType}`}>{message}</p>}
            <table>
                <tbody>
                    {words.map((word, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                            <td>{word}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default GroupWords;
