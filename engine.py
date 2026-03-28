import math

class Engine:
    def __init__(self):
        self.COR = 0.9
        self.dt = 0.025
        self.gravity = -9.8
        self.t = 0.0
        self.objs = []

    def step(self):
        for obj in self.objs:
            dt = self.dt
            floor_y = getattr(obj, "collision_radius", getattr(obj, "radius", 0.0))
            g = abs(self.gravity)

            if hasattr(obj, "theta"):
                cart_xdd = getattr(obj.cart, "xdd", 0.0)
                theta_dd = (
                    -(g / obj.length) * math.sin(obj.theta)
                    - (cart_xdd / obj.length) * math.cos(obj.theta)
                )
                obj.theta_d += theta_dd * dt
                obj.theta += obj.theta_d * dt
                obj.refresh_geometry()
                continue

            if hasattr(obj, "refresh_geometry"):
                obj.refresh_geometry()
                continue

            if getattr(obj, "fixed_y", False):
                obj.x = obj.x + obj.xd * dt + 0.5 * obj.xdd * dt * dt
                obj.xd = obj.xd + obj.xdd * dt
                obj.clamp_to_track()
                continue


            # Save state at beginning of step
            x0 = obj.x
            y0 = obj.y
            xd0 = obj.xd
            yd0 = obj.yd

            # Predict full-step motion
            x1 = x0 + xd0 * dt + 0.5 * obj.xdd * dt * dt
            y1 = y0 + yd0 * dt + 0.5 * obj.ydd * dt * dt

            xd1 = xd0 + obj.xdd * dt
            yd1 = yd0 + obj.ydd * dt

            if y1 >= floor_y:
                x = x1
                y = y1
                xd = xd1
                yd = yd1
            else:
                a = 0.5 * obj.ydd
                b = yd0
                c = y0 - floor_y

                discriminant = b * b - 4 * a * c

                if discriminant < 0:
                    x = x1
                    y = floor_y
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
                        y = floor_y
                        xd = xd1
                        yd = -yd1 * self.COR
                    else:
                        x_hit = x0 + xd0 * tau_hit + 0.5 * obj.xdd * tau_hit * tau_hit
                        y_hit = floor_y
                        xd_hit = xd0 + obj.xdd * tau_hit
                        yd_hit = yd0 + obj.ydd * tau_hit

                        yd_bounce = -yd_hit * self.COR
                        xd_bounce = xd_hit

                        dt_remain = dt - tau_hit

                        x = x_hit + xd_bounce * dt_remain + 0.5 * obj.xdd * dt_remain * dt_remain
                        y = y_hit + yd_bounce * dt_remain + 0.5 * obj.ydd * dt_remain * dt_remain

                        xd = xd_bounce + obj.xdd * dt_remain
                        yd = yd_bounce + obj.ydd * dt_remain

                        if y < floor_y:
                            y = floor_y

                        if y <= floor_y and abs(yd) < 0.15:
                            yd = 0.0
                            xd = 0.0

            # WRITE BACK TO OBJECT
            obj.x = x
            obj.y = y
            obj.xd = xd
            obj.yd = yd
            obj.xdd = obj.xdd
            obj.ydd = self.gravity

        self.t += self.dt

        
    def add_object(self, obj):
        if hasattr(obj, "refresh_geometry"):
            obj.refresh_geometry()
        if getattr(obj, "fixed_y", False):
            obj.clamp_to_track()
        self.objs.append(obj)

    def reset(self):
        self.t = 0.0
        for obj in self.objs:
            obj.reset()

    def reset_heights(self):
        self.t = 0.0
        for obj in self.objs:
            obj.reset_height()
