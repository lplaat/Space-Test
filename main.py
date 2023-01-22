import math
import pygame
import sys
import numpy as np

pygame.init()
  
surface = pygame.display.set_mode([500, 500])
clock = pygame.time.Clock()

g = 4
planets = []

def calcG(object1, object2):
    try:
        return (g * object1.mass) / (math.dist(object1.position, object2.position) ** 2)
    except:
        return (g * object1.mass) / 0.00001

def calcAngle(object1, object2):
    dx = object1[0] - object2[0]
    dy = object1[1] - object2[1]
    return math.atan2(dy, dx)

class planet():
    def __init__(self, x, y, color, size, mass, stuck, id):
        self.position = (x, y)
        self.id = id
        self.color = color
        self.stuck = stuck
        self.size = size
        self.mass = mass
        self.forces = []

    def update(self):
        if self.stuck == False:
            for otherPlanet in planets:
                if not self.id == otherPlanet.id:
                    self.forces.append([calcAngle(otherPlanet.position, self.position), calcG(otherPlanet, self)])

            endLocation = self.position
            for force in self.forces:
                forceMap = [math.cos(force[0]) * force[1], math.sin(force[0]) * force[1]]
                endLocation = np.add(endLocation, forceMap)

            rAngle = calcAngle(endLocation, self.position)
            rForce = math.dist(endLocation, self.position)

            self.forces = [[rAngle, rForce]]
            self.position = np.add(self.position, [math.cos(rAngle) * rForce, math.sin(rAngle) * rForce])

    def addForce(self, force):
        self.forces.append(force)

    def draw(self):
        pygame.draw.circle(surface, self.color, self.position, self.size, 0)


planets.append(planet(250, 250, (0, 255, 0), 50, 200, True, 0))
planets.append(planet(250, 120, (255, 0, 0), 3, 7, False, 1))
planets.append(planet(250, 380, (0, 0, 255), 3, 7, False, 2))

planets[1].addForce([0, 2.3])
planets[2].addForce([math.radians(180), 2.3])

#frame loop
while True:
    s = pygame.Surface((1000, 1000))
    s.set_alpha(50)               
    s.fill((0, 0, 0))
    surface.blit(s, (0,0)) 

    #shutdown event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    #draw planets and updates them
    for planetObject in planets:
        planetObject.update()
        planetObject.draw()

    #clock
    pygame.display.update()
    clock.tick(60)
