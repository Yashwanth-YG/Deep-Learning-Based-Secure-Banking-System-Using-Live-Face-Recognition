import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import pandas as pd
import os.path
import datetime
import pickle
import csv
import cv2
import face_recognition

import util
from Anti_Spoof.test import test

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Window")

        self.data = pd.read_csv("records.csv")

        
        self.title_label = tk.Label(self.master, text="Bank Transaction System Using Face Recognization",font=("Arial", 25, "bold"), fg="red")
        self.title_label.place(x=200,y=20)

        self.email_label = tk.Label(self.master, text="Email", font=("Arial", 14))
        self.email_label.place(x=100,y=100)

        self.email_entry = tk.Entry(self.master, font=("Arial", 14))
        self.email_entry.place(x=200,y=100)

        self.password_label = tk.Label(self.master, text="Password", font=("Arial", 14))
        self.password_label.place(x=100,y=150)

        self.password_entry = tk.Entry(self.master, font=("Arial", 14))
        self.password_entry.place(x=200,y=150)

        self.next_button = tk.Button(self.master, text="Submit", command=self.open_info_window,borderwidth=2)
        self.next_button.place(x=650,y=350)

    def open_info_window(self):

        email_check = self.data[self.data["Email"] == self.email_entry.get()]
        password_check = self.data[self.data['Password'] == self.password_entry.get()]
        if email_check.empty or password_check.empty:
            print(f"Invalid credentials")
            messagebox.showerror("Error", "Invalid credentials")

        else:
            # print(row)
            name = email_check["Name"].values[0]
            print("welcome",name)
            messagebox.showinfo("Success", "Credentials matched, welcome " + name)
        
            self.master.withdraw()
            face_window = tk.Toplevel(self.master)
            Face_Recognition_Spoof(face_window)
            
            # self.master.withdraw()
            # info_window = tk.Toplevel(self.master)
            # InfoWindow(info_window,name,email,phone,bank,account,balance)

class Face_Recognition_Spoof:
    def __init__(self,master):
        self.main_window = master
        # self.main_window = tk.Tk()
        master.geometry("1200x520+350+100")
        self.main_window.title("Face_Recognition_Spoof")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'
        self.data = pd.read_csv("records.csv")


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

        self.loop = self._label.after(20, self.process_webcam)

    def login(self):

        label = test(
                image=self.most_recent_capture_arr,
                model_dir='D:\\Project\\Anti_Spoof\\resources\\anti_spoof_models',
                device_id=0
                )

        if label == 1:

            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Error...', 'Unknown user. Please register new user or try again.')
            else:
                util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
                with open(self.log_path, 'a') as f:
                    f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                    f.close()
                info = self.data[self.data["Name"] == name]
                if info.empty:
                    print(f"Error")
                    messagebox.showerror("Error", "Data not found")

                else:
                    # print(row)
                    email = info["Email"].values[0]
                    phone = info["Phone"].values[0]
                    bank = info["Bank"].values[0]
                    account = info["Account"].values[0]
                    balance = info["Balance"].values[0]

                    self.main_window.after_cancel(self.loop)
                    self.cap.release()
                    self.main_window.withdraw()
                    info_window = tk.Toplevel(self.main_window)
                    InfoWindow(info_window,name,email,phone,bank,account,balance)

                

        else:
            util.msg_box('Hey, you are a spoofer!', 'You are fake !')

class InfoWindow:
    def __init__(self, master,name,email,phone,bank,account,balance):
        self.master = master
        self.name = name
        self.email = email
        self.phone = phone
        self.bank = bank
        self.account = account
        self.balance = balance

        master.geometry("1300x700")
        self.master.title("Information Window")
        
        # Display information here

        self.info_label = tk.Label(self.master, text="Some Information", font=("Arial", 14))
        self.info_label.place(x=100,y=20)

        self.name_label = tk.Label(self.master, text="Name: " + self.name, font=("Arial", 12))
        self.name_label.place(x=100,y=50)

        self.email_label = tk.Label(self.master, text="Email: " + self.email, font=("Arial", 12))
        self.email_label.place(x=100,y=80)

        self.phone_label = tk.Label(self.master, text="Phone: " + str(self.phone), font=("Arial", 12))
        self.phone_label.place(x=100,y=110)

        self.bank_label = tk.Label(self.master, text="Bank: " + self.bank, font=("Arial", 12))
        self.bank_label.place(x=100,y=140)

        self.account_label = tk.Label(self.master, text="Account: " + str(self.account), font=("Arial", 12))
        self.account_label.place(x=100,y=170)

        self.balance_label = tk.Label(self.master, text="Balance: " + str(self.balance), font=("Arial", 12))
        self.balance_label.place(x=100,y=200)
        

        self.withdraw_label = tk.Label(self.master, text="Withdraw: ", font=("Arial", 12))
        self.withdraw_label.place(x=100,y=450)

        self.withdraw_entry = tk.Entry(self.master)
        self.withdraw_entry.place(x=200,y=450)
        
        self.next_button = tk.Button(self.master, text="Withdraw", command=self.withdraw,borderwidth=2)
        self.next_button.place(x=600,y=450)

        self.back_button = tk.Button(self.master, text="Back", command=self.go_back,borderwidth=2)
        self.back_button.place(x=600,y=550)

    def withdraw(self):
        self.withdraw_val = self.withdraw_entry.get()
        if(self.withdraw_val == ''):
            messagebox.showerror("Error", "Please enter a valid amount")
        elif (float(self.withdraw_val) > float(self.balance)):
            messagebox.showerror("Error", "Insufficient balance")
        else:
            messagebox.showinfo("Success", "Withdrawal successful")
            self.balance = float(self.balance) - float(self.withdraw_val)
            self.balance = str(self.balance)
            self.update_balance()

    def update_balance(self):
        filename = 'records.csv'
        self.balance_label['text'] = "Balance: " + self.balance
        updated_data = []
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Email'] == self.email:
                    row['Balance'] = self.balance
                updated_data.append(row)

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_data)

    def go_back(self):
        self.master.withdraw()
        root.deiconify()

class PaymentWindow:
    def __init__(self, master):
        self.master = master
        master.geometry("1300x900")
        self.master.title("Payment Window")

        self.camera = cv2.VideoCapture(0)
        self.canvas = tk.Canvas(self.master, width=self.camera.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.name_label = tk.Label(self.master, text="Name:")
        self.name_label.place(x=250,y=50)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.place(x=350,y=50)

        self.email_label = tk.Label(self.master, text="Email:")
        self.email_label.place(x=250,y=75)
        self.email_entry = tk.Entry(self.master)
        self.email_entry.place(x=350,y=75)

        self.phone_label = tk.Label(self.master, text="Phone:")
        self.phone_label.place(x=250,y=100)
        self.phone_entry = tk.Entry(self.master)
        self.phone_entry.place(x=350,y=100)

        self.bank_label = tk.Label(self.master, text="Bank Name:")
        self.bank_label.place(x=250,y=120)
        self.bank_entry = tk.Entry(self.master)
        self.bank_entry.place(x=350,y=125)

        self.account_label = tk.Label(self.master, text="Account Number:")
        self.account_label.place(x=250,y=150)
        self.account_entry = tk.Entry(self.master)
        self.account_entry.place(x=350,y=150)

        self.pay_button = tk.Button(self.master, text="Pay", command=self.capture_image)
        self.pay_button.place(x=350,y=400)

        self.back_button = tk.Button(self.master, text="Back", command=self.go_back)
        self.back_button.place(x=350,y=450)

    def capture_image(self):
        ret, frame = self.camera.read()
        if ret:
            cv2.imwrite("captured_photo.jpg", frame)
            messagebox.showinfo("Capture", "Photo captured successfully!")
        else:
            messagebox.showerror("Error", "Failed to capture photo!")

    def go_back(self):
        self.master.withdraw()
        root.deiconify()

def main():
    global root
    root = tk.Tk()
    root.geometry("1300x900")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
