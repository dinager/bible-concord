from server.logic.structures import BibleBook, Chapter, Verse
import re


def parse_book(book_name: str, book_text: str) -> BibleBook:
    """
    # parse the text to the BibleBook structure
    # text file example: tests/resources/genesis.txt
    """
    # temporary code, does noting in the meantime returns dummy code
    #lines = book_text.splitlines()
    #print(len(lines))
    return get_bible_book(book_name, book_text)
    #return get_dummy_book(book_name)


def get_bible_book(book_name: str, book_text: str) -> BibleBook:
    lines = book_text.splitlines()
    chapter_number = 0
    bible_structure = BibleBook(book_name, chapter_number, chapters=[])

    for line in lines:
        line = line.strip()
        # skip empty lines
        if not line:
            continue

        # Check if the line is the start of a new chapter
        if re.match(r'^[a-zA-Z]+\.[0-9]+', line):
            chapter_number += 1
            bible_structure.chapters.append(Chapter(chapter_number, 0, verses=[]))
        else:
            # Extract verse number and text
            match = re.match(r'\[(\d+)\] (.+)', line)
            if match:
                verse_number = int(match.group(1))
                verse_text = match.group(2)

                # Remove punctuation from the verse text
                verse_text = re.sub(r'[^\w\s]', '', verse_text)

                # Split the verse text into words
                words = verse_text.split()

                bible_structure.chapters[chapter_number - 1].num_verses = verse_number
                bible_structure.chapters[chapter_number - 1].verses.append(Verse(verse_number, len(words), words=words))

    bible_structure.num_chapters = chapter_number

    return bible_structure

"""
def get_dummy_book(book_name: str) -> BibleBook:
    return BibleBook(
        name=book_name,
        num_chapters=50,
        chapters=[
            Chapter(
                chapter_num=1,
                num_verses=31,
                verses=[
                    Verse(verse_num=1, num_words=4, words=["In", "the", "beginning", "God"]),
                    Verse(verse_num=2, num_words=6, words=["And", "the", "earth", "was"]),
                ],
            ),
            Chapter(
                chapter_num=2,
                num_verses=25,
                verses=[
                    Verse(verse_num=1, num_words=4, words=["In", "the"]),
                ],
            ),
        ],
    )
"""