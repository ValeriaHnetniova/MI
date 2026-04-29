import queue


def brute_force_solver(W, weights, values, n):
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
    items = [(values[i] / weights[i], weights[i], values[i], i) for i in range(n)]
    items.sort(key=lambda x: x[0], reverse=True)
    current_w = 0
    max_val = 0
    best_items = []
    for _, w, v, index in items:
        if current_w + w <= W:
            current_w += w
            max_val += v
            best_items.append(index)
    best_items.sort()
    return max_val, current_w, best_items, None


def dp_solver(W, weights, values, n):
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]
    max_val = dp[n][W]
    current_W = W
    best_items = []
    for i in range(n, 0, -1):
        if max_val <= 0: break
        if max_val != dp[i - 1][current_W]:
            best_items.append(i - 1)
            max_val -= values[i - 1]
            current_W -= weights[i - 1]
    best_items.sort()
    final_val = dp[n][W]
    total_w = sum(weights[i] for i in best_items)
    return final_val, total_w, best_items, dp


def branch_and_bound_solver(W, weights, values, n):
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
        if v.bound > max_profit: q.put(v)
        v_without = Node(u.level + 1, u.profit, u.weight)
        v_without.items = u.items.copy()
        v_without.bound = bound(v_without, n, W, items)
        if v_without.bound > max_profit: q.put(v_without)

    best_items_mapped.sort()
    total_w = sum(weights[i] for i in best_items_mapped)
    return max_profit, total_w, best_items_mapped, None