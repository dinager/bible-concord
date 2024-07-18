import json
import os
import traceback
from typing import Tuple

from werkzeug.datastructures import FileStorage

from consts import EXT_DISK_PATH
from server.db_model.db_functions import insert_book_data_to_tables
from server.db_model.model.book import BookModel
from server.logic.bible_book_parser import parse_text_to_book_chapters
from server.logic.structures import BibleBook


def add_book(book_name: str, text_file: FileStorage, division: str) -> Tuple[bool, str]:
    try:
        book_name = book_name.lower()
        division = division.lower()
        if BookModel.does_book_exist(book_name):
            return False, f"book {book_name} already exists"

        book_text = text_file.read().decode("utf-8")
        book_chapters = parse_text_to_book_chapters(book_text)
        file_path = os.path.join(EXT_DISK_PATH, book_name + ".txt")
        bible_book = BibleBook(
            name=book_name,
            division=division,
            num_chapters=len(book_chapters),
            chapters=book_chapters,
            raw_text_path=file_path,
            file_size=len(book_text),
        )
        insert_book_data_to_tables(bible_book)
        # Save the raw text to 'file_path'
        with open(file_path, "w") as file:
            file.write(book_text)

        return True, f"received book with {bible_book.num_chapters} chapters"
    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_books() -> Tuple[bool, str]:
    # the return string is a JSON string
    try:
        books = BookModel.get_all_books()
        books_data = [
            {
                "name": book.title,
                "division": book.division,
                "insertTime": book.insert_date.strftime("%Y-%d-%m %H:%M"),
            }
            for book in books
        ]

        return True, json.dumps({"books": books_data})

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_book_content(book_name: str) -> Tuple[bool, str]:
    try:
        book_file_path = BookModel.get_book_file_path(book_name)
        with open(book_file_path, "r") as file:
            return True, file.read()
    except FileNotFoundError:
        return False, "The specified book was not found."
    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_book_names() -> Tuple[bool, list[str] | str]:
    # the return string is a JSON string
    try:
        book_names = BookModel.get_all_book_names()
        return True, book_names

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


def get_num_chapters_in_book(book_name: str) -> Tuple[bool, str]:
    try:
        book_name = book_name.lower()
        book_data = BookModel.get_book(book_name)
        if book_data is None:
            return False, f"book {book_name} doesn't exists"
        return True, book_data.num_chapters

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
