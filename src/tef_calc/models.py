"""
Core data models for the TEF Calculator geometry system.

All models are frozen (immutable) dataclasses with proper type hints.
Models are hashable and can be used in sets/dicts.
"""

from dataclasses import dataclass
from typing import List
import math


@dataclass(frozen=True)
class Point:
    """
    2D coordinate point.
    
    Attributes:
        x: X coordinate (float)
        y: Y coordinate (float)
    """
    x: float
    y: float
    
    def distance_to(self, other: "Point") -> float:
        """
        Calculate Euclidean distance to another point.
        
        Args:
            other: Another Point
            
        Returns:
            Distance between this point and the other point
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def midpoint(self, other: "Point") -> "Point":
        """
        Calculate the midpoint between this point and another.
        
        Args:
            other: Another Point
            
        Returns:
            New Point at the midpoint
        """
        return Point(x=(self.x + other.x) / 2, y=(self.y + other.y) / 2)


@dataclass(frozen=True)
class Circle:
    """
    Circle defined by center point and radius.
    
    Attributes:
        center: Center point of the circle
        radius: Radius of the circle (must be positive)
    """
    center: Point
    radius: float
    
    def area(self) -> float:
        """
        Calculate the area of the circle.
        
        Returns:
            Area = π * r²
        """
        return math.pi * self.radius ** 2
    
    def diameter(self) -> float:
        """
        Calculate the diameter of the circle.
        
        Returns:
            Diameter = 2 * r
        """
        return 2 * self.radius
    
    def contains(self, point: Point) -> bool:
        """
        Check if a point is inside or on the circle.
        
        Args:
            point: Point to check
            
        Returns:
            True if point is inside or on the circle boundary
        """
        distance = self.center.distance_to(point)
        return distance <= self.radius
    
    def intersects(self, other: "Circle") -> bool:
        """
        Check if this circle intersects with another circle.
        
        Two circles intersect if the distance between their centers
        is less than or equal to the sum of their radii AND
        greater than or equal to the absolute difference of their radii.
        
        Args:
            other: Another Circle
            
        Returns:
            True if circles intersect (including tangent and contained cases)
        """
        center_distance = self.center.distance_to(other.center)
        radius_sum = self.radius + other.radius
        radius_diff = abs(self.radius - other.radius)
        
        return radius_diff <= center_distance <= radius_sum


@dataclass(frozen=True)
class InfiniteLine:
    """
    Infinite line defined by two points.
    
    Attributes:
        point1: First point on the line
        point2: Second point on the line
    """
    point1: Point
    point2: Point
    
    def is_vertical(self) -> bool:
        """
        Check if the line is vertical.
        
        Returns:
            True if the line is vertical (x1 == x2)
        """
        return self.point1.x == self.point2.x
    
    def slope(self) -> float:
        """
        Calculate the slope of the line.
        
        Returns:
            Slope = (y2 - y1) / (x2 - x1)
            
        Raises:
            ZeroDivisionError: If line is vertical
        """
        if self.is_vertical():
            raise ZeroDivisionError("Vertical line has undefined slope")
        
        return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
    
    def point_at(self, x: float) -> Point:
        """
        Get a point on the line at a specific x coordinate.
        
        Uses point-slope form: y - y1 = m(x - x1)
        
        Args:
            x: X coordinate
            
        Returns:
            Point on the line with the given x coordinate
            
        Raises:
            ValueError: If line is vertical
        """
        if self.is_vertical():
            raise ValueError("Cannot use point_at(x) for vertical line; use point_at_y() instead")
        
        m = self.slope()
        y = self.point1.y + m * (x - self.point1.x)
        return Point(x=x, y=y)
    
    def point_at_y(self, y: float) -> Point:
        """
        Get a point on the line at a specific y coordinate.
        
        For vertical lines: x = point1.x
        For non-vertical lines: x = x1 + (y - y1) / m
        
        Args:
            y: Y coordinate
            
        Returns:
            Point on the line with the given y coordinate
        """
        if self.is_vertical():
            return Point(x=self.point1.x, y=y)
        
        m = self.slope()
        x = self.point1.x + (y - self.point1.y) / m
        return Point(x=x, y=y)


@dataclass(frozen=True)
class Intersection:
    """
    Result of a circle-circle intersection.
    
    Attributes:
        circle1: First circle
        circle2: Second circle
        points: List of intersection points
    """
    circle1: Circle
    circle2: Circle
    points: List[Point]


@dataclass(frozen=True)
class SVGScene:
    """
    Complete scene containing geometric elements for rendering.
    
    Attributes:
        circles: List of circles
        intersections: List of intersection results
        points: List of points
        lines: List of infinite lines
    """
    circles: List[Circle]
    intersections: List[Intersection]
    points: List[Point]
    lines: List[InfiniteLine]
