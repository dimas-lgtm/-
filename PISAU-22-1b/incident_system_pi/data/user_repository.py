from model.user import User
import datetime

class UserRepository:
    def __init__(self):
        self.users = []
        self.next_id = 1
        # Добавляем пользователей по ролям
        self.add_user("admin", "admin123", "Администратор Системы", "administrator", "admin@system.com")
        self.add_user("manager", "manager123", "Менеджер Проекта", "manager", "manager@system.com")
        self.add_user("user", "user123", "Пользователь Системы", "user", "user@system.com")

    def add_user(self, username, password, full_name, role, email="", phone=""):
        user = User(username, password, full_name, role, email, phone)
        user.id = self.next_id
        self.users.append(user)
        self.next_id += 1
        return user

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def get_users_by_role(self, role):
        return [user for user in self.users if user.role == role]

    def update_user(self, user):
        for i, existing_user in enumerate(self.users):
            if existing_user.id == user.id:
                self.users[i] = user
                return True
        return False

    def delete_user(self, user_id):
        self.users = [user for user in self.users if user.id != user_id]
        return True