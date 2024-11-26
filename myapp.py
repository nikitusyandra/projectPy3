import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer


class FactoryGame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db_name = "game_data.db"
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

        self.create_table()

        self.load_game_data()

        self.setWindowTitle("Фабрика монет")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.coins_label = QLabel(f"Монеты: {self.coins}", self)
        self.coins_label.setAlignment(Qt.AlignCenter)
        self.coins_label.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.coins_label)

        self.click_button = QPushButton("Произвести монеты", self)
        self.click_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.click_button.clicked.connect(self.produce_coin)
        self.layout.addWidget(self.click_button)

        self.worker_label = QLabel(f"Рабочие: {self.worker_count} (производят {self.worker_count * self.coins_per_worker} монет/сек)", self)
        self.worker_label.setAlignment(Qt.AlignCenter)
        self.worker_label.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.worker_label)

        self.hire_button = QPushButton(f"Нанять рабочего - {self.worker_cost} монет", self)
        self.hire_button.setStyleSheet("font-size: 16px; padding: 8px;")
        self.hire_button.clicked.connect(self.hire_worker)
        self.layout.addWidget(self.hire_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_produce)
        self.timer.start(1000)  

    def create_table(self):
        """Создание таблицы в базе данных."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coins INTEGER NOT NULL,
                worker_count INTEGER NOT NULL,
                worker_cost INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def load_game_data(self):
        """Загрузка данных из базы данных."""
        self.cursor.execute("SELECT coins, worker_count, worker_cost FROM game_data WHERE id = 1")
        data = self.cursor.fetchone()

        if data:
            self.coins, self.worker_count, self.worker_cost = data
        else:
            self.coins = 0
            self.worker_count = 0
            self.worker_cost = 50
            self.save_game_data()

        self.coins_per_worker = 1

    def save_game_data(self):
        """Сохранение данных в базу данных."""
        self.cursor.execute("""
            INSERT OR REPLACE INTO game_data (id, coins, worker_count, worker_cost)
            VALUES (1, ?, ?, ?)
        """, (self.coins, self.worker_count, self.worker_cost))
        self.connection.commit()

    def produce_coin(self):
        """Производство монет при нажатии кнопки."""
        self.coins += 1
        self.update_ui()

    def hire_worker(self):
        """Найм рабочего."""
        if self.coins >= self.worker_cost:
            self.coins -= self.worker_cost
            self.worker_count += 1
            self.worker_cost = int(self.worker_cost * 1.5)  
            self.update_ui()

    def auto_produce(self):
        """Автоматическое производство монет рабочими."""
        self.coins += self.worker_count * self.coins_per_worker
        self.update_ui()

    def update_ui(self):
        """Обновление интерфейса."""
        self.coins_label.setText(f"Монеты: {self.coins}")
        self.worker_label.setText(f"Рабочие: {self.worker_count} (производят {self.worker_count * self.coins_per_worker} монет/сек)")
        self.hire_button.setText(f"Нанять рабочего - {self.worker_cost} монет")
        self.save_game_data()

    def closeEvent(self, event):
        """Событие при закрытии приложения."""
        self.save_game_data()
        self.connection.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])

    window = FactoryGame()
    window.show()

    app.exec()
