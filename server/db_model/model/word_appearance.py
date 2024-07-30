from typing import Tuple, TypedDict

from sqlalchemy import Index, UniqueConstraint, func

from server.db_instance import db
from server.db_model.model.book import BookModel
from server.db_model.model.chapter import ChapterModel
from server.db_model.model.word import WordModel


class WordAppearance(TypedDict):
    book: str
    chapter: int
    verse: int
    indexInVerse: int
    lineNumInFile: int


class WordAppearanceModel(db.Model):
    __tablename__ = "word_appearance"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("word.word_id", ondelete="CASCADE"), nullable=False)
    verse_num = db.Column(db.Integer, nullable=False)
    chapter_num = db.Column(db.Integer, nullable=False)
    word_position = db.Column(db.Integer, nullable=False)
    line_num_in_file = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("book_id", "word_id", "verse_num", "chapter_num", "word_position"),
        Index(
            "idx_word_appearance", "book_id", "line_num_in_file", "verse_num", "chapter_num"
        ),  # Add composite index
    )

    # todo: we might use these, and uncomment
    # book = db.relationship("Book", backref="word_appearances")
    # word = db.relationship("Word", backref="word_appearances")

    @classmethod
    def get_num_words(cls, book_name: str, chapter_num: int, verse_num: int) -> int | None:
        # Query the book_id by title
        book_id = BookModel.get_book_id(book_name)
        if book_id is None:
            return -1

        # Count the words in the specified verse
        word_count = (
            db.session.query(func.count(WordAppearanceModel.index))
            .filter_by(book_id=book_id, chapter_num=chapter_num, verse_num=verse_num)
            .scalar()
            or 0
        )
        return word_count

    @classmethod
    def get_filtered_words_paginate(
        cls, filters: dict, page_index: int, page_size: int
    ) -> Tuple[list[str], int]:
        from server.db_model.model.word_in_group import WordInGroupModel

        query = (
            db.session.query(WordModel.value)
            .join(WordAppearanceModel, WordAppearanceModel.word_id == WordModel.word_id)
            .distinct()
        )

        # Apply filters if they are provided
        if book_name := filters.get("book"):
            book_id = BookModel.get_book_id(book_name.lower())
            query = query.filter(WordAppearanceModel.book_id == book_id)

        if chapter := filters.get("chapter"):
            query = query.filter(WordAppearanceModel.chapter_num == int(chapter))

        if verse := filters.get("verse"):
            query = query.filter(WordAppearanceModel.verse_num == int(verse))

        if ind_in_verse := filters.get("indexInVerse"):
            query = query.filter(WordAppearanceModel.word_position == int(ind_in_verse))

        if word_starts_with := filters.get("wordStartsWith"):
            query = query.filter(WordModel.value.startswith(word_starts_with))

        if group_name := filters.get("groupName"):
            word_ids_in_group = WordInGroupModel.get_words_ids_in_group(group_name)
            query = query.filter(WordModel.word_id.in_(word_ids_in_group))

        paginated_results = (
            query.order_by(WordModel.value).offset(page_index * page_size).limit(page_size).all()
        )

        total_count = query.count()

        word_values = [result[0] for result in paginated_results]
        return word_values, total_count

    @classmethod
    def get_word_appearances_paginate(
        cls, word: str, filters: dict, page_index: int, page_size: int
    ) -> Tuple[list[WordAppearance], int]:
        word_id = db.session.query(WordModel.word_id).filter(func.lower(WordModel.value) == word).scalar()
        # If the word is not found, return empty list and count 0
        if word_id is None:
            return [], 0

        # Build the query to find word appearances
        query = (
            db.session.query(
                WordAppearanceModel.book_id,
                WordAppearanceModel.chapter_num,
                WordAppearanceModel.verse_num,
                WordAppearanceModel.word_position,
                WordAppearanceModel.line_num_in_file,
                BookModel.title,
            )
            .join(BookModel, WordAppearanceModel.book_id == BookModel.book_id)
            .filter(WordAppearanceModel.word_id == word_id)
        )

        # Apply filters if they are provided
        if book_name := filters.get("book"):
            query = query.filter(BookModel.title == book_name.lower())

        if chapter := filters.get("chapter"):
            query = query.filter(WordAppearanceModel.chapter_num == int(chapter))

        if verse := filters.get("verse"):
            query = query.filter(WordAppearanceModel.verse_num == int(verse))

        if ind_in_verse := filters.get("indexInVerse"):
            query = query.filter(WordAppearanceModel.word_position == int(ind_in_verse))

        paginated_results = (
            query.order_by(
                BookModel.title,
                WordAppearanceModel.chapter_num,
                WordAppearanceModel.verse_num,
                WordAppearanceModel.word_position,
            )
            .offset(page_index * page_size)
            .limit(page_size)
            .all()
        )

        total_count = query.count()
        appearances = [
            WordAppearance(
                book=result.title,
                chapter=result.chapter_num,
                verse=result.verse_num,
                indexInVerse=result.word_position,
                lineNumInFile=result.line_num_in_file,
            )
            for result in paginated_results
        ]

        return appearances, total_count

    @staticmethod
    def construct_context(book_id: int, chapter_num: int, verse_num: int) -> str:
        session = db.session

        verse_num = int(verse_num)
        # Get the range of verses in the chapter
        num_verses_in_chapter = ChapterModel.get_num_verses(book_id, chapter_num)
        # Determine the actual range to query
        start_verse = max(1, verse_num - 2)
        end_verse = min(num_verses_in_chapter, verse_num + 2)

        # Fetch words from the specified range of verses
        words = (
            session.query(
                WordAppearanceModel.word_position,
                WordAppearanceModel.verse_num,
                WordModel.value.label("word"),
            )
            .join(WordModel, WordAppearanceModel.word_id == WordModel.word_id)
            .filter(
                WordAppearanceModel.book_id == book_id,
                WordAppearanceModel.chapter_num == chapter_num,
                WordAppearanceModel.verse_num.between(start_verse, end_verse),
            )
            .order_by(WordAppearanceModel.verse_num, WordAppearanceModel.word_position)
            .all()
        )

        # Construct the verse text
        verse_texts: dict[int, list[str]] = {}
        for word in words:
            if word.verse_num not in verse_texts:
                verse_texts[word.verse_num] = []
            verse_texts[word.verse_num].append(word.word)

        # Construct the entire text with each verse on a new line
        # capitalize the first word of each verse
        entire_text = "\n".join(
            [
                f"[{verse}] {verse_texts[verse][0].capitalize()} {' '.join(verse_texts[verse][1:])}"
                for verse in sorted(verse_texts.keys())
            ]
        )

        return entire_text

    @classmethod
    def get_max_word_index(cls) -> int:
        max_index = db.session.query(func.max(WordAppearanceModel.word_position)).scalar() or 0
        return max_index
