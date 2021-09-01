import pygame
import copy

WHITE = (255, 255, 255)
RED   = (120,  0 ,  0 )

class point:
    def __init__(self, win, position, previous, locked = False):
        self.win = win
        # both positions are pygame.math.Vector2
        self.position = position
        self.previous = previous
        # bool
        self.locked = locked
        # for drawing only
        self.radius = 4
    def draw(self):
        # red if locked
        if not self.locked:
            pygame.draw.circle(self.win, WHITE, self.position, self.radius)
        else:
            pygame.draw.circle(self.win, RED, self.position, self.radius)

class stick:
    def __init__(self, win, pointA, pointB, length):
        self.win = win
        # both points of the above point class
        self.pointA, self.pointB = pointA, pointB
        # length that it will try to maintain
        self.length = float(length)
    def draw(self):
        # draw a line from one point to the other (A->B)
        pygame.draw.line(self.win, WHITE, self.pointA.position, self.pointB.position, 2)


def simulate(points, sticks, dt):
    for p in points:
        if not p.locked:
            # deepcopying the value and not the location
            temp_pos = copy.deepcopy(p.position)
            # keep the point in motion
            p.position += p.position - p.previous
            p.position += pygame.math.Vector2(0, 9 * dt)
            p.previous = temp_pos
    for _ in range(1):
        for stick in sticks:
            # moving the points to keep stick to its length
            centre = (stick.pointA.position + stick.pointB.position) / 2
            direction = (stick.pointA.position - stick.pointB.position).normalize()
            if not stick.pointA.locked:
                stick.pointA.position = centre + direction * stick.length / 2
            if not stick.pointB.locked:
                stick.pointB.position = centre - direction * stick.length / 2
        # but we probably moved another sticks points and thus that stick shrunk or grew
        # so we move them 10 times to balance them out
            

        
