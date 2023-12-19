from typing import Dict


class Word:
    def __init__(self):
        self.x0 = None
        self.y0 = None
        self.width = None
        self.height = None
        self.text = None

    def get_two_points(self) -> Dict:
        return {"x0": self.x0, "y0": self.y0, "x1": self.x0 + self.width, "y1": self.y0 + self.height}

    def get_point_and_size(self) -> Dict:
        return {"x0": self.x0, "y0": self.y0, "w": self.width, "h": self.height}

    def set_two_points(self, points: Dict):
        self.x0 = points["x0"]
        self.y0 = points["y0"]
        self.width = points["x1"] - points["x0"]
        self.height = points["y1"] - points["y0"]

    def set_point_and_size(self, point_and_size: Dict):
        self.x0 = point_and_size["x0"]
        self.y0 = point_and_size["y0"]
        self.width = point_and_size["w"]
        self.height = point_and_size["h"]

    def set_text(self, text: str):
        self.text = text

    def get_text(self) -> str:
        return self.text

    def __str__(self):
        word_str = ""
        if self.text is not None:
            word_str += self.text
        word_str += f"(x0: {self.x0}, y0: {self.y0} w: {self.width} , h: {self.height})"
        return word_str
