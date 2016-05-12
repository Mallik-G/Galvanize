import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)




class Triangle(object):
    def __init__(self, p1, p2, p3):
        try:
            p1.distance(p2)
            p2.distance(p3)
            p3.distance(p1)
        except:
            return ValueError

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def perimeter(self):
        return  self.p1.distance(self.p2)+\
                self.p2.distance(self.p3)+\
                self.p3.distance(self.p1)

    def is_line(self):
        if (self.p1.x == self.p2.x == self.p3.x) or \
           (self.p1.y == self.p2.y == self.p3.y):

           print "Degenerate"
           return
        print "Not degenerate"
        return
