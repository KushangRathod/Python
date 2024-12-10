import tkinter as tk
import random

# Set up the game window
root = tk.Tk()
root.title("Snake Game")

# Game variables
screen_width = 400
screen_height = 400
block_size = 20
snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake body
direction = "Down"  # Initial direction
score = 0
food = None
game_over = False
initial_speed = 150  # Initial speed in milliseconds
speed = initial_speed  # Current speed
speed_increment = 5  # Decrease delay by this value as score increases

# Create the game canvas
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")
canvas.pack()

# Draw the snake on the canvas
def draw_snake():
    for segment in snake:
        canvas.create_rectangle(segment[0], segment[1], segment[0] + block_size, segment[1] + block_size, fill="green")

# Create food at a random position
def create_food():
    global food
    x = random.randint(0, (screen_width - block_size) // block_size) * block_size
    y = random.randint(0, (screen_height - block_size) // block_size) * block_size
    food = (x, y)
    canvas.create_rectangle(x, y, x + block_size, y + block_size, fill="red")

# Move the snake based on the current direction
def move_snake():
    global snake, game_over, score, speed

    if game_over:
        return

    head_x, head_y = snake[0]

    if direction == "Up":
        new_head = (head_x, head_y - block_size)
    elif direction == "Down":
        new_head = (head_x, head_y + block_size)
    elif direction == "Left":
        new_head = (head_x - block_size, head_y)
    elif direction == "Right":
        new_head = (head_x + block_size, head_y)

    snake = [new_head] + snake[:-1]  # Move snake

    # Check if snake has eaten food
    if snake[0] == food:
        score += 1
        snake.append(snake[-1])  # Add new segment to the snake
        create_food()

        # Increase speed as score increases
        speed = max(50, initial_speed - (score * speed_increment))

    # Check for collision with wall
    if (snake[0][0] < 0 or snake[0][0] >= screen_width or
        snake[0][1] < 0 or snake[0][1] >= screen_height):
        game_over = True
        canvas.create_text(screen_width // 2, screen_height // 2, text="Game Over", font=("Arial", 24, "bold"), fill="white")
        canvas.create_text(screen_width // 2, screen_height // 2 + 40, text=f"Score: {score}", font=("Arial", 16, "bold"), fill="white")
        return

    # Check for collision with itself
    if snake[0] in snake[1:]:
        game_over = True
        canvas.create_text(screen_width // 2, screen_height // 2, text="Game Over", font=("Arial", 24, "bold"), fill="white")
        canvas.create_text(screen_width // 2, screen_height // 2 + 30, text=f"Score: {score}", font=("Arial", 16, "bold"), fill="white")
        return

    # Redraw the snake
    canvas.delete("all")
    draw_snake()
    canvas.create_rectangle(food[0], food[1], food[0] + block_size, food[1] + block_size, fill="red")

    # Continue the game
    root.after(speed, move_snake)

# Control the snake direction using arrow keys
def change_direction(event):
    global direction

    if event.keysym == "Up" and direction != "Down":
        direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"
    elif event.keysym == "Left" and direction != "Right":
        direction = "Left"
    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"

# Start the game
create_food()
move_snake()

# Bind arrow keys to change direction
root.bind("<Up>", change_direction)
root.bind("<Down>", change_direction)
root.bind("<Left>", change_direction)
root.bind("<Right>", change_direction)

# Start the Tkinter event loop
root.mainloop()

