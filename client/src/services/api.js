import axios from 'axios';

const API_BASE_URL = 'http://localhost:4200/api';

export const getBooks = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/get_books`);
    return response.data.books;
  } catch (error) {
    console.error('Error fetching books:', error);
    throw error;
  }
};

export const getBookContent = async (bookName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/get_book_content/${bookName}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching book content:', error);
    throw error;
  }
};

export const addBook = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/add_book`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error adding book:', error);
    throw error;
  }
};

export const parseErrorResponse = (error) => {
    if (error.response?.data) {
        try {
        return JSON.stringify(error.response.data);
        } catch (jsonError) {
        return error.response.data.toString();
        }
    }
    return error.message;
}
