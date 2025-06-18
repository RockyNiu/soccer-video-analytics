import unittest
from soccer.team import Team

class TestTeam(unittest.TestCase):
    def setUp(self):
        self.team = Team(id=1, name="Team A")
        
    def test_team_initialization(self):
        self.assertEqual(self.team.id, 1)
        self.assertEqual(self.team.name, "Team A")
        
    def test_team_players(self):
        self.assertEqual(len(self.team.players), 0)

if __name__ == '__main__':
    unittest.main()
