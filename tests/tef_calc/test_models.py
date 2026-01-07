"""
Tests for core data models: Point, Circle, Intersection, InfiniteLine, SVGScene
"""

import pytest
import math
from tef_calc.models import Point, Circle, Intersection, InfiniteLine, SVGScene


class TestPoint:
    """Test Point model"""

    def test_create_point_and_compute_distance(self):
        """Test case: create_point_and_compute_distance"""
        p1 = Point(x=0, y=0)
        p2 = Point(x=3, y=4)
        
        # Verify distance calculation (3-4-5 triangle)
        distance = p1.distance_to(p2)
        assert distance == 5
        
        # Verify immutability
        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            p1.x = 10

    def test_point_immutable(self):
        """Test that Point is frozen (immutable)"""
        p = Point(x=1, y=2)
        with pytest.raises((AttributeError, Exception)):
            p.x = 5

    def test_point_hashable(self):
        """Test that Point is hashable (can be used in sets/dicts)"""
        p1 = Point(x=1, y=2)
        p2 = Point(x=1, y=2)
        p3 = Point(x=3, y=4)
        
        # Should be hashable
        point_set = {p1, p2, p3}
        assert len(point_set) == 2  # p1 and p2 are equal
        
        # Should work as dict key
        point_dict = {p1: "first", p3: "third"}
        assert point_dict[p2] == "first"

    def test_point_distance_to_self(self):
        """Test distance from point to itself is 0"""
        p = Point(x=5, y=5)
        assert p.distance_to(p) == 0

    def test_point_midpoint(self):
        """Test midpoint calculation"""
        p1 = Point(x=0, y=0)
        p2 = Point(x=4, y=4)
        
        mid = p1.midpoint(p2)
        assert mid.x == 2
        assert mid.y == 2

    def test_point_midpoint_with_floats(self):
        """Test midpoint with float coordinates"""
        p1 = Point(x=1.5, y=2.5)
        p2 = Point(x=3.5, y=4.5)
        
        mid = p1.midpoint(p2)
        assert mid.x == 2.5
        assert mid.y == 3.5


class TestCircle:
    """Test Circle model"""

    def test_create_circle_and_compute_properties(self):
        """Test case: create_circle_and_compute_properties"""
        center = Point(x=0, y=0)
        circle = Circle(center=center, radius=5)
        
        # Verify area (π * r²)
        expected_area = math.pi * 5 * 5
        assert abs(circle.area() - expected_area) < 0.01
        assert abs(circle.area() - 78.54) < 0.01
        
        # Verify diameter
        assert circle.diameter() == 10
        
        # Verify radius is positive
        assert circle.radius > 0

    def test_circle_immutable(self):
        """Test that Circle is frozen (immutable)"""
        c = Circle(center=Point(0, 0), radius=5)
        with pytest.raises((AttributeError, Exception)):
            c.radius = 10

    def test_circle_hashable(self):
        """Test that Circle is hashable"""
        c1 = Circle(center=Point(0, 0), radius=5)
        c2 = Circle(center=Point(0, 0), radius=5)
        c3 = Circle(center=Point(1, 1), radius=3)
        
        circle_set = {c1, c2, c3}
        assert len(circle_set) == 2  # c1 and c2 are equal

    def test_circle_contains_point(self):
        """Test point containment in circle"""
        center = Point(x=0, y=0)
        circle = Circle(center=center, radius=5)
        
        # Point at center
        assert circle.contains(center)
        
        # Point inside
        p_inside = Point(x=3, y=0)
        assert circle.contains(p_inside)
        
        # Point on boundary (approximately)
        p_boundary = Point(x=5, y=0)
        assert circle.contains(p_boundary)
        
        # Point outside
        p_outside = Point(x=10, y=0)
        assert not circle.contains(p_outside)

    def test_circle_intersects(self):
        """Test circle-circle intersection detection"""
        c1 = Circle(center=Point(0, 0), radius=5)
        
        # Overlapping circles
        c2 = Circle(center=Point(3, 0), radius=5)
        assert c1.intersects(c2)
        
        # Non-overlapping circles
        c3 = Circle(center=Point(20, 0), radius=5)
        assert not c1.intersects(c3)
        
        # Tangent circles (touching)
        c4 = Circle(center=Point(10, 0), radius=5)
        assert c1.intersects(c4)
        
        # One circle inside another
        c5 = Circle(center=Point(0, 0), radius=2)
        assert c1.intersects(c5)


class TestInfiniteLine:
    """Test InfiniteLine model"""

    def test_create_infinite_line_and_compute_slope(self):
        """Test case: create_infinite_line_and_compute_slope"""
        p1 = Point(x=0, y=0)
        p2 = Point(x=1, y=1)
        
        line = InfiniteLine(point1=p1, point2=p2)
        
        # Verify not vertical
        assert not line.is_vertical()
        
        # Verify slope is 1
        assert line.slope() == 1

    def test_line_immutable(self):
        """Test that InfiniteLine is frozen (immutable)"""
        line = InfiniteLine(point1=Point(0, 0), point2=Point(1, 1))
        with pytest.raises((AttributeError, Exception)):
            line.point1 = Point(5, 5)

    def test_line_hashable(self):
        """Test that InfiniteLine is hashable"""
        line1 = InfiniteLine(point1=Point(0, 0), point2=Point(1, 1))
        line2 = InfiniteLine(point1=Point(0, 0), point2=Point(1, 1))
        line3 = InfiniteLine(point1=Point(0, 0), point2=Point(2, 1))
        
        line_set = {line1, line2, line3}
        assert len(line_set) == 2

    def test_line_vertical(self):
        """Test vertical line detection"""
        # Vertical line
        vertical = InfiniteLine(point1=Point(5, 0), point2=Point(5, 10))
        assert vertical.is_vertical()

    def test_line_slope_negative(self):
        """Test negative slope"""
        line = InfiniteLine(point1=Point(0, 5), point2=Point(5, 0))
        assert line.slope() == -1

    def test_line_slope_zero(self):
        """Test zero slope (horizontal line)"""
        line = InfiniteLine(point1=Point(0, 5), point2=Point(10, 5))
        assert line.slope() == 0

    def test_line_point_at(self):
        """Test point_at() method for finding points on the line"""
        # Line y = x
        line = InfiniteLine(point1=Point(0, 0), point2=Point(1, 1))
        
        # Get point at x=5
        p = line.point_at(5)
        assert p.x == 5
        assert p.y == 5
        
    def test_line_point_at_vertical(self):
        """Test point_at() for vertical line"""
        # Vertical line at x=5
        line = InfiniteLine(point1=Point(5, 0), point2=Point(5, 10))
        
        # Get point at y=7
        p = line.point_at_y(7)
        assert p.x == 5
        assert p.y == 7


class TestIntersection:
    """Test Intersection model"""

    def test_intersection_creation(self):
        """Test creating an Intersection"""
        c1 = Circle(center=Point(0, 0), radius=5)
        c2 = Circle(center=Point(3, 0), radius=5)
        points = [Point(1.5, 2), Point(1.5, -2)]
        
        intersection = Intersection(circle1=c1, circle2=c2, points=points)
        
        assert intersection.circle1 == c1
        assert intersection.circle2 == c2
        assert len(intersection.points) == 2

    def test_intersection_immutable(self):
        """Test that Intersection is frozen"""
        c1 = Circle(center=Point(0, 0), radius=5)
        c2 = Circle(center=Point(3, 0), radius=5)
        
        intersection = Intersection(circle1=c1, circle2=c2, points=[])
        
        with pytest.raises((AttributeError, Exception)):
            intersection.circle1 = None

    def test_intersection_hashable(self):
        """Test that Intersection is hashable"""
        c1 = Circle(center=Point(0, 0), radius=5)
        c2 = Circle(center=Point(3, 0), radius=5)
        
        int1 = Intersection(circle1=c1, circle2=c2, points=[Point(0, 0)])
        int2 = Intersection(circle1=c1, circle2=c2, points=[Point(0, 0)])
        
        intersection_set = {int1, int2}
        assert len(intersection_set) == 1


class TestSVGScene:
    """Test SVGScene model"""

    def test_svg_scene_creation(self):
        """Test creating an SVGScene"""
        circles = [
            Circle(center=Point(0, 0), radius=5),
            Circle(center=Point(10, 10), radius=3)
        ]
        points = [Point(0, 0), Point(5, 5)]
        intersections = []
        lines = [InfiniteLine(point1=Point(0, 0), point2=Point(1, 1))]
        
        scene = SVGScene(
            circles=circles,
            intersections=intersections,
            points=points,
            lines=lines
        )
        
        assert len(scene.circles) == 2
        assert len(scene.points) == 2
        assert len(scene.lines) == 1
        assert len(scene.intersections) == 0

    def test_svg_scene_immutable(self):
        """Test that SVGScene is frozen"""
        scene = SVGScene(circles=[], intersections=[], points=[], lines=[])
        
        with pytest.raises((AttributeError, Exception)):
            scene.circles = []

    def test_svg_scene_hashable(self):
        """Test that SVGScene is hashable"""
        scene1 = SVGScene(circles=[], intersections=[], points=[], lines=[])
        scene2 = SVGScene(circles=[], intersections=[], points=[], lines=[])
        
        scene_set = {scene1, scene2}
        assert len(scene_set) == 1
