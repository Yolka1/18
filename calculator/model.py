import math

def calculate(expression):

    expression = expression.replace(",", ".")

    if "+" in expression:
        numbers = expression.split("+")
        a = float(numbers[0])
        b = float(numbers[1])
        return a + b

    elif "-" in expression[1:]:
        numbers = expression.split("-")
        a = float(numbers[0])
        b = float(numbers[1])
        return a - b

    elif "×" in expression:
        numbers = expression.split("×")
        a = float(numbers[0])
        b = float(numbers[1])
        return a * b

    elif "÷" in expression:
        numbers = expression.split("÷")
        a = float(numbers[0])
        b = float(numbers[1])

        if b == 0:
            raise ZeroDivisionError

        return a / b

    else:
        raise ValueError

def square_root(number):

    number = float(number.replace(",", "."))

    if number < 0:
        raise ValueError

    return math.sqrt(number)