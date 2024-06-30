import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const AddBook = () => {
  const [file, setFile] = useState(null);
  const [bookName, setBookName] = useState('');
  const [division, setDivision] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'error' or 'success'

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    validateFile(selectedFile);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    validateFile(droppedFile);
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

  const validateFile = (file) => {
    if (file.type === 'text/plain') {
      setFile(file);
      setMessage('');
    } else {
      setFile(null);
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

    try {
      const response = await axios.post('http://localhost:4200/api/add_book', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage(`Book ${bookName} uploaded successfully!`);
      setMessageType('success');
      setBookName('');
      setFile('');
      setDivision('');
    } catch (error) {
      if (error.response?.data) {
        try {
          setMessage(JSON.stringify(error.response.data));
        } catch (jsonError) {
          setMessage(error.response.data.toString());
        }
      } else {
        setMessage( 'Error uploading book. '+ error.message);
      }
      setMessageType('error');
    }
  };

  return (
    <div>
      <h1>Add Book</h1>
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
        <button type="submit">Upload</button>
      </form>
      {message && <p className={`message ${messageType}`}>{message}</p>}
      <Link to="/" className="return-link">Return to Home</Link>
    </div>
  );
};

export default AddBook;
