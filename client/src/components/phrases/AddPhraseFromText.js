import React, { useState, useEffect } from 'react';
import {getBooksNames, getBookContent, addPhraseFromText, parseErrorResponse} from '../../services/api';
import './css/AddPhraseFromText.css'; // Import the CSS file

const AddPhraseFromText = ({ onAddPhrase, onCancel }) => {
    const [books, setBooks] = useState([]);
    const [selectedBook, setSelectedBook] = useState('');
    const [bookContent, setBookContent] = useState('');
    const [selectedPhrase, setSelectedPhrase] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchBooksNames();
    }, []);

    const fetchBooksNames = async () => {
        try {
            const response = await getBooksNames();
            setBooks(response || []); // Ensure response is always an array
            setLoading(false);
        } catch (error) {
            console.error('Error fetching book names:', error);
            setError('Error fetching book names');
            setLoading(false);
        }
    };

    const handleBookChange = async (e) => {
        const book = e.target.value;
        setSelectedBook(book);
        try {
            const content = await getBookContent(book);
            setBookContent(content);
        } catch (error) {
            console.error('Error fetching book content:', error);
            setError('Error fetching book content');
        }
    };

    const handleTextSelection = () => {
        const selection = window.getSelection();
        // remove `: . , ;` from the selection
        const s = selection.toString().replace(/[,;:.]/g, '');
        setSelectedPhrase(s);
    };

    const handleAddPhrase = async () => {
        if (selectedPhrase.split(' ').length < 3) {
            alert('Phrase name must be at least 3 words long');
            return;
        }
        // allow only characters, and spaces
        if (!/^[a-zA-Z' ]+$/.test(selectedPhrase)) {
            alert('Phrase name can only contain letters, apostrophes and spaces');
            return;
        }
        try {
            await addPhraseFromText(selectedBook, selectedPhrase);
            onAddPhrase(selectedPhrase);
        } catch (error) {
            alert(parseErrorResponse(error));
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="add-phrase-container">
            <h2 className="add-phrase-header">Select Book and Add Phrase from Text</h2>
            <div className="add-phrase-select-container">
                <label className="add-phrase-select-label">
                    Book:
                    <select
                        className="add-phrase-select"
                        value={selectedBook}
                        onChange={handleBookChange}
                    >
                        <option value="">Select a book</option>
                        {Array.isArray(books) && books.map((book) => (
                            <option key={book} value={book}>{book}</option>
                        ))}
                    </select>
                </label>
                <button className="add-phrase-back-button" onClick={onCancel}>Back</button>
            </div>
            {selectedBook && (
                <div className="book-content-container">
                    <p>Select a phrase from the text below:</p>
                    <div
                        onMouseUp={handleTextSelection}
                        className="book-content"
                    >
                        {bookContent}
                    </div>
                    {selectedPhrase && (
                        <div className="selected-phrase-container">
                            <p>Selected Phrase: <span className="selected-phrase">{selectedPhrase}</span></p>
                            <button className="add-phrase-button add-phrase-button-green" onClick={handleAddPhrase}>Add Phrase</button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default AddPhraseFromText;
