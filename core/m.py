import math

def dist(a1,a2):
    return math.sqrt((a1.pos[0]-a2.pos[0])**2+(a1.pos[1]-a2.pos[1])**2)
def mdist(a1,a2):
    return (a1.pos[0]-a2.pos[0])**2+(a1.pos[1]-a2.pos[1])**2
def toward(a1,a2,amt=1):
    d = dist(a1,a2)
    dx = (a2.pos[0]-a1.pos[0])/d*amt
    dy = (a2.pos[1]-a1.pos[1])/d*amt
    return dx,dy
    