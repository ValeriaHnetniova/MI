import numpy as np

class DataProvider:
    def __init__(self):
        # Структура даних (dictionary) згідно з ТЗ
        self.datasets = {
            "Набір 1 (5 точок)": {
                "x": np.array([1, 2, 3, 4, 5]),
                "y": np.array([1.1, 1.4, 1.7, 2.1, 2.3]),
                "degree": 1
            },
            "Набір 2 (10 точок)": {
                "x": np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                "y": np.array([1, 1.41, 1.73, 2, 2.24, 2.45, 2.64, 2.82, 3.0, 3.16]),
                "degree": 2
            },
            "Набір 3 (20 точок - коливання)": {
                "x": np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5,
                               5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5]),
                "y": np.array([2.0, 2.1, 1.9, 2.3, 1.8, 2.4, 1.7, 2.5, 1.6, 2.6,
                               1.5, 2.7, 1.4, 2.8, 1.3, 2.9, 1.2, 3.0, 1.1, 3.1]),
                "degree": 3
            }
        }
        # Для етапу прототипування беремо найскладніший набір на 20 точок
        self.current_data = self.datasets["Набір 3 (20 точок - коливання)"]

    def get_data(self):
        return self.current_data['x'], self.current_data['y'], self.current_data['degree']