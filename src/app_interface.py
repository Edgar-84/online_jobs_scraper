import sys
import tkinter as tk
from threading import Thread


class StdoutRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, string)
        self.widget.configure(state='disabled')
        self.widget.see(tk.END)

    def flush(self):
        pass


class AppInterface:
    def __init__(self, scraper_start):
        self.__app_name = "Online Jobs Scraper"
        self.scraper_start = scraper_start
        self.root = tk.Tk()
        self.root.title(self.__app_name)
        self.root.geometry("800x500")

        checkbox_frame = tk.Frame(self.root)
        checkbox_frame.pack(side=tk.LEFT, padx=5, pady=5)
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(fill=tk.X, padx=5, pady=5)

        entry_label = tk.Label(entry_frame, text="Enter job title to search:  ")
        entry_label.pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(entry_frame, width=30)
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.search_button = tk.Button(entry_frame, text="Search", command=self.perform_search)
        self.search_button.pack(pady=5)

        self.text_box = tk.Text(self.root, state='disabled')
        self.text_box.pack(expand=True, fill='both')

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_text_box)
        clear_button.pack()

        self.excel_var = tk.BooleanVar(value=True)
        self.json_var = tk.BooleanVar()
        self.excel_checkbox = tk.Checkbutton(checkbox_frame, text="Excel", variable=self.excel_var)
        self.json_checkbox = tk.Checkbutton(checkbox_frame, text="Json", variable=self.json_var)
        self.excel_checkbox.pack(anchor=tk.W)
        self.json_checkbox.pack(anchor=tk.W)

        self.last_1000_var = tk.BooleanVar(value=False)
        self.last_1000_button = tk.Button(checkbox_frame, text="Get last vacancies",
                                          command=self.perform_last_search)
        self.last_1000_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

    def perform_last_search(self):
        self.last_1000_var.set(True)
        self.perform_search()

    def disable_search_button(self):
        self.search_button.config(state=tk.DISABLED)
        self.last_1000_button.config(state=tk.DISABLED)

    def enable_search_button(self):
        self.search_button.config(state=tk.NORMAL)
        self.last_1000_button.config(state=tk.NORMAL)
        self.last_1000_var.set(False)

    def clear_text_box(self):
        self.text_box.configure(state='normal')
        self.text_box.delete('1.0', tk.END)
        self.text_box.configure(state='disabled')

    def perform_search(self):
        user_input = self.entry.get()
        excel_info = self.excel_var.get()
        json_info = self.json_var.get()
        last_vacancies_info = self.last_1000_var.get()
        self.disable_search_button()
        Thread(
            target=self.scraper_start,
            args=(user_input,
                  self.enable_search_button,
                  excel_info,
                  json_info,
                  last_vacancies_info),
        ).start()

    def run(self):
        redirector = StdoutRedirector(self.text_box)
        sys.stdout = redirector
        self.root.mainloop()
        sys.stdout = sys.__stdout__
