from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QLabel, QComboBox, QFileDialog,
                             QInputDialog, QMessageBox)
from PyQt5.QtCore import Qt
import os
import subprocess
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gang Sign Recognizer")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        # Widgets
        self.label = QLabel("Выберите действие:")
        self.btn_capture = QPushButton("Сбор данных")
        self.btn_train = QPushButton("Обучение модели")
        self.btn_run = QPushButton("Распознавание")

        self.camera_label = QLabel("Выбор камеры:")
        self.camera_combo = QComboBox()
        self.camera_combo.addItem("iPhone (0)", 0)
        self.camera_combo.addItem("Mac (1)", 1)

        self.model_label = QLabel("Модель:")
        self.model_combo = QComboBox()
        self.update_model_list()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.camera_combo)
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_combo)
        layout.addWidget(self.btn_capture)
        layout.addWidget(self.btn_train)
        layout.addWidget(self.btn_run)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connections
        self.btn_capture.clicked.connect(self.start_capture)
        self.btn_train.clicked.connect(self.start_training)
        self.btn_run.clicked.connect(self.start_recognition)

    def update_model_list(self):
        self.model_combo.clear()
        models = [f for f in os.listdir() if f.startswith("gang_sign_model") and f.endswith(".pkl")]
        if not models:
            self.model_combo.addItem("Нет моделей", "")
        else:
            for model in models:
                suffix = model.replace("gang_sign_model", "").replace(".pkl", "")
                self.model_combo.addItem(model, suffix)

    def start_capture(self):
        camera_index = self.camera_combo.currentData()
        output_dir = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения данных")
        if output_dir:
            try:
                subprocess.Popen([sys.executable, "-m", "scripts.capture",
                                  "--camera", str(camera_index),
                                  "--output", output_dir])
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось запустить сбор данных: {str(e)}")

    def start_training(self):
        data_dir = QFileDialog.getExistingDirectory(self, "Выберите папку с данными")
        if data_dir:
            model_suffix, ok = QInputDialog.getText(self, "Имя модели",
                                                    "Введите суффикс для модели (оставьте пустым для стандартного):")
            if ok:
                try:
                    cmd = [sys.executable, "-m", "scripts.train", "--data", data_dir]
                    if model_suffix:
                        cmd.extend(["--suffix", model_suffix])
                    subprocess.Popen(cmd)
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось запустить обучение: {str(e)}")

    def start_recognition(self):
        camera_index = self.camera_combo.currentData()
        model_suffix = self.model_combo.currentData()

        # Проверяем наличие модели
        model_file = f"gang_sign_model{model_suffix}.pkl"
        if not os.path.exists(model_file):
            QMessageBox.critical(self, "Ошибка",
                                 f"Модель {model_file} не найдена!\nПожалуйста, сначала обучите модель.")
            return

        try:
            cmd = [sys.executable, "-m", "scripts.run", "--camera", str(camera_index)]
            if model_suffix:
                cmd.extend(["--model", model_suffix])
            subprocess.Popen(cmd)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить распознавание: {str(e)}")


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()