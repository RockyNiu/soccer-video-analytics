import pytest
from inference.box import Box
from inference.filters import BoxFilter


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
        filtered = BoxFilter.filter_by_area(sample_boxes)
        # Only boxes with area >= 1000 should remain (first and third boxes)
        assert len(filtered) == 2
        assert all(box.area >= 1000 for box in filtered)
    
    def test_filter_by_area_custom_threshold(self, sample_boxes: list[Box]):
        """Test area filtering with custom threshold"""
        filtered = BoxFilter.filter_by_area(sample_boxes, min_area=500)
        # Boxes with area >= 500 should remain (first three boxes)
        assert len(filtered) == 3
        assert all(box.area >= 500 for box in filtered)
    
    def test_filter_by_area_high_threshold(self, sample_boxes: list[Box]):
        """Test area filtering with high threshold"""
        filtered = BoxFilter.filter_by_area(sample_boxes, min_area=3000)
        # No boxes should remain
        assert len(filtered) == 0
    
    def test_filter_by_overlap_default_threshold(self, sample_boxes: list[Box]):
        """Test overlap filtering with default threshold"""
        filtered = BoxFilter.filter_by_overlap(sample_boxes)
        # Should remove one of the overlapping boxes
        assert len(filtered) == 3
    
    def test_filter_by_overlap_strict_threshold(self, sample_boxes: list[Box]):
        """Test overlap filtering with strict threshold"""
        filtered = BoxFilter.filter_by_overlap(sample_boxes, iou_threshold=0.1)
        # With very low threshold, should remove overlapping boxes
        assert len(filtered) == 3
    
    def test_filter_by_overlap_permissive_threshold(self, sample_boxes: list[Box]):
        """Test overlap filtering with permissive threshold"""
        filtered =  BoxFilter.filter_by_overlap(sample_boxes, iou_threshold=0.99)
        # With very high threshold, should keep all boxes
        assert len(filtered) == 4
    
    def test_filter_empty_list(self):
        """Test filtering empty list"""
        assert  BoxFilter.filter_by_overlap([]) == []
        assert  BoxFilter.filter_by_overlap([]) == []
    
    def test_filter_single_box(self):
        """Test filtering single box"""
        box = Box(x=0, y=0, width=10, height=10)
        assert  BoxFilter.filter_by_overlap([box], iou_threshold=50) == [box]
        assert  BoxFilter.filter_by_overlap([box]) == [box]
