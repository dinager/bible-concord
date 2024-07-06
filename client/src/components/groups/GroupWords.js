import React, {useState, useEffect} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {getWordsInGroup, addWordToGroup, parseErrorResponse} from '../../services/api';
import AddWord from './AddWord';
import {FaArrowLeft} from 'react-icons/fa';

const GroupWords = () => {
    const navigate = useNavigate();

    const {groupName} = useParams();
    const [words, setWords] = useState([]);
    const [showAddWord, setShowAddWord] = useState(false);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'


    useEffect(() => {
        fetchWords();
    }, []);

    const fetchWords = async () => {
        const response = await getWordsInGroup(groupName);
        setWords(response.words);
    };

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


    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={() => navigate('/groups')} className="return-arrow"/>
                <h1>Words in
                    <span style={{textTransform: 'uppercase', color: 'blue', fontStyle: 'italic'}}> {groupName} </span>
                </h1>
            </div>
            <div className="div-line-wrapper">
                <button onClick={() => setShowAddWord(true)}>Add Word</button>
                <button onClick={handleAddWordFromIndex}>Add Word From Index</button>
            </div>
            {showAddWord && <AddWord onAddWord={handleAddWord}/>}
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
