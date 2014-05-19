
import math


class Transform():

    @staticmethod
    def move_points(a, b):
        # a = points
        # b = offset
        
        points = []
        
        for point in a:
            points.append((point[0] + b[0], point[1] + b[1]))
        return points
    
    
    @staticmethod
    def move_lines(a, b):
        # a = lines
        # b = offset
        
        lines = []
        
        for line in a:
            lines.append((
              (line[0][0] + b[0], line[0][1] + b[1]),
              (line[1][0] + b[0], line[1][1] + b[1])
            ))
        return lines

    
    @staticmethod
    def make_point(start_point, direction, speed, time_passed):
        radians = math.radians(direction - 135)
        cos = math.cos(radians)
        sin = math.sin(radians)
        speed *= time_passed
        return (
            start_point[0] + (speed * cos - speed * sin),
            start_point[1] + (speed * sin + speed * cos)
        )