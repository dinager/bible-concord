"""
This file contains mock responses for the API endpoints.
Once endpoint is implemented remove un relevant methods
"""
MOCK_WORDS_IN_GROUPS = {
    "prophets": ["moses", "isaiah", "ezekiel"],
    "animals": ["lion", "sheep", "camel"],
}

MOCK_CONTEXT_IN_PHRASES = {
    "This is the first phrase": {"book_title": "genesis", "chapter_num": 23, "verse_num": 10},
    "This is the second phrase": {"book_title": "exudos", "chapter_num": 13, "verse_num": 5},
}
