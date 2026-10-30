from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

SPEEDS = {"Slow": 160, "Normal": 100, "Fast": 60, "Insane": 35}

score = 0
high_score = 0
direction = "down"
speed = SPEEDS["Normal"]


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append((0, 0))

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self, snake):
        occupied = set(snake.coordinates)
        free_cells = []

        for col in range(GAME_WIDTH // SPACE_SIZE):
            for row in range(GAME_HEIGHT // SPACE_SIZE):
                cell = (col * SPACE_SIZE, row * SPACE_SIZE)
                if cell not in occupied:
                    free_cells.append(cell)

        x, y = random.choice(free_cells)
        self.coordinates = (x, y)
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )


def next_turn(snake, food):
    global score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill=SNAKE_COLOR, tag="snake"
    )
    snake.squares.insert(0, square)

    if (x, y) == food.coordinates:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food(snake)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if (x, y) == body_part:
            return True

    return False


def game_over():
    global high_score

    new_record = score > high_score
    high_score = max(high_score, score)

    canvas.delete("all")
    label.config(text="")

    canvas.create_text(
        GAME_WIDTH / 2, 120,
        text="GAME OVER", fill="red",
        font=("Arial", 64, "bold")
    )
    canvas.create_text(
        GAME_WIDTH / 2, 230,
        text=f"YOUR SCORE: {score}", fill="white",
        font=("Arial", 30, "bold")
    )
    canvas.create_text(
        GAME_WIDTH / 2, 285,
        text=f"HIGHEST SCORE: {high_score}", fill="gold",
        font=("Arial", 26, "bold")
    )

    if new_record and score > 0:
        canvas.create_text(
            GAME_WIDTH / 2, 335,
            text="NEW HIGH SCORE!", fill="lime",
            font=("Arial", 20, "bold")
        )

    canvas.create_window(GAME_WIDTH / 2, 490, window=menu_frame)


def restart_game():
    global direction, snake, food, score, speed

    speed = SPEEDS[speed_var.get()]
    score = 0
    direction = "right"
    label.config(text=f"Score: {score}")

    canvas.delete("all")

    snake = Snake()
    food = Food(snake)

    window.focus_set()
    next_turn(snake, food)


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

label = Label(window, text=f"Score: {score}", font=("Arial", 16))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

speed_var = StringVar(value="Normal")

menu_frame = Frame(window, bg="#1e1e1e", padx=30, pady=20,
                   highlightbackground="white", highlightthickness=2)

Label(menu_frame, text="SPEED", bg="#1e1e1e", fg="white",
      font=("Arial", 14, "bold")).pack(pady=(0, 8))

speed_row = Frame(menu_frame, bg="#1e1e1e")
speed_row.pack()

for name in SPEEDS:
    Radiobutton(
        speed_row, text=name, value=name, variable=speed_var,
        indicatoron=0, width=8, pady=6,
        bg="#333333", fg="white", selectcolor="#2e8b57",
        activebackground="#444444", activeforeground="white",
        font=("Arial", 11, "bold")
    ).pack(side=LEFT, padx=4)

Button(
    menu_frame, text="RESTART", command=restart_game,
    bg="#2e8b57", fg="white", activebackground="#3cb371",
    activeforeground="white", font=("Arial", 16, "bold"),
    width=16, pady=8, bd=0, cursor="hand2"
).pack(pady=(20, 0))

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2) - 30)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food(snake)

next_turn(snake, food)

window.mainloop()