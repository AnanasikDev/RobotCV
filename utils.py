import math
import time

from motors import *


class Point:
    def __init__(self, x, y=None, polar=False):
        if type(x) is float or type(x) is int:
            self.x = x
            self.y = y
        elif type(x) is Point:
            self.x = x.x
            self.y = x.y
            polar = x.polar
        if polar:
            r = self.x
            a = self.y
            self.x = math.cos(a) * r
            self.y = math.sin(a) * r

    def __dist(self, point, i=None):
        if type(point) is Point:
            x = point.x
            y = point.y
        else:
            x = point
            y = i
        return ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5

    def dist(self, target=None, i=None):
        if target == None:
            return self.__dist(0, 0)
        elif (type(target) is float or type(target) is int) and \
                (type(i) is float or type(i) is int):
            return self.__dist(target, i)
        return self.__dist(target)

    def __abs__(self):
        return self.dist()

    def __str__(self):
        return f"({self.x}, {self.y})"


class Vector(Point):
    def __init__(self, x, y=None, z=None, w=None):
        if type(x) is Point and y is None:
            super().__init__(x.x, x.y)
        elif type(x) is Point and type(y) is Point:
            super().__init__(y.x - x.x, y.y - x.y)
        elif (type(x) is float or type(x) is int) and \
             (type(y) is float or type(y) is int) and \
             (type(z) is float or type(z) is int) and \
             (type(w) is float or type(w) is int):
            super().__init__(z - x, w - y)
        elif (type(x) is float or type(x) is int) and \
             (type(y) is float or type(y) is int):
            super().__init__(x, y)

    def length(self):
        return math.hypot(self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def __mul__(self, other):
        return self.dot_product(other)

    def cross_product(self, other):
        return self.x * other.y - self.y * other.x

    def __xor__(self, other):
        return self.cross_product(other)

    def mul(self, n):
        return Vector(self.x * n, self.y * n)

    def __rmul__(self, n):
        return Vector(self.x * n, self.y * n)


def clamp(x, mn, mx):
    if x > mx:
        return mx
    if x < mn:
        return mn
    return x


def stop(t):
    #timer = Timer(6)
    motor_left.forward(0)
    motor_right.forward(0)
    time.sleep(t)
    motor_left.forward(0)
    motor_right.forward(0)


class Timer:
    def __init__(self, t):
        self.start = time.time()
        self.t = t
    
    def update(self):
        if time.time() - self.t * 1000 > self.start:
            return True
        return False
