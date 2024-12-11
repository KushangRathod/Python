import tkinter as tk  # Importing the tkinter module for creating GUI-based applications.
import random  # Importing the random module for generating random positions for food.

# Set up the game window
root = tk.Tk()  # Create the main application window using Tkinter.
root.title("Snake Game")  # Set the title of the window to "Snake Game".

# Game variables
screen_width = 400  # Width of the game screen in pixels.
screen_height = 400  # Height of the game screen in pixels.
block_size = 20  # Size of each block representing the snake segment or food.
snake = [(100, 100), (80, 100), (60, 100)]  # List of tuples representing the initial position of the snake segments.
direction = "Down"  # Initial direction of the snake's movement.
score = 0  # Initialize the score to zero.
food = None  # Variable to hold the position of the food, initialized as None.
game_over = False  # Boolean flag to indicate whether the game is over.
initial_speed = 150  # Initial delay between movements in milliseconds.
speed = initial_speed  # Variable to hold the current game speed.
speed_increment = 5  # Value by which speed decreases as the score increases.

# Create the game canvas
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")
# Create a canvas widget to serve as the game's playing area, with a black background.
canvas.pack()  # Add the canvas to the Tkinter window.

# Function to draw the snake on the canvas
def draw_snake():
    for segment in snake:  # Loop through each segment of the snake.
        canvas.create_rectangle(
            segment[0], segment[1],
            segment[0] + block_size, segment[1] + block_size,
            fill="green"
        )  # Draw a green rectangle for each snake segment.

# Function to create food at a random position
def create_food():
    global food  # Use the global variable `food` to store the new position.
    x = random.randint(0, 19) * block_size  # Generate a random x-coordinate (aligned to grid).
    y = random.randint(0, 19) * block_size  # Generate a random y-coordinate (aligned to grid).
    food = (x, y)  # Update the global food variable with the new position.
    canvas.create_rectangle(x, y, x + block_size, y + block_size, fill="red")
    # Draw the food as a red rectangle on the canvas.

# Function to move the snake based on the current direction
def move_snake():
    global snake, game_over, score, speed  # Use global variables to update the snake's state and game parameters.

    if game_over:  # If the game is over, stop the function.
        return

    head_x, head_y = snake[0]  # Get the current position of the snake's head.

    # Calculate the new head position based on the current direction.
    if direction == "Up":
        new_head = (head_x, head_y - block_size)  # Move up by decreasing the y-coordinate.
    elif direction == "Down":
        new_head = (head_x, head_y + block_size)  # Move down by increasing the y-coordinate.
    elif direction == "Left":
        new_head = (head_x - block_size, head_y)  # Move left by decreasing the x-coordinate.
    elif direction == "Right":
        new_head = (head_x + block_size, head_y)  # Move right by increasing the x-coordinate.

    snake = [new_head] + snake[:-1]  # Update the snake's body by adding the new head and removing the tail.

    # Check if the snake has eaten the food.
    if snake[0] == food:  # If the head of the snake is at the food's position:
        score += 1  # Increment the score.
        snake.append(snake[-1])  # Add a new segment to the snake (grow the snake).
        create_food()  # Generate a new food on the canvas.

        # Adjust the game speed based on the score (faster as the score increases).
        speed = max(50, initial_speed - (score * speed_increment))

    # Check for collision with the walls.
    if (snake[0][0] < 0 or snake[0][0] >= screen_width or
        snake[0][1] < 0 or snake[0][1] >= screen_height):
        game_over = True  # Set the game_over flag to True.
        canvas.create_text(screen_width // 2, screen_height // 2, text="Game Over", font=("Arial", 24, "bold"), fill="white")
        # Display "Game Over" message on the canvas.
        canvas.create_text(screen_width // 2, screen_height // 2 + 40, text=f"Score: {score}", font=("Arial", 16, "bold"), fill="white")
        # Display the final score on the canvas.
        return

    # Check for collision with itself (head overlaps a body segment).
    if snake[0] in snake[1:]:
        game_over = True  # Set the game_over flag to True.
        canvas.create_text(screen_width // 2, screen_height // 2, text="Game Over", font=("Arial", 24, "bold"), fill="white")
        # Display "Game Over" message on the canvas.
        canvas.create_text(screen_width // 2, screen_height // 2 + 30, text=f"Score: {score}", font=("Arial", 16, "bold"), fill="white")
        # Display the final score on the canvas.
        return

    # Redraw the canvas.
    canvas.delete("all")  # Clear the canvas of all existing drawings.
    draw_snake()  # Draw the updated snake.
    canvas.create_rectangle(food[0], food[1], food[0] + block_size, food[1] + block_size, fill="red")
    # Redraw the food at its current position.

    # Schedule the next move after the current speed interval.
    root.after(speed, move_snake)

# Function to change the direction of the snake based on key press
def change_direction(event):
    global direction  # Use the global `direction` variable to update the direction.

    # Update the direction if it is not opposite to the current direction.
    if event.keysym == "Up" and direction != "Down":
        direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"
    elif event.keysym == "Left" and direction != "Right":
        direction = "Left"
    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"

# Start the game
create_food()  # Generate the first food on the canvas.
move_snake()  # Start the snake movement loop.

# Bind the arrow keys to the change_direction function
root.bind("<Up>", change_direction)  # Bind the Up arrow key to change the direction to "Up".
root.bind("<Down>", change_direction)  # Bind the Down arrow key to change the direction to "Down".
root.bind("<Left>", change_direction)  # Bind the Left arrow key to change the direction to "Left".
root.bind("<Right>", change_direction)  # Bind the Right arrow key to change the direction to "Right".

# Start the Tkinter event loop
root.mainloop()  # Start the event loop to keep the application window open and responsive.
