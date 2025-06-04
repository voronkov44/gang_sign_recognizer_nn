from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QLabel, QComboBox, QFileDialog,
                             QInputDialog, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt
import os
import subprocess
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gang Sign Recognizer")
        self.setGeometry(100, 100, 500, 350)  # Увеличим размер окна
        self.init_ui()

    def init_ui(self):
        # Widgets
        self.label = QLabel("Выберите действие:")
        self.btn_capture = QPushButton("Сбор данных")
        self.btn_train = QPushButton("Обучение модели")
        self.btn_run = QPushButton("Распознавание")

        # Настройки камеры
        self.camera_label = QLabel("Выбор камеры:")
        self.camera_combo = QComboBox()
        self.camera_combo.addItem("iPhone (0)", 0)
        self.camera_combo.addItem("Mac (1)", 1)

        # Настройки модели
        self.model_label = QLabel("Модель:")
        self.model_combo = QComboBox()
        self.update_model_list()

        # Настройки алгоритма обучения
        self.algorithm_label = QLabel("Алгоритм обучения:")
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItem("Обратное распространение с моментом", "backpropagation")
        self.algorithm_combo.addItem("Градиентный спуск", "gradient_descent")

        # Параметры обучения
        self.learning_rate_label = QLabel("Скорость обучения:")
        self.learning_rate_input = QComboBox()
        self.learning_rate_input.addItems(["0.1", "0.01", "0.001", "0.0001"])
        self.learning_rate_input.setCurrentText("0.001")

        self.epochs_label = QLabel("Количество эпох:")
        self.epochs_input = QComboBox()
        self.epochs_input.addItems(["100", "500", "1000", "2000"])
        self.epochs_input.setCurrentText("1000")

        # Layout
        layout = QVBoxLayout()

        # Добавляем основные элементы
        layout.addWidget(self.label)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.camera_combo)
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_combo)

        # Группируем параметры обучения
        training_group = QVBoxLayout()
        training_group.addWidget(QLabel("<b>Параметры обучения:</b>"))

        # Алгоритм обучения
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(self.algorithm_label)
        algo_layout.addWidget(self.algorithm_combo)
        training_group.addLayout(algo_layout)

        # Скорость обучения
        lr_layout = QHBoxLayout()
        lr_layout.addWidget(self.learning_rate_label)
        lr_layout.addWidget(self.learning_rate_input)
        training_group.addLayout(lr_layout)

        # Количество эпох
        epochs_layout = QHBoxLayout()
        epochs_layout.addWidget(self.epochs_label)
        epochs_layout.addWidget(self.epochs_input)
        training_group.addLayout(epochs_layout)

        layout.addLayout(training_group)

        # Кнопки
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
                    algorithm = self.algorithm_combo.currentData()
                    learning_rate = float(self.learning_rate_input.currentText())
                    epochs = int(self.epochs_input.currentText())

                    cmd = [
                        sys.executable, "-m", "scripts.train",
                        "--data", data_dir,
                        "--algorithm", algorithm,
                        "--learning_rate", str(learning_rate),
                        "--epochs", str(epochs)
                    ]

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