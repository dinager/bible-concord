from typing import TypedDict

from sqlalchemy import ForeignKeyConstraint, text
from sqlalchemy.exc import SQLAlchemyError

from server.db_instance import db


class PhraseReference(TypedDict):
    phrase_id: int
    book_id: int
    chapter_num: int
    verse_num: int
    lineNumInFile: int


class PhraseReferenceModel(db.Model):
    __tablename__ = "phrase_reference"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phrase_id = db.Column(db.Integer, db.ForeignKey("phrase.phrase_id", ondelete="CASCADE"), nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    verse_num = db.Column(db.Integer, nullable=False)
    chapter_num = db.Column(db.Integer, nullable=False)
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
                if res:
                    reference = PhraseReference(
                        phrase_id=phrase_id,
                        book_id=row.book_id,
                        chapter_num=row.chapter_num,
                        verse_num=row.verse_num,
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
    ) -> bool:
        phrase_length = len(phrase_list)

        # Iterate through potential starting points in concatenated_words
        for i in range(len(concatenated_words) - phrase_length + 1):
            # Check if the words match and positions are consecutive
            if concatenated_words[i : i + phrase_length] == phrase_list and all(
                word_positions[i + j] + 1 == word_positions[i + j + 1] for j in range(phrase_length - 1)
            ):
                return True
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
                PhraseReferenceModel.book_id, PhraseReferenceModel.chapter_num, PhraseReferenceModel.verse_num
            )
            .filter(PhraseReferenceModel.phrase_id == phrase_id)
            .all()
        )

        # Convert the results to a list of dictionaries
        result_list = [
            {"book_id": row.book_id, "chapter_num": row.chapter_num, "verse_num": row.verse_num}
            for row in results
        ]

        return result_list
