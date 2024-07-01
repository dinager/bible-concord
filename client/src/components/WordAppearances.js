import React, {useState, useEffect} from 'react';
import {useLocation, useParams} from 'react-router-dom';
import {getWordAppearances} from '../services/api';
import Pagination from "./Pagination";
import WordFilters from "./WordFilters";

const WordAppearances = () => {
    const location = useLocation();
    const {word} = useParams();

    const initialFilters = location.state?.filters || {};
    const [appearances, setAppearances] = useState([]);
    const [pageIndex, setPageIndex] = useState(0);
    const [totalPages, setTotalPages] = useState(0);
    const [filters, setFilters] = useState(initialFilters);

    const pageSize = 15;

    const fetchAppearances = async (filters, pageIndex) => {
        const response = await getWordAppearances(word, filters, pageIndex, pageSize);
        setAppearances(response.wordAppearances);
        setTotalPages(Math.ceil(response.total / pageSize));
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
    }
    return (
        <div>
            <h1 style={{color: 'blue', textTransform: 'uppercase'}}>{word}</h1>
            <WordFilters onFilterChange={handleFiltersChanged} initialFilters={filters} filterByWord={false}/>
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
