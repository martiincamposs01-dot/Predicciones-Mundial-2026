import streamlit as st
import pandas as pd
import os
import time
import urllib.parse

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mundial 2026 | Predicciones Community", page_icon="🏆", layout="wide", initial_sidebar_state="collapsed")

# --- 📸 DICCIONARIO DE IMÁGENES Y ENLACES ---
URL_APP_MUNDIAL = "https://predicciones-mundial-2026-pxopsckekdy9nhzjum8yby.streamlit.app"
IMG_FASE_GRUPOS = "https://i0.wp.com/notivisiongeorgia.com/wp-content/uploads/2025/12/Untitled-design-19.png?fit=1080%2C730&ssl=1"
# 🔥 BANNER PRINCIPAL TRICOLOR (EEUU, MÉXICO, CANADÁ)
BANNER_PRINCIPAL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4U1dDTlr3I-AYiH1mtIXlS6H4Jv0FmkwyTOzfknIBCw&s=10"

# --- ESTILOS CSS (DISEÑO MUNDIALISTA TRICOLOR: AZUL, ROJO, VERDE) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@400;600;800;900&display=swap');

/* Fondo Global (Azul Noche Estadio) */
.stApp { 
    background-color: #030b14; 
    color: #ffffff; 
    font-family: 'Montserrat', sans-serif; 
    background-image: radial-gradient(circle at 50% 0%, #0a1930 0%, #030b14 70%);
}

/* Tipografías Especiales */
h1, h2, h3, .team-name, .vs-text, .weight-class, .stat-title, .stadium-tag { 
    font-family: 'Bebas Neue', sans-serif !important; 
    letter-spacing: 1.5px;
}

header {visibility: hidden;}
footer {visibility: hidden;}

/* Ticker Estilo Deportivo Tricolor */
.ticker-wrap { 
    width: 100%; 
    background: linear-gradient(90deg, #10B981 0%, #3B82F6 50%, #EF4444 100%); 
    color: white; 
    padding: 12px 0; 
    font-family: 'Bebas Neue', sans-serif; 
    font-size: 1.8rem; 
    letter-spacing: 2px; 
    border-radius: 8px; 
    margin-bottom: 30px; 
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.6); 
    text-transform: uppercase;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
}

/* ---------------------------------------------------
   Pestañas (Tabs) ULTRA VISIBLES TRICOLOR
--------------------------------------------------- */
div[data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 3px solid #3B82F6; 
    padding-bottom: 0px;
}

button[data-baseweb="tab"] {
    font-size: 1.6rem !important; 
    font-family: 'Bebas Neue', sans-serif !important; 
    text-transform: uppercase;
    padding: 15px 35px !important; 
    background-color: #0d1b2a !important; 
    border: 2px solid #1e293b !important; 
    border-bottom: none !important;
    border-radius: 12px 12px 0 0 !important; 
    color: #64748b !important; 
    letter-spacing: 2px;
    transition: all 0.3s ease;
}

/* Pestaña Activa (Seleccionada - Azul y Rojo) */
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(180deg, #3B82F6 0%, #1e3a8a 100%) !important;
    color: #ffffff !important; 
    border: 2px solid #60A5FA !important;
    border-bottom: none !important;
    box-shadow: 0 -5px 20px rgba(59, 130, 246, 0.5);
    transform: translateY(-2px);
}

button[data-baseweb="tab"]:hover {
    background-color: #1e293b !important;
    color: #ffffff !important;
}

/* Botones de Acción Principal (Verde Cancha para Guardar) */
.stButton > button {
    background: linear-gradient(90deg, #10B981 0%, #059669 100%); 
    color: #ffffff; 
    font-weight: 900; 
    font-family: 'Montserrat', sans-serif; 
    font-size: 1.3rem; 
    border: 2px solid #34D399; 
    border-radius: 8px; 
    padding: 18px 30px; 
    text-transform: uppercase; 
    letter-spacing: 1px; 
    width: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}
.stButton > button:hover { 
    transform: translateY(-3px); 
    box-shadow: 0 10px 25px rgba(16, 185, 129, 0.8); 
    border: 2px solid #ffffff; 
}

/* Expander para las fechas (Azul oscuro) */
.stExpander { 
    border-radius: 12px !important; 
    border: 1px solid #1e3a8a !important; 
    background-color: #0f172a !important; 
    margin-bottom: 20px; 
}
.stExpander summary p { font-size: 1.5rem !important; font-family: 'Bebas Neue', sans-serif !important; color: #60A5FA !important; letter-spacing: 1px; }

/* Tarjetas de Partido Épicas */
.match-card { 
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); 
    padding: 30px 20px; 
    border-radius: 16px; 
    text-align: center; 
    border-top: 5px solid #EF4444; /* Borde rojo superior */
    border-bottom: 5px solid #3B82F6; /* Borde azul inferior */
    margin-bottom: 25px; 
    box-shadow: 0 15px 35px rgba(0,0,0,0.6); 
    position: relative; 
    overflow: hidden; 
    transition: transform 0.3s ease;
}
.match-card:hover {
    transform: scale(1.02);
    box-shadow: 0 20px 40px rgba(59, 130, 246, 0.4);
}
.match-card::before { 
    content: '🏆'; position: absolute; font-size: 10rem; opacity: 0.04; right: -20px; bottom: -40px; 
}

/* Elementos de Partido */
.flag-huge { font-size: 4.5rem; line-height: 1; filter: drop-shadow(0px 6px 8px rgba(0,0,0,0.6)); margin-bottom: 8px; }
.team-name { font-size: 2.2rem; font-weight: 400; color: #ffffff; text-transform: uppercase; margin-top: 5px; line-height: 1.1; letter-spacing: 1px;}
.vs-text { font-size: 3.5rem; color: #EF4444; font-weight: 400; font-style: italic; text-shadow: 0 0 20px rgba(239, 68, 68, 0.8); margin-top: 25px; }
.group-class { color: #9CA3AF; font-size: 1.3rem; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 15px; font-weight: 600; font-family: 'Montserrat', sans-serif;}

/* Cajas personalizadas */
.custom-box { 
    background: rgba(15, 23, 42, 0.8); 
    border-radius: 12px; 
    padding: 30px; 
    border-left: 5px solid #3B82F6; 
    margin-bottom: 20px; 
    box-shadow: 0 8px 20px rgba(0,0,0,0.5); 
}

/* Inputs de Goles Gigantes (Visual Moderno) */
.stNumberInput > div > div > input { 
    border-radius: 10px !important; font-weight: bold !important; font-family: 'Bebas Neue', sans-serif !important; 
    font-size: 3rem !important; text-align: center !important; background-color: #1e293b !important; 
    color: #ffffff !important; border: 2px solid #3B82F6 !important; height: 80px !important;
}
.stNumberInput > div > div > input:focus { border: 2px solid #10B981 !important; box-shadow: 0 0 15px rgba(16, 185, 129, 0.5) !important;}
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background-color: #0f172a !important; border: 1px solid #3B82F6 !important;
    color: #ffffff !important; border-radius: 8px !important;
    font-family: 'Montserrat', sans-serif !important; font-size: 1.1rem !important;
}

/* 🏆 BANNER ENCUADRE TOP PREMIUM 🏆 */
.banner-container {
    background-size: cover; 
    background-position: center 30%; 
    min-height: 480px; 
    display: flex; 
    flex-direction: column; 
    justify-content: flex-end; 
    align-items: center; 
    padding: 40px 20px; 
    border-radius: 16px; 
    margin-bottom: 25px; 
    border: 3px solid #1e293b; 
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.9);
    position: relative;
}
.banner-container::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(to top, #030b14, rgba(3, 11, 20, 0.2)); border-radius: 13px;
}

/* Responsivo para celulares */
@media (max-width: 768px) {
    .team-name { font-size: 1.5rem; }
    .vs-text { font-size: 2.5rem; margin-top: 30px; }
    .match-card { padding: 20px 10px; }
    button[data-baseweb="tab"] { font-size: 1.1rem !important; padding: 10px 5px !important; }
    .banner-container { min-height: 280px; background-position: center center; justify-content: flex-end; padding-bottom: 20px; }
    .banner-h1 { font-size: 4rem !important; }
    .banner-h2 { font-size: 1.5rem !important; }
    .stNumberInput > div > div > input { font-size: 2.2rem !important; height: 60px !important;}
}
</style>
""", unsafe_allow_html=True)

# --- 🔒 SISTEMA DE SEGURIDAD Y MODERACIÓN BLINDADO ---
PASSWORD_ADMIN = "Cokemma_VAR26!"

BANNED_WORDS = [
    # Generales y contenido explícito
    "puta", "puto", "mierda", "pene", "verga", "pito", "culo", "zorra", 
    "cabron", "maricon", "porno", "sexo",
    # Chilenismos
    "conchetumare", "weon", "aweonao", "culiao", "ctm", 
    # Temas sensibles, nombres y política
    "nazi", "hitler", "epstein", "charlie klirck", "charlie kirk", "klirck",
    # Cultura Narco
    "narco", "chapo", "escobar", "mencho", "cartel",
    # Mexicanismos baneables
    "pendejo", "pinche", "chinga", "chinga tu madre", "joto", "puñetas", "culero", "mamada"
]

def contiene_palabras_baneadas(texto):
    texto_lower = texto.lower()
    return any(palabra in texto_lower for palabra in BANNED_WORDS)

# --- BASES DE DATOS ---
PARTIDOS_FILE = "mundial_partidos_oficial_2026.csv"
PREDICCONES_FILE = "mundial_preds_oficial_2026.csv"
LIGAS_FILE = "mundial_ligas_oficial_2026.csv" 

# --- INICIALIZACIÓN DEL FIXTURE (72 PARTIDOS COMPLETOS) ---
if not os.path.exists(PARTIDOS_FILE):
    partidos_iniciales = [
        {"id": 1, "fecha": "Jueves 11 de junio", "grupo": "Grupo A", "local": "México 🇲🇽", "visita": "Sudáfrica 🇿🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 2, "fecha": "Jueves 11 de junio", "grupo": "Grupo A", "local": "Corea del Sur 🇰🇷", "visita": "República Checa 🇨🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 3, "fecha": "Viernes 12 de junio", "grupo": "Grupo B", "local": "Canadá 🇨🇦", "visita": "Bosnia y Herzegovina 🇧🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 4, "fecha": "Viernes 12 de junio", "grupo": "Grupo D", "local": "Estados Unidos 🇺🇸", "visita": "Paraguay 🇵🇾", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 5, "fecha": "Sábado 13 de junio", "grupo": "Grupo B", "local": "Catar 🇶🇦", "visita": "Suiza 🇨🇭", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 6, "fecha": "Sábado 13 de junio", "grupo": "Grupo C", "local": "Brasil 🇧🇷", "visita": "Marruecos 🇲🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 7, "fecha": "Sábado 13 de junio", "grupo": "Grupo C", "local": "Haití 🇭🇹", "visita": "Escocia 🏴󠁧󠁢󠁳󠁣󠁴󠁿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 8, "fecha": "Sábado 13 de junio", "grupo": "Grupo D", "local": "Australia 🇦🇺", "visita": "Turquía 🇹🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 9, "fecha": "Domingo 14 de junio", "grupo": "Grupo E", "local": "Alemania 🇩🇪", "visita": "Curazao 🇨🇼", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 10, "fecha": "Domingo 14 de junio", "grupo": "Grupo F", "local": "Países Bajos 🇳🇱", "visita": "Japón 🇯🇵", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 11, "fecha": "Domingo 14 de junio", "grupo": "Grupo E", "local": "Costa de Marfil 🇨🇮", "visita": "Ecuador 🇪🇨", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 12, "fecha": "Domingo 14 de junio", "grupo": "Grupo F", "local": "Suecia 🇸🇪", "visita": "Túnez 🇹🇳", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 13, "fecha": "Lunes 15 de junio", "grupo": "Grupo H", "local": "España 🇪🇸", "visita": "Cabo Verde 🇨🇻", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 14, "fecha": "Lunes 15 de junio", "grupo": "Grupo G", "local": "Bélgica 🇧🇪", "visita": "Egipto 🇪🇬", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 15, "fecha": "Lunes 15 de junio", "grupo": "Grupo H", "local": "Arabia Saudí 🇸🇦", "visita": "Uruguay 🇺🇾", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 16, "fecha": "Lunes 15 de junio", "grupo": "Grupo G", "local": "Irán 🇮🇷", "visita": "Nueva Zelanda 🇳🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 17, "fecha": "Martes 16 de junio", "grupo": "Grupo I", "local": "Francia 🇫🇷", "visita": "Senegal 🇸🇳", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 18, "fecha": "Martes 16 de junio", "grupo": "Grupo I", "local": "Irak 🇮🇶", "visita": "Noruega 🇳🇴", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 19, "fecha": "Martes 16 de junio", "grupo": "Grupo J", "local": "Argentina 🇦🇷", "visita": "Argelia 🇩🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 20, "fecha": "Martes 16 de junio", "grupo": "Grupo J", "local": "Austria 🇦🇹", "visita": "Jordania 🇯🇴", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 21, "fecha": "Miércoles 17 de junio", "grupo": "Grupo K", "local": "Portugal 🇵🇹", "visita": "RD Congo 🇨🇩", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 22, "fecha": "Miércoles 17 de junio", "grupo": "Grupo L", "local": "Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "visita": "Croacia 🇭🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 23, "fecha": "Miércoles 17 de junio", "grupo": "Grupo L", "local": "Ghana 🇬🇭", "visita": "Panamá 🇵🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 24, "fecha": "Miércoles 17 de junio", "grupo": "Grupo K", "local": "Uzbekistán 🇺🇿", "visita": "Colombia 🇨🇴", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 25, "fecha": "Jueves 18 de junio", "grupo": "Grupo A", "local": "República Checa 🇨🇿", "visita": "Sudáfrica 🇿🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 26, "fecha": "Jueves 18 de junio", "grupo": "Grupo B", "local": "Suiza 🇨🇭", "visita": "Bosnia y Herzegovina 🇧🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 27, "fecha": "Jueves 18 de junio", "grupo": "Grupo B", "local": "Canadá 🇨🇦", "visita": "Catar 🇶🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 28, "fecha": "Jueves 18 de junio", "grupo": "Grupo A", "local": "México 🇲🇽", "visita": "Corea del Sur 🇰🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 29, "fecha": "Viernes 19 de junio", "grupo": "Grupo D", "local": "Estados Unidos 🇺🇸", "visita": "Australia 🇦🇺", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 30, "fecha": "Viernes 19 de junio", "grupo": "Grupo C", "local": "Escocia 🏴󠁧󠁢󠁳󠁣󠁴󠁿", "visita": "Marruecos 🇲🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 31, "fecha": "Viernes 19 de junio", "grupo": "Grupo C", "local": "Brasil 🇧🇷", "visita": "Haití 🇭🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 32, "fecha": "Viernes 19 de junio", "grupo": "Grupo D", "local": "Turquía 🇹🇷", "visita": "Paraguay 🇵🇾", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 33, "fecha": "Sábado 20 de junio", "grupo": "Grupo F", "local": "Países Bajos 🇳🇱", "visita": "Suecia 🇸🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 34, "fecha": "Sábado 20 de junio", "grupo": "Grupo E", "local": "Alemania 🇩🇪", "visita": "Costa de Marfil 🇨🇮", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 35, "fecha": "Sábado 20 de junio", "grupo": "Grupo E", "local": "Ecuador 🇪🇨", "visita": "Curazao 🇨🇼", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 36, "fecha": "Sábado 20 de junio", "grupo": "Grupo F", "local": "Túnez 🇹🇳", "visita": "Japón 🇯🇵", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 37, "fecha": "Domingo 21 de junio", "grupo": "Grupo H", "local": "España 🇪🇸", "visita": "Arabia Saudí 🇸🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 38, "fecha": "Domingo 21 de junio", "grupo": "Grupo G", "local": "Bélgica 🇧🇪", "visita": "Irán 🇮🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 39, "fecha": "Domingo 21 de junio", "grupo": "Grupo H", "local": "Uruguay 🇺🇾", "visita": "Cabo Verde 🇨🇻", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 40, "fecha": "Domingo 21 de junio", "grupo": "Grupo G", "local": "Nueva Zelanda 🇳🇿", "visita": "Egipto 🇪🇬", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 41, "fecha": "Lunes 22 de junio", "grupo": "Grupo J", "local": "Argentina 🇦🇷", "visita": "Austria 🇦🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 42, "fecha": "Lunes 22 de junio", "grupo": "Grupo I", "local": "Francia 🇫🇷", "visita": "Irak 🇮🇶", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 43, "fecha": "Lunes 22 de junio", "grupo": "Grupo I", "local": "Noruega 🇳🇴", "visita": "Senegal 🇸🇳", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 44, "fecha": "Lunes 22 de junio", "grupo": "Grupo J", "local": "Jordania 🇯🇴", "visita": "Argelia 🇩🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 45, "fecha": "Martes 23 de junio", "grupo": "Grupo K", "local": "Portugal 🇵🇹", "visita": "Uzbekistán 🇺🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 46, "fecha": "Martes 23 de junio", "grupo": "Grupo L", "local": "Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "visita": "Ghana 🇬🇭", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 47, "fecha": "Martes 23 de junio", "grupo": "Grupo L", "local": "Panamá 🇵🇦", "visita": "Croacia 🇭🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 48, "fecha": "Martes 23 de junio", "grupo": "Grupo K", "local": "Colombia 🇨🇴", "visita": "RD Congo 🇨🇩", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 49, "fecha": "Miércoles 24 de junio", "grupo": "Grupo B", "local": "Suiza 🇨🇭", "visita": "Canadá 🇨🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 50, "fecha": "Miércoles 24 de junio", "grupo": "Grupo B", "local": "Bosnia y Herzegovina 🇧🇦", "visita": "Catar 🇶🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 51, "fecha": "Miércoles 24 de junio", "grupo": "Grupo C", "local": "Marruecos 🇲🇦", "visita": "Haití 🇭🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 52, "fecha": "Miércoles 24 de junio", "grupo": "Grupo C", "local": "Escocia 🏴󠁧󠁢󠁳󠁣󠁴󠁿", "visita": "Brasil 🇧🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 53, "fecha": "Miércoles 24 de junio", "grupo": "Grupo A", "local": "Sudáfrica 🇿🇦", "visita": "Corea del Sur 🇰🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 54, "fecha": "Miércoles 24 de junio", "grupo": "Grupo A", "local": "República Checa 🇨🇿", "visita": "México 🇲🇽", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 55, "fecha": "Jueves 25 de junio", "grupo": "Grupo E", "local": "Curazao 🇨🇼", "visita": "Costa de Marfil 🇨🇮", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 56, "fecha": "Jueves 25 de junio", "grupo": "Grupo E", "local": "Ecuador 🇪🇨", "visita": "Alemania 🇩🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 57, "fecha": "Jueves 25 de junio", "grupo": "Grupo F", "local": "Túnez 🇹🇳", "visita": "Países Bajos 🇳🇱", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 58, "fecha": "Jueves 25 de junio", "grupo": "Grupo F", "local": "Japón 🇯🇵", "visita": "Suecia 🇸🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 59, "fecha": "Jueves 25 de junio", "grupo": "Grupo D", "local": "Turquía 🇹🇷", "visita": "Estados Unidos 🇺🇸", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 60, "fecha": "Jueves 25 de junio", "grupo": "Grupo D", "local": "Paraguay 🇵🇾", "visita": "Australia 🇦🇺", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 61, "fecha": "Viernes 26 de junio", "grupo": "Grupo I", "local": "Noruega 🇳🇴", "visita": "Francia 🇫🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 62, "fecha": "Viernes 26 de junio", "grupo": "Grupo I", "local": "Senegal 🇸🇳", "visita": "Irak 🇮🇶", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 63, "fecha": "Viernes 26 de junio", "grupo": "Grupo H", "local": "Cabo Verde 🇨🇻", "visita": "Arabia Saudí 🇸🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 64, "fecha": "Viernes 26 de junio", "grupo": "Grupo H", "local": "Uruguay 🇺🇾", "visita": "España 🇪🇸", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 65, "fecha": "Viernes 26 de junio", "grupo": "Grupo G", "local": "Nueva Zelanda 🇳🇿", "visita": "Bélgica 🇧🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 66, "fecha": "Viernes 26 de junio", "grupo": "Grupo G", "local": "Egipto 🇪🇬", "visita": "Irán 🇮🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 67, "fecha": "Sábado 27 de junio", "grupo": "Grupo L", "local": "Panamá 🇵🇦", "visita": "Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 68, "fecha": "Sábado 27 de junio", "grupo": "Grupo L", "local": "Croacia 🇭🇷", "visita": "Ghana 🇬🇭", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 69, "fecha": "Sábado 27 de junio", "grupo": "Grupo K", "local": "Colombia 🇨🇴", "visita": "Portugal 🇵🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 70, "fecha": "Sábado 27 de junio", "grupo": "Grupo K", "local": "RD Congo 🇨🇩", "visita": "Uzbekistán 🇺🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 71, "fecha": "Sábado 27 de junio", "grupo": "Grupo J", "local": "Argelia 🇩🇿", "visita": "Austria 🇦🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 72, "fecha": "Sábado 27 de junio", "grupo": "Grupo J", "local": "Jordania 🇯🇴", "visita": "Argentina 🇦🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
    ]
    pd.DataFrame(partidos_iniciales).to_csv(PARTIDOS_FILE, index=False)

if not os.path.exists(PREDICCONES_FILE): pd.DataFrame(columns=["usuario", "liga", "partido_id", "goles_l_pred", "goles_v_pred"]).to_csv(PREDICCONES_FILE, index=False)
if not os.path.exists(LIGAS_FILE): pd.DataFrame(columns=["nombre_liga", "clave_liga", "creador"]).to_csv(LIGAS_FILE, index=False)

df_partidos = pd.read_csv(PARTIDOS_FILE)
df_partidos["goles_l_real"] = df_partidos["goles_l_real"].astype(str)
df_partidos["goles_v_real"] = df_partidos["goles_v_real"].astype(str)
df_predicciones = pd.read_csv(PREDICCONES_FILE)
df_ligas = pd.read_csv(LIGAS_FILE)
lista_fechas = df_partidos["fecha"].unique()

# --- FUNCIONES AUXILIARES ---
def calcular_tabla(df_p, df_preds, liga_filtro=None):
    if df_preds.empty: return pd.DataFrame(columns=["Participante", "Rango 🎖️", "Puntos Totales", "Exactos (3pts)", "Tendencias (1pt)"])
    if liga_filtro and liga_filtro.strip().upper() != "GLOBAL":
        df_preds = df_preds[df_preds["liga"].str.upper() == liga_filtro.strip().upper()]
        if df_preds.empty: return pd.DataFrame(columns=["Participante", "Rango 🎖️", "Puntos Totales", "Exactos (3pts)", "Tendencias (1pt)"])

    puntajes = {user: {"puntos": 0, "exactos": 0, "tendencias": 0} for user in df_preds["usuario"].unique()}
    partidos_jugados = df_p[df_p["jugado"] == True]
    
    for _, pred in df_preds.iterrows():
        user = pred["usuario"]
        p_id = int(pred["partido_id"])
        
        partido_real = list(partidos_jugados[partidos_jugados["id"] == p_id].to_dict(orient="index").values())
        if not partido_real: continue
        
        p_real = partido_real[0]
        
        try:
            gl_real = int(float(p_real["goles_l_real"]))
            gv_real = int(float(p_real["goles_v_real"]))
            gl_pred = int(pred["goles_l_pred"])
            gv_pred = int(pred["goles_v_pred"])
            
            if gl_real == gl_pred and gv_real == gv_pred:
                puntajes[user]["puntos"] += 3
                puntajes[user]["exactos"] += 1
            elif (gl_real > gv_real and gl_pred > gv_pred) or (gl_real < gv_real and gl_pred < gv_pred) or (gl_real == gv_real and gl_pred == gv_pred):
                puntajes[user]["puntos"] += 1
                puntajes[user]["tendencias"] += 1
        except ValueError:
            pass

    tabla_data = []
    for u, stats in puntajes.items():
        p = stats["puntos"]
        rango = "Calentando motores 🏃"
        if p >= 50: rango = "Oráculo Mundialista 🔮"
        elif p >= 30: rango = "Director Técnico 👔"
        elif p >= 10: rango = "Analista Táctico 📋"
        elif p > 0: rango = "Puro Vendehumo 🪵"
        tabla_data.append([u, rango, p, stats["exactos"], stats["tendencias"]])
        
    df_tabla = pd.DataFrame(tabla_data, columns=["Participante", "Rango 🎖️", "Puntos Totales", "Exactos (3pts)", "Tendencias (1pt)"])
    return df_tabla.sort_values(by=["Puntos Totales", "Exactos (3pts)"], ascending=[False, False]).reset_index(drop=True)

def parse_team(team_string):
    parts = team_string.split()
    flag = parts[-1]
    name = " ".join(parts[:-1])
    return name, flag

# --- BANNER PRINCIPAL ANIMADO Y ÉPICO TRICOLOR ---
st.markdown(f"""
<div class="banner-container" style="background-image: linear-gradient(to bottom, rgba(3, 11, 20, 0.3) 0%, rgba(3, 11, 20, 0.95) 100%), url('{BANNER_PRINCIPAL}');">
    <h1 class="banner-h1" style="color: #ffffff; font-size: 7.5rem; margin-top:10px; margin-bottom:0px; line-height: 1; text-transform: uppercase; letter-spacing: 6px; text-shadow: 4px 4px 15px rgba(239, 68, 68, 0.9); font-family: 'Bebas Neue', sans-serif; z-index: 2;">MUNDIAL <span style="color:#10B981;">2026</span></h1>
    <h2 class="banner-h2" style="color: #60A5FA; font-size: 3rem; margin-top: 10px; font-weight: 400; letter-spacing: 4px; font-family: 'Bebas Neue', sans-serif; text-shadow: 2px 2px 10px black; z-index: 2;">🇺🇸 EEUU <span style="color:white;">•</span> 🇲🇽 MÉXICO <span style="color:white;">•</span> 🇨🇦 CANADÁ</h2>
</div>
""", unsafe_allow_html=True)

# --- TICKER DE NOTICIAS ---
st.markdown("""
<div class="ticker-wrap">
    <marquee scrollamount="12">🚨 EN VIVO: EL MUNDIAL SE VIVE AQUÍ | ⚽ ¡Sella tus pronósticos antes del pitazo inicial!... 🏆 ¿Quién levantará la copa este año?... 📊 Crea tu liga privada y reta a tus amigos...</marquee>
</div>
""", unsafe_allow_html=True)

# --- PESTAÑAS NOMBRADAS EXPLÍCITAMENTE (PREDICCIONES PRIMERO) ---
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 LOBBY", "📝 PREDICCIONES ⚽", "🏆 RÁNKINGS", "ℹ️ INFO", "📺 EL VAR", "🔒 ÁRBITRO"])

# --- PESTAÑA 0: LOBBY REORGANIZADO ---
with tab0:
    
    # 🔥 SECCIÓN DE COMPARTIR TRICOLOR
    url_whatsapp = f"https://api.whatsapp.com/send?text={urllib.parse.quote('🏆 ¡Únete a la liga de pronósticos del Mundial 2026! ⚽ Deja tus resultados aquí: ' + URL_APP_MUNDIAL)}"
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #3B82F6 0%, #1e3a8a 100%); padding: 2px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);">
        <div style="background-color: #0d1b2a; padding: 20px 25px; border-radius: 10px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
            <div style="flex: 1;">
                <h3 style="color: #60A5FA; font-family: 'Bebas Neue', sans-serif; letter-spacing: 1.5px; font-size: 2.2rem; margin:0; text-transform: uppercase;">
                    🌍 INVITA A TUS AMIGOS
                </h3>
                <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 1rem;">Copia el enlace de abajo o comparte directamente con un clic.</p>
            </div>
            <div style="display: flex; gap: 15px; align-items: center;">
                <a href="{url_whatsapp}" target="_blank" style="text-decoration:none;">
                    <div style="background-color: #25D366; width: 45px; height: 45px; border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 10px rgba(37, 211, 102, 0.4); transition: transform 0.2s;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="25">
                    </div>
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.code(URL_APP_MUNDIAL, language="text")
    st.markdown("<br><hr style='border-color: #1e293b;'><br>", unsafe_allow_html=True)

    # 🔥 BLOQUE DE INSTALACIÓN COMO APP
    st.markdown("""
<div style="background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%); color: #ffffff; padding: 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);">
<h3 style="margin-top: 0; color: #ffffff; display: flex; align-items: center; font-weight: 900; text-shadow: 1px 1px 2px black;">📲 ¡Lleva el Mundial en tu Bolsillo!</h3>
<p style="font-weight: 800; font-size: 1.05rem; margin-bottom: 8px; font-family: 'Montserrat', sans-serif; text-shadow: 1px 1px 2px black;">Instala esta web como una App nativa para no perderte nada:</p>
<div style="background-color: rgba(3, 11, 20, 0.9); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #EF4444;">
<span style="font-size: 0.95rem; color: #EF4444; font-weight: bold; font-family: 'Montserrat', sans-serif;">⚠️ ¿Atrapado en el navegador de TikTok o Instagram?</span><br>
<span style="font-size: 0.85rem; color: #cbd5e1; font-family: 'Montserrat', sans-serif;">Las redes sociales bloquean la instalación. Para solucionarlo:</span><br>
<ol style="font-size: 0.85rem; color: #cbd5e1; margin-top: 5px; margin-bottom: 0; padding-left: 20px; font-family: 'Montserrat', sans-serif;">
<li>Toca la barra superior blanca que dice <em>"Estás en..."</em> o busca los 3 puntitos.</li>
<li>Copia el enlace de la página.</li>
<li>Abre <strong>Safari</strong> (iPhone) o <strong>Chrome</strong> (Android) y pega el enlace ahí.</li>
</ol>
</div>
<ul style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0; font-family: 'Montserrat', sans-serif; text-shadow: 1px 1px 2px black;">
<li><strong>🍏 Una vez en Safari:</strong> Toca 'Compartir' (📤) abajo ➔ <strong>➕ Agregar a inicio</strong>.</li>
<li><strong>🤖 Una vez en Chrome:</strong> Toca los 3 puntos (⋮) arriba ➔ <strong>📱 Agregar a la pantalla principal</strong>.</li>
</ul>
</div>
    """, unsafe_allow_html=True)

    # 🔥 SECCIÓN VISUAL DE LOS GRUPOS OFICIALES
    st.markdown("<h2 style='text-align: center; color: #3B82F6; text-transform: uppercase;'>🏆 FASE DE GRUPOS OFICIAL</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px;'>
        <img src='{IMG_FASE_GRUPOS}' style='width: 100%; max-width: 800px; border-radius: 12px; border: 2px solid #3B82F6; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4);'>
    </div>
    """, unsafe_allow_html=True)
    
    # 🔥 REGLAS DE PUNTUACIÓN
    st.markdown("""
<div class="custom-box">
    <h2 style="color: #3B82F6; margin-top: 0; font-size: 2.8rem;">📜 REGLAS DE PUNTUACIÓN</h2>
    <ul style="color: #cbd5e1; font-size: 1.2rem; line-height: 1.8; font-family: 'Montserrat', sans-serif;">
        <li><strong style="color: #10B981;">+3 Puntos (Pleno):</strong> ¡Le achuntaste al resultado exacto! (Ej: Predices 2-1 y termina 2-1).</li>
        <li><strong style="color: #60A5FA;">+1 Punto (Tendencia):</strong> Le achuntaste al ganador o al empate, pero no a los goles exactos.</li>
        <li><strong style="color: #EF4444;">+0 Puntos:</strong> No le achuntaste a nada. Suerte para la próxima.</li>
    </ul>
</div>
    """, unsafe_allow_html=True)

    # 🔥 CONTADOR DE DIRECTORES TÉCNICOS
    total_peleadores = df_predicciones["usuario"].nunique() if not df_predicciones.empty else 0
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #EF4444 0%, #991b1b 100%); padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4); border: 2px solid #fca5a5;">
        <h2 style="color: white; margin: 0; font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; font-size: 2.2rem; text-shadow: 2px 2px 5px black;">
            ⚽ {total_peleadores} DIRECTOR TÉCNICOS YA ESTÁN EN LA CANCHA
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # DIRECTORIO DE LIGAS
    st.markdown("<h2 style='color: #ffffff; margin-top:40px; margin-bottom: 25px; font-size: 3rem;'>📋 DIRECTORIO DE LIGAS</h2>", unsafe_allow_html=True)
    if not df_ligas.empty:
        ligas_texto = " | ".join([f"🎟️ {row['nombre_liga']}" for _, row in df_ligas.iterrows()])
        st.markdown(f"""
        <div style="background-color: #0f172a; color: #60A5FA; padding: 10px; border-radius: 8px; font-family: 'Montserrat', sans-serif; font-size: 1rem; border: 1px solid #1e293b;">
            <marquee scrollamount="8">🔥 LIGAS PRIVADAS ACTIVAS: {ligas_texto}</marquee>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Aún no hay ligas privadas creadas. Ve a la pestaña 'PREDICCIONES' y sé el primero.")

# --- PESTAÑA 1: PREDICCIONES (PRIORIDAD Y GUARDADO POR DÍA) ---
with tab1:
    st.markdown("<h2 style='color: #ffffff; text-align:center; font-size: 3.5rem;'>📝 TUS PRONÓSTICOS</h2>", unsafe_allow_html=True)
    
    # 🔥 SEGURIDAD: LÍMITE DE CARACTERES EN EL APODO
    usuario_input = st.text_input("👤 INGRESA TU APODO (Hazte Famoso):", placeholder="Ej. El Analista", max_chars=20)
    usuario_limpio = usuario_input.strip().title()
    
    opcion_liga = st.selectbox("🤝 ¿DÓNDE QUIERES COMPETIR?", ["🌍 Ranking Global (Público)", "➕ Crear Liga Privada", "🔐 Unirse a Liga Existente"])
    liga_limpia, clave_ingresada, clave_creada, liga_nueva = "GLOBAL", "", "", ""
    
    if opcion_liga == "➕ Crear Liga Privada":
        col_nl, col_cl = st.columns(2)
        with col_nl: liga_nueva = st.text_input("Nombre de Liga:")
        with col_cl: clave_creada = st.text_input("Clave Secreta:")
        liga_limpia = liga_nueva.strip().upper()
    elif opcion_liga == "🔐 Unirse a Liga Existente":
        ligas_disp = df_ligas["nombre_liga"].tolist()
        if ligas_disp:
            col_sel, col_pass = st.columns(2)
            with col_sel: liga_seleccionada = st.selectbox("Selecciona Liga:", ligas_disp)
            with col_pass: clave_ingresada = st.text_input("Contraseña:", type="password")
            liga_limpia = liga_seleccionada
        else: st.error("No hay ligas privadas aún.")

    if usuario_limpio:
        st.markdown("---")
        
        es_baneado = contiene_palabras_baneadas(usuario_limpio)
        
        # 🔥 EL FIX MAESTRO: Validar si el nombre ya está registrado SOLO en la liga seleccionada
        ya_registrado = not df_predicciones[(df_predicciones["usuario"] == usuario_limpio) & (df_predicciones["liga"] == liga_limpia)].empty
        acaba_de_guardar = st.session_state.get("usuario_registrado") == usuario_limpio
        
        # 🔥 SEGURIDAD Y PREVENCIÓN DE DUPLICADOS DENTRO DE LA MISMA LIGA
        if es_baneado:
            st.error("🚨 ¡Epa! Ese apodo contiene palabras no permitidas. Por favor, usa otro.")
        elif ya_registrado and not acaba_de_guardar:
            st.error(f"🚨 ¡NOMBRE OCUPADO EN ESTA LIGA! El apodo '{usuario_limpio}' ya envió predicciones en '{liga_limpia}'. Si no eres tú, por favor cambia tu nombre arriba.")
        
        if not es_baneado and (not ya_registrado or acaba_de_guardar):
            
            # --- BOTÓN DE ALARDEAR ---
            if acaba_de_guardar:
                texto_wa = f"🏆 ¡Sellé mi cartilla para el Mundial 2026 en la liga {liga_limpia}! 🔥 ¿Crees que sabes más de fútbol que yo? ¡Entra y supérame aquí: {URL_APP_MUNDIAL}"
                link_wa = f"https://api.whatsapp.com/send?text={urllib.parse.quote(texto_wa)}"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #10B981 0%, #047857 100%); padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 30px; border: 2px solid #34D399; box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);">
                    <h3 style="color: white; margin-top: 0; font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; letter-spacing: 1px; text-shadow: 1px 1px 2px black;">✅ ¡PRONÓSTICOS GUARDADOS!</h3>
                    <p style="color: #ecfdf5; font-size: 1.2rem; margin-bottom: 20px; font-family: 'Montserrat', sans-serif;">Tus predicciones ya están en el sistema. ¡Desafía a tus amigos por WhatsApp!</p>
                    <a href="{link_wa}" target="_blank" style="text-decoration: none; display: inline-block; background-color: #ffffff; color: #047857; padding: 15px 30px; border-radius: 8px; font-weight: 800; font-family: 'Montserrat', sans-serif; font-size: 1.1rem; text-transform: uppercase; box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: transform 0.2s;">
                        📲 ALARDEAR MIS PRONÓSTICOS
                    </a>
                </div>
                """, unsafe_allow_html=True)
            
            st.info("💡 **Guarda tus pronósticos por día.** Abre la fecha, ingresa tus resultados y presiona el botón Guardar verde que está debajo de esos partidos.")
            
            # 🔥 GUARDADO INDEPENDIENTE POR DÍA CON DISEÑO LIMPIO
            for fecha in lista_fechas:
                partidos_dia = df_partidos[df_partidos["fecha"] == fecha]
                todos_jugados = partidos_dia["jugado"].all()
                
                estado_fecha = "✅ FINALIZADOS" if todos_jugados else "🗓️"
                
                with st.expander(f"{estado_fecha} {fecha}", expanded=False):
                    if todos_jugados:
                        st.success("Todos los partidos de esta fecha ya han finalizado. Resultados cerrados.")
                        
                    with st.form(f"form_{fecha}"):
                        for _, row in partidos_dia.iterrows():
                            p_id_f = int(row["id"])
                            # 🔥 CARGAR PREDICCIÓN ESPECÍFICA DE ESTE USUARIO EN ESTA LIGA
                            pred_existente = df_predicciones[(df_predicciones["usuario"] == usuario_limpio) & (df_predicciones["liga"] == liga_limpia) & (df_predicciones["partido_id"] == p_id_f)]
                            
                            val_l = int(pred_existente.iloc[0]["goles_l_pred"]) if not pred_existente.empty else 0
                            val_v = int(pred_existente.iloc[0]["goles_v_pred"]) if not pred_existente.empty else 0
                            
                            l_name, l_flag = parse_team(row['local'])
                            v_name, v_flag = parse_team(row['visita'])

                            html_tarjeta = f"""
                            <div class='match-card'>
                                <div class='group-class'>{row['grupo']}</div>
                                <div style='display:flex; justify-content:space-around; align-items:center;'>
                                    <div style='width:35%;'>
                                        <div class='flag-huge'>{l_flag}</div>
                                        <div class='team-name'>{l_name}</div>
                                    </div>
                                    <div style='width:30%;'>
                                        <div class='vs-text'>VS</div>
                                    </div>
                                    <div style='width:35%;'>
                                        <div class='flag-huge'>{v_flag}</div>
                                        <div class='team-name'>{v_name}</div>
                                    </div>
                                </div>
                            </div>
                            """
                            st.markdown(html_tarjeta, unsafe_allow_html=True)
                            
                            esta_bloqueado = bool(row["jugado"])
                            if esta_bloqueado:
                                try:
                                    st.markdown(f"<p style='text-align:center; color:#EF4444; font-weight:bold; font-size:1.2rem; font-family: \"Montserrat\", sans-serif;'>🛑 FINALIZADO | Real: {int(float(row['goles_l_real']))} - {int(float(row['goles_v_real']))}</p>", unsafe_allow_html=True)
                                except ValueError: pass

                            col1, col2 = st.columns(2)
                            with col1: st.number_input(f"Goles {l_name}", min_value=0, max_value=15, value=val_l, step=1, key=f"l_{p_id_f}", disabled=esta_bloqueado)
                            with col2: st.number_input(f"Goles {v_name}", min_value=0, max_value=15, value=val_v, step=1, key=f"v_{p_id_f}", disabled=esta_bloqueado)
                            st.markdown("<br><hr style='border-color: #1e293b;'><br>", unsafe_allow_html=True)
                            
                        # Botón Submit POR DÍA
                        if st.form_submit_button(f"🔒 GUARDAR PRONÓSTICOS: {fecha}", disabled=todos_jugados):
                            acceso = True
                            
                            if opcion_liga == "➕ Crear Liga Privada":
                                if not liga_nueva or not clave_creada: st.error("Faltan datos de la liga."); acceso = False
                                else:
                                    liga_existente = df_ligas[df_ligas["nombre_liga"] == liga_limpia]
                                    if not liga_existente.empty:
                                        if str(liga_existente.iloc[0]["creador"]) != usuario_limpio:
                                            st.error("❌ Ese nombre de liga ya existe y pertenece a otro usuario. Elige otro.")
                                            acceso = False
                                    else:
                                        df_ligas = pd.concat([df_ligas, pd.DataFrame([{"nombre_liga": liga_limpia, "clave_liga": clave_creada, "creador": usuario_limpio}])], ignore_index=True)
                                        df_ligas.to_csv(LIGAS_FILE, index=False)
                            elif opcion_liga == "🔐 Unirse a Liga Existente" and ligas_disp:
                                if str(clave_ingresada) != str(df_ligas[df_ligas["nombre_liga"] == liga_limpia]["clave_liga"].values[0]):
                                    st.error("Contraseña incorrecta."); acceso = False

                            if acceso:
                                for _, row in partidos_dia.iterrows():
                                    p_id_s = int(row["id"])
                                    if row["jugado"]: continue
                                    g_l_v = st.session_state[f"l_{p_id_s}"]
                                    g_v_v = st.session_state[f"v_{p_id_s}"]
                                    
                                    # 🔥 EL FIX MAESTRO PARA NO BORRAR DATOS DE OTRAS LIGAS
                                    df_predicciones = df_predicciones[~((df_predicciones["usuario"] == usuario_limpio) & (df_predicciones["liga"] == liga_limpia) & (df_predicciones["partido_id"] == p_id_s))]
                                    
                                    nueva_p = {"usuario": usuario_limpio, "liga": liga_limpia, "partido_id": p_id_s, "goles_l_pred": int(g_l_v), "goles_v_pred": int(g_v_v)}
                                    df_predicciones = pd.concat([df_predicciones, pd.DataFrame([nueva_p])], ignore_index=True)
                                
                                df_predicciones.to_csv(PREDICCONES_FILE, index=False)
                                
                                st.session_state["usuario_registrado"] = usuario_limpio
                                
                                st.toast(f'¡Pronósticos de {fecha} asegurados!', icon='🏆')
                                st.markdown("""
                                <div style="text-align:center; animation: shake 0.5s;">
                                    <h1 style="color: #10B981; font-size: 6rem; font-family: 'Bebas Neue', sans-serif; text-shadow: 2px 2px 10px black;">¡GOL! ⚽</h1>
                                    <p style="font-size: 1.8rem; color:white; font-family:'Bebas Neue', sans-serif; letter-spacing:2px;">¡CARTILLA OFICIAL EN LA CANCHA!</p>
                                </div>
                                """, unsafe_allow_html=True)
                                st.snow()
                                time.sleep(2)
                                st.rerun()

# --- PESTAÑA 2: RÁNKINGS (Buscador y Scroll) ---
with tab2:
    st.markdown("<h2 style='color: #3B82F6; font-size: 3.5rem;'>🏅 TABLA DE POSICIONES OFICIAL</h2>", unsafe_allow_html=True)
    
    opciones_ligas = ["GLOBAL"]
    if not df_ligas.empty: opciones_ligas.extend(sorted(df_ligas["nombre_liga"].unique().tolist()))
    
    # 🔥 BÚSQUEDA Y FILTRO
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        liga_busqueda = st.selectbox("🔍 Filtrar por Liga:", opciones_ligas).strip().upper()
    with col_filtro2:
        busqueda_usuario = st.text_input("🔍 Buscar mi apodo:")
    
    df_ranking = calcular_tabla(df_partidos, df_predicciones, liga_busqueda)
    
    if busqueda_usuario:
        df_ranking = df_ranking[df_ranking["Participante"].str.contains(busqueda_usuario, case=False, na=False)]
        
    if not df_ranking.empty: 
        if len(df_ranking) >= 3 and not busqueda_usuario:
            st.markdown("### 🏟️ El Podio Actual")
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("🥇 1er Lugar", df_ranking.iloc[0]["Participante"], f"{df_ranking.iloc[0]['Puntos Totales']} pts")
            with col2: st.metric("🥈 2do Lugar", df_ranking.iloc[1]["Participante"], f"{df_ranking.iloc[1]['Puntos Totales']} pts")
            with col3: st.metric("🥉 3er Lugar", df_ranking.iloc[2]["Participante"], f"{df_ranking.iloc[2]['Puntos Totales']} pts")
            st.markdown("---")
        
        # 🔥 SCROLL: height=400 limita la tabla para que no sea infinita
        st.dataframe(df_ranking, use_container_width=True, hide_index=True, height=400)
    else: 
        st.info("Aún no hay predictores registrados o no se encontraron resultados.")

# --- PESTAÑA 3: INFO (Estadísticas Reales Añadidas) ---
with tab3:
    st.header("ℹ️ Información del Torneo")
    st.markdown("""
    <div class="custom-box">
        <h2 style="color: #60A5FA; margin-top: 0;">⚽ Curiosidades Norteamérica 2026</h2>
        <ul style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.8; font-family: 'Montserrat', sans-serif;">
            <li>Primera vez en la historia que el Mundial se juega en <strong>3 países simultáneamente</strong>.</li>
            <li>El torneo cuenta con un récord de <strong>48 selecciones</strong> participantes.</li>
            <li>El Estadio Azteca de México se convierte en el único recinto en albergar partidos en tres Copas del Mundo distintas.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("⏱️ Avance del Torneo")
    jugados = len(df_partidos[df_partidos["jugado"] == True])
    st.progress(jugados / len(df_partidos) if len(df_partidos) > 0 else 0)
    st.write(f"**Partidos finalizados:** {jugados} de {len(df_partidos)}")

# --- PESTAÑA 4: EL VAR (STATS EXPANDIDAS) ---
with tab4:
    st.markdown("""
    <div style="background-image: linear-gradient(rgba(3, 11, 20, 0.6), rgba(3, 11, 20, 0.9)), url('https://images.unsplash.com/photo-1508344928928-7137b29de216?auto=format&fit=crop&w=1200&q=80'); background-size: cover; background-position: center; padding: 30px; border-radius: 12px; margin-bottom: 20px; border-bottom: 4px solid #3B82F6;">
        <h1 style="color: #60A5FA; margin:0; text-transform: uppercase; font-family: 'Bebas Neue', sans-serif; font-size: 4rem;">📺 Sala del VAR</h1>
        <p style="color: #cbd5e1; margin-top: 5px; font-family: 'Montserrat', sans-serif; font-size: 1.1rem;">Análisis en vivo de las tendencias globales de los apostadores.</p>
    </div>
    """, unsafe_allow_html=True)
    if df_predicciones.empty:
        st.info("Aún no hay suficientes predicciones para mostrar las estadísticas.")
    else:
        col1, col2 = st.columns(2)
        total_apuestas = len(df_predicciones["usuario"].unique())
        total_goles_predichos = df_predicciones["goles_l_pred"].sum() + df_predicciones["goles_v_pred"].sum()
        with col1: st.metric("👥 Directores Técnicos (Globales)", total_apuestas)
        with col2: st.metric("⚽ Goles Totales Pronosticados", total_goles_predichos)
        st.markdown("---")
        st.subheader("📊 Tendencia de Goles Promedio por Partido")
        df_predicciones["Total_Goles_Predichos"] = df_predicciones["goles_l_pred"] + df_predicciones["goles_v_pred"]
        chart_data = df_predicciones["Total_Goles_Predichos"].value_counts().sort_index()
        st.bar_chart(chart_data, color="#3B82F6")

# --- PESTAÑA 5: ADMIN ---
with tab5:
    st.markdown("<h2 style='color: #EF4444; font-size: 3.5rem;'>🔒 CAMARÍN DEL ÁRBITRO (OFFICIALS ONLY)</h2>", unsafe_allow_html=True)
    if st.text_input("Ingresa la credencial de acceso:", type="password") == PASSWORD_ADMIN:
        with st.form("admin_form"):
            for fecha in lista_fechas:
                st.markdown(f"### 🗓️ {fecha}")
                partidos_dia = df_partidos[df_partidos["fecha"] == fecha]
                for idx, row in partidos_dia.iterrows():
                    l_name, l_flag = parse_team(row['local'])
                    v_name, v_flag = parse_team(row['visita'])
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1: st.write(f"**{l_flag} {l_name} vs {v_name} {v_flag}**")
                    with col2:
                        try: val_l_real = int(float(row["goles_l_real"])) if row["jugado"] else 0
                        except ValueError: val_l_real = 0
                        g_l_r = st.number_input("Local", min_value=0, max_value=15, value=val_l_real, key=f"rl_{row['id']}")
                    with col3:
                        try: val_v_real = int(float(row["goles_v_real"])) if row["jugado"] else 0
                        except ValueError: val_v_real = 0
                        g_v_r = st.number_input("Visita", min_value=0, max_value=15, value=val_v_real, key=f"rv_{row['id']}")
                    with col4: marcar_jugado = st.checkbox("¿Terminó?", value=row["jugado"], key=f"j_{row['id']}")
                    st.markdown("---")
            if st.form_submit_button("CERRAR RESULTADOS OFICIALES"):
                for idx, row in df_partidos.iterrows():
                    p_id = row["id"]
                    df_partidos.at[idx, "goles_l_real"] = str(int(st.session_state[f"rl_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "goles_v_real"] = str(int(st.session_state[f"rv_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "jugado"] = bool(st.session_state[f"j_{p_id}"])
                df_partidos.to_csv(PARTIDOS_FILE, index=False)
                st.success('Resultados Guardados Oficialmente.')
                time.sleep(1)
                st.rerun()

# --- PIE DE PÁGINA ---
st.markdown("""
<div style="text-align: center; margin-top: 60px; padding: 25px; border-top: 1px solid #1e293b;">
    <p style="color: #94a3b8; font-size: 1.1rem; font-weight:600;">Mundial 2026 Predictions © 2026</p>
</div>
""", unsafe_allow_html=True)
