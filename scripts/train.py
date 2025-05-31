import argparse

import numpy as np

from models.model_manager import ModelManager
from data.dataset import DatasetLoader
from data.augment import DataAugmentor


def main():
    parser = argparse.ArgumentParser(description="Train gang sign recognition model")
    parser.add_argument("--data", type=str, default="training_data", help="Data directory")
    parser.add_argument("--suffix", type=str, default="", help="Model suffix")

    args = parser.parse_args()

    print("Loading training data...")
    try:
        X, y = DatasetLoader.load_training_data(args.data)
        num_classes = len(np.unique(y))
        print(f"Количество классов в данных: {num_classes}")
    except Exception as e:
        print(f"Ошибка загрузки данных: {str(e)}")
        return

    print("Augmenting data...")
    X_aug, y_aug = DataAugmentor.augment_data(X, y)
    print(f"После аугментации: {X_aug.shape[0]} образцов")

    print("Creating model...")
    manager = ModelManager()
    try:
        model = manager.create_new_model(64 * 64, [128, 64], num_classes)
        print(f"Создана модель с {num_classes} выходными нейронами")
    except Exception as e:
        print(f"Ошибка создания модели: {str(e)}")
        return

    print("Training model...")
    try:
        model.train(X_aug, y_aug, epochs=2000)  # Увеличили количество эпох
    except Exception as e:
        print(f"Ошибка обучения: {str(e)}")
        return

    print("Saving model...")
    try:
        saved_file = manager.save_model(args.suffix)
        print(f"Модель сохранена в {saved_file}")
    except Exception as e:
        print(f"Ошибка сохранения модели: {str(e)}")


if __name__ == "__main__":
    main()