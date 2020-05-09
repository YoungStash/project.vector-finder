from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *


# Класс с элементами для интерфейса
class GuiMainWindow(object):
    # Метод, добавляющий элементы на окно
    def setup(self, main_window):
        main_window.resize(640, 480)    # Устанавливает размер окна
        main_window.setMinimumSize(QtCore.QSize(640, 480))

        central_widget = QtWidgets.QWidget(main_window)
        self.create_widgets(central_widget)
        main_window.setCentralWidget(central_widget)

        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 26))
        main_window.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

    # Создает виджеты в окне
    def create_widgets(self, central_widget):
        horizontal_layout = QtWidgets.QHBoxLayout(central_widget)

        # Список векторов
        vertical_layout = QtWidgets.QVBoxLayout(central_widget)

        self.itemList = QtWidgets.QListWidget()
        self.itemList.setWindowTitle("Stored Vectors")
        vertical_layout.addWidget(self.itemList)

        horizontal_layout.addLayout(vertical_layout)

        vertical_layout = QtWidgets.QVBoxLayout(central_widget)
        vertical_layout.setAlignment(Qt.AlignTop)

        # Виджеты добавления вектора
        horizontal_layout_1 = QtWidgets.QHBoxLayout(central_widget)
        horizontal_layout_1.setContentsMargins(0, 10, 0, 0)

        self.add_x = QtWidgets.QLineEdit()
        self.add_x.setPlaceholderText("X position")
        horizontal_layout_1.addWidget(self.add_x)

        self.add_y = QtWidgets.QLineEdit()
        self.add_y.setPlaceholderText("Y position")
        horizontal_layout_1.addWidget(self.add_y)

        self.add_z = QtWidgets.QLineEdit()
        self.add_z.setPlaceholderText("Z position")
        horizontal_layout_1.addWidget(self.add_z)

        vertical_layout.addLayout(horizontal_layout_1)

        self.add_push = QtWidgets.QPushButton()
        self.add_push.setText("Add to vectors")
        vertical_layout.addWidget(self.add_push)

        # Виджеты удаления вектора
        horizontal_layout_1 = QtWidgets.QHBoxLayout(central_widget)
        horizontal_layout_1.setContentsMargins(0, 20, 0, 0)

        self.remove_id = QtWidgets.QLineEdit()
        self.remove_id.setPlaceholderText('Type name (unique id) here...')
        horizontal_layout_1.addWidget(self.remove_id)

        self.remove_push = QtWidgets.QPushButton()
        self.remove_push.setText("Remove vector by it's id")
        horizontal_layout_1.addWidget(self.remove_push)

        vertical_layout.addLayout(horizontal_layout_1)

        # Виджеты поиска ближаших векторов
        horizontal_layout_1 = QtWidgets.QHBoxLayout(central_widget)
        horizontal_layout_1.setContentsMargins(0, 50, 0, 0)

        self.target_x = QtWidgets.QLineEdit()
        self.target_x.setPlaceholderText("X position")
        horizontal_layout_1.addWidget(self.target_x)

        self.target_y = QtWidgets.QLineEdit()
        self.target_y.setPlaceholderText("Y position")
        horizontal_layout_1.addWidget(self.target_y)

        self.target_z = QtWidgets.QLineEdit()
        self.target_z.setPlaceholderText("Z position")
        horizontal_layout_1.addWidget(self.target_z)

        vertical_layout.addLayout(horizontal_layout_1)

        self.target_push = QtWidgets.QPushButton()
        self.target_push.setText("Find closest")
        vertical_layout.addWidget(self.target_push)

        horizontal_layout.addLayout(vertical_layout)
