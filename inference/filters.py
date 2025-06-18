from typing import List, TypedDict
from .box import Box
from .colors import HSVColor, black, blue, green, sky_blue


class TeamFilter(TypedDict):
    name: str
    colors: List[HSVColor]


chelsea_filter: TeamFilter = {
    "name": "Chelsea",
    "colors": [blue, green],
}

city_filter: TeamFilter = {
    "name": "Man City",
    "colors": [sky_blue],
}

referee_filter: TeamFilter = {
    "name": "Referee",
    "colors": [black],
}

filters: List[TeamFilter] = [
    chelsea_filter,
    city_filter,
    referee_filter,
]


def filter_boxes_by_area(boxes: List[Box], min_area: float = 1000) -> List[Box]:
    """
    Filter boxes based on their area

    Parameters
    ----------
    boxes : List[Box]
        List of boxes to filter
    min_area : float, optional
        Minimum area threshold, by default 1000

    Returns
    -------
    List[Box]
        List of boxes with area >= min_area
    """
    return [box for box in boxes if box.area >= min_area]


def filter_boxes_by_overlap(boxes: List[Box], iou_threshold: float = 0.5) -> List[Box]:
    """
    Filter boxes based on their overlap (IoU)

    Parameters
    ----------
    boxes : List[Box]
        List of boxes to filter
    iou_threshold : float, optional
        IoU threshold for filtering, by default 0.5

    Returns
    -------
    List[Box]
        List of boxes after removing overlapping boxes
    """
    if not boxes:
        return []

    # Sort boxes by area in descending order
    sorted_boxes = sorted(boxes, key=lambda x: x.area, reverse=True)
    kept_boxes = [sorted_boxes[0]]

    # Compare each box with previously kept boxes
    for box in sorted_boxes[1:]:
        should_keep = True
        for kept_box in kept_boxes:
            if box.iou(kept_box) > iou_threshold:
                should_keep = False
                break
        if should_keep:
            kept_boxes.append(box)

    return kept_boxes
