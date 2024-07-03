import React, {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import {filterWords} from '../services/api';
import Pagination from './Pagination';
import WordFilters from './WordFilters';

const WordList = () => {
    const navigate = useNavigate();

    const [words, setWords] = useState([]);
    const [pageIndex, setPageIndex] = useState(0);
    const [totalPages, setTotalPages] = useState(0);
    const [filters, setFilters] = useState(
        {book: '', chapter: '', verse: '', wordStartsWith: '', indexInVerse: ''}
    );
    const [keepFilters, setKeepFilters] = useState(true);

    const pageSize = 14;

    const fetchWords = async (filters, pageIndex) => {
        const filteredWords = await filterWords(filters, pageIndex, pageSize);
        setWords(filteredWords.words);
        setTotalPages(Math.ceil(filteredWords.total / pageSize));
    };

    useEffect(() => {
        fetchWords(filters, 0);
    }, [filters]);

    const handlePageChange = (newPageIndex) => {
        setPageIndex(newPageIndex);
        fetchWords(filters, newPageIndex);
    };

    const handleViewAppearances = (word) => {
        let {wordStartsWith, ...filtersWithoutWord} = filters;
        const currentFilters = keepFilters ? filtersWithoutWord : {};
        navigate(`/word/${word}/appearances`, {state: {filters: currentFilters}});
    };

    const handleKeepFiltersChange = (e) => {
        setKeepFilters(e.target.checked);
    };

    const handleFiltersChanged = (newFilters) => {
        setFilters(newFilters);
        setPageIndex(0);
    };

    return (
        <div>
            <h1>Search Words</h1>
            <WordFilters onFilterChange={handleFiltersChanged} initialFilters={{}} filterByWord={true}/>
            <div className="word-list">
                <table>
                    <tbody>
                    {words.map((word, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                            <td>{word}</td>
                            <td>
                                <button onClick={() => handleViewAppearances(word)}>Appearances</button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
                <div
                    style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '20px'}}>
                    <div>
                        <input
                            type="checkbox"
                            id="keepFilters"
                            checked={keepFilters}
                            onChange={handleKeepFiltersChange}
                        />
                        <label htmlFor="keepFilters">Keep current filters when viewing appearances</label>
                    </div>
                    <Pagination
                        currentPage={pageIndex}
                        totalPages={totalPages}
                        onPageChange={handlePageChange}
                    />
                </div>
            </div>
        </div>
    );
};

export default WordList;
