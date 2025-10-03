import datetime

class Incident:
    def __init__(self, incident_type, date_time, location, description, priority, created_by=None):
        self.incident_type = incident_type
        self.date_time = date_time
        self.location = location
        self.description = description
        self.priority = priority
        self.status = "Зарегистрировано"
        self.media_files = []
        self.responsible_user = None
        self.id = None
        self.created_by = created_by
        self.created_date = datetime.datetime.now().isoformat()
        self.extensions = []
        self.cause_analysis = None
        self.documentation = None
        self.archived = False
        self.archived_date = None

    def __str__(self):
        return f"Incident(id={self.id}, type={self.incident_type}, date={self.date_time})"

    def add_media_file(self, media_file):
        self.media_files.append(media_file)

    def set_responsible_user(self, user):
        self.responsible_user = user

    def change_status(self, new_status):
        self.status = new_status

    def extend_incident(self, additional_info):
        """Расширение информации о происшествии"""
        self.extensions.append({
            'date': datetime.datetime.now().isoformat(),
            'info': additional_info
        })

    def analyze_cause(self, cause, root_cause):
        """Анализ причины возникновения"""
        self.cause_analysis = {
            'cause': cause,
            'root_cause': root_cause,
            'analyzed_date': datetime.datetime.now().isoformat()
        }

    def document_results(self, results):
        """Документирование результатов"""
        self.documentation = results
        self.documented_date = datetime.datetime.now().isoformat()

    def archive_incident(self):
        """Архивация и закрытие запроса"""
        self.status = 'closed'
        self.archived = True
        self.archived_date = datetime.datetime.now().isoformat()