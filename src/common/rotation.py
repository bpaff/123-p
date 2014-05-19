
import math


class Rotation():
    
    @staticmethod
    def rotate_points(a, b, c, d):
        # a = points
        # b = rotation
        # c = center
        # d = offset (optional)
        
        radians = math.radians(b)
        cos = math.cos(radians)
        sin = math.sin(radians)
        if d is None:
            d = (0, 0)
        points = []
        
        for point in a:
            points.append((
            ((point[0] - c[0]) * cos - (point[1] - c[1]) * sin) + c[0] + d[0],
            ((point[0] - c[0]) * sin + (point[1] - c[1]) * cos) + c[1] + d[1]
           ))
        return points
    
    
    @staticmethod
    def rotate_lines(a, b, c, d):
        # a = lines
        # b = rotation
        # c = center
        # d = offset (optional)
        
        radians = math.radians(b)
        cos = math.cos(radians)
        sin = math.sin(radians)
        if d is None:
            d = (0, 0)
        lines = []
        
        for line in a:
            lines.append((
              (((line[0][0] - c[0]) * cos - (line[0][1] - c[1]) * sin) + c[0] + d[0],
              ((line[0][0] - c[0]) * sin + (line[0][1] - c[1]) * cos) + c[1] + d[1]),
              (((line[1][0] - c[0]) * cos - (line[1][1] - c[1]) * sin) + c[0] + d[0],
              ((line[1][0] - c[0]) * sin + (line[1][1] - c[1]) * cos) + c[1] + d[1])
           ))
        return lines
    
