import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class ProjectileView:
    """
    Клас, що відповідає за візуалізацію (View).
    Ітерація 3: Динамічна анімація польоту (FuncAnimation).
    """

    def __init__(self, max_distance, max_height):
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.ax.set_title("Анімація руху тіла, кинутого під кутом до горизонту")
        self.ax.set_xlabel("Відстань X (м)")
        self.ax.set_ylabel("Висота Y (м)")

        # жорсткі межі, щоб графік не масштабувався під час анімації
        self.ax.set_xlim(0, max_distance * 1.05)
        self.ax.set_ylim(0, max_height * 1.15)
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # створює порожні графічні об'єкти, які будемо рухати:
        # 1. синя пунктирна лінія (слід від траєкторії)
        self.trail, = self.ax.plot([], [], 'b--', alpha=0.6, label="Траєкторія")
        # 2. червона точка (саме тіло)
        self.body, = self.ax.plot([], [], 'ro', markersize=8, label="Тіло")

        self.ax.legend()

    def animate(self, x_array, y_array, interval=30):
        """Головна функція для запуску анімації"""

        def init():
            """Початковий (порожній) кадр"""
            self.trail.set_data([], [])
            self.body.set_data([], [])
            return self.trail, self.body

        def update(frame):
            """
            Функція малювання одного кадру.
            frame - це індекс (від 0 до кінця масиву координат).
            """
            # малює хвіст від початку [0] до поточного кадру [frame]
            self.trail.set_data(x_array[:frame + 1], y_array[:frame + 1])
            # малює тіло тільки в поточній точці [frame]
            self.body.set_data([x_array[frame]], [y_array[frame]])

            return self.trail, self.body

        self.ani = FuncAnimation(self.fig, update, frames=len(x_array),
                                 init_func=init, blit=True,
                                 interval=interval, repeat=False)

        plt.show()