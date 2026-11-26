import model
import view

# Добавление символа в поле ввода
def add_symbol(symbol):

    view.input_field.insert("end", symbol)

# Очистка всего поля
def clear():

    view.input_field.delete("1.0", "end")
    view.result_field.configure(text="0")

# Удаление последнего символа
def delete():

    expression = view.input_field.get("1.0", "end-1c")

    view.input_field.delete("1.0", "end")
    view.input_field.insert("1.0", expression[:-1])

# Вычисление
def calculate():

    expression = view.input_field.get("1.0", "end-1c")

    try:

        if "√" in expression:

            number = expression.replace("√", "")
            result = model.square_root(number)

        else:

            result = model.calculate(expression)

        view.result_field.configure(
            text=str(round(result, 10))
        )

    except ZeroDivisionError:

        view.result_field.configure(
            text="На ноль делить нельзя!"
        )

    except ValueError:

        if "√" in expression:
            message = "Корень из отрицательного числа!"
        else:
            message = "Некорректное выражение!"

        view.result_field.configure(text=message)

    except Exception:

        view.result_field.configure(
            text="Ошибка ввода!"
        )

# Связывание кнопок с функциями
for symbol in view.buttons:

    if symbol == "C":
        view.buttons[symbol].configure(command=clear)

    elif symbol == "DEL":
        view.buttons[symbol].configure(command=delete)

    elif symbol == "=":
        view.buttons[symbol].configure(command=calculate)

    else:
        view.buttons[symbol].configure(
            command=lambda s=symbol: add_symbol(s)
        )

# Ввод с клавиатуры
def keyboard_input(event):

    if event.keysym == "Return":
        calculate()
        return "break"

    if event.keysym == "BackSpace":
        delete()
        return "break"

    if event.keysym == "Escape":
        clear()
        return "break"

    if event.char == "=":
        calculate()
        return "break"

    if event.char == "*":
        add_symbol("×")
        return "break"

    if event.char == "/":
        add_symbol("÷")
        return "break"

    if event.char.lower() == "r":
        add_symbol("√")
        return "break"

    # Разрешённые символы
    allowed = "0123456789,+-."

    if event.char and event.char not in allowed:
        return "break"

view.input_field.bind(
    "<KeyPress>",
    keyboard_input
)

# Запуск программы
view.root.mainloop()