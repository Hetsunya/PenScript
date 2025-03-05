# MNIST Dataset

Welcome to the GitHub page of DeepTrackAI's MNIST dataset. The MNIST dataset is a large collection of handwritten digits and is widely used for training and evaluating machine learning and deep learning models.

## Description

The MNIST dataset contains 60,000 training images and 10,000 testing images. Each image is a grayscale picture of a digit, and the associated label is the digit value (from 0 to 9).

- **Dataset Size**: 70,000 images
- **Image Size**: 28x28 pixels
- **Color**: Grayscale
- **Labels**: 10 (0 through 9)

## Usage

To use the MNIST dataset in your project:

1. Clone this repository to your local machine.
2. Import the dataset into your machine learning framework of choice.
3. Train or evaluate your models using the dataset.

### Download via Command Line

To clone the repository and access the MNIST dataset:

```bash
git clone -b mnist github.com/DeepTrackAI/MNIST_deeplay
cd MNIST_deeplay
```

### Download Programmatically in Python

If you want to load the dataset directly into a Python script or Jupyter notebook:

```python
import requests
from io import BytesIO
from zipfile import ZipFile

# URL to the repository (modify this if the dataset is hosted in a specific location or file)
DATASET_URL = 'https://github.com/DeepTrackAI/MNIST_dataset/raw/main/mnist.zip'

response = requests.get(DATASET_URL)
with ZipFile(BytesIO(response.content)) as z:
    z.extractall()

# Now you can load the dataset using your preferred library, e.g., deeplay, PyTorch, TensorFlow.
```

## Acknowledgements

- The MNIST dataset was originally created by Yann LeCun, Corinna Cortes, and Christopher Burges. Their efforts have made it one of the benchmark datasets in the machine learning community.
- [Official MNIST Database Website](http://yann.lecun.com/exdb/mnist/)

## License

The MNIST dataset is made available under the terms of the [Creative Commons Attribution-Share Alike 3.0 license](https://creativecommons.org/licenses/by-sa/3.0/).

## Contributing

If you find any issues with the dataset or have suggestions for improvements, please open an issue or submit a pull request.
