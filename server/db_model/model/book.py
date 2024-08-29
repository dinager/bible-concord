from datetime import datetime
from typing import Self

from sqlalchemy import DateTime, UniqueConstraint, func

from server.db_instance import db


class BookModel(db.Model):
    __tablename__ = "book"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), nullable=False, unique=True)
    division = db.Column(db.String(32), nullable=False)
    file_path = db.Column(db.String(128), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    num_chapters = db.Column(db.Integer, nullable=False)
    insert_date = db.Column(DateTime(), nullable=False, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("title"),)

    @classmethod
    def does_book_exist(cls, title: str) -> bool:
        return db.session.query(BookModel.book_id).filter_by(title=title.lower()).scalar() is not None

    @classmethod
    def get_all_books(cls) -> list[Self]:
        return db.session.query(BookModel).all()

    @classmethod
    def get_all_book_names(cls) -> list[str]:
        return [row.title for row in db.session.query(BookModel.title).all()]

    @classmethod
    def get_book(cls, title: str) -> Self | None:
        return db.session.query(BookModel).filter_by(title=title.lower()).one_or_none()

    @classmethod
    def get_book_id(cls, title: str) -> int | None:
        return db.session.query(BookModel.book_id).filter_by(title=title.lower()).scalar()

    @classmethod
    def get_book_file_path(cls, title: str) -> str | None:
        return db.session.query(BookModel.file_path).filter_by(title=title.lower()).scalar()

    @classmethod
    def delete_book_by_title(cls, title: str) -> None:
        db.session.query(BookModel).filter_by(title=title.lower()).delete()
        db.session.commit()

    @classmethod
    def get_book_statistics(cls, book_name: str | None) -> dict:
        from server.db_model.model.chapter import ChapterModel
        from server.db_model.model.word import WordModel
        from server.db_model.model.word_appearance import WordAppearanceModel

        book_id: str | None = None
        book = BookModel.get_book(book_name) if book_name else None
        # Number of Chapters
        if book:
            num_chapters = book.num_chapters
            book_id = book.book_id
        else:
            num_chapters = db.session.query(func.sum(BookModel.num_chapters)).scalar()

        # Total Number of Verses
        verse_query = db.session.query(func.sum(ChapterModel.num_verses))
        if book_id:
            verse_query = verse_query.filter(ChapterModel.book_id == book_id)
        num_verses = verse_query.scalar()

        # Total Number of Words
        word_query = db.session.query(func.count(WordAppearanceModel.index))
        if book_id:
            word_query = word_query.filter(WordAppearanceModel.book_id == book_id)
        num_words = word_query.scalar()

        # Unique Words Count
        unique_word_query = db.session.query(func.count(func.distinct(WordAppearanceModel.word_id)))
        if book_id:
            unique_word_query = unique_word_query.filter(WordAppearanceModel.book_id == book_id)
        unique_words_count = unique_word_query.scalar()

        # Total Number of Letters
        letter_query = db.session.query(func.sum(WordModel.length)).join(
            WordAppearanceModel, WordModel.word_id == WordAppearanceModel.word_id
        )
        if book_id:
            letter_query = letter_query.filter(WordAppearanceModel.book_id == book_id)
        total_letters = letter_query.scalar()

        # Average Number of Verses per Chapter
        avg_verses_per_chapter_query = db.session.query(func.avg(ChapterModel.num_verses))
        if book_id:
            avg_verses_per_chapter_query = avg_verses_per_chapter_query.filter(
                ChapterModel.book_id == book_id
            )
        avg_verses_per_chapter = avg_verses_per_chapter_query.scalar()

        # Average Number of Words per Verse
        word_count_subquery = db.session.query(
            WordAppearanceModel.book_id,
            WordAppearanceModel.chapter_num,
            WordAppearanceModel.verse_num,
            func.count(WordAppearanceModel.word_id).label("word_count"),
        )

        if book_id is not None:
            word_count_subquery = word_count_subquery.filter(WordAppearanceModel.book_id == book_id)

        word_count_subquery = word_count_subquery.group_by(
            WordAppearanceModel.book_id, WordAppearanceModel.chapter_num, WordAppearanceModel.verse_num
        ).subquery()

        avg_words_per_verse_query = db.session.query(func.avg(word_count_subquery.c.word_count)).scalar()

        # Average Number of Letters per Verse
        letter_count_subquery = db.session.query(
            WordAppearanceModel.book_id,
            WordAppearanceModel.chapter_num,
            WordAppearanceModel.verse_num,
            func.sum(WordModel.length).label("letter_count"),
        ).join(WordModel, WordModel.word_id == WordAppearanceModel.word_id)

        if book_id is not None:
            letter_count_subquery = letter_count_subquery.filter(WordAppearanceModel.book_id == book_id)

        letter_count_subquery = letter_count_subquery.group_by(
            WordAppearanceModel.book_id, WordAppearanceModel.chapter_num, WordAppearanceModel.verse_num
        ).subquery()

        avg_letters_per_verse_query = db.session.query(
            func.avg(letter_count_subquery.c.letter_count)
        ).scalar()

        return {
            "numChapters": num_chapters,
            "numVerses": num_verses,
            "totalWords": num_words,
            "totalUniqueWords": unique_words_count,
            "totalLetters": total_letters,
            "avgVersesPerChapter": int(avg_verses_per_chapter),
            "avgWordsPerVerse": int(avg_words_per_verse_query),
            "avgLettersPerVerse": int(avg_letters_per_verse_query),
        }
