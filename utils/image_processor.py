import cv2
import numpy as np


class ImageProcessor:
    # Оптимальные параметры для детекции кожи
    SKIN_LOWER = np.array([0, 135, 85], dtype=np.uint8)
    SKIN_UPPER = np.array([255, 180, 135], dtype=np.uint8)
    MORPH_KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    BLUR_KERNEL = (3, 3)
    MIN_CONTOUR_AREA = 1000
    ASPECT_RATIO_RANGE = (0.3, 3.0)
    PADDING = 20

    @staticmethod
    def preprocess_image(image, size=(64, 64)):
        """Улучшенная обработка изображения с детекцией руки"""
        try:
            # Конвертация в YCrCb и создание маски кожи
            ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            skin_mask = cv2.inRange(ycrcb, ImageProcessor.SKIN_LOWER, ImageProcessor.SKIN_UPPER)

            # Морфологические операции для улучшения маски
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, ImageProcessor.MORPH_KERNEL)
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, ImageProcessor.MORPH_KERNEL)
            skin_mask = cv2.GaussianBlur(skin_mask, ImageProcessor.BLUR_KERNEL, 0)

            # Поиск и фильтрация контуров
            contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                return None, None, skin_mask

                # Фильтрация контуров по площади и соотношению сторон
            valid_contours = [
                cnt for cnt in contours
                if (ImageProcessor._is_valid_contour(cnt, image.shape))
            ]

            if not valid_contours:
                return None, None, skin_mask

                # Выбор основного контура и получение ROI
            hand_contour = max(valid_contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(hand_contour)

            # Добавление padding с проверкой границ
            x, y, w, h = ImageProcessor._apply_padding(x, y, w, h, image.shape)

            # Выделение и обработка области руки
            hand_roi = skin_mask[y:y + h, x:x + w]
            processed = ImageProcessor._normalize_roi(hand_roi, size)

            return processed, (x, y, w, h), skin_mask

        except Exception as e:
            print(f"Ошибка обработки изображения: {str(e)}")
            return None, None, np.zeros_like(image[:, :, 0]) if len(image.shape) == 3 else np.zeros_like(image)

    @staticmethod
    def _is_valid_contour(cnt, img_shape):
        """Проверяет валидность контура по площади и соотношению сторон"""
        area = cv2.contourArea(cnt)
        if area < ImageProcessor.MIN_CONTOUR_AREA:
            return False

        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        min_ratio, max_ratio = ImageProcessor.ASPECT_RATIO_RANGE

        return min_ratio <= aspect_ratio <= max_ratio

    @staticmethod
    def _apply_padding(x, y, w, h, img_shape):
        """Добавляет padding к ограничивающему прямоугольнику с проверкой границ"""
        pad = ImageProcessor.PADDING
        new_x = max(0, x - pad)
        new_y = max(0, y - pad)
        new_w = min(img_shape[1] - new_x, w + 2 * pad)
        new_h = min(img_shape[0] - new_y, h + 2 * pad)
        return new_x, new_y, new_w, new_h

    @staticmethod
    def _normalize_roi(roi, size):
        """Нормализует и изменяет размер области интереса"""
        resized = cv2.resize(roi, size)
        normalized = resized / 255.0
        return np.nan_to_num(normalized).flatten()

    @staticmethod
    def select_camera(camera_index=0):
        """Пытается подключиться к камере с обработкой исключений"""
        try:
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                raise RuntimeError(f"Камера {camera_index} недоступна")

                # Проверка, что камера действительно работает
            ret, _ = cap.read()
            if not ret:
                cap.release()
                raise RuntimeError(f"Не удалось получить кадр с камеры {camera_index}")

            return cap
        except Exception as e:
            print(f"Ошибка инициализации камеры: {str(e)}")
            return None

    @staticmethod
    def draw_debug_info(image, bbox, label, confidence):
        """Рисует отладочную информацию на изображении"""
        if bbox is not None:
            x, y, w, h = bbox
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, f"{label} ({confidence:.2f})",
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return image

    @staticmethod
    def draw_prediction(image, gesture, confidence):
        """Рисует результат распознавания на изображении"""
        text = f"{gesture} ({confidence:.2%})"
        cv2.putText(image, text, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return image