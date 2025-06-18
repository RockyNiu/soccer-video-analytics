from typing import Optional
import numpy as np
from numpy.typing import NDArray

from .types import Box as BoxBase


class Box(BoxBase):
    """A bounding box in an image."""
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        img: Optional[NDArray[np.uint8]] = None
    ):
        """
        Initialize Box with coordinates and optional image data

        Parameters
        ----------
        x : float
            X coordinate of top-left corner
        y : float
            Y coordinate of top-left corner
        width : float
            Width of the box
        height : float
            Height of the box
        img : Optional[NDArray[np.uint8]], optional
            Image containing the box, by default None
        """
        super().__init__(x, y, width, height)
        self.img = self.cut(img.copy()) if img is not None else None

    def cut(self, img: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Cuts the box from the image

        Parameters
        ----------
        img : NDArray[np.uint8]
            Image containing the box

        Returns
        -------
        NDArray[np.uint8]
            Image containing only the box
        """
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        return img[y1:y2, x1:x2]
