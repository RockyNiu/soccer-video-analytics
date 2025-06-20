from typing import List, Tuple, Optional, Any
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont


RGB = Tuple[int, int, int]
RGBA = Tuple[int, int, int, int]
Point = Tuple[int, int]


class Draw:
    @staticmethod
    def draw_rectangle(
        img: Image.Image,
        origin: Point,
        width: int,
        height: int,
        color: RGB,
        thickness: int = 2,
    ) -> Image.Image:
        """Draw a rectangle on the image."""
        draw = ImageDraw.Draw(img)
        rectangle = [
            origin,
            (origin[0] + width, origin[1] + height),
        ]
        draw.rectangle(rectangle, outline=color, width=thickness)
        return img

    @staticmethod
    def draw_text(
        img: Image.Image,
        origin: Point,
        text: str,
        font: Optional[FreeTypeFont] = None,
        color: RGB = (255, 255, 255),
    ) -> Image.Image:
        """Draw text on the image."""
        draw = ImageDraw.Draw(img)
        if font is None:
            font = ImageFont.truetype("fonts/Gidole-Regular.ttf", size=20)
        draw.text(origin, text, font=font, fill=color)
        return img

    @staticmethod
    def draw_bounding_box(
        img: Image.Image,
        rectangle: List[Point],
        color: RGB = (0, 255, 0),
        thickness: int = 3
    ) -> Image.Image:
        """Draw a bounding box on the image."""
        draw = ImageDraw.Draw(img, "RGBA")
        points = [(x, y) for x, y in rectangle]  # Ensure points are tuples
        draw.rounded_rectangle(points, radius=7, outline=color, width=thickness)
        return img

    @staticmethod
    def draw_detection(
        img: Image.Image,
        x: float,
        y: float,
        width: float,
        height: float,
        color: RGB = (0, 255, 0),
    ) -> Image.Image:
        """Draw a detection box on the image."""
        points = [
            (int(x), int(y)),
            (int(x + width), int(y + height))
        ]
        return Draw.draw_bounding_box(img=img, rectangle=points, color=color)

    @staticmethod
    def half_rounded_rectangle(
        img: Image.Image,
        rectangle: Any,
        color: RGB,
        radius: int = 15,
        left: bool = False,
    ) -> Image.Image:
        """Draw a half-rounded rectangle on the image."""
        draw = ImageDraw.Draw(img)
        
        # Convert rectangle to proper format
        if hasattr(rectangle, '__len__') and len(rectangle) == 2:
            if hasattr(rectangle[1], '__len__'):
                # Handle list/tuple in rectangle[1]
                if isinstance(rectangle[1], (list, tuple)) and len(rectangle[1]) >= 2:
                    rect_coords = (rectangle[0][0], rectangle[0][1], rectangle[1][0], rectangle[1][1])
                else:
                    rect_coords = (rectangle[0][0], rectangle[0][1], rectangle[1][0], rectangle[1][1])
            else:
                rect_coords = (rectangle[0][0], rectangle[0][1], rectangle[1][0], rectangle[1][1])
        else:
            # Fallback - assume it's already in the right format
            rect_coords = rectangle
        
        # Validate coordinates to prevent PIL errors
        x1, y1, x2, y2 = rect_coords
        
        # Convert to integers
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        
        if x2 <= x1:
            x2 = x1 + 1  # Ensure positive width
        if y2 <= y1:
            y2 = y1 + 1  # Ensure positive height
        
        rect_coords = (x1, y1, x2, y2)
        
        if left:
            # Left rounded corners only
            try:
                draw.rounded_rectangle(rect_coords, radius=radius, fill=color, corners=(True, False, False, True))
            except ValueError:
                # Fallback to simple rectangle
                draw.rectangle(rect_coords, fill=color)
        else:
            # Right rounded corners only  
            try:
                draw.rounded_rectangle(rect_coords, radius=radius, fill=color, corners=(False, True, True, False))
            except ValueError:
                # Fallback to simple rectangle
                draw.rectangle(rect_coords, fill=color)
        
        return img

    @staticmethod
    def add_alpha(img: Image.Image, alpha: int) -> Image.Image:
        """Add alpha transparency to an image."""
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create alpha mask
        alpha_mask = Image.new('L', img.size, alpha)
        img.putalpha(alpha_mask)
        
        return img

    @staticmethod
    def text_in_middle_rectangle(
        img: Image.Image,
        origin: Any,
        width: int,
        height: int,
        text: str,
        color: RGB = (255, 255, 255),
        font: Optional[FreeTypeFont] = None,
    ) -> Image.Image:
        """Draw text centered in a rectangle."""
        draw = ImageDraw.Draw(img)
        
        if font is None:
            font = ImageFont.truetype("fonts/Gidole-Regular.ttf", size=16)
        
        # Convert origin to tuple if it's a list
        if isinstance(origin, list):
            origin = (origin[0], origin[1])
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate center position
        x = origin[0] + (width - text_width) // 2
        y = origin[1] + (height - text_height) // 2
        
        draw.text((x, y), text, font=font, fill=color)
        return img


class PathPoint:
    """Represents a point in a path with color and alpha."""
    def __init__(self, id: int, center: Point, color: RGB = (255, 255, 255), alpha: float = 1.0):
        self.id = id
        self.center = center
        self.color = color
        self.alpha = alpha

    @property
    def color_with_alpha(self) -> RGBA:
        """Get color with alpha channel."""
        return (self.color[0], self.color[1], self.color[2], int(self.alpha * 255))

    @staticmethod
    def get_center_from_bounding_box(bounding_box: Any) -> Point:
        """Get center point from bounding box."""
        x1, y1 = bounding_box[0]
        x2, y2 = bounding_box[1]
        return (int((x1 + x2) / 2), int((y1 + y2) / 2))

    @classmethod
    def from_abs_bbox(cls, id: int, abs_point: Any, coord_transformations: Any, color: Optional[RGB] = None, alpha: Optional[float] = None) -> 'PathPoint':
        """Create PathPoint from absolute bounding box."""
        if color is None:
            color = (255, 255, 255)
        if alpha is None:
            alpha = 1.0
        
        # For now, assume abs_point is already in relative coordinates
        center = cls.get_center_from_bounding_box(abs_point)
        return cls(id=id, center=center, color=color, alpha=alpha)


class AbsolutePath:
    """Manages a path with absolute coordinates."""
    def __init__(self):
        self.past_points: List[Any] = []
        self.color_by_index: dict[int, RGB] = {}

    def add_new_point(self, detection: Any, color: RGB = (255, 255, 255)) -> None:
        """Add a new point to the path."""
        if detection is None:
            return
        
        # For now, assume detection has an absolute_points attribute
        if hasattr(detection, 'absolute_points'):
            self.past_points.append(detection.absolute_points)
        else:
            # Fallback: use detection points directly
            self.past_points.append(detection.points if hasattr(detection, 'points') else detection)
        
        self.color_by_index[len(self.past_points) - 1] = color

    def __len__(self) -> int:
        """Get the number of points in the path."""
        return len(self.past_points)

    def filter_points_outside_frame(self, points: List[PathPoint], width: int, height: int, margin: int = 0) -> List[PathPoint]:
        """Filter out points that are outside the frame."""
        return [
            point for point in points
            if (point.center[0] > 0 - margin
                and point.center[1] > 0 - margin
                and point.center[0] < width + margin
                and point.center[1] < height + margin)
        ]

    def draw_path_slow(self, img: Image.Image, path: List[PathPoint], thickness: int = 4) -> Image.Image:
        """Draw path with individual line segments."""
        draw = ImageDraw.Draw(img, "RGBA")
        
        for i in range(len(path) - 1):
            draw.line(
                [path[i].center, path[i + 1].center],
                fill=path[i].color_with_alpha,
                width=thickness
            )
        return img

    def draw_path_arrows(self, img: Image.Image, path: List[PathPoint], thickness: int = 4, frame_frequency: int = 30) -> Image.Image:
        """Draw path with arrows indicating direction."""
        # For simplicity, just draw the path without arrows for now
        return self.draw_path_slow(img, path, thickness)

    def draw_arrow(
        self,
        img: Image.Image,
        points: List[PathPoint],
        color: RGB = (255, 255, 255),
        width: int = 4,
        alpha: int = 255,
    ) -> Image.Image:
        """Draw an arrow between points."""
        if len(points) < 2:
            return img
        
        draw = ImageDraw.Draw(img, "RGBA")
        
        # Convert color to RGBA with alpha
        arrow_color = (color[0], color[1], color[2], alpha)
        
        # Draw line between points
        start_point = points[0].center
        end_point = points[-1].center
        
        draw.line([start_point, end_point], fill=arrow_color, width=width)
        
        # Draw arrowhead
        import math
        arrow_size = width * 2
        
        # Calculate arrow direction
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        
        if dx == 0 and dy == 0:
            return img
            
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return img
            
        # Normalize direction
        dx = dx / length
        dy = dy / length
        
        # Calculate arrowhead points
        arrow_angle = math.pi / 6  # 30 degrees
        
        # Left arrowhead point
        left_x = end_point[0] - arrow_size * (dx * math.cos(arrow_angle) - dy * math.sin(arrow_angle))
        left_y = end_point[1] - arrow_size * (dy * math.cos(arrow_angle) + dx * math.sin(arrow_angle))
        
        # Right arrowhead point  
        right_x = end_point[0] - arrow_size * (dx * math.cos(-arrow_angle) - dy * math.sin(-arrow_angle))
        right_y = end_point[1] - arrow_size * (dy * math.cos(-arrow_angle) + dx * math.sin(-arrow_angle))
        
        # Draw arrowhead
        arrow_points = [
            (int(left_x), int(left_y)),
            end_point,
            (int(right_x), int(right_y))
        ]
        
        draw.line([arrow_points[0], arrow_points[1]], fill=arrow_color, width=width)
        draw.line([arrow_points[1], arrow_points[2]], fill=arrow_color, width=width)
        
        return img

    def draw(
        self,
        img: Image.Image,
        detection: Any,
        coord_transformations: Any,
        color: RGB = (255, 255, 255),
    ) -> Image.Image:
        """Draw the complete path on the image."""
        self.add_new_point(detection=detection, color=color)
        
        if len(self.past_points) < 2:
            return img

        # Convert past points to PathPoint objects
        path = [
            PathPoint.from_abs_bbox(
                id=i,
                abs_point=point,
                coord_transformations=coord_transformations,
                color=self.color_by_index[i],
                alpha=1.0 - (i / len(self.past_points)) * 0.5  # Fade older points
            )
            for i, point in enumerate(self.past_points)
        ]

        # Filter points outside frame
        path_filtered = self.filter_points_outside_frame(
            points=path,
            width=img.size[0] if hasattr(img, 'size') else 1920,
            height=img.size[1] if hasattr(img, 'size') else 1080,
        )

        # Draw the path
        img = self.draw_path_slow(img=img, path=path_filtered)
        img = self.draw_path_arrows(img=img, path=path)
        return img
