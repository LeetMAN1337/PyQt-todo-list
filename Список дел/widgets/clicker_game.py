from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class ClickerGameTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.score = 0
        self.click_power = 1
        self.auto_click_power = 0

        self.base_click_price = 10
        self.base_auto_price = 50
        self.base_super_price = 200

        self.current_click_price = self.base_click_price
        self.current_auto_price = self.base_auto_price
        self.current_super_price = self.base_super_price

        self.click_price_multiplier = 2
        self.auto_price_multiplier = 2
        self.super_price_multiplier = 10

        self.number_format = "обычная"

        self.auto_click_timer = QTimer()
        self.setup_ui()
        self.setup_game()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🎮 Кликер")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(title)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Формат чисел:"))

        self.format_combo = QComboBox()
        self.format_combo.addItem("Обычная нотация", "обычная")
        self.format_combo.addItem("Научная нотация", "научная")
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        format_layout.addWidget(self.format_combo)

        format_layout.addStretch()
        layout.addLayout(format_layout)

        self.click_button = QPushButton("КЛИКАЙ СЮДА!")
        self.click_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.click_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 30px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.click_button.clicked.connect(self.on_click)
        layout.addWidget(self.click_button)

        stats_layout = QVBoxLayout()

        self.score_label = QLabel()
        self.score_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.score_label)

        self.click_power_label = QLabel()
        self.click_power_label.setFont(QFont("Arial", 12))
        self.click_power_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.click_power_label)

        self.auto_click_label = QLabel()
        self.auto_click_label.setFont(QFont("Arial", 12))
        self.auto_click_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.auto_click_label)

        layout.addLayout(stats_layout)

        upgrades_label = QLabel("Улучшения:")
        upgrades_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(upgrades_label)

        self.upgrade_click_btn = QPushButton()
        self.upgrade_click_btn.clicked.connect(self.upgrade_click_power)
        layout.addWidget(self.upgrade_click_btn)

        self.upgrade_auto_btn = QPushButton()
        self.upgrade_auto_btn.clicked.connect(self.upgrade_auto_click)
        layout.addWidget(self.upgrade_auto_btn)

        self.super_upgrade_btn = QPushButton()
        self.super_upgrade_btn.setStyleSheet("background-color: #ff9800; color: white; font-weight: bold;")
        self.super_upgrade_btn.clicked.connect(self.super_upgrade)
        layout.addWidget(self.super_upgrade_btn)

        reset_btn = QPushButton("Сбросить игру")
        reset_btn.setStyleSheet("background-color: #f44336; color: white;")
        reset_btn.clicked.connect(self.reset_game)
        layout.addWidget(reset_btn)

        layout.addStretch()
        self.setLayout(layout)

    def on_format_changed(self, text):
        if text == "Обычная нотация":
            self.number_format = "обычная"
        else:
            self.number_format = "научная"
        self.update_ui()

    def format_number(self, number):
        if self.number_format == "научная":
            if number >= 1000:
                return f"{number:.2e}"
            else:
                return str(number)
        else:
            return f"{number:,}".replace(",", " ")

    def setup_game(self):
        self.auto_click_timer.timeout.connect(self.auto_click)
        self.auto_click_timer.start(1000)
        self.update_ui()

    def on_click(self):
        self.score += self.click_power
        self.update_ui()

        self.click_button.setStyleSheet("""
            QPushButton {
                background-color: #45a049;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 30px;
                margin: 20px;
            }
        """)
        QTimer.singleShot(100, self.reset_button_style)

    def reset_button_style(self):
        self.click_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 30px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

    def auto_click(self):
        if self.auto_click_power > 0:
            self.score += self.auto_click_power
            self.update_ui()

    def upgrade_click_power(self):
        if self.score >= self.current_click_price:
            self.score -= self.current_click_price
            self.click_power += 1
            self.current_click_price *= self.click_price_multiplier
            self.update_ui()
        else:
            self.show_message("Недостаточно очков!")

    def upgrade_auto_click(self):
        if self.score >= self.current_auto_price:
            self.score -= self.current_auto_price
            self.auto_click_power += 1
            self.current_auto_price *= self.auto_price_multiplier
            self.update_ui()
        else:
            self.show_message("Недостаточно очков!")

    def super_upgrade(self):
        if self.score >= self.current_super_price:
            self.score -= self.current_super_price
            self.click_power += 5
            self.auto_click_power += 5
            self.current_super_price *= self.super_price_multiplier
            self.update_ui()
        else:
            self.show_message("Недостаточно очков!")

    def reset_game(self):
        reply = QMessageBox.question(self, 'Сброс игры',
                                     'Вы уверены, что хотите сбросить игру?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.score = 0
            self.click_power = 1
            self.auto_click_power = 0

            self.current_click_price = self.base_click_price
            self.current_auto_price = self.base_auto_price
            self.current_super_price = self.base_super_price

            self.update_ui()
            self.show_message("Игра сброшена!")

    def update_ui(self):
        formatted_score = self.format_number(self.score)
        formatted_click_power = self.format_number(self.click_power)
        formatted_auto_power = self.format_number(self.auto_click_power)
        formatted_click_price = self.format_number(self.current_click_price)
        formatted_auto_price = self.format_number(self.current_auto_price)
        formatted_super_price = self.format_number(self.current_super_price)

        format_hint = " (научная)" if self.number_format == "научная" else " (обычная)"

        self.score_label.setText(f"Очков: {formatted_score}{format_hint}")
        self.click_power_label.setText(f"Сила клика: {formatted_click_power}")
        self.auto_click_label.setText(f"Авто-клики: {formatted_auto_power}/сек")

        self.upgrade_click_btn.setText(f"Усилить клик (+1) - {formatted_click_price} очков")
        self.upgrade_auto_btn.setText(f"Авто-клик (+1/сек) - {formatted_auto_price} очков")
        self.super_upgrade_btn.setText(f"СУПЕР УЛУЧШЕНИЕ (+5) - {formatted_super_price} очков")

        self.upgrade_click_btn.setEnabled(self.score >= self.current_click_price)
        self.upgrade_auto_btn.setEnabled(self.score >= self.current_auto_price)
        self.super_upgrade_btn.setEnabled(self.score >= self.current_super_price)

        self.update_button_colors()

    def update_button_colors(self):
        if self.score >= self.current_click_price:
            self.upgrade_click_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
        else:
            self.upgrade_click_btn.setStyleSheet("""
                QPushButton {
                    background-color: #BDBDBD;
                    color: #757575;
                    padding: 8px;
                }
            """)

        if self.score >= self.current_auto_price:
            self.upgrade_auto_btn.setStyleSheet("""
                QPushButton {
                    background-color: #9C27B0;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #7B1FA2;
                }
            """)
        else:
            self.upgrade_auto_btn.setStyleSheet("""
                QPushButton {
                    background-color: #BDBDBD;
                    color: #757575;
                    padding: 8px;
                }
            """)

        if self.score >= self.current_super_price:
            self.super_upgrade_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
            """)
        else:
            self.super_upgrade_btn.setStyleSheet("""
                QPushButton {
                    background-color: #BDBDBD;
                    color: #757575;
                    padding: 8px;
                }
            """)

    def show_message(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Кликер")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()