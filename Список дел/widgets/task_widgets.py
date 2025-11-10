from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QListWidgetItem, QDialog, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class TaskItemWidget(QWidget):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        id_time_layout = QHBoxLayout()
        id_label = QLabel(f"ID: {self.task.id}")
        id_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))

        time_label = QLabel(f"Время: {self.task.time}")
        time_label.setFont(QFont("Arial", 9))

        id_time_layout.addWidget(id_label)
        id_time_layout.addStretch()
        id_time_layout.addWidget(time_label)

        text_label = QLabel(self.task.text)
        text_label.setWordWrap(True)
        text_label.setFont(QFont("Arial", 10))

        layout.addLayout(id_time_layout)
        layout.addWidget(text_label)

        self.setLayout(layout)
        self.setStyleSheet("""
            TaskItemWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
                margin: 2px;
            }
            TaskItemWidget:hover {
                background-color: #e9e9e9;
            }
        """)


class AdviceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Совет")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Совет для продуктивности:")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.advice_label = QLabel()
        self.advice_label.setWordWrap(True)
        self.advice_label.setFont(QFont("Arial", 10))
        self.advice_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.advice_label)

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def set_advice(self, advice):
        self.advice_label.setText(advice)