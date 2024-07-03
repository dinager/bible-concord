import os
from typing import Tuple

from werkzeug.datastructures import FileStorage

from consts import ROOT_PATH
from server.db_model.db_functions import insert_book_data_to_tables
from server.db_model.model.book import BookModel
from server.logic.bible_book_parser import parse_text_to_book_chapters
from server.logic.structures import BibleBook

EXT_DISK_PATH = os.path.join(ROOT_PATH, "ext_disk")


def add_book(book_name: str, text_file: FileStorage, division: str) -> Tuple[bool, str]:
    # todo: validate text file
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
