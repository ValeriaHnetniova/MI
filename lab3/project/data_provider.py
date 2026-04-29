class DataProvider:
    """
    Клас, що відповідає за надання початкових даних та валідацію вводу користувача.
    Діє як проміжний шар між графічним інтерфейсом та алгоритмічним ядром.
    """

    @staticmethod
    def parse_input(w_str, weights_str, values_str):
        """
        Перетворює рядкові дані з графічного інтерфейсу у числові масиви для алгоритмів.
        Виконує валідацію на некоректні символи та відповідність розмірностей масивів.

        Args:
            w_str (str): Рядок із загальною місткістю рюкзака.
            weights_str (str): Рядок із вагами предметів, розділеними комами.
            values_str (str): Рядок із цінностями предметів, розділеними комами.

        Returns:
            tuple: (success (bool), result (tuple або str)).
                   Якщо успішно: (True, (W, weights, values, n)).
                   Якщо помилка: (False, "Текст помилки").
        """
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
        """
        Повертає параметри Варіанту 11 для автоматичного заповнення полів при старті програми.

        Returns:
            dict: Словник з ключами "W", "weights" та "values".
        """
        return {
            "W": "24",
            "weights": "9, 3, 3, 3, 5, 8, 9",
            "values": "11, 10, 6, 4, 15, 3, 12"
        }