from model import ProjectileModel
from view import ProjectileView


class ProjectileController:
    """
    Головний клас управління програмою (Controller в архітектурі MVC).
    Ітерація 2: Перевірка базової візуалізації.
    """

    def __init__(self):
        print("=" * 45)
        print("  ПРОГРАМА МОДЕЛЮВАННЯ РУХУ ТІЛА (MVP)")
        print("=" * 45)

    def run(self):
        # 1. зчитування даних (поки що без складної обробки помилок)
        v0 = float(input("Введіть початкову швидкість (v0, м/с): "))
        alpha = float(input("Введіть кут кидання (alpha, градуси): "))

        # 2. робота Моделі
        model = ProjectileModel(v0, alpha)

        print("\nВиконуємо розрахунки...")
        print(f"Дальність: {model.get_max_distance():.2f} м, Висота: {model.get_max_height():.2f} м")

        t_arr, x_arr, y_arr = model.generate_trajectory(num_points=100)

        # 3. робота Вигляду (View) - Статичний графік
        view = ProjectileView(model.get_max_distance(), model.get_max_height())

        print("Відкриваємо вікно з графіком...")
        view.plot_static_trajectory(x_arr, y_arr)


if __name__ == "__main__":
    app = ProjectileController()
    app.run()