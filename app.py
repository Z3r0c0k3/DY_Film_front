
import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import datetime
import random
import win32print


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="light sky blue")
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="MAKE; PHOTO!", font=("Arial", 48), bg="light sky blue")
        label.grid(row=0, column=0, pady=150, padx=300)

        start_button = tk.Button(self, text="Start!", font=("Arial", 24), command=lambda: controller.show_frame("CapturePage"), bg="white")
        start_button.grid(row=1, column=0, pady=50)

        version_info = tk.Label(self, text="Version 1.0 | Developed by. ZEROCOKE", font=("Arial", 20), bg="light sky blue", anchor="e")
        version_info.place(relx=1, rely=0, x=-10, y=10, anchor="ne")

        admin_button = tk.Button(self, text="Admin", font=("Arial", 18), command=self.admin_popup, bg="white")
        admin_button.place(relx=0, rely=0, x=10, y=10, anchor="nw")

    def admin_popup(self):
        password = simpledialog.askstring("Password", "Enter Admin Password:", show='*')
        if password == "admin123":  # 기본 비밀번호는 "admin123"
            AdminSettings()
        else:
            messagebox.showerror("Error", "Incorrect Password!")

class AdminSettings(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Admin Settings")

        available_cameras = self.get_available_cameras()
        self.camera_label = tk.Label(self, text="Select Camera Device:")
        self.camera_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.camera_var = tk.StringVar(self)
        self.camera_dropdown = tk.OptionMenu(self, self.camera_var, *available_cameras)
        self.camera_dropdown.grid(row=0, column=1, padx=10, pady=10)

        available_printers = self.get_available_printers()
        self.printer_label = tk.Label(self, text="Select Printer Device:")
        self.printer_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.printer_var = tk.StringVar(self)
        self.printer_dropdown = tk.OptionMenu(self, self.printer_var, *available_printers)
        self.printer_dropdown.grid(row=1, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self, text="Change Admin Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        self.server_label = tk.Label(self, text="Server Address:")
        self.server_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.server_entry = tk.Entry(self)
        self.server_entry.grid(row=3, column=1, padx=10, pady=10)

        self.save_button = tk.Button(self, text="Save", command=self.save_settings)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=20)

    def get_available_cameras(self):
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append(f"Camera {index}")
            cap.release()
            index += 1
        return arr

    def get_available_printers(self):
        return [printer[2] for printer in win32print.EnumPrinters(2)]

    def save_settings(self):
        messagebox.showinfo("Info", "Settings saved successfully!")

class CapturePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="light pink")
        self.controller = controller
        self.capture_count = 0
        self.messages = ["한번더! 포즈를 바꿔보세요!", "좋아요! 너무 아름답네요 :)", "잘했어요. 한번 더!"]
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.preview_label = tk.Label(self, bg="black")
        self.preview_label.grid(row=0, column=0, pady=50, padx=150, sticky="nsew")

        self.info_label = tk.Label(self, text="사진은 총 3번 찍어요. 찰칵을 눌러주세요!", font=("Arial", 24), bg="light pink", fg="black")
        self.info_label.grid(row=1, column=0, pady=(0, 15))

        self.capture_button = tk.Button(self, text="찰칵!", font=("Arial", 24), command=self.start_countdown, bg="white")
        self.capture_button.grid(row=2, column=0, pady=12)

        back_button = tk.Button(self, text="처음으로 돌아가기!", font=("Arial", 18), command=lambda: controller.show_frame("StartPage"), bg="white")
        back_button.grid(row=3, column=0, pady=30)

        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.preview_label.config(image=self.photo)
        self.after(10, self.update_camera)

    def start_countdown(self):
        self.capture_button.config(state=tk.DISABLED)
        self.countdown(3)

    def countdown(self, count):
        if count > 0:
            self.info_label.config(text=str(count))
            self.after(1000, self.countdown, count-1)
        else:
            self.capture()
            self.info_label.config(text=random.choice(self.messages))
            if self.capture_count < 3:
                self.after(3000, self.start_countdown)
            else:
                self.capture_button.config(state=tk.NORMAL)
                self.controller.show_frame("StartPage")

    def capture(self):
        ret, frame = self.cap.read()
        if ret:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f'DYHS_PHOTOBOX_{timestamp}.jpg'
            cv2.imwrite(filename, frame)
            self.capture_count += 1


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Photo Booth")
        self.geometry("1280x720")
        self.frames = {}

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        for page in [StartPage, CapturePage]:
            frame = page(self, self)
            self.frames[page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


app = MainApp()
app.mainloop()
