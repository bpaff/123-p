

class Collision():

    # http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/    
    @staticmethod
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    
    @staticmethod
    def intersect_two_lines(a, b, c, d):
        # a, b = line 1
        # c, d = line 2
        return Collision.ccw(a, c, d) != Collision.ccw(b, c, d) and Collision.ccw(a, b, c) != Collision.ccw(a, b, d)
    
    @staticmethod
    def intersect_box_lines_to_line(a, b, c, d, e, f):
        # a, b, c, d = points of the four corners of the box
        # e, f = the line
        if Collision.intersect_two_lines(a, b, e, f):
            return True
        if Collision.intersect_two_lines(b, c, e, f):
            return True
        if Collision.intersect_two_lines(c, d, e, f):
            return True
        if Collision.intersect_two_lines(d, a, e, f):
            return True
        return False

    @staticmethod
    def intersect_lines_to_lines(a, b):
        # a = lines 1
        # b = lines 2
        # line is ((x1,y1),(x2,y2))
        for line_a in a:
            for line_b in b:
                if Collision.intersect_two_lines(line_a[0], line_a[1], line_b[0], line_b[1]):
                    return True
        return False