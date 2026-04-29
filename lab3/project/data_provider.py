class DataProvider:
    @staticmethod
    def parse_input(w_str, weights_str, values_str):
        """Перетворює рядки з GUI у числів масиви для алгоритмів"""
        try:
            W = int(w_str.strip())
            # Розбиває рядок по комі, прибирає пробіли і перетворює в int
            weights = [int(x.strip()) for x in weights_str.split(',') if x.strip()]
            values = [int(x.strip()) for x in values_str.split(',') if x.strip()]

            if len(weights) != len(values):
                return False, "Кількість ваг ({}) не збігається з кількістю цінностей ({})".format(len(weights),
                                                                                                    len(values))

            if not weights:
                return False, "Список предметів порожній"

            return True, (W, weights, values, len(weights))
        except ValueError:
            return False, "Некоректний формат. Вводьте лише цілі числа. Масиви розділяйте комами."

    @staticmethod
    def get_defaults():
        """Повертає дані Варіанту 11 для автоматичного заповнення при старті"""
        return {
            "W": "24",
            "weights": "9, 3, 3, 3, 5, 8, 9",
            "values": "11, 10, 6, 4, 15, 3, 12"
        }