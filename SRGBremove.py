from PIL import Image

# 重新保存背景图片
bg_image_path = "images/background.png"
bg_image = Image.open(bg_image_path)
bg_image.save(bg_image_path)

# 重新保存解锁背景图片（如果有的话）
unlock_bg_image_path = "images/unlockbg.png"
unlock_bg_image = Image.open(unlock_bg_image_path)
unlock_bg_image.save(unlock_bg_image_path)

# 重新保存图标图片
icon_image_path = "images/icon.ico"
icon_image = Image.open(icon_image_path)
icon_image.save(icon_image_path)
