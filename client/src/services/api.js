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
        console.error('Error in getBooksNames:', error);
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

export const filterWords = async (filters, pageIndex = 0, pageSize = 14) => {
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

export const getTextContext = async (book, chapter, verse) => {
    try {
        const response = await axios.get(
            `${API_BASE_URL}/text_context/book/${book}/chapter/${chapter}/verse/${verse}`,
        );
        return await response.data;
    } catch (error) {
        console.error('Error get text_context:', error);
        throw error;
    }
};


export const getGroups = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/groups`);
        return response.data;
    } catch (error) {
        console.error('Error in getGroups:', error);
        throw error;
    }

};


export const getGroupWordAppearancesIndex = async (groupName) => {
    try {
        const response = await axios.get(
            `${API_BASE_URL}/group/${groupName}/word_appearances_index`
        );
        return response.data;
    } catch (error) {
        console.error('Error in getWordsInGroup:', error);
        throw error;
    }

};


export const addGroup = async (groupName) => {
    try {
        await axios.post(`${API_BASE_URL}/add_group`, {groupName});

    } catch (error) {
        console.error('Error in addGroup:', error);
        throw error;
    }
};

export const getWordsInGroup = async (groupName) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/group/${groupName}/words`);
        return response.data;
    } catch (error) {
        console.error('Error in getWordsInGroup:', error);
        throw error;
    }

};

export const addWordToGroup = async (groupName, word) => {
    try {
        await axios.post(`${API_BASE_URL}/groups/add_word`, {groupName, word});

    } catch (error) {
        console.error('Error in addWordToGroup:', error);
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
};

export const getPhrases = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/phrases`);
        return response.data;
    } catch (error) {
        console.error('Error in getPhrases:', error);
        throw error;
    }

};

export const addPhrase = async (phraseText) => {
    try {
        await axios.post(`${API_BASE_URL}/add_phrase`, {phraseText});

    } catch (error) {
        console.error('Error in addPhrase:', error);
        throw error;
    }
};

export const getPhraseReference = async (phraseText) => {
    try {
        const encodedPhraseText = encodeURIComponent(phraseText);
        const response = await axios.get(`${API_BASE_URL}/phrase/${encodedPhraseText}/reference`);
        return response.data;
    } catch (error) {
        console.error('Error fetching phrase context:', error);
        throw error;
    }
};

export const addPhraseFromText = async (book, phrase) => {
    try {
        await axios.post(`${API_BASE_URL}/add_phrase`, { phraseText: phrase });
    } catch (error) {
        console.error('Error in addPhraseFromText:', error);
        throw error;
    }
};

export const deleteBook = async (bookName) => {
    try {
        const response = await axios.delete(`${API_BASE_URL}/book-to-delete/${bookName}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting book:', error);
        throw error;
    }
};

export const deleteGroup = async (groupName) => {
    try {
        const response = await axios.delete(`${API_BASE_URL}/group-to-delete/${groupName}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting group:', error);
        throw error;
    }
};

export const deletePhrase = async (phraseText) => {
    try {
        const response = await axios.delete(`${API_BASE_URL}/phrase-to-delete/${phraseText}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting phrase:', error);
        throw error;
    }
};

export const getTotalStats = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/general_stats`);
        return response.data;
    } catch (error) {
        console.error('Error fetching totals:', error);
        throw error;
    }
};

export const getBookStats = async (bookName) => {
    try {
        const url = bookName 
            ? `${API_BASE_URL}/books/${encodeURIComponent(bookName)}/stats`
            : `${API_BASE_URL}/books/stats`; // No book name specified
        
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error('Error fetching book stats:', error);
        throw error;
    }
};