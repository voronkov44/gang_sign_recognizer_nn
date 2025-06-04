import os
import cv2
import numpy as np
from utils.image_processor import ImageProcessor

class DataCapture:
    def __init__(self, output_dir="training_data"):
        self.output_dir = output_dir
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

    def capture(self, camera_index=0, samples_per_class=700):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        cap = ImageProcessor.select_camera(camera_index)
        if cap is None:
            return

        print("Сбор данных для обучения гангстерских символов:")
        for class_id, class_name in self.class_names.items():
            print(f"{class_id}: {class_name}")

        print("\nНажмите 'c' для захвата изображения")
        print("Нажмите 'q' для завершения")

        try:
            for class_id in range(len(self.class_names)):
                class_dir = os.path.join(self.output_dir, str(class_id))
                if not os.path.exists(class_dir):
                    os.makedirs(class_dir)

                print(f"\nГотовьтесь к захвату изображений для класса {class_id} ({self.class_names[class_id]})")
                print("Нажмите любую клавишу, когда будете готовы...")

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        continue

                    cv2.putText(frame, "Press any key to start capturing...",
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.imshow("Capture Training Data", frame)

                    key = cv2.waitKey(30)
                    if key != -1:
                        break
                    if cv2.getWindowProperty("Capture Training Data", cv2.WND_PROP_VISIBLE) < 1:
                        break

                count = 0
                while count < samples_per_class:
                    ret, frame = cap.read()
                    if not ret:
                        continue

                    display_frame = frame.copy()
                    cv2.putText(display_frame,
                                f"Class: {self.class_names[class_id]} - Captured: {count}/{samples_per_class}",
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(display_frame, "Press 'c' to capture, 'q' to quit",
                                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    processed, bbox, skin_mask = ImageProcessor.preprocess_image(frame)
                    if processed is not None:
                        hand_img = (processed.reshape(64, 64) * 255).astype(np.uint8)
                        hand_img_display = cv2.resize(hand_img, (128, 128))
                        cv2.imshow("Hand Preview", hand_img_display)

                    cv2.imshow("Capture Training Data", display_frame)

                    key = cv2.waitKey(30) & 0xFF
                    if key == ord('c'):
                        if processed is not None:
                            filename = os.path.join(class_dir, f"sample_{count}.npy")
                            np.save(filename, processed)
                            count += 1
                            print(f"Saved sample {count} for class {class_id} ({self.class_names[class_id]})")
                        else:
                            print("Hand not detected! Try again.")
                    elif key == ord('q'):
                        raise KeyboardInterrupt

        except KeyboardInterrupt:
            print("\nЗавершение сбора данных по запросу пользователя")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            for i in range(5):
                cv2.waitKey(1)