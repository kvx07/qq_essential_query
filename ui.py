import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageEnhance
import os
from functionality import query_qq, query_phone, save_results, resource_path, password

class QQQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("琴里QQ查询器")
        self.root.geometry("600x400")
        self.root.iconbitmap(resource_path("images/icon.ico"))

        # Center the window
        self.center_window(self.root)

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
        self.subtitle_id = self.canvas.create_text(300, 80, text="版本 0.3", font=("宋体", 14), fill="white")

        self.text_id = self.canvas.create_text(300, 120, text="请输入QQ号或手机号:", font=("宋体", 14), fill="white")

        self.entry = tk.Entry(root, font=("宋体", 14), width=50)
        self.entry_window = self.canvas.create_window(300, 150, window=self.entry)

        self.qq_button = tk.Button(root, text="根据QQ号查询", font=("宋体", 14), command=self.query_qq)
        self.qq_button_window = self.canvas.create_window(200, 200, window=self.qq_button)

        self.phone_button = tk.Button(root, text="根据手机号查询", font=("宋体", 14), command=self.query_phone)
        self.phone_button_window = self.canvas.create_window(400, 200, window=self.phone_button)

        self.batch_query_var = tk.BooleanVar()
        self.batch_query_check = tk.Checkbutton(root, text="启用批量查询（用逗号分隔）", variable=self.batch_query_var, font=("宋体", 12), bg='#d9d9d9')
        self.batch_query_check_window = self.canvas.create_window(300, 240, window=self.batch_query_check)

        self.import_button = tk.Button(root, text="从文件导入", font=("宋体", 14), command=self.import_from_file)
        self.import_button_window = self.canvas.create_window(300, 280, window=self.import_button)

        self.disclaimer_id = self.canvas.create_text(300, 380, text="本软件由@傻福二刺猿 开发，查询结果来自公用接口！", font=("宋体", 10), fill="white")

    def resize_bg(self, event):
        if event.widget == self.root:
            new_width, new_height = event.width, event.height
            aspect_ratio = self.bg_image.width / self.bg_image.height
            new_width, new_height = (new_width, int(new_width / aspect_ratio)) if new_width / new_height > aspect_ratio else (int(new_height * aspect_ratio), new_height)
            resized_image = self.bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.bg_image_id, image=self.bg_photo)
            self.canvas.coords(self.bg_image_id, 0, 0)
            self.update_widget_positions(event.width, event.height)

    def update_widget_positions(self, width, height):
        self.canvas.coords(self.title_id, width // 2, 50)
        self.canvas.coords(self.subtitle_id, width // 2, 80)
        self.canvas.coords(self.text_id, width // 2, 120)
        self.canvas.coords(self.entry_window, width // 2, 150)
        self.canvas.coords(self.qq_button_window, width // 2 - 100, 200)
        self.canvas.coords(self.phone_button_window, width // 2 + 100, 200)
        self.canvas.coords(self.batch_query_check_window, width // 2, 240)
        self.canvas.coords(self.import_button_window, width // 2, 280)
        self.canvas.coords(self.disclaimer_id, width // 2, height - 20)

    def query_qq(self):
        qq_numbers = self.entry.get().split(',') if self.batch_query_var.get() else [self.entry.get()]
        success_count, fail_count, results = query_qq([qq.strip() for qq in qq_numbers if qq.strip().isdigit()])
        self.show_results(success_count, fail_count, results, "QQ查询结果")

    def query_phone(self):
        phone_numbers = self.entry.get().split(',') if self.batch_query_var.get() else [self.entry.get()]
        success_count, fail_count, results = query_phone([phone.strip() for phone in phone_numbers if phone.strip().isdigit()])
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
            log_file = save_results(title, results)
            os.startfile(log_file)
        else:
            detailed_results = "\n\n".join(results)
            messagebox.showinfo(title, f"{result_summary}\n\n{detailed_results}\n\n详细结果已保存到日志文件。")
            log_file = save_results(title, results)
            messagebox.showinfo(title, f"详细结果已保存到 {log_file}")

    def center_window(self, window):
        window.update_idletasks()
        width, height = window.winfo_width(), window.winfo_height()
        x, y = (window.winfo_screenwidth() // 2) - (width // 2), (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

def unlock_app(root):
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

    tk.Label(unlock_window, text="请输入密码解锁:", font=("宋体", 12)).pack(pady=10)
    tk.Label(unlock_window, text="版本 0.3", font=("宋体", 10)).pack(pady=5)
    password_entry = tk.Entry(unlock_window, show="*", font=("宋体", 12))
    password_entry.pack(pady=5)

    tk.Button(unlock_window, text="确定", font=("宋体", 12), command=check_password).pack(pady=10)
    password_entry.bind("<Return>", lambda event: check_password())

    # 确保窗口居中
    center_window(unlock_window)

def center_window(window):
    window.update_idletasks()
    width, height = window.winfo_width(), window.winfo_height()
    x, y = (window.winfo_screenwidth() // 2) - (width // 2), (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def start_app():
    root = tk.Tk()
    app = QQQueryApp(root)
    unlock_app(root)
    root.mainloop()
