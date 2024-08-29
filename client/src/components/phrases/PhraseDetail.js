import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {getPhraseReference, getTextContext, parseErrorResponse} from '../../services/api';
import { FaArrowLeft } from 'react-icons/fa';
import Modal from "react-modal";

const PhraseDetail = () => {
    const navigate = useNavigate();

    const { phraseText } = useParams();
    const [context, setContext] = useState([]);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState('');
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState({book: '', title: '', content: ''});

    useEffect(() => {
        const fetchContext = async () => {
            try {
                const response = await getPhraseReference(phraseText);
                if (response) {
                    setContext(response);
                } else {
                    setContext([]);
                }
                setMessage('');
                setMessageType('');
            } catch (error) {
                setMessage(`Failed to fetch context for phrase "${phraseText}". ${parseErrorResponse(error)}`);
                setMessageType('error');
            }
        };

        fetchContext();
    }, [phraseText]);

    const highlightWord = (text, phrase) => {
        const regex = new RegExp(`(\\b${phrase}\\b)`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    };

    const handleViewContext = async (ref) => {
        const contextText = await getTextContext(
            ref.title,
            ref.chapter_num,
            ref.verse_num,
        );
        const highlightedText = highlightWord(contextText, phraseText);

        setModalContent({
            book: ref.title,
            title: ` ${ref.chapter_num}:${ref.verse_num} (position ${ref.word_position})`,
            content: highlightedText
        });
        setIsModalOpen(true);

    };

    const closeModal = () => {
        setIsModalOpen(false);
        setModalContent({book: '', title: '', content: ''});
    };


    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={() => navigate('/phrases')} className="return-arrow" />
                <h1>Context of phrase:
                    <span style={{textTransform: 'uppercase', color: 'blue', fontStyle: 'italic'}}> {phraseText} </span>
                    ({context.length})
                </h1>
            </div>
            {message && <p className={`n-message ${messageType}`}>{message}</p>}
             <div style={{maxHeight: '750px', overflowY: 'auto', border: '1px solid #ccc'}}>
                 <table style={{width: '100%', borderCollapse: 'collapse'}}>
                     <thead>
                     <tr style={{position: 'sticky', top: 0, backgroundColor: '#fff', zIndex: 1}}>
                         <th>Book Name</th>
                         <th>Chapter Number</th>
                         <th>Verse Number</th>
                         <th>Word Position</th>
                         <th></th>
                     </tr>
                     </thead>
                     <tbody>
                     {context.length > 0 ? (
                         context.map((ref, index) => (
                             <tr key={index}>
                                 <td>{ref.title}</td>
                                 <td>{ref.chapter_num}</td>
                                 <td>{ref.verse_num}</td>
                                 <td>{ref.word_position}</td>
                                 <td>
                                     <button type="button" onClick={() => handleViewContext(ref)}>
                                         View Context
                                     </button>
                                 </td>
                             </tr>
                         ))
                     ) : (
                         <tr>
                             <td colSpan="4">No context available</td>
                         </tr>
                     )}
                     </tbody>
                 </table>
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

export default PhraseDetail;
