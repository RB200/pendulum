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

    def world_to_screen(self, x, y):
        screen_x = int(x * self.pixels_per_unit + self.width / 2)
        screen_y = int(self.height - (y * self.pixels_per_unit + 50))
        return screen_x, screen_y

    def draw(self, balls):
        self.screen.fill(self.background_color)

        ground_y = self.world_to_screen(0, 0)[1]
        pygame.draw.line(
            self.screen,
            self.ground_color,
            (0, ground_y),
            (self.width, ground_y),
            3,
        )

        for index, ball in enumerate(balls):
            center = self.world_to_screen(ball.x, ball.y)
            radius = max(1, int(ball.radius * self.pixels_per_unit))
            color = self.ball_colors[index % len(self.ball_colors)]
            pygame.draw.circle(self.screen, color, center, radius)

        pygame.display.flip()

    def tick(self, fps=40):
        self.clock.tick(fps)

    def shutdown(self):
        pygame.quit()
