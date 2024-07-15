"""
This file contains mock responses for the API endpoints.
Once endpoint is implemented remove un relevant methods
"""
import json
import os
from typing import Tuple

from consts import ROOT_PATH

MOCK_WORDS_IN_GROUPS = {
    "prophets": ["moses", "isaiah", "ezekiel"],
    "animals": ["lion", "sheep", "camel"],
}


def get_all_words_paginate_mock(page_index: int, page_size: int) -> Tuple[list[str], int]:
    with open(os.path.join(os.path.dirname(__file__), "unique_words.json"), "r") as json_file:
        all_words = json.load(json_file)
    return all_words[page_index * page_size : (page_index + 1) * page_size], len(all_words)


def get_filtered_words_paginate_mock(filters: dict, page_index: int, page_size: int) -> Tuple[list[str], int]:
    with open(os.path.join(os.path.dirname(__file__), "unique_words.json"), "r") as json_file:
        all_words = json.load(json_file)
    word_prefix = filters["wordStartsWith"].lower() if filters.get("wordStartsWith") else None
    book = filters["book"].lower() if filters.get("book") else None
    if not word_prefix:
        filtered_words = all_words
        if book == "genesis":
            filtered_words = [word for word in all_words if word.startswith("o")]
        elif book == "exodus":
            filtered_words = [word for word in all_words if word.startswith("m")]
    else:
        filtered_words = [word for word in all_words if word.startswith(word_prefix)]
    return filtered_words[page_index * page_size : (page_index + 1) * page_size], len(filtered_words)


def get_word_appearances_paginate_mock(
    word: str, filters: dict, page_index: int, page_size: int
) -> Tuple[list[dict], int]:
    words_num = (
        35 + len(word)
        if not filters.get("book")
        else 20
        if not filters.get("chapter")
        else 10
        if not filters.get("verse")
        else 2
    )
    word_appearances = [
        {
            "book": filters["book"].lower() if filters.get("book") else "genesis",
            "chapter": filters["chapter"] if filters.get("chapter") else len(word) + i,
            "verse": filters["verse"] if filters.get("verse") else len(word) + i + 2,
            "indexInVerse": filters["indexInVerse"] if filters.get("indexInVerse") else len(word) + i + 1,
        }
        for i in range(words_num)
    ]
    return word_appearances[page_index * page_size : (page_index + 1) * page_size], len(word_appearances)


def get_word_text_context_mock(word: str, book: str, chapter: int, verse: int, index: int) -> str | None:
    with open(os.path.join(ROOT_PATH, "tests", "resources", f"{book.lower()}.txt"), "r") as file:
        lines = file.readlines()
    # Prepare a list to store the results
    mock_prefix = f"Mock text for word: '{word}' in {book} {chapter}:{verse} index {index}\n"
    # Iterate through the lines
    for i, line in enumerate(lines):
        if word in line:
            # Get the context (two lines before and after)
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            context = lines[start:end]
            return mock_prefix + "".join(context)

    return None
