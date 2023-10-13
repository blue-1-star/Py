import turtle
#turtle.shape("turtle")
##turtle.forward(120)
##turtle.right(36)
##turtle.forward(44)
##turtle.left(36)
##turtle.forward(44)
#turtle.exitonClick()

##for i in range(0,5):
##    turtle.forward(100)
##    turtle.right(72)

##scr = turtle.Screen()
##for i in range(0,3):
##
##    for j in range(0,4): 
##        turtle.forward(112)
##        turtle.right(90)
##    
##    if i == 0:
##        clr = "green"
##    elif i == 1:
##        clr = "yellow"
##    else:
##        clr = "black"
##    #scr.bgcolor(clr)
##    #turtle.begin_fill()
##    turtle.color("black",clr)
##
##    turtle.penup()
##    turtle.forward(224)    
##    turtle.pendown()    
##    #turtle.end_fill()

    
for j in range(0,3):

    if j == 0:
        clr = "green"
    elif j == 1:
        clr = "yellow"
    else:
        clr = "red"
    
    turtle.pendown()
    turtle.color("black", clr)
    turtle.begin_fill()
    for i in range(0, 4):
        turtle.forward(70)
        turtle.right(90)
    turtle.penup()
    turtle.end_fill()
    turtle.forward(100)



