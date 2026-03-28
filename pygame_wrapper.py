import pygame


class PygameWrapper:
    def __init__(self, width=800, height=600, pixels_per_unit=400):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pendulum")
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.pixels_per_unit = pixels_per_unit

        self.background_color = (245, 247, 250)
        self.ground_color = (60, 60, 60)
        self.ball_colors = [
            (52, 152, 219),
            (231, 76, 60),
            (46, 204, 113),
            (155, 89, 182),
        ]
        self.cart_body_color = (241, 196, 15)
        self.cart_wheel_color = (44, 62, 80)
        self.pendulum_rod_color = (52, 73, 94)
        self.pendulum_bob_color = (192, 57, 43)

    def world_to_screen(self, x, y):
        screen_x = int(x * self.pixels_per_unit + self.width / 2)
        screen_y = int(self.height - (y * self.pixels_per_unit + 50))
        return screen_x, screen_y

    def draw_ball(self, ball, index):
        center = self.world_to_screen(ball.x, ball.y)
        radius = max(1, int(ball.radius * self.pixels_per_unit))
        color = self.ball_colors[index % len(self.ball_colors)]
        pygame.draw.circle(self.screen, color, center, radius)

    def draw_cart(self, cart):
        wheel_offset = cart.width / 2 - cart.wheel_radius * 1.5
        left_wheel_center = self.world_to_screen(
            cart.x - wheel_offset,
            cart.y,
        )
        right_wheel_center = self.world_to_screen(
            cart.x + wheel_offset,
            cart.y,
        )
        wheel_radius_px = max(1, int(cart.wheel_radius * self.pixels_per_unit))

        pygame.draw.circle(
            self.screen,
            self.cart_wheel_color,
            left_wheel_center,
            wheel_radius_px,
        )
        pygame.draw.circle(
            self.screen,
            self.cart_wheel_color,
            right_wheel_center,
            wheel_radius_px,
        )

        body_width_px = int(cart.width * self.pixels_per_unit)
        body_height_px = int(cart.height * self.pixels_per_unit)
        body_center_y = cart.y + cart.wheel_radius + cart.height / 2
        body_center = self.world_to_screen(cart.x, body_center_y)
        body_rect = pygame.Rect(0, 0, body_width_px, body_height_px)
        body_rect.center = body_center
        pygame.draw.rect(self.screen, self.cart_body_color, body_rect, border_radius=8)

    def draw_pendulum(self, pendulum):
        pivot = self.world_to_screen(pendulum.pivot_x, pendulum.pivot_y)
        bob = self.world_to_screen(pendulum.x, pendulum.y)
        bob_radius_px = max(1, int(pendulum.bob_radius * self.pixels_per_unit))

        pygame.draw.line(self.screen, self.pendulum_rod_color, pivot, bob, 4)
        pygame.draw.circle(self.screen, self.pendulum_bob_color, bob, bob_radius_px)
        pygame.draw.circle(self.screen, self.pendulum_rod_color, pivot, 5)

    def draw(self, objs):
        self.screen.fill(self.background_color)

        ground_y = self.world_to_screen(0, 0)[1]
        pygame.draw.line(
            self.screen,
            self.ground_color,
            (0, ground_y),
            (self.width, ground_y),
            3,
        )

        for index, obj in enumerate(objs):
            if hasattr(obj, "bob_radius"):
                self.draw_pendulum(obj)
            elif hasattr(obj, "wheel_radius"):
                self.draw_cart(obj)
            elif hasattr(obj, "radius"):
                self.draw_ball(obj, index)

        pygame.display.flip()

    def tick(self, fps=40):
        self.clock.tick(fps)

    def shutdown(self):
        pygame.quit()
