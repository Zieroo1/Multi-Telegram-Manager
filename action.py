import fnmatch
import os
import shutil
import subprocess
import time
import tkinter as tk
import psutil
import pyautogui

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget
from image_list_item import image_list_item
from worker import worker


class view_model(QWidget):
    data_changed = pyqtSignal()
    def __init__ (self, directory):
        super().__init__(None)
        self.profile_dir = directory
        self.profiles = []
        self.profile_items = []
        self.update()
        self.scale = False
        self.worker = None

    def get_profile_list(self, directory):
        # Проверяем, что указанная директория существует
        if not os.path.exists(directory):
            print(f"Directory '{directory}' does not exist.")
            return []

        # Получаем список всех элементов в директории
        items = os.listdir(directory)

        # Фильтруем только папки
        folders = [os.path.join(directory, item) for item in items if os.path.isdir(os.path.join(directory, item))]

        return folders

    def create_profile_item(self):
        profile_items = []
        for i, profile_name in enumerate(self.profiles, start=1):
            unchecked_icon_path = os.path.join('gui_img', 'tguncli.png')
            checked_icon_path = os.path.join('gui_img', 'tgcli.png')
            icon_size = QSize(38, 38)
            item = image_list_item(unchecked_icon_path, checked_icon_path, icon_size, profile_name)
            item.setData(Qt.UserRole, profile_name)
            item.setSizeHint(QSize(180, 43))
            item.setTextAlignment(Qt.AlignCenter)
            profile_items.append(item)

        return profile_items

    def on_item_clicked(self, item):
        item.setChecked(not item.icon().cacheKey() == item.checked_icon.cacheKey())

    def select_all_action(self):
        for i in self.profile_items:
            i.setChecked(True)

    def unselect_all_action(self):
        for i in self.profile_items:
            i.setChecked(False)

    def launch(self):
        for tdata_path in self.get_checked():
            self.create_inst(tdata_path.item.profile)
            self.launch_telegram_with_tdata(tdata_path.item.profile)
        time.sleep(5)
        if len(self.get_checked()) > 0 and self.scale:
            self.position_windows(len(self.get_checked()))

    def start_worker(self, function, *args, **kwargs):
        self.worker = worker(function, *args, **kwargs)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.result.connect(self.handle_result)
        self.worker.start()

    def handle_result(self, result):
        pass

    def get_checked(self):
        checked = []
        for i in self.profile_items:
            if i.item.select:
                checked.append(i)
        return checked

    def create_inst(self, inst):
        number = inst.split('_')[1]
        inst_new = 'tg\\' + number
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

        self.copy_tdata(inst, inst_new)

    def copy_tdata(self, tdata, inst):

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

    def launch_telegram_with_tdata(self, inst):
        number = inst.split('_')[1]
        inst_new = 'tg\\' + number
        telegram_path = f'{inst_new}\\Telegram.exe'
        command = f"{telegram_path}"
        subprocess.Popen(command, shell=True)
        time.sleep(3)

    def get_screen_resolution(self):
        root = tk.Tk()
        root.withdraw()
        return root.winfo_screenwidth(), root.winfo_screenheight()

    def position_windows(self, num_windows):
        screen_width, screen_height = self.get_screen_resolution()
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

    def update(self):
        self.profiles = self.get_profile_list(self.profile_dir)
        self.profile_items = self.create_profile_item()
        self.data_changed.emit()

    def delete_profile(self):
        for profile in self.get_checked():
            try:
                if os.path.exists(profile.item.inst):
                    shutil.rmtree(profile.item.inst)
                    print(f"Inst '{profile.item.name}' успешно удален.")
                if os.path.exists(profile.item.profile):
                    shutil.rmtree(profile.item.profile)
                    print(f"Профиль '{profile.item.name}' успешно удален.")
            except Exception as e:
                print(f"Ошибка при удалении профиля: {e}")

        self.update()

    def stop(self):
        base_path = os.getcwd()
        process_name = 'Telegram.exe'
        path_pattern = os.path.normcase(os.path.join(base_path, 'tg', '*', process_name))

        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                # Проверяем, совпадает ли имя процесса и путь
                if proc.info['name'] == process_name and fnmatch.fnmatch(os.path.normcase(proc.info['exe']), path_pattern):
                    # Завершаем процесс
                    proc.kill()
                    print(f"Процесс {process_name} с PID {proc.info['pid']} был убит")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                # Игнорируем ошибки, если процесс уже не существует или недоступен
                print(f"Не удалось убить процесс {process_name}: {e}")

    def switch_scale(self):
        self.scale = not self.scale

