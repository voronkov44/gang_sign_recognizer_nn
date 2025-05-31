import os
import numpy as np


class DatasetLoader:
    @staticmethod
    def load_training_data(data_dir):
        X = []
        y = []

        if not os.path.exists(data_dir):
            raise ValueError(f"Директория {data_dir} не существует")

        class_ids = sorted([int(d) for d in os.listdir(data_dir)
                            if os.path.isdir(os.path.join(data_dir, d)) and d.isdigit()])

        if not class_ids:
            raise ValueError(f"В директории {data_dir} нет числовых поддиректорий (0, 1, 2...)")

        print("Найдены следующие классы:")
        for class_id in class_ids:
            print(f"  {class_id}: {class_id}")

        for class_id in class_ids:
            class_dir = os.path.join(data_dir, str(class_id))

            if not os.listdir(class_dir):
                print(f"Предупреждение: директория класса {class_id} пуста")
                continue

            for filename in os.listdir(class_dir):
                if filename.endswith('.npy'):  # Изменено для загрузки .npy файлов
                    filepath = os.path.join(class_dir, filename)
                    try:
                        # Загружаем .npy файл
                        img_data = np.load(filepath)
                        X.append(img_data)
                        y.append(class_id)
                    except Exception as e:
                        print(f"Ошибка загрузки файла {filepath}: {str(e)}")

        if not X:
            raise ValueError("Не найдено ни одного валидного .npy файла для обучения")

        return np.array(X), np.array(y)