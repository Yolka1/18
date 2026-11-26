import os


class FastqController:
    """Контроллер: связывает действия пользователя, модель и интерфейс."""

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.set_analyze_command(self.analyze)

    def analyze(self):
        filename = self.view.get_selected_file()

        if not filename:
            self.view.show_warning("Сначала выберите FASTQ-файл.")
            return

        if not os.path.exists(filename):
            self.view.show_error("Выбранный файл не найден.")
            return

        try:
            count, average_length = self.model.get_statistics(filename)

            if count == 0:
                self.view.show_warning(
                    "В файле не найдены последовательности."
                )
                return

            graph_path = self.model.create_graph(filename)

            self.view.show_statistics(count, average_length)
            self.view.show_graph(graph_path)

        except Exception as error:
            self.view.show_error(str(error))
