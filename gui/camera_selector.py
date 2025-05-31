from PyQt5 import QtWidgets
import cv2

class CameraSelectorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор камеры")
        self.layout = QtWidgets.QVBoxLayout(self)

        self.camera_list = QtWidgets.QComboBox()
        self.layout.addWidget(self.camera_list)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.populate_cameras()

    def populate_cameras(self):
        self.camera_list.clear()
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.camera_list.addItem(f"Камера {i}", i)
                cap.release()

    def get_selected_camera(self):
        return self.camera_list.currentData()
