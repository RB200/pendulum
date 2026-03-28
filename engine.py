import time
import math

class Engine:
    def __init__(self):
        self.gravity = 9.8

        self.x = 0.0
        self.y = 1.0

        self.xd = 0.0
        self.yd = 0.0

        self.xdd = 0.0
        self.ydd = -self.gravity

        self.COR = 0.9
        self.t = 0.0

    def step(self):
        t0 = time.monotonic()
        time.sleep(0.025)
        dt = time.monotonic() - t0

        # Save state at beginning of step
        x0 = self.x
        y0 = self.y
        xd0 = self.xd
        yd0 = self.yd

        # Predict full-step motion
        x1 = x0 + xd0 * dt + 0.5 * self.xdd * dt * dt
        y1 = y0 + yd0 * dt + 0.5 * self.ydd * dt * dt

        xd1 = xd0 + self.xdd * dt
        yd1 = yd0 + self.ydd * dt

        if y1 > 0:
            x = x1
            y = y1
            xd = xd1
            yd = yd1
        else:
            a = 0.5 * self.ydd
            b = yd0
            c = y0

            discriminant = b * b - 4 * a * c

            if discriminant < 0:
                x = x1
                y = 0.0
                xd = xd1
                yd = -yd1 * self.COR
            else:
                sqrt_disc = math.sqrt(discriminant)

                tau1 = (-b + sqrt_disc) / (2 * a)
                tau2 = (-b - sqrt_disc) / (2 * a)

                tau_hit = None
                for tau in (tau1, tau2):
                    if 0 <= tau <= dt:
                        tau_hit = tau
                        break

                if tau_hit is None:
                    x = x1
                    y = 0.0
                    xd = xd1
                    yd = -yd1 * self.COR
                else:
                    x_hit = x0 + xd0 * tau_hit + 0.5 * self.xdd * tau_hit * tau_hit
                    y_hit = 0.0
                    xd_hit = xd0 + self.xdd * tau_hit
                    yd_hit = yd0 + self.ydd * tau_hit

                    yd_bounce = -yd_hit * self.COR
                    xd_bounce = xd_hit

                    dt_remain = dt - tau_hit

                    x = x_hit + xd_bounce * dt_remain + 0.5 * self.xdd * dt_remain * dt_remain
                    y = y_hit + yd_bounce * dt_remain + 0.5 * self.ydd * dt_remain * dt_remain

                    xd = xd_bounce + self.xdd * dt_remain
                    yd = yd_bounce + self.ydd * dt_remain

                    if y < 0:
                        y = 0

                    if y == 0 and abs(yd) < 0.15:
                        yd = 0.0
                        xd = 0.0

        # WRITE BACK TO OBJECT
        self.x = x
        self.y = y
        self.xd = xd
        self.yd = yd
        self.t += dt

        return [round(self.x,4), round(self.y,4), round(self.xd,4), round(self.yd,4), round(self.xdd,4), round(self.ydd,4), round(self.t,4)]