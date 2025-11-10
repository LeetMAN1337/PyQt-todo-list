from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QLineEdit, QTextEdit, QListWidget,
                            QListWidgetItem, QMessageBox, QDateTimeEdit,
                            QFormLayout)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal
from PyQt6.QtGui import QFont

from models import Task
from database import DatabaseManager
from widgets import TaskItemWidget

class CreateTaskTab(QWidget):
    task_created = pyqtSignal()

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Создание нового дела")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()

        self.time_edit = QDateTimeEdit()
        self.time_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.time_edit.setCalendarPopup(True)
        self.time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        form_layout.addRow("Время выполнения:", self.time_edit)

        self.task_edit = QTextEdit()
        self.task_edit.setMaximumHeight(150)
        self.task_edit.setPlaceholderText("Введите описание дела...")
        form_layout.addRow("Описание дела:", self.task_edit)

        layout.addLayout(form_layout)

        add_btn = QPushButton("Добавить дело")
        add_btn.clicked.connect(self.add_task)
        add_btn.setFont(QFont("Arial", 12))
        layout.addWidget(add_btn)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setLayout(layout)

    def add_task(self):
        time = self.time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        text = self.task_edit.toPlainText().strip()

        if not text:
            self.show_status("Ошибка: Введите описание дела!", "red")
            return

        task = Task(
            id=None,
            time=time,
            text=text,
            created_at=QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        )

        try:
            task_id = self.db_manager.add_task(task)
            self.show_status(f"Успех: Дело с ID {task_id} добавлено!", "green")
            self.clear_form()
            self.task_created.emit()
        except Exception as e:
            self.show_status(f"Ошибка: Не удалось добавить дело - {str(e)}", "red")

    def show_status(self, message, color):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def clear_form(self):
        self.task_edit.clear()
        self.time_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))


class ViewTasksTab(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Мои дела")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        control_layout = QHBoxLayout()

        delete_layout = QVBoxLayout()
        delete_label = QLabel("Удалить дело по ID:")
        self.delete_edit = QLineEdit()
        self.delete_edit.setPlaceholderText("Введите ID дела...")
        delete_btn = QPushButton("Удалить дело")
        delete_btn.clicked.connect(self.delete_task)

        delete_layout.addWidget(delete_label)
        delete_layout.addWidget(self.delete_edit)
        delete_layout.addWidget(delete_btn)

        refresh_btn = QPushButton("Обновить список")
        refresh_btn.clicked.connect(self.load_tasks)

        control_layout.addLayout(delete_layout)
        control_layout.addStretch()
        control_layout.addWidget(refresh_btn)

        layout.addLayout(control_layout)

        tasks_label = QLabel("Текущие дела:")
        tasks_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(tasks_label)

        self.tasks_list = QListWidget()
        layout.addWidget(self.tasks_list)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def load_tasks(self):
        self.tasks_list.clear()
        tasks = self.db_manager.get_all_tasks()

        if not tasks:
            self.status_label.setText("Нет активных дел")
            self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        else:
            self.status_label.setText(f"Найдено дел: {len(tasks)}")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")

        for task in tasks:
            item = QListWidgetItem()
            widget = TaskItemWidget(task)
            item.setSizeHint(widget.sizeHint())
            self.tasks_list.addItem(item)
            self.tasks_list.setItemWidget(item, widget)

    def delete_task(self):
        task_id_text = self.delete_edit.text().strip()

        if not task_id_text:
            self.show_status("Ошибка: Введите ID дела для удаления!", "red")
            return

        try:
            task_id = int(task_id_text)
        except ValueError:
            self.show_status("Ошибка: ID должен быть числом!", "red")
            return

        if self.db_manager.delete_task(task_id):
            self.show_status(f"Успех: Дело с ID {task_id} удалено!", "green")
            self.delete_edit.clear()
            self.load_tasks()
        else:
            self.show_status(f"Ошибка: Дело с ID {task_id} не найдено!", "red")

    def show_status(self, message, color):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")