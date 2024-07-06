import json
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog

from decoder import decode_all

CONFIG_FILE = "config.json"
SATDUMP_PATH_NAME = "satdump_folder"
INPUT_PATH_NAME = "input_folder"
OUTPUT_PATH_NAME = "output_folder"


def build_path_field(root, label: str, default_insert: str, button_command, row: int):
    tk.Label(root, text=label).grid(row=row, column=0, sticky="e")
    entry = tk.Entry(root, width=50)
    entry.grid(row=row, column=1)
    entry.insert(0, default_insert)
    tk.Button(root, text="Browse", command=button_command).grid(row=row, column=2)
    return entry


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {SATDUMP_PATH_NAME: "", INPUT_PATH_NAME: "", OUTPUT_PATH_NAME: ""}


class DecoderUI:
    def __init__(self):
        self.progress_var = None
        self.run_button = None
        self.satdump_folder_entry = None
        self.input_folder_entry = None
        self.output_folder_entry = None

    def start_ui(self):
        root = self.build_ui()
        root.mainloop()

    def build_ui(self):
        root = tk.Tk()
        root.title("Interface")

        # Загрузка сохраненной конфигурации
        config = load_config()

        # Поле для пути к файлу
        default_exe_path = config[SATDUMP_PATH_NAME]
        self.satdump_folder_entry = build_path_field(
            root=root,
            label="The path to the SatDump folder:",
            default_insert=default_exe_path,
            button_command=self.browse_satdump_folder,
            row=0
        )

        # Поле для пути к папке с входными данными
        default_input_path = config[INPUT_PATH_NAME]
        self.input_folder_entry = build_path_field(
            root=root,
            label="The folder with the input data:",
            default_insert=default_input_path,
            button_command=self.browse_input_folder,
            row=1
        )

        # Поле для пути к папке с результирующими данными
        default_output_path = config[OUTPUT_PATH_NAME]
        self.output_folder_entry = build_path_field(
            root=root,
            label="Results folder:",
            default_insert=default_output_path,
            button_command=self.browse_output_folder,
            row=2
        )

        # Кнопка запуска скрипта
        self.run_button = tk.Button(root, text="Run the script", command=self.run_script)
        self.run_button.grid(row=3, column=1)

        # Индикатор прогресса
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=1000)
        progress_bar.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # Сохранение конфигурации при закрытии окна
        root.protocol("WM_DELETE_WINDOW", lambda: (self.save_config(), root.destroy()))

        return root

    def save_config(self):
        config = {
            SATDUMP_PATH_NAME: self.satdump_folder_entry.get(),
            INPUT_PATH_NAME: self.input_folder_entry.get(),
            OUTPUT_PATH_NAME: self.output_folder_entry.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    def browse_satdump_folder(self):
        filename = filedialog.askdirectory()
        self.satdump_folder_entry.delete(0, tk.END)
        self.satdump_folder_entry.insert(0, filename)

    def browse_input_folder(self):
        folder = filedialog.askdirectory()
        self.input_folder_entry.delete(0, tk.END)
        self.input_folder_entry.insert(0, folder)

    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        self.output_folder_entry.delete(0, tk.END)
        self.output_folder_entry.insert(0, folder)

    def run_script(self):
        satdump_folder = self.satdump_folder_entry.get()
        input_folder = self.input_folder_entry.get()
        output_folder = self.output_folder_entry.get()

        exe_path = f"{satdump_folder}/bin/satdump.exe"

        # Блокировка кнопки на время выполнения
        self.run_button.config(state=tk.DISABLED)

        # Запуск декодинга в отдельном потоке чтобы не блокировать главный поток и UI
        thread = threading.Thread(
            target=decode_all,
            args=(exe_path, input_folder, output_folder, self.progress_var, self.unblock_button)
        )
        thread.start()

        self.save_config()

    def unblock_button(self):
        self.run_button.config(state=tk.NORMAL)
