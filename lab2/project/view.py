import matplotlib.pyplot as plt


class ProjectileView:
    """
    Клас, що відповідає за візуалізацію (View в архітектурі MVC).
    """

    def __init__(self, max_distance, max_height):
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.ax.set_title("Траєкторія руху тіла (Статичний графік)")
        self.ax.set_xlabel("Відстань (м)")
        self.ax.set_ylabel("Висота (м)")

        # встановлює жорсткі межі осей, щоб графік мав правильні пропорції
        self.ax.set_xlim(0, max_distance * 1.1)
        self.ax.set_ylim(0, max_height * 1.2)

        self.ax.grid(True, linestyle='--', alpha=0.7)

    def plot_static_trajectory(self, x_array, y_array):
        """Функція для малювання статичної параболи"""
        # будуємо лінію за заданими масивами координат
        self.ax.plot(x_array, y_array, 'b-', linewidth=2, label="Траєкторія польоту")

        # позначає початкову і кінцеву точки
        self.ax.plot(x_array[0], y_array[0], 'go', label="Точка кидання")
        self.ax.plot(x_array[-1], y_array[-1], 'ro', label="Точка падіння")

        self.ax.legend()

        plt.show()