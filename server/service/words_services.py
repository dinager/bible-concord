import traceback
from typing import Tuple

from server.db_model.model.book import BookModel


def get_word_text_context(book_name: str, line_number: int) -> Tuple[bool, str]:
    try:
        book_file_path = BookModel.get_book_file_path(book_name)
        with open(book_file_path, "r") as file:
            lines = file.readlines()

        # Calculate the start and end indices, ensuring they are within bounds
        start_index = max(0, line_number - 4)
        end_index = min(len(lines), line_number + 4)

        # Get the surrounding lines
        surrounding_lines = lines[start_index:end_index]

        return True, "".join(surrounding_lines)

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
