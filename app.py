import streamlit as st
import pandas as pd
import os
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Predicción Mundialista 2026", page_icon="🏆", layout="wide")

# --- ESTILOS CSS (MODO ESTADIO / GAMER) ---
st.markdown("""
<style>
    .stApp { background-color: #0b101a; color: #ffffff; }
    
    .stButton > button {
        background: linear-gradient(135deg, #00FF87 0%, #60EFFF 100%);
        color: #000000; font-weight: 900; border: none; border-radius: 12px;
        padding: 12px 24px; transition: all 0.3s ease; text-transform: uppercase;
        letter-spacing: 1.5px; width: 100%; box-shadow: 0 4px 15px rgba(0, 255, 135, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0, 255, 135, 0.5); color: #000;
    }
    
    .stExpander { 
        border-radius: 12px !important; border: 1px solid #1f2937 !important; 
        background-color: #111827 !important; margin-bottom: 15px;
    }
    
    /* NUEVAS TARJETAS DE PARTIDOS CON BANDERAS GIGANTES */
    .match-card {
        background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
        padding: 15px; border-radius: 12px; text-align: center; 
        border-top: 3px solid #00FF87; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .flag-huge { font-size: 3rem; line-height: 1; }
    .team-name { font-size: 1.1rem; font-weight: 800; color: #ffffff; text-transform: uppercase; margin-top: 5px; }
    .vs-text { font-size: 1.5rem; color: #00FF87; font-weight: 900; font-style: italic; }
    
    .stNumberInput > div > div > input { 
        border-radius: 8px; font-weight: bold; font-size: 1.5rem; text-align: center; 
        background-color: #374151; color: #00FF87; border: 1px solid #4B5563;
    }
    .stTextInput > div > div > input { border-radius: 8px; background-color: #1f2937; color: white; }
</style>
""", unsafe_allow_html=True)

PARTIDOS_FILE = "partidos_mundial_v8.csv"
PREDICCONES_FILE = "predicciones_mundial_v8.csv"
PASSWORD_ADMIN = "grupos2026"

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

if not os.path.exists(PREDICCONES_FILE):
    pd.DataFrame(columns=["usuario", "liga", "partido_id", "goles_l_pred", "goles_v_pred"]).to_csv(PREDICCONES_FILE, index=False)

df_partidos = pd.read_csv(PARTIDOS_FILE)
df_partidos["goles_l_real"] = df_partidos["goles_l_real"].astype(str)
df_partidos["goles_v_real"] = df_partidos["goles_v_real"].astype(str)
df_predicciones = pd.read_csv(PREDICCONES_FILE)
lista_fechas = df_partidos["fecha"].unique()

# --- FUNCIONES AUXILIARES ---
def calcular_tabla(df_p, df_preds, liga_filtro=None):
    if df_preds.empty: return pd.DataFrame(columns=["Participante", "Rango 🎖️", "Puntos Totales", "Exactos (3pts)", "Tendencias (1pt)"])
    if liga_filtro and liga_filtro.strip().upper() != "GLOBAL":
        df_preds = df_preds[df_preds["liga"].str.upper() == liga_filtro.strip().upper()]
        if df_preds.empty: return pd.DataFrame(columns=["Participante", "Rango 🎖️", "Puntos Totales", "Exactos (3pts)", "Tendencias (1pt)"])

    partidos_jugados = df_p[df_p["jugado"] == True]
    puntajes = {}
    for _, pred in df_preds.iterrows():
        user = pred["usuario"]
        p_id = int(pred["partido_id"])
        partido_real = list(partidos_jugados[partidos_jugados["id"] == p_id].to_dict(orient="index").values())
        if not partido_real: continue
        p_real = partido_real[0]
        if user not in puntajes: puntajes[user] = {"puntos": 0, "exactos": 0, "tendencias": 0}
        
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
    """Separa el nombre del país del emoji de la bandera para el nuevo diseño UI"""
    parts = team_string.split()
    flag = parts[-1]
    name = " ".join(parts[:-1])
    return name, flag

# --- PANEL LATERAL ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1518605368461-1ee125225f2b?auto=format&fit=crop&w=800&q=80", use_column_width=True)
    st.markdown("<h2 style='text-align: center; color: #00FF87;'>⚽ La Previa</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("📜 Reglas Oficiales")
    st.success("**3 Puntos:** ¡Pleno! Acierto exacto al resultado.")
    st.info("**1 Punto:** Tendencia. Acierto al ganador o empate.")
    st.error("**0 Puntos:** Nada. Pa' la casa.")
    st.markdown("---")
    st.header("⏳ Avance del Mundial")
    jugados = len(df_partidos[df_partidos["jugado"] == True])
    st.progress(jugados / len(df_partidos))
    st.caption(f"Partidos finalizados: {jugados} de {len(df_partidos)}")

# --- BANNER PRINCIPAL ---
st.markdown("""
<div style="background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.8)), url('https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=1200&q=80'); background-size: cover; background-position: center; padding: 40px; border-radius: 15px; text-align: center; margin-bottom: 25px; border: 1px solid #1f2937;">
    <h1 style="color: #00FF87; margin:0; font-size: 3.5em; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 10px rgba(0,255,135,0.5);">🏆 Predicción Mundialista</h1>
    <p style="color: #e5e7eb; font-size: 1.2em; margin-top: 10px; font-weight: 500; letter-spacing: 3px;">🇺🇸 EEUU • 🇲🇽 MÉXICO • 🇨🇦 CANADÁ 2026</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Tabla de Posiciones", "📝 Mis Predicciones", "📺 El VAR (Estadísticas)", "🔒 Admin"])

# --- PESTAÑA 1: RANKING Y LIGAS ---
with tab1:
    liga_busqueda = st.text_input("🔍 Buscar Liga (Código Secreto):", value="GLOBAL", placeholder="Ej: LosVendehumos")
    liga_activa = liga_busqueda.strip().upper() if liga_busqueda.strip() else "GLOBAL"
    
    st.markdown(f"<div style='text-align:center; padding:15px; background-color:#1f2937; border-radius:10px; border-left: 5px solid #00FF87;'><h3 style='margin:0; color:white;'>📊 Viendo la Liga: <span style='color:#00FF87;'>{liga_activa}</span></h3></div>", unsafe_allow_html=True)
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
        st.warning(f"No se encontraron jugadores para la liga '{liga_busqueda}' o aún no hay partidos jugados.")

# --- PESTAÑA 2: PREDICCIONES (CON BANDERAS GIGANTES) ---
with tab2:
    st.header("📝 Tu Cartilla de Pronósticos")
    col_u, col_l = st.columns(2)
    with col_u: usuario = st.text_input("👤 Tu Apodo:", key="user_name", placeholder="Ej. Tesla Jr.")
    with col_l: liga_ingreso = st.text_input("🔑 Código de tu Liga (Opcional):", key="liga_name", placeholder="Ej. FamiliaMundial")
    
    if usuario:
        with st.form("form_cronologico_preds"):
            for fecha in lista_fechas:
                with st.expander(f"🗓️ {fecha}"):
                    partidos_dia = df_partidos[df_partidos["fecha"] == fecha]
                    for _, row in partidos_dia.iterrows():
                        pred_existente = df_predicciones[(df_predicciones["usuario"].str.lower() == usuario.strip().lower()) & (df_predicciones["partido_id"] == row["id"])]
                        val_l = int(pred_existente.iloc[0]["goles_l_pred"]) if not pred_existente.empty else 0
                        val_v = int(pred_existente.iloc[0]["goles_v_pred"]) if not pred_existente.empty else 0
                        
                        # PARSEO DE BANDERAS Y NOMBRES
                        l_name, l_flag = parse_team(row['local'])
                        v_name, v_flag = parse_team(row['visita'])
                        
                        # RENDERIZADO DE LA TARJETA VS
                        html_tarjeta = f"""
                        <div class='match-card'>
                            <p style='color:#9CA3AF; margin:0 0 10px 0; font-size:0.8rem; letter-spacing: 1px; text-transform: uppercase;'>{row['grupo']}</p>
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
                                st.markdown(f"<p style='text-align:center; color:#EF4444; font-weight:bold;'>✅ FINALIZADO | Real: {int(float(row['goles_l_real']))} - {int(float(row['goles_v_real']))}</p>", unsafe_allow_html=True)
                            except ValueError: pass
                                
                        esta_bloqueado = bool(row["jugado"])
                        col1, col2 = st.columns(2)
                        with col1: g_l = st.number_input(f"Goles {l_name}", min_value=0, max_value=15, value=val_l, step=1, key=f"l_{row['id']}", disabled=esta_bloqueado)
                        with col2: g_v = st.number_input(f"Goles {v_name}", min_value=0, max_value=15, value=val_v, step=1, key=f"v_{row['id']}", disabled=esta_bloqueado)
                        st.markdown("<br><br>", unsafe_allow_html=True)
            
            if st.form_submit_button("🚀 Guardar Todas Mis Predicciones"):
                liga_final = liga_ingreso.strip() if liga_ingreso else "GLOBAL"
                for _, row in df_partidos.iterrows():
                    p_id = row["id"]
                    if row["jugado"]: continue 
                    g_l_v = st.session_state[f"l_{p_id}"]
                    g_v_v = st.session_state[f"v_{p_id}"]
                    df_predicciones = df_predicciones[~((df_predicciones["usuario"].str.lower() == usuario.strip().lower()) & (df_predicciones["partido_id"] == p_id))]
                    nueva_p = {"usuario": usuario.strip(), "liga": liga_final, "partido_id": p_id, "goles_l_pred": int(g_l_v), "goles_v_pred": int(g_v_v)}
                    df_predicciones = pd.concat([df_predicciones, pd.DataFrame([nueva_p])], ignore_index=True)
                
                df_predicciones.to_csv(PREDICCONES_FILE, index=False)
                st.balloons()
                st.toast('¡Tus pronósticos se guardaron como un crack!', icon='🔥')
                time.sleep(1.5)
                st.rerun()
    else:
        st.warning("Escribe tu nombre arriba para desbloquear el calendario de partidos.")

# --- PESTAÑA 3: EL VAR ---
with tab3:
    st.header("📺 El VAR: Análisis Global")
    if df_predicciones.empty:
        st.info("Aún no hay suficientes predicciones para mostrar las estadísticas del VAR.")
    else:
        col1, col2 = st.columns(2)
        total_apuestas = len(df_predicciones["usuario"].unique())
        total_goles_predichos = df_predicciones["goles_l_pred"].sum() + df_predicciones["goles_v_pred"].sum()
        
        with col1: st.metric("👥 Jugadores Registrados", total_apuestas)
        with col2: st.metric("⚽ Goles Totales Apostados", total_goles_predichos)
        
        st.markdown("---")
        st.subheader("📊 Tendencia de Goles por Partido")
        df_predicciones["Total_Goles_Predichos"] = df_predicciones["goles_l_pred"] + df_predicciones["goles_v_pred"]
        chart_data = df_predicciones["Total_Goles_Predichos"].value_counts().sort_index()
        st.bar_chart(chart_data, color="#00FF87")

# --- PESTAÑA 4: ADMIN ---
with tab4:
    st.header("🔒 Panel del Árbitro (Admin)")
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
            
            if st.form_submit_button("🔄 Actualizar Resultados Reales"):
                for idx, row in df_partidos.iterrows():
                    p_id = row["id"]
                    df_partidos.at[idx, "goles_l_real"] = str(int(st.session_state[f"rl_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "goles_v_real"] = str(int(st.session_state[f"rv_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "jugado"] = bool(st.session_state[f"j_{p_id}"])
                df_partidos.to_csv(PARTIDOS_FILE, index=False)
                st.toast('¡Resultados oficiales subidos!', icon='✅')
                time.sleep(1)
                st.rerun()
        
        st.subheader("📥 La Caja Fuerte (Respaldos)")
        st.download_button("Descargar Excel de Partidos", df_partidos.to_csv(index=False).encode('utf-8'), "partidos_mundial_v8.csv", "text/csv")
        st.download_button("Descargar Excel de Predicciones", df_predicciones.to_csv(index=False).encode('utf-8'), "predicciones_mundial_v8.csv", "text/csv")
