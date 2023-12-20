from . import Word, Row
from ..image import ImageSegment
from typing import List

class Block:
    def __init__(self, rows: List[Row] = [], words: List[Word] = [],
                 x0: int = 0, y0: int = 0, x1: int = 0, y1: int = 0):
        self.rows = rows
        self.words = words
        self.segment = ImageSegment(x0, y0, x1, y1)

    def set_words(self, words):
        self.words = words
        self.segment.set_segment_max_segments([word.segment for word in words])
