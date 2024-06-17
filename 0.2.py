import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import requests
import sys
import os

# 密码变量
password = "kotori02"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class QQQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("琴里QQ查询器")
        self.root.geometry("600x400")
        self.root.iconbitmap(resource_path("icon.ico"))

        # Load and adjust background image transparency
        self.bg_image = Image.open(resource_path("background.png"))
        self.bg_image = ImageEnhance.Brightness(self.bg_image).enhance(0.85)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)

        self.bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.root.bind("<Configure>", self.resize_bg)

        # Add titles
        self.title_id = self.canvas.create_text(300, 50, text="琴里QQ查询器", font=("宋体", 20, "bold"), fill="white")
        self.subtitle_id = self.canvas.create_text(300, 80, text="版本 0.2", font=("宋体", 14), fill="white")

        self.text_id = self.canvas.create_text(300, 120, text="请输入QQ号或手机号:", font=("宋体", 14), fill="white")

        self.entry = tk.Entry(root, font=("宋体", 14), width=50)
        self.entry_window = self.canvas.create_window(300, 150, window=self.entry)

        self.qq_button = tk.Button(root, text="根据QQ号查询", font=("宋体", 14), command=self.query_qq)
        self.qq_button_window = self.canvas.create_window(200, 200, window=self.qq_button)

        self.phone_button = tk.Button(root, text="根据手机号查询", font=("宋体", 14), command=self.query_phone)
        self.phone_button_window = self.canvas.create_window(400, 200, window=self.phone_button)

        self.batch_query_var = tk.BooleanVar()
        self.batch_query_check = tk.Checkbutton(root, text="启用批量查询（用逗号分隔）", variable=self.batch_query_var,
                                                font=("宋体", 12), bg='#d9d9d9')
        self.batch_query_check_window = self.canvas.create_window(300, 240, window=self.batch_query_check)

        self.disclaimer_id = self.canvas.create_text(300, 380, text="本软件由@傻福二刺猿 开发，查询结果来自公用接口！",
                                                     font=("宋体", 10), fill="white")

    def resize_bg(self, event):
        if event.widget == self.root:
            new_width = event.width
            new_height = event.height

            aspect_ratio = self.bg_image.width / self.bg_image.height
            if new_width / new_height > aspect_ratio:
                new_height = int(new_width / aspect_ratio)
            else:
                new_width = int(new_height * aspect_ratio)

            resized_image = self.bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.bg_image_id, image=self.bg_photo)
            self.canvas.coords(self.bg_image_id, 0, 0)

            self.canvas.coords(self.title_id, event.width // 2, 50)
            self.canvas.coords(self.subtitle_id, event.width // 2, 80)
            self.canvas.coords(self.text_id, event.width // 2, 120)
            self.canvas.coords(self.entry_window, event.width // 2, 150)
            self.canvas.coords(self.qq_button_window, event.width // 2 - 100, 200)
            self.canvas.coords(self.phone_button_window, event.width // 2 + 100, 200)
            self.canvas.coords(self.batch_query_check_window, event.width // 2, 240)
            self.canvas.coords(self.disclaimer_id, event.width // 2, event.height - 20)

    def query_qq(self):
        qq_numbers = self.entry.get()
        if self.batch_query_var.get():
            qq_numbers = qq_numbers.split(',')
        else:
            qq_numbers = [qq_numbers]

        for qq_number in qq_numbers:
            qq_number = qq_number.strip()
            if not qq_number.isdigit():
                messagebox.showerror("错误", f"{qq_number} 不是有效的QQ号")
                continue

            url = f"https://zy.xywlapi.cc/qqapi?qq={qq_number}"
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.RequestException as e:
                messagebox.showerror("查询结果", f"{qq_number} 查询失败，请稍后再试: {e}")
                continue

            data = response.json()
            message = data.get("message", "没有找到相关信息")
            qq = data.get('qq')
            phone = data.get('phone')
            phonediqu = data.get('phonediqu')

            if message == "没有找到相关信息":
                messagebox.showinfo("查询结果", f"没有找到与QQ号 {qq_number} 相关的信息")
            elif not qq and not phone and not phonediqu:
                messagebox.showinfo("查询结果", f"查询结果为空")
            else:
                result = f"查询结果:\nQQ: {qq}\n手机: {phone}\n归属地: {phonediqu}"
                messagebox.showinfo("查询结果", result)

    def query_phone(self):
        phone_numbers = self.entry.get()
        if self.batch_query_var.get():
            phone_numbers = phone_numbers.split(',')
        else:
            phone_numbers = [phone_numbers]

        for phone_number in phone_numbers:
            phone_number = phone_number.strip()
            if not phone_number.isdigit():
                messagebox.showerror("错误", f"{phone_number} 不是有效的手机号")
                continue

            url = f"https://zy.xywlapi.cc/qqphone?phone={phone_number}"
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.RequestException as e:
                messagebox.showerror("查询结果", f"{phone_number} 查询失败，请稍后再试: {e}")
                continue

            data = response.json()
            message = data.get("message", "没有找到相关信息")
            qq = data.get('qq')

            if message == "没有找到相关信息":
                messagebox.showinfo("查询结果", f"没有找到与手机号 {phone_number} 相关的QQ号")
            elif not qq:
                messagebox.showinfo("查询结果", f"查询结果为空")
            else:
                result = f"查询结果:\n手机: {phone_number}\nQQ: {qq}"
                messagebox.showinfo("查询结果", result)


def unlock_app():
    def check_password():
        if password_entry.get() == password:
            unlock_window.destroy()
            root.deiconify()
        else:
            messagebox.showerror("错误", "密码错误，请寻求管理员帮助")

    root.withdraw()
    unlock_window = tk.Toplevel(root)
    unlock_window.title("解锁")
    unlock_window.geometry("300x150")
    unlock_window.resizable(False, False)
    unlock_window.iconbitmap(resource_path("icon.ico"))

    tk.Label(unlock_window, text="请输入密码解锁:", font=("宋体", 12)).pack(pady=20)
    password_entry = tk.Entry(unlock_window, show="*", font=("宋体", 12))
    password_entry.pack(pady=5)

    tk.Button(unlock_window, text="确定", font=("宋体", 12), command=check_password).pack(pady=10)
    password_entry.bind("<Return>", lambda event: check_password())


if __name__ == "__main__":
    root = tk.Tk()
    app = QQQueryApp(root)
    unlock_app()
    root.mainloop()
