import matplotlib.pyplot as plt
from physics import PhysicalBody
from ui_view import SimulationUI


class SimulationController:
    def __init__(self):
        self.ui = SimulationUI()

        self.ui.btn_draw.on_clicked(self.draw)
        self.ui.btn_clear.on_clicked(self.clear)

        self.lines = []

    def draw(self, _):
        """Зчитування даних та побудова графіка"""
        try:
            d = {k: v.text for k, v in self.ui.inputs.items()}

            body = PhysicalBody(
                float(d['x0']),
                float(d['y0']),
                float(d['v0']),
                float(d['a']),
                float(d['Кут'])
            )

            x, y = body.calculate()

            line, = self.ui.ax.plot(x, y, color='blue', lw=2)
            self.lines.append(line)

            # оновлює межі графіка, щоб він підлаштовувався під нові точки
            self.ui.ax.relim()
            self.ui.ax.autoscale_view()
            plt.draw()

        except ValueError:
            print("Помилка: введіть коректні числа в усі поля")

    def clear(self, _):
        """Видалення всіх намальованих ліній"""
        for line in self.lines:
            line.remove()
        self.lines.clear()
        plt.draw()


if __name__ == "__main__":
    app = SimulationController()
    plt.show()