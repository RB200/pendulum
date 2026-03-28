import engine
import ball
import cart
import pendulum
import pygame
from pygame_wrapper import PygameWrapper

x = 0
y = 0.5
radius = 0.1
xd = 0
yd = 0
xdd = 0
ydd = 0
cart_acceleration = 3.5

e = engine.Engine()

cart_state = cart.CartState(-0.45, 0.08, 0, 0, 0, 0)
cart1 = cart.Cart(cart_state, width=0.45, height=0.12, wheel_radius=0.08)
pendulum_state = pendulum.PendulumState(0.35, 0.0)
pendulum1 = pendulum.Pendulum(pendulum_state, cart1, length=0.45, bob_radius=0.06)

e.add_object(cart1)
e.add_object(pendulum1)

renderer = PygameWrapper()

running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                e.reset()
            elif event.key == pygame.K_h:
                e.reset_heights()
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_s:
                cart1.xd = 0.0
                cart1.xdd = 0.0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        cart1.xdd = -cart_acceleration
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cart1.xdd = cart_acceleration
    else:
        cart1.xdd = 0.0

    if not paused:
        e.step()
    renderer.draw(e.objs)
    renderer.tick()

renderer.shutdown()
