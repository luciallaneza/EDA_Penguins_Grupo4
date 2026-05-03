# ⊹₊⋆🐧ྀི⊹₊⋆ Proyecto grupal sobre EDA ⊹₊⋆🐧ྀི⊹₊⋆

# Integrantes del equipo:
🐧[Chiara Contreras](https://github.com/chiaracont)   
🐧[Jenireé Tovar](https://github.com/JenireeTovar)   
🐧[Michelle Olivares](https://github.com/michelleolivares86-tech)   
🐧[Lucía Llaneza](https://github.com/luciallaneza)   
🐧[Sara Bailón](https://github.com/Sara89359)

# Cliente: 
### Organización de Investigación Biológica Polar


## 1) 🔮 ¿Qué solicita el cliente?

Convertir el dataset **Palmer Penguins** en un informe exploratorio claro y util para toma de decisiones cientificas.

## 2) 📊 ¿Por qué es útil nuestro análisis?

Queremos responder **tres necesidades** reales:

1. Entender diferencias observables entre especies y su distribución por isla.
2. Detectar riesgos de calidad del dato y posibles sesgos de muestreo.
3. Obtener recomendaciones concretas para mejorar futuras campañas de recogida de datos.

## 3) ✅ ¿Cómo lo vamos a resolver?

Nos vamos a centrar en las siguientes cuestiones:

1. Qué **especies** predominan y como se distribuyen.
2. Qué **diferencias morfologicas** relevantes aparecen entre especies.
3. Qué variables son mas útiles para entender **perfiles biológicos**.
4. Qué **limitaciones** tiene el dataset para interpretar resultados.
5. Qué **recomendaciones concretas** puede aplicar el cliente.

## 4) 📁 Estructura del proyecto:
│
├── app_penguins.py          # App principal de Streamlit
├── src/
│   ├── penguins_pipeline.py # Funciones de carga, filtros, KPIs, gráficos
├── notebooks/
│   ├── 01_data
│         ├── penguins_raw.csv   
│   ├── 02_limpieza
│         ├── penguins_limpieza.ipynb  
│         ├── penguins_limpio.csv
│   ├── 03_analisis
│         ├── 01_Univariado.ipynb 
│         ├── 02_Bivariado.ipynb
│         ├── 03_Visualizacion.ipynb
│   ├── 04_hallazgos_y_conclusiones
│         ├── 01_limitaciones.ipynb 
│         ├── 02_conclusiones.ipynb
├── README.md
├── Imagenes
├── assets
├── requirements.txt
└── roles_y_tareas.md

## 6) “Flujo de notebooks”

🔹 Notebook 01 — penguins_limpieza.ipynb  
•     Diagnósico inicial
•     Limpieza básica
🔹 Notebook 02 — Univariado.ipynb 
•     Análisis morfológico general
•     Distribución por isla, sexo y especie
🔹 Notebook 03 — Bivariado.ipynb
•    Relación de masa corporal por especie
•    Relación de especie por islas
•    Diferencias morfológicas (longitud del pico, profundidad del pico, longitud de aleta y masa corporal)
🔹 Notebook 03 — Visualizacion.ipynb
•    Estudio visual de las estadísticas analizadas
•    Combinaciones posibles de visualización
🔹 Notebook 03 — limitaciones.ipynb
•    Limitaciones del dataset
🔹 Notebook 03 — conclusiones.ipynb
•    Hallazgos encontrados tras el análisis
•    Recomendaciones al cliente


## 6) 🔗 Enlaces de interes: 

💻 [Iceberg Intelligence App](https://icebergintelligence.streamlit.app/)

🔨 [Progreso del proyecto](https://github.com/users/chiaracont/projects/1)
