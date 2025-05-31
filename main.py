import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Проверяем наличие хотя бы одной модели
    import os
    models = [f for f in os.listdir() if f.startswith("gang_sign_model") and f.endswith(".pkl")]

    window = MainWindow()
    window.show()

    if not models:
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(window, "Предупреждение",
                            "Не найдено ни одной обученной модели!\nПожалуйста, сначала обучите модель.")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()