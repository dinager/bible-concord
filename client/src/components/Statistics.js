import React, { useState, useEffect } from 'react';
import './Statistics.css';
import { getBooksNames, getTotalStats, getBookStats } from '../services/api';

function Statistics() {
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState('');
  const [details, setDetails] = useState(null);
  const [totals, setTotals] = useState({
    totalBooks: 0,
    totalGroups: 0,
    totalPhrases: 0,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch totals
        const totalData = await getTotalStats();
        setTotals({
          totalBooks: totalData['Total Number of Books'] || 0,
          totalGroups: totalData['Total Number of Groups'] || 0,
          totalPhrases: totalData['Total Number of Phrases'] || 0,
        });

        // Fetch the list of books
        const booksData = await getBooksNames();
        setBooks(booksData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleBookSelect = async (event) => {
    const selectedBookName = event.target.value;
    setSelectedBook(selectedBookName);
    if (!selectedBookName) {
      // Clear the details if no book is selected
      setDetails(null);
      return;
    }
    try {
      // If "All" is selected, pass null to get statistics for all books
      const detailsData = await getBookStats(selectedBookName === 'All' ? null : selectedBookName);
      setDetails(detailsData);
    } catch (error) {
      console.error('Error fetching book details:', error);
    }
  };

  // Function to capitalize the first letter of a string
  const capitalizeFirstLetter = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  return (
    <div className="Statistics">
      <div className="Statistics-content">
        <h1>Statistics</h1>

        <div className="overview">
          <h2>General Statistics:</h2>
          <div className="stat-item">
            <span>Total Number of Books:</span>
            <span>{totals.totalBooks}</span>
          </div>
          <div className="stat-item">
            <span>Total Number of Groups:</span>
            <span>{totals.totalGroups}</span>
          </div>
          <div className="stat-item">
            <span>Total Number of Phrases:</span>
            <span>{totals.totalPhrases}</span>
          </div>
        </div>

        <div className="book-selection">
          <h2>Select Book:</h2>
          <select value={selectedBook} onChange={handleBookSelect}>
            <option value="">Select a book</option>
            <option value="All">All Books</option>
            {books.map((bookName, index) => (
              <option key={index} value={bookName}>
                {capitalizeFirstLetter(bookName)}
              </option>
            ))}
          </select>
        </div>

        {details && (
          <div className="book-details">
            <h2>Book Details:</h2>
            <div className="book-stats">
              <div className="book-summary">
                <h3>Summary Statistics</h3>
                <p>Number of Chapters: {details.numChapters}</p>
                <p>Number of Verses: {details.numVerses}</p>
                <p>Total Number of Words: {details.numWords}</p>
                <p>Unique Words: {details.uniqueWords}</p>
                <p>Number of Letters: {details.numLetters}</p>
              </div>
              <div className="book-averages">
                <h3>Average Statistics</h3>
                <p>Verses per Chapter: {details.avgVersesPerChapter}</p>
                <p>Words per Verse: {details.avgWordsPerVerse}</p>
                <p>Letters per Verse: {details.avgLettersPerVerse}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      <img
        className="image-right"
        src="/Stats.jpeg"
        alt="Statistics"
      />
    </div>
  );
}

export default Statistics;
