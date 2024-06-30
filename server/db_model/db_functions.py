from server.db_instance import db
from server.db_model.model.book import BookModel
from server.db_model.model.chapter import ChapterModel
from server.db_model.model.word import WordModel
from server.db_model.model.word_appearance import WordAppearanceModel
from server.logic.structures import BibleBook


def insert_book(book: BibleBook) -> None:
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

        unique_words = set(
            word for chapter in book.chapters for verse in chapter.verses for word in verse.words
        )
        new_words = [WordModel(value=word, length=len(word)) for word in unique_words]
        session.add_all(new_words)
        session.flush()  # Ensures new_words.word_id are available

        def get_word_obj(word_value: str) -> WordModel:
            return next(word for word in new_words if word.value == word_value)

            # Check if step already exists in master_rid_params and has an rid

        new_word_appearances = []
        for chapter in book.chapters:
            for verse in chapter.verses:
                # Create new word appearances
                new_word_appearances += [
                    WordAppearanceModel(
                        book_id=new_book.book_id,
                        word_id=get_word_obj(word_str).word_id,
                        verse_num=1,
                        chapter_num=1,
                        word_position=1,
                    )
                    for word_str in verse.words
                ]
        session.add_all(new_word_appearances)

        # Commit the transaction
        session.commit()
        print("Data inserted successfully.")
    except Exception as e:
        session.rollback()  # Rollback the transaction on error
        print(f"An error occurred: {e}")
    #     todo: raise e
    finally:
        session.close()


# Run the insert function
# insert_data()
# book2 = {"chapters": [
#       {"verses": [
#           {"words": ["hello", "world"]},
#           {"words": ["bob", "jim"]},
#       ]},
#       {"verses": [
#           {"words": ["donald", "trump"]},
#           {"words": ["good", "bye"]},
#       ]}
#   ]}
#   a = [
#       word
#       for chapter in book2["chapters"]
#       for verse in chapter["verses"]
#       for word in verse["words"]
#   ]
