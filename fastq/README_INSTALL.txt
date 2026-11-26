FASTQ ANALYZER — MVC
====================

ВАЖНО:
Групповой репозиторий не изменяем.
Скопируйте из него sequence_reader.py и reader.py в папку этой программы.
Оба файла должны лежать рядом с main.py, model.py, view.py и controller.py.

СТРУКТУРА ПАПКИ:

FASTQ_Analyzer/
    main.py
    model.py
    view.py
    controller.py
    sequence_reader.py
    reader.py
    FASTQ_files/
        ваш_файл.fastq

FASTQ-файл можно положить также прямо в папку FASTQ_Analyzer.
Выпадающий список ищет *.fastq и *.fq в этих двух местах.

1. Откройте терминал в папке FASTQ_Analyzer.

2. Установите системные компоненты (Ubuntu/Debian):

    sudo apt update
    sudo apt install python3-venv python3-tk

3. Создайте виртуальное окружение:

    python3 -m venv .venv
    source .venv/bin/activate

4. Установите библиотеки:

    python -m pip install --upgrade pip
    python -m pip install customtkinter matplotlib pillow

5. Запустите графический интерфейс:

    python main.py --gui

6. Запустите командную строку:

    python main.py -i "FASTQ_files/ваш_файл.fastq"

Только количество последовательностей:

    python main.py -i "FASTQ_files/ваш_файл.fastq" -a count

Только средняя длина:

    python main.py -i "FASTQ_files/ваш_файл.fastq" -a avg_len

Только график:

    python main.py -i "FASTQ_files/ваш_файл.fastq" -a plot

Справка:

    python main.py --help

КАК РАБОТАЕТ PNG:

1. Model вызывает исходный reader.plot_quality().
2. Исходный метод строит график Matplotlib и сохраняет quality_plot.png.
3. Model возвращает путь к созданному PNG.
4. View открывает файл через Pillow (Image.open).
5. View создаёт CTkImage и показывает картинку в окне.

То есть PNG не импортируется как Python-модуль.
Это обычная картинка, которую программа открывает и показывает.

ВАЖНО ПРО ПУТЬ К PNG:
Исходный plot_quality() сохраняет quality_plot.png в текущую рабочую папку
(обычно это папка, из которой вы запустили команду python).
Поэтому запускайте программу из папки FASTQ_Analyzer.

Исходные sequence_reader.py и reader.py не изменяются.
Файл quality_plot.png будет создаваться или перезаписываться при каждом новом анализе.
