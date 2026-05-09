import numpy as np

class MathEngine:
    @staticmethod
    def calculate_lagrange(x_points, y_points, x_dense):
        # ЗАГЛУШКА: Замість реального полінома повертаємо масив нулів
        return np.zeros_like(x_dense)

    @staticmethod
    def calculate_lsm(x_points, y_points, degree, x_dense):
        # ЗАГЛУШКА: Повертаємо нульову лінію для МНК та нулі для вузлів
        return np.zeros_like(x_dense), np.zeros_like(x_points)

    @staticmethod
    def calculate_residuals(y_experimental, y_calculated):
        # ЗАГЛУШКА: Залишки (похибки) поки що дорівнюють нулю
        return np.zeros_like(y_experimental)