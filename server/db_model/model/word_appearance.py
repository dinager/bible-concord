from typing import Tuple, TypedDict

from sqlalchemy import Index, UniqueConstraint, and_, func, literal_column, or_

from server.db_instance import db
from server.db_model.model.book import BookModel
from server.db_model.model.chapter import ChapterModel
from server.db_model.model.word import WordModel


class WordAppearance(TypedDict):
    book: str
    chapter: int
    verse: int
    word_position: int


class WordAppearanceModel(db.Model):
    __tablename__ = "word_appearance"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey("word.word_id", ondelete="CASCADE"), nullable=False)
    verse_num = db.Column(db.Integer, nullable=False)
    chapter_num = db.Column(db.Integer, nullable=False)
    word_position = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("book_id", "word_id", "verse_num", "chapter_num", "word_position"),
        Index("idx_word_appearance", "book_id", "verse_num", "chapter_num"),  # Add composite index
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

        if word_position := filters.get("wordPosition"):
            query = query.filter(WordAppearanceModel.word_position == int(word_position))

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

        if word_position := filters.get("wordPosition"):
            query = query.filter(WordAppearanceModel.word_position == int(word_position))

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
                word_position=result.word_position,
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

    @classmethod
    def find_all_references_of_phrase(cls, phrase_text: str) -> list[WordAppearance]:
        phrase_list = phrase_text.split()
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
                WordAppearanceModel.book_id,
                WordAppearanceModel.chapter_num,
                WordAppearanceModel.verse_num,
                BookModel.title,
                concatenated_words,
                word_positions,
            )
            .join(WordModel, WordAppearanceModel.word_id == WordModel.word_id)
            .join(BookModel, WordAppearanceModel.book_id == BookModel.book_id)
            .filter(WordModel.value.in_(phrase_list))
            .group_by(
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
        print("Query Result11:", result)

        all_references = []

        for row in result:
            concatenated_words = row.concatenated_words.split(" ")
            word_positions = [int(pos) for pos in row.word_positions.split(",")]

            starting_word_positions = cls.get_consecutive_positions(
                phrase_list, concatenated_words, word_positions
            )

            # Check if the result is a tuple (indicating a match)
            if starting_word_positions:
                # Extract the starting word position from the result
                references = [
                    WordAppearance(
                        book=row.title,
                        chapter=row.chapter_num,
                        verse=row.verse_num,
                        word_position=starting_pos,
                    )
                    for starting_pos in starting_word_positions
                ]
                all_references.extend(references)
        return all_references

    @staticmethod
    def get_consecutive_positions(
        words_in_phrase: list[str], concatenated_words: list[str], word_positions: list[int]
    ) -> list[int]:
        """
        Get the starting positions of the phrase in the concatenated words where the positions are consecutive
        Example:
        >>>> get_consecutive_positions(["a", "b",], ["a", "b", "c", "a", "b"], [1, 2, 3, 4, 5)
        [1, 4]
        """
        phrase_length = len(words_in_phrase)
        match_start_positions = []
        # Iterate through potential starting points in concatenated_words
        for i in range(len(concatenated_words) - phrase_length + 1):
            # Check if the words match and positions are consecutive
            if concatenated_words[i : i + phrase_length] == words_in_phrase and all(
                word_positions[i + j] + 1 == word_positions[i + j + 1] for j in range(phrase_length - 1)
            ):
                match_start_positions.append(word_positions[i])
        return match_start_positions

    @staticmethod
    def get_group_word_appearances_index(group_name: str) -> list[dict]:
        from server.db_model.model.word_in_group import WordInGroupModel

        word_ids_in_group = WordInGroupModel.get_words_ids_in_group(group_name)
        # Subquery to get all matching word_ids, verse_num, and chapter_num
        subquery = (
            db.session.query(
                WordAppearanceModel.book_id,
                WordAppearanceModel.verse_num,
                WordAppearanceModel.chapter_num,
            )
            .filter(WordAppearanceModel.word_id.in_(word_ids_in_group))
            .distinct()
            .subquery()
        )

        # Sub query, for all verses that contain any of the group's words, get the full verse text
        text_query = (
            db.session.query(
                WordAppearanceModel.book_id,
                WordAppearanceModel.chapter_num,
                WordAppearanceModel.verse_num,
                func.group_concat(
                    literal_column("`word`.`value` ORDER BY `word_appearance`.`word_position` SEPARATOR ' '")
                ).label("verse_text"),
            )
            .join(WordModel, WordAppearanceModel.word_id == WordModel.word_id)
            .join(
                subquery,
                and_(
                    WordAppearanceModel.book_id == subquery.c.book_id,
                    WordAppearanceModel.verse_num == subquery.c.verse_num,
                    WordAppearanceModel.chapter_num == subquery.c.chapter_num,
                ),
            )
            .group_by(
                WordAppearanceModel.book_id,
                WordAppearanceModel.chapter_num,
                WordAppearanceModel.verse_num,
            )
            .subquery()
        )

        # Main query to get all the word appearances in the group
        query = (
            db.session.query(
                WordModel.value.label("word"),
                BookModel.title.label("book"),
                WordAppearanceModel.chapter_num,
                WordAppearanceModel.verse_num,
                WordAppearanceModel.word_position.label("word_index"),
                text_query.c.verse_text.label("verse_text"),
            )
            .join(WordModel, WordAppearanceModel.word_id == WordModel.word_id)
            .join(BookModel, WordAppearanceModel.book_id == BookModel.book_id)
            .join(
                text_query,
                and_(
                    WordAppearanceModel.book_id == text_query.c.book_id,
                    WordAppearanceModel.verse_num == text_query.c.verse_num,
                    WordAppearanceModel.chapter_num == text_query.c.chapter_num,
                ),
            )
            .order_by(
                WordModel.value,
                BookModel.title,
                WordAppearanceModel.chapter_num,
                WordAppearanceModel.verse_num,
                WordAppearanceModel.word_position,
                WordAppearanceModel.word_position,
            )
            .filter(WordAppearanceModel.word_id.in_(word_ids_in_group))
            .distinct()
        )

        res = [
            {
                "word": result.word,
                "book": result.book,
                "chapter": result.chapter_num,
                "verse": result.verse_num,
                "word_position": result.word_index,
                "verse_text": result.verse_text,
            }
            for result in query
        ]
        return res


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
