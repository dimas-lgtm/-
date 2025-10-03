import os
import sys

# Простой путь к проекту
sys.path.append('..')

from data.user_repository import UserRepository
from logic.incident_manager import IncidentManager
from data.incident_repository import IncidentRepository
from model.location import Location


def test_basics():
    """Минимальный тест основных функций"""
    print("🚀 Запуск быстрого теста...")
    
    # 1. Тест пользователей
    print("1. Проверяем пользователей...")
    user_repo = UserRepository()
    
    admin = user_repo.get_user_by_username("admin")
    if admin and admin.password == "admin123":
        print("   ✅ Админ работает")
    else:
        print("   ❌ Проблема с админом")
        return False
    
    # 2. Тест происшествий
    print("2. Проверяем происшествия...")
    incident_repo = IncidentRepository()
    incident_manager = IncidentManager(incident_repo)
    
    # Создаем тестовое происшествие
    location = Location(55.7558, 37.6173, "Тестовое место")
    incident = incident_manager.register_incident(
        "Тестовый сбой",
        "2024-01-15 12:00:00", 
        location,
        "Это тестовое происшествие",
        "Низкий",
        "test_user"
    )
    
    if incident and incident.id:
        print("   ✅ Создание происшествия работает")
    else:
        print("   ❌ Не удалось создать происшествие")
        return False
    
    # 3. Проверяем поиск
    found_incident = incident_manager.get_incident_by_id(incident.id)
    if found_incident and found_incident.id == incident.id:
        print("   ✅ Поиск по ID работает")
    else:
        print("   ❌ Поиск по ID не работает")
        return False
    
    # 4. Проверяем получение всех происшествий
    all_incidents = incident_manager.get_all_incidents()
    if len(all_incidents) > 0:
        print("   ✅ Получение всех происшествий работает")
    else:
        print("   ❌ Нет происшествий в списке")
        return False
    
    # 5. Быстрая проверка архивации
    if incident_manager.archive_incident(incident.id):
        print("   ✅ Архивация работает")
    else:
        print("   ❌ Архивация не работает")
        return False
    
    return True


def test_stats():
    """Тест статистики"""
    print("3. Проверяем статистику...")
    
    incident_repo = IncidentRepository()
    incident_manager = IncidentManager(incident_repo)
    
    stats = incident_manager.view_reports_statistics()
    
    if 'total_incidents' in stats and 'open_incidents' in stats:
        print("   ✅ Статистика работает")
        print(f"   📊 Всего: {stats['total_incidents']}, Открытых: {stats['open_incidents']}")
        return True
    else:
        print("   ❌ Статистика не работает")
        return False


if __name__ == "__main__":
    print("=" * 50)
    
    test1_passed = test_basics()
    test2_passed = test_stats()
    
    print("=" * 50)
    
    if test1_passed and test2_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Программа работает нормально.")
    else:
        print("💥 Есть проблемы в программе!")
        sys.exit(1)