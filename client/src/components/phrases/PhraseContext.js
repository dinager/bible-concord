import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {getTextContext, parseErrorResponse} from '../../services/api';
import { FaArrowLeft } from 'react-icons/fa';

const PhraseContext = () => {
    const navigate = useNavigate();
    const { phraseText, book_title, chapter_num, verse_num, word_position } = useParams();
    const [contextDetail, setContextDetail] = useState(null);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');

    useEffect(() => {
        const fetchContextDetail = async () => {
            try {
                const response = await getTextContext(book_title, chapter_num, verse_num);
                setContextDetail(response);
                setMessage('');
                setMessageType('');
            } catch (error) {
                setMessage(`Failed to fetch context detail. ${parseErrorResponse(error)}`);
                setMessageType('error');
            }
        };

        fetchContextDetail();
    }, [phraseText, book_title, chapter_num, verse_num, word_position]);

    const highlightPhrase = (text, phrase) => {
        const regex = new RegExp(`(\\b${phrase}\\b)`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    };

    const renderContextDetail = () => {
        if (!contextDetail) {
            return null;
        }

        // Replace newline characters with <br> for HTML rendering and highlight the phrase
        const formattedContext = highlightPhrase(contextDetail.replace(/\n/g, '<br>'), phraseText);

        return (
            <div className="phrase-context">
                <pre dangerouslySetInnerHTML={{__html: formattedContext}}></pre>
            </div>
        );
    };

    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={() => navigate(`/phrase/${phraseText}/context`)} className="return-arrow"/> 
                <h1>Context detail for phrase name "{phraseText}"</h1>
            </div>
            {message && <p className={`n-message ${messageType}`}>{message}</p>}
            {renderContextDetail()}
        </div>
    );
};

export default PhraseContext;
