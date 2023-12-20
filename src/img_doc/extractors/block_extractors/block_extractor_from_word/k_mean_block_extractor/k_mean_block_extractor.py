from ..base_block_extractor_from_word import *
from img_doc.data_structures import ImageSegment, Word, Block
import numpy as np


class KMeanBlockExtractor(BaseBlockExtractorFromWord):
    def extract_from_word(self, words: List[Word]) -> List[Block]:
        neighbors = self.get_index_neighbors_word(words)

        return [Block()]

    def get_index_neighbors_word(self, words, max_level=3):
        hash_matrix, fun_hashkey = self.get_hash_matrix(words)
        neighbors = []
        for k in range(len(words)):
            top_right_bottom_left = [k, k, k, k]
            for i, vec in enumerate(["top", "right", "bottom", "left"]):
                top_right_bottom_left[i] = self.get_neighbor_fun(words, k, hash_matrix,
                                                                 fun_hashkey, max_level, vec)

            neighbors.append(top_right_bottom_left)
        return neighbors

    def get_hash_matrix(self, words):
        n = len(words)

        segment_words = ImageSegment(0, 0, 0, 0)
        segment_words.set_segment_max_segments([word.segment for word in words])

        h = segment_words.get_height()
        w = segment_words.get_width()

        coef = w / h

        m_width = round((n * coef) ** 0.5)
        m_height = round(m_width / coef)

        dh = h / m_height
        dw = w / m_width
        ch = segment_words.y_top_left
        cw = segment_words.x_top_left
        hashkey = lambda word: self.get_index_hash(word, dh, dw, ch, cw)

        hash_matrix = [[[] for i in range(m_width)] for j in range(m_height)]

        for i, word in enumerate(words):
            hash_i, hash_j = hashkey(word)
            hash_matrix[hash_i][hash_j].append(i)

        return hash_matrix, hashkey

    def get_index_hash(self, word, dh, dw, ch, cw):
        x_c, y_c = word.segment.get_center()
        hash_i = int((y_c - ch) / dh)
        hash_j = int((x_c - cw) / dw)
        return hash_i, hash_j

    def get_words_hash_cell(self, hash_matrix, hash_i, hash_j):

        return hash_matrix[hash_i][hash_j]

    def get_word_index_level(self, words, k, hash_matrix, fun_hashkey, level, vec):
        index_h, index_w = fun_hashkey(words[k])

        index_h_max = len(hash_matrix)
        index_w_max = len(hash_matrix[0])

        if vec in ("left", "right"):
            new_index_w = index_w - level if vec == "left" else index_w + level
            new_index_h = index_h

            new_index_h0 = max(0, index_h - level)
            new_index_h1 = min(index_h_max - 1, index_h + level)
            word_ = words[k].segment.x_top_left if vec == "left" else - words[k].segment.x_bottom_right
        elif vec in ("top", "bottom"):
            new_index_h = index_h - level if vec == "top" else index_h + level
            new_index_w = index_w
            new_index_w0 = max(0, index_w - level)
            new_index_w1 = min(index_w_max - 1, index_w + level)
            word_ = words[k].segment.y_top_left if vec == "top" else - words[k].segment.y_bottom_right

        if new_index_w < 0 or new_index_w >= index_w_max or new_index_h < 0 or new_index_h >= index_h_max:
            return k
        else:
            neighbors = []
            if vec in ("left", "right"):
                for new_index_h_i in range(new_index_h0, new_index_h1 + 1):
                    neighbors += self.get_words_hash_cell(hash_matrix, new_index_h_i, new_index_w)  #
            else:
                for new_index_w_i in range(new_index_w0, new_index_w1 + 1):  #
                    neighbors += self.get_words_hash_cell(hash_matrix, new_index_h, new_index_w_i)  #

        min_distance = np.inf
        min_index = k

        for neighbor_index_word in neighbors:
            if vec in ("left", "right"):
                neughbord_word_ = words[neighbor_index_word].segment.x_bottom_right if vec == "left" \
                    else - words[neighbor_index_word].segment.x_top_left
            else:
                neughbord_word_ = words[neighbor_index_word].segment.y_bottom_right if vec == "top" \
                    else - words[neighbor_index_word].segment.y_top_left

            distance = word_ - neughbord_word_
            if distance > 0 and distance < min_distance:
                min_distance = distance
                min_index = neighbor_index_word
        return min_index

    def get_neighbor_fun(self, words, k, hash_matrix, fun_hashkey, max_level, vec):
        for level in range(max_level):
            min_index_word = self.get_word_index_level(words, k, hash_matrix, fun_hashkey, level, vec)
            if min_index_word != k:
                return min_index_word
        return k
