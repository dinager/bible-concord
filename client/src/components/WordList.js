import React, { useState, useEffect, useCallback } from 'react';
import {getNumChaptersInBook, getNumVersesInChapter, filterWords, getBooksNames} from '../services/api';

const WordList = () => {
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState('');
  const [chapters, setChapters] = useState([]);
  const [selectedChapter, setSelectedChapter] = useState('');
  const [verses, setVerses] = useState([]);
  const [selectedVerse, setSelectedVerse] = useState('');
  const [word, setWord] = useState('');
  const [words, setWords] = useState([]);
  const [pageIndex, setPageIndex] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const pageSize = 15;

  useEffect(() => {
    const fetchBooks = async () => {
      const books = await getBooksNames();
      setBooks(books);
    };

    fetchBooks();
  }, []);

  const fetchWords = async (filters, pageIndex) => {
    const filteredWords = await filterWords(filters, pageIndex);
    setWords(filteredWords.words);
    setTotalPages(Math.ceil(filteredWords.total / pageSize));
  };

  const handleBookChange = async (e) => {
    const bookName = e.target.value;
    setSelectedBook(bookName);
    setSelectedChapter('');
    setSelectedVerse('');
    setChapters([]);
    setVerses([]);
    setPageIndex(0);

    if (bookName) {
      const numChapters = await getNumChaptersInBook(bookName);
      setChapters(Array.from({ length: numChapters }, (_, i) => i + 1));
    }

    fetchWords({
      book: bookName,
      chapter: '',
      verse: '',
      wordStartsWith: word,
    }, 0);
  };

  const handleChapterChange = async (e) => {
    const chapterNum = e.target.value;
    setSelectedChapter(chapterNum);
    setSelectedVerse('');
    setVerses([]);
    setPageIndex(0);

    if (chapterNum) {
      const numVerses = await getNumVersesInChapter(selectedBook, chapterNum);
      setVerses(Array.from({ length: numVerses }, (_, i) => i + 1));
    }

    fetchWords({
      book: selectedBook,
      chapter: chapterNum,
      verse: '',
      wordStartsWith: word,
    }, 0);
  };

  const handleVerseChange = (e) => {
    const verseNum = e.target.value;
    setSelectedVerse(verseNum);
    setPageIndex(0);

    fetchWords({
      book: selectedBook,
      chapter: selectedChapter,
      verse: verseNum,
      wordStartsWith: word,
    }, 0);
  };

  const debounce = (func, wait) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  };

  const debouncedFetchWords = useCallback(
    debounce((filters, pageIndex) => {
      fetchWords(filters, pageIndex);
    }, 300),
    []
  );

  const handleWordChange = (e) => {
    const wordValue = e.target.value;
    setWord(wordValue);
    setPageIndex(0);

    debouncedFetchWords({
      book: selectedBook,
      chapter: selectedChapter,
      verse: selectedVerse,
      wordStartsWith: wordValue,
    }, 0);
  };

  const handleReset = async () => {
    setSelectedBook('');
    setSelectedChapter('');
    setSelectedVerse('');
    setWord('');
    setChapters([]);
    setVerses([]);
    setPageIndex(0);

    fetchWords({}, 0);
  };

  useEffect(() => {
    handleReset();
  }, []);

  const handlePageChange = (newPageIndex) => {
    setPageIndex(newPageIndex);
    fetchWords({
      book: selectedBook,
      chapter: selectedChapter,
      verse: selectedVerse,
      wordStartsWith: word,
    }, newPageIndex);
  };

  return (
    <div>
      <h1>Word List</h1>
      <div className="filters">
        <label>Book Name:</label>
        <select value={selectedBook} onChange={handleBookChange}>
          <option value="">All</option>
          {books.map((book) => (
            <option key={book} value={book}>{book}</option>
          ))}
        </select>
        <label>Chapter:</label>
        <select value={selectedChapter} onChange={handleChapterChange} disabled={!selectedBook}>
          <option value="">All</option>
          {chapters.map((chapter) => (
            <option key={chapter} value={chapter}>{chapter}</option>
          ))}
        </select>
        <label>Verse:</label>
        <select value={selectedVerse} onChange={handleVerseChange} disabled={!selectedChapter}>
          <option value="">All</option>
          {verses.map((verse) => (
            <option key={verse} value={verse}>{verse}</option>
          ))}
        </select>
        <label>Word:</label>
        <input type="text" value={word} onChange={handleWordChange} />
        <button onClick={handleReset}>Reset Filters</button>
      </div>
      <div className="word-list">
        <table>
          <tbody>
            {words.map((word, index) => (
              <tr key={index} className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                <td>{word}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <Pagination
          currentPage={pageIndex}
          totalPages={totalPages}
          onPageChange={handlePageChange}
        />
      </div>
    </div>
  );
};

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  const handlePrevious = () => {
    if (currentPage > 0) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages - 1) {
      onPageChange(currentPage + 1);
    }
  };

  return (
    <div className="pagination">
      <button onClick={handlePrevious} disabled={currentPage === 0}>Previous</button>
      <span>Page {currentPage + 1} of {totalPages}</span>
      <button onClick={handleNext} disabled={currentPage === totalPages - 1}>Next</button>
    </div>
  );
};

export default WordList;
