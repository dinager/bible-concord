import React, { useState, useEffect } from 'react';
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

  useEffect(() => {
    const fetchBooks = async () => {
      const books = await getBooksNames();
      console.log("hey");
      console.log(books);
      setBooks(books);
    };

    fetchBooks();
  }, []);

  const handleBookChange = async (e) => {
    const bookName = e.target.value;
    setSelectedBook(bookName);
    setSelectedChapter('');
    setSelectedVerse('');
    setChapters([]);
    setVerses([]);

    if (bookName) {
      const numChapters = await getNumChaptersInBook(bookName);
      setChapters(Array.from({ length: numChapters }, (_, i) => i + 1));
    }
  };

  const handleChapterChange = async (e) => {
    const chapterNum = e.target.value;
    setSelectedChapter(chapterNum);
    setSelectedVerse('');
    setVerses([]);

    if (chapterNum) {
      const numVerses = await getNumVersesInChapter(selectedBook, chapterNum);
      setVerses(Array.from({ length: numVerses }, (_, i) => i + 1));
    }
  };

  const handleFilter = async () => {
    const filters = {
      book: selectedBook,
      chapter: selectedChapter,
      verse: selectedVerse,
      wordStartsWith: word,
    };
    const filteredWords = await filterWords(filters, pageIndex);
    setWords(filteredWords);
  };

  const handleReset = async () => {
    setSelectedBook('');
    setSelectedChapter('');
    setSelectedVerse('');
    setWord('');
    setChapters([]);
    setVerses([]);
    const filteredWords = await filterWords({}, pageIndex);
    setWords(filteredWords);
  };

  useEffect(() => {
    handleReset();
  }, []);

  return (
    <div>
      <h1>Word List</h1>
      <div className="filters">
        <div>
          <label>Book Name</label>
          <select value={selectedBook} onChange={handleBookChange}>
            <option value="">All</option>
            {books.map((book) => (
              <option key={book} value={book}>{book}</option>
            ))}
          </select>
        </div>
        <div>
          <label>Chapter</label>
          <select value={selectedChapter} onChange={handleChapterChange} disabled={!selectedBook}>
            <option value="">All</option>
            {chapters.map((chapter) => (
              <option key={chapter} value={chapter}>{chapter}</option>
            ))}
          </select>
        </div>
        <div>
          <label>Verse</label>
          <select value={selectedVerse} onChange={(e) => setSelectedVerse(e.target.value)} disabled={!selectedChapter}>
            <option value="">All</option>
            {verses.map((verse) => (
              <option key={verse} value={verse}>{verse}</option>
            ))}
          </select>
        </div>
        <div>
          <label>Word</label>
          <input type="text" value={word} onChange={(e) => setWord(e.target.value)} />
        </div>
        <div className="buttons">
          <button onClick={handleFilter}>Filter</button>
          <button onClick={handleReset}>Reset Filters</button>
        </div>
      </div>
      <div className="word-list">
        <ul>
          {words.map((word, index) => (
            <li key={index}>{word}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default WordList;
