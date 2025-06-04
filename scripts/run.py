import argparse
import cv2
import numpy as np
from collections import deque
from models.model_manager import ModelManager
from models.neural_network import NeuralNetwork
from utils.image_processor import ImageProcessor
import os
import sys
from data.gesture_info import GESTURE_INFO


class GangSignRecognizer:
    def __init__(self, model_suffix=""):
        self.class_names = {
            0: "Westcoast",
            1: "Crips",
            2: "MS-13",
            3: "Latin kings",
            4: "Ronaldinho",
            5: "Players club",
            6: "Simple"
        }
        self.num_classes = len(self.class_names)

        # Проверяем наличие файла модели
        model_file = f"gang_sign_model{model_suffix}.pkl"
        if not os.path.exists(model_file):
            available_models = [f for f in os.listdir() if f.startswith("gang_sign_model") and f.endswith(".pkl")]
            error_msg = f"Файл модели {model_file} не найден!\n"
            if available_models:
                error_msg += f"Доступные модели: {', '.join(available_models)}"
            else:
                error_msg += "Нет доступных моделей. Сначала обучите модель."
            raise ValueError(error_msg)

        # Загружаем модель
        manager = ModelManager()
        self.model = manager.load_model(model_suffix)
        if self.model is None:
            self.model = NeuralNetwork(64 * 64, [128, 64], self.num_classes)
            if os.path.exists(model_file):
                self.model.load_model(model_file)
            else:
                raise ValueError("Не удалось загрузить модель")

        if self.model.layer_sizes[-1] != self.num_classes:
            raise ValueError(f"Модель ожидает {self.model.layer_sizes[-1]} классов, "
                             f"но определено {self.num_classes} классов")

        self.prediction_history = deque(maxlen=15)
        self.confidence_history = deque(maxlen=15)
        self.min_confidence = 0.6
        self.show_info = False
        self.frozen_gesture = None
        self.frozen_info_image = None

        # Проверяем папку с изображениями жестов
        self.gesture_images_dir = os.path.join(os.path.dirname(__file__), "..", "data", "gesture_images")
        if not os.path.exists(self.gesture_images_dir):
            print(f"Предупреждение: папка с изображениями жестов не найдена: {self.gesture_images_dir}")

    def put_russian_text(self, img, text, position, font_scale, color, thickness):
        """Отображает русский текст на изображении"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

    def load_gesture_image(self, image_path, max_width=300, max_height=200):
        """Загружает изображение с сохранением пропорций"""
        if image_path is None or not os.path.exists(image_path):
            placeholder = np.zeros((150, 150, 3), dtype=np.uint8)
            self.put_russian_text(placeholder, "Нет изображения", (10, 75), 0.7, (255, 255, 255), 2)
            return placeholder

        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Не удалось загрузить изображение")

            # Сохраняем пропорции при ресайзе
            h, w = image.shape[:2]
            ratio = min(max_width / w, max_height / h)
            new_w, new_h = int(w * ratio), int(h * ratio)
            return cv2.resize(image, (new_w, new_h))
        except Exception as e:
            print(f"Ошибка загрузки изображения: {str(e)}")
            placeholder = np.zeros((150, 150, 3), dtype=np.uint8)
            self.put_russian_text(placeholder, "Ошибка загрузки", (10, 75), 0.7, (255, 255, 255), 2)
            return placeholder

    def create_info_window(self, gesture_name):
        """Создает информационное окно с изображением и текстом"""
        info = GESTURE_INFO.get(gesture_name)

        # Если жеста нет в словаре, создаем пустую информацию
        if info is None:
            info = {
                "description": "Информация об этом жесте отсутствует",
                "history": "",
                "meaning": "",
                "image": None
            }

        # Создаем основное изображение для окна
        info_img = np.zeros((600, 500, 3), dtype=np.uint8)
        info_img.fill(230)  # Светло-серый фон

        # Загружаем и размещаем изображение жеста
        gesture_img = self.load_gesture_image(info.get("image"))
        h, w = gesture_img.shape[:2]
        x_offset = (500 - w) // 2  # Центрируем по горизонтали
        info_img[20:20 + h, x_offset:x_offset + w] = gesture_img

        # Добавляем русский текст
        y_offset = 20 + h + 30

        self.put_russian_text(info_img, f"Gesture: {gesture_name}", (20, y_offset), 0.7, (0, 0, 0), 2)
        y_offset += 40

        self.put_russian_text(info_img, "Description:", (20, y_offset), 0.6, (0, 0, 0), 1)
        y_offset += 30
        for line in self.wrap_text(info["description"], 60):
            self.put_russian_text(info_img, line, (20, y_offset), 0.5, (0, 0, 0), 1)
            y_offset += 25
        y_offset += 20

        self.put_russian_text(info_img, "History:", (20, y_offset), 0.6, (0, 0, 0), 1)
        y_offset += 30
        for line in self.wrap_text(info["history"], 60):
            self.put_russian_text(info_img, line, (20, y_offset), 0.5, (0, 0, 0), 1)
            y_offset += 25
        y_offset += 20

        self.put_russian_text(info_img, "Meaning:", (20, y_offset), 0.6, (0, 0, 0), 1)
        y_offset += 30
        for line in self.wrap_text(info["meaning"], 60):
            self.put_russian_text(info_img, line, (20, y_offset), 0.5, (0, 0, 0), 1)
            y_offset += 25

        return info_img


    def wrap_text(self, text, max_width):
        """Переносит текст по словам"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def run(self, camera_index=0):
        cap = ImageProcessor.select_camera(camera_index)
        if cap is None:
            print("Не удалось подключиться к камере")
            return

        print("Запуск распознавания... Нажмите 'q' для выхода, 'p' для информации")

        # Создаем окно для информации
        cv2.namedWindow("Gesture Info", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Gesture Info", 500, 600)
        cv2.imshow("Gesture Info", np.zeros((600, 500, 3), dtype=np.uint8))

        current_gesture = None  # Инициализируем как None
        confidence = 0.0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    continue

                processed, bbox, skin_mask = ImageProcessor.preprocess_image(frame)

                if processed is not None:
                    try:
                        probs = self.model.predict_proba(processed.reshape(1, -1))
                        prediction = np.argmax(probs)
                        confidence = np.max(probs)

                        if confidence > self.min_confidence:
                            self.prediction_history.append(prediction)
                            self.confidence_history.append(confidence)

                        if self.prediction_history:
                            weights = np.array(self.confidence_history)
                            if weights.sum() > 0:
                                weights /= weights.sum()
                                smoothed_pred = np.round(np.dot(self.prediction_history, weights))
                                predicted_class = int(smoothed_pred)
                            else:
                                predicted_class = prediction
                        else:
                            predicted_class = prediction

                        x, y, w, h = bbox
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        current_gesture = self.class_names.get(predicted_class, "Unknown")

                        # Отображаем русский текст на основном окне
                        self.put_russian_text(frame, f"{current_gesture} ({confidence:.2f})",
                                              (x, y - 10), 0.7, (0, 255, 0), 2)

                    except Exception as e:
                        print(f"Ошибка при обработке кадра: {str(e)}")

                # Управление информационным окном
                if self.show_info:
                    if self.frozen_info_image is None and current_gesture:
                        self.frozen_gesture = current_gesture
                        self.frozen_info_image = self.create_info_window(current_gesture)

                    if self.frozen_info_image is not None:
                        cv2.imshow("Gesture Info", self.frozen_info_image)
                else:
                    self.frozen_gesture = None
                    self.frozen_info_image = None
                    cv2.imshow("Gesture Info", np.zeros((600, 500, 3), dtype=np.uint8))

                # Инструкция на русском
                self.put_russian_text(frame, "Click 'q' for exit | 'p' for information",
                                      (10, 30), 0.7, (0, 0, 255), 2)
                cv2.imshow("Gang Sign Recognizer", frame)

                key = cv2.waitKey(30) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('p'):
                    self.show_info = not self.show_info
                    if self.show_info and current_gesture:
                        self.frozen_gesture = current_gesture
                        self.frozen_info_image = self.create_info_window(current_gesture)
                        print(f"Показана информация о жесте: {current_gesture}")
                    else:
                        print("Информация скрыта")

        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Программа завершена")


def main():
    parser = argparse.ArgumentParser(description="Распознавание жестов бандитских группировок")
    parser.add_argument("--camera", type=int, default=0,
                        help="Индекс камеры (0 - встроенная, 1 - внешняя и т.д.)")
    parser.add_argument("--model", type=str, default="",
                        help="Суффикс модели (например, '_v2' для gang_sign_model_v2.pkl)")

    args = parser.parse_args()

    try:
        recognizer = GangSignRecognizer(args.model)
        recognizer.run(args.camera)
    except ValueError as e:
        print(f"Ошибка: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()