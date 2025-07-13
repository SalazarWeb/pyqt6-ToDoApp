import sys
import json
import os
import uuid
from datetime import datetime, timedelta
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal
from PyQt6.QtWidgets import (QMessageBox, QListWidgetItem, QFileDialog, QCheckBox, 
                           QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
                           QProgressBar, QDialog, QDateTimeEdit, QComboBox, QTextEdit,
                           QInputDialog, QFrame, QSpacerItem, QSizePolicy, QScrollArea)
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QBrush, QPen
import subprocess

class TaskCard(QWidget):
    """Widget simplificado para tarjetas de tareas"""
    
    taskToggled = pyqtSignal(str, bool)
    taskDeleted = pyqtSignal(str)
    
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.is_completed = task_data.get('completed', False)
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz simplificada de la tarjeta"""
        self.setFixedHeight(60)
        
        # Aplicar estilos base
        base_style = """
            QWidget {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                margin: 6px 0;
            }
        """
        
        if self.is_completed:
            base_style += """
                QWidget {
                    opacity: 0.6;
                    background-color: #F9FAFB;
                }
            """
            
        self.setStyleSheet(base_style)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(12)
        
        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.is_completed)
        self.checkbox.setFixedSize(20, 20)
        self.checkbox.stateChanged.connect(self.on_toggle)
        main_layout.addWidget(self.checkbox)
        
        # Título de la tarea
        self.title_label = QLabel(self.task_data['text'])
        title_style = "font-size: 14px; font-weight: 600; color: #111827;"
        if self.is_completed:
            title_style += " text-decoration: line-through; color: #9CA3AF;"
        self.title_label.setStyleSheet(title_style)
        self.title_label.setWordWrap(True)
        main_layout.addWidget(self.title_label, 1)  # Toma el espacio restante
        
        # Fecha de vencimiento (si existe)
        if self.task_data.get('due_date'):
            due_date = QLabel(f"📅 {self.task_data['due_date']}")
            due_date.setStyleSheet("font-size: 12px; color: #6B7280;")
            main_layout.addWidget(due_date)
        
        # Botón eliminar al final de la fila
        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 12px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        self.delete_btn.clicked.connect(self.on_delete)
        main_layout.addWidget(self.delete_btn)
        
        # Efecto hover
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
    
    def on_toggle(self, state):
        """Manejar cambio de estado"""
        is_completed = state == Qt.CheckState.Checked.value
        self.taskToggled.emit(self.task_data['id'], is_completed)
    
    def on_delete(self):
        """Manejar eliminación de tarea"""
        reply = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Eliminar la tarea '{self.task_data['text']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.taskDeleted.emit(self.task_data['id'])
    
    def enterEvent(self, event):
        """Efecto hover"""
        self.setStyleSheet(self.styleSheet() + """
            QWidget {
                border-color: #2563EB;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
        """)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Quitar efecto hover"""
        self.setup_ui()
        super().leaveEvent(event)

class TaskMasterPro(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar la interfaz
        uic.loadUi('interface.ui', self)
        
        # Archivo donde se guardan las tareas
        self.data_file = 'tareas.json'
        
        # Inicializar componentes
        self.setup_connections()
        
        # Cargar datos
        self.load_tasks()
        
        # Timer para auto-guardado
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_tasks)
        self.auto_save_timer.start(30000)  # 30 segundos
        
        # Estado inicial
        self.update_stats()
        self.statusBar().showMessage("✨ TaskMaster Pro - Versión ultra simplificada", 3000)
    
    def setup_connections(self):
        """Configurar todas las conexiones de señales"""
        # Botones principales
        self.quickAddButton.clicked.connect(self.quick_add_task)
        self.quickTaskInput.returnPressed.connect(self.quick_add_task)
        
        # Configurar búsqueda en tiempo real
        self.searchInput.textChanged.connect(self.on_search_changed)
        
        # Filtros del panel derecho
        self.statusFilterCombo.currentTextChanged.connect(self.apply_filters)
        self.dateFilterTypeCombo.currentTextChanged.connect(self.on_date_filter_changed)
        self.clearFiltersButton.clicked.connect(self.clear_filters)
        
        # Nota: Las acciones del menú fueron removidas del archivo .ui para compatibilidad con PyQt6
        # Si necesitas menús, puedes crearlos programáticamente aquí
    
    def quick_add_task(self):
        """Agregar tarea rápidamente"""
        task_text = self.quickTaskInput.text().strip()
        if not task_text:
            self.quickTaskInput.setFocus()
            return
        
        # Crear nueva tarea sin prioridad por defecto
        task_data = {
            'id': str(uuid.uuid4()),
            'text': task_text,
            'completed': False,
            'created': datetime.now().isoformat()
        }
        
        # Agregar a la lista
        self.add_task_to_list(task_data)
        
        # Limpiar input
        self.quickTaskInput.clear()
        
        # Feedback visual
        self.statusBar().showMessage(f"✅ Tarea agregada: '{task_text}'", 2000)
        
        # Auto-enfocar para siguiente tarea
        self.quickTaskInput.setFocus()
    
    def add_task_to_list(self, task_data):
        """Agregar tarea con tarjeta simplificada"""
        # Crear tarjeta de tarea
        task_card = TaskCard(task_data)
        task_card.taskToggled.connect(self.on_task_toggled)
        task_card.taskDeleted.connect(self.on_task_deleted)
        
        # Agregar al widget de lista
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, task_data)
        item.setSizeHint(task_card.sizeHint())
        
        self.tasksList.addItem(item)
        self.tasksList.setItemWidget(item, task_card)
        
        # Actualizar estadísticas
        self.update_stats()
        self.auto_save_tasks()
    
    def on_task_toggled(self, task_id, is_completed):
        """Manejar cambio de estado de tarea"""
        # Encontrar y actualizar la tarea
        for i in range(self.tasksList.count()):
            item = self.tasksList.item(i)
            task_data = item.data(Qt.ItemDataRole.UserRole)
            
            if task_data['id'] == task_id:
                task_data['completed'] = is_completed
                
                if is_completed:
                    task_data['completed_date'] = datetime.now().isoformat()
                else:
                    task_data.pop('completed_date', None)
                
                item.setData(Qt.ItemDataRole.UserRole, task_data)
                
                # Actualizar tarjeta visual
                widget = self.tasksList.itemWidget(item)
                if widget:
                    widget.task_data = task_data
                    widget.is_completed = is_completed
                    widget.setup_ui()
                
                break
        
        self.update_stats()
        self.auto_save_tasks()
        
        status = "completada" if is_completed else "marcada como pendiente"
        self.statusBar().showMessage(f"✅ Tarea {status}", 2000)
    
    def on_task_deleted(self, task_id):
        """Manejar eliminación de tarea"""
        # Encontrar y eliminar la tarea
        for i in range(self.tasksList.count()):
            item = self.tasksList.item(i)
            task_data = item.data(Qt.ItemDataRole.UserRole)
            
            if task_data['id'] == task_id:
                self.tasksList.takeItem(i)
                self.update_stats()
                self.auto_save_tasks()
                self.statusBar().showMessage(f"🗑️ Tarea eliminada: '{task_data['text']}'", 3000)
                break
    
    def on_search_changed(self, text):
        """Búsqueda en tiempo real"""
        search_term = text.lower().strip()
        
        for i in range(self.tasksList.count()):
            item = self.tasksList.item(i)
            task_data = item.data(Qt.ItemDataRole.UserRole)
            
            # Mostrar/ocultar según coincidencia
            matches = search_term in task_data['text'].lower()
            item.setHidden(not matches and search_term != "")
        
        # Feedback en status bar
        if search_term:
            visible_count = sum(1 for i in range(self.tasksList.count()) 
                              if not self.tasksList.item(i).isHidden())
            self.statusBar().showMessage(f"🔍 {visible_count} resultados para '{text}'", 2000)
    
    def apply_filters(self):
        """Aplicar filtros de estado"""
        filter_text = self.statusFilterCombo.currentText()
        
        for i in range(self.tasksList.count()):
            item = self.tasksList.item(i)
            task_data = item.data(Qt.ItemDataRole.UserRole)
            show_item = True
            
            if filter_text == "Pendientes":
                show_item = not task_data.get('completed', False)
            elif filter_text == "Completadas":
                show_item = task_data.get('completed', False)
            # "Todas las tareas" muestra todo
            
            item.setHidden(not show_item)
        
        # Mostrar feedback
        visible_count = sum(1 for i in range(self.tasksList.count()) 
                          if not self.tasksList.item(i).isHidden())
        self.statusBar().showMessage(f"🔧 Filtro aplicado: {visible_count} tareas visibles", 2000)
    
    def on_date_filter_changed(self):
        """Manejar cambio en filtro de fecha"""
        filter_type = self.dateFilterTypeCombo.currentText()
        
        # Mostrar/ocultar widget de rango personalizado
        if filter_type == "Rango personalizado":
            self.customDateWidget.setVisible(True)
        else:
            self.customDateWidget.setVisible(False)
            self.apply_date_filter()
    
    def apply_date_filter(self):
        """Aplicar filtro de fecha"""
        filter_type = self.dateFilterTypeCombo.currentText()
        today = datetime.now().date()
        
        for i in range(self.tasksList.count()):
            item = self.tasksList.item(i)
            task_data = item.data(Qt.ItemDataRole.UserRole)
            show_item = True
            
            if filter_type != "Todas las fechas" and 'created' in task_data:
                try:
                    created_date = datetime.fromisoformat(task_data['created']).date()
                    
                    if filter_type == "Creadas hoy":
                        show_item = created_date == today
                    elif filter_type == "Esta semana":
                        week_start = today - timedelta(days=today.weekday())
                        show_item = created_date >= week_start
                    elif filter_type == "Este mes":
                        show_item = (created_date.year == today.year and 
                                   created_date.month == today.month)
                except:
                    show_item = True
            
            # Solo aplicar si no está oculto por otros filtros
            if not item.isHidden():
                item.setHidden(not show_item)
    
    def clear_filters(self):
        """Limpiar todos los filtros"""
        # Resetear combos
        self.statusFilterCombo.setCurrentIndex(0)  # "Todas las tareas"
        self.dateFilterTypeCombo.setCurrentIndex(0)  # "Todas las fechas"
        
        # Limpiar búsqueda
        self.searchInput.clear()
        
        # Mostrar todas las tareas
        for i in range(self.tasksList.count()):
            item = self.tasksList.item(i)
            item.setHidden(False)
        
        # Ocultar widget de fecha personalizada
        self.customDateWidget.setVisible(False)
        
        self.statusBar().showMessage("🧹 Filtros limpiados", 2000)
    
    def update_stats(self):
        """Actualizar estadísticas"""
        total = self.tasksList.count()
        completed = 0
        
        for i in range(total):
            item = self.tasksList.item(i)
            task_data = item.data(Qt.ItemDataRole.UserRole)
            if task_data.get('completed', False):
                completed += 1
        
        # Estadísticas básicas
        percentage = (completed / total * 100) if total > 0 else 0
        self.statsLabel.setText(f"📊 {completed}/{total} tareas completadas ({percentage:.0f}%)")
        
        # Productividad simplificada
        today_completed = 0
        for i in range(total):
            item = self.tasksList.item(i)
            task_data = item.data(Qt.ItemDataRole.UserRole)
            if (task_data.get('completed', False) and 
                task_data.get('completed_date') and
                task_data['completed_date'][:10] == datetime.now().strftime('%Y-%m-%d')):
                today_completed += 1
        
        productivity = min(today_completed * 20, 100)
        self.productivityLabel.setText(f"⚡ Productividad: {productivity}%")
    
    def save_tasks(self, filename=None):
        """Guardar tareas en archivo JSON"""
        if filename is None:
            filename = self.data_file
            
        tasks = []
        for i in range(self.tasksList.count()):
            item = self.tasksList.item(i)
            task_data = item.data(Qt.ItemDataRole.UserRole)
            tasks.append(task_data)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{str(e)}")
            return False
    
    def save_tasks_as(self):
        """Guardar tareas con diálogo de archivo"""
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar Lista de Tareas", 
            "mis_tareas.json", 
            "Archivos JSON (*.json);;Todos los archivos (*)"
        )
        if filename:
            if self.save_tasks(filename):
                self.statusBar().showMessage(f"💾 Tareas guardadas en: {filename}", 3000)
    
    def load_tasks_from(self):
        """Cargar tareas con diálogo de archivo"""
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Cargar Lista de Tareas", 
            "", 
            "Archivos JSON (*.json);;Todos los archivos (*)"
        )
        if filename:
            self.load_tasks(filename)
            self.update_stats()
            self.statusBar().showMessage(f"📂 Tareas cargadas desde: {filename}", 3000)
    
    def load_tasks(self, filename=None):
        """Cargar tareas desde archivo JSON"""
        if filename is None:
            filename = self.data_file
            
        if not os.path.exists(filename):
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            
            self.tasksList.clear()
            for task_data in tasks:
                # Asegurar que tenga ID único si no lo tiene
                if 'id' not in task_data:
                    task_data['id'] = str(uuid.uuid4())
                
                # Crear tarjeta de tarea
                task_card = TaskCard(task_data)
                task_card.taskToggled.connect(self.on_task_toggled)
                task_card.taskDeleted.connect(self.on_task_deleted)
                
                # Agregar al widget de lista
                item = QListWidgetItem()
                item.setData(Qt.ItemDataRole.UserRole, task_data)
                item.setSizeHint(task_card.sizeHint())
                
                self.tasksList.addItem(item)
                self.tasksList.setItemWidget(item, task_card)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{str(e)}")

    def auto_save_tasks(self):
        """Auto-guardar tareas (llamado por timer)"""
        self.save_tasks()

    def closeEvent(self, event):
        """Guardar tareas antes de cerrar la aplicación"""
        self.save_tasks()
        self.statusBar().showMessage("💾 Tareas guardadas automáticamente", 1000)
        event.accept()
    
    def refresh_task_list(self):
        """Actualizar lista de tareas"""
        self.tasksList.clear()
        self.load_tasks()
        self.update_stats()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TaskMasterPro()
    window.show()
    sys.exit(app.exec())