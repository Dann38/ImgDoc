from abc import ABC, abstractmethod
from img_doc.data_structures import Word, Block
from typing import List


class BaseBlockExtractorFromWord(ABC):
    @abstractmethod
    def extract_from_word(self, words: List[Word]) -> List[Block]:
        pass
