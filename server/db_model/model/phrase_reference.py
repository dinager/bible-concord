from typing import Dict, List, Tuple, TypedDict

from sqlalchemy import ForeignKeyConstraint, text
from sqlalchemy.exc import SQLAlchemyError

from server.db_instance import db
from server.db_model.model.word import WordModel
from server.db_model.model.word_appearance import WordAppearanceModel


class PhraseReference(TypedDict):
    phrase_id: int
    book_id: int
    chapter_num: int
    verse_num: int
    word_position: int
    lineNumInFile: int


class PhraseReferenceModel(db.Model):
    __tablename__ = "phrase_reference"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phrase_id = db.Column(db.Integer, db.ForeignKey("phrase.phrase_id", ondelete="CASCADE"), nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    verse_num = db.Column(db.Integer, nullable=False)
    chapter_num = db.Column(db.Integer, nullable=False)
    word_position = db.Column(db.Integer, nullable=False)
    line_num_in_file = db.Column(db.Integer, nullable=False)

    # Composite foreign key relationship
    __table_args__ = (
        ForeignKeyConstraint(
            ["book_id", "line_num_in_file", "verse_num", "chapter_num"],
            [
                "word_appearance.book_id",
                "word_appearance.line_num_in_file",
                "word_appearance.verse_num",
                "word_appearance.chapter_num",
            ],
            ondelete="CASCADE",
        ),
    )

    @staticmethod
    def add_references_of_phrases(phrase_name: str, phrase_id: int) -> int:
        phrase_list = phrase_name.split()
        references = []
        phrase_joined = " ".join(phrase_list)

        placeholders = ", ".join([f":value_{i}" for i in range(len(phrase_list))])

        sql_query = text(
            f"""
            SELECT
                wa.line_num_in_file,
                wa.book_id,
                wa.chapter_num,
                wa.verse_num,
                GROUP_CONCAT(wi.value ORDER BY wa.word_position SEPARATOR ' ') AS concatenated_words,
                GROUP_CONCAT(wa.word_position ORDER BY wa.word_position) AS word_positions
            FROM
                word_appearance wa
            INNER JOIN
                word wi ON wa.word_id = wi.word_id
            WHERE
                wi.value in ({placeholders})
            GROUP BY
                wa.line_num_in_file,
                wa.book_id,
                wa.chapter_num,
                wa.verse_num
            HAVING
                GROUP_CONCAT(wi.value ORDER BY wa.word_position SEPARATOR ' ') LIKE :phrase_joined
        """
        )

        params = {f"value_{i}": word for i, word in enumerate(phrase_list)}
        params["phrase_joined"] = f"%{phrase_joined}%"

        session = db.session

        print(str(sql_query))

        try:
            result = session.execute(sql_query, params).fetchall()
            print("Query Result:", result)

            for row in result:
                concatenated_words = [char for char in row.concatenated_words]
                concatenated_words = row.concatenated_words.split(" ")
                word_positions = [int(pos) for pos in row.word_positions.split(",")]

                res = PhraseReferenceModel.has_consecutive_positions(
                    phrase_list, concatenated_words, word_positions
                )

                # Check if the result is a tuple (indicating a match)
                if isinstance(res, tuple) and res[0] is True:
                    # Extract the starting word position from the result
                    starting_word_position = res[1]
                    reference = PhraseReference(
                        phrase_id=phrase_id,
                        book_id=row.book_id,
                        chapter_num=row.chapter_num,
                        verse_num=row.verse_num,
                        word_position=starting_word_position,
                        lineNumInFile=row.line_num_in_file,
                    )
                    references.append(reference)

            if not references:
                return -1
            else:
                if PhraseReferenceModel.insert_phrase_reference_to_table(references) == -1:
                    return -1
                return 0

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error executing query: {e}")
            return -1

    @staticmethod
    def has_consecutive_positions(
        phrase_list: list[str], concatenated_words: list[str], word_positions: list[int]
    ) -> Tuple[bool, int] | bool:
        phrase_length = len(phrase_list)

        # Iterate through potential starting points in concatenated_words
        for i in range(len(concatenated_words) - phrase_length + 1):
            # Check if the words match and positions are consecutive
            if concatenated_words[i : i + phrase_length] == phrase_list and all(
                word_positions[i + j] + 1 == word_positions[i + j + 1] for j in range(phrase_length - 1)
            ):
                return True, word_positions[i]
        return False

    @staticmethod
    def insert_phrase_reference_to_table(phrase_pointer: list[PhraseReference]) -> int:
        try:
            for phrase_object in phrase_pointer:
                phrase_reference = PhraseReferenceModel(
                    phrase_id=phrase_object["phrase_id"],
                    book_id=phrase_object["book_id"],
                    verse_num=phrase_object["verse_num"],
                    chapter_num=phrase_object["chapter_num"],
                    word_position=phrase_object["word_position"],
                    line_num_in_file=phrase_object["lineNumInFile"],
                )
                db.session.add(phrase_reference)
            db.session.commit()
            return 0

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error inserting phrase references: {e}")
            return -1

    @staticmethod
    def get_all_phrase_references(phrase_id: int) -> list[dict]:
        # Query to fetch all rows for the specific phrase_id
        results = (
            db.session.query(
                PhraseReferenceModel.book_id,
                PhraseReferenceModel.chapter_num,
                PhraseReferenceModel.verse_num,
                PhraseReferenceModel.word_position,
            )
            .filter(PhraseReferenceModel.phrase_id == phrase_id)
            .all()
        )

        # Convert the results to a list of dictionaries
        result_list = [
            {
                "book_id": row.book_id,
                "chapter_num": row.chapter_num,
                "verse_num": row.verse_num,
                "word_position": row.word_position,
            }
            for row in results
        ]

        return result_list

    @staticmethod
    def get_verse_range(book_id: int, chapter_num: int) -> Tuple[int, int]:
        session = db.session
        min_verse = (
            session.query(db.func.min(WordAppearanceModel.verse_num))
            .filter(WordAppearanceModel.book_id == book_id, WordAppearanceModel.chapter_num == chapter_num)
            .scalar()
        )

        max_verse = (
            session.query(db.func.max(WordAppearanceModel.verse_num))
            .filter(WordAppearanceModel.book_id == book_id, WordAppearanceModel.chapter_num == chapter_num)
            .scalar()
        )

        return min_verse, max_verse

    @staticmethod
    def construct_context_from_db(book_id: int, chapter_num: int, verse_num: int) -> str:
        session = db.session

        verse_num = int(verse_num)
        # Get the range of verses in the chapter
        min_verse, max_verse = PhraseReferenceModel.get_verse_range(book_id, chapter_num)

        # Determine the actual range to query
        start_verse = max(min_verse, verse_num - 2)
        end_verse = min(max_verse, verse_num + 2)

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
        verse_texts: Dict[int, List[str]] = {}
        for word in words:
            if word.verse_num not in verse_texts:
                verse_texts[word.verse_num] = []
            verse_texts[word.verse_num].append(word.word)

        # Construct the entire text with each verse on a new line
        entire_text = "\n".join([" ".join(verse_texts[verse]) for verse in sorted(verse_texts.keys())])

        return entire_text
