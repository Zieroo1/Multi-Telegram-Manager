import os
import subprocess
import pyautogui
import time
import tkinter as tk
import shutil


def get_screen_resolution():
    root = tk.Tk()
    root.withdraw()
    return root.winfo_screenwidth(), root.winfo_screenheight()

def copy_tdata(tdata, inst):

    # Проверяем, существует ли исходный файл
    if not os.path.isdir(tdata):
        print(f"Нет профиля")
        return

    try:
        # Создаем путь для новой папки
        new_folder_path = os.path.join(inst, 'tdata')

        # Копируем папку со всем её содержимым рекурсивно
        shutil.copytree(tdata, new_folder_path)
        print(f"Папка '{tdata}' успешно скопирована в '{new_folder_path}'.")
    except Exception as e:
        print(f"Ошибка при копировании папки: {e}")

def create_inst(inst):
    number = inst.split('_')[1]
    inst_new = 'tg\\'+number
    source_file = 'Telegram.exe'

    # Проверяем, существует ли исходный файл
    if not os.path.isfile(source_file):
        print(f"Нет телеги")
        return

    # Проверяем, существует ли папка назначения, иначе создаем её
    if not os.path.exists(inst_new):
        os.makedirs(inst_new)

    # Получаем только имя файла из полного пути источника
    file_name = os.path.basename(source_file)

    # Путь для копии файла в папке назначения
    destination_file = os.path.join(inst_new, file_name)

    try:
        # Копируем файл
        shutil.copy2(source_file, destination_file)
        print(f"Файл успешно скопирован в {destination_file}")
    except Exception as e:
        print(f"Ошибка при копировании файла: {e}")

    copy_tdata(inst, inst_new)

def launch_telegram_with_tdata(inst):
    number = inst.split('_')[1]
    inst_new = 'tg\\' + number
    telegram_path = f'{inst_new}\\Telegram.exe'
    command = f"{telegram_path}"
    subprocess.Popen(command, shell=True)
    time.sleep(3)


def position_windows(num_windows):
    screen_width, screen_height = get_screen_resolution()
    cols = int(num_windows ** 0.5)
    rows = int(num_windows / cols) + (num_windows % cols > 0)
    window_width = screen_width // cols
    window_height = screen_height // rows

    telegram_windows = pyautogui.getWindowsWithTitle("Telegram")
    num_telegram_windows = len(telegram_windows)

    for i in range(min(num_telegram_windows, num_windows)):
        col = i % cols
        row = i // cols
        x = col * window_width
        y = row * window_height
        telegram_windows[i].moveTo(x, y)
        telegram_windows[i].resizeTo(window_width, window_height)

def get_folder_names(directory):
    # Проверяем, что указанная директория существует
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return []

    # Получаем список всех элементов в директории
    items = os.listdir(directory)

    # Фильтруем только папки
    folders = [os.path.join(directory, item) for item in items if os.path.isdir(os.path.join(directory, item))]

    return folders

def main():
    tdata_paths = get_folder_names('tdatas')

    for tdata_path in tdata_paths:
        create_inst(tdata_path)
        launch_telegram_with_tdata(tdata_path)

    time.sleep(5)
    position_windows(len(tdata_paths))


if __name__ == "__main__":
    main()
