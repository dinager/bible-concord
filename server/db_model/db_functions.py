from server.db_instance import db
from server.db_model.model.book import BookModel
from server.db_model.model.chapter import ChapterModel
from server.db_model.model.word import WordModel
from server.db_model.model.word_appearance import WordAppearanceModel
from server.logic.structures import BibleBook


# tod: add lock?..
def insert_book_data_to_tables(book: BibleBook) -> None:
    session = db.session

    try:
        # Create new book
        new_book = BookModel(
            title=book.name,
            division=book.division,
            file_path=book.raw_text_path,
            file_size=book.file_size,
            num_chapters=book.num_chapters,
        )
        session.add(new_book)
        session.flush()  # Ensures new_book.book_id is available
        # Create new chapters
        new_chapters = [
            ChapterModel(
                book_id=new_book.book_id, num_chapter=chapter.chapter_num, num_verses=chapter.num_verses
            )
            for chapter in book.chapters
        ]

        session.add_all(new_chapters)

        # Create new words
        unique_words = list(
            set(word for chapter in book.chapters for verse in chapter.verses for word in verse.words)
        )
        existing_words_model = WordModel.get_existing_words(unique_words)
        existing_words = {word.value for word in existing_words_model}

        new_words = [
            WordModel(value=word, length=len(word)) for word in unique_words if word not in existing_words
        ]
        session.add_all(new_words)
        session.flush()  # Ensures new_words.word_id are available

        all_book_unique_words = existing_words_model + new_words

        def get_word_id(word_value: str) -> int:
            return next(word.word_id for word in all_book_unique_words if word.value == word_value)

        new_word_appearances = []
        for chapter in book.chapters:
            for verse in chapter.verses:
                # Create new word appearances
                for index, word_str in enumerate(verse.words, start=1):
                    new_word_appearances.append(
                        WordAppearanceModel(
                            book_id=new_book.book_id,
                            word_id=get_word_id(word_str),
                            verse_num=verse.verse_num,
                            chapter_num=chapter.chapter_num,
                            word_position=index,
                            line_num_in_file=verse.line_num_in_file,
                        )
                    )
        session.add_all(new_word_appearances)

        # Commit the transaction
        session.commit()
        print("Data inserted successfully.")
    except Exception as e:
        session.rollback()  # Rollback the transaction on error
        print(f"An error occurred: {e}")
        raise e
    finally:
        session.close()
