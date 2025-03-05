import os
from PIL import Image
import numpy as np

# Путь к папкам с датасетами
mnist_train_dir = 'datasets/MNIST_dataset/mnist/train'
mnist_test_dir = 'datasets/MNIST_dataset/mnist/test'
letters_dir = 'datasets/all_letters_image/all_letters_image'

# Папка для сохранения нового объединенного датасета
output_dir = 'datasets/combined_dataset'

# Создаем необходимые папки
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    os.makedirs(os.path.join(output_dir, 'images'))
    os.makedirs(os.path.join(output_dir, 'labels'))

# Функция для обработки MNIST
def process_mnist(source_dir, target_dir, dataset_type):
    print(f"Начинаем обработку MNIST из папки {source_dir}...")

    for file in os.listdir(source_dir):
        if file.endswith('.png'):
            try:
                # Извлекаем метку из имени файла
                label = file.split('_')[0]  # Берем первую часть до _

                # Создаем нужную структуру
                image = Image.open(os.path.join(source_dir, file))
                image = image.convert('L')  # Преобразуем в черно-белое изображение

                # Переименовываем файл
                new_file_name = f'{dataset_type}_digit_{label}_{file}'

                # Сохраняем изображение в новую папку
                image.save(os.path.join(target_dir, 'images', new_file_name))

                # Записываем метку в файл
                with open(os.path.join(target_dir, 'labels', 'labels.txt'), 'a') as label_file:
                    label_file.write(f'{new_file_name} {label}\n')

            except Exception as e:
                print(f"Ошибка при обработке файла {file}: {e}")

# Функция для обработки кириллических букв
def process_letters(source_dir, target_dir):
    print(f"Начинаем обработку букв из папки {source_dir}...")

    for i, file in enumerate(os.listdir(source_dir)):
        if file.endswith('.png'):
            try:
                # Извлекаем букву из имени файла
                file_name = file.split('_')[0]  # Берем первую часть до _
                letter = chr(int(file_name))  # Преобразуем номер в символ

                # Создаем нужную структуру
                image = Image.open(os.path.join(source_dir, file))
                image = image.convert('L')  # Преобразуем в черно-белое изображение

                # Переименовываем файл
                new_file_name = f'letter_{letter}_{i}.png'

                # Сохраняем изображение в одну папку
                image.save(os.path.join(target_dir, 'images', new_file_name))

                # Записываем метку в файл
                with open(os.path.join(target_dir, 'labels', 'labels.txt'), 'a') as label_file:
                    label_file.write(f'{new_file_name} {letter}\n')

            except Exception as e:
                print(f"Ошибка при обработке файла {file}: {e}")

# Обрабатываем MNIST для train
process_mnist(mnist_train_dir, output_dir, "train")
print("Датасет MNIST успешно переорганизован для train.")

# Обрабатываем MNIST для test
process_mnist(mnist_test_dir, output_dir, "test")
print("Датасет MNIST успешно переорганизован для test.")

# Обрабатываем буквы для всего датасета
process_letters(letters_dir, output_dir)
print("Датасет с буквами успешно переорганизован.")

print("Датасет успешно объединен.")
