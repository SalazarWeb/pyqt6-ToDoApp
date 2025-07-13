# 📋 TaskMaster Pro

Una aplicación moderna de gestión de tareas construida con PyQt6 y Qt Designer, diseñada para maximizar tu productividad con una interfaz intuitiva y funcionalidades avanzadas.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Activo-brightgreen.svg)

## ✨ Características Principales

### 🚀 Funcionalidades Core
- **Gestión Rápida de Tareas**: Agrega tareas instantáneamente con un solo clic o presionando Enter
- **Interfaz Moderna**: Diseño limpio y profesional con estilos CSS personalizados
- **Tarjetas Interactivas**: Cada tarea se presenta en una tarjeta visual con controles integrados
- **Persistencia Automática**: Guardado automático cada 30 segundos sin interrumpir tu flujo de trabajo

### 🔍 Búsqueda y Filtros Avanzados
- **Búsqueda en Tiempo Real**: Encuentra tareas instantáneamente mientras escribes
- **Filtros por Estado**: 
  - Todas las tareas
  - Solo pendientes
  - Solo completadas
- **Filtros por Fecha**:
  - Todas las fechas
  - Creadas hoy
  - Esta semana
  - Este mes
  - Rango personalizado

### 📊 Estadísticas y Productividad
- **Contador de Progreso**: Visualiza tu avance con estadísticas en tiempo real
- **Medidor de Productividad**: Porcentaje basado en tareas completadas hoy
- **Feedback Visual**: Notificaciones y mensajes de estado informativos

### 💾 Gestión de Datos
- **Formato JSON**: Datos almacenados en formato legible y portable
- **Auto-guardado**: Nunca pierdas tu progreso
- **Importar/Exportar**: Comparte listas de tareas entre dispositivos
- **IDs Únicos**: Cada tarea tiene un identificador UUID único

## 🛠️ Tecnologías Utilizadas

- **Python 3.7+**: Lenguaje de programación principal
- **PyQt6**: Framework GUI moderno y potente
- **Qt Designer**: Herramienta de diseño de interfaces visuales
- **JSON**: Formato de almacenamiento de datos
- **UUID**: Generación de identificadores únicos

## 📦 Instalación

### Prerrequisitos
```bash
# Verificar versión de Python
python --version  # Debe ser 3.7 o superior
```

### Instalación de Dependencias
```bash
# Instalar PyQt6
pip install PyQt6

# O usando requirements.txt (si existe)
pip install -r requirements.txt
```

### Clonar o Descargar
```bash
# Si usas Git
git clone <tu-repositorio>
cd pyqt6-designer

# O simplemente descarga los archivos:
# - main.py
# - interface.ui
# - tareas.json (se crea automáticamente)
```

## 🚀 Uso

### Ejecutar la Aplicación
```bash
python main.py
```

### Uso Básico

1. **Agregar Tareas**:
   - Escribe en el campo "Agregar nueva tarea..."
   - Presiona Enter o haz clic en "+ Agregar Tarea"

2. **Gestionar Tareas**:
   - ✅ Marca como completada haciendo clic en el checkbox
   - 🗑️ Elimina tareas con el botón de eliminar
   - 📅 Las fechas de creación se muestran automáticamente

3. **Buscar y Filtrar**:
   - 🔍 Usa la barra de búsqueda para encontrar tareas específicas
   - 🔧 Aplica filtros desde el panel derecho
   - 🧹 Limpia todos los filtros con un solo clic

4. **Monitorear Progreso**:
   - 📊 Observa las estadísticas en el panel izquierdo
   - ⚡ Sigue tu productividad diaria

## 📁 Estructura del Proyecto

```
pyqt6-designer/
│
├── main.py           # Aplicación principal con lógica de negocio
├── interface.ui      # Diseño de interfaz creado con Qt Designer
├── tareas.json       # Archivo de datos (se genera automáticamente)
└── README.md         # Este archivo
```

### Arquitectura del Código

#### `main.py`
- **TaskMasterPro**: Clase principal de la aplicación
- **TaskCard**: Widget personalizado para cada tarea
- **Funcionalidades**: Gestión de eventos, persistencia, filtros

#### `interface.ui`
- **Diseño Visual**: Layout de 3 paneles (izquierdo, central, derecho)
- **Estilos CSS**: Tema moderno con colores profesionales
- **Componentes**: Inputs, botones, listas, combos, filtros de fecha

## 🔧 Funcionalidades Técnicas

### Características Avanzadas
- **Señales PyQt6**: Comunicación reactiva entre componentes
- **Timer de Auto-guardado**: Persistencia automática sin bloqueos
- **Gestión de Estados**: Control preciso del estado de cada tarea
- **Manejo de Errores**: Validaciones y mensajes informativos
- **Efectos Visuales**: Hover effects y transiciones suaves

### Estructura de Datos
```json
{
  "id": "uuid-único",
  "text": "Descripción de la tarea",
  "completed": false,
  "created": "2025-07-13T03:12:34.138742",
  "completed_date": "2025-07-13T03:45:20.333744"
}
```

## 🎨 Personalización

### Modificar Estilos
Los estilos CSS están integrados en `interface.ui`. Puedes personalizarlos editando:
- Colores de fondo y bordes
- Tipografías y tamaños
- Espaciados y márgenes
- Efectos hover y focus

### Extender Funcionalidades
El código está estructurado para fácil extensión:
- Agregar nuevos filtros en `apply_filters()`
- Modificar estructura de datos en métodos de guardado/carga
- Personalizar tarjetas de tareas en la clase `TaskCard`

## 🐛 Solución de Problemas

### Problemas Comunes

**Error: "No module named 'PyQt6'"**
```bash
pip install PyQt6
```

**Error: "No such file 'interface.ui'"**
- Asegúrate de que `interface.ui` esté en el mismo directorio que `main.py`

**Tareas no se guardan**
- Verifica permisos de escritura en el directorio
- El archivo `tareas.json` se crea automáticamente

**Interfaz no se ve correctamente**
- Asegúrate de usar PyQt6 (no PyQt5)
- Verifica que Qt Designer sea compatible con PyQt6

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si quieres mejorar TaskMaster Pro:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Ideas para Contribuir
- 🌙 Modo oscuro
- 📱 Diseño responsive
- 🔔 Notificaciones de recordatorio
- 📈 Más métricas de productividad
- 🎯 Categorías y etiquetas
- 📤 Exportar a otros formatos (CSV, PDF)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

## 🙏 Agradecimientos

- PyQt6 Team por el excelente framework
- Qt Designer por la herramienta de diseño visual
- La comunidad de Python por el soporte continuo

---

## 📸 Capturas de Pantalla

*Nota: Agrega capturas de pantalla de tu aplicación aquí para mostrar la interfaz*

```
[Captura Principal] [Captura Filtros] [Captura Estadísticas]
```

---

**⭐ Si este proyecto te ayuda, considera darle una estrella ⭐**

```bash
# Para ejecutar rápidamente:
python main.py
```

¡Disfruta organizando tus tareas con TaskMaster Pro! 🚀