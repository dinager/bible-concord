from operator import and_
from typing import Dict, List, TypedDict

from sqlalchemy import ForeignKeyConstraint, func, literal_column, or_

from server.db_instance import db
from server.db_model.model.chapter import ChapterModel
from server.db_model.model.word import WordModel
from server.db_model.model.word_appearance import WordAppearanceModel


class PhraseReference(TypedDict):
    book_id: int
    chapter_num: int
    verse_num: int
    word_position: int
    line_num_in_file: int


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

    @classmethod
    def find_references_of_phrase(cls, phrase_name: str) -> list[PhraseReference]:
        phrase_list = phrase_name.split()
        phrase_joined = " ".join(phrase_list)
        max_index = WordAppearanceModel.get_max_word_index()
        seq = generate_sequences(max_index, len(phrase_list))

        session = db.session

        # https://groups.google.com/g/sqlalchemy/c/LKScX7jmrR4?pli=1
        concatenated_words = func.group_concat(
            literal_column("`word`.`value` ORDER BY `word_appearance`.`word_position` SEPARATOR ' '")
        ).label("concatenated_words")

        word_positions = func.group_concat(
            WordAppearanceModel.word_position.op("ORDER BY")(WordAppearanceModel.word_position)
        ).label("word_positions")

        ref_query = (
            session.query(
                WordAppearanceModel.line_num_in_file,
                WordAppearanceModel.book_id,
                WordAppearanceModel.chapter_num,
                WordAppearanceModel.verse_num,
                concatenated_words,
                word_positions,
            )
            .join(WordModel, WordAppearanceModel.word_id == WordModel.word_id)
            .filter(WordModel.value.in_(phrase_list))
            .group_by(
                WordAppearanceModel.line_num_in_file,
                WordAppearanceModel.book_id,
                WordAppearanceModel.chapter_num,
                WordAppearanceModel.verse_num,
            )
            .having(
                and_(
                    concatenated_words.like(f"%{phrase_joined}%"),
                    or_(*[word_positions.like(f"%{seq_item}%") for seq_item in seq]),
                )
            )
        )

        result = ref_query.all()
        print("Query Result:", result)

        all_references = []

        for row in result:
            concatenated_words = row.concatenated_words.split(" ")
            word_positions = [int(pos) for pos in row.word_positions.split(",")]

            starting_word_positions = PhraseReferenceModel.get_consecutive_positions(
                phrase_list, concatenated_words, word_positions
            )

            # Check if the result is a tuple (indicating a match)
            if starting_word_positions:
                # Extract the starting word position from the result
                references = [
                    PhraseReference(
                        book_id=row.book_id,
                        chapter_num=row.chapter_num,
                        verse_num=row.verse_num,
                        word_position=starting_pos,
                        line_num_in_file=row.line_num_in_file,
                    )
                    for starting_pos in starting_word_positions
                ]
                all_references.extend(references)
        return all_references

    @staticmethod
    def get_consecutive_positions(
        phrase_list: list[str], concatenated_words: list[str], word_positions: list[int]
    ) -> list[int]:
        """
        Get the starting positions of the phrase in the concatenated words where the positions are consecutive
        Example:
        >>>> get_consecutive_positions(["a", "b",], ["a", "b", "c", "a", "b"], [1, 2, 3, 4, 5)
        [1, 4]
        """
        phrase_length = len(phrase_list)
        match_start_positions = []
        # Iterate through potential starting points in concatenated_words
        for i in range(len(concatenated_words) - phrase_length + 1):
            # Check if the words match and positions are consecutive
            if concatenated_words[i : i + phrase_length] == phrase_list and all(
                word_positions[i + j] + 1 == word_positions[i + j + 1] for j in range(phrase_length - 1)
            ):
                match_start_positions.append(word_positions[i])
        return match_start_positions

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
    def construct_context_from_db(book_id: int, chapter_num: int, verse_num: int) -> str:
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
        verse_texts: Dict[int, List[str]] = {}
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


def generate_sequences(x: int, n: int) -> list[str]:
    """
    Generate all sequences of length n starting from 1 to x
    Example:
    >>>> generate_sequences(5, 3)
    ["1,2,3", "2,3,4", "3,4,5"]
    """
    sequences = []
    for i in range(1, x - n + 2):
        sequence = list(range(i, i + n))
        sequences.append(sequence)
    return [",".join(map(str, seq)) for seq in sequences]
