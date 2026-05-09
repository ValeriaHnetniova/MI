import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, TextBox
from matplotlib.animation import FuncAnimation

from data_provider import DataProvider
from math_engine import MathEngine
from visualization_module import VisualizationModule


class AnimationController:
    def __init__(self):
        self.data_provider = DataProvider()
        self.math_engine = MathEngine()
        self.vis = VisualizationModule()

        self.current_dataset_name = "Набір 1 (5 точок)"
        self.x, self.y = self.data_provider.get_data(self.current_dataset_name)
        self.degree = 3
        self.mode = 'Усі'
        self.anim = None

        self.setup_ui()
        self.update_plot()

    def stop_animation(self):
        """БЕЗПЕЧНА зупинка анімації. Виправляє помилку 'NoneType'."""
        if self.anim is not None and self.anim.event_source is not None:
            self.anim.event_source.stop()
        self.anim = None

    def setup_ui(self):
        # Вибір даних
        ax_data = self.vis.fig.add_axes([0.82, 0.78, 0.16, 0.15], facecolor='#111827')
        self.radio_data = RadioButtons(ax_data, list(self.data_provider.datasets.keys()))
        for l in self.radio_data.labels: l.set_color('white')
        self.radio_data.on_clicked(self.change_dataset)

        # Вибір режиму
        ax_mode = self.vis.fig.add_axes([0.82, 0.60, 0.16, 0.12], facecolor='#111827')
        self.radio_mode = RadioButtons(ax_mode, ('Інтерполяція', 'МНК', 'Усі'), active=2)
        for l in self.radio_mode.labels: l.set_color('white')
        self.radio_mode.on_clicked(self.change_mode)

        # Степінь МНК
        ax_deg = self.vis.fig.add_axes([0.88, 0.52, 0.06, 0.04])
        self.text_deg = TextBox(ax_deg, 'Степінь: ', initial=str(self.degree), color='#111827')
        self.text_deg.label.set_color('white')
        self.text_deg.on_submit(self.change_degree)

        # Кнопки анімації
        ax_b1 = self.vis.fig.add_axes([0.82, 0.38, 0.16, 0.05])
        self.btn_lag = Button(ax_b1, 'Анімація Лагранжа', color='#111827', hovercolor='#ff00ff')
        self.btn_lag.label.set_color('white')
        self.btn_lag.on_clicked(self.animate_lagrange)

        ax_b2 = self.vis.fig.add_axes([0.82, 0.31, 0.16, 0.05])
        self.btn_lsm = Button(ax_b2, 'Анімація МНК', color='#111827', hovercolor='#ff3366')
        self.btn_lsm.label.set_color('white')
        self.btn_lsm.on_clicked(self.animate_lsm)

        # Кнопка: Очистити
        ax_clear = self.vis.fig.add_axes([0.82, 0.20, 0.16, 0.05])
        self.btn_clear = Button(ax_clear, 'ОЧИСТИТИ ВСЕ', color='#374151', hovercolor='#ef4444')
        self.btn_clear.label.set_color('white')
        self.btn_clear.on_clicked(self.clear_all_handler)

    def clear_all_handler(self, event):
        self.stop_animation()
        self.vis.ax_main.clear()
        self.vis.ax_res.clear()
        self.vis.setup_axes()
        self.vis.fig.canvas.draw_idle()

    def change_dataset(self, label):
        self.current_dataset_name = label
        self.x, self.y = self.data_provider.get_data(label)
        self.update_plot()

    def change_mode(self, label):
        self.mode = label
        self.update_plot()

    def change_degree(self, text):
        try:
            self.degree = int(text)
            self.update_plot()
        except:
            pass

    def update_plot(self):
        self.stop_animation()
        self.vis.ax_main.clear()
        self.vis.ax_res.clear()
        self.vis.setup_axes()

        self.vis.ax_main.scatter(self.x, self.y, c=self.vis.colors['points'], s=80, zorder=5, label='Дані')
        x_dense = np.linspace(min(self.x), max(self.x), 400)

        if self.mode in ['Інтерполяція', 'Усі']:
            p = self.math_engine.calculate_lagrange(self.x, self.y)
            self.vis.ax_main.plot(x_dense, p(x_dense), '--', color=self.vis.colors['lagrange'], label='Лагранж')

        if self.mode in ['МНК', 'Усі']:
            p = self.math_engine.calculate_lsm(self.x, self.y, self.degree)
            self.vis.ax_main.plot(x_dense, p(x_dense), '-', color=self.vis.colors['lsm'], lw=2, label='МНК')
            res = self.math_engine.calculate_residuals(self.y, p(self.x))
            self.vis.ax_res.stem(self.x, res, linefmt='y:', markerfmt='yo')

        self.vis.ax_main.legend()
        self.vis.fig.canvas.draw_idle()

    def animate_lagrange(self, event):
        self.update_plot()
        line, = self.vis.ax_main.plot([], [], '--', color=self.vis.colors['lagrange'])
        x_dense = np.linspace(min(self.x), max(self.x), 400)

        def up(f):
            if f > 0:
                p = self.math_engine.calculate_lagrange(self.x[:f + 1], self.y[:f + 1])
                line.set_data(x_dense, p(x_dense))
            return line,

        self.anim = FuncAnimation(self.vis.fig, up, frames=len(self.x), interval=600, blit=True, repeat=False)

    def animate_lsm(self, event):
        self.update_plot()
        line, = self.vis.ax_main.plot([], [], '-', color=self.vis.colors['lsm'], lw=3)
        x_dense = np.linspace(min(self.x), max(self.x), 400)
        f_coefs = np.polyfit(self.x, self.y, self.degree)
        s_coefs = np.zeros_like(f_coefs);
        s_coefs[-1] = np.mean(self.y)

        def up(f):
            t = f / 29
            p = np.poly1d((1 - t) * s_coefs + t * f_coefs)
            line.set_data(x_dense, p(x_dense))
            return line,

        self.anim = FuncAnimation(self.vis.fig, up, frames=30, interval=40, blit=True, repeat=False)


if __name__ == '__main__':
    app = AnimationController()
    plt.show()