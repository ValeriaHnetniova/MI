'''
ФУНКЦІЯ BruteForce(W, w[], v[], n):
    max_value = 0
    best_combination = []

    // Перебирає всі 2^n варіантів (від 0 до 2^n - 1)
    ДЛЯ mask ВІД 0 ДО (2^n - 1):
        current_weight = 0
        current_value = 0
        current_combination = []

        ДЛЯ i ВІД 0 ДО n - 1:
            // Якщо i-тий біт у масці дорівнює 1
            ЯКЩО (mask має 1 на позиції i):
                current_weight = current_weight + w[i]
                current_value = current_value + v[i]
                current_combination.додати(i)

        // Перевіряє, чи влізли в рюкзак і чи це найкращий результат
        ЯКЩО (current_weight <= W) І (current_value > max_value):
            max_value = current_value
            best_combination = current_combination

    ПОВЕРНУТИ max_value, best_combination





ФУНКЦІЯ Recursive(W, w[], v[], n):
    // Базовий випадок
    ЯКЩО n == 0 АБО W == 0:
        ПОВЕРНУТИ 0

    // Якщо вага останнього предмета більша за залишок місця,
    // ми його точно не беремо
    ЯКЩО w[n-1] > W:
        ПОВЕРНУТИ Recursive(W, w[], v[], n-1)

    ІНАКШЕ:
        // Гілка 1: БЕРЕМО предмет (додаємо його цінність і зменшуємо W)
        value_with = v[n-1] + Recursive(W - w[n-1], w[], v[], n-1)

        // Гілка 2: НЕ БЕРЕМО предмет (W не змінюється)
        value_without = Recursive(W, w[], v[], n-1)

        ПОВЕРНУТИ Максимум(value_with, value_without)





ФУНКЦІЯ Greedy(W, w[], v[], n):
    Створити список items
    ДЛЯ i ВІД 0 ДО n - 1:
        питома_цінність = v[i] / w[i]
        items.додати( (w[i], v[i], i, питома_цінність) )

    Відсортувати items ЗА СПАДАННЯМ питомої_цінності

    current_weight = 0
    total_value = 0
    selected_items = []

    ДЛЯ КОЖНОГО item З items:
        ЯКЩО current_weight + item.вага <= W:
            current_weight = current_weight + item.вага
            total_value = total_value + item.цінність
            selected_items.додати(item.індекс)

    ПОВЕРНУТИ total_value, selected_items




ФУНКЦІЯ DP_Solver(W, w[], v[], n):
    // Ініціалізація матриці станів (n+1) рядків, (W+1) стовпців нулями
    Створити матрицю dp[n+1][W+1] = 0

    // Прямий прохід (Заповнення таблиці)
    ДЛЯ i ВІД 1 ДО n:
        ДЛЯ j ВІД 1 ДО W:
            ЯКЩО w[i-1] <= j: // Якщо предмет влазить у поточну вагу j
                dp[i][j] = Максимум( dp[i-1][j], v[i-1] + dp[i-1][ j - w[i-1] ] )
            ІНАКШЕ:
                dp[i][j] = dp[i-1][j]

    max_value = dp[n][W]

    // Зворотний прохід (Backtracking)
    current_W = W
    selected_items = []

    ДЛЯ i ВІД n ДО 1 З КРОКОМ -1:
        // Якщо значення змінилося порівняно з попереднім рядком,
        // значить ми взяли цей предмет
        ЯКЩО dp[i][current_W] != dp[i-1][current_W]:
            selected_items.додати(i-1)
            current_W = current_W - w[i-1]

    ПОВЕРНУТИ max_value, selected_items, dp (матрицю)




// Евристична функція розрахунку верхньої межі
ФУНКЦІЯ CalculateBound(node, W, n, items):
    ЯКЩО node.weight >= W: ПОВЕРНУТИ 0

    bound_value = node.profit
    total_weight = node.weight
    j = node.level + 1

    // Додає цілі предмети
    ПОКИ j < n І (total_weight + items[j].вага <= W):
        total_weight = total_weight + items[j].вага
        bound_value = bound_value + items[j].цінність
        j = j + 1

    // Додає дробову частину наступного предмета (якщо є)
    ЯКЩО j < n:
        bound_value = bound_value + (W - total_weight) * items[j].питома_цінність

    ПОВЕРНУТИ bound_value

// Основний алгоритм
ФУНКЦІЯ BranchAndBound(W, w[], v[], n):
    Відсортувати предмети за питомою цінністю
    Створити Чергу Q
    Створити вузол root(level=-1, profit=0, weight=0)
    Q.додати(root)

    max_profit = 0

    ПОКИ Q НЕ порожня:
        node = Q.вилучити_перший()
        ЯКЩО node.level == n - 1: ПРОДОВЖИТИ

        // Гілка 1: БЕРЕ наступний предмет
        left_child = Створити_вузол(level = node.level+1,
                                    profit = node.profit + v[left_child.level],
                                    weight = node.weight + w[left_child.level])

        ЯКЩО left_child.weight <= W І left_child.profit > max_profit:
            max_profit = left_child.profit

        left_child.bound = CalculateBound(left_child, W, n, items)
        // Відсікання (Pruning)
        ЯКЩО left_child.bound > max_profit:
            Q.додати(left_child)

        // Гілка 2: НЕ БЕРЕ предмет
        right_child = Створити_вузол(level = node.level+1,
                                     profit = node.profit,
                                     weight = node.weight)
        right_child.bound = CalculateBound(right_child, W, n, items)

        ЯКЩО right_child.bound > max_profit:
            Q.додати(right_child)

    ПОВЕРНУТИ max_profit
'''