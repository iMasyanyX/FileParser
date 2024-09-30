import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def log_result(message):
    """Запись результата в файл log.txt с отметкой времени."""
    with open("log.txt", "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_file.write(f"{timestamp} - {message}\n")

def calculate_md5(file_path):
    """Вычисление контрольной суммы MD5 для файла."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compare_by_size(dir1, dir2):
    """Сравнение файлов в двух директориях по размеру."""
    files1 = {f: os.path.getsize(os.path.join(dir1, f)) for f in os.listdir(dir1) if os.path.isfile(os.path.join(dir1, f))}
    files2 = {f: os.path.getsize(os.path.join(dir2, f)) for f in os.listdir(dir2) if os.path.isfile(os.path.join(dir2, f))}

    common_files = set(files1.keys()).intersection(set(files2.keys()))
    differences_found = False

    for file in common_files:
        size1 = files1[file] // 1024  # Конвертация в КБ
        size2 = files2[file] // 1024  # Конвертация в КБ
        if size1 != size2:
            log_result(f"Файл '{file}' отличается (Размер: {dir1}: {size1} KB, {dir2}: {size2} KB)")
            differences_found = True

    if not differences_found:
        log_result("Все файлы прошли проверку по размеру.")

    show_result_message()

def compare_by_md5(dir1, dir2):
    """Сравнение файлов в двух директориях по контрольной сумме MD5."""
    files1 = {f: calculate_md5(os.path.join(dir1, f)) for f in os.listdir(dir1) if os.path.isfile(os.path.join(dir1, f))}
    files2 = {f: calculate_md5(os.path.join(dir2, f)) for f in os.listdir(dir2) if os.path.isfile(os.path.join(dir2, f))}

    common_files = set(files1.keys()).intersection(set(files2.keys()))
    differences_found = False

    for file in common_files:
        md5_1 = files1[file]
        md5_2 = files2[file]
        if md5_1 != md5_2:
            log_result(f"Файл '{file}' отличается (MD5: {dir1}: {md5_1}, {dir2}: {md5_2})")
            differences_found = True

    if not differences_found:
        log_result("Все файлы прошли проверку по MD5.")

    show_result_message()

def browse_directory(entry):
    """Выбор директории с помощью диалогового окна."""
    directory = filedialog.askdirectory()
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)

def show_result_message():
    """Показать сообщение о завершении работы программы."""
    messagebox.showinfo("Завершено", "Результат записан в log.txt")

# Создаем основное окно
root = tk.Tk()
root.title("[ROTcorp] FileParser")

# Поля для ввода директорий
label1 = tk.Label(root, text="Директория 1:")
label1.grid(row=0, column=0, padx=10, pady=5)

entry1 = tk.Entry(root, width=50)
entry1.grid(row=0, column=1, padx=10, pady=5)

button_browse1 = tk.Button(root, text="Обзор...", command=lambda: browse_directory(entry1))
button_browse1.grid(row=0, column=2, padx=10, pady=5)

label2 = tk.Label(root, text="Директория 2:")
label2.grid(row=1, column=0, padx=10, pady=5)

entry2 = tk.Entry(root, width=50)
entry2.grid(row=1, column=1, padx=10, pady=5)

button_browse2 = tk.Button(root, text="Обзор...", command=lambda: browse_directory(entry2))
button_browse2.grid(row=1, column=2, padx=10, pady=5)

# Создаем основной контейнер для кнопок
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=3, pady=10)  # Размещаем контейнер для кнопок

# Кнопки для сравнения внутри контейнера
button_compare_size = tk.Button(button_frame, text="Сравнить по весу", command=lambda: compare_by_size(entry1.get(), entry2.get()))
button_compare_size.grid(row=0, column=0, padx=10)  # Добавляем небольшой отступ справа от кнопки

button_compare_md5 = tk.Button(button_frame, text="Сравнить по MD5", command=lambda: compare_by_md5(entry1.get(), entry2.get()))
button_compare_md5.grid(row=0, column=1, padx=10)  # Добавляем такой же отступ слева от кнопки

# Запуск основного цикла программы
root.mainloop()




# Рекурсия

# def get_all_files_with_sizes(directory):
#     """Получить все файлы и их размеры в указанной директории рекурсивно."""
#     files = {}
#     for root, _, filenames in os.walk(directory):
#         for filename in filenames:
#             file_path = os.path.join(root, filename)
#             files[file_path[len(directory):]] = os.path.getsize(file_path)
#     return files
#
# def get_all_files_with_md5(directory):
#     """Получить все файлы и их контрольные суммы MD5 в указанной директории рекурсивно."""
#     files = {}
#     for root, _, filenames in os.walk(directory):
#         for filename in filenames:
#             file_path = os.path.join(root, filename)
#             files[file_path[len(directory):]] = calculate_md5(file_path)
#     return files
#
# def compare_by_size(dir1, dir2):
#     """Сравнение файлов в двух директориях по размеру, рекурсивно."""
#     files1 = get_all_files_with_sizes(dir1)
#     files2 = get_all_files_with_sizes(dir2)
#
#     common_files = set(files1.keys()).intersection(set(files2.keys()))
#     differences_found = False
#
#     for file in common_files:
#         size1 = files1[file] // 1024  # Конвертация в КБ
#         size2 = files2[file] // 1024  # Конвертация в КБ
#         if size1 != size2:
#             log_result(f"Файл '{file}' отличается (Размер: {dir1}: {size1} KB, {dir2}: {size2} KB)")
#             differences_found = True
#
#     if not differences_found:
#         log_result("Все файлы прошли проверку по размеру.")
#
#     show_result_message()
#
# def compare_by_md5(dir1, dir2):
#     """Сравнение файлов в двух директориях по контрольной сумме MD5, рекурсивно."""
#     files1 = get_all_files_with_md5(dir1)
#     files2 = get_all_files_with_md5(dir2)
#
#     common_files = set(files1.keys()).intersection(set(files2.keys()))
#     differences_found = False
#
#     for file in common_files:
#         md5_1 = files1[file]
#         md5_2 = files2[file]
#         if md5_1 != md5_2:
#             log_result(f"Файл '{file}' отличается (MD5: {dir1}: {md5_1}, {dir2}: {md5_2})")
#             differences_found = True
#
#     if not differences_found:
#         log_result("Все файлы прошли проверку по MD5.")
#
#     show_result_message()