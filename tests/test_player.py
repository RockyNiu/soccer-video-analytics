import unittest
import numpy as np
from norfair import Detection  # type: ignore
from soccer.player import Player
from soccer.team import Team

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.team = Team(id=1, name="Team A")
        # Create a Detection object with points representing a bounding box
        points = np.array([[200, 200], [250, 300]])  # Top-left and bottom-right corners
        detection_data = {"team": self.team}
        self.detection = Detection(points=points, data=detection_data)
        self.player = Player(detection=self.detection)
        
    def test_player_initialization(self):
        self.assertIsNotNone(self.player.detection)
        self.assertIsNotNone(self.player.team)
        assert self.player.team is not None  # Type guard for mypy
        self.assertEqual(self.player.team.name, "Team A")
        # Cast detection points to avoid type checker issues
        expected_points = np.array([[200, 200], [250, 300]])
        np.testing.assert_array_equal(np.asarray(self.player.detection.points), expected_points)  # type: ignore
        
    def test_player_position(self):
        # Test that we can access the left and right foot properties
        left_foot = self.player.left_foot
        right_foot = self.player.right_foot  # type: ignore
        self.assertIsNotNone(left_foot)
        self.assertIsNotNone(right_foot)  # type: ignore
        # Left foot should be [200, 300] (x1, y2)
        self.assertEqual(left_foot, [200.0, 300.0])
        # Right foot should be [250, 300] (x2, y2)
        # Cast to avoid type checker issues with norfair types
        expected_right_foot = np.array([250, 300])
        np.testing.assert_array_equal(np.asarray(right_foot), expected_right_foot)  # type: ignore