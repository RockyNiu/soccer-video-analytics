from typing import List, Optional

import numpy as np
import PIL.Image
from norfair.tracker import Detection  # type: ignore
from numpy.typing import NDArray

from soccer.ball import Ball
from soccer.draw import Draw
from soccer.team import Team


class Player:
    def __init__(self, detection: Detection) -> None:
        """

        Initialize Player

        Parameters
        ----------
        detection : Detection
            Detection containing the player
        """
        self.detection = detection

        self.team: Optional[Team] = None

        if detection:
            if "team" in detection.data:
                self.team = detection.data["team"]

    def get_left_foot(self, points: NDArray[np.float64]) -> List[float]:
        """Get left foot position from detection points."""
        x1, _ = points[0]
        _, y2 = points[1]
        return [float(x1), float(y2)]

    def get_right_foot(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        """Get right foot position from detection points."""
        result = points[1].copy()
        return result.astype(np.float64)

    @property
    def left_foot(self) -> List[float]:
        points = self.detection.points  # type: ignore
        if not isinstance(points, np.ndarray):
            points = np.array(points, dtype=np.float64)
        else:
            points = points.astype(np.float64)
        left_foot = self.get_left_foot(points)
        return left_foot

    @property
    def right_foot(self) -> NDArray[np.float64]:
        points = self.detection.points  # type: ignore
        if not isinstance(points, np.ndarray):
            points = np.array(points, dtype=np.float64)
        else:
            points = points.astype(np.float64)
        right_foot = self.get_right_foot(points)
        return right_foot

    @property
    def left_foot_abs(self) -> List[float]:
        points = self.detection.absolute_points  # type: ignore
        if not isinstance(points, np.ndarray):
            points = np.array(points, dtype=np.float64)
        else:
            points = points.astype(np.float64)
        left_foot_abs = self.get_left_foot(points)
        return left_foot_abs

    @property
    def right_foot_abs(self) -> NDArray[np.float64]:
        points = self.detection.absolute_points  # type: ignore
        if not isinstance(points, np.ndarray):
            points = np.array(points, dtype=np.float64)
        else:
            points = points.astype(np.float64)
        right_foot_abs = self.get_right_foot(points)
        return right_foot_abs

    @property
    def feet(self) -> NDArray[np.float64]:
        return np.array([self.left_foot, self.right_foot], dtype=np.float64)

    def distance_to_ball(self, ball: Ball) -> Optional[float]:
        """
        Returns the distance between the player closest foot and the ball

        Parameters
        ----------
        ball : Ball
            Ball object

        Returns
        -------
        Optional[float]
            Distance between the player closest foot and the ball
        """

        if ball.center is None:
            return None

        left_foot_distance = np.linalg.norm(np.array(ball.center) - np.array(self.left_foot))
        right_foot_distance = np.linalg.norm(np.array(ball.center) - self.right_foot)

        return float(min(left_foot_distance, right_foot_distance))

    def closest_foot_to_ball(self, ball: Ball) -> Optional[NDArray[np.float64]]:
        """

        Returns the closest foot to the ball

        Parameters
        ----------
        ball : Ball
            Ball object

        Returns
        -------
        Optional[NDArray[np.float64]]
            Closest foot to the ball (x, y)
        """

        if ball.center is None:
            return None

        left_foot_distance = np.linalg.norm(np.array(ball.center) - np.array(self.left_foot))
        right_foot_distance = np.linalg.norm(np.array(ball.center) - np.array(self.right_foot))

        if left_foot_distance < right_foot_distance:
            return np.array(self.left_foot, dtype=np.float64)

        return self.right_foot

    def closest_foot_to_ball_abs(self, ball: Ball) -> Optional[NDArray[np.float64]]:
        """

        Returns the closest foot to the ball

        Parameters
        ----------
        ball : Ball
            Ball object

        Returns
        -------
        Optional[NDArray[np.float64]]
            Closest foot to the ball (x, y)
        """

        if ball.center_abs is None:
            return None

        left_foot_distance = np.linalg.norm(np.array(ball.center_abs) - np.array(self.left_foot_abs))
        right_foot_distance = np.linalg.norm(np.array(ball.center_abs) - np.array(self.right_foot_abs))

        if left_foot_distance < right_foot_distance:
            return np.array(self.left_foot_abs, dtype=np.float64)

        return self.right_foot_abs

    def draw(
        self, frame: PIL.Image.Image, confidence: bool = False, id: bool = False
    ) -> PIL.Image.Image:
        """
        Draw the player on the frame

        Parameters
        ----------
        frame : PIL.Image.Image
            Frame to draw on
        confidence : bool, optional
            Whether to draw confidence text in bounding box, by default False
        id : bool, optional
            Whether to draw id text in bounding box, by default False

        Returns
        -------
        PIL.Image.Image
            Frame with player drawn
        """
        if self.team is not None:
            self.detection.data["color"] = self.team.color

        # Extract position and size from detection points
        points = self.detection.points  # type: ignore
        if not isinstance(points, np.ndarray):
            points = np.array(points, dtype=np.float64)
        else:
            points = points.astype(np.float64)
        
        x = float(points[0][0])
        y = float(points[0][1])
        width = float(points[1][0] - points[0][0])
        height = float(points[1][1] - points[0][1])
        
        # Use team color if available, otherwise default green
        color = self.team.color if self.team is not None else (0, 255, 0)

        return Draw.draw_detection(frame, x, y, width, height, color)

    def __str__(self) -> str:
        return f"Player: {self.feet}, team: {self.team}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False

        self_id = self.detection.data["id"]
        other_id = other.detection.data["id"]

        return bool(self_id == other_id)

    @staticmethod
    def have_same_id(player1: Optional["Player"], player2: Optional["Player"]) -> bool:
        """
        Check if player1 and player2 have the same ids

        Parameters
        ----------
        player1 : Optional[Player]
            One player
        player2 : Optional[Player]
            Another player

        Returns
        -------
        bool
            True if they have the same id
        """
        if not player1 or not player2:
            return False
        if "id" not in player1.detection.data or "id" not in player2.detection.data:
            return False
        return player1 == player2

    @staticmethod
    def draw_players(
        players: List["Player"],
        frame: PIL.Image.Image,
        confidence: bool = False,
        id: bool = False,
    ) -> PIL.Image.Image:
        """
        Draw all players on the frame

        Parameters
        ----------
        players : List[Player]
            List of Player objects
        frame : PIL.Image.Image
            Frame to draw on
        confidence : bool, optional
            Whether to draw confidence text in bounding box, by default False
        id : bool, optional
            Whether to draw id text in bounding box, by default False

        Returns
        -------
        PIL.Image.Image
            Frame with players drawn
        """
        for player in players:
            frame = player.draw(frame, confidence=confidence, id=id)

        return frame

    @staticmethod
    def from_detections(
        detections: List[Detection], teams: Optional[List[Team]] = None
    ) -> List["Player"]:
        """
        Create a list of Player objects from a list of detections and a list of teams.

        It reads the classification string field of the detection, converts it to a
        Team object and assigns it to the player.

        Parameters
        ----------
        detections : List[Detection]
            List of detections
        teams : Optional[List[Team]], optional
            List of teams, by default None

        Returns
        -------
        List[Player]
            List of Player objects
        """
        if teams is None:
            teams = []
            
        players: List[Player] = []

        for detection in detections:
            if "classification" in detection.data:
                team_name = detection.data["classification"]
                team = Team.from_name(teams=teams, name=team_name)
                detection.data["team"] = team

            player = Player(detection=detection)
            players.append(player)

        return players
