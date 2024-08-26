import turtle
from snake import Snake
from food import Food
from score import Score

# #initialisation
window = turtle.Screen()
window.title("Snake Game")
window.colormode(255)
window.bgcolor(235, 195, 52)
window.setup(width=600, height=600)
window.cv._rootwindow.resizable(False, False)
window.tracer(0)

line = turtle.Turtle()
line.hideturtle()
line.fillcolor('black')
line.width(4)
line.penup()
line.goto(-300, 240)
line.pendown()
line.goto(290, 240)

if __name__ == "__main__":

    score = Score()
    food = Food()
    snake = Snake(window, speed=0, shape="square", color="black", direction="stop")

    while True:
        window.update()

        #check collision with border
        snake.check_collide_border(score)

        #snake colide with ownself
        snake.check_collide_self(score)

        #snake collide with food, move food to new random location
        snake.check_collide_food(food, score)

        #everything is normal, continue moving
        snake.move()
