import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QListView,
    QSplitter,
)
from PyQt6.QtCore import QDir, QModelIndex
from PyQt6.QtGui import QFileSystemModel


class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.url_bar = QLineEdit()
        self.layout.addWidget(self.url_bar)

        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath(QDir.rootPath())

        self.tree_view = QListView()
        self.tree_view.setModel(self.dir_model)
        self.tree_view.setRootIndex(self.dir_model.index(QDir.rootPath()))

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())

        self.file_list = QTreeView()
        self.file_list.setModel(self.file_model)

        splitter = QSplitter()
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.file_list)

        self.layout.addWidget(splitter)

        self.url_bar.returnPressed.connect(self.change_directory)
        self.tree_view.clicked.connect(self.update_directory_from_tree)

        # Initialize with home directory
        home_dir = QDir.homePath()
        self.url_bar.setText(home_dir)
        self.change_directory()

    def change_directory(self):
        path = self.url_bar.text()
        if os.path.exists(path):
            self.file_model.setRootPath(path)
            self.file_list.setRootIndex(self.file_model.index(path))

    def update_directory_from_tree(self, index: QModelIndex):
        path = self.dir_model.filePath(index)
        self.url_bar.setText(path)
        self.change_directory()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileExplorer()
    window.show()
    sys.exit(app.exec())
