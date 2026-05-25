import random
from collections import Counter

import matplotlib.pyplot as plt

NUM_ROLLS = 100_000

# Аналітичні ймовірності: кількість комбінацій для кожної суми
ANALYTICAL_COUNTS = {
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 5,
    9: 4,
    10: 3,
    11: 2,
    12: 1,
}
TOTAL_OUTCOMES = 36


def analytical_probabilities() -> dict[int, float]:
    return {total: count / TOTAL_OUTCOMES for total, count in ANALYTICAL_COUNTS.items()}


def roll_two_dice() -> int:
    return random.randint(1, 6) + random.randint(1, 6)


def monte_carlo_simulation(num_rolls: int) -> dict[int, float]:
    counts = Counter(roll_two_dice() for _ in range(num_rolls))
    return {total: counts[total] / num_rolls for total in range(2, 13)}


def print_comparison_table(mc_probs: dict[int, float], theory_probs: dict[int, float]) -> None:
    print(f"{'Сума':<6} {'Monte Carlo':>12} {'Теорія':>12} {'Різниця':>12}")
    print("-" * 46)

    for total in range(2, 13):
        mc = mc_probs[total] * 100
        theory = theory_probs[total] * 100
        diff = mc - theory
        print(f"{total:<6} {mc:>11.2f}% {theory:>11.2f}% {diff:>+11.2f}%")


def plot_probabilities(mc_probs: dict[int, float], theory_probs: dict[int, float]) -> None:
    totals = list(range(2, 13))
    mc_values = [mc_probs[total] * 100 for total in totals]
    theory_values = [theory_probs[total] * 100 for total in totals]

    x_positions = range(len(totals))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar([x - width / 2 for x in x_positions], mc_values, width, label="Monte Carlo", color="#1296F0")
    plt.bar([x + width / 2 for x in x_positions], theory_values, width, label="Теорія", color="#FFA500")

    plt.xlabel("Сума")
    plt.ylabel("Ймовірність (%)")
    plt.title(f"Ймовірності сум двох кубиків (N = {NUM_ROLLS:,})")
    plt.xticks(x_positions, totals)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    theory = analytical_probabilities()
    mc = monte_carlo_simulation(NUM_ROLLS)

    print(f"Симуляція: {NUM_ROLLS:,} кидків двох кубиків\n")
    print_comparison_table(mc, theory)

    plot_probabilities(mc, theory)
