import json
import os
import datetime
from model.incident import Incident
from model.location import Location

class IncidentRepository:
    def __init__(self):
        self.incidents = []
        self.next_id = 1
        self.data_file = "data/incidents.json"
        self.load_data()

    def load_data(self):
        """Загрузка данных из JSON файла"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for incident_data in data:
                        # Создаем объект Location
                        location_data = incident_data['location']
                        location = Location(
                            location_data['latitude'],
                            location_data['longitude'], 
                            location_data['address'],
                            location_data['description']
                        )
                        
                        # Создаем объект Incident
                        incident = Incident(
                            incident_data['incident_type'],
                            incident_data['date_time'],
                            location,
                            incident_data['description'],
                            incident_data['priority'],
                            incident_data.get('created_by')
                        )
                        
                        # Восстанавливаем остальные поля
                        incident.id = incident_data['id']
                        incident.status = incident_data['status']
                        incident.created_date = incident_data['created_date']
                        incident.extensions = incident_data.get('extensions', [])
                        incident.cause_analysis = incident_data.get('cause_analysis')
                        incident.documentation = incident_data.get('documentation')
                        incident.archived = incident_data.get('archived', False)
                        incident.archived_date = incident_data.get('archived_date')
                        
                        self.incidents.append(incident)
                        if incident.id >= self.next_id:
                            self.next_id = incident.id + 1
                            
                print(f"Загружено {len(self.incidents)} происшествий из файла")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")

    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            incidents_data = []
            for incident in self.incidents:
                incident_data = {
                    'id': incident.id,
                    'incident_type': incident.incident_type,
                    'date_time': incident.date_time,
                    'location': {
                        'address': incident.location.address,
                        'latitude': incident.location.latitude,
                        'longitude': incident.location.longitude,
                        'description': incident.location.description
                    },
                    'description': incident.description,
                    'priority': incident.priority,
                    'status': incident.status,
                    'created_by': incident.created_by,
                    'created_date': incident.created_date,
                    'extensions': incident.extensions,
                    'cause_analysis': incident.cause_analysis,
                    'documentation': incident.documentation,
                    'archived': incident.archived,
                    'archived_date': incident.archived_date
                }
                incidents_data.append(incident_data)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(incidents_data, f, ensure_ascii=False, indent=2)
            print(f"Сохранено {len(self.incidents)} происшествий в файл")
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def add_incident(self, incident):
        incident.id = self.next_id
        self.incidents.append(incident)
        self.next_id += 1
        print(f"Добавлен инцидент с ID: {incident.id}, всего инцидентов: {len(self.incidents)}")
        self.save_data()
        return incident

    def get_incident_by_id(self, incident_id):
        for incident in self.incidents:
            if incident.id == incident_id:
                return incident
        return None

    def get_all_incidents(self):
        return self.incidents

    def update_incident(self, incident):
        for i, existing_incident in enumerate(self.incidents):
            if existing_incident.id == incident.id:
                self.incidents[i] = incident
                self.save_data()
                return True
        return False

    def delete_incident(self, incident_id):
        initial_count = len(self.incidents)
        self.incidents = [incident for incident in self.incidents if incident.id != incident_id]
        if len(self.incidents) < initial_count:
            self.save_data()
            return True
        return False

    def get_incidents_by_status(self, status):
        return [incident for incident in self.incidents if incident.status == status]

    def get_archived_incidents(self):
        return [incident for incident in self.incidents if incident.archived]

    def get_recent_incidents(self, days=7):
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        recent_incidents = []
        for incident in self.incidents:
            incident_date = datetime.datetime.fromisoformat(incident.created_date)
            if incident_date > cutoff_date:
                recent_incidents.append(incident)
        return recent_incidents