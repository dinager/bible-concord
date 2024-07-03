import React, {useEffect, useState} from 'react';
import {useParams, useNavigate} from 'react-router-dom';
import {FaArrowLeft} from 'react-icons/fa';
import {getTextContext} from '../services/api';

const TextContext = () => {
    const {word, book, chapter, verse, index} = useParams();
    const navigate = useNavigate();
    const [text, setText] = useState('');

    useEffect(() => {
        const fetchTextContext = async () => {
            const contextText = await getTextContext(word, book, chapter, verse, index);
            const highlightedText = highlightWord(contextText, word);
            setText(highlightedText);
        };

        fetchTextContext();
    }, [word, book, chapter, verse, index]);

    const highlightWord = (text, word) => {
        const regex = new RegExp(`(${word})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    };

    const handleBackClick = () => {
        navigate(`/word/${word}/appearances`); // todo: check how to reserve filters
    };

    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={handleBackClick} className="return-arrow"/>
                <h1>
                    <span style={{textTransform: 'uppercase', color: 'blue'}}>{word} </span>
                    <span style={{fontStyle: 'italic'}}>
                        <span style={{textTransform: 'capitalize'}}>{book} </span>
                        {chapter}:{verse} (position {index})
                    </span>

                </h1>
            </div>
            <div className="book-content">
                <pre dangerouslySetInnerHTML={{__html: text}}></pre>
            </div>
        </div>
    );
};

export default TextContext;
