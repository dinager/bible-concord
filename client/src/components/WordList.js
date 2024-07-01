import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { filterWords } from '../services/api';
import Pagination from "./Pagination";
import WordFilters from "./WordFilters";

const WordList = () => {
  const [words, setWords] = useState([]);
  const [pageIndex, setPageIndex] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [filters, setFilters] = useState(
      { book: '', chapter: '', verse: '',  wordStartsWith: ''}
  );
  const navigate = useNavigate();

  const pageSize = 15;

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

  const handleViewAppearances = (word, keepFilters) => {
    let { wordStartsWith, ...filtersWithoutWord } = filters;
    const currentFilters = keepFilters ? filtersWithoutWord : {};
    navigate(`/word/${word}/appearances`, { state: { filters: currentFilters } });
  };

  const handleFiltersChanged = (newFilters) => {
    setFilters(newFilters);
    setPageIndex(0);
  }

  return (
    <div>
      <h1>Word List</h1>
      <WordFilters onFilterChange={handleFiltersChanged} initialFilters={filters} filterByWord={true}/>
      <div className="word-list">
        <table>
          <tbody>
            {words.map((word, index) => (
              <tr key={index} className={index % 2 === 0 ? 'even-row' : 'odd-row'}>
                <td>{word}</td>
                <td>
                  <button onClick={() => handleViewAppearances(word, false)}>Appearances</button>
                  <button onClick={() => handleViewAppearances(word, true)}>Appearances (Use Filters)</button>
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

export default WordList;
