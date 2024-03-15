import math


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, no):
        return Point(self.x - no.x, self.y - no.y, self.z - no.z)

    def dot(self, no):
        return self.x * no.x + self.y * no.y + self.z * no.z

    def cross(self, no):
        return Point(self.y * no.z - self.z * no.y,
                     self.z * no.x - self.x * no.z,
                     self.x * no.y - self.y * no.x)

    def absolute(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


def plane_angle(a, b, c, d):
    ab = b - a
    bc = c - b
    cd = d - c

    x = ab.cross(bc)
    y = bc.cross(cd)

    cosine_angle = x.dot(y) / (x.absolute() * y.absolute())
    angle_rad = math.acos(cosine_angle)
    angle_deg = math.degrees(angle_rad)

    return round(angle_deg, 2)


if __name__ == '__main__':
    points = [Point(*map(float, input().split())) for i in range(4)]
    angle = plane_angle(*points)
    print(angle)
