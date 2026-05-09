import numpy as np
from data_provider import DataProvider
from math_engine import MathEngine
from visualization_module import VisualizationModule


class AnimationController:
    def __init__(self):
        self.dp = DataProvider()
        self.math = MathEngine()
        self.viz = VisualizationModule()

    def run_prototype(self):
        x, y, degree = self.dp.get_data()

        # Створює щільну сітку X для плавного малювання ліній (500 точок між min і max)
        x_dense = np.linspace(min(x), max(x), 500)

        y_lagrange = self.math.calculate_lagrange(x, y, x_dense)
        y_lsm, y_nodes = self.math.calculate_lsm(x, y, degree, x_dense)
        residuals = self.math.calculate_residuals(y, y_nodes)

        self.viz.render_prototype(x, y, x_dense, y_lagrange, y_lsm, residuals)


if __name__ == "__main__":
    app = AnimationController()
    app.run_prototype()