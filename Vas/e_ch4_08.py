wrs_works = {
    "Александр Пушкин": "Евгений Онегин",
    "Фёдор Достоевский": "Преступление и наказание",
    "Лев Толстой": "Война и мир",
    "Антон Чехов": "Три сестры",
    "Марк Твен": "Приключения Гекльберри Финна"
}
# for s in wrs_works.keys():
    # print(s+":", wrs_works[s])
win = 0    
for v in wrs_works.values():
    s = "Автор произведения  " + '"' + v +'"' +" - "
    a = input(s).upper()
    print(a)
    for w in wrs_works.keys():

        if  w.upper().find(a)>0: 
            win+=1
            print("Found:",a )
            break
print("Right answers: ",win)                