from dataclasses import dataclass


@dataclass
class Verse:
    verse_num: int
    num_words: int
    words: list[str]


@dataclass
class Chapter:
    chapter_num: int
    num_verses: int
    verses: list[Verse]


@dataclass
class BibleBook:
    name: str
    num_chapters: int
    chapters: list[Chapter]
