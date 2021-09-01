import pygame
import objects

# creating a shorten call the Vector2 function
vector2 = pygame.math.Vector2
# width and height of the display
width = 1000
height = 1000
win = pygame.display.set_mode((width, height))
points = []
sticks = []

# how many points for cloth, could package all of below into function
how_many_x = 50
how_many_y = 50
dy = int((height - 200) / how_many_y)
dx = int((width - 200) / how_many_x)

for y in range(100, height - 100, dy):
    for x in range(100, width - 100, dx):
        pos = vector2(x, y)
        points.append(objects.point(win, pos, pos, False))

for i in range(len(points)):
    if (i + how_many_x) < len(points):
        stick = objects.stick(win, points[i], points[i + how_many_x], (points[i].position - points[i + how_many_x].position).length())
        sticks.append(stick)
    if  i + 1 < len(points) and (i+1) % how_many_x != 0:
        stick = objects.stick(win, points[i], points[i + 1], (points[i].position - points[i + 1].position).length())
        sticks.append(stick)
# end of function if needed

# not my code but used because its very fast
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

# for creating own ropes and cloth
selected_point = None
# for slicing the sticks
start_slice = None
end_slice = None
# for the while loop
running = True
# for creating and drawing
simulating = False
clock = pygame.time.Clock()
while running:
    # delta time
    dt = clock.tick(144) / 1000
    win.fill((0, 0, 0))
    for event in pygame.event.get():
        # x arrow clicked on window
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN and not simulating:
            '''
            1 - left click
            2 - middle click
            3 - right click
            4 - scroll up
            5 - scroll down'''
            pos = vector2(pygame.mouse.get_pos())
            if event.button == 1:
                # creating a point
                points.append(objects.point(win, pos, pos, False))
                
            if event.button == 3:
                pos = vector2(pygame.mouse.get_pos())
                # seeing if the click was in a point
                for point in points:
                    if (point.position - pos).length() <= point.radius:
                        if selected_point != None:
                            # first click
                            sticks.append(objects.stick(win, selected_point, point, (selected_point.position - point.position).length()))
                            selected_point = None
                            break
                        else:
                            # second click
                            if selected_point == point:
                                # remove if clicked again
                                selected_point = None
                            else:
                                # assign if not already clicked
                                selected_point = point                               
            if event.button == 2:
                # locking a point
                pos = vector2(pygame.mouse.get_pos())
                for point in points:
                    if (point.position - pos).length() <= point.radius:
                        point.locked = not point.locked                      
        if event.type == pygame.MOUSEBUTTONDOWN and simulating:
            # slicing the sticks in a straight line
            pos = vector2(pygame.mouse.get_pos())
            start_slice = pos
        if event.type == pygame.MOUSEBUTTONUP and simulating:
            end_slice = vector2(pygame.mouse.get_pos())
            # remove after to not affect the loop
            need_to_remove = []
            for stick in sticks:
                a = stick.pointA
                b = stick.pointB
                # see if they intersect
                if intersect(a.position, b.position, vector2(start_slice), vector2(end_slice)):
                    need_to_remove.append(stick)
            # remove needed sticks
            for stick in need_to_remove:
                sticks.remove(stick)
        # start/stop simulation with space key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                simulating = not simulating
    # drawing
    for stick in sticks:
        stick.draw()
    if not simulating:
        for point in points:
            point.draw()
    if simulating:
        # simulate
        objects.simulate(points, sticks, dt)
    pygame.display.update()
pygame.quit()
