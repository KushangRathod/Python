import tkinter as tk  # Importing the tkinter module for GUI applications.
import random  # Importing the random module for generating random food positions.

# Set up the game window
root = tk.Tk()  # Create the main application window.
root.title("Snake Game")  # Set the title of the window.

# Game variables
screen_width = 400  # Width of the game screen.
screen_height = 400  # Height of the game screen.
block_size = 20  # Size of each block (snake segment and food).
snake = [(100, 100), (80, 100), (60, 100)]  # Initial position and segments of the snake.
direction = "Down"  # Initial movement direction of the snake.
score = 0  # Initial score.
food = None  # Placeholder for the food position.
game_over = False  # Flag to indicate whether the game is over.
initial_speed = 150  # Initial delay between moves (in milliseconds).
speed = initial_speed  # Current speed of the game.
speed_increment = 5  # Speed adjustment factor when score increases.

# Create the game canvas
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")  # Create the canvas for the game.
canvas.pack()  # Pack the canvas into the window.

# Draw the snake on the canvas
def draw_snake():
    for segment in snake:  # Loop through each segment of the snake.
        canvas.create_rectangle(segment[0], segment[1], segment[0] + block_size, segment[1] + block_size, fill="green")  # Draw each segment.

# Create food at a random position
def create_food():
    global food  # Use the global variable food.
    x = random.randint(0, 19) * block_size  # Generate a random x-coordinate for the food.
    y = random.randint(0, 19) * block_size  # Generate a random y-coordinate for the food.
    food = (x, y)  # Set the food's position.
    canvas.create_rectangle(x, y, x + block_size, y + block_size, fill="red")  # Draw the food on the canvas.

# Move the snake based on the current direction
def move_snake():
    global snake, game_over, score, speed  # Use global variables for snake, game state, score, and speed.

    if game_over:  # Stop movement if the game is over.
        return

    head_x, head_y = snake[0]  # Get the current position of the snake's head.

    # Determine the new head position based on the direction.
    if direction == "Up":
        new_head = (head_x, head_y - block_size)
    elif direction == "Down":
        new_head = (head_x, head_y + block_size)
    elif direction == "Left":
        new_head = (head_x - block_size, head_y)
    elif direction == "Right":
        new_head = (head_x + block_size, head_y)

    snake = [new_head] + snake[:-1]  # Update the snake's position by adding the new head and removing the tail.

    # Check if the snake has eaten the food.
    if snake[0] == food:
        score += 1  # Increment the score.
        snake.append(snake[-1])  # Extend the snake's body by one segment.
        create_food()  # Generate new food.

        # Adjust the game speed based on the score.
        speed = max(50, initial_speed - (score * speed_increment))

    # Check for collision with the walls.
    if (snake[0][0] < 0 or snake[0][0] >= screen_width or
        snake[0][1] < 0 or snake[0][1] >= screen_height):
        game_over = True  # Set the game over flag.
        canvas.create_text(screen_width // 2, screen_height // 2, text="Game Over", font=("Arial", 24, "bold"), fill="white")  # Display "Game Over".
        canvas.create_text(screen_width // 2, screen_height // 2 + 40, text=f"Score: {score}", font=("Arial", 16, "bold"), fill="white")  # Display the final score.
        return

    # Check for collision with itself.
    if snake[0] in snake[1:]:
        game_over = True  # Set the game over flag.
        canvas.create_text(screen_width // 2, screen_height // 2, text="Game Over", font=("Arial", 24, "bold"), fill="white")  # Display "Game Over".
        canvas.create_text(screen_width // 2, screen_height // 2 + 30, text=f"Score: {score}", font=("Arial", 16, "bold"), fill="white")  # Display the final score.
        return

    # Redraw the snake and food.
    canvas.delete("all")  # Clear the canvas.
    draw_snake()  # Draw the updated snake.
    canvas.create_rectangle(food[0], food[1], food[0] + block_size, food[1] + block_size, fill="red")  # Redraw the food.

    # Continue the game after a delay.
    root.after(speed, move_snake)

# Control the snake direction using arrow keys
def change_direction(event):
    global direction  # Use the global direction variable.

    # Update direction, avoiding a reversal.
    if event.keysym == "Up" and direction != "Down":
        direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"
    elif event.keysym == "Left" and direction != "Right":
        direction = "Left"
    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"

# Start the game
create_food()  # Generate the initial food.
move_snake()  # Start the snake movement.

# Bind arrow keys to change direction
root.bind("<Up>", change_direction)  # Bind the Up arrow key.
root.bind("<Down>", change_direction)  # Bind the Down arrow key.
root.bind("<Left>", change_direction)  # Bind the Left arrow key.
root.bind("<Right>", change_direction)  # Bind the Right arrow key.

# Start the Tkinter event loop
root.mainloop()  # Start the Tkinter event loop to handle events and updates.
