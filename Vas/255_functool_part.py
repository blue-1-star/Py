#  Вот пример использования functools.partial, partial(func, *args, **kwargs)
# где фиксируются и позиционные аргументы (*args), и именованные аргументы (**kwargs).
def format_string(template, *args, **kwargs):
    return template.format(*args, **kwargs)
from functools import partial

# Фиксируем template, один *args и один **kwargs
formatted_greeting = partial(
    format_string,
    "Hello, {}! Your balance is {balance}.",  # template
    "Alice",  # фиксируем первый аргумент для *args
    balance=100  # фиксируем именованный аргумент для **kwargs
)
# Не передаём дополнительные аргументы, так как всё уже зафиксировано
print(formatted_greeting())
# Вывод: "Hello, Alice! Your balance is 100."

# Можно переопределить фиксированные аргументы при вызове
print(formatted_greeting(balance=200))
# Вывод: "Hello, Alice! Your balance is 200."

# Если нужно изменить первый аргумент (для *args)
print(formatted_greeting("Bob", balance=300))
# Вывод: "Hello, Bob! Your balance is 300."
"""
в примере с фиксированием *args значение "Alice" останется зафиксированным как первый аргумент,
и даже если мы передадим другое значение, оно не заменит уже зафиксированный.
Давай разберём это подробнее и уточним, как корректно использовать partial в таких случаях.

В partial фиксированные аргументы задаются один раз и не могут быть заменены при вызове частичной функции,
если они указаны в *args.
Поэтому в третьем вызове, где я пытался заменить "Alice" на "Bob", это невозможно.


"""
# from functools import partial

# def format_string(template, *args, **kwargs):
#  return template.format(*args, **kwargs)

# Фиксируем только шаблон и balance как именованный аргумент
formatted_greeting = partial(
    format_string,
    "Hello, {}! Your balance is {balance}.",  # только шаблон фиксируется
    balance=100  # фиксируем balance как именованный аргумент
)

# Теперь мы можем задавать первый аргумент динамически
print(formatted_greeting("Alice"))  # Вывод: Hello, Alice! Your balance is 100.
print(formatted_greeting("Bob"))    # Вывод: Hello, Bob! Your balance is 100.

# И переопределять balance
print(formatted_greeting("Charlie", balance=200))  # Вывод: Hello, Charlie! Your balance is 200.
print(formatted_greeting("Bob", balance=300))
