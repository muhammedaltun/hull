import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '140,40'

import pygame, sys, math
from pygame.locals import *

WINDOWWIDTH = 720                          # size of window's width in pixels
WINDOWHEIGHT = 720                         # size of windows' height in pixels

BLACK    = (  0,   0,   0)
DARK     = ( 50,  50,  50)
GRAY     = (100, 100, 100)
WHITE    = (255, 255, 255)
YELLOW   = (255, 255,   0)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)

points = set()
hull = []            

def main():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(GRAY)
    pygame.display.set_caption('CONVEX HULL')
    for p in points:
        pygame.draw.circle(DISPLAYSURF, YELLOW, p, 5, 0)
    
    
    while True:                                # main loop
        for event in pygame.event.get():       # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos     
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    DISPLAYSURF.fill(GRAY)
                    if len(hull) == 2: pygame.draw.line(DISPLAYSURF, BLUE,hull[0],hull[1],5)
                    if len(hull) > 2: pygame.draw.polygon(DISPLAYSURF,BLUE,hull,5)
                    for p in points:
                        pygame.draw.circle(DISPLAYSURF, YELLOW, p, 5, 0)
                    if hull: pygame.draw.circle(DISPLAYSURF, RED, hull[0], 5, 0)
                                              
        if pygame.mouse.get_pressed()[0]: 
            points.add((mousex,mousey))
            pygame.draw.circle(DISPLAYSURF, YELLOW, (mousex,mousey), 5, 0)
        hull = convexHull(points)
            
        pygame.display.update()


def convexHull(points):
    if len(points) < 3: return list(points)
    first = 0
    for p in points:
        if not first: first = p
        elif p[0] < first[0]: first = p
        elif p[0] == first[0] and p[1] > first[1]: first = p

    hull = [first]
    
    while len(hull) == 1 or (len(hull) > 1 and hull[-1] != hull[0]):
        candidates = []
        for p in points: 
            if p != hull[-1] and all([cross(hull[-1],p,r) >= 0 for r in points]):
                candidates.append(p)
        dist = -1    
        for c in candidates:
            if dist == -1: 
                nextOne = c
                dist = distance(c,hull[-1])
            elif dist < distance(c,hull[-1]):
                nextOne = c
                dist = distance(c,hull[-1])
        hull.append(nextOne)
    return hull[:-1]


def cross(point1,point2,point3):     
    # finds the sign of cross product: (point1,point2) x (point1,point3)
    vector0 = (point2[0]-point1[0],point2[1]-point1[1])
    vector1 = (point3[0]-point1[0],point3[1]-point1[1])
    determinant = vector0[0]*vector1[1] - vector0[1]*vector1[0]
    if determinant == 0: return 0     # the points are linear
    if determinant > 0: return 1      # point3 is on the right side of (point1,point2)
    if determinant < 0: return -1     # point3 is on the left side of (point1,point2)

def distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2) 

main()