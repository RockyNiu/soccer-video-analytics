import pytest
import numpy as np
from norfair import Detection  # type: ignore
from soccer.team import Team
from soccer.player import Player
from soccer.ball import Ball
from inference.box import Box

@pytest.fixture
def team_a() -> Team:
    return Team(name="Team A", id=1)

@pytest.fixture
def team_b() -> Team:
    return Team(name="Team B", id=2)

@pytest.fixture
def player_a(team_a: Team) -> Player:
    # Create norfair Detection with proper format
    detection = Detection(
        points=np.array([[200, 200], [250, 300]]),  # [xmin, ymin], [xmax, ymax]
        data={"name": "person", "p": 0.9, "team": team_a}
    )
    return Player(detection=detection)

@pytest.fixture
def player_b(team_b: Team) -> Player:
    # Create norfair Detection with proper format  
    detection = Detection(
        points=np.array([[300, 200], [350, 300]]),  # [xmin, ymin], [xmax, ymax]
        data={"name": "person", "p": 0.9, "team": team_b}
    )
    return Player(detection=detection)

@pytest.fixture
def ball() -> Ball:
    return Ball(box=Box(x=100, y=100, width=20, height=20))
