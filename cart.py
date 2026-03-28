class Cart:
    def __init__(self, state, width, height, wheel_radius, min_x=-0.85, max_x=0.85):
        self.width = width
        self.height = height
        self.wheel_radius = wheel_radius
        self.collision_radius = wheel_radius
        self.fixed_y = True
        self.min_x = min_x
        self.max_x = max_x
        self.initial_state = CartState(
            state.x,
            state.y,
            state.xd,
            state.yd,
            state.xdd,
            state.ydd,
        )
        self.reset()

    def update_state(self, state):
        if isinstance(state, CartState):
            self.x = state.x
            self.y = state.y
            self.xd = state.xd
            self.yd = state.yd
            self.xdd = state.xdd
            self.ydd = state.ydd
            return

        self.x = state[0]
        self.y = state[1]
        self.xd = state[2]
        self.yd = state[3]
        self.xdd = state[4]
        self.ydd = state[5]

    def reset(self):
        self.update_state(self.initial_state)

    def reset_height(self):
        self.y = self.initial_state.y
        self.yd = 0.0
        self.ydd = self.initial_state.ydd

    def clamp_to_track(self):
        self.y = self.collision_radius
        self.yd = 0.0
        self.ydd = 0.0

        if self.x < self.min_x:
            self.x = self.min_x
            self.xd = 0.0
            self.xdd = 0.0
        elif self.x > self.max_x:
            self.x = self.max_x
            self.xd = 0.0
            self.xdd = 0.0


class CartState:
    def __init__(self, x, y, xd, yd, xdd, ydd):
        self.x = x
        self.y = y
        self.xd = xd
        self.yd = yd
        self.xdd = xdd
        self.ydd = ydd
