import pytest
from inference.box import Box


class TestBox:
    """Test the Box class functionality"""
    
    def test_box_initialization(self):
        """Test box creation with different parameters"""
        box = Box(x=10, y=20, width=30, height=40)
        assert box.x == 10
        assert box.y == 20
        assert box.width == 30
        assert box.height == 40
    
    def test_box_area(self):
        """Test area calculation"""
        box = Box(x=0, y=0, width=10, height=20)
        assert box.area == 200
    
    def test_box_points(self):
        """Test points property"""
        box = Box(x=10, y=20, width=30, height=40)
        points = box.points
        assert points == [(10, 20), (40, 60)]
    
    def test_box_iou_no_overlap(self):
        """Test IoU calculation with no overlap"""
        box1 = Box(x=0, y=0, width=10, height=10)
        box2 = Box(x=20, y=20, width=10, height=10)
        assert box1.iou(box2) == 0.0
    
    def test_box_iou_full_overlap(self):
        """Test IoU calculation with full overlap"""
        box1 = Box(x=0, y=0, width=10, height=10)
        box2 = Box(x=0, y=0, width=10, height=10)
        assert box1.iou(box2) == 1.0
    
    def test_box_iou_partial_overlap(self):
        """Test IoU calculation with partial overlap"""
        box1 = Box(x=0, y=0, width=10, height=10)
        box2 = Box(x=5, y=5, width=10, height=10)
        # Intersection: 5x5 = 25, Union: 100 + 100 - 25 = 175
        expected_iou = 25 / 175
        assert abs(box1.iou(box2) - expected_iou) < 1e-6
