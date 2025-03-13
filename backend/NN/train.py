import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, random_split
from sklearn.metrics import precision_recall_fscore_support
import logging

from model_utils import get_image_transforms

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HandwritingCNN(nn.Module):
    """Сверточная нейронная сеть для классификации почерка."""
    
    def __init__(self, num_classes: int = 3):
        super(HandwritingCNN, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 32 * 32, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

def load_data(data_path: str, batch_size: int = 16, train_ratio: float = 0.8) -> tuple:
    """
    Загружает и разделяет данные на обучающую и тестовую выборки.
    
    Args:
        data_path: Путь к данным.
        batch_size: Размер батча.
        train_ratio: Доля данных для обучения.
    
    Returns:
        Кортеж (train_loader, test_loader).
    """
    transform = get_image_transforms()
    dataset = ImageFolder(root=data_path, transform=transform)
    
    train_size = int(train_ratio * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    logger.info(f"Обучающих примеров: {len(train_dataset)}, тестовых примеров: {len(test_dataset)}")
    return train_loader, test_loader

def train_model(model: nn.Module, train_loader: DataLoader, optimizer: optim.Optimizer, 
                criterion: nn.Module, epochs: int = 10, device: torch.device = None):
    """Обучает модель на заданных данных."""
    device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct, total = 0, 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        train_accuracy = 100 * correct / total
        logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}, "
                    f"Train Accuracy: {train_accuracy:.2f}%")

def evaluate_model(model: nn.Module, test_loader: DataLoader, device: torch.device = None) -> dict:
    """Оценивает модель на тестовых данных."""
    device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device).eval()
    
    correct, total = 0, 0
    all_labels, all_preds = [], []
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            all_labels.extend(labels.cpu().numpy())
            all_preds.extend(predicted.cpu().numpy())
    
    accuracy = 100 * correct / total
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='weighted')
    
    metrics = {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}
    logger.info(f"Test Accuracy: {accuracy:.2f}%, Precision: {precision:.2f}, "
                f"Recall: {recall:.2f}, F1-Score: {f1:.2f}")
    return metrics

def save_model(model: nn.Module, filepath: str):
    """Сохраняет модель в файл."""
    try:
        torch.save(model.state_dict(), filepath)
        logger.info(f"Модель сохранена в {filepath}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении модели: {e}")
        raise

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data_path = "./processed_images"
    
    train_loader, test_loader = load_data(data_path)
    model = HandwritingCNN(num_classes=3)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    train_model(model, train_loader, optimizer, criterion, epochs=10, device=device)
    evaluate_model(model, test_loader, device=device)
    save_model(model, "handwriting_model.pth")