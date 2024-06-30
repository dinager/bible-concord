import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {Link, useParams} from 'react-router-dom';

const BookDetail = () => {
  const { name } = useParams();
  const [bookContent, setBookContent] = useState('');

  useEffect(() => {
    const fetchBookContent = async () => {
      try {
        const response = await axios.get(`http://localhost:4200/api/get_book_content/${name}`);
        setBookContent(response.data);
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
