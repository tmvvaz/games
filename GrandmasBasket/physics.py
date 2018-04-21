import math


def get_angle(basket_coord, shirt_coord):

    dx = basket_coord[0] - shirt_coord[0]
    dy = basket_coord[1] - shirt_coord[1]

    angle = math.degrees(math.atan(float(dx) / dy))

    return angle
"""
class Kinematics:
    def __init__(self):
        self.position =
        self.dX =
        self.dY =
        self.acceleration =

class Dynamics:
    def __init__(self):
        self.friction =
"""