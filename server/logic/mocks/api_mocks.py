"""
This file contains mock responses for the API endpoints.
Once endpoint is implemented remove un relevant methods
"""
import json
import os
from typing import Tuple

ROOT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..")

MOCK_BOOKS = [
    {
        "name": "Genesis",
        "division": "Torah",
        "insertTime": "2024-30-06 10:55",
    },
    {
        "name": "Exodus",
        "division": "Neviim",
        "insertTime": "2024-01-07 11:01",
    },
]

MOCK_BOOKS_NAMES = ["genesis", "exodus"]


def get_book_content_mock(book_name: str) -> str | None:
    test_resources_path = os.path.join(ROOT_PATH, "tests", "resources")
    book_name = book_name.lower()
    if book_name not in ["genesis", "exodus"]:
        return None
    with open(os.path.join(test_resources_path, f"{book_name}.txt"), "r") as file:
        return file.read()


def get_num_chapters_in_book_mock(book_name: str) -> int | None:
    book_name = book_name.lower()
    match book_name:
        case "genesis":
            return 20
        case "exodus":
            return 30
    return None


def get_num_verses_in_chapter_mock(book_name: str, num_chapter: int) -> int | None:
    book_name = book_name.lower()
    match book_name:
        case "genesis":
            return num_chapter + 2
        case "exodus":
            return num_chapter + 3
    return None


def get_num_words_in_verse_mock(book_name: str, num_chapter: int, verse_num: int) -> int | None:
    book_name = book_name.lower()
    if book_name not in ["genesis", "exodus"]:
        return None
    return verse_num + 1


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
