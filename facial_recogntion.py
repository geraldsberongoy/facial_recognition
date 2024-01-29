#FINAL PROJECT: Facial Recognition 
# https://www.youtube.com/watch?v=z_dbnYHAQYg&t=461s

import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.title("Facial Recognition")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)
        
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

    def add_webcam(self,label):
        if 'capture' not in self.__dict__:
            self.capture = cv2.VideoCapture(0)
        
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.capture.read()
        self.most_recent_capture_array = frame

        img_ = cv2.cvtColor(self.most_recent_capture_array, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_array_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_array_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        pass
    def register_new_user(self):
        pass


    def start(self):
        self.main_window.mainloop()
if __name__ == "__main__":
    app = App()
    app.start()