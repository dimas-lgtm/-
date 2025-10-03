from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QHBoxLayout, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class LoginDialog(QDialog):
    def __init__(self, user_repository, parent=None):
        super().__init__(parent)
        self.user_repository = user_repository
        self.setWindowTitle("Вход в систему PIPIPUPUCHECK")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(400, 300)
        
        # Устанавливаем стиль
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                margin-bottom: 5px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QComboBox {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        title_label = QLabel("Добро пожаловать в систему управления происшествиями")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 30px;")
        self.layout.addWidget(title_label)

        # Поле для имени пользователя
        username_layout = QVBoxLayout()
        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя пользователя")
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_input)
        self.layout.addLayout(username_layout)

        # Поле для пароля
        password_layout = QVBoxLayout()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)
        self.layout.addLayout(password_layout)

        # Быстрый выбор пользователей (для тестирования)
        quick_login_layout = QVBoxLayout()
        quick_login_label = QLabel("Быстрый вход (для тестирования):")
        self.quick_login_combo = QComboBox()
        self.quick_login_combo.addItems(["Выберите пользователя...", "admin (Администратор)", "manager (Менеджер)", "user (Пользователь)"])
        self.quick_login_combo.currentTextChanged.connect(self.on_quick_login_changed)
        quick_login_layout.addWidget(quick_login_label)
        quick_login_layout.addWidget(self.quick_login_combo)
        self.layout.addLayout(quick_login_layout)

        # Кнопка входа
        self.login_button = QPushButton("Войти в систему")
        self.login_button.clicked.connect(self.attempt_login)
        
        # Обработка нажатия Enter
        self.username_input.returnPressed.connect(self.attempt_login)
        self.password_input.returnPressed.connect(self.attempt_login)
        
        self.layout.addWidget(self.login_button)

        # Информация о тестовых пользователях
        info_label = QLabel(
            "Тестовые пользователи:\n"
            "• admin / admin123 - Администратор\n"
            "• manager / manager123 - Менеджер\n" 
            "• user / user123 - Пользователь"
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #7f8c8d; font-size: 12px; margin-top: 20px;")
        info_label.setWordWrap(True)
        self.layout.addWidget(info_label)

    def on_quick_login_changed(self, text):
        """Обработка быстрого выбора пользователя"""
        if text == "admin (Администратор)":
            self.username_input.setText("admin")
            self.password_input.setText("admin123")
        elif text == "manager (Менеджер)":
            self.username_input.setText("manager")
            self.password_input.setText("manager123")
        elif text == "user (Пользователь)":
            self.username_input.setText("user")
            self.password_input.setText("user123")

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, заполните все поля.")
            return

        user = self.user_repository.get_user_by_username(username)

        if user and user.password == password:
            if not user.is_active:
                QMessageBox.warning(self, "Аккаунт заблокирован", "Ваш аккаунт временно заблокирован.")
                return
                
            QMessageBox.information(self, "Вход выполнен", 
                                  f"Добро пожаловать, {user.full_name}!\n"
                                  f"Роль: {self.get_role_display_name(user.role)}")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка входа", 
                              "Неверное имя пользователя или пароль.\n\n"
                              "Доступные тестовые пользователи:\n"
                              "• admin / admin123\n"
                              "• manager / manager123\n"
                              "• user / user123")
            self.password_input.clear()
            self.password_input.setFocus()

    def get_role_display_name(self, role):
        """Получить отображаемое название роли"""
        role_names = {
            'administrator': 'Администратор',
            'manager': 'Менеджер',
            'user': 'Пользователь'
        }
        return role_names.get(role, role)

    def get_username(self):
        return self.username_input.text()