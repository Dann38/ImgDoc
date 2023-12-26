from abc import ABC, abstractmethod
from img_doc.data_structures import Word, Block
from typing import List


class BaseBlockExtractorFromWord(ABC):
    @abstractmethod
    def extract_from_word(self, words: List[Word]) -> List[Block]:
        pass

    def join_intersect_blocks(self, blocks: List[Block]) -> List[Block]:
        new_blocks = []

        for block in blocks:
            self.__add_block_in_new_list(new_blocks, block)
        return new_blocks


    def __add_block_in_new_list(self, new_blocks, block):
        for new_block in new_blocks:
            if new_block.intersection(block):
                new_block.add_block_in_block(block)
                return
        new_blocks.append(block)
