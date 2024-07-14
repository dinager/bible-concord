import traceback
from typing import Tuple

from server.db_model.model.chapter import ChapterModel


def get_num_verses_in_chapter(book_name: str, chpater_number: int) -> Tuple[bool, str]:
    try:
        book_name = book_name.lower()
        num_verses = ChapterModel.get_num_verses(book_name, chpater_number)
        if num_verses == -1:
            return False, f"Book {book_name} was not found"
        if num_verses == -2:
            return False, f"chapter number {chpater_number} was not found"
        return True, num_verses

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
