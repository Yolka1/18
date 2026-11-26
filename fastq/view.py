import os
import glob
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD


class CTkDND(ctk.CTk, TkinterDnD.DnDWrapper):
    """Окно CustomTkinter с поддержкой перетаскивания файлов."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


class FastqView:
    """Представление: создаёт окно и показывает информацию пользователю."""

    def __init__(self):
        ctk.set_appearance_mode("light")

        self.window = CTkDND()
        self.window.title("FASTQ Analyzer")
        self.window.geometry("900x780")
        self.window.minsize(700, 600)
        self.window.configure(fg_color="#F8F1E7")

        self.selected_file = ""
        self.graph_image = None

        self.create_widgets()
        self.find_fastq_files()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self.window,
            text="FASTQ Analyzer",
            font=("Arial", 30, "bold"),
            text_color="#8B4B3A"
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self.window,
            text="Анализ файлов с биологическими последовательностями",
            font=("Arial", 14),
            text_color="#704638"
        )
        subtitle.pack(pady=(0, 15))

        self.main_frame = ctk.CTkFrame(
            self.window,
            fg_color="#F1DFC8",
            corner_radius=18
        )
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=10)

        file_label = ctk.CTkLabel(
            self.main_frame,
            text="Выберите FASTQ-файл",
            font=("Arial", 18, "bold"),
            text_color="#63372D"
        )
        file_label.pack(anchor="w", padx=25, pady=(20, 8))

        self.file_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["Файлы не найдены"],
            command=self.select_from_list,
            width=520,
            fg_color="#8B4B3A",
            button_color="#704033",
            button_hover_color="#63372D"
        )
        self.file_menu.pack(anchor="w", padx=25, pady=5)

        choose_button = ctk.CTkButton(
            self.main_frame,
            text="Выбрать файл на компьютере",
            command=self.open_file,
            fg_color="#E8C49A",
            hover_color="#D8AE7F",
            text_color="#63372D",
            width=250
        )
        choose_button.pack(anchor="w", padx=25, pady=8)

        # Область, в которую можно перетащить FASTQ-файл из проводника.
        self.drop_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#FFF8EE",
            border_width=2,
            border_color="#C99A75",
            corner_radius=12,
            height=75
        )
        self.drop_frame.pack(fill="x", padx=25, pady=(5, 12))
        self.drop_frame.pack_propagate(False)

        self.drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="Или перетащите FASTQ-файл сюда",
            font=("Arial", 14),
            text_color="#8B4B3A"
        )
        self.drop_label.pack(expand=True)

        # Регистрируем и рамку, и надпись как области для перетаскивания.
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind("<<Drop>>", self.on_file_drop)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.on_file_drop)

        self.analyze_button = ctk.CTkButton(
            self.main_frame,
            text="Обработать файл",
            command=None,  # Команду кнопке назначает Controller
            fg_color="#8B4B3A",
            hover_color="#704033",
            text_color="#FFF8EE",
            width=200,
            height=38
        )
        self.analyze_button.pack(anchor="w", padx=25, pady=(5, 15))

        stats_title = ctk.CTkLabel(
            self.main_frame,
            text="Статистика",
            font=("Arial", 20, "bold"),
            text_color="#63372D"
        )
        stats_title.pack(anchor="w", padx=25, pady=(0, 5))

        self.stats_label = ctk.CTkLabel(
            self.main_frame,
            text="Выберите файл и нажмите «Обработать файл».",
            font=("Arial", 15),
            text_color="#63372D",
            justify="left"
        )
        self.stats_label.pack(anchor="w", padx=25, pady=(0, 12))

        graph_title = ctk.CTkLabel(
            self.main_frame,
            text="График качества",
            font=("Arial", 20, "bold"),
            text_color="#63372D"
        )
        graph_title.pack(anchor="w", padx=25, pady=(0, 8))

        self.graph_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#FFF8EE",
            corner_radius=12
        )
        self.graph_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        self.graph_label = ctk.CTkLabel(
            self.graph_frame,
            text="Здесь появится PNG-график",
            text_color="#8B4B3A"
        )
        self.graph_label.pack(expand=True, padx=10, pady=10)

    def find_fastq_files(self):
        """Ищет FASTQ-файлы в папке программы и в FASTQ_files."""
        folder = os.path.dirname(os.path.abspath(__file__))

        patterns = [
            os.path.join(folder, "*.fastq"),
            os.path.join(folder, "*.fq"),
            os.path.join(folder, "FASTQ_files", "*.fastq"),
            os.path.join(folder, "FASTQ_files", "*.fq")
        ]

        self.files = []

        for pattern in patterns:
            self.files.extend(glob.glob(pattern))

        self.file_names = [os.path.basename(file) for file in self.files]

        if self.file_names:
            self.file_menu.configure(values=self.file_names)
            self.file_menu.set(self.file_names[0])
            self.selected_file = self.files[0]
        else:
            self.file_menu.configure(values=["Файлы не найдены"])
            self.file_menu.set("Файлы не найдены")

    def select_from_list(self, file_name):
        """Запоминает файл, выбранный в выпадающем списке."""
        for file_path in self.files:
            if os.path.basename(file_path) == file_name:
                self.selected_file = file_path

    def open_file(self):
        """Открывает стандартное окно выбора файла."""
        file_path = filedialog.askopenfilename(
            title="Выберите FASTQ-файл",
            filetypes=[
                ("FASTQ files", "*.fastq *.fq"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)

            if file_name not in self.file_names:
                self.files.append(file_path)
                self.file_names.append(file_name)
                self.file_menu.configure(values=self.file_names)

            self.file_menu.set(file_name)

    def on_file_drop(self, event):
        """Получает путь к файлу, который перетащили в окно."""
        # splitlist корректно обрабатывает пути с пробелами.
        dropped_files = self.window.tk.splitlist(event.data)

        if not dropped_files:
            return

        file_path = dropped_files[0]

        if not file_path.lower().endswith((".fastq", ".fq")):
            self.show_warning("Можно перетаскивать только файлы .fastq или .fq.")
            return

        if not os.path.isfile(file_path):
            self.show_error("Не удалось найти перетащенный файл.")
            return

        self.selected_file = file_path
        file_name = os.path.basename(file_path)

        if file_name not in self.file_names:
            self.files.append(file_path)
            self.file_names.append(file_name)
            self.file_menu.configure(values=self.file_names)

        self.file_menu.set(file_name)
        self.drop_label.configure(text="Выбран файл: " + file_name)

    def get_selected_file(self):
        return self.selected_file

    def show_statistics(self, count, average_length):
        text = (
            "Количество последовательностей: " + str(count) + "\n"
            + "Средняя длина последовательности: "
            + str(round(average_length, 2))
        )
        self.stats_label.configure(text=text)

    def show_graph(self, graph_path):
        """Открывает готовый PNG и показывает его в окне."""
        image = Image.open(graph_path)

        # Уменьшаем изображение, если оно слишком большое для окна.
        image.thumbnail((700, 350))

        self.graph_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )

        self.graph_label.configure(
            text="",
            image=self.graph_image
        )

    def show_error(self, message):
        messagebox.showerror("Ошибка", message)

    def show_warning(self, message):
        messagebox.showwarning("Внимание", message)

    def set_analyze_command(self, command):
        """Передаёт кнопке функцию контроллера."""
        # Кнопка создаётся в create_widgets; здесь задаём её команду.
        self.analyze_button.configure(command=command)

    def run(self):
        self.window.mainloop()
