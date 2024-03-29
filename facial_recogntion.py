#FINAL PROJECT: Facial Recognition 
# https://www.youtube.com/watch?v=z_dbnYHAQYg&t=461s

# Libraries
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import os
import subprocess
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

class App:
    def __init__(self):
        # Initialize the main window
        self.intro_window = tk.Tk()
        self.intro_window.title("Welcome to Facial Recognition")
        self.intro_window.geometry("400x200+568+332")
        self.intro_window.configure(background='#335357')
        self.intro_window.resizable(False, False)
        
        # Create and pack widgets for the introduction window
        self.label_intro_window = util.get_text_label(self.intro_window, "Facial Recognition System")
        self.label_intro_window.pack(pady=20)

        self.start_button = util.get_button(self.intro_window, 'Start', 'green', self.start_main_application)
        self.start_button.pack()

    def start_main_application(self):
        # Destroy the introduction window and create the main window
        self.intro_window.destroy()
        self.main_window = tk.Tk()
        self.main_window.title("Facial Recognition System")
        self.main_window.geometry("1200x520+168+172")
        self.main_window.configure(background='#335357')
        self.main_window.resizable(False, False)

        # Widgets for the main window
        self.text_label_main_window = util.get_cincode_label(self.main_window, "CINCODE\nAttendance\nSystem")
        self.text_label_main_window.place(x=780, y=45)

        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=770, y=300)
        
        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register New User', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=770, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=10, width=700, height=500)

        self.add_webcam(self.webcam_label)
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.log_path = './log.txt'

    def add_webcam(self,label):
        # Add webcam to the label
        if 'capture' not in self.__dict__:
            self.capture = cv2.VideoCapture(0)
        
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        # Process webcam feed
        ret, frame = self.capture.read()
        self.most_recent_capture_array = frame

        img_ = cv2.cvtColor(self.most_recent_capture_array, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_array_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_array_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        # Perform login using facial recognition
        unknown_person = './.tmp.jpg'

        cv2.imwrite(unknown_person, self.most_recent_capture_array)
        
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_person]))
        name = output.split(',') [1][:-3][:-2]
        
        if name in ["unknown_person", "no_persons_found"]:
            util.msg_box('Error', 'No match found, please register new user or try again.')
        else:
            util.msg_box('Welcome', 'Welcome, {}'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close()
            self.send_email()
        os.remove(unknown_person)

    def register_new_user(self):
        # Register a new user
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.title("Register New User")
        self.register_new_user_window.configure(background='#335357')
        self.register_new_user_window.resizable(False, False)
        self.register_new_user_window.geometry("1200x520+180+187")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green',
                                                                       self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=760, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red', 
                                                                         self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=760, y=400)       

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=760, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Enter your username:')
        self.text_label_register_new_user.place(x=800, y=70)

        self.add_img_to_label(self.capture_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

    def try_again_register_new_user(self):
        # Close the register new user window
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        # Add image to label in register new user window
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_array_pil)        
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_capture = self.most_recent_capture_array.copy()
    
    def accept_register_new_user(self):
        # Accept the registration of a new user
        name = self.entry_text_register_new_user.get("1.0", "end-1c")
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_capture)

        util.msg_box('Success','User registered successfully')
        self.register_new_user_window.destroy()

    def send_email(self):
        # Send an email with the log file
        email_address = "testingforkeylog@gmail.com" 
        password = "zfqqffoxtxaprkvd"  
        toaddr = "testingforkeylog@gmail.com" 

        fromaddr = email_address

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Log File"
        body = "Logsheet Attendance"
        msg.attach(MIMEText(body, 'plain'))

        filename = "log.txt"
        attachment = open(filename, "rb")

        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, password)
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        util.msg_box('Success','Log saved')

    def start(self):
        # Start the main loop
        self.intro_window.mainloop()

# Run the application
if __name__ == "__main__":
    app = App()
    app.start()