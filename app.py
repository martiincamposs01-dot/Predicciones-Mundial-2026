import streamlit as st
import pandas as pd
import os
import time
import urllib.parse

# --- CONFIGURACIÓN DE PÁGINA (ÍCONO EMOJI INFALIBLE) ---
st.set_page_config(page_title="Mundial 2026", page_icon="🏆", layout="wide")

# --- ENLACES Y RECURSOS ---
URL_APP_MUNDIAL = "https://predicciones-mundial-2026-pxopsckekdy9nhzjum8yby.streamlit.app"
URL_NOTICIA_GRUPOS = "https://notivisiongeorgia.com/2025/12/05/asi-quedaron-los-grupos-de-la-copa-mundial-2026/"
URL_IMAGEN_GRUPOS = "https://i0.wp.com/notivisiongeorgia.com/wp-content/uploads/2025/12/Untitled-design-19.png?fit=1080%2C730&ssl=1"

# --- ESTILOS CSS (TIPOGRAFÍA ÉPICA Y MODO ESTADIO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@400;700;900&display=swap');
    
    .stApp { background-color: #0b101a; color: #ffffff; font-family: 'Roboto', sans-serif; }
    
    h1, h2, h3, .team-name, .vs-text, button[data-baseweb="tab"] { 
        font-family: 'Bebas Neue', sans-serif !important; 
        letter-spacing: 1px; 
    }
    
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 15px rgba(0, 255, 135, 0.4); }
        50% { box-shadow: 0 0 30px rgba(0, 255, 135, 0.8); }
        100% { box-shadow: 0 0 15px rgba(0, 255, 135, 0.4); }
    }
    
    button[data-baseweb="tab"] {
        font-size: 1.5rem !important; 
        text-transform: uppercase;
        padding: 10px 20px !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00FF87 0%, #60EFFF 100%);
        color: #000000; font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; border: none; border-radius: 12px;
        padding: 10px 24px; transition: all 0.3s ease; letter-spacing: 2px; width: 100%;
    }
    .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0, 255, 135, 0.6); color: #000; }
    
    .stExpander { border-radius: 12px !important; border: 1px solid #1f2937 !important; background-color: #111827 !important; margin-bottom: 15px; }
    
    .match-card { 
        background: linear-gradient(180deg, #1f2937 0%, #0d131f 100%); 
        padding: 15px; border-radius: 12px; text-align: center; 
        border-top: 4px solid #00FF87; margin-bottom: 20px; 
        box-shadow: 0 8px 16px rgba(0,0,0,0.4); position: relative; overflow: hidden;
    }
    .match-card::before { content: '⚽'; position: absolute; font-size: 5rem; opacity: 0.03; right: -10px; bottom: -20px; }
    
    .flag-huge { font-size: 3.5rem; line-height: 1; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3)); }
    .team-name { font-size: 1.8rem; font-weight: 400; color: #ffffff; text-transform: uppercase; margin-top: 5px; letter-spacing: 2px; }
    .vs-text { font-size: 2.5rem; color: #00FF87; font-weight: 400; font-style: italic; text-shadow: 0 0 10px rgba(0,255,135,0.5); }
    
    .stNumberInput > div > div > input { border-radius: 8px; font-weight: bold; font-family: 'Bebas Neue', sans-serif; font-size: 2rem; text-align: center; background-color: #374151; color: #00FF87; border: 1px solid #4B5563; }
    .stTextInput > div > div > input { border-radius: 8px; background-color: #1f2937; color: white; font-weight: bold; font-family: 'Roboto', sans-serif;}
    .stSelectbox > div > div > div { background-color: #1f2937; color: white; border-radius: 8px; }
    .lobby-box { background-color: #1f2937; border-radius: 12px; padding: 20px; text-align: center; border-bottom: 3px solid #60EFFF; }
    
    /* Optimizaciones exclusivas para Celulares */
    @media (max-width: 768px) {
        h1 { font-size: 2.2rem !important; }
        .banner-subtitle { font-size: 1.2rem !important; }
        .flag-huge { font-size: 2.5rem !important; }
        .team-name { font-size: 1.2rem !important; }
        .vs-text { font-size: 1.8rem !important; }
        button[data-baseweb="tab"] { font-size: 1rem !important; padding: 10px 5px !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- BASES DE DATOS ---
PARTIDOS_FILE = "mundial_partidos_oficial_2026.csv"
PREDICCONES_FILE = "mundial_preds_oficial_2026.csv"
LIGAS_FILE = "mundial_ligas_oficial_2026.csv" 
PASSWORD_ADMIN = "grupos2026"

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

# --- PANEL LATERAL (CON BOTÓN DE COMPARTIR) ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <h1 style="font-size: 4rem; margin: 0; filter: drop-shadow(0px 0px 10px rgba(0,255,135,0.5));">⚽</h1>
        <h2 style="color: #00FF87; margin-top: 10px; text-transform: uppercase; letter-spacing: 2px;">La Previa</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.info("💡 **Tip Pro:** Ve a la pestaña '🏠 Inicio' para ver cómo instalar esta web en tu celular.")
    
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: white;'>🔗 Invita a tus amigos</h3>", unsafe_allow_html=True)
    st.caption("Copia este link para invitar a más jugadores:")
    
    st.code(URL_APP_MUNDIAL, language="text")
    
    mensaje_whatsapp = f"🏆 ¡Únete a nuestra liga de pronósticos del Mundial 2026! ⚽ Deja tus resultados aquí: {URL_APP_MUNDIAL}"
    url_whatsapp = f"https://api.whatsapp.com/send?text={urllib.parse.quote(mensaje_whatsapp)}"
    
    st.markdown(f"""
    <a href="{url_whatsapp}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #25D366; color: white; text-align: center; padding: 12px; border-radius: 8px; font-weight: bold; margin-top: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); font-family: 'Roboto', sans-serif;">
            📲 Enviar por WhatsApp
        </div>
    </a>
    """, unsafe_allow_html=True)

# --- BANNER PRINCIPAL ANIMADO (FONDO ESTADIO) ---
st.markdown("""
<div style="animation: pulseGlow 3s infinite; background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)), url('https://mediospublicos.uy/wp-content/uploads/2025/10/fad1fab784a384e167d98804139a10414dc89088w-1191x670.jpg'); background-size: cover; background-position: center; padding: 50px; border-radius: 15px; text-align: center; margin-bottom: 25px; border: 2px solid #00FF87;">
    <h1 style="color: #00FF87; margin:0; text-transform: uppercase; letter-spacing: 4px; text-shadow: 0 0 15px rgba(0,255,135,0.8); font-size: 4rem;">🏆 Predicción Mundialista</h1>
    <p class="banner-subtitle" style="color: #e5e7eb; font-size: 1.5rem; margin-top: 10px; font-weight: 800; letter-spacing: 4px; font-family: 'Bebas Neue', sans-serif;">🇺🇸 EEUU • 🇲🇽 MÉXICO • 🇨🇦 CANADÁ 2026</p>
</div>
""", unsafe_allow_html=True)

# --- REORGANIZACIÓN DE PESTAÑAS ---
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Inicio", "📊 Posiciones", "📝 Jugar", "ℹ️ Info", "📺 VAR", "🔒 Árbitro"])

# --- PESTAÑA 0: INICIO (LOBBY GRÁFICO E INSTRUCCIONES) ---
with tab0:
    # 1. BLOQUE DE INSTALACIÓN TIPO UFC (ANTI-TIKTOK)
    st.markdown("""
<div style="background: linear-gradient(135deg, #00FF87 0%, #60EFFF 100%); color: #000000; padding: 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 8px 20px rgba(0, 255, 135, 0.4);">
    <h3 style="margin-top: 0; color: #000000; display: flex; align-items: center; font-weight: 900;">📲 ¡Lleva el Mundial en tu Bolsillo!</h3>
    <p style="font-weight: 800; font-size: 1.05rem; margin-bottom: 8px; font-family: 'Roboto', sans-serif;">Instala esta web como una App nativa para no perderte nada:</p>
    
    <div style="background-color: rgba(0,0,0,0.8); padding: 12px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #60EFFF;">
        <span style="font-size: 0.95rem; color: #00FF87; font-weight: bold; font-family: 'Roboto', sans-serif;">⚠️ ¿Atrapado en el navegador de TikTok o Instagram?</span><br>
        <span style="font-size: 0.85rem; color: #fff; font-family: 'Roboto', sans-serif;">Las redes sociales bloquean la instalación. Para solucionarlo:</span><br>
        <ol style="font-size: 0.85rem; color: #fff; margin-top: 5px; margin-bottom: 0; padding-left: 20px; font-family: 'Roboto', sans-serif;">
            <li>Toca la barra superior blanca que dice <em>"Estás en..."</em> o busca los 3 puntitos.</li>
            <li>Copia el enlace de la página.</li>
            <li>Abre <strong>Safari</strong> (iPhone) o <strong>Chrome</strong> (Android) y pega el enlace ahí.</li>
        </ol>
    </div>
    
    <ul style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0; font-family: 'Roboto', sans-serif;">
        <li><strong>🍏 Una vez en Safari:</strong> Toca 'Compartir' (📤) abajo ➔ <strong>➕ Agregar a inicio</strong>.</li>
        <li><strong>🤖 Una vez en Chrome:</strong> Toca los 3 puntos (⋮) arriba ➔ <strong>📱 Agregar a la pantalla principal</strong>.</li>
    </ul>
</div>
    """, unsafe_allow_html=True)

    # 2. SECCIÓN VISUAL DE LOS GRUPOS OFICIALES
    st.markdown("<h2 style='text-align: center; color: #00FF87; text-transform: uppercase;'>🏆 Grupos Oficiales Mundial 2026</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px;'>
        <a href='{URL_NOTICIA_GRUPOS}' target='_blank'>
            <img src='{URL_IMAGEN_GRUPOS}' style='width: 100%; max-width: 800px; border-radius: 12px; border: 2px solid #00FF87; box-shadow: 0 4px 10px rgba(0,255,135,0.3); transition: transform 0.3s ease;' onmouseover='this.style.transform="scale(1.02)"' onmouseout='this.style.transform="scale(1)"'>
        </a>
        <p style='color: #9CA3AF; font-size: 0.85rem; margin-top: 5px; font-family: "Roboto", sans-serif;'>Haz clic en la imagen para leer la noticia oficial del sorteo.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background-image: linear-gradient(to right, #1f2937, #111827); padding: 30px; border-radius: 12px; border-left: 5px solid #60EFFF; margin-bottom: 20px;">
        <h2 style="color: white; margin-top: 0;">🏟️ ¡Bienvenidos a la Fiesta del Fútbol!</h2>
        <p style="color: #9CA3AF; font-size: 1.1rem; font-family: 'Roboto', sans-serif;">Demuestra quién es el verdadero analista táctico en la competencia definitiva de predicciones. Únete a una liga privada o compite en el ranking global.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.markdown("<div class='lobby-box'><h2>🌍</h2><h3 style='color:white; margin:0;'>Global</h3><p style='color:#9CA3AF; font-family: \"Roboto\", sans-serif;'>Compite en el Ranking Abierto.</p></div>", unsafe_allow_html=True)
    with col_b: st.markdown("<div class='lobby-box'><h2>🔐</h2><h3 style='color:white; margin:0;'>Privadas</h3><p style='color:#9CA3AF; font-family: \"Roboto\", sans-serif;'>Crea tu propia sala con candado.</p></div>", unsafe_allow_html=True)
    with col_c: st.markdown("<div class='lobby-box'><h2>🏆</h2><h3 style='color:white; margin:0;'>Podio</h3><p style='color:#9CA3AF; font-family: \"Roboto\", sans-serif;'>Suma puntos y domina la tabla.</p></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("✅ Marcador Oficial (Resultados)")
    partidos_jugados = df_partidos[df_partidos["jugado"] == True]
    
    if not partidos_jugados.empty:
        for _, row in partidos_jugados.iterrows():
            l_name, l_flag = parse_team(row['local'])
            v_name, v_flag = parse_team(row['visita'])
            try:
                gl = int(float(row['goles_l_real']))
                gv = int(float(row['goles_v_real']))
                st.markdown(f"<div style='background-color:#1f2937; padding:12px; border-radius:8px; margin-bottom:10px; text-align:center; border-left: 4px solid #00FF87; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'><span style='color:#9CA3AF; font-size:0.9rem; margin-right:15px; font-weight:bold; font-family: \"Roboto\", sans-serif;'>{row['fecha']}</span> <span style='font-size:1.4rem; font-weight:900;'>{l_flag} <span class='team-name' style='font-size:1.4rem;'>{l_name}</span> &nbsp;&nbsp;<span style='color:#00FF87; background-color:#111827; padding: 2px 10px; border-radius:5px;'>{gl} - {gv}</span>&nbsp;&nbsp; <span class='team-name' style='font-size:1.4rem;'>{v_name}</span> {v_flag}</span></div>", unsafe_allow_html=True)
            except ValueError: pass
    else:
        st.info("⏱️ Aún no hay partidos finalizados. ¡El balón está por rodar!")
        
    st.markdown("---")
    st.subheader("📋 Directorio de Ligas Activas")
    if not df_predicciones.empty:
        ligas_stats = df_predicciones.groupby('liga')['usuario'].nunique().reset_index()
        ligas_stats.columns = ['🎟️ Nombre de la Liga', '👥 Jugadores Activos']
        st.dataframe(ligas_stats, hide_index=True, use_container_width=True)
    else:
        st.info("🎟️ Aún no hay ligas creadas. Ve a la pestaña 'Jugar' y sé el primero.")

# --- PESTAÑA 1: RANKING Y LIGAS ---
with tab1:
    st.markdown("""
    <div style="background-color: #1f2937; padding: 20px; border-radius: 12px; border-left: 5px solid #00FF87; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        <h2 style="color: white; margin-top: 0; display: flex; align-items: center;">🏆 ¿Qué tabla quieres ver?</h2>
        <p style="color: #D1D5DB; font-size: 1rem; margin-bottom: 0; font-family: 'Roboto', sans-serif;">Elige 'GLOBAL' para ver el ranking mundial, o selecciona la sala privada de tus amigos en la lista.</p>
    </div>
    """, unsafe_allow_html=True)
    
    opciones_ligas = ["GLOBAL"]
    if not df_ligas.empty:
        ligas_privadas = sorted(df_ligas["nombre_liga"].unique().tolist())
        opciones_ligas.extend(ligas_privadas)
        
    liga_seleccionada = st.selectbox("🔍 Selecciona una liga para ver sus posiciones:", opciones_ligas)
    liga_busqueda = liga_seleccionada.strip().upper()
    
    st.markdown(f"<div style='text-align:center; padding:15px; background-color:#111827; border-radius:10px; border-top: 3px solid #00FF87;'><h2 style='margin:0; color:white;'>📊 Viendo la Liga: <span style='color:#00FF87;'>{liga_busqueda}</span></h2></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df_ranking = calcular_tabla(df_partidos, df_predicciones, liga_busqueda)
    
    if not df_ranking.empty:
        if len(df_ranking) >= 3:
            st.markdown("### 🏟️ El Podio Actual")
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("🥇 1er Lugar", df_ranking.iloc[0]["Participante"], f"{df_ranking.iloc[0]['Puntos Totales']} pts")
            with col2: st.metric("🥈 2do Lugar", df_ranking.iloc[1]["Participante"], f"{df_ranking.iloc[1]['Puntos Totales']} pts")
            with col3: st.metric("🥉 3er Lugar", df_ranking.iloc[2]["Participante"], f"{df_ranking.iloc[2]['Puntos Totales']} pts")
            st.markdown("---")
        elif len(df_ranking) > 0:
             st.success(f"🥇 Líder indiscutido en esta liga: **{df_ranking.iloc[0]['Participante']}** con {df_ranking.iloc[0]['Puntos Totales']} puntos.")
             
        st.dataframe(df_ranking, use_container_width=True, hide_index=True)
    else:
        st.warning(f"No se encontraron jugadores con predicciones para la liga '{liga_busqueda}' o aún no se han jugado partidos.")

# --- PESTAÑA 2: PREDICCIONES CON SISTEMA DE CANDADOS ---
with tab2:
    st.header("📝 Tu Cartilla de Pronósticos")
    usuario_input = st.text_input("👤 Tu Apodo:", key="user_name", placeholder="Ej. Tesla Jr.")
    usuario_limpio = usuario_input.strip().title()
    
    st.markdown("### 🤝 ¿Dónde quieres jugar?")
    opcion_liga = st.selectbox("Selecciona tu modalidad:", ["🌍 Ranking Global (Público, sin clave)", "➕ Crear una Nueva Liga Privada", "🔐 Unirme a una Liga Existente"])
    
    liga_limpia = "GLOBAL" 
    clave_ingresada = ""
    clave_creada = ""
    liga_nueva = ""
    
    if opcion_liga == "➕ Crear una Nueva Liga Privada":
        col_nl, col_cl = st.columns(2)
        with col_nl: liga_nueva = st.text_input("Nombre de tu nueva liga:", placeholder="Ej. FamiliaMundial")
        with col_cl: clave_creada = st.text_input("Inventa una clave secreta:", placeholder="Para que se unan tus amigos")
        liga_limpia = liga_nueva.strip().upper()
        st.info("💡 Asegúrate de compartir el Nombre y la Clave con tus amigos para que puedan entrar.")
        
    elif opcion_liga == "🔐 Unirme a una Liga Existente":
        ligas_disponibles = df_ligas["nombre_liga"].tolist()
        if not ligas_disponibles:
            st.error("Aún no hay ligas privadas creadas. ¡Crea una!")
        else:
            col_sel, col_pass = st.columns(2)
            with col_sel: liga_seleccionada = st.selectbox("Selecciona la liga:", ligas_disponibles)
            with col_pass: clave_ingresada = st.text_input("Contraseña de la liga:", type="password")
            liga_limpia = liga_seleccionada
    
    if usuario_limpio:
        st.markdown("---")
        with st.form("form_cronologico_preds"):
            for fecha in lista_fechas:
                with st.expander(f"🗓️ {fecha}"):
                    partidos_dia = df_partidos[df_partidos["fecha"] == fecha]
                    for _, row in partidos_dia.iterrows():
                        pred_existente = df_predicciones[(df_predicciones["usuario"] == usuario_limpio) & (df_predicciones["partido_id"] == row["id"])]
                        val_l = int(pred_existente.iloc[0]["goles_l_pred"]) if not pred_existente.empty else 0
                        val_v = int(pred_existente.iloc[0]["goles_v_pred"]) if not pred_existente.empty else 0
                        
                        l_name, l_flag = parse_team(row['local'])
                        v_name, v_flag = parse_team(row['visita'])
                        
                        html_tarjeta = f"""
                        <div class='match-card'>
                            <p style='color:#9CA3AF; margin:0 0 10px 0; font-size:0.9rem; letter-spacing: 2px; text-transform: uppercase; font-family: "Bebas Neue", sans-serif;'>{row['grupo']}</p>
                            <div style='display:flex; justify-content:space-around; align-items:center;'>
                                <div style='width: 40%;'><div class='flag-huge'>{l_flag}</div><div class='team-name'>{l_name}</div></div>
                                <div style='width: 20%;'><div class='vs-text'>VS</div></div>
                                <div style='width: 40%;'><div class='flag-huge'>{v_flag}</div><div class='team-name'>{v_name}</div></div>
                            </div>
                        </div>
                        """
                        st.markdown(html_tarjeta, unsafe_allow_html=True)
                        
                        if row["jugado"]:
                            try:
                                st.markdown(f"<p style='text-align:center; color:#EF4444; font-weight:bold; font-family: \"Roboto\", sans-serif;'>✅ FINALIZADO | Real: {int(float(row['goles_l_real']))} - {int(float(row['goles_v_real']))}</p>", unsafe_allow_html=True)
                            except ValueError: pass
                                
                        esta_bloqueado = bool(row["jugado"])
                        col1, col2 = st.columns(2)
                        with col1: g_l = st.number_input(f"Goles {l_name}", min_value=0, max_value=15, value=val_l, step=1, key=f"l_{row['id']}", disabled=esta_bloqueado)
                        with col2: g_v = st.number_input(f"Goles {v_name}", min_value=0, max_value=15, value=val_v, step=1, key=f"v_{row['id']}", disabled=esta_bloqueado)
                        st.markdown("<br><br>", unsafe_allow_html=True)
            
            if st.form_submit_button("🚀 Guardar Todas Mis Predicciones"):
                if not usuario_limpio:
                    st.error("❌ ¡Epa! Se te olvidó poner tu apodo arriba.")
                else:
                    acceso_permitido = True
                    if opcion_liga == "➕ Crear una Nueva Liga Privada":
                        if not liga_nueva or not clave_creada:
                            st.error("❌ Faltan datos: Debes ponerle un nombre y una clave a tu nueva liga.")
                            acceso_permitido = False
                        elif liga_limpia in df_ligas["nombre_liga"].tolist() or liga_limpia == "GLOBAL":
                            st.error("❌ Ese nombre de liga ya existe. Elige otro.")
                            acceso_permitido = False
                        else:
                            nueva_l = {"nombre_liga": liga_limpia, "clave_liga": clave_creada, "creador": usuario_limpio}
                            df_ligas = pd.concat([df_ligas, pd.DataFrame([nueva_l])], ignore_index=True)
                            df_ligas.to_csv(LIGAS_FILE, index=False)
                            
                    elif opcion_liga == "🔐 Unirme a una Liga Existente":
                        clave_real = str(df_ligas[df_ligas["nombre_liga"] == liga_limpia]["clave_liga"].values[0])
                        if str(clave_ingresada) != clave_real:
                            st.error("❌ Contraseña incorrecta para esta liga. Revisa bien.")
                            acceso_permitido = False
                    
                    if acceso_permitido:
                        for _, row in df_partidos.iterrows():
                            p_id = row["id"]
                            if row["jugado"]: continue 
                            g_l_v = st.session_state[f"l_{p_id}"]
                            g_v_v = st.session_state[f"v_{p_id}"]
                            df_predicciones = df_predicciones[~((df_predicciones["usuario"] == usuario_limpio) & (df_predicciones["partido_id"] == p_id))]
                            nueva_p = {"usuario": usuario_limpio, "liga": liga_limpia, "partido_id": p_id, "goles_l_pred": int(g_l_v), "goles_v_pred": int(g_v_v)}
                            df_predicciones = pd.concat([df_predicciones, pd.DataFrame([nueva_p])], ignore_index=True)
                        
                        df_predicciones.to_csv(PREDICCONES_FILE, index=False)
                        st.balloons()
                        st.toast(f'¡Pronósticos sellados en la liga {liga_limpia}!', icon='🔒')
                        time.sleep(1.5)
                        st.rerun()
    else:
        st.warning("Escribe tu apodo para desplegar el fixture oficial.")

# --- PESTAÑA 3: INFORMACIÓN ---
with tab3:
    st.header("ℹ️ Información del Torneo")
    st.markdown("""
    <div style="background-color: #1f2937; padding: 20px; border-radius: 12px; margin-bottom: 20px; border-left: 5px solid #00FF87;">
        <h2 style="color: white; margin-top: 0;">📜 Reglas de Puntuación</h2>
        <ul style="color: #D1D5DB; font-size: 1.1rem; line-height: 1.8; font-family: 'Roboto', sans-serif;">
            <li><strong style="color: #00FF87;">3 Puntos (Pleno):</strong> ¡Le achuntaste al resultado exacto! (Ej: Predices 2-1 y termina 2-1).</li>
            <li><strong style="color: #60EFFF;">1 Punto (Tendencia):</strong> Le achuntaste al ganador o al empate, pero no a los goles exactos.</li>
            <li><strong style="color: #F87171;">0 Puntos:</strong> No le achuntaste a nada. Suerte para la próxima.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("⏱️ Avance del Torneo")
    jugados = len(df_partidos[df_partidos["jugado"] == True])
    st.progress(jugados / len(df_partidos) if len(df_partidos) > 0 else 0)
    st.write(f"**Partidos finalizados:** {jugados} de {len(df_partidos)}")

# --- PESTAÑA 4: EL VAR ---
with tab4:
    st.markdown("""
    <div style="background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.9)), url('https://images.unsplash.com/photo-1508344928928-7137b29de216?auto=format&fit=crop&w=1200&q=80'); background-size: cover; background-position: center; padding: 30px; border-radius: 12px; margin-bottom: 20px; border-bottom: 4px solid #60EFFF;">
        <h1 style="color: #60EFFF; margin:0; text-transform: uppercase;">📺 Sala del VAR</h1>
        <p style="color: #D1D5DB; margin-top: 5px; font-family: 'Roboto', sans-serif; font-size: 1.1rem;">Análisis en vivo de las tendencias globales.</p>
    </div>
    """, unsafe_allow_html=True)
    if df_predicciones.empty:
        st.info("Aún no hay suficientes predicciones para mostrar las estadísticas.")
    else:
        col1, col2 = st.columns(2)
        total_apuestas = len(df_predicciones["usuario"].unique())
        total_goles_predichos = df_predicciones["goles_l_pred"].sum() + df_predicciones["goles_v_pred"].sum()
        with col1: st.metric("👥 Jugadores Globales", total_apuestas)
        with col2: st.metric("⚽ Goles Totales Apostados", total_goles_predichos)
        st.markdown("---")
        st.subheader("📊 Tendencia de Goles por Partido")
        df_predicciones["Total_Goles_Predichos"] = df_predicciones["goles_l_pred"] + df_predicciones["goles_v_pred"]
        chart_data = df_predicciones["Total_Goles_Predichos"].value_counts().sort_index()
        st.bar_chart(chart_data, color="#60EFFF")

# --- PESTAÑA 5: ADMIN ---
with tab5:
    st.markdown("""
    <div style="background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.9)), url('https://images.unsplash.com/photo-1552667466-07770ae110d0?auto=format&fit=crop&w=1200&q=80'); background-size: cover; background-position: center; padding: 30px; border-radius: 12px; margin-bottom: 20px; border-bottom: 4px solid #F87171;">
        <h1 style="color: #F87171; margin:0; text-transform: uppercase;">🔒 Camarín del Árbitro</h1>
        <p style="color: #D1D5DB; margin-top: 5px; font-family: 'Roboto', sans-serif; font-size: 1.1rem;">Ingreso de resultados oficiales. Acceso restringido.</p>
    </div>
    """, unsafe_allow_html=True)
    input_pass = st.text_input("Contraseña secreta:", type="password")
    if input_pass == PASSWORD_ADMIN:
        with st.form("form_admin_crono"):
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
            if st.form_submit_button("🔄 Confirmar Resultados Oficiales"):
                for idx, row in df_partidos.iterrows():
                    p_id = row["id"]
                    df_partidos.at[idx, "goles_l_real"] = str(int(st.session_state[f"rl_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "goles_v_real"] = str(int(st.session_state[f"rv_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "jugado"] = bool(st.session_state[f"j_{p_id}"])
                df_partidos.to_csv(PARTIDOS_FILE, index=False)
                st.toast('¡Resultados bloqueados y tabla actualizada!', icon='⚖️')
                time.sleep(1)
                st.rerun()
        st.subheader("📥 La Caja Fuerte (Respaldos)")
        st.download_button("Descargar Base de Partidos", df_partidos.to_csv(index=False).encode('utf-8'), "partidos_final.csv", "text/csv")
        st.download_button("Descargar Base de Predicciones", df_predicciones.to_csv(index=False).encode('utf-8'), "predicciones_final.csv", "text/csv")
        st.download_button("Descargar Base de Ligas", df_ligas.to_csv(index=False).encode('utf-8'), "ligas_final.csv", "text/csv")
