import os
import pickle
from models.gradient_descent import GradientDescentNN
from models.backpropagation import BackpropagationNN

class ModelManager:
    def __init__(self, model_name="gang_sign_model"):
        self.model_name = model_name
        self.model = None

    def create_new_model(self, input_size, hidden_sizes, output_size, model_type="backpropagation", **kwargs):
        """Создает новую модель с указанными параметрами"""
        if model_type == "gradient_descent":
            self.model = GradientDescentNN(
                input_size, hidden_sizes, output_size,
                learning_rate=kwargs.get('learning_rate', 0.001),
                reg_lambda=kwargs.get('reg_lambda', 0.0001)
            )
        elif model_type == "backpropagation":
            self.model = BackpropagationNN(
                input_size, hidden_sizes, output_size,
                learning_rate=kwargs.get('learning_rate', 0.001),
                reg_lambda=kwargs.get('reg_lambda', 0.0001),
                momentum=kwargs.get('momentum', 0.9)
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        return self.model

    def save_model(self, suffix=""):
        """Сохраняет модель в файл"""
        if self.model is None:
            raise ValueError("Model not initialized")
        filename = f"{self.model_name}{suffix}.pkl"
        self.model.save_model(filename)
        return filename

    def load_model(self, suffix=""):
        """Загружает модель из файла"""
        filename = f"{self.model_name}{suffix}.pkl"
        if not os.path.exists(filename):
            return None

        with open(filename, 'rb') as f:
            model_data = pickle.load(f)

        model_type = model_data.get('model_type', 'BackpropagationNN')
        input_size = model_data['layer_sizes'][0]
        hidden_sizes = model_data['layer_sizes'][1:-1]
        output_size = model_data['layer_sizes'][-1]

        if model_type in ["GradientDescentNN", "gradient_descent"]:
            self.model = GradientDescentNN(input_size, hidden_sizes, output_size)
        elif model_type in ["BackpropagationNN", "backpropagation"]:
            self.model = BackpropagationNN(input_size, hidden_sizes, output_size)
        else:
            raise ValueError(f"Unknown model type in file: {model_type}")

        self.model.load_model(filename)
        return self.model