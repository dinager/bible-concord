from typing import List, Optional, Tuple

from sqlalchemy import UniqueConstraint, func

from server.db_instance import db
from server.db_model.model.book import BookModel
from server.db_model.model.word import WordModel


class WordAppearanceModel(db.Model):
    __tablename__ = "word_appearance"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("word.word_id", ondelete="CASCADE"), nullable=False)
    verse_num = db.Column(db.Integer, nullable=False)
    chapter_num = db.Column(db.Integer, nullable=False)
    word_position = db.Column(db.Integer, nullable=False)
    line_num_in_file = db.Column(db.Integer, nullable=False)

    __table_args__ = (UniqueConstraint("book_id", "word_id", "verse_num", "chapter_num", "word_position"),)

    @staticmethod
    def get_num_words(book_name: str, chapter_num: int, verse_num: int) -> Optional[int]:
        # Query the book_id by title
        book = BookModel.get_book_by_title(book_name)
        book_id = book.book_id
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

    @staticmethod
    def get_filtered_words_paginate(filters: dict, page_index: int, page_size: int) -> Tuple[List[str], int]:
        query = db.session.query(WordModel.value).join(
            WordAppearanceModel, WordAppearanceModel.word_id == WordModel.word_id
        )

        # Apply filters if they are provided
        if book_name := filters.get("book"):
            book = BookModel.get_book_by_title(book_name.lower())
            query = query.filter(WordAppearanceModel.book_id == book.book_id)

        if chapter := filters.get("chapter"):
            query = query.filter(WordAppearanceModel.chapter_num == int(chapter))

        if verse := filters.get("verse"):
            query = query.filter(WordAppearanceModel.verse_num == int(verse))

        if ind_in_verse := filters.get("indexInVerse"):
            query = query.filter(WordAppearanceModel.word_position == int(ind_in_verse))

        if word_starts_with := filters.get("wordStartsWith"):
            query = query.filter(WordModel.value.startswith(word_starts_with))

        paginated_results = (
            # query.distinct().offset(page_index * page_size).limit(page_size).all()
            query.order_by(WordModel.value)
            .distinct()
            .offset(page_index * page_size)
            .limit(page_size)
            .all()
        )
        total_count = query.with_entities(func.count(func.distinct(WordModel.value))).scalar()

        word_values = [result[0] for result in paginated_results]
        return word_values, total_count

    @staticmethod
    def get_word_appearances_paginate(
        word: str, filters: dict, page_index: int, page_size: int
    ) -> Tuple[List[dict], int]:
        # Query to find the word ID by the word value
        word_record = db.session.query(WordModel).filter(func.lower(WordModel.value) == word).first()
        if not word_record:
            return [], 0  # If the word is not found, return empty list and count 0

        word_id = word_record.word_id

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
            book = BookModel.get_book_by_title(book_name.lower())
            query = query.filter(WordAppearanceModel.book_id == book.book_id)

        if chapter := filters.get("chapter"):
            query = query.filter(WordAppearanceModel.chapter_num == int(chapter))

        if verse := filters.get("verse"):
            query = query.filter(WordAppearanceModel.verse_num == int(verse))

        if ind_in_verse := filters.get("indexInVerse"):
            query = query.filter(WordAppearanceModel.word_position == int(ind_in_verse))

        # Apply ordering
        query = query.order_by(
            BookModel.title,
            WordAppearanceModel.chapter_num,
            WordAppearanceModel.verse_num,
            WordAppearanceModel.word_position,
        )

        # Apply pagination
        paginated_results = query.distinct().offset(page_index * page_size).limit(page_size).all()

        total_count = query.with_entities(func.count(func.distinct(WordModel.value))).scalar()

        # Format the results into a list of dictionaries
        appearances = [
            {
                "book": result.title,
                "chapter": result.chapter_num,
                "verse": result.verse_num,
                "indexInVerse": result.word_position,
                "lineNumInFile": result.line_num_in_file,
            }
            for result in paginated_results
        ]

        return appearances, total_count

    # todo: we might use these, and uncomment
    # book = db.relationship("Book", backref="word_appearances")
    # word = db.relationship("Word", backref="word_appearances")
