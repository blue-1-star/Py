import turtle
import random

tup = (0.2, 0.8, 0.55)
turtle.pensize(3)
for j in range(0,9):

   
    #turtle.forward(90)
    #turtle.pendown()
    #turtle.color("black", clr)
    #turtle.begin_fill()
    #for i in range(0, 4):
        colour = random.choice(["red", "black", "green","brown",tup,"blue"])
        turtle.pencolor(colour)
        turtle.forward(90)
        turtle.right(45)
    



