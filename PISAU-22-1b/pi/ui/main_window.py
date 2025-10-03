import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QFormLayout, QLineEdit, QComboBox, QMessageBox,
                             QHBoxLayout, QGridLayout, QTabWidget, QTextEdit, QDateEdit,
                             QGroupBox)
from PyQt5.QtCore import Qt, QDate
from model.incident import Incident
from model.location import Location


class IncidentForm(QDialog):
    def __init__(self, incident_manager, current_user, incident=None, parent=None):
        super().__init__(parent)
        self.incident_manager = incident_manager
        self.current_user = current_user
        self.incident = incident
        self.setWindowTitle("Регистрация происшествия")
        self.layout = QFormLayout(self)

        self.type_input = QLineEdit()
        self.date_input = QLineEdit()
        self.location_input = QLineEdit()
        self.description_input = QLineEdit()
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Низкий", "Средний", "Высокий", "Критический"])

        if self.incident:
            self.type_input.setText(self.incident.incident_type)
            self.date_input.setText(self.incident.date_time)
            self.location_input.setText(self.incident.location.address)
            self.description_input.setText(self.incident.description)
            self.priority_combo.setCurrentText(self.incident.priority)
            self.setWindowTitle("Редактирование происшествия")

        self.layout.addRow("Тип:", self.type_input)
        self.layout.addRow("Дата:", self.date_input)
        self.layout.addRow("Местоположение:", self.location_input)
        self.layout.addRow("Описание:", self.description_input)
        self.layout.addRow("Приоритет:", self.priority_combo)

        self.submit_button = QPushButton("Регистрация" if not self.incident else "Сохранить")
        self.submit_button.clicked.connect(self.submit_form)
        self.layout.addRow(self.submit_button)

    def submit_form(self):
        incident_type = self.type_input.text()
        date_time = self.date_input.text()
        location_str = self.location_input.text()
        description = self.description_input.text()
        priority = self.priority_combo.currentText()

        location = Location(0.0, 0.0, location_str)

        if self.incident:
            self.incident.incident_type = incident_type
            self.incident.date_time = date_time
            self.incident.location = location
            self.incident.description = description
            self.incident.priority = priority

            if self.incident_manager.update_incident(self.incident):
                QMessageBox.information(self, "Успех", "Происшествие успешно обновлено!")
                self.accept()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось обновить происшествие.")
        else:
            incident = self.incident_manager.register_incident(
                incident_type, date_time, location, description, priority, self.current_user.username
            )

            if incident:
                QMessageBox.information(self, "Успех", "Происшествие успешно зарегистрировано!")
                self.accept()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось зарегистрировать происшествие.")


class ExtendIncidentDialog(QDialog):
    def __init__(self, incident_manager, incident_id, parent=None):
        super().__init__(parent)
        self.incident_manager = incident_manager
        self.incident_id = incident_id
        self.setWindowTitle("Расширение информации о происшествии")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        self.info_input = QTextEdit()
        self.info_input.setPlaceholderText("Введите дополнительную информацию...")
        layout.addWidget(QLabel("Дополнительная информация:"))
        layout.addWidget(self.info_input)
        
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        
        self.submit_button.clicked.connect(self.submit_extension)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def submit_extension(self):
        additional_info = self.info_input.toPlainText()
        if additional_info.strip():
            if self.incident_manager.extend_incident(self.incident_id, additional_info):
                QMessageBox.information(self, "Успех", "Информация успешно расширена!")
                self.accept()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось расширить информацию.")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите дополнительную информацию.")


class CauseAnalysisDialog(QDialog):
    def __init__(self, incident_manager, incident_id, parent=None):
        super().__init__(parent)
        self.incident_manager = incident_manager
        self.incident_id = incident_id
        self.setWindowTitle("Анализ причин возникновения")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        self.cause_input = QTextEdit()
        self.cause_input.setMaximumHeight(100)
        self.root_cause_input = QTextEdit()
        self.root_cause_input.setMaximumHeight(100)
        
        layout.addRow("Причина:", self.cause_input)
        layout.addRow("Корневая причина:", self.root_cause_input)
        
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Сохранить анализ")
        self.cancel_button = QPushButton("Отмена")
        
        self.submit_button.clicked.connect(self.submit_analysis)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        layout.addRow(button_layout)

    def submit_analysis(self):
        cause = self.cause_input.toPlainText()
        root_cause = self.root_cause_input.toPlainText()
        
        if cause.strip() and root_cause.strip():
            if self.incident_manager.analyze_cause(self.incident_id, cause, root_cause):
                QMessageBox.information(self, "Успех", "Анализ причин сохранен!")
                self.accept()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось сохранить анализ.")
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")


class DocumentResultsDialog(QDialog):
    def __init__(self, incident_manager, incident_id, parent=None):
        super().__init__(parent)
        self.incident_manager = incident_manager
        self.incident_id = incident_id
        self.setWindowTitle("Документирование результатов")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        self.results_input = QTextEdit()
        self.results_input.setPlaceholderText("Введите результаты документирования...")
        layout.addWidget(QLabel("Результаты документирования:"))
        layout.addWidget(self.results_input)
        
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        
        self.submit_button.clicked.connect(self.submit_documentation)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def submit_documentation(self):
        results = self.results_input.toPlainText()
        if results.strip():
            if self.incident_manager.document_results(self.incident_id, results):
                QMessageBox.information(self, "Успех", "Результаты документированы!")
                self.accept()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось сохранить результаты.")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите результаты документирования.")


class DateSearchDialog(QDialog):
    def __init__(self, incident_manager, parent=None):
        super().__init__(parent)
        self.incident_manager = incident_manager
        self.setWindowTitle("Поиск по датам")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        layout.addRow("Начальная дата:", self.start_date)
        layout.addRow("Конечная дата:", self.end_date)
        
        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.perform_search)
        layout.addRow(self.search_button)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels(["ID", "Тип", "Дата", "Местоположение", "Описание", "Приоритет"])
        layout.addRow(self.results_table)

    def perform_search(self):
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        
        incidents = self.incident_manager.get_incidents_by_date(start_date, end_date)
        self.results_table.setRowCount(len(incidents))
        
        for row, incident in enumerate(incidents):
            self.results_table.setItem(row, 0, QTableWidgetItem(str(incident.id)))
            self.results_table.setItem(row, 1, QTableWidgetItem(incident.incident_type))
            self.results_table.setItem(row, 2, QTableWidgetItem(incident.date_time))
            self.results_table.setItem(row, 3, QTableWidgetItem(incident.location.address))
            self.results_table.setItem(row, 4, QTableWidgetItem(incident.description))
            self.results_table.setItem(row, 5, QTableWidgetItem(incident.priority))


class StatisticsDialog(QDialog):
    def __init__(self, incident_manager, parent=None):
        super().__init__(parent)
        self.incident_manager = incident_manager
        self.setWindowTitle("Отчеты и статистика")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        stats = self.incident_manager.view_reports_statistics()
        
        # Общая статистика
        general_group = QGroupBox("Общая статистика")
        general_layout = QGridLayout()
        
        general_layout.addWidget(QLabel("Всего происшествий:"), 0, 0)
        general_layout.addWidget(QLabel(str(stats['total_incidents'])), 0, 1)
        
        general_layout.addWidget(QLabel("Открытых:"), 1, 0)
        general_layout.addWidget(QLabel(str(stats['open_incidents'])), 1, 1)
        
        general_layout.addWidget(QLabel("Закрытых:"), 2, 0)
        general_layout.addWidget(QLabel(str(stats['closed_incidents'])), 2, 1)
        
        general_layout.addWidget(QLabel("Архивированных:"), 3, 0)
        general_layout.addWidget(QLabel(str(stats['archived_incidents'])), 3, 1)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # Статистика по типам
        type_group = QGroupBox("Статистика по типам происшествий")
        type_layout = QVBoxLayout()
        
        for inc_type, count in stats['type_statistics'].items():
            type_layout.addWidget(QLabel(f"{inc_type}: {count}"))
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)


class MainWindow(QWidget):
    def __init__(self, incident_manager, current_user):
        super().__init__()
        self.incident_manager = incident_manager
        self.current_user = current_user
        self.setWindowTitle(f"Система управления происшествиями - {current_user.username} ({current_user.role})")
        self.setGeometry(100, 100, 1000, 700)

        self.layout = QVBoxLayout(self)

        # Создаем вкладки
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Вкладка управления происшествиями
        self.incident_tab = QWidget()
        self.setup_incident_tab()
        self.tab_widget.addTab(self.incident_tab, "Управление происшествиями")

        # Вкладка отчетов
        self.reports_tab = QWidget()
        self.setup_reports_tab()
        self.tab_widget.addTab(self.reports_tab, "Отчеты и статистика")

        self.load_incidents()

    def setup_incident_tab(self):
        layout = QVBoxLayout(self.incident_tab)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.add_incident_button = QPushButton("Зарегистрировать новое происшествие")
        self.add_incident_button.clicked.connect(self.open_incident_form)
        button_layout.addWidget(self.add_incident_button)

        self.edit_incident_button = QPushButton("Редактировать")
        self.edit_incident_button.clicked.connect(self.edit_incident)
        self.edit_incident_button.setEnabled(False)
        button_layout.addWidget(self.edit_incident_button)

        self.delete_incident_button = QPushButton("Удалить")
        self.delete_incident_button.clicked.connect(self.delete_incident)
        self.delete_incident_button.setEnabled(False)
        button_layout.addWidget(self.delete_incident_button)

        # Новые кнопки по схеме
        self.extend_button = QPushButton("Расширить информацию")
        self.extend_button.clicked.connect(self.extend_incident)
        self.extend_button.setEnabled(False)
        button_layout.addWidget(self.extend_button)

        self.analyze_button = QPushButton("Анализ причин")
        self.analyze_button.clicked.connect(self.analyze_cause)
        self.analyze_button.setEnabled(False)
        button_layout.addWidget(self.analyze_button)

        self.document_button = QPushButton("Документировать")
        self.document_button.clicked.connect(self.document_results)
        self.document_button.setEnabled(False)
        button_layout.addWidget(self.document_button)

        self.archive_button = QPushButton("Архивировать")
        self.archive_button.clicked.connect(self.archive_incident)
        self.archive_button.setEnabled(False)
        button_layout.addWidget(self.archive_button)

        layout.addLayout(button_layout)

        # Таблица происшествий
        self.incident_table = QTableWidget()
        self.incident_table.setColumnCount(8)
        self.incident_table.setHorizontalHeaderLabels(["ID", "Тип", "Дата", "Местоположение", "Описание", "Приоритет", "Статус", "Создал"])
        layout.addWidget(self.incident_table)
        self.incident_table.itemSelectionChanged.connect(self.on_incident_selected)

    def setup_reports_tab(self):
        layout = QVBoxLayout(self.reports_tab)

        # Кнопки отчетов
        reports_button_layout = QHBoxLayout()

        self.stats_button = QPushButton("Просмотр статистики")
        self.stats_button.clicked.connect(self.show_statistics)
        reports_button_layout.addWidget(self.stats_button)

        self.date_search_button = QPushButton("Поиск по датам")
        self.date_search_button.clicked.connect(self.search_by_date)
        reports_button_layout.addWidget(self.date_search_button)

        self.my_incidents_button = QPushButton("Мои происшествия")
        self.my_incidents_button.clicked.connect(self.show_my_incidents)
        reports_button_layout.addWidget(self.my_incidents_button)

        layout.addLayout(reports_button_layout)

        # Таблица для отчетов
        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(8)
        self.reports_table.setHorizontalHeaderLabels(["ID", "Тип", "Дата", "Местоположение", "Описание", "Приоритет", "Статус", "Создал"])
        layout.addWidget(self.reports_table)

    def open_incident_form(self):
        form = IncidentForm(self.incident_manager, self.current_user, None, self)
        result = form.exec_()
        if result == QDialog.Accepted:
            self.load_incidents()

    def edit_incident(self):
        selected_row = self.incident_table.currentRow()
        if selected_row >= 0:
            incident_id = int(self.incident_table.item(selected_row, 0).text())
            incident = self.incident_manager.get_incident_by_id(incident_id)
            if incident:
                form = IncidentForm(self.incident_manager, self.current_user, incident, self)
                result = form.exec_()
                if result == QDialog.Accepted:
                    self.load_incidents()
            else:
                QMessageBox.critical(self, "Ошибка", "Происшествие не найдено")

    def delete_incident(self):
        selected_row = self.incident_table.currentRow()
        if selected_row >= 0:
            incident_id = int(self.incident_table.item(selected_row, 0).text())
            reply = QMessageBox.question(self, 'Удаление', "Вы уверены, что хотите удалить это происшествие?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.incident_manager.delete_incident(incident_id)
                self.load_incidents()

    def extend_incident(self):
        selected_row = self.incident_table.currentRow()
        if selected_row >= 0:
            incident_id = int(self.incident_table.item(selected_row, 0).text())
            dialog = ExtendIncidentDialog(self.incident_manager, incident_id, self)
            dialog.exec_()
            self.load_incidents()

    def analyze_cause(self):
        selected_row = self.incident_table.currentRow()
        if selected_row >= 0:
            incident_id = int(self.incident_table.item(selected_row, 0).text())
            dialog = CauseAnalysisDialog(self.incident_manager, incident_id, self)
            dialog.exec_()
            self.load_incidents()

    def document_results(self):
        selected_row = self.incident_table.currentRow()
        if selected_row >= 0:
            incident_id = int(self.incident_table.item(selected_row, 0).text())
            dialog = DocumentResultsDialog(self.incident_manager, incident_id, self)
            dialog.exec_()
            self.load_incidents()

    def archive_incident(self):
        selected_row = self.incident_table.currentRow()
        if selected_row >= 0:
            incident_id = int(self.incident_table.item(selected_row, 0).text())
            if self.incident_manager.archive_incident(incident_id):
                QMessageBox.information(self, "Успех", "Происшествие архивировано!")
                self.load_incidents()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось архивировать происшествие.")

    def show_statistics(self):
        dialog = StatisticsDialog(self.incident_manager, self)
        dialog.exec_()

    def search_by_date(self):
        dialog = DateSearchDialog(self.incident_manager, self)
        dialog.exec_()

    def show_my_incidents(self):
        my_incidents = self.incident_manager.get_my_incidents(self.current_user.username)
        self.reports_table.setRowCount(len(my_incidents))
        
        for row, incident in enumerate(my_incidents):
            self.reports_table.setItem(row, 0, QTableWidgetItem(str(incident.id)))
            self.reports_table.setItem(row, 1, QTableWidgetItem(incident.incident_type))
            self.reports_table.setItem(row, 2, QTableWidgetItem(incident.date_time))
            self.reports_table.setItem(row, 3, QTableWidgetItem(incident.location.address))
            self.reports_table.setItem(row, 4, QTableWidgetItem(incident.description))
            self.reports_table.setItem(row, 5, QTableWidgetItem(incident.priority))
            self.reports_table.setItem(row, 6, QTableWidgetItem(incident.status))
            self.reports_table.setItem(row, 7, QTableWidgetItem(incident.created_by or ""))

    def load_incidents(self):
        incidents = self.incident_manager.get_all_incidents()
        self.incident_table.setRowCount(len(incidents))

        for row, incident in enumerate(incidents):
            self.incident_table.setItem(row, 0, QTableWidgetItem(str(incident.id)))
            self.incident_table.setItem(row, 1, QTableWidgetItem(incident.incident_type))
            self.incident_table.setItem(row, 2, QTableWidgetItem(incident.date_time))
            self.incident_table.setItem(row, 3, QTableWidgetItem(incident.location.address))
            self.incident_table.setItem(row, 4, QTableWidgetItem(incident.description))
            self.incident_table.setItem(row, 5, QTableWidgetItem(incident.priority))
            self.incident_table.setItem(row, 6, QTableWidgetItem(incident.status))
            self.incident_table.setItem(row, 7, QTableWidgetItem(incident.created_by or ""))

    def on_incident_selected(self):
        selected_row = self.incident_table.currentRow()
        has_selection = selected_row >= 0
        
        self.edit_incident_button.setEnabled(has_selection)
        self.delete_incident_button.setEnabled(has_selection)
        self.extend_button.setEnabled(has_selection)
        self.analyze_button.setEnabled(has_selection)
        self.document_button.setEnabled(has_selection)
        self.archive_button.setEnabled(has_selection)