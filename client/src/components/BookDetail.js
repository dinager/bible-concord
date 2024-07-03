import React, {useState, useEffect} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {getBookContent} from '../services/api';
import {FaArrowLeft} from "react-icons/fa";

const BookDetail = () => {
    const {name} = useParams();
    const [bookContent, setBookContent] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchBookContent = async () => {
            try {
                const content = await getBookContent(name);
                setBookContent(content);
            } catch (error) {
                console.error('Error fetching book content:', error);
            }
        };

        fetchBookContent();
    }, [name]);

    const handleBackClick = () => {
        navigate('/books');
    };

    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={handleBackClick} className="return-arrow"/>
                <h1>{name}</h1>
            </div>
            <div className="book-content">
                <pre>{bookContent}</pre>
            </div>
        </div>
    );
};

export default BookDetail;
