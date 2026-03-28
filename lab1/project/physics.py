import numpy as np


class PhysicalBody:
    def __init__(self, x0, y0, v0, a, angle_deg):
        self.x0 = x0
        self.y0 = y0

        rad = np.radians(angle_deg)

        self.vx = v0 * np.cos(rad)
        self.vy = v0 * np.sin(rad)

        self.ax = a * np.cos(rad)
        self.ay = a * np.sin(rad)

    def calculate(self, t_end=10, points=200):
        t = np.linspace(0, t_end, points)

        x = self.x0 + self.vx * t + 0.5 * self.ax * t ** 2
        y = self.y0 + self.vy * t + 0.5 * self.ay * t ** 2

        return x, y