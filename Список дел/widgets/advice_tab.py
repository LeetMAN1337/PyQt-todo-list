import random
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AdviceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Советы по продуктивности")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        advice_btn = QPushButton("Получить случайный совет")
        advice_btn.setFont(QFont("Arial", 12))
        advice_btn.clicked.connect(self.show_advice)
        layout.addWidget(advice_btn)

        self.advice_label = QLabel("Нажмите кнопку, чтобы получить совет!")
        self.advice_label.setWordWrap(True)
        self.advice_label.setFont(QFont("Arial", 11))
        self.advice_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.advice_label.setStyleSheet("""
            QLabel {
                background-color: #f0f8ff;
                border: 2px solid #4682b4;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                color: black;
            }
        """)
        layout.addWidget(self.advice_label)

        layout.addStretch()
        self.setLayout(layout)

    def show_advice(self):
        self.listofhelps = []
        with open('advices.txt', 'r', encoding='utf-8') as f:
            self.listofhelps = f.readlines()
            self.advice = random.choice(self.listofhelps)
            self.advice_label.setText(self.advice)