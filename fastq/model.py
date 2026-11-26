import os

from sequence_reader import FastqReader


class FastqModel:
    """Модель: обрабатывает FASTQ-файл и получает результаты."""

    def get_statistics(self, filename):
        reader = FastqReader(filename)

        count = reader.get_sequences_count()
        average_length = reader.get_average_length()

        return count, average_length

    def create_graph(self, filename):
        reader = FastqReader(filename)

        # Удаляем старый график, чтобы случайно не показать его снова.
        graph_path = os.path.abspath("quality_plot.png")

        if os.path.exists(graph_path):
            os.remove(graph_path)

        # Это исходный метод из группового проекта.
        # Мы его не меняем: он сам создаёт quality_plot.png.
        reader.plot_quality()

        if not os.path.exists(graph_path):
            raise ValueError(
                "График не был создан. Проверьте, что выбран настоящий FASTQ-файл."
            )

        return graph_path
