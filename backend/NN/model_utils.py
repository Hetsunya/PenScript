import torch
from torchvision import transforms
from PIL import Image
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_model(model, filepath: str, device: torch.device) -> torch.nn.Module:
    """
    Загружает модель из указанного файла и переводит её в режим предсказания.
    
    Args:
        model: Экземпляр модели PyTorch.
        filepath: Путь к файлу с сохранённой моделью.
        device: Устройство для работы модели (CPU или GPU).
    
    Returns:
        Загруженная модель в режиме предсказания.
    
    Raises:
        FileNotFoundError: Если файл модели не найден.
    """
    try:
        model.load_state_dict(torch.load(filepath, map_location=device))
        model.to(device)
        model.eval()
        logger.info(f"Модель успешно загружена из {filepath}")
        return model
    except FileNotFoundError:
        logger.error(f"Файл модели {filepath} не найден")
        raise
    except Exception as e:
        logger.error(f"Ошибка при загрузке модели: {e}")
        raise

def get_image_transforms(image_size: tuple = (128, 128)) -> transforms.Compose:
    """
    Возвращает композицию преобразований для обработки изображений.
    
    Args:
        image_size: Кортеж с размерами изображения (высота, ширина).
    
    Returns:
        Объект transforms.Compose с заданными преобразованиями.
    """
    return transforms.Compose([
        transforms.Resize(image_size),
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5,), std=(0.5,))
    ])

def predict(model: torch.nn.Module, image: Image.Image, transform: transforms.Compose,
            device: torch.device) -> int:
    """
    Выполняет предсказание класса для изображения.

    Args:
        model: Модель PyTorch для предсказания.
        image: Объект изображения PIL.
        transform: Преобразования для изображения.
        device: Устройство для работы модели.

    Returns:
        Индекс предсказанного класса.
    """
    try:
        # Apply transformations to the image
        image = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output, 1)
            return predicted.item()
    except Exception as e:
        logger.error(f"Ошибка при предсказании: {e}")
        raise
