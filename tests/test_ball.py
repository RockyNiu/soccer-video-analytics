import unittest
from soccer.ball import Ball
from inference.box import Box

class TestBall(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(box=Box(x=100, y=100, width=20, height=20))
        
    def test_ball_initialization(self):
        assert self.ball.box is not None
        self.assertEqual(self.ball.box.x, 100)
        self.assertEqual(self.ball.box.y, 100)
        self.assertEqual(self.ball.box.width, 20)
        self.assertEqual(self.ball.box.height, 20)
        
    def test_ball_position(self):
        self.assertEqual(self.ball.position, (100, 100))

if __name__ == '__main__':
    unittest.main()
