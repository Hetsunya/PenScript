import os
import cv2
import shutil
import numpy as np

# Определяем пути
raw_root = "../data/raw"
processed_root = "../data/processed"
letters_src = os.path.join(raw_root, "letters")
digits_src = os.path.join(raw_root, "digits")
letters_dest = os.path.join(processed_root, "letters")
digits_dest = os.path.join(processed_root, "digits")

# Создаём папки, если их нет
os.makedirs(letters_dest, exist_ok=True)
os.makedirs(digits_dest, exist_ok=True)

def preprocess_and_save(src_folder, dest_folder, size=(32, 32)):
    for file_name in os.listdir(src_folder):
        src_path = os.path.join(src_folder, file_name)
        dest_path = os.path.join(dest_folder, file_name)
        
        # Загружаем изображение
        image = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)  # Читаем в градациях серого
        if image is None:
            print(f"Ошибка загрузки {src_path}")
            continue
        
        # Приводим к нужному размеру
        image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        
        # Сохраняем обработанное изображение
        cv2.imwrite(dest_path, image)

# Обрабатываем буквы и цифры
preprocess_and_save(letters_src, letters_dest)
preprocess_and_save(digits_src, digits_dest)

print("Предобработка завершена, файлы сохранены в data/processed/")
