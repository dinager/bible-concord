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
        <img src="/Stats.jpeg" alt="Statistics" className="image-right" />
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
        <h2>Select a Book:</h2>
        <select onChange={handleBookSelect} value={selectedBook}>
          <option value="">-- Select a Book --</option>
          <option value="All">All</option>
          {books.map((book) => (
            <option key={book} value={book}>
              {book}
            </option>
          ))}
        </select>
      </div>

      {selectedBook && details && (
        <div className="book-details">
          <h2>
            {selectedBook === 'All'
              ? 'All Books Statistics'
              : `${capitalizeFirstLetter(selectedBook)} Details`}
          </h2>

          <div className="book-stats">
            <div className="book-summary">
              <h3>Book Summary</h3>
              <p>Number of Chapters: {details?.numChapters ?? 'N/A'}</p>
              <p>Number of Verses: {details?.numVerses ?? 'N/A'}</p>
              <p>Total Words: {details?.totalWords ?? 'N/A'}</p>
              <p>Total Unique Words: {details?.totalUniqueWords ?? 'N/A'}</p>
              <p>Total Letters: {details?.totalLetters ?? 'N/A'}</p>
            </div>

            <div className="book-averages">
              <h3>Average Statistics</h3>
              <p>Average Number of Verses per Chapter: {details?.avgVersesPerChapter ?? 'N/A'}</p>
              <p>Average Number of Words per Verse: {details?.avgWordsPerVerse ?? 'N/A'}</p>
              <p>Average Number of Letters per Verse: {details?.avgLettersPerVerse ?? 'N/A'}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Statistics;
