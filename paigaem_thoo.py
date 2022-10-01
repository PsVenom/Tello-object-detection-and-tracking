import tt
import time
import math
import turtle
screen = turtle.Screen()
screen.title('Map')
screen.bgcolor('green')
screen.setup(width=400, height=400)  # (170,170)

screen.tracer(0)

drone = turtle.Turtle()
drone.shape('turtle')
drone.color('black')
drone.penup()
drone.goto(-150, 150)
drone.pendown()
drone.speed(0)
drone.dx = 0.5
drone.dy = 0.5
drone.setheading(270)


def targetdraw(drone):
    drone.penup()
    x = 170
    y = 170
    drone.goto(x, y)

'''def drawdot(tur,space = 5, x = 10, y = 12):
    for j in range(x):
            print(math.atan(x/y)*180/math.pi)
            tur.left(math.atan(x/y)*180/math.pi)
            tur.dot()
            tur.forward(space)
            tur.right(math.atan(x/y)*180/math.pi)'''



if drone.xcor() == -150:
    drone.sety(drone.ycor() - drone.dy)
    if drone.ycor() < -100:
        drone.sety(-100)
    if drone.ycor() == -100:
        drone.setheading(0)
if drone.ycor() == -100:
    drone.setx(drone.xcor() + (drone.dx + 0.5))
    if drone.xcor() > 100:
        drone.setx(100)
    if drone.xcor() == 100:
        drone.setheading(90)
if drone.xcor() == 100:
    drone.sety(drone.ycor() + (drone.dy + 1))
    if drone.ycor() > 150:
        drone.sety(150)
    if drone.ycor() == 150:
        drone.setheading(180)
if drone.ycor() == 150:
    drone.setx(drone.xcor() - (drone.dx + 1.5))
    if drone.xcor() < -150:
        drone.setx(-150)
    if drone.xcor() == -150:
        drone.setheading(270)




