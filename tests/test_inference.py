import pytest
from inference.box import Box
from inference.filters import filter_boxes_by_area, filter_boxes_by_overlap

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


class TestFilters:
    """Test the filter functions"""
    
    @pytest.fixture
    def sample_boxes(self):
        """Create sample boxes for testing"""
        return [
            Box(x=100, y=100, width=50, height=50),  # area = 2500
            Box(x=200, y=200, width=30, height=30),  # area = 900
            Box(x=101, y=101, width=48, height=48),  # area = 2304, overlaps with first
            Box(x=300, y=300, width=10, height=10),  # area = 100
        ]
    
    def test_filter_by_area_default_threshold(self, sample_boxes: list[Box]):
        """Test area filtering with default threshold"""
        filtered = filter_boxes_by_area(sample_boxes)
        # Only boxes with area >= 1000 should remain (first and third boxes)
        assert len(filtered) == 2
        assert all(box.area >= 1000 for box in filtered)
    
    def test_filter_by_area_custom_threshold(self, sample_boxes: list[Box]):
        """Test area filtering with custom threshold"""
        filtered = filter_boxes_by_area(sample_boxes, min_area=500)
        # Boxes with area >= 500 should remain (first three boxes)
        assert len(filtered) == 3
        assert all(box.area >= 500 for box in filtered)
    
    def test_filter_by_area_high_threshold(self, sample_boxes: list[Box]):
        """Test area filtering with high threshold"""
        filtered = filter_boxes_by_area(sample_boxes, min_area=3000)
        # No boxes should remain
        assert len(filtered) == 0
    
    def test_filter_by_overlap_default_threshold(self, sample_boxes: list[Box]):
        """Test overlap filtering with default threshold"""
        filtered = filter_boxes_by_overlap(sample_boxes)
        # Should remove one of the overlapping boxes
        assert len(filtered) == 3
    
    def test_filter_by_overlap_strict_threshold(self, sample_boxes: list[Box]):
        """Test overlap filtering with strict threshold"""
        filtered = filter_boxes_by_overlap(sample_boxes, iou_threshold=0.1)
        # With very low threshold, should remove overlapping boxes
        assert len(filtered) == 3
    
    def test_filter_by_overlap_permissive_threshold(self, sample_boxes: list[Box]):
        """Test overlap filtering with permissive threshold"""
        filtered = filter_boxes_by_overlap(sample_boxes, iou_threshold=0.99)
        # With very high threshold, should keep all boxes
        assert len(filtered) == 4
    
    def test_filter_empty_list(self):
        """Test filtering empty list"""
        assert filter_boxes_by_area([]) == []
        assert filter_boxes_by_overlap([]) == []
    
    def test_filter_single_box(self):
        """Test filtering single box"""
        box = Box(x=0, y=0, width=10, height=10)
        assert filter_boxes_by_area([box], min_area=50) == [box]
        assert filter_boxes_by_overlap([box]) == [box]
