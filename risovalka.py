import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка для символов")

        self.canvas_width = 200
        self.canvas_height = 200

        # Создаем холст для рисования
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        # Создаем изображение для сохранения рисованного
        self.image = Image.new("L", (self.canvas_width, self.canvas_height), 255)  # "L" — это режим серого
        self.draw = ImageDraw.Draw(self.image)

        # Обработчики событий
        self.canvas.bind("<B1-Motion>", self.paint)  # Рисование мышкой
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Кнопки для сохранения и очистки
        self.clear_button = tk.Button(self.root, text="Очистить", command=self.clear_canvas)
        self.clear_button.pack()

        self.save_button = tk.Button(self.root, text="Сохранить", command=self.save_image)
        self.save_button.pack()

    def paint(self, event):
        # Рисуем на холсте
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)
        self.canvas.create_oval(x1, y1, x2, y2, fill='black', width=5)

        # Рисуем на изображении
        self.draw.line([x1, y1, x2, y2], fill=0, width=5)

    def on_release(self, event):
        # Преобразуем изображение в numpy массив
        img_array = np.array(self.image)
        # Выведем массив для дальнейшего использования (можно передавать в модель)
        print(img_array)
        # Преобразуем в тензор, если нужно, с помощью библиотеки PyTorch/TensorFlow

    def clear_canvas(self):
        self.canvas.delete("all")
        # Очистим изображение
        self.image = Image.new("L", (self.canvas_width, self.canvas_height), 255)
        self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        # Сохраняем изображение
        self.image.save("drawing.png")
        print("Изображение сохранено!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
