from typing import List, TypedDict, Tuple

class HSVColor(TypedDict):
    name: str
    lower_hsv: Tuple[int, int, int]
    upper_hsv: Tuple[int, int, int]

white: HSVColor = {
    "name": "white",
    "lower_hsv": (0, 0, 184),
    "upper_hsv": (179, 39, 255),
}

red: HSVColor = {
    "name": "red",
    "lower_hsv": (0, 100, 0),
    "upper_hsv": (8, 255, 255),
}

blueish_red: HSVColor = {
    "name": "blueish_red",
    "lower_hsv": (170, 0, 0),
    "upper_hsv": (178, 255, 255),
}

orange: HSVColor = {
    "name": "orange",
    "lower_hsv": (7, 178, 0),
    "upper_hsv": (15, 255, 255),
}

yellow: HSVColor = {
    "name": "yellow",
    "lower_hsv": (23, 0, 0),
    "upper_hsv": (29, 255, 255),
}

green: HSVColor = {
    "name": "green",
    "lower_hsv": (48, 50, 0),
    "upper_hsv": (55, 255, 255),
}

sky_blue: HSVColor = {
    "name": "sky_blue",
    "lower_hsv": (95, 38, 0),
    "upper_hsv": (111, 190, 255),
}

blue: HSVColor = {
    "name": "blue",
    "lower_hsv": (112, 80, 0),
    "upper_hsv": (126, 255, 255),
}

black: HSVColor = {
    "name": "black",
    "lower_hsv": (0, 0, 0),
    "upper_hsv": (179, 255, 49),
}

all: List[HSVColor] = [white, red, orange, yellow, green, sky_blue, blue, blueish_red, black]
