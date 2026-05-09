import matplotlib.pyplot as plt


class VisualizationModule:
    def __init__(self):
        plt.style.use('dark_background')
        self.colors = {
            'bg': '#0b0f19', 'grid': '#1f2937',
            'points': '#00ffcc', 'lagrange': '#ff00ff',
            'lsm': '#ff3366', 'stem': '#ffff00', 'text': '#e5e7eb'
        }

        self.fig = plt.figure(figsize=(13, 8), facecolor=self.colors['bg'])
        self.fig.canvas.manager.set_window_title('Лабораторна 4: Апроксимація')

        self.ax_main = self.fig.add_axes([0.08, 0.45, 0.7, 0.5], facecolor=self.colors['bg'])
        self.ax_res = self.fig.add_axes([0.08, 0.15, 0.7, 0.25], facecolor=self.colors['bg'])
        self.setup_axes()

    def setup_axes(self):
        for ax in [self.ax_main, self.ax_res]:
            ax.tick_params(colors=self.colors['text'])
            ax.grid(True, color=self.colors['grid'], linestyle='--', alpha=0.6)
            for spine in ax.spines.values():
                spine.set_color(self.colors['grid'])
        self.ax_main.set_ylabel('Y', color=self.colors['text'])
        self.ax_res.set_ylabel('Залишки', color=self.colors['text'])