import React, {useState, useEffect} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {filterWords} from '../../services/api';
import Pagination from './Pagination';
import WordFilters from './WordFilters';
import {FaArrowLeft} from "react-icons/fa";

const WordList = () => {
    const navigate = useNavigate();

    const {groupName} = useParams();
    const [words, setWords] = useState([]);
    const [pageIndex, setPageIndex] = useState(0);
    const [totalPages, setTotalPages] = useState(0);
    const [filters, setFilters] = useState({
        book: '',
        chapter: '',
        verse: '',
        wordStartsWith: '',
        indexInVerse: '',
    });
    const [keepFilters, setKeepFilters] = useState(true);
    const [isFreeSearch, setIsFreeSearch] = useState(false);

    const pageSize = 14;

    const fetchWords = async (filters, pageIndex) => {
        const userFilters = groupName ?
            {...filters, groupName: groupName} :
            filters
        const filteredWords = await filterWords(userFilters, pageIndex, pageSize);
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
        // todo: only if groupName
        navigate(`/word/${word}/appearances`, {
            state: {filters: {...currentFilters, groupName: groupName}, isFreeSearch: isFreeSearch}
        });
    };

    const handleKeepFiltersChange = (e) => {
        setKeepFilters(e.target.checked);
    };

    const handleFiltersChanged = (newFilters) => {
        setFilters(newFilters);
        setPageIndex(0);
    };

    const handleFreeSearchChange = (newIsFreeSearch) => {
        setIsFreeSearch(newIsFreeSearch);
    };

    return (
        <div>
            <div className="screen-header-container">
                {groupName && <FaArrowLeft onClick={() => navigate(-1)} className="return-arrow"/>}
                <h1>Search Words
                    <span style={{textTransform: 'uppercase', color: 'blue', fontStyle: 'italic'}}> {groupName} </span>
                </h1>
            </div>
            <WordFilters
                onFilterChange={handleFiltersChanged}
                initialFilters={{}}
                filterByWord={true}
                freeSearch={isFreeSearch}
                onFreeSearchChange={handleFreeSearchChange}
            />
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
