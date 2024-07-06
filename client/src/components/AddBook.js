import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {addBook, parseErrorResponse} from '../services/api';
import {FaArrowLeft} from 'react-icons/fa';

const AddBook = () => {
    const [file, setFile] = useState(null);
    const [fileContent, setFileContent] = useState('');
    const [bookName, setBookName] = useState('');
    const [division, setDivision] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'error' or 'success'
    const [isUploadSuccessful, setIsUploadSuccessful] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        validateAndReadFile(selectedFile);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const droppedFile = e.dataTransfer.files[0];
        validateAndReadFile(droppedFile);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const handleBookNameChange = (e) => {
        setBookName(e.target.value);
        setMessage('');
    };

    const handleDivisionChange = (e) => {
        setDivision(e.target.value);
        setMessage('');
    };

    const validateAndReadFile = (file) => {
        if (file.type === 'text/plain') {
            setFile(file);
            setMessage('');
            const reader = new FileReader();
            reader.onload = (e) => {
                setFileContent(e.target.result);
            };
            reader.readAsText(file);
        } else {
            setFile(null);
            setFileContent('');
            setMessage('Please upload a valid text file.');
            setMessageType('error');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file || !bookName || !division) {
            setMessage('Please select a file, enter a book name, and choose a division.');
            setMessageType('error');
            return;
        }

        const formData = new FormData();
        formData.append('textFile', file);
        formData.append('bookName', bookName);
        formData.append('division', division);

        setIsLoading(true);

        try {
            await addBook(formData);
            setMessage(`Book ${bookName} uploaded successfully!`);
            setMessageType('success');
            setIsUploadSuccessful(true);
        } catch (error) {
            setMessage('Error uploading book. ' + parseErrorResponse(error));
            setMessageType('error');
        } finally {
            setIsLoading(false);
        }
    };

    const handleReset = () => {
        setFile(null);
        setFileContent('');
        setBookName('');
        setDivision('');
        setMessage('');
        setMessageType('');
        setIsUploadSuccessful(false);
    };


    return (
        <div>
            <div className="screen-header-container">
                <FaArrowLeft onClick={() => navigate('/books')} className="return-arrow"/>
                <h1>Add Book</h1>
            </div>
            <form onSubmit={handleSubmit}>
                <div className="form-row">
                    <div>
                        <label htmlFor="bookName">Book Name: </label>
                        <input
                            type="text"
                            id="bookName"
                            value={bookName}
                            onChange={handleBookNameChange}
                        />
                    </div>
                    <div>
                        <label htmlFor="division">Division: </label>
                        <select id="division" value={division} onChange={handleDivisionChange} required>
                            <option value="">Select a division</option>
                            <option value="Torah">Torah</option>
                            <option value="Neviim">Neviim</option>
                            <option value="Ketuvim">Ketuvim</option>
                        </select>
                    </div>
                </div>
                <div
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    style={{
                        border: '2px dashed #ccc',
                        padding: '20px',
                        marginBottom: '20px',
                    }}
                >
                    {file ? (
                        <p>{file.name}</p>
                    ) : (
                        <p>Drag and drop a text file here, or click to select a file.</p>
                    )}
                    <input
                        type="file"
                        onChange={handleFileChange}
                        style={{display: 'none'}}
                        id="fileInput"
                    />
                </div>
                {fileContent && (
                    <div className="file-preview">
                        <pre>{fileContent}</pre>
                    </div>
                )}
                {!isUploadSuccessful ? (
                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Uploading...' : 'Upload'}
                    </button>
                ) : (
                    <button type="button" onClick={handleReset}>Upload Another Book</button>
                )}
            </form>
            {message && <p className={`message ${messageType}`}>{message}</p>}
        </div>
    );
};

export default AddBook;
