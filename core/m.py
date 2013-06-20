import math

def dist(a1,a2,center=True):
    if center:
        p1 = a1.rect().center[:]
        p2 = a2.rect().center[:]
    else:
        p1 = a1.pos[:]
        p2 = a2.pos[:]
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
def mdist(a1,a2,center=True):
    if center:
        p1 = a1.rect().center[:]
        p2 = a2.rect().center[:]
    else:
        p1 = a1.pos[:]
        p2 = a2.pos[:]
    return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2
def toward(a1,a2,amt=1):
    d = dist(a1,a2)
    dx = (a2.pos[0]-a1.pos[0])/d*amt
    dy = (a2.pos[1]-a1.pos[1])/d*amt
    return dx,dy
    