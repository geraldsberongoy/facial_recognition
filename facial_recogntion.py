#FINAL PROJECT: Facial Recognition 
# https://www.youtube.com/watch?v=z_dbnYHAQYg&t=461s

import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import os

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.title("Facial Recognition")

        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)
        
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register New User', 'gray',
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
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green',
                                                                       self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red', 
                                                                         self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)       

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Enter your username:')
        self.text_label_register_new_user.place(x=790, y=70)


        self.add_img_to_label(self.capture_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_array_pil)        
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_capture = self.most_recent_capture_array.copy()




    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get("1.0", "end-1c")
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_capture)

        util.msg_box('User registered successfully', 'Success')
        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()
if __name__ == "__main__":
    app = App()
    app.start()