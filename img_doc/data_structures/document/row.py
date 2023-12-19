from .word import Word
from typing import List


class Row:
    def __init__(self):
        self.words: List[Word]
        self.x0: int
        self.y0: int
        self.width: int
        self.height: int

    def set_words(self, words: List[Word]):
        self.words = words


        p1, p2 = words[0].get_two_points()
        x0 = p1[0]
        y0 = p1[1]
        x1 = p2[0]
        y1 = p2[1]
        for word in words[1:]:
            pass


