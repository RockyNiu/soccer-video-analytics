import numpy as np
from typing import Optional, Tuple, TYPE_CHECKING, Any
from numpy.typing import NDArray
from PIL import Image

from soccer.draw import Draw, RGB
from inference.box import Box

if TYPE_CHECKING:
    from soccer.match import Match


class Ball:
    def __init__(self, detection: Optional[Any] = None, box: Optional[Box] = None):
        """
        Initialize Ball

        Parameters
        ----------
        detection : norfair.Detection, optional
            norfair.Detection containing the ball
        box : Box, optional
            Bounding box for the ball
        """
        if detection is not None:
            self.detection = detection
            self.box = None  # Convert detection to box if needed
        elif box is not None:
            self.box = box
            self.detection = None
        else:
            raise ValueError("Either detection or box must be provided")
        
        self.color: Optional[RGB] = None

    @property
    def position(self) -> Tuple[float, float]:
        """Get the position (x, y) of the ball."""
        if self.box is not None:
            return (self.box.x, self.box.y)
        elif self.detection is not None:
            # Extract position from detection
            points = self.detection.points
            return (float(points[0][0]), float(points[0][1]))
        else:
            return (0.0, 0.0)

    def set_color(self, match: "Match"):
        """
        Sets the color of the ball to the team color with the ball possession in the match.

        Parameters
        ----------
        match : Match
            Match object
        """
        # Check if match has team_possession attribute and it's not None
        team_possession = getattr(match, 'team_possession', None)
        if team_possession is None:
            return

        self.color = team_possession.color

        if self.detection:
            self.detection.data["color"] = team_possession.color

    def get_center(self, points: NDArray[np.float64]) -> Tuple[float, float]:
        """
        Returns the center of the points

        Parameters
        ----------
        points : NDArray[np.float64]
            2D points array with shape (2, 2) containing [[x1, y1], [x2, y2]]

        Returns
        -------
        Tuple[float, float]
            (x, y) coordinates of the center
        """
        x1, y1 = points[0]
        x2, y2 = points[1]

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        return (float(center_x), float(center_y))

    @property
    def center(self) -> Optional[Tuple[int, int]]:
        """
        Returns the center of the ball

        Returns
        -------
        Optional[Tuple[int, int]]
            Center of the ball (x, y), or None if no detection
        """
        if self.detection is None:
            return None

        center = self.get_center(self.detection.points)
        round_center = np.round(center).astype(int)

        return (int(round_center[0]), int(round_center[1]))

    @property
    def center_abs(self) -> Optional[Tuple[int, int]]:
        """
        Returns the center of the ball in absolute coordinates

        Returns
        -------
        Optional[Tuple[int, int]]
            Center of the ball (x, y), or None if no detection
        """
        if self.detection is None:
            return None

        center = self.get_center(self.detection.absolute_points)
        round_center = np.round(center).astype(int)

        return (int(round_center[0]), int(round_center[1]))

    def draw(self, frame: Image.Image) -> Image.Image:
        """
        Draw the ball on the frame

        Parameters
        ----------
        frame : Image.Image
            Frame to draw on

        Returns
        -------
        Image.Image
            Frame with ball drawn
        """
        if self.detection is None:
            return frame

        # Extract position and size from detection points
        points = self.detection.points
        x = float(points[0][0])
        y = float(points[0][1])
        width = float(points[1][0] - points[0][0])
        height = float(points[1][1] - points[0][1])
        
        # Use ball color if available, otherwise default green
        color = self.color if self.color is not None else (0, 255, 0)

        return Draw.draw_detection(frame, x, y, width, height, color)

    def __str__(self) -> str:
        return f"Ball: {self.center}"
