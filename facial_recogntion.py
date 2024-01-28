#FINAL PROJECT: Facial Recognition 
# https://www.youtube.com/watch?v=z_dbnYHAQYg&t=461s

import tkinter as tk
import customtkinter as ctk

class App:
    def __init__(self):
        self.main_window = ctk.CTk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.title("Facial Recognition")
    def start(self):
        self.main_window.mainloop()
if __name__ == "__main__":
    app = App()
    app.start()