"""
This file contains mock responses for the API endpoints.
Once endpoint is implemented remove un relevant methods
"""
import os

ROOT_PATH = os.path.join(os.path.dirname(__file__), "..", "..")

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
