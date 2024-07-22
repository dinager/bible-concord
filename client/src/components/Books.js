import React, {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import {getBooks} from '../services/api';

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

    return (
        <div>
            <h1>Books</h1>
            <button onClick={() => navigate(`/add-book`)}>Add Book</button>
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
                        <td style={{textTransform: 'capitalize'}}>{book.name}</td>
                        <td style={{textTransform: 'capitalize'}}>{book.division}</td>
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
