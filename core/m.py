import math

def dist(a1,a2):
    return math.sqrt((a1.pos[0]-a2.pos[0])**2+(a1.pos[1]-a2.pos[1])**2)
def mdist(a1,a2):
    return (a1.pos[0]-a2.pos[0])**2+(a1.pos[1]-a2.pos[1])**2