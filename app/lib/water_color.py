from enum import Enum


class WaterColor(Enum):

    not_recorded = 0
    clear = 1
    slightly_cloudy = 2
    cloudy = 3
    murky = 4

    current_color = ""

    def __init__(self, color_int):
        self.not_recorded = 0
        self.clear = 1
        self.slightly_cloudy = 2
        self.cloudy = 3
        self.murky = 4
        if color_int == self.not_recorded:
            self.current_color = "Not Recorded"
        elif color_int == self.clear:
            self.current_color = "Clear"
        elif color_int == self.slightly_cloudy:
            self.current_color = "Slighty Cloudy"
        elif color_int == self.cloudy:
            self.current_color = "Cloudy"
        elif color_int == self.murky:
            self.current_color = "Murky"

    def get_color(self):
        return self.current_color

