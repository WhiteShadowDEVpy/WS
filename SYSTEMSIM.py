import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 1920,1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sabit Parlak Güneş Sistemi")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 100)  # Daha yumuşak sarı
SATURN_RING = (200, 200, 200)

clock = pygame.time.Clock()
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1,2)) for _ in range(150)]

def draw_glowing_circle(surface, color, x, y, radius, layers=5):
    """Sabit parlaklık ile gradyan oluştur"""
    for i in range(layers, 0, -1):
        alpha = int(30 * (i / layers))  # Sabit parlaklık
        s = pygame.Surface((radius*4, radius*4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*color, alpha), (radius*2, radius*2), int(radius + i))
        surface.blit(s, (x - radius*2, y - radius*2))

class Moon:
    def __init__(self, color, radius, distance, speed):
        self.color = color
        self.radius = radius
        self.distance = distance
        self.angle = 0
        self.speed = speed / 2  # Daha yavaş

    def move(self):
        self.angle += self.speed
        if self.angle >= 360:
            self.angle -= 360

    def draw(self, screen, planet_x, planet_y):
        x = planet_x + self.distance * math.cos(math.radians(self.angle))
        y = planet_y + self.distance * math.sin(math.radians(self.angle))
        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.radius)

class Planet:
    def __init__(self, color, radius, a, b, speed, moons=None, rotate_speed=0.1, ring=None):
        self.color = color
        self.radius = radius
        self.a = a
        self.b = b
        self.angle = 0
        self.speed = speed / 4  # Daha yavaş
        self.moons = moons if moons else []
        self.rotate_angle = 0
        self.rotate_speed = rotate_speed
        self.ring = ring

    def move(self):
        self.angle += self.speed
        if self.angle >= 360:
            self.angle -= 360
        self.rotate_angle += self.rotate_speed
        if self.rotate_angle >= 360:
            self.rotate_angle -= 360
        for moon in self.moons:
            moon.move()

    def draw(self, screen, sun_x, sun_y):
        x = sun_x + self.a * math.cos(math.radians(self.angle))
        y = sun_y + self.b * math.sin(math.radians(self.angle))
        pygame.draw.ellipse(screen, (150,150,150), (sun_x - self.a, sun_y - self.b, 2*self.a, 2*self.b), 1)
        draw_glowing_circle(screen, self.color, x, y, self.radius, layers=4)
        end_x = x + self.radius * math.cos(math.radians(self.rotate_angle))
        end_y = y + self.radius * math.sin(math.radians(self.rotate_angle))
        pygame.draw.line(screen, WHITE, (x, y), (end_x, end_y), 1)
        if self.ring:
            inner, outer = self.ring
            pygame.draw.ellipse(screen, SATURN_RING, (x-outer, y-outer, 2*outer, 2*outer), 2)
        for moon in self.moons:
            moon.draw(screen, x, y)

sun_x, sun_y = WIDTH//2, HEIGHT//2
sun_radius = 50

# Gezegenler
mercury = Planet((128,128,128), 5, 80, 70, 1.6)
venus = Planet((255,165,100), 9, 120, 110, 1.2)
earth = Planet((100,149,237), 10, 160, 150, 1, moons=[Moon(WHITE,3,20,5)])
mars = Planet((188,39,50), 8, 200, 180, 0.8, moons=[Moon((128,128,128),2,15,4)])
jupiter = Planet((139,69,19), 20, 280, 250, 0.5)
saturn = Planet((255,165,0), 18, 350, 320, 0.4, ring=(22,35))
uranus = Planet((173,216,230), 15, 420, 380, 0.3)
neptune = Planet((138,43,226), 14, 490, 450, 0.25)

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
    draw_glowing_circle(screen, YELLOW, sun_x, sun_y, sun_radius, layers=8)
    for planet in planets:
        planet.move()
        planet.draw(screen, sun_x, sun_y)

    pygame.display.flip()

pygame.quit()
