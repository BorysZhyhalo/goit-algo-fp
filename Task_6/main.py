items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: dict, budget: int) -> tuple[list[str], int, int]:
    sorted_items = sorted(
        items.items(),
        key=lambda x: x[1]["calories"] / x[1]["cost"],
        reverse=True,
    )

    total_calories = 0
    total_cost = 0
    selected_items = []

    for item, details in sorted_items:
        if total_cost + details["cost"] <= budget:
            selected_items.append(item)
            total_calories += details["calories"]
            total_cost += details["cost"]

    return selected_items, total_calories, total_cost


def dynamic_programming(items: dict, budget: int) -> tuple[list[str], int, int]:
    item_list = list(items.items())
    n = len(item_list)
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        _, details = item_list[i - 1]
        cost = details["cost"]
        calories = details["calories"]

        for w in range(budget + 1):
            if cost <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - cost] + calories)
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            item_name, details = item_list[i - 1]
            selected_items.append(item_name)
            w -= details["cost"]

    selected_items.reverse()
    total_calories = dp[n][budget]
    total_cost = sum(items[item]["cost"] for item in selected_items)

    return selected_items, total_calories, total_cost


if __name__ == "__main__":
    budget = int(input("Введіть бюджет: "))

    greedy_result = greedy_algorithm(items, budget)
    dp_result = dynamic_programming(items, budget)

    print("\nЖадібний алгоритм:")
    print(f"Вибрані страви: {greedy_result[0]}")
    print(f"Загальна калорійність: {greedy_result[1]}")
    print(f"Загальна вартість: {greedy_result[2]}")

    print("\nДинамічне програмування:")
    print(f"Вибрані страви: {dp_result[0]}")
    print(f"Загальна калорійність: {dp_result[1]}")
    print(f"Загальна вартість: {dp_result[2]}")
