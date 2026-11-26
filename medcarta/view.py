import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk


# Цвета из выбранной голубой палитры.
CLOUD_VEIL = "#F2F8FF"
ICE_PETAL = "#E3F1FF"
COOL_BLUE = "#CFE6FF"
SKY_RIPPLE = "#B7D8F7"
BLUE_LAGOON = "#9FC8EE"
DARK_BLUE = "#35536F"
WHITE = "#FFFFFF"


class View:
    """Создаёт графический интерфейс программы."""

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("Медицинские карточки пациентов")
        self.root.geometry("1250x780")
        self.root.minsize(1050, 680)
        self.root.configure(fg_color=CLOUD_VEIL)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.edit_mode = False
        self.selected_index = None
        self.table_rows = []

        self.create_top_panel()
        self.create_main_area()

    def create_top_panel(self):
        """Верхняя панель с кнопками и поиском."""
        top = ctk.CTkFrame(self.root, fg_color=ICE_PETAL, corner_radius=0)
        top.pack(fill="x", padx=12, pady=(12, 8))

        self.add_button = ctk.CTkButton(
            top, text="＋ Добавить", width=130,
            fg_color=BLUE_LAGOON, hover_color=SKY_RIPPLE,
            text_color=DARK_BLUE,
            command=self.controller.add_or_save
        )
        self.add_button.pack(side="left", padx=(12, 6), pady=12)

        self.edit_button = ctk.CTkButton(
            top, text="Изменить", width=120,
            fg_color=COOL_BLUE, hover_color=SKY_RIPPLE,
            text_color=DARK_BLUE,
            command=self.controller.start_or_cancel_edit
        )
        self.edit_button.pack(side="left", padx=6, pady=12)

        self.clear_button = ctk.CTkButton(
            top, text="Очистить", width=120,
            fg_color=COOL_BLUE, hover_color=SKY_RIPPLE,
            text_color=DARK_BLUE,
            command=self.controller.clear_all
        )
        self.clear_button.pack(side="left", padx=6, pady=12)

        # Кнопка для вывода всех четырёх графиков в одном окне.
        self.graph_button = ctk.CTkButton(
            top, text="Графики", width=120,
            fg_color=COOL_BLUE, hover_color=SKY_RIPPLE,
            text_color=DARK_BLUE,
            command=self.controller.show_all_charts
        )
        self.graph_button.pack(side="left", padx=6, pady=12)

        self.search_entry = ctk.CTkEntry(
            top, placeholder_text="Поиск по ФИО...",
            width=220, height=34
        )
        self.search_entry.pack(side="right", padx=12, pady=12)
        # Поиск запускается по Enter, а не после каждой введённой буквы.
        self.search_entry.bind(
            "<Return>",
            lambda event: self.update_table(self.controller.patients)
        )
        self.search_entry.bind("<Escape>", self.clear_search)

    def create_main_area(self):
        """Левая карточка и правая таблица."""
        main = ctk.CTkFrame(self.root, fg_color=CLOUD_VEIL)
        main.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.left_panel = ctk.CTkFrame(
            main, width=310, fg_color=ICE_PETAL, corner_radius=12
        )
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))
        self.left_panel.pack_propagate(False)

        self.create_patient_form()
        self.create_graph_buttons()

        self.right_panel = ctk.CTkFrame(
            main, fg_color=WHITE, corner_radius=12
        )
        self.right_panel.pack(side="left", fill="both", expand=True)

        self.create_table()

    def create_patient_form(self):
        """Поля ввода информации о пациенте."""
        title = ctk.CTkLabel(
            self.left_panel, text="Карточка пациента",
            font=("Arial", 19, "bold"), text_color=DARK_BLUE
        )
        title.pack(pady=(14, 10))

        self.surname_entry = self.add_text_field("Фамилия")
        self.name_entry = self.add_text_field("Имя")
        self.patronymic_entry = self.add_text_field("Отчество")

        self.age_entry = self.add_number_field("Возраст", True)
        self.height_entry = self.add_number_field("Рост, см", False)
        self.weight_entry = self.add_number_field("Вес, кг", False)

        sex_label = ctk.CTkLabel(
            self.left_panel, text="Пол",
            text_color=DARK_BLUE, font=("Arial", 14)
        )
        sex_label.pack(anchor="w", padx=18, pady=(8, 2))

        self.sex_var = tk.StringVar(value="")

        sex_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        sex_frame.pack(fill="x", padx=14)

        for text in ["М", "Ж", "Н/О"]:
            radio = ctk.CTkRadioButton(
                sex_frame, text=text, variable=self.sex_var,
                value=text, text_color=DARK_BLUE,
                fg_color=BLUE_LAGOON, hover_color=SKY_RIPPLE,
                width=55
            )
            radio.pack(side="left", padx=2, pady=4)

        bmi_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        bmi_frame.pack(fill="x", padx=18, pady=(8, 12))

        ctk.CTkLabel(
            bmi_frame, text="ИМТ",
            text_color=DARK_BLUE, font=("Arial", 14)
        ).pack(side="left")

        self.bmi_value = ctk.CTkLabel(
            bmi_frame, text="—", width=100, height=30,
            fg_color=WHITE, corner_radius=7,
            text_color=DARK_BLUE, font=("Arial", 14, "bold")
        )
        self.bmi_value.pack(side="right")

        # При изменении роста или веса обновляем предварительный ИМТ.
        self.height_entry.bind("<KeyRelease>", self.update_bmi_preview)
        self.weight_entry.bind("<KeyRelease>", self.update_bmi_preview)

    def add_text_field(self, label_text):
        """Создаёт обычное поле ФИО."""
        label = ctk.CTkLabel(
            self.left_panel, text=label_text,
            text_color=DARK_BLUE, font=("Arial", 14)
        )
        label.pack(anchor="w", padx=18, pady=(5, 0))

        entry = ctk.CTkEntry(
            self.left_panel, height=30,
            fg_color=WHITE, border_color=BLUE_LAGOON
        )
        entry.pack(fill="x", padx=18, pady=(2, 3))
        return entry

    def add_number_field(self, label_text, is_integer):
        """Создаёт числовое поле с кнопками увеличения и уменьшения."""
        label = ctk.CTkLabel(
            self.left_panel, text=label_text,
            text_color=DARK_BLUE, font=("Arial", 14)
        )
        label.pack(anchor="w", padx=18, pady=(5, 0))

        line = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        line.pack(fill="x", padx=18, pady=(2, 3))

        entry = ctk.CTkEntry(
            line, height=30, fg_color=WHITE,
            border_color=BLUE_LAGOON
        )
        entry.pack(side="left", fill="x", expand=True)

        if is_integer:
            allowed = lambda value: value.isdigit() or value == ""
        else:
            allowed = lambda value: (
                value == "" or
                value.replace(",", ".", 1).replace(".", "", 1).isdigit()
            )

        validation = (self.root.register(allowed), "%P")
        entry.configure(validate="key", validatecommand=validation)

        buttons = ctk.CTkFrame(line, fg_color="transparent")
        buttons.pack(side="right", padx=(4, 0))

        up_button = ctk.CTkButton(
            buttons, text="▲", width=25, height=14,
            font=("Arial", 9), fg_color=BLUE_LAGOON,
            hover_color=SKY_RIPPLE, text_color=DARK_BLUE,
            command=lambda: self.change_number(entry, 1, is_integer)
        )
        up_button.pack()

        down_button = ctk.CTkButton(
            buttons, text="▼", width=25, height=14,
            font=("Arial", 9), fg_color=BLUE_LAGOON,
            hover_color=SKY_RIPPLE, text_color=DARK_BLUE,
            command=lambda: self.change_number(entry, -1, is_integer)
        )
        down_button.pack()

        return entry

    def change_number(self, entry, step, is_integer):
        """Меняет значение в числовом поле на один шаг."""
        value = entry.get().replace(",", ".")

        try:
            if value == "":
                number = 0
            elif is_integer:
                number = int(value)
            else:
                number = float(value)

            number = number + step

            if number < 0:
                number = 0

            if is_integer:
                new_value = str(int(number))
            else:
                new_value = str(round(number, 2))

            entry.delete(0, "end")
            entry.insert(0, new_value)

        except ValueError:
            entry.delete(0, "end")
            entry.insert(0, "0")

        self.update_bmi_preview()

    def update_bmi_preview(self, event=None):
        """Показывает ИМТ до сохранения пациента."""
        try:
            height = float(self.height_entry.get().replace(",", "."))
            weight = float(self.weight_entry.get().replace(",", "."))

            if height > 0 and weight > 0:
                bmi = weight / ((height / 100) ** 2)
                self.bmi_value.configure(text=str(round(bmi, 2)))
                return
        except ValueError:
            pass

        self.bmi_value.configure(text="—")

    def create_graph_buttons(self):
        """Четыре небольших поля-перехода к графикам."""
        separator = ctk.CTkFrame(
            self.left_panel, height=2, fg_color=BLUE_LAGOON
        )
        separator.pack(fill="x", padx=12, pady=(5, 8))

        ctk.CTkLabel(
            self.left_panel, text="Статистика",
            font=("Arial", 16, "bold"), text_color=DARK_BLUE
        ).pack(pady=(0, 5))

        graph_names = [
            "1. Распределение по полу",
            "2. Распределение по возрасту",
            "3. ИМТ с учётом пола",
            "4. ИМТ и возраст"
        ]

        for number, graph_name in enumerate(graph_names, start=1):
            button = ctk.CTkButton(
                self.left_panel, text=graph_name,
                height=42, fg_color=COOL_BLUE,
                hover_color=SKY_RIPPLE, text_color=DARK_BLUE,
                anchor="w",
                command=lambda n=number: self.controller.show_charts(n)
            )
            button.pack(fill="x", padx=14, pady=4)

    def create_table(self):
        """Создаёт заголовки и прокручиваемую таблицу."""
        title = ctk.CTkLabel(
            self.right_panel, text="Список пациентов",
            font=("Arial", 20, "bold"), text_color=DARK_BLUE
        )
        title.pack(pady=(16, 10))

        header = ctk.CTkFrame(
            self.right_panel, fg_color=SKY_RIPPLE, corner_radius=7
        )
        header.pack(fill="x", padx=(12, 28), pady=(0, 5))

        columns = [
            ("ФИО", 3), ("Возраст", 1), ("Пол", 1),
            ("Рост", 1), ("Вес", 1), ("ИМТ", 1)
        ]

        for column, (name, weight) in enumerate(columns):
            header.grid_columnconfigure(
                column, weight=weight, uniform="patient_columns"
            )
            label = ctk.CTkLabel(
                header, text=name, text_color=DARK_BLUE,
                font=("Arial", 12, "bold")
            )
            label.grid(row=0, column=column, padx=5, pady=9, sticky="ew")

        self.table_frame = ctk.CTkScrollableFrame(
            self.right_panel, fg_color=WHITE,
            scrollbar_button_color=BLUE_LAGOON,
            scrollbar_button_hover_color=SKY_RIPPLE
        )
        self.table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        # Ширины столбцов строк повторяют пропорции заголовков.
        for column, (_, weight) in enumerate(columns):
            self.table_frame.grid_columnconfigure(
                column, weight=weight, uniform="patient_columns"
            )

    def clear_search(self, event=None):
        """Очищает поиск и возвращает полный список пациентов."""
        self.search_entry.delete(0, "end")
        self.update_table(self.controller.patients)

    def update_table(self, patients):
        """Обновляет видимые строки, не пересоздавая таблицу каждый раз."""
        search_text = self.search_entry.get().strip().lower()

        # Создаём кнопки-ячейки только для новых пациентов.
        # При поиске и отмене редактирования уже созданные ячейки переиспользуются.
        while len(self.table_rows) < len(patients):
            index = len(self.table_rows)
            cells = []

            for column in range(6):
                cell = ctk.CTkButton(
                    self.table_frame,
                    text="",
                    anchor="center",
                    height=42,
                    fg_color="transparent",
                    hover_color=COOL_BLUE,
                    text_color=DARK_BLUE,
                    command=lambda i=index: self.controller.select_patient(i)
                )
                cells.append(cell)

            self.table_rows.append(cells)

        visible_row = 0

        for index, patient in enumerate(patients):
            full_name = " ".join([
                patient.get("Фамилия", ""),
                patient.get("Имя", ""),
                patient.get("Отчество", "")
            ]).strip()
            if not full_name:
                full_name = "Без ФИО"

            values = [
                full_name,
                str(patient["Возраст"]),
                patient["Пол"],
                str(patient["Рост"]),
                str(patient["Вес"]),
                f"{patient['ИМТ']:.2f}"
            ]

            search_data = " ".join(values).lower()
            cells = self.table_rows[index]

            if search_text not in search_data:
                for cell in cells:
                    cell.grid_remove()
                continue

            row_color = ICE_PETAL if visible_row % 2 == 0 else CLOUD_VEIL

            for column, (cell, value) in enumerate(zip(cells, values)):
                cell.configure(
                    text=value,
                    fg_color=row_color,
                    hover_color=COOL_BLUE if self.edit_mode else row_color,
                    command=lambda i=index: self.controller.select_patient(i)
                )
                cell.grid(
                    row=visible_row,
                    column=column,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )

            visible_row += 1

        # Если список стал короче (например, после удаления), прячем лишние ячейки.
        for cells in self.table_rows[len(patients):]:
            for cell in cells:
                cell.grid_remove()

    def get_form_data(self):
        """Возвращает введённые значения."""
        return {
            "surname": self.surname_entry.get().strip(),
            "name": self.name_entry.get().strip(),
            "patronymic": self.patronymic_entry.get().strip(),
            "age": self.age_entry.get().strip(),
            "height": self.height_entry.get().strip(),
            "weight": self.weight_entry.get().strip(),
            "sex": self.sex_var.get()
        }

    def clear_form(self):
        """Очищает все поля карточки."""
        entries = [
            self.surname_entry, self.name_entry, self.patronymic_entry,
            self.age_entry, self.height_entry, self.weight_entry
        ]

        for entry in entries:
            entry.delete(0, "end")

        self.sex_var.set("")
        self.bmi_value.configure(text="—")

    def fill_form(self, patient):
        """Переносит выбранного пациента в поля ввода."""
        self.clear_form()

        self.surname_entry.insert(0, patient["Фамилия"])
        self.name_entry.insert(0, patient["Имя"])
        self.patronymic_entry.insert(0, patient["Отчество"])
        self.age_entry.insert(0, str(patient["Возраст"]))
        self.height_entry.insert(0, str(patient["Рост"]))
        self.weight_entry.insert(0, str(patient["Вес"]))
        self.sex_var.set(patient["Пол"])
        self.bmi_value.configure(text=str(patient["ИМТ"]))

    def set_edit_mode(self, enabled):
        """Меняет надписи кнопок при редактировании."""
        self.edit_mode = enabled

        if enabled:
            self.add_button.configure(text="Сохранить")
            self.edit_button.configure(text="Отмена")
        else:
            self.add_button.configure(text="＋ Добавить")
            self.edit_button.configure(text="Изменить")

    def show_error(self, message):
        messagebox.showerror("Ошибка", message)

    def show_info(self, message):
        messagebox.showinfo("Информация", message)

    def ask_confirmation(self, message):
        return messagebox.askyesno("Подтверждение", message)
