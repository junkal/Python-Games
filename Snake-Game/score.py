import turtle

default_level = 1
default_score = 0
default_level_jump = 50

class Score(object):

    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.level = default_level
        self.score = default_score
        self.high_score = 0
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("black")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.write_scores()

    def add_score(self, score):
        self.score = self.score + score
        self.update_high_score()
        self.write_scores()

    def update_level(self):
        if self.score % default_level_jump == 0:
            self.level += 1
            self.write_scores()
            return True
        else:
            return False

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def get_level(self):
        return self.level

    def get_score(self):
        return self.score

    def get_high_score(self):
        return self.high_score

    def reset_score(self):
        self.level = default_level
        self.score = default_score
        self.write_scores()

    def reset_high_score(self):
        self.high_score = default_score

    def write_scores(self):
        self.pen.clear()
        self.pen.write("Level : {}  Score : {}  High Score : {}".format(self.level, self.score, self.high_score),
                    align = "center",
                    font  = ("Courier", 24, "normal"))
