import React, { useState, useEffect } from 'react';
import {Link, useParams} from 'react-router-dom';
import { getBookContent } from '../services/api';

const BookDetail = () => {
  const { name } = useParams();
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
      <Link to="/books" className="return-link">Return to Books</Link>
      <h1>{name}</h1>
      <div className="book-content">
        <pre>{bookContent}</pre>
      </div>
    </div>
  );
};

export default BookDetail;
