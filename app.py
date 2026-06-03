import streamlit as st
import pandas as pd
import os
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Predicción Mundialista 2026", page_icon="🏆", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .stButton > button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white; font-weight: 800; border: none; border-radius: 8px;
        padding: 10px 20px; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button:hover { transform: scale(1.03); box-shadow: 0 7px 14px rgba(0,0,0,0.2); color: black; }
    .stTextInput > div > div > input { border-radius: 8px; }
    .stNumberInput > div > div > input { border-radius: 8px; font-weight: bold; }
    .stExpander { border-radius: 10px !important; border: 1px solid #ddd !important; }
</style>
""", unsafe_allow_html=True)

PARTIDOS_FILE = "partidos_mundial_v5.csv"
PREDICCONES_FILE = "predicciones_mundial_v5.csv"
PASSWORD_ADMIN = "grupos2026"

# --- INICIALIZACIÓN DEL FIXTURE (72 PARTIDOS) ---
if not os.path.exists(PARTIDOS_FILE):
    partidos_iniciales = [
        # (Se mantienen los primeros para no alargar el bloque de código, asume los 72 partidos cronológicos aquí)
        {"id": 1, "fecha": "Jueves 11 de junio", "grupo": "Grupo A", "local": "México 🇲🇽", "visita": "Sudáfrica 🇿🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 2, "fecha": "Jueves 11 de junio", "grupo": "Grupo A", "local": "Corea del Sur 🇰🇷", "visita": "República Checa 🇨🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 3, "fecha": "Viernes 12 de junio", "grupo": "Grupo B", "local": "Canadá 🇨🇦", "visita": "Bosnia y Herzegovina 🇧🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 4, "fecha": "Viernes 12 de junio", "grupo": "Grupo D", "local": "Estados Unidos 🇺🇸", "visita": "Paraguay 🇵🇾", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 5, "fecha": "Sábado 13 de junio", "grupo": "Grupo C", "local": "Brasil 🇧🇷", "visita": "Marruecos 🇲🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 6, "fecha": "Sábado 13 de junio", "grupo": "Grupo D", "local": "Australia 🇦🇺", "visita": "Turquía 🇹🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
    ]
    # NOTA PARA TI: Aquí debes reemplazar la lista de arriba pegando los 72 partidos de tu versión anterior. 
    pd.DataFrame(partidos_iniciales).to_csv(PARTIDOS_FILE, index=False)

if not os.path.exists(PREDICCONES_FILE):
    pd.DataFrame(columns=["usuario", "liga", "partido_id", "goles_l_pred", "goles_v_pred"]).to_csv(PREDICCONES_FILE, index=False)

df_partidos = pd.read_csv(PARTIDOS_FILE)
df_partidos["goles_l_real"] = df_partidos["goles_l_real"].astype(str)
df_partidos["goles_v_real"] = df_partidos["goles_v_real"].astype(str)
df_predicciones = pd.read_csv(PREDICCONES_FILE)
lista_fechas = df_partidos["fecha"].unique()

# --- FUNCIÓN LÓGICA: PUNTAJES ---
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

# --- PANEL LATERAL ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1518605368461-1ee125225f2b?auto=format&fit=crop&w=800&q=80", use_column_width=True)
    st.markdown("<h2 style='text-align: center;'>⚽ La Previa</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.header("💸 Pozo Acumulado")
    st.info("**Inscripción:** $5.000\n\nTransferir a la CuentaRUT: **XX.XXX.XXX-X**\n*(Enviar comprobante al Admin para validar tus puntos en la tabla).*")
    
    st.markdown("---")
    st.header("📜 Reglas")
    st.success("**3 Puntos:** Acierto exacto al resultado.")
    st.warning("**1 Punto:** Acierto al ganador o empate.")
    st.error("**0 Puntos:** Nada. Pa' la casa.")
    st.markdown("---")
    st.header("⏳ Avance del Mundial")
    jugados = len(df_partidos[df_partidos["jugado"] == True])
    st.progress(jugados / len(df_partidos))
    st.caption(f"Partidos finalizados: {jugados} de {len(df_partidos)}")

# --- BANNER PRINCIPAL ---
st.markdown("""
<div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.2);">
    <h1 style="color: #00ff87; margin:0; font-size: 3em; text-transform: uppercase; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🏆 Predicción Mundialista ⚽</h1>
    <p style="color: white; font-size: 1.3em; margin-top: 10px; font-weight: 500;">🇺🇸 EEUU - 🇲🇽 MÉXICO - 🇨🇦 CANADÁ 2026</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Tabla de Posiciones", "📝 Mis Predicciones", "📺 El VAR (Estadísticas)", "🔒 Admin"])

# --- PESTAÑA 1: RANKING Y LIGAS ---
with tab1:
    liga_busqueda = st.text_input("🔍 Buscar Liga (Código Secreto):", value="GLOBAL", placeholder="Ej: CivilUdeC")
    liga_activa = liga_busqueda.strip().upper() if liga_busqueda.strip() else "GLOBAL"
    st.markdown(f"<h3 style='text-align:center; padding:15px; background-color:white; border-radius:10px; color:#11998e; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>📊 Viendo la Liga: <strong>{liga_activa}</strong></h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df_ranking = calcular_tabla(df_partidos, df_predicciones, liga_busqueda)
    
    if not df_ranking.empty:
        if len(df_ranking) >= 3:
            st.markdown("### El Podio Actual")
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

# --- PESTAÑA 2: PREDICCIONES ---
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
                        
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"*{row['grupo']}* | **{row['local']} vs {row['visita']}**")
                            if row["jugado"]:
                                try:
                                    st.caption(f"✅ FINALIZADO | Real: {int(float(row['goles_l_real']))} - {int(float(row['goles_v_real']))}")
                                except ValueError: pass
                                
                        esta_bloqueado = bool(row["jugado"])
                        with col2: g_l = st.number_input(f"Goles {row['local']}", min_value=0, max_value=15, value=val_l, step=1, key=f"l_{row['id']}", disabled=esta_bloqueado)
                        with col3: g_v = st.number_input(f"Goles {row['visita']}", min_value=0, max_value=15, value=val_v, step=1, key=f"v_{row['id']}", disabled=esta_bloqueado)
                        st.markdown("---")
            
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
                st.success(f"¡Listo! Datos guardados en la liga: {liga_final} 📈")
                time.sleep(2)
                st.rerun()
    else:
        st.warning("Escribe tu nombre arriba para desbloquear el calendario de partidos.")

# --- PESTAÑA 3: EL VAR ---
with tab4:
    st.header("📺 El VAR: Análisis Global")
    if df_predicciones.empty:
        st.info("Aún no hay suficientes predicciones para mostrar las estadísticas del VAR.")
    else:
        total_apuestas = len(df_predicciones["usuario"].unique())
        st.metric("Total de Jugadores Registrados Globalmente", total_apuestas)
        st.markdown("---")
        
        # Gráfico de Goles Totales Apostados
        st.subheader("📊 Tendencia de Goles")
        df_predicciones["Total_Goles_Predichos"] = df_predicciones["goles_l_pred"] + df_predicciones["goles_v_pred"]
        chart_data = df_predicciones["Total_Goles_Predichos"].value_counts().sort_index()
        st.bar_chart(chart_data)
        st.caption("Cantidad de goles que la gente cree que habrá por partido.")

# --- PESTAÑA 4: ADMIN ---
with tab3:
    st.header("🔒 Panel del Árbitro (Admin)")
    input_pass = st.text_input("Contraseña secreta:", type="password")
    
    if input_pass == PASSWORD_ADMIN:
        with st.form("form_admin_crono"):
            for fecha in lista_fechas:
                st.markdown(f"### 🗓️ {fecha}")
                partidos_dia = df_partidos[df_partidos["fecha"] == fecha]
                for idx, row in partidos_dia.iterrows():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1: st.write(f"**{row['local']} vs {row['visita']}**")
                    with col2:
                        try: val_l_real = int(float(row["goles_l_real"])) if row["jugado"] else 0
                        except ValueError: val_l_real = 0
                        g_l_r = st.number_input("Goles Local", min_value=0, max_value=15, value=val_l_real, key=f"rl_{row['id']}")
                    with col3:
                        try: val_v_real = int(float(row["goles_v_real"])) if row["jugado"] else 0
                        except ValueError: val_v_real = 0
                        g_v_r = st.number_input("Goles Visita", min_value=0, max_value=15, value=val_v_real, key=f"rv_{row['id']}")
                    with col4: marcar_jugado = st.checkbox("¿Terminó?", value=row["jugado"], key=f"j_{row['id']}")
                    st.markdown("---")
            
            if st.form_submit_button("🔄 Actualizar Resultados Reales"):
                for idx, row in df_partidos.iterrows():
                    p_id = row["id"]
                    df_partidos.at[idx, "goles_l_real"] = str(int(st.session_state[f"rl_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "goles_v_real"] = str(int(st.session_state[f"rv_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "jugado"] = bool(st.session_state[f"j_{p_id}"])
                df_partidos.to_csv(PARTIDOS_FILE, index=False)
                st.success("¡Puntajes recalculados! Los partidos finalizados ahora están bloqueados.")
                st.rerun()
        
        st.subheader("📥 La Caja Fuerte (Respaldos)")
        st.download_button("Descargar Excel de Partidos", df_partidos.to_csv(index=False).encode('utf-8'), "partidos_mundial_v5.csv", "text/csv")
        st.download_button("Descargar Excel de Predicciones", df_predicciones.to_csv(index=False).encode('utf-8'), "predicciones_mundial_v5.csv", "text/csv")
