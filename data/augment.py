import cv2
import numpy as np

# X — массив изображений (плоский вид)
#
# y — соответствующие метки (классы)
#
# метод статический — можно вызывать без создания экземпляра класса.

class DataAugmentor:
    @staticmethod
    # Списки для новых данных
    def augment_data(X, y):
        augmented_X = []
        augmented_y = []

        # Проходим по каждому изображению в датасете
        for i in range(len(X)):
            img = X[i].reshape(64, 64) # возвращаем плоское изображение в 64x64
            label = y[i]

            # Добавляем оригинальное изображение
            augmented_X.append(img.flatten())
            augmented_y.append(label)

            # Отзеркаленное изображение
            flipped = cv2.flip(img, 1)
            augmented_X.append(flipped.flatten())
            augmented_y.append(label)

            # Вращение изображения на разные углы
            for angle in [-15, -10, -5, 5, 10, 15]:
                M = cv2.getRotationMatrix2D((32, 32), angle, 1.0) # матрица поворота вокруг центра
                rotated = cv2.warpAffine(img, M, (64, 64)) # применяем поворот

                augmented_X.append(rotated.flatten())
                augmented_y.append(label)

            # Смещение изображения
            for dx, dy in [(5, 0), (-5, 0), (0, 5), (0, -5)]:
                M = np.float32([[1, 0, dx], [0, 1, dy]]) # матрица смещения
                shifted = cv2.warpAffine(img, M, (64, 64))
                augmented_X.append(shifted.flatten())
                augmented_y.append(label)

            # Добавление шума
            noise = np.random.normal(0, 0.05, (64, 64)) # нормальный шум
            noisy_img = np.clip(img + noise, 0, 1) # ограничиваем значения от 0 до 1
            augmented_X.append(noisy_img.flatten())
            augmented_y.append(label)

        # Возвращаем массивы в виде numpy-массивов
        return np.array(augmented_X), np.array(augmented_y)