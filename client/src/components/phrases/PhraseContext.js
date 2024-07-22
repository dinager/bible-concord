import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getPhraseContext, parseErrorResponse } from '../../services/api'; 
import { FaArrowLeft } from 'react-icons/fa';

const PhraseContext = () => {
    const navigate = useNavigate();
    const { phraseName } = useParams();
    const [context, setContext] = useState([]);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'

    useEffect(() => {
        const fetchContext = async () => {
            try {
                const response = await getPhraseContext(phraseName);
                setContext(response);
                setMessage('');
                setMessageType('');
            } catch (error) {
                setMessage(`Failed to fetch context for phrase "${phraseName}". ${parseErrorResponse(error)}`);
                setMessageType('error');
            }
        };

        fetchContext();
    }, [phraseName]);

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
                        <th>Book Title</th>
                        <th>Chapter Number</th>
                        <th>Verse Number</th>
                    </tr>
                </thead>
                <tbody>
                    {context && context.length > 0 ? (
                        <tr>
                            <td>{context.book_title}</td>
                            <td>{context.chapter_num}</td>
                            <td>{context.verse_num}</td>
                        </tr>
                    ) : (
                        <tr>
                            <td colSpan="3">No context available</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default PhraseContext;
