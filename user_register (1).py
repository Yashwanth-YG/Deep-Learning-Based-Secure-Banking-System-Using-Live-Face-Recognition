import os.path
import datetime
import pickle

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition

import util
# from test import test
import csv


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=200)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

        self.fields = ['Name', 'Email', 'Phone','Bank','Account','Password','Balance']

        self.file_path = "records.csv"


    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1500x600")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'username:')
        self.text_label_register_new_user.place(x=750, y=40)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=950, y=45)

        self.text_label_email = util.get_text_label(self.register_new_user_window, 'email:')
        self.text_label_email.place(x=750, y=80)

        self.entry_email = util.get_entry_text(self.register_new_user_window)
        self.entry_email.place(x=950, y=85) 

        self.text_label_phone = util.get_text_label(self.register_new_user_window, 'phone:')
        self.text_label_phone.place(x=750, y=120)

        self.entry_phone = util.get_entry_text(self.register_new_user_window)
        self.entry_phone.place(x=950, y=125)

        self.text_label_bank_name = util.get_text_label(self.register_new_user_window, 'bank name:')
        self.text_label_bank_name.place(x=750, y=160)

        self.entry_bank_name = util.get_entry_text(self.register_new_user_window)
        self.entry_bank_name.place(x=950, y=165)

        self.text_label_account = util.get_text_label(self.register_new_user_window, 'account:')
        self.text_label_account.place(x=750, y=200)

        self.entry_account = util.get_entry_text(self.register_new_user_window)
        self.entry_account.place(x=950, y=205)

        self.text_label_password = util.get_text_label(self.register_new_user_window, 'password:')
        self.text_label_password.place(x=750, y=240)

        self.entry_password = util.get_entry_text(self.register_new_user_window)
        self.entry_password.place(x=950, y=245)

        self.entry_text_register_new_user.bind(
        "<Return>", lambda event: self.entry_email.focus()
        )

        self.entry_email.bind(
        "<Return>", lambda event: self.entry_phone.focus()
        )

        self.entry_phone.bind(
        "<Return>", lambda event: self.entry_bank_name.focus()
        )

        self.entry_bank_name.bind(
        "<Return>", lambda event: self.entry_account.focus()
        )

        self.entry_account.bind(
        "<Return>", lambda event: self.entry_password.focus()
        )

        self.entry_password.bind(
        "<Return>", lambda event: self.accept_register_new_user()
        )

        self.entry_text_register_new_user.focus()


        

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        email = self.entry_email.get(1.0, "end-1c")
        phone = self.entry_phone.get(1.0, "end-1c")
        bank = self.entry_bank_name.get(1.0, "end-1c")
        account = self.entry_account.get(1.0, "end-1c")
        password = self.entry_password.get(1.0, "end-1c")

        if not name or not email or not phone or not bank or not account or not password:
            util.msg_box("Required Fields", "All fields are mandatory.")
            return

        embeddings = face_recognition.face_encodings(self.register_new_user_capture)[0]

        file = open(os.path.join(self.db_dir, '{}.pickle'.format(name)), 'wb')
        pickle.dump(embeddings, file)

        with open(self.file_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            # Write the data as a dictionary to the csv
            data = {"Name": name, "Email": email, "Phone": phone, "Bank": bank, "Account": account, "Password": password, "Balance":10000}
            writer.writerow(data)

        util.msg_box('Success!', 'User was registered successfully !')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
