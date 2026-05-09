import matplotlib.pyplot as plt


class VisualizationModule:
    def __init__(self):
        # Проєктування Layout: ax1 (75%), ax2 (25%)
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
        self.fig.subplots_adjust(hspace=0.3)

        # Головна зона (ax1)
        self.ax1.set_title("Прототип: Апроксимація функцій (Лагранж та МНК)")
        self.ax1.set_ylabel("Значення Y")
        self.ax1.grid(True, linestyle=':', alpha=0.7)

        # Зона залишків (ax2)
        self.ax2.set_title("Діаграма залишків (r_i)")
        self.ax2.set_xlabel("Координата X")
        self.ax2.set_ylabel("Похибка")
        self.ax2.grid(True, linestyle=':', alpha=0.7)
        self.ax2.axhline(0, color='black', linewidth=1)  # Базова лінія відліку

    def render_prototype(self, x, y, x_dense, y_lagrange_stub, y_lsm_stub, residuals_stub):

        # 1. Точки — чорні крапки ('ko')
        self.ax1.plot(x, y, 'ko', markersize=6, label='Експериментальні точки')

        # 2. Інтерполяція Лагранжа — зелена пунктирна лінія ('g--')
        self.ax1.plot(x_dense, y_lagrange_stub, 'g--', linewidth=1.5, label='Лагранж (Заглушка)')

        # 3. МНК — товста червона суцільна лінія ('r-')
        self.ax1.plot(x_dense, y_lsm_stub, 'r-', linewidth=2.5, label='МНК (Заглушка)')

        self.ax1.legend(loc="upper right")

        # 4. Штрих-графік залишків у нижній зоні
        self.ax2.stem(x, residuals_stub, linefmt='orange', markerfmt='D', basefmt='black')

        plt.show()