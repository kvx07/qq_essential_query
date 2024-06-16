import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
import requests
import sys
import os

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
        self.root.title("QQ Query App")
        self.root.geometry("400x300")
        self.root.iconbitmap(resource_path("icon.ico"))

        # Load and adjust background image transparency
        self.bg_image = Image.open(resource_path("background.png"))
        self.bg_image = self.bg_image.resize((400, 300), Image.Resampling.LANCZOS)
        self.bg_image = ImageEnhance.Brightness(self.bg_image).enhance(0.85)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.canvas.create_text(200, 50, text="请输入QQ号:", font=("宋体", 14), fill="white")

        self.qq_entry = tk.Entry(root, font=("宋体", 14))
        self.canvas.create_window(200, 100, window=self.qq_entry)

        self.query_button = tk.Button(root, text="查询", font=("宋体", 14), command=self.query_qq)
        self.canvas.create_window(200, 150, window=self.query_button)

        disclaimer = "本软件由@傻福二刺猿 开发，查询结果来自公用接口！"
        self.canvas.create_text(200, 280, text=disclaimer, font=("宋体", 10), fill="white")

    def query_qq(self):
        qq_number = self.qq_entry.get()
        if not qq_number.isdigit():
            messagebox.showerror("错误", "请输入有效的QQ号")
            return

        url = f"https://zy.xywlapi.cc/qqapi?qq={qq_number}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            message = data.get("message", "没有找到相关信息")
            qq = data.get('qq')
            phone = data.get('phone')
            phonediqu = data.get('phonediqu')

            if message == "没有找到相关信息" or (not qq and not phone and not phonediqu):
                messagebox.showerror("查询结果", "查询失败")
            else:
                result = f"查询成功\nQQ: {qq}\n手机: {phone}\n归属地: {phonediqu}"
                messagebox.showinfo("查询结果", result)
        else:
            messagebox.showerror("错误", "查询失败，请稍后再试")

if __name__ == "__main__":
    root = tk.Tk()
    app = QQQueryApp(root)
    root.mainloop()