import os
from PIL import Image
import json

# 讀取設定檔
config_path = "./config.json"
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

print(config.get("input_folder")+"\n")
folder_path = config.get("input_folder")

# 檢查資料夾中是否有 .webp 檔案
for file_name in os.listdir(folder_path):
    if not file_name.lower().endswith('.webp'):
        continue

    file_path = os.path.join(folder_path, file_name)
    try:
        # 嘗試開啟圖片
        img = Image.open(file_path)
        if img.format == 'WEBP':
            print(f"{file_name} is available WEBP")
            is_animated = getattr(img, "is_animated", False)
            status = "animated" if is_animated else "static"
            print(f" - {file_name} is {status} WEBP")
        else:
            print(f"{file_name} format error, is {img.format}")
    except Exception as e:
        print(f"Cannot open {file_name}, error: {e}")
