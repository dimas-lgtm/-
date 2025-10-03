from data.incident_repository import IncidentRepository
from model.incident import Incident
import datetime
from typing import List, Dict

class IncidentManager:
    def __init__(self, incident_repository):
        self.incident_repository = incident_repository

    def register_incident(self, incident_type, date_time, location, description, priority, created_by=None):
        incident = Incident(incident_type, date_time, location, description, priority, created_by)
        return self.incident_repository.add_incident(incident)

    def get_incident_by_id(self, incident_id):
        return self.incident_repository.get_incident_by_id(incident_id)

    def get_all_incidents(self):
        return self.incident_repository.get_all_incidents()

    def update_incident(self, incident):
        return self.incident_repository.update_incident(incident)

    def delete_incident(self, incident_id):
        return self.incident_repository.delete_incident(incident_id)

    def extend_incident(self, incident_id, additional_info):
        """Расширение информации о происшествии"""
        incident = self.get_incident_by_id(incident_id)
        if incident:
            incident.extend_incident(additional_info)
            return self.update_incident(incident)
        return False

    def analyze_cause(self, incident_id, cause, root_cause):
        """Анализ причины возникновения"""
        incident = self.get_incident_by_id(incident_id)
        if incident:
            incident.analyze_cause(cause, root_cause)
            return self.update_incident(incident)
        return False

    def document_results(self, incident_id, results):
        """Документирование результатов"""
        incident = self.get_incident_by_id(incident_id)
        if incident:
            incident.document_results(results)
            return self.update_incident(incident)
        return False

    def archive_incident(self, incident_id):
        """Архивация и закрытие запроса"""
        incident = self.get_incident_by_id(incident_id)
        if incident:
            incident.archive_incident()
            return self.update_incident(incident)
        return False

    def get_incidents_by_date(self, start_date, end_date):
        """Поиск по датам"""
        try:
            start = datetime.datetime.fromisoformat(start_date)
            end = datetime.datetime.fromisoformat(end_date)
            
            result = []
            for incident in self.get_all_incidents():
                inc_date = datetime.datetime.fromisoformat(incident.created_date)
                if start <= inc_date <= end:
                    result.append(incident)
            
            return result
        except ValueError:
            return []

    def view_reports_statistics(self):
        """Просмотр отчетов и статистики"""
        incidents = self.get_all_incidents()
        total = len(incidents)
        open_count = len([i for i in incidents if i.status == 'Зарегистрировано'])
        closed_count = len([i for i in incidents if i.status == 'closed'])
        archived_count = len([i for i in incidents if i.archived])
        
        # Статистика по типам
        type_stats = {}
        for incident in incidents:
            inc_type = incident.incident_type
            type_stats[inc_type] = type_stats.get(inc_type, 0) + 1
        
        return {
            'total_incidents': total,
            'open_incidents': open_count,
            'closed_incidents': closed_count,
            'archived_incidents': archived_count,
            'type_statistics': type_stats
        }

    def get_my_incidents(self, username):
        """Получение происшествий текущего пользователя"""
        return [incident for incident in self.get_all_incidents() if incident.created_by == username]