import React, {useState, useEffect} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {addWordToGroup, filterWords, parseErrorResponse} from '../../services/api';
import Pagination from '../search/Pagination';
import WordFilters from '../search/WordFilters';
import {FaArrowLeft} from 'react-icons/fa';

const AddFromWordList = () => {
    const navigate = useNavigate();
    const {groupName} = useParams();
    const [words, setWords] = useState([]);
    const [pageIndex, setPageIndex] = useState(0);
    const [totalPages, setTotalPages] = useState(0);
    const [filters, setFilters] = useState(
        {book: '', chapter: '', verse: '', wordStartsWith: '', wordPosition: ''}
    );
    const [isFreeSearch, setIsFreeSearch] = useState(false);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'

    const pageSize = 13;

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

    const handleAddWord = async (word) => {
        try {
            await addWordToGroup(groupName, word);
            setMessage(`Word "${word}" added successfully to ${groupName}!`);
            setMessageType('success');
        } catch (error) {
            setMessage(`Failed to add word "${word}" to ${groupName}. ${parseErrorResponse(error)}`);
            setMessageType('error');
        }
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
                <FaArrowLeft onClick={() => navigate(`/groups/${groupName}/words`)} className="return-arrow"/>
                <h1>Add Word To
                    <span style={{textTransform: 'uppercase', color: 'blue', fontStyle: 'italic'}}> {groupName} </span>
                </h1>
            </div>
            {message && <p className={`n-message ${messageType}`}>{message}</p>}
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
                                <button onClick={() => handleAddWord(word)}>Add Word</button>
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

export default AddFromWordList;
