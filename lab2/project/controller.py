import tkinter as tk
from model import ProjectileModel
from view import ProjectileView


class ProjectileController:
    """
    Головний клас (Controller).
    Керує GUI-вікном, обробляє натискання кнопок та зв'язує View з Model.
    """

    def __init__(self):
        self.root = tk.Tk()

        # Передає у View посилання на вікно та функції, які треба викликати при натисканні кнопок
        self.view = ProjectileView(self.root, on_draw_callback=self.on_draw, on_clear_callback=self.on_clear)

    def on_draw(self):
        """Викликається при натисканні кнопки 'Малювати'"""
        # 1. Отримує текст з полів вводу
        v0_str, alpha_str = self.view.get_inputs()

        # 2. Валідація даних
        try:
            v0 = float(v0_str.replace(',', '.'))
            alpha = float(alpha_str.replace(',', '.'))

            if v0 <= 0:
                self.view.show_error("Помилка: Швидкість має бути більшою за нуль")
                return
            if not (0 < alpha < 90):
                self.view.show_error("Помилка: Кут має бути в межах від 1 до 89 градусів")
                return
        except ValueError:
            self.view.show_error("Помилка: Введіть коректні числові значення")
            return

        # 3. Передає правильні дані в Модель для розрахунків
        model = ProjectileModel(v0, alpha)

        t_max = model.get_max_time()
        l_max = model.get_max_distance()
        h_max = model.get_max_height()

        # 4. Оновлює текст з результатами на панелі
        self.view.update_results(t_max, l_max, h_max)

        # 5. Генерує координати і запускає анімацію на графіку
        t_arr, x_arr, y_arr = model.generate_trajectory(num_points=120)
        self.view.start_animation(t_arr, x_arr, y_arr, l_max, h_max)

    def on_clear(self):
        """Викликається при натисканні кнопки 'Очистити'"""
        self.view.reset_plot()
        self.view.lbl_results.config(text="Введіть дані та\nнатисніть 'Малювати'")

    def run(self):
        """Запуск безкінечного циклу відображення вікна"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ProjectileController()
    app.run()