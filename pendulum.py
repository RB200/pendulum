import math


class Pendulum:
    def __init__(self, state, cart, length, bob_radius):
        self.cart = cart
        self.length = length
        self.bob_radius = bob_radius
        self.initial_state = PendulumState(state.theta, state.theta_d)
        self.reset()

    def update_state(self, state):
        if isinstance(state, PendulumState):
            self.theta = state.theta
            self.theta_d = state.theta_d
            return

        self.theta = state[0]
        self.theta_d = state[1]

    def reset(self):
        self.update_state(self.initial_state)
        self.refresh_geometry()

    def reset_height(self):
        self.refresh_geometry()

    def pivot_position(self):
        return self.cart.x, self.cart.y + self.cart.wheel_radius + self.cart.height

    def refresh_geometry(self):
        self.pivot_x, self.pivot_y = self.pivot_position()
        self.x = self.pivot_x + self.length * math.sin(self.theta)
        self.y = self.pivot_y - self.length * math.cos(self.theta)
        self.xd = 0.0
        self.yd = 0.0
        self.xdd = 0.0
        self.ydd = 0.0


class PendulumState:
    def __init__(self, theta, theta_d):
        self.theta = theta
        self.theta_d = theta_d
