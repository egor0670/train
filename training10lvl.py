import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime

# Имя файла для сохранения данных
DATA_FILE = "training_data.json"

# Создаем главное окно
root = tk.Tk()
root.title("Training Planner")

# --- Вводные поля ---
# Дата
tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5)
entry_date = tk.Entry(root)
entry_date.grid(row=0, column=1, padx=5, pady=5)

# Тип тренировки
tk.Label(root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
entry_type = tk.Entry(root)
entry_type.grid(row=1, column=1, padx=5, pady=5)

# Длительность
tk.Label(root, text="Длительность (минут):").grid(row=2, column=0, padx=5, pady=5)
entry_duration = tk.Entry(root)
entry_duration.grid(row=2, column=1, padx=5, pady=5)

# --- Таблица для отображения тренировок ---
columns = ("Дата", "Тип", "Длительность")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')

# Настраиваем растягивание
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(3, weight=1)

# --- Функции для работы с данными ---

def save_data():
    data = []
    for item in tree.get_children():
        record = tree.item(item)['values']
        data.append({'Дата': record[0], 'Тип': record[1], 'Длительность': record[2]})
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_table():
    # Загружаем из файла и заполняем таблицу
    data = load_data()
    for rec in data:
        tree.insert('', 'end', values=(rec['Дата'], rec['Тип'], rec['Длительность']))

# Загружать данные при запуске
load_table()

# --- Обработка добавления новой тренировки ---
def add_training():
    date_str = entry_date.get().strip()
    t_type = entry_type.get().strip()
    duration_str = entry_duration.get().strip()

    # Проверка даты
    try:
        datetime.datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте DD.MM.YYYY")
        return

    # Проверка длительности
    if not duration_str.isdigit() or int(duration_str) <= 0:
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
        return

    # Добавление записи в таблицу
    tree.insert('', 'end', values=(date_str, t_type, duration_str))
    save_data()  # сохраняем после добавления

    # Очистка полей
    entry_date.delete(0, tk.END)
    entry_type.delete(0, tk.END)
    entry_duration.delete(0, tk.END)

add_button = tk.Button(root, text="Добавить тренировку", command=add_training)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# --- Фильтрация ---
tk.Label(root, text="Фильтр по типу:").grid(row=5, column=0, padx=5, pady=5)
filter_type_entry = tk.Entry(root)
filter_type_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=6, column=0, padx=5, pady=5)
filter_date_entry = tk.Entry(root)
filter_date_entry.grid(row=6, column=1, padx=5, pady=5)

def apply_filters():
    filter_type = filter_type_entry.get().strip().lower()
    filter_date = filter_date_entry.get().strip()

    # Проверка формата даты фильтра, если введена
    if filter_date:
        try:
            datetime.datetime.strptime(filter_date, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат фильтра по дате. Используйте DD.MM.YYYY")
            return

    # Загружаем все данные и фильтруем
    data = load_data()

    # Очищаем таблицу
    for item in tree.get_children():
        tree.delete(item)

    for rec in data:
        if filter_type and filter_type not in rec['Тип'].lower():
            continue
        if filter_date and rec['Дата'] != filter_date:
            continue
        tree.insert('', 'end', values=(rec['Дата'], rec['Тип'], rec['Длительность']))

filter_button = tk.Button(root, text="Применить фильтр", command=apply_filters)
filter_button.grid(row=7, column=0, columnspan=2, pady=10)

# --- Запуск ---
root.mainloop()
