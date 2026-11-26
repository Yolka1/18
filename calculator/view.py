import customtkinter as ctk

# Цветовая палитра
COLORS = {
    "background": "#FFE5EC",
    "panel": "#FFC2D1",
    "buttons": "#FFB3C6",
    "operations": "#FF8FAB",
    "equals": "#FB6F92",
    "text": "#89235B"
}

# Главное окно
root = ctk.CTk()
root.title("Petal Calc")
root.geometry("430x720")
root.minsize(350, 620)

root.configure(fg_color=COLORS["background"])

# Основная панель
panel = ctk.CTkFrame(
    root,
    fg_color=COLORS["panel"],
    corner_radius=15,
    border_width=0
)

panel.pack(fill="both", expand=True, padx=15, pady=15)

# Пустая верхняя область
header = ctk.CTkFrame(
    panel,
    fg_color="transparent",
    height=40
)

header.pack(fill="x", padx=15)

# Поле ввода выражения
input_field = ctk.CTkTextbox(
    panel,
    height=90,
    wrap="none",
    font=("DejaVu Sans", 26),
    fg_color=COLORS["background"],
    text_color=COLORS["text"],
    corner_radius=20,
    activate_scrollbars=False
)

input_field.pack(fill="x", padx=15, pady=10)

# Полоса прокрутки
scrollbar = ctk.CTkScrollbar(
    panel,
    orientation="horizontal",
    command=input_field.xview,
    fg_color=COLORS["panel"],
    button_color=COLORS["buttons"],
    button_hover_color=COLORS["equals"],
    corner_radius=10,
    width=10,
    hover=True
)

scrollbar.pack(fill="x", padx=15, pady=(0, 10))

input_field.configure(
    xscrollcommand=scrollbar.set
)

# Поле вывода результата
result_field = ctk.CTkLabel(
    panel,
    text="0",
    height=80,
    font=("DejaVu Sans", 28, "bold"),
    fg_color=COLORS["background"],
    text_color=COLORS["text"],
    corner_radius=20
)

result_field.pack(fill="x", padx=15, pady=20)

# Панель кнопок
buttons_frame = ctk.CTkFrame(
    panel,
    fg_color="transparent"
)

buttons_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# Настройка расположения кнопок
for i in range(4):
    buttons_frame.grid_columnconfigure(i, weight=1)

for i in range(6):
    buttons_frame.grid_rowconfigure(i, weight=1)

# Расположение кнопок
button_layout = [
    ["", "", "C", "DEL"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["√", "0", ",", "+"]
]

buttons = {}

# Создание кнопок
for row in range(len(button_layout)):

    for column in range(4):

        symbol = button_layout[row][column]

        if symbol == "":
            continue

        if symbol in ["+", "-", "×", "÷", "√", "C", "DEL"]:
            color = COLORS["operations"]
            text_color = "white"
        else:
            color = COLORS["buttons"]
            text_color = COLORS["text"]

        button = ctk.CTkButton(
            buttons_frame,
            text=symbol,
            font=("DejaVu Sans", 22, "bold"),
            fg_color=color,
            hover_color=COLORS["equals"],
            text_color=text_color,
            corner_radius=18,
            command=None
        )

        button.grid(
            row=row,
            column=column,
            padx=5,
            pady=5,
            sticky="nsew"
        )

        buttons[symbol] = button

# Кнопка равно в нижнем левом углу
buttons["="] = ctk.CTkButton(
    buttons_frame,
    text="=",
    font=("DejaVu Sans", 25, "bold"),
    fg_color=COLORS["equals"],
    hover_color=COLORS["operations"],
    text_color="white",
    corner_radius=18,
    command=None
)

buttons["="].grid(
    row=5,
    column=0,
    columnspan=2,
    padx=5,
    pady=5,
    sticky="nsew"
)