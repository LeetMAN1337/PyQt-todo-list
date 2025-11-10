from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QMessageBox
from PyQt6.QtCore import Qt, QDateTime, QTimer
from PyQt6.QtGui import QFont

from database import DatabaseManager
from tabs.task_tabs import CreateTaskTab, ViewTasksTab
from widgets import AdviceTab, ClickerGameTab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setup_ui()
        self.setup_timers()

    def setup_ui(self):
        self.setWindowTitle("Список дел - Умный планировщик")
        self.setFixedSize(900, 700)

        main_layout = QVBoxLayout()

        title = QLabel("🗓️ Умный Планировщик Дел")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 10px;")
        main_layout.addWidget(title)

        self.tabs = QTabWidget()

        self.view_tasks_tab = ViewTasksTab(self.db_manager)
        self.tabs.addTab(self.view_tasks_tab, "📋 Мои дела")

        self.create_task_tab = CreateTaskTab(self.db_manager)
        self.create_task_tab.task_created.connect(self.on_task_created)
        self.tabs.addTab(self.create_task_tab, "➕ Создать дело")

        self.advice_tab = AdviceTab()
        self.tabs.addTab(self.advice_tab, "💡 Советы")

        self.clicker_tab = ClickerGameTab()
        self.tabs.addTab(self.clicker_tab, "🎮 Кликер")

        main_layout.addWidget(self.tabs)

        self.status_label = QLabel("Готов к работе")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("background-color: #ecf0f1; padding: 5px;")
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def setup_timers(self):
        self.reminder_timer = QTimer()
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(60000)

        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self.cleanup_completed_tasks)
        self.cleanup_timer.start(60000)

    def on_task_created(self):
        self.tabs.setCurrentIndex(0)
        self.view_tasks_tab.load_tasks()
        self.status_label.setText("Новое дело успешно добавлено!")

    def check_reminders(self):
        current_time = QDateTime.currentDateTime()
        tasks = self.db_manager.get_all_tasks()

        for task in tasks:
            task_time = QDateTime.fromString(task.time, "yyyy-MM-dd HH:mm:ss")
            if not task_time.isValid():
                continue

            time_diff = current_time.secsTo(task_time) / 60

            if 25 <= time_diff <= 35:
                self.show_reminder(task)

    def show_reminder(self, task):
        msg = QMessageBox(self)
        msg.setWindowTitle("⏰ Напоминание о деле")
        msg.setText(f"Скоро наступит время для выполнения дела!\n\n"
                    f"📝 {task.text}\n"
                    f"⏰ Время: {task.time}\n\n"
                    f"У вас есть около 30 минут чтобы подготовиться!")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def cleanup_completed_tasks(self):
        current_time = QDateTime.currentDateTime()
        tasks = self.db_manager.get_all_tasks()
        deleted_count = 0

        for task in tasks:
            task_time = QDateTime.fromString(task.time, "yyyy-MM-dd HH:mm:ss")
            if not task_time.isValid():
                continue

            time_diff = current_time.secsTo(task_time) / 60

            if time_diff < -5:
                if self.db_manager.delete_task(task.id):
                    deleted_count += 1

        if deleted_count > 0:
            self.view_tasks_tab.load_tasks()
            self.status_label.setText(f"Автоматически удалено {deleted_count} завершенных дел")