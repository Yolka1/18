import json
import math
import os
import re


# Файл patients.json будет лежать рядом с файлами программы.
DATA_FILE = os.path.join(os.path.dirname(__file__), "patients.json")


def load_patients():
    """Загружает список пациентов из JSON-файла."""
    if not os.path.exists(DATA_FILE):
        save_patients([])
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            patients = json.load(file)

        if isinstance(patients, list):
            return patients

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_patients(patients):
    """Сохраняет список пациентов в JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(patients, file, ensure_ascii=False, indent=4)


def calculate_bmi(height_cm, weight_kg):
    """Рассчитывает индекс массы тела."""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 2)


def create_patient(surname, name, patronymic,
                   age_text, height_text, weight_text, sex):
    """
    Проверяет введённые данные и создаёт словарь пациента.
    Если данные неправильные, функция сообщает об ошибке.
    """

    # ФИО можно не заполнять, но если поле заполнено,
    # в нём должны быть буквы, пробелы или дефисы.
    fio_fields = [surname, name, patronymic]

    for field in fio_fields:
        if field != "":
            pattern = r"[A-Za-zА-Яа-яЁё]+(?:[ -][A-Za-zА-Яа-яЁё]+)*"
            if re.fullmatch(pattern, field) is None:
                raise ValueError(
                    "В полях ФИО можно использовать только буквы, "
                    "пробелы и дефисы."
                )

    # Возраст должен быть целым числом.
    if age_text == "":
        raise ValueError("Укажите возраст пациента.")

    if not age_text.isdigit():
        raise ValueError("Возраст должен быть целым числом.")

    age = int(age_text)

    if age < 0 or age > 120:
        raise ValueError("Возраст должен быть от 0 до 120 лет.")

    # Запятая в дробных числах заменяется точкой.
    height_text = height_text.replace(",", ".")
    weight_text = weight_text.replace(",", ".")

    if height_text == "":
        raise ValueError("Укажите рост пациента.")

    if weight_text == "":
        raise ValueError("Укажите вес пациента.")

    try:
        height = float(height_text)
        weight = float(weight_text)
    except ValueError:
        raise ValueError("Рост и вес должны быть числами.")

    if not math.isfinite(height) or not math.isfinite(weight):
        raise ValueError("Введите корректные числовые значения.")

    if height <= 0:
        raise ValueError("Рост должен быть больше нуля.")

    if weight <= 0:
        raise ValueError("Вес должен быть больше нуля.")

    if sex not in ["М", "Ж", "Н/О"]:
        raise ValueError("Выберите пол пациента.")

    bmi = calculate_bmi(height, weight)

    # Один пациент — один словарь.
    patient = {
        "Фамилия": surname,
        "Имя": name,
        "Отчество": patronymic,
        "Возраст": age,
        "Пол": sex,
        "Рост": height,
        "Вес": weight,
        "ИМТ": bmi
    }

    return patient


def get_full_name(patient):
    """Собирает ФИО из трёх полей."""
    parts = [
        patient.get("Фамилия", ""),
        patient.get("Имя", ""),
        patient.get("Отчество", "")
    ]

    full_name = " ".join(part for part in parts if part)

    if full_name == "":
        return "Без ФИО"

    return full_name
