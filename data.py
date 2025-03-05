import os
import shutil

# Определяем пути
source_root = "datasets"
destination_root = "data/raw"
letters_dest = os.path.join(destination_root, "letters")
digits_dest = os.path.join(destination_root, "digits")

# Создаём папки, если их нет
os.makedirs(letters_dest, exist_ok=True)
os.makedirs(digits_dest, exist_ok=True)

# Переносим файлы из all_letters_image
letters_src = os.path.join(source_root, "all_letters_image")
for root, _, files in os.walk(letters_src):
    for file in files:
        src_path = os.path.join(root, file)
        dst_path = os.path.join(letters_dest, file)
        shutil.move(src_path, dst_path)

# Переносим файлы из mnist/train и mnist/test
mnist_src_train = os.path.join(source_root, "mnist", "train")
mnist_src_test = os.path.join(source_root, "mnist", "test")

for mnist_src in [mnist_src_train, mnist_src_test]:
    for root, _, files in os.walk(mnist_src):
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(digits_dest, file)
            shutil.move(src_path, dst_path)

print("Файлы успешно перемещены в data/raw/")
