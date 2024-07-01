import React, {useState, useEffect, useCallback} from 'react';
import {getBooksNames, getNumChaptersInBook, getNumVersesInChapter} from '../services/api';

const WordFilters = ({onFilterChange, initialFilters, filterByWord}) => {
    const [books, setBooks] = useState([]);
    const [selectedBook, setSelectedBook] = useState(initialFilters.book || '');
    const [chapters, setChapters] = useState([]);
    const [selectedChapter, setSelectedChapter] = useState(initialFilters.chapter || '');
    const [verses, setVerses] = useState([]);
    const [selectedVerse, setSelectedVerse] = useState(initialFilters.verse || '');
    const [word, setWord] = useState('');

    useEffect(() => {
        const fetchBooks = async () => {
            const books = await getBooksNames();
            setBooks(books);
        };
        fetchBooks();
    }, []);

    const fetchChapters = async (bookName) => {
        const numChapters = await getNumChaptersInBook(bookName);
        setChapters(Array.from({length: numChapters}, (_, i) => i + 1));
    };

    const fetchVerses = async (bookName, chapterNum) => {
        const numVerses = await getNumVersesInChapter(bookName, chapterNum);
        setVerses(Array.from({length: numVerses}, (_, i) => i + 1));
    };

    //     todo: check usage.. move to other?
    // useEffect(() => {
    //     console.log('useEffect initialFilters:', initialFilters)
    //     if (initialFilters.book) {
    //         fetchChapters(initialFilters.book);
    //         if (initialFilters.chapter) {
    //             fetchVerses(initialFilters.book, initialFilters.chapter);
    //         }
    //     }
    // }, [initialFilters]);

    const handleBookChange = async (e) => {
        const bookName = e.target.value;
        setSelectedBook(bookName);
        setSelectedChapter('');
        setSelectedVerse('');
        setChapters([]);
        setVerses([]);

        if (bookName) {
            await fetchChapters(bookName);
        }

        onFilterChange({book: bookName, chapter: '', verse: '', wordStartsWith: word});
    };

    const handleChapterChange = async (e) => {
        const chapterNum = e.target.value;
        setSelectedChapter(chapterNum);
        setSelectedVerse('');
        setVerses([]);

        if (chapterNum) {
            await fetchVerses(selectedBook, chapterNum);
        }

        onFilterChange({book: selectedBook, chapter: chapterNum, verse: '', wordStartsWith: word});
    };

    const handleVerseChange = (e) => {
        const verseNum = e.target.value;
        setSelectedVerse(verseNum);

        onFilterChange({book: selectedBook, chapter: selectedChapter, verse: verseNum, wordStartsWith: word});
    };

    const debounce = (func, wait) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    };

    const debouncedOnFilterChange = useCallback(
        debounce((filters) => {
            onFilterChange(filters);
        }, 300),
        []
    );

    const handleWordChange = (e) => {
        const wordValue = e.target.value;
        setWord(wordValue);

        debouncedOnFilterChange({
            book: selectedBook,
            chapter: selectedChapter,
            verse: selectedVerse,
            wordStartsWith: wordValue,
        });
    };

    const handleReset = () => {
        setSelectedBook('');
        setSelectedChapter('');
        setSelectedVerse('');
        setWord('');
        setChapters([]);
        setVerses([]);

        onFilterChange({book: '', chapter: '', verse: '', wordStartsWith: ''});
    };

    return (
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
            {filterByWord && (<label>Word:</label>)}
            {filterByWord && (<input type="text" value={word} onChange={handleWordChange}/>)}
            <button onClick={handleReset}>Reset Filters</button>
        </div>
    );
};

export default WordFilters;
