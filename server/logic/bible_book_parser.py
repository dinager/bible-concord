from server.logic.structures import BibleBook, Chapter, Verse


def parse_book(book_text: str) -> BibleBook:
    """
    # parse the text to the BibleBook structure
    # text file example: tests/resources/genesis.txt
    """
    # temporary code, does noting in the meantime returns dummy code
    lines = book_text.splitlines()
    print(len(lines))
    return get_dummy_book()


def get_dummy_book() -> BibleBook:
    return BibleBook(
        name="genesis",
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
