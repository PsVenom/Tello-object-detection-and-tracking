import math
import turtle
import pygame
screen_1 = turtle.Screen()
screen_1.title("Ping-Pong Game")
screen_1.bgcolor("Yellow")
# pygame.init()
# screen = pygame.display.set_mode((400, 500))
# done =
def drawdot(tur,space = 5, x = 10, y = 12):
    for j in range(x):
            print(math.atan(x/y)*180/math.pi)
            tur.left(math.atan(x/y)*180/math.pi)
            tur.dot()
            tur.forward(space)
            tur.right(math.atan(x/y)*180/math.pi)



hit_ball = turtle.Turtle()
hit_ball.speed(45)
hit_ball.shape("circle")
hit_ball.color("Black")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 5
hit_ball.dy = -5
hit_ball.penup()
drawdot(tur = hit_ball,space = 10, x = 13, y = 12)
hit_ball.penup()
turtle.done()
