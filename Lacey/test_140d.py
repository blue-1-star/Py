sel = 6
again = "y"
while again == "y":
    print()
    print("Main Menu")
    print()
    print("1) View phone book")
    print("2) Add to phone book")
    print("3) Search for surname")
    print("4) Delete person from phone book")
    print("5) Quit")
    print()
    if sel == 1:
        print("1")
    elif sel == 5:
        print("Quit")
        again = "n"
    else:
        print("Incorrect")
