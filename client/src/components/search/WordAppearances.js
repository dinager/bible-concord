import React, {useState, useEffect} from 'react';
import {useLocation, useParams, useNavigate} from 'react-router-dom';
import {getWordAppearances, getTextContext} from '../../services/api';
import Pagination from './Pagination';
import WordFilters from './WordFilters';
import {FaArrowLeft} from 'react-icons/fa';
import Modal from 'react-modal';

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
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState({book: '', title: '', content: ''});

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

    const handleViewTextContext = async (appearance) => {
        const contextText = await getTextContext(
            word,
            appearance.book,
            appearance.chapter,
            appearance.verse,
            appearance.indexInVerse,
            appearance.lineNumInFile,
        );
        const highlightedText = highlightWord(contextText, word);

        setModalContent({
            book: appearance.book,
            title: ` ${appearance.chapter}:${appearance.verse} (position ${appearance.indexInVerse})`,
            content: highlightedText
        });
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setModalContent({book: '', title: '', content: ''});
    };

    const highlightWord = (text, word) => {
        const regex = new RegExp(`(\\b${word}\\b)`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    };

    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={() => navigate('/search-words')} className="return-arrow"/>
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
            <Modal
                isOpen={isModalOpen}
                onRequestClose={closeModal}
                contentLabel="Text Context"
                ariaHideApp={false}
                style={{left: "300px", top: "100px"}}
            >
                <div>
                    <h1>
                        <span style={{textTransform: 'uppercase', color: 'blue'}}>{word} </span>
                        <span style={{fontStyle: 'italic'}}>
                            <span style={{textTransform: 'capitalize'}}>{modalContent.book}
                        </span> {modalContent.title}
                    </span>

                    </h1>
                    <div className="book-content">
                        <pre dangerouslySetInnerHTML={{__html: modalContent.content}}></pre>
                    </div>
                    <button style={{marginTop: '20px'}} onClick={closeModal}>Close</button>
                </div>

            </Modal>
        </div>
    );
};

export default WordAppearances;
