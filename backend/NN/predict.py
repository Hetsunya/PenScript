from flask import Flask, request, jsonify
from flask_cors import CORS  # Импортируем CORS
import torch
from model_utils import load_model, get_image_transforms, predict
from train import HandwritingCNN
import logging
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех источников

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class_names = ["Дени", "Дмитрий", "Виталий"]  # Имена классов

# Загрузка модели
model = HandwritingCNN(num_classes=len(class_names))
model = load_model(model, "handwriting_model.pth", device)

@app.route("/predict", methods=["POST"])
def predict_image():
    logger.info("Received prediction request")
    data = request.json
    encoded_image = data["image"]

    # Декодируем изображение
    image_data = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(image_data)).convert("L")

    transform = get_image_transforms()
    owner_idx = predict(model, image, transform, device)
    predicted_class = class_names[owner_idx]

    logger.info(f"Predicted class: {predicted_class}")
    return jsonify({"predicted_class": predicted_class})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
