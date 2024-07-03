import React, {useState, useEffect, useCallback} from 'react';
import {getBooksNames, getNumChaptersInBook, getNumVersesInChapter, getNumWordsInVerse} from '../services/api';

const WordFilters = ({onFilterChange, initialFilters, filterByWord, freeSearch, onFreeSearchChange}) => {
    const [books, setBooks] = useState([]);
    const [selectedBook, setSelectedBook] = useState(initialFilters.book || '');
    const [chapters, setChapters] = useState([]);
    const [selectedChapter, setSelectedChapter] = useState(initialFilters.chapter || '');
    const [verses, setVerses] = useState([]);
    const [selectedVerse, setSelectedVerse] = useState(initialFilters.verse || '');
    const [indexesInVerse, setIndexesInVerse] = useState([]);
    const [selectedIndexInVerse, setSelectedIndexInVerse] = useState(initialFilters.indexInVerse || '');
    const [wordStartsWith, setWord] = useState('');

    useEffect(() => {
        fetchBooks();
        if (initialFilters.book && !freeSearch) {
            fetchChapters(initialFilters.book);
            if (initialFilters.chapter) {
                fetchVerses(initialFilters.book, initialFilters.chapter);
                if (initialFilters.verse) {
                    fetchNumWordsInVerse(initialFilters.book, initialFilters.chapter, initialFilters.verse);
                }
            }
        }
    }, []);

    const fetchBooks = async () => {
        const books = await getBooksNames();
        setBooks(books);
    };

    const fetchChapters = async (bookName) => {
        const numChapters = await getNumChaptersInBook(bookName);
        setChapters(Array.from({length: numChapters}, (_, i) => i + 1));
    };

    const fetchVerses = async (bookName, chapterNum) => {
        const numVerses = await getNumVersesInChapter(bookName, chapterNum);
        setVerses(Array.from({length: numVerses}, (_, i) => i + 1));
    };

    const fetchNumWordsInVerse = async (bookName, chapterNum, verseNum) => {
        const numWords = await getNumWordsInVerse(bookName, chapterNum, verseNum);
        setIndexesInVerse(Array.from({length: numWords}, (_, i) => i + 1));
    };

    const handleBookChange = async (e) => {
        const bookName = e.target.value;
        setSelectedBook(bookName);
        if (!freeSearch) {
            setSelectedChapter('');
            setSelectedVerse('');
            setSelectedIndexInVerse('');
            setChapters([]);
            setVerses([]);
            setIndexesInVerse([]);

            if (bookName) {
                await fetchChapters(bookName);
            }
        }

        onFilterChange({
            book: bookName,
            chapter: '',
            verse: '',
            indexInVerse: '',
            wordStartsWith: wordStartsWith
        });
    };

    const handleChapterChange = async (e) => {
        const chapterNum = e.target.value;
        setSelectedChapter(chapterNum);
        if (!freeSearch) {
            setSelectedVerse('');
            setSelectedIndexInVerse('');
            setVerses([]);
            setIndexesInVerse([]);
            if (chapterNum) {
                await fetchVerses(selectedBook, chapterNum);
            }
        }

        onFilterChange({
            book: selectedBook,
            chapter: chapterNum,
            verse: '',
            indexInVerse: '',
            wordStartsWith: wordStartsWith
        });
    };

    const handleVerseChange = async (e) => {
        const verseNum = e.target.value;
        setSelectedVerse(verseNum);
        if (!freeSearch) {
            setSelectedIndexInVerse('');
            setIndexesInVerse([]);

            if (verseNum) {
                await fetchNumWordsInVerse(selectedBook, selectedChapter, verseNum);
            }
        }

        onFilterChange({
            book: selectedBook,
            chapter: selectedChapter,
            verse: verseNum,
            indexInVerse: '',
            wordStartsWith: wordStartsWith
        });
    };

    const handleIndexInVerseChange = (e) => {
        const indexVal = e.target.value;
        setSelectedIndexInVerse(indexVal);

        onFilterChange({
            book: selectedBook,
            chapter: selectedChapter,
            verse: selectedVerse,
            indexInVerse: indexVal,
            wordStartsWith: wordStartsWith
        });
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
            indexInVerse: selectedIndexInVerse,
            wordStartsWith: wordValue,
        });
    };

    const handleReset = () => {
        setSelectedBook('');
        setSelectedChapter('');
        setSelectedVerse('');
        setWord('');
        setSelectedIndexInVerse('');
        setChapters([]);
        setVerses([]);
        setIndexesInVerse([]);

        onFilterChange({
            book: '',
            chapter: '',
            verse: '',
            indexInVerse: '',
            wordStartsWith: '',
        });
    };

    const handleFreeSearchChange = (e) => {
        onFreeSearchChange(e.target.checked);
        handleReset();
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
            {freeSearch ? (
                <input
                    className="number-input"
                    type="number"
                    value={selectedChapter}
                    onChange={handleChapterChange}
                    min="1"
                />
            ) : (
                <select value={selectedChapter} onChange={handleChapterChange} disabled={!selectedBook}>
                    <option value="">All</option>
                    {chapters.map((chapter) => (
                        <option key={chapter} value={chapter}>{chapter}</option>
                    ))}
                </select>
            )}
            <label>Verse:</label>
            {freeSearch ? (
                <input
                    className="number-input"
                    type="number"
                    value={selectedVerse}
                    onChange={handleVerseChange}
                    min="1"
                />
            ) : (
                <select value={selectedVerse} onChange={handleVerseChange} disabled={!selectedChapter}>
                    <option value="">All</option>
                    {verses.map((verse) => (
                        <option key={verse} value={verse}>{verse}</option>
                    ))}
                </select>
            )}
            <label>Position:</label>
            {freeSearch ? (
                <input
                    className="number-input"
                    type="number"
                    value={selectedIndexInVerse}
                    onChange={handleIndexInVerseChange}
                    min="1"
                />
            ) : (
                <select value={selectedIndexInVerse} onChange={handleIndexInVerseChange} disabled={!selectedVerse}>
                    <option value="">All</option>
                    {indexesInVerse.map((ind) => (
                        <option key={ind} value={ind}>{ind}</option>
                    ))}
                </select>
            )}
            {filterByWord && (<label>Word:</label>)}
            {filterByWord && (
                <input style={{width: '80px'}} type="text" value={wordStartsWith} onChange={handleWordChange}/>)}
            <button onClick={handleReset}>Reset</button>
            <input
                type="checkbox"
                id="isFreeSearch"
                checked={freeSearch}
                onChange={handleFreeSearchChange}
            />
            <label htmlFor="isFreeSearch">Free Search</label>
        </div>
    );
};

export default WordFilters;
