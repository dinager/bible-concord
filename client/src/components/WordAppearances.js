import React, { useState, useEffect } from 'react';
import {useLocation, useParams} from 'react-router-dom';
import { getBooksNames, getNumChaptersInBook, getNumVersesInChapter, getWordAppearances } from '../services/api';
import Pagination from "./Pagination";

const WordAppearances = () => {
  const location = useLocation();
  const { word } = useParams();

  const initialFilters = location.state?.filters || {};
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState(initialFilters.book || '');
  const [chapters, setChapters] = useState([]);
  const [selectedChapter, setSelectedChapter] = useState(initialFilters.chapter || '');
  const [verses, setVerses] = useState([]);
  const [selectedVerse, setSelectedVerse] = useState(initialFilters.verse || '');
  const [appearances, setAppearances] = useState([]);
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

  const fetchAppearances = async (filters, pageIndex) => {
    const response = await getWordAppearances(word, filters, pageIndex);
    setAppearances(response.wordAppearances);
    setTotalPages(Math.ceil(response.total / pageSize));
  };

  useEffect(() => {
    fetchAppearances(initialFilters, 0);
  }, [initialFilters]);

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

    fetchAppearances({
      book: bookName,
      chapter: '',
      verse: '',
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

    fetchAppearances({
      book: selectedBook,
      chapter: chapterNum,
      verse: '',
    }, 0);
  };

  const handleVerseChange = (e) => {
    const verseNum = e.target.value;
    setSelectedVerse(verseNum);
    setPageIndex(0);

    fetchAppearances({
      book: selectedBook,
      chapter: selectedChapter,
      verse: verseNum,
    }, 0);
  };

  const handleReset = async () => {
    setSelectedBook('');
    setSelectedChapter('');
    setSelectedVerse('');
    setChapters([]);
    setVerses([]);
    setPageIndex(0);

    fetchAppearances({}, 0);
  };

  const handlePageChange = (newPageIndex) => {
    setPageIndex(newPageIndex);
    fetchAppearances({
      book: selectedBook,
      chapter: selectedChapter,
      verse: selectedVerse,
    }, newPageIndex);
  };

  return (
    <div>
      <h1>
        <spawn style={{color: 'blue', textTransform: 'uppercase'}}
        >{word}</spawn> appearances
      </h1>
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
        <button onClick={handleReset}>Reset Filters</button>
      </div>
      <div className="appearances-list">
        <table>
          <thead>
            <tr>
              <th>Book</th>
              <th>Chapter</th>
              <th>Verse</th>
            </tr>
          </thead>
          <tbody>
            {appearances.map((appearance, index) => (
              <tr key={index} className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                <td>{appearance.book}</td>
                <td>{appearance.chapter}</td>
                <td>{appearance.verse}</td>
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


export default WordAppearances;
