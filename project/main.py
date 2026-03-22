import matplotlib.pyplot as plt
from tkinter import colorchooser, Tk
from physics import PhysicalBody
from ui_view import SimulationUI


class SimulationController:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()

        self.ui = SimulationUI()

        self.ui.btn_draw.on_clicked(self.draw)
        self.ui.btn_clear.on_clicked(self.clear)
        self.ui.btn_color.on_clicked(self.choose_color)

        self.lines = []

    def choose_color(self, _):
        """Викликає системне вікно вибору кольору"""
        color = colorchooser.askcolor(title="Оберіть колір для наступної лінії")[1]
        if color:
            self.ui.current_color = color
            self.ui.btn_color.color = color
            plt.draw()

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

            line, = self.ui.ax.plot(x, y, color=self.ui.current_color, lw=2, label=f"v={d['v0']}, a={d['a']}")
            self.lines.append(line)

            # оновлює межі графіка, щоб він підлаштовувався під нові точки
            self.ui.ax.legend()
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
        if self.ui.ax.get_legend():
            self.ui.ax.get_legend().remove()
        plt.draw()


if __name__ == "__main__":
    app = SimulationController()
    plt.show()