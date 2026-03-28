import time
import math
import engine
import ball

engine = engine.Engine()
ball = ball.Ball()
while True:
    state = engine.step()
    print(state)


