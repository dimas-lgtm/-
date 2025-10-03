import datetime

class User:
    def __init__(self, username, password, full_name, role, email="", phone=""):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.role = role
        self.email = email
        self.phone = phone
        self.id = None
        self.created_date = datetime.datetime.now().isoformat()
        self.is_active = True

    def __str__(self):
        return f"User(id={self.id}, username={self.username}, role={self.role})"

    def change_password(self, new_password):
        self.password = new_password

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def has_permission(self, permission):
        """Проверка прав пользователя"""
        permissions = {
            'user': ['create_incident', 'view_own_incidents'],
            'manager': ['create_incident', 'view_all_incidents', 'analyze_cause', 'document_results', 'archive_incident'],
            'administrator': ['create_incident', 'view_all_incidents', 'analyze_cause', 'document_results', 
                            'archive_incident', 'delete_incident', 'system_administration']
        }
        return permission in permissions.get(self.role, [])