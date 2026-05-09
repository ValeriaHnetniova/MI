import numpy as np
from scipy.interpolate import lagrange
import warnings

try:
    from numpy.exceptions import RankWarning
except ImportError:
    from numpy import RankWarning

warnings.simplefilter('ignore', RankWarning)

class MathEngine:
    @staticmethod
    def calculate_lagrange(x, y):
        poly = lagrange(x, y)
        return np.poly1d(poly.coef)

    @staticmethod
    def calculate_lsm(x, y, degree):
        coefs = np.polyfit(x, y, degree)
        return np.poly1d(coefs)

    @staticmethod
    def calculate_residuals(y_true, y_calc):
        return y_true - y_calc