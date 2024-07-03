import React, {useState, useEffect} from 'react';
import {useLocation, useParams, useNavigate} from 'react-router-dom';
import {getWordAppearances} from '../../services/api';
import Pagination from './Pagination';
import WordFilters from './WordFilters';
import {FaArrowLeft} from 'react-icons/fa';

const WordAppearances = () => {
    const location = useLocation();
    const {word} = useParams();
    const navigate = useNavigate();

    const initialFilters = location.state?.filters || {};
    const initialFreeSearch = location.state?.isFreeSearch || false;
    const [appearances, setAppearances] = useState([]);
    const [pageIndex, setPageIndex] = useState(0);
    const [totalPages, setTotalPages] = useState(0);
    const [filters, setFilters] = useState(initialFilters);
    const [totalAppearances, setTotalAppearances] = useState(0);
    const [isFreeSearch, setIsFreeSearch] = useState(initialFreeSearch);

    const pageSize = 14;

    const fetchAppearances = async (filters, pageIndex) => {
        const response = await getWordAppearances(word, filters, pageIndex, pageSize);
        setAppearances(response.wordAppearances);
        setTotalPages(Math.ceil(response.total / pageSize));
        setTotalAppearances(response.total);
    };

    useEffect(() => {
        fetchAppearances(filters, 0);
    }, [filters]);

    const handlePageChange = (newPageIndex) => {
        setPageIndex(newPageIndex);
        fetchAppearances(filters, newPageIndex);
    };

    const handleFiltersChanged = (newFilters) => {
        setFilters(newFilters);
        setPageIndex(0);
    };

    const handleFreeSearchChange = (newIsFreeSearch) => {
        setIsFreeSearch(newIsFreeSearch);
    };

    const handleBackClick = () => {
        navigate('/search-words');
    };

    const handleViewTextContext = (appearance) => {
        navigate(`/text_context/${word}/book/${appearance.book}/chapter/${appearance.chapter}/verse/${appearance.verse}/index/${appearance.indexInVerse}`, {
            state: {filters, isFreeSearch}
        });
    };

    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={handleBackClick} className="return-arrow"/>
                <h1>
                    Appearances
                    <span style={{textTransform: 'uppercase', color: 'blue', fontStyle: 'italic'}}> {word} </span>
                </h1>
                <span className="total-appearances">Total Appearances: {totalAppearances}</span>
            </div>
            <WordFilters
                onFilterChange={handleFiltersChanged}
                initialFilters={filters}
                filterByWord={false}
                freeSearch={isFreeSearch}
                onFreeSearchChange={handleFreeSearchChange}
            />
            <div className="word-list">
                <table>
                    <thead>
                    <tr>
                        <th>Book</th>
                        <th>Chapter</th>
                        <th>Verse</th>
                        <th>Position In Verse</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    {appearances.map((appearance, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                            <td>{appearance.book}</td>
                            <td>{appearance.chapter}</td>
                            <td>{appearance.verse}</td>
                            <td>{appearance.indexInVerse}</td>
                            <td>
                                <button onClick={() => handleViewTextContext(appearance)}>View Text Context</button>
                            </td>
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
