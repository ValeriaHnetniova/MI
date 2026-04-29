import customtkinter as ctk
from data_provider import DataProvider
from gui_view import KnapsackAppView
import solvers


class MainController:
    """
    Головний контролер програми. Відповідає за зв'язок між графічним інтерфейсом
    (View) та обчислювальними алгоритмами (Model).
    Реалізує патерн проєктування 'Стратегія' (Strategy).
    """

    def __init__(self):
        """
        Ініціалізує вікно програми, завантажує стандартні дані та формує
        список алгоритмів-стратегій для вирішення задачі.
        """
        self.root = ctk.CTk()

        defaults = DataProvider.get_defaults()
        self.view = KnapsackAppView(self.root, self.execute_logic, defaults)

        # Патерн "Стратегія": сімейство взаємозамінних алгоритмів
        # з однаковим інтерфейсом (вхідними аргументами та типом результату)
        self.methods = [
            solvers.brute_force_solver,
            solvers.recursive_solver,
            solvers.greedy_solver,
            solvers.dp_solver,
            solvers.branch_and_bound_solver
        ]

    def execute_logic(self, w_str, weights_str, values_str, m_idx):
        """
        Основний метод виконання бізнес-логіки. Викликається по натисканню
        кнопки в GUI. Парсить дані, обирає потрібну стратегію та формує звіт.

        Args:
            w_str (str): Введена користувачем місткість рюкзака.
            weights_str (str): Введені користувачем ваги.
            values_str (str): Введені користувачем цінності.
            m_idx (int): Індекс обраного методу (стратегії) з випадного списку.
        """
        # 1. Парсинг та валідація
        success, result = DataProvider.parse_input(w_str, weights_str, values_str)

        if not success:
            self.view.update_result_text(f"ПОМИЛКА:\n{result}")
            return

        W, weights, values, n = result

        # 2. Обчислення (Виклик конкретної стратегії за індексом)
        solver = self.methods[m_idx]
        max_v, total_w, items, matrix = solver(W, weights, values, n)

        # 3. Формування звіту
        method_name = self.view.methods_list[m_idx]
        report = (
            f"--- ЗВІТ ОБЧИСЛЕНЬ ---\n"
            f"Метод: {method_name}\n"
            f"Вхідні дані: Місткість (W) = {W}, Кількість предметів (n) = {n}\n"
            f"----------------------\n"
            f"РЕЗУЛЬТАТ:\n"
            f"> Максимальна сумарна цінність: {max_v}\n"
            f"> Загальна вага обраних предметів: {total_w}\n"
            f"> Індекси обраних предметів (нумерація з 0): {items}\n"
            f"----------------------"
        )

        self.view.update_result_text(report)
        self.view.render_grid(matrix, W, n)

    def run(self):
        """Запускає головний цикл обробки подій графічного вікна."""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainController()
    app.run()