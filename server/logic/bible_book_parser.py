import re

from server.logic.structures import Chapter, Verse


def parse_text_to_book_chapters(book_text: str) -> list[Chapter]:
    lines = book_text.splitlines()
    chapter_number = 0
    book_chapters: list[Chapter] = []
    for line in lines:
        line = line.strip()
        # skip empty lines
        if not line:
            continue

        # Check if the line is the start of a new chapter
        if re.match(r"^\d?[a-zA-Z]+\.[0-9]+", line):
            if len(book_chapters) > 0 and book_chapters[-1].num_verses == 0:
                raise ValueError(f"Chapter {chapter_number} has no verses")
            chapter_number += 1
            book_chapters.append(Chapter(chapter_num=chapter_number, num_verses=0, verses=[]))
        else:
            # Extract verse number and text
            match = re.match(r"\[(\d+)\] (.+)", line)
            if not match:
                raise ValueError(f"Invalid verse line format: {line}")

            verse_number = int(match.group(1))
            verse_text = match.group(2)

            # Remove punctuation from the verse text
            verse_text = re.sub(r"[^\w\s']", " ", verse_text)

            # Split the verse text into words
            words = [word.lower() for word in verse_text.split()]

            book_chapters[chapter_number - 1].num_verses = verse_number
            book_chapters[chapter_number - 1].verses.append(
                Verse(
                    verse_num=verse_number,
                    num_words=len(words),
                    words=words,
                )
            )

    if not book_chapters:
        raise ValueError("No chapters found in the text")
    if book_chapters[-1].num_verses == 0:
        raise ValueError(f"Chapter {chapter_number} has no verses")
    return book_chapters
