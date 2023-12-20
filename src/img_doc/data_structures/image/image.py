from abc import ABC
import numpy as np
from .image_segment import ImageSegment


class Image(ABC):
    """
    img : RGB !!!
    """
    def __init__(self, img: np.ndarray):
        self.img = img
        self.segment = ImageSegment(0, 0, self.img.shape[1], self.img.shape[0])


