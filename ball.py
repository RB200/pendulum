class Ball:
    def __init__(self, state, radius):
        self.radius = radius
        self.initial_state = BallState(
            state.x,
            state.y,
            state.xd,
            state.yd,
            state.xdd,
            state.ydd,
        )
        self.reset()
    
    def update_state(self, state):
        if isinstance(state, BallState):
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
        
    def get_state(self):
        return [round(self.x,4), round(self.y,4), round(self.xd,4), round(self.yd,4), round(self.xdd,4), round(self.ydd,4)]
    
class BallState:
    def __init__(self, x, y, xd, yd, xdd, ydd):
        self.x = x
        self.y = y
        self.xd = xd
        self.yd = yd
        self.xdd = xdd    
        self.ydd = ydd
