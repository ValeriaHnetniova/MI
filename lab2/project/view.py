import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation


class ProjectileView:
    """
    Клас візуалізації (View).
    ФІнальна версія.
    """

    def __init__(self, root, on_draw_callback, on_clear_callback):
        self.root = root
        self.root.title("Моделювання руху тіла (ЛР №2)")
        self.root.geometry("950x550")

        # Ліва панель(графік)
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Права панель(управління)
        self.control_frame = tk.Frame(self.root, width=250, bg="#e6e6e6", padx=15, pady=15)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.control_frame, text="Панель управління", font=("Arial", 12, "bold"), bg="#e6e6e6").pack(
            pady=(0, 15))

        tk.Label(self.control_frame, text="Швидкість (v0, м/с):", bg="#e6e6e6").pack(anchor="w")
        self.entry_v0 = tk.Entry(self.control_frame)
        self.entry_v0.pack(fill=tk.X, pady=(0, 10))
        self.entry_v0.insert(0, "20")

        tk.Label(self.control_frame, text="Кут (alpha, градуси):", bg="#e6e6e6").pack(anchor="w")
        self.entry_alpha = tk.Entry(self.control_frame)
        self.entry_alpha.pack(fill=tk.X, pady=(0, 15))
        self.entry_alpha.insert(0, "45")

        self.btn_draw = tk.Button(self.control_frame, text="Малювати", command=on_draw_callback, bg="#4CAF50",
                                  fg="white", font=("Arial", 10, "bold"))
        self.btn_draw.pack(fill=tk.X, pady=5)

        self.btn_clear = tk.Button(self.control_frame, text="Очистити", command=on_clear_callback, bg="#f44336",
                                   fg="white", font=("Arial", 10, "bold"))
        self.btn_clear.pack(fill=tk.X, pady=5)

        self.lbl_results = tk.Label(self.control_frame, text="Введіть дані та\nнатисніть 'Малювати'", bg="#e6e6e6",
                                    justify=tk.LEFT, anchor="w", font=("Arial", 10))
        self.lbl_results.pack(fill=tk.X, pady=20)

        self.ani = None
        self.current_x_arr = None  # координати останнього запуску
        self.current_y_arr = None

        self.global_max_x = 10  # глобальні межі графіка
        self.global_max_y = 10

        self.reset_plot(initial=True)

    def get_inputs(self):
        return self.entry_v0.get(), self.entry_alpha.get()

    def show_error(self, message):
        messagebox.showerror("Помилка вводу", message)

    def update_results(self, t, l, h):
        res_text = f"Час польоту: {t:.2f} с\nДальність: {l:.2f} м\nВисота: {h:.2f} м"
        self.lbl_results.config(text=res_text)

    def reset_plot(self, initial=False):
        """Повністю очищає графік і стирає історію"""
        if self.ani is not None and self.ani.event_source is not None:
            self.ani.event_source.stop()

        self.ax.clear()
        self.ax.set_title("Анімація руху тіла", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Відстань X (м)")
        self.ax.set_ylabel("Висота Y (м)")
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # Скидає глобальні межі
        self.global_max_x = 10
        self.global_max_y = 10
        self.ax.set_xlim(0, self.global_max_x)
        self.ax.set_ylim(0, self.global_max_y)

        # Створює графічні об'єкти для поточної анімації
        self.trail, = self.ax.plot([], [], 'b-', alpha=0.8, linewidth=2, label="Поточний політ")
        self.body, = self.ax.plot([], [], 'ro', markersize=8, markeredgecolor='black', label="Тіло")
        self.info_text = self.ax.text(0.02, 0.85, '', transform=self.ax.transAxes, fontsize=10,
                                      bbox=dict(facecolor='white', alpha=0.9))

        self.ax.legend(loc="upper right")

        # Скидає історію
        self.current_x_arr = None
        self.current_y_arr = None

        if not initial:
            self.canvas.draw()

    def start_animation(self, t_arr, x_arr, y_arr, max_x, max_y):
        """Додає попередню лінію в історію і запускає нову анімацію"""
        if self.ani is not None and self.ani.event_source is not None:
            self.ani.event_source.stop()

        # 1. Збереження історії, малює сірим пунктиром
        if self.current_x_arr is not None:
            self.ax.plot(self.current_x_arr, self.current_y_arr, color='gray', alpha=0.4, linestyle='--', linewidth=1.5)

        self.current_x_arr = x_arr
        self.current_y_arr = y_arr

        # 2. Розширює межі осей
        if max_x > self.global_max_x or self.global_max_x == 10:
            self.global_max_x = max_x
        if max_y > self.global_max_y or self.global_max_y == 10:
            self.global_max_y = max_y

        self.ax.set_xlim(0, self.global_max_x * 1.05)
        self.ax.set_ylim(0, self.global_max_y * 1.15)

        # Очищає попередню синю лінію та кульку перед новим стартом
        self.trail.set_data([], [])
        self.body.set_data([], [])
        self.canvas.draw()

        # 3. Запуск анімації
        def init():
            self.trail.set_data([], [])
            self.body.set_data([], [])
            self.info_text.set_text('')
            return self.trail, self.body, self.info_text

        def update(frame):
            self.trail.set_data(x_arr[:frame + 1], y_arr[:frame + 1])
            self.body.set_data([x_arr[frame]], [y_arr[frame]])
            self.info_text.set_text(f"Час: {t_arr[frame]:.2f} c\nX: {x_arr[frame]:.2f} м\nY: {y_arr[frame]:.2f} м")
            return self.trail, self.body, self.info_text

        self.ani = FuncAnimation(self.fig, update, frames=len(x_arr), init_func=init, blit=True, interval=25,
                                 repeat=False)
        self.canvas.draw()