import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getBooks, deleteBook } from '../services/api';
import './Books.css'; // Import the CSS file

const Books = () => {
    const [books, setBooks] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchBooks = async () => {
            try {
                const booksData = await getBooks();
                setBooks(booksData);
            } catch (error) {
                console.error('Error fetching books:', error);
            }
        };

        fetchBooks();
    }, []);

    const handleRowClick = (bookName) => {
        navigate(`/book/${bookName}`);
    };

    const handleDelete = async (bookName) => {
        const confirmDelete = window.confirm(`Are you sure you want to delete the book: ${bookName}?`);
        if (confirmDelete) {
            try {
                await deleteBook(bookName);
                setBooks((prevBooks) => prevBooks.filter(book => book.name !== bookName));
            } catch (error) {
                console.error('Error deleting book:', error);
            }
        }
    };

    return (
        <div>
            <h1>Books</h1>
            <button onClick={() => navigate(`/add-book`)}>Add Book</button>
            <div style={{maxHeight: '700px', overflowY: 'auto', border: '1px solid #ccc'}}>
                <table style={{width: '100%', borderCollapse: 'collapse'}}>
                    <thead>
                    <tr>
                        <th>Book Name</th>
                        <th>Division</th>
                        <th>Insert Time</th>
                        <th>Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {books.map((book) => (
                        <tr key={book.name} onClick={() => handleRowClick(book.name)}>
                            <td style={{ textTransform: 'capitalize'}}>{book.name}</td>
                            <td style={{ textTransform: 'capitalize'}}>{book.division}</td>
                            <td>{book.insertTime}</td>
                            <td>
                                <button
                                    type="button"
                                    onClick={() => handleRowClick(book.name)}
                                    className="button-spacing button-green"
                                >
                                    Show Content
                                </button>
                                <button
                                    type="button"
                                    onClick={(e) => {e.stopPropagation();handleDelete(book.name);}}
                                    className="button-delete"
                                >
                                    Delete Book
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Books;
