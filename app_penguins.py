"""
App_conclusiones.py — Iceberg Intelligence Dashboard (versión unificada)
=========================================================================
"""

# ══════════════════════════════════════════════════════════════════════════════
# 1. IMPORTS
# ══════════════════════════════════════════════════════════════════════════════
import base64
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import folium
import streamlit as st
from PIL import Image
from streamlit_folium import st_folium

from src.penguins_pipeline import (
    carga_datos,
    compute_kpis,
    distribucion_especie,
    grafico_masa_por_especie,
    graficos_lmplot,
    heatmap_correlaciones,
)

# ══════════════════════════════════════════════════════════════════════════════
# 2. CONFIGURACIÓN DE PÁGINA — PRIMERA LLAMADA A STREAMLIT, SIEMPRE
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Iceberg Intelligence",
    layout="wide",
    page_icon="🐧",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. CSS GLOBAL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>

.block-container {
    padding-top: 0rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-bottom: 4rem;
}

.stAlert {
    background-color: rgba(22, 27, 34, 0.85) !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
    padding: 15px !important;
    color: #e2e8f0 !important;
}

.banner-wrapper {
    width: 100%;
    max-height: 900px;
    overflow: hidden;
}

.banner-wrapper img {
    width: 100%;
    height: 900px;
    object-fit: cover;
    object-position: center;
    display: block;
}

.acto-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: white;
    border-radius: 14px;
    padding: 18px 24px;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 14px;
}

.acto-numero {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 2px;
}

.acto-titulo {
    font-size: 1.3rem;
    font-weight: 800;
    color: #f1f5f9;
    margin: 0;
}

.acto-duracion {
    margin-left: auto;
    background: rgba(255,255,255,0.1);
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: #94a3b8;
    white-space: nowrap;
}

.section-label {
    font-size: 1.35rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 6px;
}

.section-content {
    font-size: 1.35rem;
    line-height: 1.55;
    color: #374151;
    margin: 0;
}

.badge-evidencia      { color: #1d4ed8; }
.badge-interpretacion { color: #7c3aed; }
.badge-implicacion    { color: #b45309; }
.badge-recomendacion  { color: #065f46; }

.pill-evidencia {
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 12px 14px;
}

.pill-interpretacion {
    background: #f5f3ff;
    border-left: 4px solid #8b5cf6;
    border-radius: 0 8px 8px 0;
    padding: 12px 14px;
}

.pill-implicacion {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 12px 14px;
}

.pill-recomendacion {
    background: #ecfdf5;
    border-left: 4px solid #10b981;
    border-radius: 0 8px 8px 0;
    padding: 12px 14px;
}

div[data-testid="column"] { padding: 4px 8px; }

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgba(255,255,255,0.85);
    color: #333;
    text-align: center;
    padding: 8px 0;
    font-size: 0.9rem;
    border-top: 1px solid #ccc;
}

.lim-card {
    background: #161b22; border: 1px solid #21262d; border-radius: 14px;
    padding: 18px 20px; margin-bottom: 10px;
}
.lim-card-titulo { font-size: 1rem; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
.lim-card-desc { font-size: 0.83rem; color: #64748b; line-height: 1.5; }

.seccion-titulo {
    font-size: 1rem; font-weight: 700;
    color: #e2e8f0; margin: 1.8rem 0 0.6rem;
    padding-bottom: 8px; border-bottom: 1px solid #1e293b;
}
.nota {
    background: rgba(56,189,248,0.07); border-left: 3px solid #38bdf8;
    border-radius: 0 8px 8px 0; padding: 10px 14px;
    font-size: 0.83rem; color: #7dd3fc; line-height: 1.6; margin-top: 8px;
}

/* FLECHA COLAPSADA - FUNCIONA 100% */
div[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background-color: rgba(255,255,255,0.9) !important;
    border-radius: 0 8px 8px 0 !important;
    z-index

            
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 4. DATOS DE LIMITACIONES
# ══════════════════════════════════════════════════════════════════════════════
LIMITACIONES = [
    {
        "id": "ids",
        "icono": "🔢",
        "titulo": "IDs individuales sin trazabilidad",
        "descripcion": "Los IDs se reutilizan entre especies, sexos e islas. Imposible seguir a un individuo a lo largo del tiempo.",
        "color": "#f87171",
        "categorias": ["Trazabilidad\nindividual", "Seguimiento\ntemporal", "Calidad\ndel dato", "Análisis\nlongitudinal", "Fiabilidad\ncomparativa"],
        "antes":   [1, 1, 5, 1, 4],
        "despues": [9, 8, 9, 8, 8],
        "mejoras": [
            "Nomenclatura alfanumérica única (ej. ADL-F-001)",
            "Registro de pareja macho/hembra vinculada al ID",
            "Historial temporal por individuo año a año",
        ],
        "impacto_registros": "+0 filas (mismo nº, mejor calidad)",
        "impacto_variables": "+2 variables (ID_pareja, ID_unico)",
        "analisis_nuevo": "Series temporales por individuo, análisis de supervivencia, seguimiento reproductivo",
    },
    {
        "id": "comportamiento",
        "icono": "🐧",
        "titulo": "Sin datos de comportamiento",
        "descripcion": "Solo hay medidas morfológicas. No se puede concluir nada sobre migración, reproducción ni anidación.",
        "color": "#fb923c",
        "categorias": ["Análisis\nreproductivo", "Estudio\nmigración", "Dinámica\npoblacional", "Predicción\nestacional", "Valor para\nel cliente"],
        "antes":   [0, 0, 2, 1, 4],
        "despues": [8, 7, 8, 7, 9],
        "mejoras": [
            "Variable de fase reproductiva (cortejo/incubación/crianza)",
            "Coordenadas GPS de movimiento entre islas",
            "Fecha exacta y fase del ciclo anual",
            "Nº de huevos/crías por pareja",
        ],
        "impacto_registros": "+4 variables nuevas por registro",
        "impacto_variables": "+4 variables (fase, GPS_lat, GPS_lon, n_crias)",
        "analisis_nuevo": "Mapas de movimiento, modelos de ciclo reproductivo, predicción de éxito de cría",
    },
    {
        "id": "errores",
        "icono": "⚠️",
        "titulo": "Errores sistemáticos de identificación",
        "descripcion": "Los errores de identificación se mantienen a lo largo de los años, contaminando el análisis longitudinal.",
        "color": "#facc15",
        "categorias": ["Fiabilidad\ndel dato", "Consistencia\ntemporal", "Confianza\nestadística", "Reproducib.\ndel estudio", "Calidad\ngeneral"],
        "antes":   [4, 3, 5, 3, 5],
        "despues": [9, 9, 9, 9, 9],
        "mejoras": [
            "Protocolo de doble verificación por dos observadores",
            "Fotografía de identificación vinculada a cada muestra",
            "Flag de confianza en cada registro (alta/media/baja)",
        ],
        "impacto_registros": "Posible reducción de ~5-10% de registros dudosos",
        "impacto_variables": "+1 variable (nivel_confianza)",
        "analisis_nuevo": "Análisis de sensibilidad, comparativas con y sin registros dudosos, estudios replicables",
    },
    {
        "id": "temporal",
        "icono": "📅",
        "titulo": "Cobertura temporal limitada (nov-dic)",
        "descripcion": "Solo se tienen datos de 2 meses al año. No se puede conocer la dinámica poblacional anual ni estacional.",
        "color": "#34d399",
        "categorias": ["Cobertura\nanual", "Análisis\nestacional", "Dinámica\npoblacional", "Tendencias\na largo plazo", "Representativ.\ndel dataset"],
        "antes":   [2, 1, 2, 1, 3],
        "despues": [9, 9, 8, 8, 8],
        "mejoras": [
            "Muestreo en 4 momentos anuales",
            "Conteos de población total por isla en cada visita",
            "Comparativa interanual con los mismos individuos marcados",
        ],
        "impacto_registros": "x4 registros (muestreo en 4 estaciones)",
        "impacto_variables": "+1 variable (estacion_año)",
        "analisis_nuevo": "Series temporales estacionales, modelos de crecimiento poblacional, detección de tendencias de conservación",
    },
    {
        "id": "muestras",
        "icono": "⚖️",
        "titulo": "Dataset desequilibrado por especie e isla",
        "descripcion": "Chinstrap = 20%, Torgersen = 13%. Cualquier análisis comparativo entre especies o islas está sesgado.",
        "color": "#38bdf8",
        "categorias": ["Equidad\nmuestral", "Comparativas\ninter-especie", "Represent.\ngeográfica", "Validez\nestadística", "Análisis\ncomparativo"],
        "antes":   [3, 3, 3, 4, 3],
        "despues": [8, 9, 8, 9, 9],
        "mejoras": [
            "Muestreo estratificado (mismo nº por especie)",
            "Campaña específica para Chinstrap y Torgersen",
            "Tamaño muestral mínimo definido antes de cada campaña",
        ],
        "impacto_registros": "+~200 registros (para equilibrar Chinstrap y Torgersen)",
        "impacto_variables": "+0 variables (mismo formato, más datos)",
        "analisis_nuevo": "ANOVA entre especies válido, análisis de clustering fiable, comparativas inter-isla robustas",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. CONFIGURACIÓN MATPLOTLIB
# ══════════════════════════════════════════════════════════════════════════════
plt.rcParams.update({
    "figure.facecolor":   "#161b22",
    "axes.facecolor":     "#161b22",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.spines.left":   False,
    "axes.spines.bottom": False,
    "axes.labelcolor":    "#64748b",
    "xtick.color":        "#475569",
    "ytick.color":        "#475569",
    "text.color":         "#e2e8f0",
    "grid.color":         "#1e293b",
    "grid.linewidth":     0.8,
    "font.family":        "sans-serif",
})

# ══════════════════════════════════════════════════════════════════════════════
# 6. FUNCIONES DE GRÁFICOS DE LIMITACIONES
# ══════════════════════════════════════════════════════════════════════════════

def grafico_radar(lim: dict) -> plt.Figure:
    categorias = lim["categorias"]
    N = len(categorias)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    antes   = lim["antes"]   + lim["antes"][:1]
    despues = lim["despues"] + lim["despues"][:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True), facecolor="#161b22")
    ax.set_facecolor("#161b22")
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=7, color="#334155")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categorias, fontsize=8, color="#94a3b8")
    ax.grid(color="#1e293b", linewidth=0.8)
    ax.spines["polar"].set_color("#1e293b")
    ax.fill(angles, antes, color="#475569", alpha=0.25)
    ax.plot(angles, antes, color="#475569", linewidth=1.5, linestyle="--", label="Situación actual")
    ax.fill(angles, despues, color=lim["color"], alpha=0.25)
    ax.plot(angles, despues, color=lim["color"], linewidth=2, label="Tras la mejora")
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15),
              fontsize=8, framealpha=0, labelcolor="#94a3b8")
    fig.tight_layout()
    return fig


def grafico_barras_comparativo(lim: dict) -> plt.Figure:
    categorias = [c.replace("\n", " ") for c in lim["categorias"]]
    antes   = lim["antes"]
    despues = lim["despues"]
    mejora  = [d - a for d, a in zip(despues, antes)]
    y = np.arange(len(categorias))

    fig, ax = plt.subplots(figsize=(7, 3.5), facecolor="#161b22")
    ax.barh(y, [10] * len(y), color="#1e293b", height=0.6, zorder=1)
    ax.barh(y, antes, color="#334155", height=0.6, label="Situación actual", zorder=2)
    ax.barh(y, mejora, left=antes, color=lim["color"], height=0.6,
            alpha=0.85, label="Mejora estimada", zorder=3)
    for i, (a, d) in enumerate(zip(antes, despues)):
        ax.text(a - 0.3, i, str(a), va="center", ha="right", fontsize=8, color="#64748b")
        ax.text(d + 0.2, i, str(d), va="center", ha="left",  fontsize=8, color=lim["color"], fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(categorias, fontsize=9, color="#94a3b8")
    ax.set_xlim(0, 11.5)
    ax.set_xlabel("Puntuación (0 = imposible / 10 = óptimo)", fontsize=8, color="#475569")
    ax.axvline(x=10, color="#1e293b", linewidth=1, linestyle="--")
    ax.legend(fontsize=8, framealpha=0, labelcolor="#94a3b8", loc="lower right")
    ax.set_facecolor("#161b22")
    fig.tight_layout()
    return fig


def grafico_resumen_global(limitaciones: list) -> plt.Figure:
    titulos = [l["icono"] + " " + l["titulo"].split(" ")[0] + "..." for l in limitaciones]
    mejoras_medias = [
        round(np.mean([d - a for d, a in zip(l["despues"], l["antes"])]), 1)
        for l in limitaciones
    ]
    colores = [l["color"] for l in limitaciones]

    fig, ax = plt.subplots(figsize=(10, 4), facecolor="#161b22")
    bars = ax.bar(range(len(titulos)), mejoras_medias, color=colores, alpha=0.85,
                  edgecolor="#161b22", linewidth=1.5, width=0.6)
    for bar, val in zip(bars, mejoras_medias):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                f"+{val}", ha="center", va="bottom", fontsize=10,
                fontweight="bold", color="#e2e8f0")
    ax.set_xticks(range(len(titulos)))
    ax.set_xticklabels(titulos, fontsize=9, color="#94a3b8")
    ax.set_ylabel("Mejora media estimada (puntos)", fontsize=9, color="#475569")
    ax.set_ylim(0, 10)
    ax.set_facecolor("#161b22")
    ax.grid(axis="y", color="#1e293b", linewidth=0.8)
    fig.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 7. HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def imagen_a_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(path: str):
    data = imagen_a_base64(path)
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

def render_audio_player(path: str):
    audio_b64 = imagen_a_base64(path)
    html_code = f"""
    <div style="text-align:center; margin-top:10px;">
        <button onclick="playMusic()">🐧▶️ Reproducir</button>
        <button onclick="pauseMusic()">❄️⏸️ Pausar</button>
        <br><br>
        <input type="range" min="0" max="1" step="0.05" value="0.15"
               onchange="setVolume(this.value)" style="width:200px;">
    </div>
    <audio id="bg-music" loop>
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    </audio>
    <script>
        var audio = document.getElementById("bg-music");
        audio.volume = 0.15;
        function playMusic()  {{ audio.play();    }}
        function pauseMusic() {{ audio.pause();   }}
        function setVolume(v) {{ audio.volume = v; }}
    </script>
    """
    st.iframe(html_code, height=100)

def render_banner(path: str):
    img_b64 = imagen_a_base64(path)
    st.markdown(f"""
    <div class="banner-wrapper">
        <img src="data:image/png;base64,{img_b64}" />
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_bg(path: str):
    img_b64 = imagen_a_base64(path)
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("data:image/png;base64,{img_b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """, unsafe_allow_html=True)

def acto_header(titulo: str, emoji: str):
    st.markdown(f"""
    <div class="acto-header">
        <div style="font-size:2rem;">{emoji}</div>
        <div>
            <div class="acto-titulo">{titulo}</div>
        </div>
        
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 8. CARGA DE DATOS
# ══════════════════════════════════════════════════════════════════════════════
df = carga_datos()

# ══════════════════════════════════════════════════════════════════════════════
# 9. SIDEBAR — TODOS LOS WIDGETS AQUÍ EN EL CUERPO PRINCIPAL
#    CLAVE: nunca dentro de funciones llamadas condicionalmente.
#    Streamlit necesita ver los st.sidebar.* en el primer render para mostrarla.
# ══════════════════════════════════════════════════════════════════════════════


st.sidebar.markdown("---")

# Bajar las opciones de la barra lateral a la parte inferior
st.sidebar.markdown(
    "<div style='flex: 1; min-height: 300px;'></div>",
    unsafe_allow_html=True
)

st.sidebar.markdown("### 🗺️ Filtrar por isla")
filtro_isla = st.sidebar.multiselect(
    "Isla:",
    options=df["Island"].unique().tolist(),
)

st.sidebar.markdown("### 🐧 Filtrar por especie")
filtro_especie = st.sidebar.multiselect(
    "Especie:",
    options=df["Species"].unique().tolist(),
)

# ══════════════════════════════════════════════════════════════════════════════
# 10. FONDOS, BANNER Y SIDEBAR BG
# ══════════════════════════════════════════════════════════════════════════════
set_background("Imagenes/Version_nocturna_del.webp")
render_banner("Imagenes/imagen_pinguinos.png")
render_sidebar_bg("Imagenes/Pingu_fit.webp")

# ══════════════════════════════════════════════════════════════════════════════
# 11. LÓGICA DE FILTROS
# ══════════════════════════════════════════════════════════════════════════════

# Filtro isla
if filtro_isla:
    df_isla = df[df["Island"].isin(filtro_isla)]
    resumen_isla = df_isla.groupby("Species")[[
        "Body Mass (g)", "Culmen Length (mm)", "Culmen Depth (mm)", "Flipper Length (mm)"
    ]].mean().round(2)
    resumen_isla["Nº Pingüinos"] = df_isla.groupby("Species").size()
else:
    df_isla = df
    resumen_isla = None

# Filtro especie
if filtro_especie:
    df_especie = df[df["Species"].isin(filtro_especie)]
    resumen_especie = df_especie.groupby("Island")[[
        "Body Mass (g)", "Culmen Length (mm)", "Culmen Depth (mm)", "Flipper Length (mm)"
    ]].mean().round(2)
    resumen_especie["Nº Pingüinos"] = df_especie.groupby("Island").size()
else:
    df_especie = df
    resumen_especie = None


# ══════════════════════════════════════════════════════════════════════════════
# ── INTRODUCCIÓN ───────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
st.title("Iceberg Intelligence")
render_audio_player("assets/musica_fondo.mp3")

acto_header("Introducción — Equipo y contexto del encargo", "🧊")

with st.expander("👥 About Us — Iceberg Intelligence", expanded=False):
    st.markdown("""
    Iceberg Intelligence nació con una idea sencilla: si solo vemos la punta del iceberg,
    estamos perdiendo el 90% del valor. Por eso analizamos, visualizamos y contamos historias
    con datos para revelar lo que normalmente queda oculto bajo la superficie.

    Somos un equipo que combina análisis, diseño y tecnología para crear dashboards claros,
    modelos fiables y recomendaciones que realmente importan.

    **Integrantes:**
    - **Chiara Contreras**
    - **Jenireé Tovar**
    - **Lucia Llaneza**
    - **Michelle Olivares**
    - **Sara Bailon**
    """)

st.markdown("""
<div style="background-color:rgba(255,255,255,0.08); border-left:4px solid #38bdf8;
            border-radius:0 10px 10px 0; padding:14px 18px; margin:1rem 0;">
    <strong>📋 Encargo:</strong> Convertir el dataset Palmer Penguins en un informe exploratorio
    claro y útil para toma de decisiones científicas de la
    <em>Organización de Investigación Biológica Polar</em>.
</div>
""", unsafe_allow_html=True)

st.subheader("🗺️ Mapa de las islas analizadas")

conteo_islas = df["Island"].value_counts().to_dict()
m = folium.Map(location=[-65.0, -64.5], zoom_start=8)
m.get_root().html.add_child(folium.Element(
    '<h3 align="center" style="font-size:18px"><b>Islas Palmer — Antarctica</b></h3>'
))

islas = {
    "Biscoe":    {"coords": [-65.4333, -65.5000], "color": "blue"},
    "Dream":     {"coords": [-64.7333, -64.2333], "color": "green"},
    "Torgersen": {"coords": [-64.7667, -64.0833], "color": "red"},
}
for nombre, datos in islas.items():
    n = conteo_islas.get(nombre, 0)
    folium.Marker(
        datos["coords"],
        popup=f"Isla {nombre} — {n} 🐧",
        tooltip=f"{nombre}: {n} 🐧",
        icon=folium.Icon(color=datos["color"], icon="info-sign"),
    ).add_to(m)

st_folium(m, width=True, height=400)

with st.expander("📊 Métricas generales del dataset", expanded=True):
    compute_kpis(df)


# ══════════════════════════════════════════════════════════════════════════════
# ── QUÉ ENCONTRAMOS ────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
acto_header("Qué encontramos — Hallazgos del análisis exploratorio", "🔬")

st.markdown("### 🐧 Pregunta 1 — ¿Qué especies predominan y cómo se distribuyen?")

col1, col2 = st.columns(2)
with col1:
    distribucion_especie(df)
with col2:
    if resumen_isla is not None:
        st.markdown("**Resumen filtrado por isla:**")
        st.dataframe(resumen_isla)
    else:
        st.info("Selecciona una isla en la barra lateral para ver el resumen.")

    if resumen_especie is not None:
        st.markdown("**Resumen filtrado por especie:**")
        st.dataframe(resumen_especie)
    else:
        st.info("Selecciona una especie en la barra lateral para ver el resumen.")

st.markdown("---")
st.markdown("### 📐 Preguntas 2 y 3 — ¿Qué diferencias morfológicas hay? ¿Qué variables son más útiles?")

opcion_morfo = st.selectbox(
    "Selecciona el análisis morfológico a mostrar:",
    [
        "Masa corporal por especie",
        "Regresiones lineales (lmplot)",
        "Heatmap de correlaciones",
    ]
)

if opcion_morfo == "Masa corporal por especie":
    grafico_masa_por_especie(df)
elif opcion_morfo == "Regresiones lineales (lmplot)":
    graficos_lmplot(df)
elif opcion_morfo == "Heatmap de correlaciones":
    heatmap_correlaciones(df)


st.markdown("---")
st.markdown("### 📋 Resumen de hallazgos del análisis")
st.caption("Cada hallazgo muestra la evidencia observada, su interpretación, la implicación para el cliente y la recomendación concreta.")

HALLAZGOS = [
    {
        "titulo": "Primer hallazgo — Individual IDs",
        "evidencia": "Observamos un patrón en los IDs individuales: aunque se pierdan los datos o aparezcan como nulos, en su gran mayoría hacen referencia a una pareja (macho/hembra).",
        "interpretacion": "El estudio se enfoca en parejas de pingüinos.",
        "implicacion": "Al tratarse de un dato muy relevante para el estudio, el cliente debe asegurar la calidad de este dato.",
        "recomendacion": "Asignar un número en el individual_ID (1 o 2) dependiendo de si se trata de un macho (ej. 1) o una hembra (ej. 2) para mantener la trazabilidad.",
    },
    {
        "titulo": "Segundo hallazgo — Desequilibrio por especies",
        "evidencia": "Existe una gran diferencia en la cantidad de datos analizados por especie. Chinstrap aporta solo el 20% de las muestras, mientras que Adelie y Gentoo suponen casi el 40% cada una.",
        "interpretacion": "El dataset no está equilibrado para hacer un análisis comparativo por especies.",
        "implicacion": "Para el cliente, las comparaciones entre especies no aportarán valor real.",
        "recomendacion": "Reconsiderar el muestreo de cada especie o especificar mejor si estos datos son relevantes para comparaciones futuras.",
    },
    {
        "titulo": "Tercer hallazgo — Concentración por islas",
        "evidencia": "La toma de muestras está concentrada en las islas Biscoe y Dream; la isla Torgersen supone únicamente el 13%.",
        "interpretacion": "El dataset es escaso para representar una distribución real entre islas.",
        "implicacion": "El análisis puede estar sesgado debido a esta distribución desigual.",
        "recomendacion": "Mejorar la calidad del dato para que las comparativas sean más fieles.",
    },
    {
        "titulo": "Cuarto hallazgo — Similitud morfológica Adelie/Chinstrap",
        "evidencia": "Las especies Adelie y Chinstrap comparten características similares (profundidad del pico y longitud de la aleta), lo que las hace difíciles de separar para interpretar perfiles biológicos.",
        "interpretacion": "Al tener datos similares, las comparaciones entre estas dos especies no son relevantes.",
        "implicacion": "Si el objetivo es obtener diferencias observables entre estas especies, será necesario aportar otros datos.",
        "recomendacion": "Recoger datos más significativos que las diferencien y crear perfiles biológicos más completos.",
    },
    {
        "titulo": "Quinto hallazgo — Escasez de datos temporales",
        "evidencia": "Los datos temporales son muy limitados: solo cubren noviembre y principios de diciembre.",
        "interpretacion": "Probablemente se trate de la época de mayor anidación y reproducción, pero no es posible concluir si la población aumenta o disminuye a lo largo del año.",
        "implicacion": "El cliente tendría datos más fieles del aumento o decrecimiento de la población si se ampliara el periodo de muestreo.",
        "recomendacion": "Mantener un seguimiento anual o estacional para ver la evolución de la distribución poblacional.",
    },
]

numeros = ["①", "②", "③", "④", "⑤"]

with st.expander("📋 Ver todos los hallazgos", expanded=False):
    for i, h in enumerate(HALLAZGOS):
        with st.expander(f"{numeros[i]} {h['titulo']}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(
                    f'<div class="pill-evidencia">'
                    f'<p class="section-label badge-evidencia">🔍 Evidencia observada</p>'
                    f'<p class="section-content">{h["evidencia"]}</p>'
                    f'</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(
                    f'<div class="pill-interpretacion">'
                    f'<p class="section-label badge-interpretacion">🧠 Interpretación</p>'
                    f'<p class="section-content">{h["interpretacion"]}</p>'
                    f'</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(
                    f'<div class="pill-implicacion">'
                    f'<p class="section-label badge-implicacion">💼 Implicación para el cliente</p>'
                    f'<p class="section-content">{h["implicacion"]}</p>'
                    f'</div>', unsafe_allow_html=True)
            with col4:
                st.markdown(
                    f'<div class="pill-recomendacion">'
                    f'<p class="section-label badge-recomendacion">✅ Recomendación concreta</p>'
                    f'<p class="section-content">{h["recomendacion"]}</p>'
                    f'</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── QUÉ NOS FRENA ──────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
acto_header("Qué nos frena — Limitaciones y sesgos del dataset", "⚠️")

st.markdown("### ❓ Pregunta 4 — ¿Qué limitaciones tiene el dataset?")

st.markdown("""
<div style="background-color:#fdecea; border-left:4px solid #d93025;
            padding:12px 16px; border-radius:6px; margin-bottom:1rem;">
  <span style="color:#b71c1c; font-weight:bold; font-size:22px;">
    🛑 Limitación Crítica: Sin datos de comportamiento
  </span><br>
  <span style="color:#5a0000; font-size:18px;">
    No podemos concluir diferencias respecto a migración, reproducción ni anidación.
    Los datos solo cubren morfología.
  </span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("""
        <h4 style="font-size:20px; margin-bottom:6px;">⚖️ Sesgos de Identificación</h4>
        <p style="font-size:18px; line-height:1.5;">
            <strong>IDs reutilizados:</strong> imposible el seguimiento multianual.<br>
            <strong>Errores sistemáticos:</strong> identificación errónea persistente a lo largo de los años.
        </p>
        """, unsafe_allow_html=True)
with col2:
    with st.container(border=True):
        st.markdown("""
        <h4 style="font-size:20px; margin-bottom:6px;">🧬 Barrera Técnica</h4>
        <p style="font-size:18px; line-height:1.5;">
            Las columnas Delta (δ13C, δ15N) requieren conocimiento en biología marina
            para interpretarse correctamente. Sin ese contexto, no podemos incluirlas en el análisis.
        </p>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="background-color:#e8f4fd; border-left:4px solid #1f77b4;
            padding:12px 16px; border-radius:6px; margin-top:1rem;">
  <span style="color:#0A4D8C; font-weight:bold; font-size:20px;">💡 Propuesta para el Cliente</span><br>
  <span style="color:#333333; font-size:18px; line-height:1.5;">
    Implementar una nomenclatura alfanumérica optimizada para garantizar
    trazabilidad y eliminar el sesgo de información en futuras campañas.
  </span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📊 ¿Cuánto mejoraría el análisis si se corrigieran?")
st.pyplot(grafico_resumen_global(LIMITACIONES))

opciones_lim = {f"{l['icono']} {l['titulo']}": l for l in LIMITACIONES}
seleccion_lim = st.selectbox("Ver detalle de una limitación:", list(opciones_lim.keys()))
lim = opciones_lim[seleccion_lim]

st.markdown(f"""
<div class="lim-card" style="border-color: {lim['color']}33;">
    <div class="lim-card-titulo">{lim['icono']} {lim['titulo']}</div>
    <div class="lim-card-desc">{lim['descripcion']}</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.4])
with col1:
    st.markdown("**Gráfico radar — visión global**")
    st.pyplot(grafico_radar(lim))
with col2:
    st.markdown("**Barras comparativas — dimensión a dimensión**")
    st.pyplot(grafico_barras_comparativo(lim))

st.markdown('<p class="seccion-titulo">📋 Impacto estimado en el dataset</p>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("📁 Impacto en registros", lim["impacto_registros"])
with m2:
    st.metric("📐 Nuevas variables", lim["impacto_variables"])
with m3:
    mejora_media = round(np.mean([d - a for d, a in zip(lim["despues"], lim["antes"])]), 1)
    st.metric("📈 Mejora media estimada", f"+{mejora_media} puntos")

st.markdown('<p class="seccion-titulo">✅ Mejoras propuestas al cliente</p>', unsafe_allow_html=True)
for mejora in lim["mejoras"]:
    st.markdown(f"""
    <div style="background:#161b22; border:1px solid #21262d; border-radius:8px;
                padding:10px 14px; margin-bottom:6px; font-size:0.9rem; color:#cbd5e1;">
        ✅ {mejora}
    </div>
    """, unsafe_allow_html=True)

st.markdown('<p class="seccion-titulo">🔬 Análisis que se desbloquearían</p>', unsafe_allow_html=True)
st.markdown(f"""
<div class="nota">
    {lim['analisis_nuevo']}
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── ACTO 4: QUÉ LE DECIMOS AL CLIENTE ───────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
acto_header("Qué le decimos al cliente — Recomendaciones concretas", "🎯")

st.markdown("### ✅ Pregunta 5 — ¿Qué recomendaciones concretas puede aplicar el cliente?")

recomendaciones = [
    {
        "icono": "🔢",
        "area": "Trazabilidad de individuos",
        "accion": "Asignar un ID alfanumérico único por individuo (ej. ADL-F-001) que no se reutilice entre años, especies ni islas.",
        "impacto": "Permite seguimiento real a lo largo del tiempo y elimina errores sistemáticos.",
        "color": "#3b82f6",
    },
    {
        "icono": "⚖️",
        "area": "Equilibrio muestral",
        "accion": "Definir un tamaño muestral mínimo por especie antes de cada campaña. Priorizar Chinstrap (hoy solo 20%) y la isla Torgersen (solo 13%).",
        "impacto": "Hace válidas las comparativas entre especies e islas, eliminando el sesgo de muestreo.",
        "color": "#8b5cf6",
    },
    {
        "icono": "📅",
        "area": "Cobertura temporal",
        "accion": "Ampliar el muestreo a 4 momentos anuales (verano, otoño, invierno, primavera) en lugar de solo noviembre-diciembre.",
        "impacto": "Permite conocer la dinámica poblacional anual y detectar tendencias de conservación.",
        "color": "#10b981",
    },
    {
        "icono": "🐧",
        "area": "Variables de comportamiento",
        "accion": "Añadir variables de fase reproductiva, coordenadas GPS y número de crías por pareja.",
        "impacto": "Desbloquea análisis de migración, reproducción y anidación.",
        "color": "#f59e0b",
    },
    {
        "icono": "🧬",
        "area": "Columnas Delta",
        "accion": "Incorporar metadatos explicativos y rangos de referencia publicados para δ13C y δ15N, o colaborar con un laboratorio especializado.",
        "impacto": "Permite interpretar los isótopos sin riesgo de especulación, añadiendo información sobre dieta y hábitat.",
        "color": "#f87171",
    },
]

for rec in recomendaciones:
    st.markdown(f"""
    <div style="background:white; border-left:5px solid {rec['color']};
                border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:10px;
                box-shadow:0 1px 4px rgba(0,0,0,0.06);">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <span style="font-size:1.4rem;">{rec['icono']}</span>
            <span style="font-weight:700; color:#1e293b; font-size:1rem;">{rec['area']}</span>
        </div>
        <div style="color:#374151; font-size:0.95rem; margin-bottom:6px;">
            <strong>Acción:</strong> {rec['accion']}
        </div>
        <div style="color:{rec['color']}; font-size:0.88rem; font-weight:600;">
            💡 Impacto: {rec['impacto']}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    Dashboard renderizado a -20°C. Compilado entre ventiscas y mucho café + té
    para mantener los insights calientes.
    Informe realizado para Organización de Investigación Biológica Polar por Iceberg Intelligence.
</div>
""", unsafe_allow_html=True)
