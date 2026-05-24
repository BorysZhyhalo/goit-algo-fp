import math
import turtle


def draw_square(t: turtle.Turtle, size: float) -> None:
    for _ in range(4):
        t.forward(size)
        t.left(90)


def pythagoras_tree(t: turtle.Turtle, size: float, level: int) -> None:
    if level == 0:
        return

    draw_square(t, size)

    t.forward(size)
    t.left(45)

    new_size = size / math.sqrt(2)
    pythagoras_tree(t, new_size, level - 1)

    t.right(90)
    pythagoras_tree(t, new_size, level - 1)

    t.left(45)
    t.backward(size)


def ask_level() -> int:
    while True:
        raw = input("Введіть рівень рекурсії (0-10): ").strip()
        try:
            level = int(raw)
        except ValueError:
            print("Потрібно ціле число.")
            continue
        if 0 <= level <= 10:
            return level
        print("Рівень має бути від 0 до 10.") # Вказуємо допустимий діапазон рівнів рекурсії.


def main() -> None:
    level = ask_level()

    screen = turtle.Screen()
    screen.title("Дерево Піфагора")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.pensize(2)
    t.color("darkblue")

    t.penup()
    t.goto(0, -250)
    t.setheading(90)
    t.pendown()

    pythagoras_tree(t, 100, level)
    turtle.done()


if __name__ == "__main__":
    main()
