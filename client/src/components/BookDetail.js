import React, {useState, useEffect} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {getBookContent} from '../services/api';
import {FaArrowLeft} from "react-icons/fa";

const BookDetail = () => {
    const navigate = useNavigate();

    const {name} = useParams();
    const [bookContent, setBookContent] = useState('');

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


    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={() => navigate('/books')} className="return-arrow"/>
                <h1 style={{textTransform: 'uppercase'}}>{name}</h1>
            </div>
            <div className="book-content" style={{maxHeight: '650px'}}>
                <pre>{bookContent}</pre>
            </div>
        </div>
    );
};

export default BookDetail;
