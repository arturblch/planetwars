import pygame
import math

background_colour = (255,255,255)
(width, height) = (900, 900)

screen = pygame.display.set_mode((width, height))

icon = pygame.image.load('../../planets/planetIcon.png')

def findPlanet(planets, x, y):
    for p in planets:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None




pygame.display.set_icon(icon)
pygame.display.set_caption('Map Maker')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            print(mouseX, mouseY)
            # selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
            # selected_particle = None

    # if selected_particle:
    #     (mouseX, mouseY) = pygame.mouse.get_pos()
    #     dx = mouseX - selected_particle.x
    #     dy = mouseY - selected_particle.y
    #     selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
    #     selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)

    # for particle in my_particles:
    #     particle.move()
    #     particle.bounce()
    #     particle.display()

    pygame.display.flip()
