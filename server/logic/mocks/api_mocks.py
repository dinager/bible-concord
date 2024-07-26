"""
This file contains mock responses for the API endpoints.
Once endpoint is implemented remove un relevant methods
"""
MOCK_WORDS_IN_GROUPS = {
    "prophets": ["moses", "isaiah", "ezekiel"],
    "animals": ["lion", "sheep", "camel"],
}

MOCK_CONTEXT_IN_PHRASES = {
    "phrase1": {
        "book_title": "genesis",
        "chapter_num": 23,
        "verse_num": 10,
        "word_position": 8,
        "line_num_in_file": 23,
    },
    "phrase2": {
        "book_title": "exudos",
        "chapter_num": 13,
        "verse_num": 5,
        "word_position": 18,
        "line_num_in_file": 223,
    },
    "phrase3": {
        "book_title": "genesis",
        "chapter_num": 3,
        "verse_num": 2,
        "word_position": 12,
        "line_num_in_file": 213,
    },
    "this is a great phrase": {
        "book_title": "genesis",
        "chapter_num": 3,
        "verse_num": 2,
        "word_position": 12,
        "line_num_in_file": 213,
    },
}
