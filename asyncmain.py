import os
import subprocess
import shutil
import json
import asyncio


async def run_command(cmd):
    """執行 shell 指令的非同步版本。"""
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise Exception(stderr.decode().strip())
    return stdout.decode().strip()


async def convert_webp_to_gif(input_folder):
    """
    將指定資料夾內的所有 WebP 檔案非同步轉換為 GIF。

    Args:
        input_folder (str): WebP 檔案所在資料夾路徑。
    """
    output_folder = os.path.join(os.path.dirname(input_folder), "gif")
    palette_path = os.path.join(output_folder, "palette")

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(palette_path, exist_ok=True)

    async def process_file(file_name):
        input_file_path = os.path.join(input_folder, file_name)
        if file_name.lower().endswith('.webp'):
            try:
                palette_file_name = os.path.splitext(file_name)[0] + '.png'
                palette_file_path = os.path.join(
                    palette_path, palette_file_name)

                # 生成調色板
                await run_command([
                    "ffmpeg", "-i", input_file_path,
                    "-vf", "fps=24,scale=400:-1:flags=lanczos,palettegen",
                    palette_file_path
                ])
                print(f"成功生成調色板: {input_file_path} -> {palette_file_path}")

                # 生成 GIF
                output_file_name = os.path.splitext(file_name)[0] + '.gif'
                output_file_path = os.path.join(
                    output_folder, output_file_name)

                await run_command([
                    "ffmpeg", "-i", input_file_path, "-i", palette_file_path,
                    "-lavfi", "fps=24,scale=400:-1:flags=lanczos [x]; [x][1:v] paletteuse",
                    output_file_path
                ])
                print(f"成功轉換: {file_name} -> {output_file_name}")

            except Exception as e:
                print(f"轉換失敗: {file_name} -> {e}")

    # 收集所有 WebP 檔案進行非同步處理
    tasks = [process_file(file_name) for file_name in os.listdir(input_folder)]
    await asyncio.gather(*tasks)

    shutil.rmtree(palette_path)
    print(f"清理完成: {palette_path}")


if __name__ == "__main__":
    config_path = "./config.json"

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    input_folder = config.get("input_folder")

    print(f"輸入資料夾: {input_folder}")
    try:
        asyncio.run(convert_webp_to_gif(input_folder))
    except:
        print('在 config.json 內的 "input_folder" 需要正確的路徑')
