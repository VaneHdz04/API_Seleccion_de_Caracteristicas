# 🧩 FeatureSelect: Plataforma Inteligente de Selección de Características y Optimización de Modelos para Detección de Malware

[Deteccion de Malware_API con Django](https://shameless-caren-compactedly.ngrok-free.dev/)


**DFeatureSelect** es una plataforma web desarrollada con Django que integra técnicas avanzadas de selección de características, procesamiento automatizado de datos y análisis comparativo del rendimiento de modelos predictivos en el contexto de la detección de malware.

Diseñada para investigadores, analistas de ciberseguridad y profesionales de ciencia de datos, la herramienta permite subir datasets, aplicar métodos de reducción de dimensionalidad y evaluar el impacto de las variables seleccionadas mediante métricas de rendimiento, todo desde una interfaz moderna, intuitiva y accesible.

---

## 🎯 Visión del Proyecto

El objetivo de FeatureSelect es optimizar el proceso de modelado predictivo en el ámbito de la ciberseguridad, ayudando a los analistas a identificar las variables más influyentes en la detección de malware y a mejorar la eficiencia de los modelos sin comprometer su precisión.

La plataforma busca reducir la complejidad de los datos y aumentar la interpretabilidad de los modelos mediante una combinación equilibrada de automatización, análisis estadístico y visualización interactiva, facilitando la toma de decisiones informadas.

---

## 🧱 Características Principales

- 📁 Carga inteligente de datasets CSV, con validación automática de estructura, tipos de datos y valores nulos.

- 🧮 Aplicación de técnicas de selección de características, como filtros estadísticos y métodos de importancia de variables.

- ⚙️ Comparación de modelos base vs. modelos optimizados, evaluando el impacto de la reducción de características.

- 📊 Métricas de rendimiento integradas, incluyendo F1 Score, Accuracy y Precision.

- 🔍 Análisis exploratorio de datos: estadísticas descriptivas, distribución de variables y detección de correlaciones.

- 🧠 Visualización interactiva de resultados, con tablas dinámicas y reportes de las características más relevantes.

- 💾 Exportación y reanálisis: los resultados pueden ser almacenados o reutilizados para nuevos experimentos.  

---

## 🧠 Tecnologías Implementadas

| Área | Tecnología | Descripción |
|------|-------------|-------------|
| **Backend** | Django | Framework principal para la API y gestión del servidor |
| **Machine Learning** | Scikit-learn | Entrenamiento y evaluación de modelos |
| **Procesamiento de Datos** | Pandas / NumPy | Limpieza, transformación y análisis de datasets |
| **Visualización** | Matplotlib / Seaborn | Gráficas interactivas de resultados |
| **Frontend** | TailwindCSS + HTML Templates | Interfaz moderna, responsiva y limpia |
| **Control de Versiones** | Git / GitHub | Mantenimiento y colaboración del código fuente |

---

## ⚙️ Requisitos Previos

Antes de ejecutar la aplicación, asegúrate de contar con:

- 🐍 **Python 3.8+**
- 📦 **pip** (Administrador de paquetes de Python)
- 🧭 **Git** (opcional, para clonar el repositorio)
- 🧰 **Entorno virtual** recomendado (venv o conda)

---

## 🚀 Instalación y Puesta en Marcha

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Jesusnm21/malware_api.git
cd malware_api
```

### 2️⃣ Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows
```
### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4️⃣ Ejecutar el servidor de desarrollo
```bash
python manage.py runserver 0.0.0.0:8000
```
### 5️⃣ Abrir en el navegador
```bash

http://localhost:8000
```
### 🧪 Flujo de Uso

- 📤 Carga del dataset en formato .csv desde la interfaz web.

- 🔄 Validación automática de los datos (columnas, tipos, valores faltantes).

- 🧠 Ejecución del proceso de selección de características.

- 🤖 Entrenamiento y comparación de modelos antes y después de la reducción.

- 📊 Visualización de métricas (F1 Score, Accuracy, Precision, Recall).

- 📈 Presentación de las variables más influyentes y parámetros del modelo final.

El sistema genera además reportes detallados con las métricas, estadísticas y resultados de la optimización.


### 📂 Estructura del Proyecto
```bash
├── ml_app/
│   ├── forms.py                # Definición del formulario de carga de datasets
│   ├── views.py                # Lógica principal de análisis y visualización
│   ├── utils/                  # Funciones auxiliares (procesamiento y modelado)
│   ├── templates/
│   │   ├── index.html          # Interfaz principal de carga de datos
│   │   ├── resultados.html     # Página de resultados y métricas
│   └── static/                 # Archivos estáticos (CSS, JS, imágenes)
│
├── malware_api/
│   ├── settings.py             # Configuración global del proyecto Django
│   └── urls.py                 # Enrutamiento principal
│
├── requirements.txt            # Dependencias del entorno
└── manage.py                   # Script principal de gestión de Django
```
### 🔐 Buenas Prácticas y Consideraciones

- 🧩 Utiliza entornos virtuales para evitar conflictos de dependencias.

- 🧾 Asegúrate de que tu dataset tenga encabezados y formato válido antes de subirlo.

- 📦 Evita archivos mayores a 50 MB en entornos locales.

- 🔄 Reinicia el servidor tras realizar modificaciones en la estructura o modelos.

- 🧠 Puedes extender los modelos agregando nuevas clases en ml_models.py.


### 👨‍💻 Autor

Desarrollado por: Vanesa Hernández Martínez
Proyecto: Caso Práctico: API de Selección de Características para Detección de Malware
