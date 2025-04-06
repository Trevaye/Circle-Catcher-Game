import turtle
import random
import time
import platform

# Sound setup for Windows
if platform.system() == "Windows":
    import winsound
    def play_sound(event):
        sounds = {
            "catch": "SystemAsterisk",
            "miss": "SystemHand",
            "triangle": "SystemExclamation",
            "gameover": "SystemQuestion"
        }
        winsound.PlaySound(sounds.get(event, "SystemAsterisk"),
                           winsound.SND_ALIAS | winsound.SND_ASYNC)
else:
    def play_sound(event):
        pass  # No-op if not on Windows

# Set up screen
win = turtle.Screen()
win.title("Catch the Falling Objects")
win.bgcolor("lightblue")
win.setup(width=600, height=600)
win.tracer(0)

# --- Instructions Screen ---
instructions = turtle.Turtle()
instructions.hideturtle()
instructions.penup()
instructions.color("black")
instructions.goto(0, 100)
instructions.write("Catch the RED circles!\nAvoid the PURPLE triangles!\nYou only have 3 lives.\n\nPress SPACE to start.",
                      align="center", font=("Arial", 18, "bold"))

game_started = False
def start_game():
    global game_started
    game_started = True
    instructions.clear()

win.listen()
win.onkeypress(start_game, "space")

while not game_started:
    win.update()

# Paddle setup 
player = turtle.Turtle()
player.shape("square")
player.color("black")
player.shapesize(stretch_wid=1, stretch_len=5)
player.penup()
player.goto(0, -250)
paddle_length = 5

# Score and Lives 
score = 0
lives = 3

score_display = turtle.Turtle()
score_display.penup()
score_display.hideturtle()
score_display.goto(-280, 260)
score_display.write(f"Score: {score}  Lives: {lives}", font=("Arial", 16, "bold"))

# Create Falling Ball 
def create_ball():
    ball = turtle.Turtle()
    ball.shape("circle")
    ball.color("red")
    ball.penup()
    ball.goto(random.randint(-280, 280), 250)
    ball.speed(0)
    return ball

falling_objects = [create_ball()]

# Bad Object (Triangle) 
bad_object = turtle.Turtle()
bad_object.shape("triangle")
bad_object.color("purple")
bad_object.penup()
bad_object.goto(random.randint(-280, 280), 250)
bad_object.speed(0)

# --- Movement ---
def go_left():
    x = player.xcor()
    if x > -250:
        player.setx(x - 30)

def go_right():
    x = player.xcor()
    if x < 250:
        player.setx(x + 30)

win.listen()
win.onkeypress(go_left, "Left")
win.onkeypress(go_right, "Right")

# Game Over Screen 
def show_game_over():
    play_sound("gameover")

    over = turtle.Turtle()
    over.hideturtle()
    over.penup()
    over.color("red")
    over.goto(0, 50)
    over.write("GAME OVER", align="center", font=("Arial", 36, "bold"))

    retry = turtle.Turtle()
    retry.hideturtle()
    retry.penup()
    retry.color("black")
    retry.goto(0, -20)
    retry.write("Click here to Try Again", align="center", font=("Arial", 20, "normal"))

    def restart_game(x, y):
        win.bye()  # Closes the window

    win.onclick(restart_game)

# Main Game Loop
while True:
    win.update()

    # Gently increase fall speed and cap it
    if score < 5:
        fall_speed = 4
    elif score < 10:
        fall_speed = 5
    elif score < 15:
        fall_speed = 6
    else:
        fall_speed = 7

    # Add second ball at score 12
    if score >= 12 and len(falling_objects) == 1:
        falling_objects.append(create_ball())

    # Widen paddle
    if score == 5:
        paddle_length = 6
        player.shapesize(stretch_wid=1, stretch_len=paddle_length)
    elif score == 10:
        paddle_length = 7
        player.shapesize(stretch_wid=1, stretch_len=paddle_length)
    elif score == 15:
        paddle_length = 8
        player.shapesize(stretch_wid=1, stretch_len=paddle_length)

    # Move balls
    for ball in falling_objects:
        ball.sety(ball.ycor() - fall_speed)

        # Caught
        if ball.distance(player) < 50:
            score += 1
            play_sound("catch")
            score_display.clear()
            score_display.write(f"Score: {score}  Lives: {lives}", font=("Arial", 16, "bold"))
            ball.goto(random.randint(-280, 280), 250)

        # Missed
        elif ball.ycor() < -280:
            play_sound("miss")
            lives -= 1
            score_display.clear()
            score_display.write(f"Score: {score}  Lives: {lives}", font=("Arial", 16, "bold"))
            ball.goto(random.randint(-280, 280), 250)

    # Move and check triangle
    bad_object.sety(bad_object.ycor() - fall_speed)

    if bad_object.distance(player) < 50:
        score -= 1
        play_sound("triangle")
        score_display.clear()
        score_display.write(f"Score: {score}  Lives: {lives}", font=("Arial", 16, "bold"))
        bad_object.goto(random.randint(-280, 280), 250)

    if bad_object.ycor() < -280:
        bad_object.goto(random.randint(-280, 280), 250)

    if lives <= 0:
        show_game_over()
        break

    time.sleep(0.03)
