import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageEnhance
import requests
import sys
import os
from datetime import datetime

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
        self.root.iconbitmap(resource_path("images/icon.ico"))

        # Load and adjust background image transparency
        self.bg_image = Image.open(resource_path("images/background.png"))
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

        self.import_button = tk.Button(root, text="从文件导入", font=("宋体", 14), command=self.import_from_file)
        self.import_button_window = self.canvas.create_window(300, 280, window=self.import_button)

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
            self.canvas.coords(self.import_button_window, event.width // 2, 280)
            self.canvas.coords(self.disclaimer_id, event.width // 2, event.height - 20)

    def query_qq(self):
        qq_numbers = self.entry.get()
        if self.batch_query_var.get():
            qq_numbers = qq_numbers.split(',')
        else:
            qq_numbers = [qq_numbers]

        success_count = 0
        fail_count = 0
        results = []

        for qq_number in qq_numbers:
            qq_number = qq_number.strip()
            if not qq_number.isdigit():
                results.append(f"{qq_number} 不是有效的QQ号")
                fail_count += 1
                continue

            url = f"https://zy.xywlapi.cc/qqapi?qq={qq_number}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                message = data.get("message", "没有找到相关信息")
                qq = data.get('qq')
                phone = data.get('phone')
                phonediqu = data.get('phonediqu')

                if message == "没有找到相关信息":
                    results.append(f"{qq_number}: 没有找到相关信息")
                    fail_count += 1
                elif not qq and not phone and not phonediqu:
                    results.append(f"{qq_number}: 查询结果为空")
                    fail_count += 1
                else:
                    results.append(f"{qq_number} 查询结果:\nQQ: {qq}\n手机: {phone}\n归属地: {phonediqu}")
                    success_count += 1
            except requests.RequestException as e:
                results.append(f"{qq_number} 查询失败: {e}")
                fail_count += 1

        self.show_results(success_count, fail_count, results, "QQ查询结果")

    def query_phone(self):
        phone_numbers = self.entry.get()
        if self.batch_query_var.get():
            phone_numbers = phone_numbers.split(',')
        else:
            phone_numbers = [phone_numbers]

        success_count = 0
        fail_count = 0
        results = []

        for phone_number in phone_numbers:
            phone_number = phone_number.strip()
            if not phone_number.isdigit():
                results.append(f"{phone_number} 不是有效的手机号")
                fail_count += 1
                continue

            url = f"https://zy.xywlapi.cc/qqphone?phone={phone_number}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                message = data.get("message", "没有找到相关信息")
                qq = data.get('qq')

                if message == "没有找到相关信息":
                    results.append(f"{phone_number}: 没有找到相关信息")
                    fail_count += 1
                elif not qq:
                    results.append(f"{phone_number}: 查询结果为空")
                    fail_count += 1
                else:
                    results.append(f"{phone_number} 查询结果:\n手机: {phone_number}\nQQ: {qq}")
                    success_count += 1
            except requests.RequestException as e:
                results.append(f"{phone_number} 查询失败: {e}")
                fail_count += 1

        self.show_results(success_count, fail_count, results, "手机号查询结果")

    def import_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                data = file.read()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, data)
            self.batch_query_var.set(True)

    def show_results(self, success_count, fail_count, results, title):
        result_summary = f"查询完成！\n成功: {success_count} 条\n失败: {fail_count} 条"
        if success_count + fail_count > 10:
            messagebox.showinfo(title, f"{result_summary}\n结果过长，已生成日志文件并打开。")

            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            log_file = os.path.join(log_dir, f"{title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(log_file, "w", encoding="utf-8") as file:
                for result in results:
                    file.write(result + "\n")
            os.startfile(log_file)
        else:
            detailed_results = "\n\n".join(results)
            messagebox.showinfo(title, f"{result_summary}\n\n{detailed_results}\n\n详细结果已保存到日志文件。")

            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            log_file = os.path.join(log_dir, f"{title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(log_file, "w", encoding="utf-8") as file:
                for result in results:
                    file.write(result + "\n")
            messagebox.showinfo(title, f"详细结果已保存到 {log_file}")


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
    unlock_window.iconbitmap(resource_path("images/icon.ico"))

    # 设置背景图片
    unlock_bg_image = Image.open(resource_path("images/unlockbg.png"))
    unlock_bg_image = ImageEnhance.Brightness(unlock_bg_image).enhance(0.85)
    unlock_bg_photo = ImageTk.PhotoImage(unlock_bg_image)

    bg_canvas = tk.Canvas(unlock_window, width=300, height=150)
    bg_canvas.pack(fill="both", expand=True)
    bg_canvas.create_image(0, 0, image=unlock_bg_photo, anchor="nw")

    # 设置透明背景色
    bg_canvas.create_text(150, 30, text="请输入密码解锁:", font=("宋体", 12), fill="white", tags="text")
    password_entry = tk.Entry(unlock_window, show="*", font=("宋体", 12), bg='#d9d9d9')
    bg_canvas.create_window(150, 70, window=password_entry, tags="entry")

    check_button = tk.Button(unlock_window, text="确定", font=("宋体", 12), command=check_password, bg='#d9d9d9')
    bg_canvas.create_window(150, 110, window=check_button, tags="button")

    password_entry.bind("<Return>", lambda event: check_password())

    # 确保窗口居中
    center_window(unlock_window)


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    root = tk.Tk()
    app = QQQueryApp(root)
    unlock_app()
    root.mainloop()
