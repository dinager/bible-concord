import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const AddBook = () => {
  const [file, setFile] = useState(null);
  const [bookName, setBookName] = useState('');
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    setFile(droppedFile);
    setMessage('');
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleBookNameChange = (e) => {
    setBookName(e.target.value);
    setMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !bookName) {
      setMessage('Please select a file and enter a book name.');
      return;
    }

    const formData = new FormData();
    formData.append('textFile', file);
    formData.append('bookName', bookName);

    try {
      const response = await axios.post('http://localhost:4200/api/add_book', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      // todo: if response returned error, show
      setMessage('File uploaded successfully!');
    } catch (error) {
      setMessage('Error uploading file.');
    }
  };

  return (
    <div>
      <h1>Add Book</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="bookName">Book Name: </label>
          <input
              type="text"
              id="bookName"
              value={bookName}
              onChange={handleBookNameChange}
          />
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
      {message && <p className="message">{message}</p>}
      <Link to="/" className="return-link">Return to Home</Link>
    </div>
  );
};

export default AddBook;
