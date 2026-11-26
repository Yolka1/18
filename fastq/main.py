import argparse
import os

from model import FastqModel
from view import FastqView
from controller import FastqController


def run_command_line(filename, action):
    """Простой режим командной строки для FASTQ."""
    if not os.path.exists(filename):
        print("Ошибка: файл не найден.")
        return

    model = FastqModel()

    if action == "count" or action == "all":
        count, average_length = model.get_statistics(filename)
        print("Количество последовательностей:", count)

    if action == "avg_len":
        count, average_length = model.get_statistics(filename)
        print("Средняя длина последовательности:", round(average_length, 2))

    if action == "all":
        print("Средняя длина последовательности:", round(average_length, 2))

    if action == "plot" or action == "all":
        graph_path = model.create_graph(filename)
        print("График сохранён:", graph_path)


def main():
    parser = argparse.ArgumentParser(
        description="Программа для анализа FASTQ-файлов."
    )

    parser.add_argument(
        "--gui",
        action="store_true",
        help="Запустить графический интерфейс."
    )

    parser.add_argument(
        "-i", "--input",
        help="Путь к FASTQ-файлу для командной строки."
    )

    parser.add_argument(
        "-a", "--action",
        choices=["count", "avg_len", "plot", "all"],
        default="all",
        help="Действие: count, avg_len, plot или all."
    )

    args = parser.parse_args()

    if args.gui:
        model = FastqModel()
        view = FastqView()
        controller = FastqController(model, view)
        view.run()

    elif args.input:
        run_command_line(args.input, args.action)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
