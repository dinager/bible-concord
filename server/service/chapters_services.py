import traceback
from typing import Tuple

from server.db_model.model.book import BookModel
from server.db_model.model.chapter import ChapterModel


def get_num_verses_in_chapter(book_name: str, chapter_number: int) -> Tuple[bool, str | int]:
    try:
        book_id = BookModel.get_book_id(book_name.lower())
        if book_id is None:
            return False, f"Book {book_name} was not found"
        num_verses = ChapterModel.get_num_verses(book_id, chapter_number)
        if num_verses == -1:
            return False, f"Book {book_name} was not found"
        if num_verses == -2:
            return False, f"chapter number {chapter_number} was not found"
        return True, num_verses

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
