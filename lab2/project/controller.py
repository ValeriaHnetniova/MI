from model import ProjectileModel
from view import ProjectileView


class ProjectileController:
    """
    Головний клас управління програмою (Controller в архітектурі MVC).
    Ітерація 3: Запуск розрахунків та передача даних на анімацію.
    """

    def __init__(self):
        print("=" * 45)
        print("  ПРОГРАМА МОДЕЛЮВАННЯ РУХУ ТІЛА (MVP)")
        print("=" * 45)

    def run(self):
        try:
            v0 = float(input("Введіть початкову швидкість (v0, м/с): "))
            alpha = float(input("Введіть кут кидання (alpha, градуси): "))
        except ValueError:
            print("Помилка: введено некоректні дані. Будь ласка, введіть числа.")
            return

        model = ProjectileModel(v0, alpha)

        print("\n--- Результати ---")
        print(f"Час польоту:  {model.get_max_time():.2f} с")
        print(f"Дальність:    {model.get_max_distance():.2f} м")
        print(f"Макс. висота: {model.get_max_height():.2f} м")
        print("------------------\nЗапуск анімації...")

        # генерує 100 точок для плавної анімації
        t_arr, x_arr, y_arr = model.generate_trajectory(num_points=100)

        view = ProjectileView(model.get_max_distance(), model.get_max_height())

        view.animate(x_arr, y_arr, interval=30)

        print("Анімацію завершено.")


if __name__ == "__main__":
    app = ProjectileController()
    app.run()