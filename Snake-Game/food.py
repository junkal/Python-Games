import turtle
import random

class Food:
    def __init__(self, speed=0, shape="circle", color="red"):
        #define the snake
        self.food = turtle.Turtle()
        self.food.speed(speed)
        self.food.shape(shape)
        self.food.color(color)
        self.food.penup()
        self.food.goto(random.randint(-280, 280), random.randint(-240, 220))

    def get_food(self):
        return self.food

    def new_location(self):
        self.food.goto(random.randint(-280, 280), random.randint(-240, 220))
