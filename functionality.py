import requests
from datetime import datetime
import os
import sys

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

def query_qq(qq_numbers):
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

    return success_count, fail_count, results

def query_phone(phone_numbers):
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

    return success_count, fail_count, results

def save_results(title, results):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, f"{title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_file, "w", encoding="utf-8") as file:
        for result in results:
            file.write(result + "\n")
    return log_file
