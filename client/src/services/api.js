import axios from 'axios';

const API_BASE_URL = 'http://localhost:4200/api';

export const getBooks = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/books`);
    return response.data.books;
  } catch (error) {
    console.error('Error fetching books:', error);
    throw error;
  }
};

export const getBookContent = async (bookName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/book_content/${bookName}`);
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


export const getBooksNames = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/book_names`);
    return response.data;
  } catch (error) {
    console.error('Error fetching books:', error);
    throw error;
  }
};

export const getNumChaptersInBook = async (bookName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/book/${bookName}/num_chapters/`);
    return parseInt(response.data, 10);
  } catch (error) {
    console.error(`Error fetching number of chapters for ${bookName}:`, error);
    throw error;
  }
};

export const getNumVersesInChapter = async (bookName, chapterNum) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/book/${bookName}/chapter/${chapterNum}/num_verses`);
    return parseInt(response.data, 10);
  } catch (error) {
    console.error(`Error fetching number of verses for ${bookName} chapter ${chapterNum}:`, error);
    throw error;
  }
};

export const getNumWordsInVerse = async (bookName, chapterNum, verseNum) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/book/${bookName}/chapter/${chapterNum}/verse/${verseNum}/num_words`);
    return parseInt(response.data, 10);
  } catch (error) {
    console.error(`Error fetching number of words for ${bookName} chapter ${chapterNum} verse ${verseNum}:`, error);
    throw error;
  }
};

export const filterWords = async (filters, pageIndex = 0, pageSize= 14) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/words/`, {
      filters,
      pageIndex,
      pageSize,
    });
    return response.data;
  } catch (error) {
    console.error('Error filtering words:', error);
    throw error;
  }
};

export const getWordAppearances = async (word, filters, pageIndex, pageSize = 15) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/word/${word}`, {
      filters,
      pageIndex,
      pageSize,
    });
    return response.data;
  } catch (error) {
    console.error('Error filtering words:', error);
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

