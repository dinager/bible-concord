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
    def get_filtered_words_paginate(filters: dict, page_index: int, page_size: int) -> Tuple[List[dict], int]:
        # Query the book_id by title
        if filters.get("book"):
            book = BookModel.get_book_by_title(filters["book"].lower())
            book_id = book.book_id

        # Build the base query
        # query = db.session.query(WordAppearanceModel)

        # Build the base query
        query = db.session.query(WordAppearanceModel).join(
            WordModel, WordAppearanceModel.word_id == WordModel.word_id
        )

        # Initialize word_ids to None
        word_ids = None

        # Apply filters if they are provided
        if filters.get("book"):
            book_id = book_id
            query = query.filter(WordAppearanceModel.book_id == book_id)

        if filters.get("chapter"):
            query = query.filter(WordAppearanceModel.chapter_num == int(filters["chapter"]))

        if filters.get("verse"):
            query = query.filter(WordAppearanceModel.verse_num == int(filters["verse"]))

        if filters.get("indexInVerse"):
            query = query.filter(WordAppearanceModel.word_position == int(filters["indexInVerse"]))

        if filters.get("wordStartsWith"):
            # Use the helper function to get the relevant word_ids
            words_id = WordModel.get_word_ids_starting_with(filters["wordStartsWith"])
            if words_id:
                query = query.filter(WordAppearanceModel.word_id.in_(words_id))

        # Count the total number of unique results
        total_count_query = db.session.query(func.count(func.distinct(WordModel.value))).join(
            WordAppearanceModel, WordAppearanceModel.word_id == WordModel.word_id
        )

        # Apply the same filters to the total count query
        if filters.get("book"):
            total_count_query = total_count_query.filter(WordAppearanceModel.book_id == book_id)

        if filters.get("chapter"):
            total_count_query = total_count_query.filter(
                WordAppearanceModel.chapter_num == int(filters["chapter"])
            )

        if filters.get("verse"):
            total_count_query = total_count_query.filter(
                WordAppearanceModel.verse_num == int(filters["verse"])
            )

        if filters.get("indexInVerse"):
            total_count_query = total_count_query.filter(
                WordAppearanceModel.word_position == int(filters["indexInVerse"])
            )

        if filters.get("wordStartsWith"):
            if word_ids:
                total_count_query = total_count_query.filter(WordAppearanceModel.word_id.in_(word_ids))

        # Count the total number of results
        total_count = total_count_query.scalar()

        # Apply pagination
        # paginated_query = query.offset(page_index * page_size).limit(page_size)
        paginated_query = (
            query.with_entities(WordModel.value).distinct().offset(page_index * page_size).limit(page_size)
        )

        # Execute the query and fetch results
        word_values = [result[0] for result in paginated_query.all()]
        # Execute the query and fetch results
        # results = paginated_query.all()
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
        if filters.get("book"):
            book = BookModel.get_book_by_title(filters["book"].lower())
            query = query.filter(WordAppearanceModel.book_id == book.book_id)

        if filters.get("chapter"):
            query = query.filter(WordAppearanceModel.chapter_num == int(filters["chapter"]))

        if filters.get("verse"):
            query = query.filter(WordAppearanceModel.verse_num == int(filters["verse"]))

        if filters.get("indexInVerse"):
            query = query.filter(WordAppearanceModel.word_position == int(filters["indexInVerse"]))

        # Count the total number of results
        total_count_query = db.session.query(func.count(WordAppearanceModel.index)).filter(
            WordAppearanceModel.word_id == word_id
        )

        # Apply the same filters to the total count query
        if filters.get("book"):
            total_count_query = total_count_query.filter(WordAppearanceModel.book_id == book.book_id)

        if filters.get("chapter"):
            total_count_query = total_count_query.filter(
                WordAppearanceModel.chapter_num == int(filters["chapter"])
            )

        if filters.get("verse"):
            total_count_query = total_count_query.filter(
                WordAppearanceModel.verse_num == int(filters["verse"])
            )

        if filters.get("indexInVerse"):
            total_count_query = total_count_query.filter(
                WordAppearanceModel.word_position == int(filters["indexInVerse"])
            )

        total_count = total_count_query.scalar()

        # Apply pagination
        paginated_query = query.offset(page_index * page_size).limit(page_size)

        # Execute the query and fetch results
        results = paginated_query.all()

        # Format the results into a list of dictionaries
        appearances = [
            {
                "book": result.title,
                "chapter": result.chapter_num,
                "verse": result.verse_num,
                "indexInVerse": result.word_position,
                "lineNumInFile": result.line_num_in_file,
            }
            for result in results
        ]

        return appearances, total_count

    # todo: we might use these, and uncomment
    # book = db.relationship("Book", backref="word_appearances")
    # word = db.relationship("Word", backref="word_appearances")
