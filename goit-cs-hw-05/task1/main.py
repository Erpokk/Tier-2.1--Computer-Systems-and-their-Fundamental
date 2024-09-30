import argparse
import asyncio
import os
import aiofiles
from aiofiles.os import makedirs
import logging

# Налаштовуємо логування помилок
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# Функція для обробки аргументів командного рядка
def parse_args():
    parser = argparse.ArgumentParser(description="Async File Copy Script")
    parser.add_argument("source_folder", type=str, help="Path to the source folder")
    parser.add_argument("target_folder", type=str, help="Path to the target folder")
    return parser.parse_args()


# Асинхронна функція для рекурсивного читання файлів у вихідній папці
async def read_folder(source_folder, target_folder):
    for root, _, files in os.walk(source_folder):
        for file in files:
            src_file_path = os.path.join(root, file)
            await copy_file(src_file_path, target_folder)


# Асинхронна функція для копіювання файлів у відповідну підпапку за розширенням
async def copy_file(src_file_path, target_folder):
    file_ext = src_file_path.split(".")[-1]  # Отримуємо розширення файлу
    dest_dir = os.path.join(target_folder, file_ext)

    try:
        await makedirs(dest_dir, exist_ok=True)  # Створюємо папку, якщо її ще немає
        dest_file_path = os.path.join(dest_dir, os.path.basename(src_file_path))

        async with aiofiles.open(src_file_path, "rb") as src_file:
            async with aiofiles.open(dest_file_path, "wb") as dest_file:
                content = await src_file.read()
                await dest_file.write(content)

        print(f"Copied {src_file_path} to {dest_file_path}")

    except Exception as e:
        logger.error(f"Failed to copy {src_file_path} to {dest_file_path}: {e}")


# Головна функція
async def main():
    args = parse_args()
    source_folder = args.source_folder
    target_folder = args.target_folder

    await read_folder(source_folder, target_folder)


# Запускаємо головну функцію
if __name__ == "__main__":
    asyncio.run(main())
