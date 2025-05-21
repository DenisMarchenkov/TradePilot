import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox
)

API_URL = "http://127.0.0.1:8000"

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM - Клиенты")
        self.init_ui()
        self.get_clients()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поля для ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя клиента")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email клиента")

        # Кнопки
        add_button = QPushButton("Добавить клиента")
        add_button.clicked.connect(self.add_client)

        refresh_button = QPushButton("Обновить список")
        refresh_button.clicked.connect(self.get_clients)

        # Поле вывода
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)

        # Компоновка
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(refresh_button)
        layout.addLayout(buttons_layout)

        layout.addWidget(QLabel("Клиенты:"))
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def add_client(self):
        name = self.name_input.text()
        email = self.email_input.text()
        if not name or not email:
            QMessageBox.warning(self, "Внимание", "Заполните имя и email")
            return

        try:
            response = requests.post(f"{API_URL}/clients", json={"name": name, "email": email})
            response.raise_for_status()
            QMessageBox.information(self, "Успешно", "Клиент добавлен")
            self.get_clients()
            self.name_input.clear()
            self.email_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def get_clients(self):
        try:
            response = requests.get(f"{API_URL}/clients")
            response.raise_for_status()
            clients = response.json()
            self.result_area.clear()
            for client in clients:
                self.result_area.append(f"{client['id']}: {client['name']} - {client['email']}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при получении данных", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
