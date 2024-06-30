import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const Books = () => {
  const [books, setBooks] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get('http://localhost:4200/api/get_books');
        setBooks(response.data.books);
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    };

    fetchBooks();
  }, []);

  const handleRowClick = (bookName) => {
    navigate(`/book/${bookName}`);
  };

  return (
      <div>
        <Link to="/add-book" className="return-link">Add Book</Link>
        <h1>Books</h1>
        <table>
          <thead>
          <tr>
            <th>Book Name</th>
            <th>Division</th>
            <th>Insert Time</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          {books.map((book) => (
              <tr key={book.name} onClick={() => handleRowClick(book.name)}>
                <td>{book.name}</td>
                <td>{book.division}</td>
                <td>{book.insertTime}</td>
                <td>
                  <button type="button" onClick={() => handleRowClick(book.name)}>Show Content</button>
                </td>
              </tr>
          ))}
          </tbody>
        </table>
      </div>
  );
};

export default Books;
