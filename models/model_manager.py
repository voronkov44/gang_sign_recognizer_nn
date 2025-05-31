import os
import pickle
from models.neural_network import NeuralNetwork


class ModelManager:
    def __init__(self, model_name="gang_sign_model"):
        self.model_name = model_name
        self.model = None

    def create_new_model(self, input_size, hidden_sizes, output_size):
        """Создает новую модель с указанными параметрами"""
        self.model = NeuralNetwork(input_size, hidden_sizes, output_size)
        return self.model

    def save_model(self, suffix=""):
        """Сохраняет модель в файл"""
        filename = f"{self.model_name}{suffix}.pkl"
        self.model.save_model(filename)
        return filename

    def load_model(self, suffix=""):
        """Загружает модель из файла"""
        filename = f"{self.model_name}{suffix}.pkl"
        if not os.path.exists(filename):
            return None

            # Сначала загружаем данные модели
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)

            # Затем создаем модель с правильными параметрами
        input_size = model_data['layer_sizes'][0]
        hidden_sizes = model_data['layer_sizes'][1:-1]
        output_size = model_data['layer_sizes'][-1]

        self.model = NeuralNetwork(input_size, hidden_sizes, output_size)
        self.model.load_model(filename)
        return self.model