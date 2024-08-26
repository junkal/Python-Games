import turtle
import random
import time

default_speed = 0.3

class Snake:
    def __init__(self, window, speed, shape="square", color="black", direction="stop"):
        #define the snake
        self.snake = turtle.Turtle()
        self.window = window
        self.snake.direction = direction
        self.snake.speed(speed)
        self.snake.shape(shape)
        self.snake.color(color)
        self.snake.penup()
        self.snake.goto(0, 0)
        self.segments = [] #snake body
        self.movement_speed = default_speed
        self.initialise_keys()

    def go_up(self):
        if self.snake.direction != "down":
            self.snake.direction = "up"

    def go_down(self):
        if self.snake.direction != "up":
            self.snake.direction = "down"

    def go_left(self):
        if self.snake.direction != "right":
            self.snake.direction = "left"

    def go_right(self):
        if self.snake.direction != "left":
            self.snake.direction = "right"

    def initialise_keys(self):
        self.window.onkeypress(self.go_up, "Up")
        self.window.onkeypress(self.go_down, "Down")
        self.window.onkeypress(self.go_left, "Left")
        self.window.onkeypress(self.go_right, "Right")
        self.window.listen()

    def reset_location(self):
        self.snake.goto(0, 0)
        self.snake.direction = "stop"

    #helper functions
    def sety(self, ycoord):
        self.snake.sety(ycoord)

    def setx(self, xcoord):
        self.snake.setx(xcoord)

    def ycor(self):
        return self.snake.ycor()

    def xcor(self):
        return self.snake.xcor()

    def get_segments(self):
        return self.segments

    #check for collision with food
    def check_collide_food(self, food, score):
        if self.snake.distance(food.food) < 20: #snake got food!
            #increase snake body length
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            self.segments.append(new_segment)

            #spawn food in new location
            food.new_location()
            score.add_score(10)
            if score.update_level():
                if self.movement_speed > 0.05:
                    self.movement_speed = self.movement_speed - 0.05

    def check_collide_border(self, score):
        if self.xcor() >= 290 or self.xcor() <= -290 or self.ycor() >= 240 or self.ycor() <= -280:
            time.sleep(0.5)
            self.reset_location()
            score.reset_score()
            self.movement_speed = default_speed

            #necessary to clear the screen
            for segment in self.segments:
                segment.hideturtle()

            self.segments = []

    def check_collide_self(self, score):
        for segment in self.segments:
            if segment.distance(self.snake) < 20:
                time.sleep(0.5)
                self.reset_location()
                score.reset_score()
                self.movement_speed = default_speed

                #necessary to clear the screen
                for segment in self.segments:
                    segment.hideturtle()

                self.segments = []

    def move(self):
        #move the snake head and body
        segments = self.segments
        for index in range(len(segments)-1, 0, -1):
            x = segments[index-1].xcor()
            y = segments[index-1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            segments[0].goto(self.snake.xcor(), self.snake.ycor())

        ######################
        if self.snake.direction == "up":
            self.snake.sety(self.snake.ycor() + 20)

        elif self.snake.direction == "down":
            self.snake.sety(self.snake.ycor() - 20)

        elif self.snake.direction == "left":
            self.snake.setx(self.snake.xcor() - 20)

        elif self.snake.direction == "right":
            self.snake.setx(self.snake.xcor() + 20)

        time.sleep(self.movement_speed)
