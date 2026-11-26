import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

from model import (
    load_patients,
    save_patients,
    create_patient
)
from view import View


class Controller:
    """Связывает интерфейс, данные и действия пользователя."""

    def __init__(self, root):
        self.root = root
        self.patients = load_patients()
        self.editing = False
        self.selected_index = None

        self.view = View(root, self)
        self.view.update_table(self.patients)

    def read_patient_from_form(self):
        """Берёт данные из полей и передаёт их на проверку."""
        data = self.view.get_form_data()

        patient = create_patient(
            data["surname"],
            data["name"],
            data["patronymic"],
            data["age"],
            data["height"],
            data["weight"],
            data["sex"]
        )

        return patient

    def add_or_save(self):
        """Добавляет нового пациента или сохраняет изменения."""
        try:
            patient = self.read_patient_from_form()

            if self.editing:
                if self.selected_index is None:
                    self.view.show_error("Сначала выберите пациента в таблице.")
                    return

                self.patients[self.selected_index] = patient
                self.editing = False
                self.selected_index = None
                self.view.set_edit_mode(False)
                self.view.show_info("Изменения сохранены.")

            else:
                self.patients.append(patient)
                self.view.show_info("Пациент добавлен.")

            save_patients(self.patients)
            self.view.clear_form()
            self.view.update_table(self.patients)

        except ValueError as error:
            self.view.show_error(str(error))
        except OSError:
            self.view.show_error("Не удалось сохранить файл с пациентами.")

    def start_or_cancel_edit(self):
        """Включает режим редактирования или отменяет его."""
        if self.editing:
            self.editing = False
            self.selected_index = None
            self.view.set_edit_mode(False)
            self.view.clear_form()
            self.view.update_table(self.patients)
            return

        self.editing = True
        self.selected_index = None
        self.view.set_edit_mode(True)
        self.view.update_table(self.patients)
        self.view.show_info(
            "Нажмите на строку пациента в таблице. "
            "Его данные появятся в карточке слева."
        )

    def select_patient(self, index):
        """Выбирает пациента для редактирования."""
        if not self.editing:
            return

        self.selected_index = index
        patient = self.patients[index]
        self.view.fill_form(patient)

    def clear_all(self):
        """Удаляет всех пациентов после подтверждения."""
        answer = self.view.ask_confirmation(
            "Удалить всех пациентов и очистить файл?"
        )

        if answer:
            self.patients = []
            self.editing = False
            self.selected_index = None

            save_patients(self.patients)
            self.view.set_edit_mode(False)
            self.view.clear_form()
            self.view.update_table(self.patients)

            self.view.show_info("Все карточки пациентов удалены.")

    def show_all_charts(self):
        """Открывает все четыре графика в одном окне."""

        if len(self.patients) == 0:
            self.view.show_error(
                "Сначала добавьте хотя бы одного пациента."
            )
            return

        data = pd.DataFrame(self.patients)
        window = ctk.CTkToplevel(self.root)
        window.title("Вся статистика пациентов")
        window.geometry("1100x800")
        window.configure(fg_color="#F2F8FF")

        figure, axes = plt.subplots(2, 2, figsize=(12, 8))
        figure.patch.set_facecolor("#F2F8FF")

        sex_counts = data["Пол"].value_counts()
        axes[0, 0].bar(
            sex_counts.index, sex_counts.values,
            color=["#9FC8EE", "#B7D8F7", "#CFE6FF"][:len(sex_counts)]
        )
        axes[0, 0].set_title("Распределение пациентов по полу")
        axes[0, 0].set_xlabel("Пол")
        axes[0, 0].set_ylabel("Количество пациентов")

        axes[0, 1].hist(
            data["Возраст"], bins=10,
            color="#9FC8EE", edgecolor="#35536F"
        )
        axes[0, 1].set_title("Распределение пациентов по возрасту")
        axes[0, 1].set_xlabel("Возраст, лет")
        axes[0, 1].set_ylabel("Количество пациентов")

        sexes = ["М", "Ж", "Н/О"]
        bmi_groups = [
            data[data["Пол"] == sex]["ИМТ"].tolist()
            for sex in sexes
        ]
        non_empty_groups = []
        non_empty_labels = []
        for sex, values in zip(sexes, bmi_groups):
            if values:
                non_empty_groups.append(values)
                non_empty_labels.append(sex)

        if non_empty_groups:
            axes[1, 0].boxplot(
                non_empty_groups, tick_labels=non_empty_labels
            )
        axes[1, 0].set_title("Распределение ИМТ с учётом пола")
        axes[1, 0].set_xlabel("Пол")
        axes[1, 0].set_ylabel("ИМТ")

        axes[1, 1].scatter(
            data["Возраст"], data["ИМТ"],
            color="#5796CD", alpha=0.8
        )
        axes[1, 1].set_title("Зависимость ИМТ от возраста")
        axes[1, 1].set_xlabel("Возраст, лет")
        axes[1, 1].set_ylabel("ИМТ")

        for axis in axes.flat:
            axis.grid(True, alpha=0.25)

        figure.tight_layout()
        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        def close_window():
            plt.close(figure)
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", close_window)

    def show_charts(self, graph_number):
        """Открывает выбранный график."""

        if len(self.patients) == 0:
            self.view.show_error(
                "Сначала добавьте хотя бы одного пациента."
            )
            return

        data = pd.DataFrame(self.patients)

        window = ctk.CTkToplevel(self.root)
        window.title("Статистика пациентов")
        window.geometry("800x600")
        window.configure(fg_color="#F2F8FF")

        figure, axis = plt.subplots(figsize=(8, 6))
        figure.patch.set_facecolor("#F2F8FF")

        if graph_number == 1:
            sex_counts = data["Пол"].value_counts()
            axis.bar(
                sex_counts.index, sex_counts.values,
                color=["#9FC8EE", "#B7D8F7", "#CFE6FF"][:len(sex_counts)]
            )
            axis.set_title("Распределение пациентов по полу")
            axis.set_xlabel("Пол")
            axis.set_ylabel("Количество пациентов")

        elif graph_number == 2:
            axis.hist(
                data["Возраст"], bins=10,
                color="#9FC8EE", edgecolor="#35536F"
            )
            axis.set_title("Распределение пациентов по возрасту")
            axis.set_xlabel("Возраст, лет")
            axis.set_ylabel("Количество пациентов")

        elif graph_number == 3:
            sexes = ["М", "Ж", "Н/О"]
            bmi_groups = [
                data[data["Пол"] == sex]["ИМТ"].tolist()
                for sex in sexes
            ]
            non_empty_groups = []
            non_empty_labels = []

            for sex, values in zip(sexes, bmi_groups):
                if len(values) > 0:
                    non_empty_groups.append(values)
                    non_empty_labels.append(sex)

            axis.boxplot(
                non_empty_groups, tick_labels=non_empty_labels
            )
            axis.set_title("Распределение ИМТ с учётом пола")
            axis.set_xlabel("Пол")
            axis.set_ylabel("ИМТ")

        elif graph_number == 4:
            axis.scatter(
                data["Возраст"], data["ИМТ"],
                color="#5796CD", alpha=0.8
            )
            axis.set_title("Зависимость ИМТ от возраста")
            axis.set_xlabel("Возраст, лет")
            axis.set_ylabel("ИМТ")

        axis.grid(True, alpha=0.25)
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        def close_window():
            plt.close(figure)
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", close_window)
