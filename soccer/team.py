from typing import List, Optional, TYPE_CHECKING
from soccer.draw import RGB

if TYPE_CHECKING:
    from soccer.player import Player
    from soccer.pass_event import Pass


class Team:
    def __init__(
        self,
        name: str,
        id: Optional[int] = None,
        color: RGB = (0, 0, 0),
        abbreviation: str = "NNN",
        board_color: Optional[RGB] = None,
        text_color: RGB = (0, 0, 0),
    ):
        """
        Initialize Team

        Parameters
        ----------
        name : str
            Team name
        id : int, optional
            Team ID
        color : RGB, optional
            Team color, by default (0, 0, 0)
        abbreviation : str, optional
            Team abbreviation, by default "NNN"
        board_color : RGB, optional
            Board color for the team, by default None
        text_color : RGB, optional
            Text color for the team, by default (0, 0, 0)
        """
        self.name = name
        self.id = id
        self.color = color
        self.abbreviation = abbreviation
        self.board_color = board_color if board_color is not None else color
        self.text_color = text_color
        self.players: List["Player"] = []
        self.possession: int = 0
        self.passes: List["Pass"] = []

        if len(abbreviation) != 3 or not abbreviation.isupper():
            raise ValueError("abbreviation must be length 3 and uppercase")

    def get_percentage_possession(self, duration: int) -> float:
        """
        Return team possession in percentage

        Parameters
        ----------
        duration : int
            Match duration in frames

        Returns
        -------
        float
            Team possession in percentage
        """
        if duration == 0:
            return 0
        return round(self.possession / duration, 2)

    def get_time_possession(self, fps: int) -> str:
        """
        Return team possession in time format

        Parameters
        ----------
        fps : int
            Frames per second

        Returns
        -------
        str
            Team possession in time format (mm:ss)
        """

        seconds = round(self.possession / fps)
        minutes = seconds // 60
        seconds = seconds % 60

        # express seconds in 2 digits
        seconds = str(seconds)
        if len(seconds) == 1:
            seconds = "0" + seconds

        # express minutes in 2 digits
        minutes = str(minutes)
        if len(minutes) == 1:
            minutes = "0" + minutes

        return f"{minutes}:{seconds}"

    def __str__(self):
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Team):
            return False

        return self.name == other.name

    @staticmethod
    def from_name(teams: List["Team"], name: str) -> Optional["Team"]:
        """
        Return team object from name

        Parameters
        ----------
        teams : List[Team]
            List of Team objects
        name : str
            Team name

        Returns
        -------
        Optional[Team]
            Team object or None if not found
        """
        for team in teams:
            if team.name == name:
                return team
        return None
