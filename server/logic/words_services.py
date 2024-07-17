import os
import re
import traceback
from typing import Tuple

from consts import EXT_DISK_PATH


def get_word_text_context(
    word: str, book_name: str, chapter_num: int, verse_num: int, index: int
) -> Tuple[bool, list[str] | str | None]:
    try:
        book_name = book_name.lower()

        with open(os.path.join(EXT_DISK_PATH, book_name + ".txt"), "r") as file:
            lines = file.readlines()

        # Prepare a list to store the results
        results = []

        # Define regex patterns for chapters and verses
        chapter_pattern = re.compile(rf"^[a-zA-Z]+\.{chapter_num}", re.IGNORECASE)
        verse_pattern = re.compile(rf"^\[{verse_num}\] (.+)$", re.IGNORECASE)

        in_chapter = False

        # Iterate over the lines and find the word
        for i, line in enumerate(lines):
            if chapter_pattern.match(line.strip()):
                in_chapter = True
            if in_chapter and verse_pattern.match(line.strip()):
                print(line.strip())
                prefix = f"Text content for word: '{word}' in book name {book_name}, chapter number {chapter_num}, verse number {verse_num} at position {index}\n\n"
                # Get the context lines (two before and two after)
                start_index = max(0, i - 2)
                end_index = min(len(lines), i + 3)
                context = lines[start_index:end_index]
                # Combine the prefix with the context and to to results
                result = prefix + "".join(context)
                results.append(result)
                return True, results

        return True, None

    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)
