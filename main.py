import engine
import ball
import pygame
from pygame_wrapper import PygameWrapper

x = 0
y = 0.5
radius = 0.1
xd = 0
yd = 0
xdd = 0
ydd = 0

e = engine.Engine() # initial state passed to engine

bs1 = ball.BallState(0.1, 0.75, 0, 0, 0, 0)
ball1 = ball.Ball(bs1, radius)

bs2 = ball.BallState(x, y, xd, yd, xdd, ydd)
ball2 = ball.Ball(bs2, radius)

e.add_object(ball1)
e.add_object(ball2)

renderer = PygameWrapper()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                e.reset()
            elif event.key == pygame.K_h:
                e.reset_heights()

    e.step()
    renderer.draw(e.objs)
    renderer.tick()

renderer.shutdown()
