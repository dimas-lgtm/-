import sys
import json
import datetime
from typing import List, Dict, Optional
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from logic.incident_manager import IncidentManager
from data.incident_repository import IncidentRepository
from data.user_repository import UserRepository

def main():
    app = QApplication(sys.argv)
    
    # Инициализация репозиториев
    user_repository = UserRepository()
    incident_repository = IncidentRepository()
    incident_manager = IncidentManager(incident_repository)
    
    # Показ диалога входа
    login_dialog = LoginDialog(user_repository)
    
    if login_dialog.exec_() == LoginDialog.Accepted:
        username = login_dialog.get_username()
        current_user = user_repository.get_user_by_username(username)
        
        # Запуск главного окна с передачей менеджера и текущего пользователя
        main_window = MainWindow(incident_manager, current_user)
        main_window.show()
        
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()