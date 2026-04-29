import queue


def brute_force_solver(W, weights, values, n):
    """
    Розв'язує задачу 0/1 рюкзака методом повного перебору (Brute Force).
    Перевіряє всі можливі 2^n комбінації предметів за допомогою бітових масок.

    Args:
        W (int): Максимальна місткість рюкзака.
        weights (list): Список ваг предметів.
        values (list): Список цінностей предметів.
        n (int): Кількість предметів.

    Returns:
        tuple: (max_val (int), total_w (int), best_items (list), matrix (None)).
    """
    max_val = 0
    best_items = []
    for i in range(1 << n):
        current_weight = 0
        current_value = 0
        current_combination = []
        for j in range(n):
            if (i & (1 << j)):
                current_weight += weights[j]
                current_value += values[j]
                current_combination.append(j)
        if current_weight <= W and current_value > max_val:
            max_val = current_value
            best_items = current_combination
    total_w = sum(weights[i] for i in best_items)
    return max_val, total_w, best_items, None


def recursive_solver(W, weights, values, n):
    """
    Розв'язує задачу 0/1 рюкзака методом чистої рекурсії.
    Для кожного предмета розглядає дві гілки: предмет взято або пропущено.

    Args:
        W (int): Максимальна місткість рюкзака.
        weights (list): Список ваг предметів.
        values (list): Список цінностей предметів.
        n (int): Кількість предметів.

    Returns:
        tuple: (max_val (int), total_w (int), best_items (list), matrix (None)).
    """

    def solve(curr_W, index):
        if index < 0 or curr_W == 0:
            return 0, []
        if weights[index] > curr_W:
            return solve(curr_W, index - 1)
        val_without, items_without = solve(curr_W, index - 1)
        val_with, items_with = solve(curr_W - weights[index], index - 1)
        val_with += values[index]
        if val_with > val_without:
            return val_with, items_with + [index]
        else:
            return val_without, items_without

    max_val, best_items = solve(W, n - 1)
    best_items.sort()
    total_w = sum(weights[i] for i in best_items)
    return max_val, total_w, best_items, None


def greedy_solver(W, weights, values, n):
    """
    Наближено розв'язує задачу 0/1 рюкзака жадібним алгоритмом (Greedy).
    Предмети сортуються за спаданням питомої цінності (v/w) і додаються до заповнення рюкзака.

    Args:
        W (int): Максимальна місткість рюкзака.
        weights (list): Список ваг предметів.
        values (list): Список цінностей предметів.
        n (int): Кількість предметів.

    Returns:
        tuple: (total_value (int), total_weight (int), selected_items (list), matrix (None)).
    """
    items = [(values[i] / weights[i], weights[i], values[i], i) for i in range(n)]
    items.sort(key=lambda x: x[0], reverse=True)
    total_weight = 0
    total_value = 0
    selected_items = []
    for _, w, v, index in items:
        if total_weight + w <= W:
            total_weight += w
            total_value += v
            selected_items.append(index)
    selected_items.sort()
    return total_value, total_weight, selected_items, None


def dp_solver(W, weights, values, n):
    """
    Розв'язує задачу 0/1 рюкзака методом динамічного програмування (DP).
    Будує матрицю станів та відновлює набір предметів зворотним проходом (backtracking).

    Args:
        W (int): Максимальна місткість рюкзака.
        weights (list): Список ваг предметів.
        values (list): Список цінностей предметів.
        n (int): Кількість предметів.

    Returns:
        tuple: (max_val (int), total_weight (int), selected_items (list), dp_matrix (list of lists)).
               Цей метод єдиний повертає матрицю для відмальовування в GUI.
    """
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    max_val = dp[n][W]
    current_W = W
    selected_items = []
    for i in range(n, 0, -1):
        if max_val <= 0:
            break
        if max_val != dp[i - 1][current_W]:
            selected_items.append(i - 1)
            max_val -= values[i - 1]
            current_W -= weights[i - 1]

    selected_items.sort()
    total_weight = sum(weights[i] for i in selected_items)
    return dp[n][W], total_weight, selected_items, dp


def branch_and_bound_solver(W, weights, values, n):
    """
    Розв'язує задачу 0/1 рюкзака методом гілок і меж (Branch and Bound).
    Використовує дерево простору станів та функцію оцінки верхньої межі (bound)
    для відсікання неперспективних гілок.

    Args:
        W (int): Максимальна місткість рюкзака.
        weights (list): Список ваг предметів.
        values (list): Список цінностей предметів.
        n (int): Кількість предметів.

    Returns:
        tuple: (max_profit (int), total_weight (int), best_items_mapped (list), matrix (None)).
    """

    class Node:
        def __init__(self, level, profit, weight):
            self.level = level
            self.profit = profit
            self.weight = weight
            self.bound = 0
            self.items = []

    def bound(node, n, W, items):
        if node.weight >= W: return 0
        profit_bound = node.profit
        j = node.level + 1
        totweight = node.weight
        while j < n and totweight + items[j][1] <= W:
            totweight += items[j][1]
            profit_bound += items[j][2]
            j += 1
        if j < n:
            profit_bound += (W - totweight) * items[j][0]
        return profit_bound

    items = [(values[i] / weights[i], weights[i], values[i], i) for i in range(n)]
    items.sort(key=lambda x: x[0], reverse=True)
    q = queue.Queue()
    u = Node(-1, 0, 0)
    q.put(u)
    max_profit = 0
    best_items_mapped = []

    while not q.empty():
        u = q.get()
        if u.level == n - 1: continue

        v = Node(u.level + 1, u.profit + items[u.level + 1][2], u.weight + items[u.level + 1][1])
        v.items = u.items + [items[u.level + 1][3]]

        if v.weight <= W and v.profit > max_profit:
            max_profit = v.profit
            best_items_mapped = v.items

        v.bound = bound(v, n, W, items)
        if v.bound > max_profit:
            q.put(v)

        v_no = Node(u.level + 1, u.profit, u.weight)
        v_no.items = u.items
        v_no.bound = bound(v_no, n, W, items)
        if v_no.bound > max_profit:
            q.put(v_no)

    best_items_mapped.sort()
    total_weight = sum(weights[i] for i in best_items_mapped)
    return max_profit, total_weight, best_items_mapped, None