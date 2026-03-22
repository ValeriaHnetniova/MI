import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button


class SimulationUI:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        plt.subplots_adjust(left=0.08, bottom=0.1, right=0.75, top=0.92)

        self.ax.set_title("Моделювання прямолінійного руху")
        self.ax.set_xlabel("Відстань (м)")
        self.ax.set_ylabel("Висота (м)")
        self.ax.grid(True, linestyle='--', alpha=0.6)

        panel_x = 0.82
        input_w = 0.12
        input_h = 0.05
        start_y = 0.85
        step_h = 0.08

        self.fig.text(panel_x - 0.02, 0.93, "Параметри", fontsize=14, fontweight='bold')

        self.inputs = {}

        labels = ['x0', 'y0', 'v0', 'a', 'Кут']
        default_vals = ['0', '0', '10', '0', '45']

        for i, (label, val) in enumerate(zip(labels, default_vals)):
            ax_box = plt.axes([panel_x, start_y - i * step_h, input_w, input_h])
            self.inputs[label] = TextBox(ax_box, f'{label}: ', initial=val)
            self.inputs[label].label.set_position((-0.3, 0.5))

        self.ax_draw_btn = plt.axes([panel_x - 0.02, 0.3, input_w + 0.04, 0.08])
        self.btn_draw = Button(self.ax_draw_btn, 'Малювати', color='lightgreen')

        self.ax_clear_btn = plt.axes([panel_x - 0.02, 0.2, input_w + 0.04, 0.08])
        self.btn_clear = Button(self.ax_clear_btn, 'Очистити', color='salmon')

        # колір за замовчуванням (поки не реалізовано вибору кольору)
        self.current_color = 'blue'

    def show(self):
        plt.show()

