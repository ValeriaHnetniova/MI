import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from tkinter import colorchooser, Tk
from physics import PhysicalBody
from ui_view import SimulationUI


class SimulationController:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        self.ui = SimulationUI()

        self.ui.btn_draw.on_clicked(self.start_animation)
        self.ui.btn_clear.on_clicked(self.clear)
        self.ui.btn_color.on_clicked(self.choose_color)

        self.lines = []
        self.ani = None

    def choose_color(self, _):
        color = colorchooser.askcolor(title="Вибери колір")[1]
        if color:
            self.ui.current_color = color
            self.ui.btn_color.color = color
            plt.draw()

    def start_animation(self, _):
        try:
            d = {k: v.text for k, v in self.ui.inputs.items()}
            body = PhysicalBody(float(d['x0']), float(d['y0']), float(d['v0']), float(d['a']), float(d['Кут']))

            line, = self.ui.ax.plot([], [], color=self.ui.current_color, lw=2, label=f"v={d['v0']}, a={d['a']}")

            point, = self.ui.ax.plot([], [], marker='o', ms=10, color=self.ui.current_color)

            self.lines.extend([line, point])
            self.ui.ax.legend(loc='upper left')

            def update(frame):
                # frame від 0 до 20
                t = np.linspace(0, frame / 4, frame + 1)
                x, y = body.calculate(t)

                line.set_data(x, y)
                if len(x) > 0:
                    point.set_data([x[-1]], [y[-1]])  # малює тільки одну точку в кінці

                self.ui.ax.relim()
                self.ui.ax.autoscale_view()
                return line, point

            # невелика пауза перед стартом
            plt.pause(0.1)

            self.ani = FuncAnimation(
                self.ui.fig, update, frames=20, interval=40,
                blit=True, repeat=False, cache_frame_data=False
            )
            plt.draw()

        except ValueError:
            print("Помилка даних")

    def clear(self, _):
        for obj in self.lines:
            obj.remove()
        self.lines.clear()
        if self.ui.ax.get_legend():
            self.ui.ax.get_legend().remove()
        plt.draw()


if __name__ == "__main__":
    app = SimulationController()
    plt.show()