import os
import subprocess
import shutil
import json


def convert_webp_to_gif(input_folder):
    """
    將指定資料夾內的所有 WebP 檔案轉換為 GIF。

    Args:
        input_folder (str): WebP 檔案所在資料夾路徑。
        output_folder (str): 轉換後 GIF 檔案的輸出資料夾路徑。
    """
    output_folder = os.path.join(os.path.dirname(input_folder), "gif")
    palette_path = os.path.join(output_folder, "palette")

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(palette_path, exist_ok=True)

    for file_name in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, file_name)
        if (file_name.lower().endswith('.webp')):
            try:
                palette_file_name = os.path.splitext(file_name)[0] + '.png'
                palette_file_path = os.path.join(
                    palette_path, palette_file_name)

                subprocess.run([
                    "ffmpeg", "-i", input_file_path,
                    "-vf", "fps=24,scale=400:-1:flags=lanczos,palettegen",
                    palette_file_path
                ], check=True)
                print(f"成功生成調色板:{input_file_path} -> {palette_file_path}")

                output_file_name = os.path.splitext(file_name)[0] + '.gif'
                output_file_path = os.path.join(
                    output_folder, output_file_name)

                subprocess.run([
                    "ffmpeg", "-i", input_file_path, "-i", palette_file_path,
                    "-lavfi", "fps=24,scale=400:-1:flags=lanczos [x]; [x][1:v] paletteuse",
                    output_file_path
                ], check=True)

            except Exception as e:
                print(f"轉換失敗:{file_name} -> {e}")
    shutil.rmtree(palette_path)


if __name__ == "__main__":
    config = "config.json"

    with open(config, "r", encoding="utf-8") as f:
        config = json.load(f)

    input_folder = config.get("input_folder")

    convert_webp_to_gif(input_folder)
