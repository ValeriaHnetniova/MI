import numpy as np


class ProjectileModel:
    """
    Клас, що відповідає за математичну та фізичну логіку (Model в архітектурі MVC).
    Розраховує кінематику руху тіла, кинутого під кутом до горизонту.
    """

    def __init__(self, v0, alpha_deg, g=9.81):
        self.v0 = v0
        self.alpha_rad = np.radians(alpha_deg)
        self.g = g

    def get_max_time(self):
        """Розраховунок загального часу польоту (t_max)"""
        return (2 * self.v0 * np.sin(self.alpha_rad)) / self.g

    def get_max_distance(self):
        """Розрахунок максимальної дальності польоту (L)"""
        return (self.v0 ** 2 * np.sin(2 * self.alpha_rad)) / self.g

    def get_max_height(self):
        """Розрахунок максимальної висоти підйому (H)"""
        return (self.v0 ** 2 * (np.sin(self.alpha_rad) ** 2)) / (2 * self.g)

    def generate_trajectory(self, num_points=100):
        """
        Генерує масиви часу та координат для побудови графіка/анімації.
        num_points - кількість кадрів (точок) траєкторії.
        """
        t_max = self.get_max_time()

        # створює масив часу: від 0 до t_max, розбитий на num_points рівних частин
        t_array = np.linspace(0, t_max, num_points)

        # розраховує X та Y для кожного моменту часу t
        x_array = self.v0 * np.cos(self.alpha_rad) * t_array
        y_array = self.v0 * np.sin(self.alpha_rad) * t_array - 0.5 * self.g * t_array ** 2

        # захист від похибок: щоб тіло не провалювалося під землю (y < 0)
        y_array = np.maximum(y_array, 0)

        return t_array, x_array, y_array
