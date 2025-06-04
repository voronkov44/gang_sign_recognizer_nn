import numpy as np
import pickle
from abc import ABC, abstractmethod


class BaseNeuralNetwork(ABC):
    def __init__(self, input_size, hidden_sizes, output_size):
        self.layer_sizes = [input_size] + hidden_sizes + [output_size]
        self.weights = []
        self.biases = []

        # Инициализация весов и смещений
        for i in range(len(self.layer_sizes) - 1):
            scale = np.sqrt(2.0 / (self.layer_sizes[i] + self.layer_sizes[i + 1]))
            self.weights.append(np.random.randn(self.layer_sizes[i], self.layer_sizes[i + 1]) * scale)
            self.biases.append(np.zeros((1, self.layer_sizes[i + 1])))

        self.best_weights = None
        self.best_biases = None

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return (x > 0).astype(float)

    def softmax(self, x):
        exps = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exps / np.sum(exps, axis=1, keepdims=True)

    def forward(self, X):
        self.activations = [X]
        self.z_values = []

        for i in range(len(self.weights) - 1):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            self.z_values.append(z)
            self.activations.append(self.relu(z))

        z = np.dot(self.activations[-1], self.weights[-1]) + self.biases[-1]
        self.z_values.append(z)
        self.activations.append(self.softmax(z))

        return self.activations[-1]

    @abstractmethod
    def backward(self, X, y):
        pass

    @abstractmethod
    def train(self, X, y, epochs=1000, batch_size=64, validation_split=0.2):
        pass

    def predict(self, X):
        probs = self.forward(X)
        return np.argmax(probs, axis=1)

    def predict_proba(self, X):
        return self.forward(X)

    def accuracy(self, X, y):
        predictions = self.predict(X)
        return np.mean(predictions == y) * 100

    def save_model(self, filename):
        model_data = {
            'weights': self.weights,
            'biases': self.biases,
            'layer_sizes': self.layer_sizes,
            'model_type': self.__class__.__name__
        }
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        self.weights = model_data['weights']
        self.biases = model_data['biases']
        self.layer_sizes = model_data['layer_sizes']