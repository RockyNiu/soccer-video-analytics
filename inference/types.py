from typing import Tuple, TypedDict


class HSVColor(TypedDict):
    name: str
    lower_hsv: Tuple[int, int, int]
    upper_hsv: Tuple[int, int, int]


class Box:
    """A bounding box in an image."""
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        """Calculate the area of the box."""
        return self.width * self.height

    @property
    def points(self) -> list[Tuple[int, int]]:
        """Get the box corners as a list of points [(x1,y1), (x2,y2)]."""
        return [
            (int(self.x), int(self.y)),
            (int(self.x + self.width), int(self.y + self.height))
        ]

    def iou(self, other: 'Box') -> float:
        """Calculate Intersection over Union with another box."""
        # Calculate intersection coordinates
        x1 = max(self.x, other.x)
        y1 = max(self.y, other.y)
        x2 = min(self.x + self.width, other.x + other.width)
        y2 = min(self.y + self.height, other.y + other.height)

        # Check if boxes overlap
        if x2 <= x1 or y2 <= y1:
            return 0.0

        # Calculate intersection and union areas
        intersection = (x2 - x1) * (y2 - y1)
        union = self.area + other.area - intersection
        return intersection / union if union > 0 else 0.0