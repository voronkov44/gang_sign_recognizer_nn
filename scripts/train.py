import argparse
import numpy as np
from models.model_manager import ModelManager
import os


def load_data(data_dir):
    X = []
    y = []

    for class_id in os.listdir(data_dir):
        class_dir = os.path.join(data_dir, class_id)
        if not os.path.isdir(class_dir):
            continue

        for sample_file in os.listdir(class_dir):
            if sample_file.endswith('.npy'):
                sample_path = os.path.join(class_dir, sample_file)
                data = np.load(sample_path)
                X.append(data.flatten())
                y.append(int(class_id))

    return np.array(X), np.array(y)


def main():
    parser = argparse.ArgumentParser(description="Обучение модели распознавания жестов")
    parser.add_argument("--data", required=True, help="Путь к папке с данными")
    parser.add_argument("--suffix", default="", help="Суффикс для имени модели")
    parser.add_argument("--algorithm", default="backpropagation",
                        choices=["backpropagation", "gradient_descent"],
                        help="Алгоритм обучения")
    parser.add_argument("--learning_rate", type=float, default=0.001,
                        help="Скорость обучения")
    parser.add_argument("--epochs", type=int, default=1000,
                        help="Количество эпох обучения")

    args = parser.parse_args()

    # Загрузка данных
    X, y = load_data(args.data)
    input_size = X.shape[1]
    output_size = len(np.unique(y))

    # Создание модели
    manager = ModelManager()
    model = manager.create_new_model(
        input_size=input_size,
        hidden_sizes=[128, 64],
        output_size=output_size,
        model_type=args.algorithm,
        learning_rate=args.learning_rate
    )

    # Обучение модели
    model.train(X, y, epochs=args.epochs)

    # Сохранение модели
    model_file = manager.save_model(args.suffix)
    print(f"Модель сохранена как {model_file}")


if __name__ == "__main__":
    main()