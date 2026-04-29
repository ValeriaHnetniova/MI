import customtkinter as ctk
from data_provider import DataProvider
from gui_view import KnapsackAppView
import solvers


class MainController:
    def __init__(self):
        self.root = ctk.CTk()

        defaults = DataProvider.get_defaults()
        self.view = KnapsackAppView(self.root, self.execute_logic, defaults)

        self.methods = [
            solvers.brute_force_solver,
            solvers.recursive_solver,
            solvers.greedy_solver,
            solvers.dp_solver,
            solvers.branch_and_bound_solver
        ]

    def execute_logic(self, w_str, weights_str, values_str, m_idx):
        # 1. Парсинг та валідація
        success, result = DataProvider.parse_input(w_str, weights_str, values_str)

        if not success:
            self.view.update_result_text(f"ПОМИЛКА:\n{result}")
            return

        W, weights, values, n = result

        # 2. Обчислення
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
            f"> Загальна вага обраних предметів: {total_w} / {W}\n"
            f"> Індекси обраних предметів (від 1 до n): {[i + 1 for i in items]}\n"
            f"----------------------"
        )

        # 4. Передача в GUI
        self.view.update_result_text(report)
        self.view.render_grid(matrix, W, n)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainController()
    app.run()