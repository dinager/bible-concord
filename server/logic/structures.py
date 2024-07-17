from dataclasses import dataclass


@dataclass
class Verse:
    verse_num: int
    num_words: int
    words: list[str]
    line_num_in_file: int


@dataclass
class Chapter:
    chapter_num: int
    num_verses: int
    verses: list[Verse]


@dataclass
class BibleBook:
    name: str
    division: str
    num_chapters: int
    chapters: list[Chapter]
    raw_text_path: str
    file_size: int
