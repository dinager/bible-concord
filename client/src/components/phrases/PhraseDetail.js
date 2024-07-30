import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getPhraseReference, parseErrorResponse } from '../../services/api'; 
import { FaArrowLeft } from 'react-icons/fa';

const PhraseDetail = () => {
    const navigate = useNavigate();

    const { phraseName } = useParams();
    const [context, setContext] = useState([]);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); 

    useEffect(() => {
        const fetchContext = async () => {
            try {
                const response = await getPhraseReference(phraseName);
                if (response) {
                    setContext(response);
                } else {
                    setContext([]);
                }
                setMessage('');
                setMessageType('');
            } catch (error) {
                setMessage(`Failed to fetch context for phrase "${phraseName}". ${parseErrorResponse(error)}`);
                setMessageType('error');
            }
        };

        fetchContext();
    }, [phraseName]);

    const handleRowClick = (book_title, chapter_num, verse_num, word_position) => {
        navigate(`/phrase/${phraseName}/book/${book_title}/chapter_num/${chapter_num}/verse_num/${verse_num}/word_position/${word_position}`);
    };

    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={() => navigate('/phrases')} className="return-arrow" />
                <h1>Context in phrase: <span style={{ textTransform: 'uppercase', color: 'blue', fontStyle: 'italic' }}>{phraseName}</span></h1>
            </div>
            {message && <p className={`n-message ${messageType}`}>{message}</p>}
            <table>
                <thead>
                    <tr>
                        <th>Book Name</th>
                        <th>Chapter Number</th>
                        <th>Verse Number</th>
                        <th>Word Position</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {context.length > 0 ? (
                        context.map((ref, index) => (
                            <tr key={index}>
                                <td>{ref.title}</td>
                                <td>{ref.chapter_num}</td>
                                <td>{ref.verse_num}</td>
                                <td>{ref.word_position}</td>
                                <td>
                                    <button type="button" onClick={() => handleRowClick(ref.title, ref.chapter_num, ref.verse_num, ref.word_position)}>View Context</button>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="4">No context available</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default PhraseDetail;
