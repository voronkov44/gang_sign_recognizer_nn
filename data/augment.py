import cv2
import numpy as np

class DataAugmentor:
    @staticmethod
    def augment_data(X, y):
        augmented_X = []
        augmented_y = []

        for i in range(len(X)):
            img = X[i].reshape(64, 64)
            label = y[i]

            augmented_X.append(img.flatten())
            augmented_y.append(label)

            flipped = cv2.flip(img, 1)
            augmented_X.append(flipped.flatten())
            augmented_y.append(label)

            for angle in [-15, -10, -5, 5, 10, 15]:
                M = cv2.getRotationMatrix2D((32, 32), angle, 1.0)
                rotated = cv2.warpAffine(img, M, (64, 64))
                augmented_X.append(rotated.flatten())
                augmented_y.append(label)

            for dx, dy in [(5, 0), (-5, 0), (0, 5), (0, -5)]:
                M = np.float32([[1, 0, dx], [0, 1, dy]])
                shifted = cv2.warpAffine(img, M, (64, 64))
                augmented_X.append(shifted.flatten())
                augmented_y.append(label)

            noise = np.random.normal(0, 0.05, (64, 64))
            noisy_img = np.clip(img + noise, 0, 1)
            augmented_X.append(noisy_img.flatten())
            augmented_y.append(label)

        return np.array(augmented_X), np.array(augmented_y)