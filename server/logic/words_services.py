import os
import traceback
from typing import Tuple

from consts import EXT_DISK_PATH


def get_word_text_context(book_name: str, line_number: int) -> Tuple[bool, str]:
    try:
        book_name = book_name.lower()
        with open(os.path.join(EXT_DISK_PATH, book_name + ".txt"), "r") as file:
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
