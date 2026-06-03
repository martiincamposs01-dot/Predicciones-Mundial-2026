import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Polla Mundial 2026 - Grupos", page_icon="⚽", layout="wide")

# Archivos de base de datos local (Nuevos nombres para limpiar datos anteriores)
PARTIDOS_FILE = "partidos_mundial_completo.csv"
PREDICCONES_FILE = "predicciones_mundial_completo.csv"
PASSWORD_ADMIN = "grupos2026"  # Contraseña del administrador

# --- INICIALIZACIÓN DEL FIXTURE COMPLETO (72 PARTIDOS) ---
if not os.path.exists(PARTIDOS_FILE):
    partidos_iniciales = [
        # GRUPO A
        {"id": 1, "grupo": "Grupo A", "local": "México 🇲🇽", "visita": "Sudáfrica 🇿🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 2, "grupo": "Grupo A", "local": "República de Corea 🇰🇷", "visita": "República Checa 🇨🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 3, "grupo": "Grupo A", "local": "República Checa 🇨🇿", "visita": "Sudáfrica 🇿🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 4, "grupo": "Grupo A", "local": "México 🇲🇽", "visita": "República de Corea 🇰🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 5, "grupo": "Grupo A", "local": "República Checa 🇨🇿", "visita": "México 🇲🇽", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 6, "grupo": "Grupo A", "local": "Sudáfrica 🇿🇦", "visita": "República de Corea 🇰🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO B
        {"id": 7, "grupo": "Grupo B", "local": "Canadá 🇨🇦", "visita": "Bosnia y Herzegovina 🇧🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 8, "grupo": "Grupo B", "local": "Catar 🇶🇦", "visita": "Suiza 🇨🇭", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 9, "grupo": "Grupo B", "local": "Suiza 🇨🇭", "visita": "Bosnia y Herzegovina 🇧🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 10, "grupo": "Grupo B", "local": "Canadá 🇨🇦", "visita": "Catar 🇶🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 11, "grupo": "Grupo B", "local": "Suiza 🇨🇭", "visita": "Canadá 🇨🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 12, "grupo": "Grupo B", "local": "Bosnia y Herzegovina 🇧🇦", "visita": "Catar 🇶🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO C
        {"id": 13, "grupo": "Grupo C", "local": "Brasil 🇧🇷", "visita": "Marruecos 🇲🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 14, "grupo": "Grupo C", "local": "Haití 🇭🇹", "visita": "Escocia 🏴󠁧󠁢󠁳󠁣󠁴󠁿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 15, "grupo": "Grupo C", "local": "Escocia 🏴󠁧󠁢󠁳󠁣󠁴󠁿", "visita": "Marruecos 🇲🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 16, "grupo": "Grupo C", "local": "Brasil 🇧🇷", "visita": "Haití 🇭🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 17, "grupo": "Grupo C", "local": "Brasil 🇧🇷", "visita": "Escocia 🏴󠁧󠁢󠁳󠁣󠁴󠁿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 18, "grupo": "Grupo C", "local": "Marruecos 🇲🇦", "visita": "Haití 🇭🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO D
        {"id": 19, "grupo": "Grupo D", "local": "Estados Unidos 🇺🇸", "visita": "Paraguay 🇵🇾", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 20, "grupo": "Grupo D", "local": "Australia 🇦🇺", "visita": "Turquía 🇹🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 21, "grupo": "Grupo D", "local": "Estados Unidos 🇺🇸", "visita": "Australia 🇦🇺", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 22, "grupo": "Grupo D", "local": "Turquía 🇹🇷", "visita": "Paraguay 🇵🇾", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 23, "grupo": "Grupo D", "local": "Turquía 🇹🇷", "visita": "Estados Unidos 🇺🇸", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 24, "grupo": "Grupo D", "local": "Paraguay 🇵🇾", "visita": "Australia 🇦🇺", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO E
        {"id": 25, "grupo": "Grupo E", "local": "Alemania 🇩🇪", "visita": "Curazao 🇨🇼", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 26, "grupo": "Grupo E", "local": "Costa de Marfil 🇨🇮", "visita": "Ecuador 🇪🇨", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 27, "grupo": "Grupo E", "local": "Alemania 🇩🇪", "visita": "Costa de Marfil 🇨🇮", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 28, "grupo": "Grupo E", "local": "Ecuador 🇪🇨", "visita": "Curazao 🇨🇼", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 29, "grupo": "Grupo E", "local": "Curazao 🇨🇼", "visita": "Costa de Marfil 🇨🇮", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 30, "grupo": "Grupo E", "local": "Ecuador 🇪🇨", "visita": "Alemania 🇩🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO F
        {"id": 31, "grupo": "Grupo F", "local": "Países Bajos 🇳🇱", "visita": "Japón 🇯🇵", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 32, "grupo": "Grupo F", "local": "Suecia 🇸🇪", "visita": "Túnez 🇹🇳", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 33, "grupo": "Grupo F", "local": "Países Bajos 🇳🇱", "visita": "Suecia 🇸🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 34, "grupo": "Grupo F", "local": "Túnez 🇹🇳", "visita": "Japón 🇯🇵", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 35, "grupo": "Grupo F", "local": "Japón 🇯🇵", "visita": "Suecia 🇸🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 36, "grupo": "Grupo F", "local": "Túnez 🇹🇳", "visita": "Países Bajos 🇳🇱", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO G
        {"id": 37, "grupo": "Grupo G", "local": "Bélgica 🇧🇪", "visita": "Egipto 🇪🇬", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 38, "grupo": "Grupo G", "local": "Irán 🇮🇷", "visita": "Nueva Zelanda 🇳🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 39, "grupo": "Grupo G", "local": "Bélgica 🇧🇪", "visita": "Irán 🇮🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 40, "grupo": "Grupo G", "local": "Nueva Zelanda 🇳🇿", "visita": "Egipto 🇪🇬", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 41, "grupo": "Grupo G", "local": "Egipto 🇪🇬", "visita": "Irán 🇮🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 42, "grupo": "Grupo G", "local": "Nueva Zelanda 🇳🇿", "visita": "Bélgica 🇧🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO H
        {"id": 43, "grupo": "Grupo H", "local": "España 🇪🇸", "visita": "Cabo Verde 🇨🇻", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 44, "grupo": "Grupo H", "local": "Arabia Saudí 🇸🇦", "visita": "Uruguay 🇺🇾", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 45, "grupo": "Grupo H", "local": "España 🇪🇸", "visita": "Arabia Saudí 🇸🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 46, "grupo": "Grupo H", "local": "Uruguay 🇺🇾", "visita": "Cabo Verde 🇨🇻", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 47, "grupo": "Grupo H", "local": "Uruguay 🇺🇾", "visita": "España 🇪🇸", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 48, "grupo": "Grupo H", "local": "Cabo Verde 🇨🇻", "visita": "Arabia Saudí 🇸🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO I
        {"id": 49, "grupo": "Grupo I", "local": "Francia 🇫🇷", "visita": "Senegal 🇸🇳", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 50, "grupo": "Grupo I", "local": "Irak 🇮🇶", "visita": "Noruega 🇳🇴", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 51, "grupo": "Grupo I", "local": "Francia 🇫🇷", "visita": "Irak 🇮🇶", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 52, "grupo": "Grupo I", "local": "Noruega 🇳🇴", "visita": "Senegal 🇸🇳", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 53, "grupo": "Grupo I", "local": "Senegal 🇸🇳", "visita": "Irak 🇮🇶", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 54, "grupo": "Grupo I", "local": "Noruega 🇳🇴", "visita": "Francia 🇫🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO J
        {"id": 55, "grupo": "Grupo J", "local": "Argentina 🇦🇷", "visita": "Argelia 🇩🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 56, "grupo": "Grupo J", "local": "Austria 🇦🇹", "visita": "Jordania 🇯🇴", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 57, "grupo": "Grupo J", "local": "Argentina 🇦🇷", "visita": "Austria 🇦🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 58, "grupo": "Grupo J", "local": "Jordania 🇯🇴", "visita": "Argelia 🇩🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 59, "grupo": "Grupo J", "local": "Argelia 🇩🇿", "visita": "Austria 🇦🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 60, "grupo": "Grupo J", "local": "Jordania 🇯🇴", "visita": "Argentina 🇦🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO K
        {"id": 61, "grupo": "Grupo K", "local": "Portugal 🇵🇹", "visita": "RD Congo 🇨🇩", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 62, "grupo": "Grupo K", "local": "Uzbekistán 🇺🇿", "visita": "Colombia 🇨🇴", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 63, "grupo": "Grupo K", "local": "Portugal 🇵🇹", "visita": "Uzbekistán 🇺🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 64, "grupo": "Grupo K", "local": "Colombia 🇨🇴", "visita": "RD Congo 🇨🇩", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 65, "grupo": "Grupo K", "local": "Colombia 🇨🇴", "visita": "Portugal 🇵🇹", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 66, "grupo": "Grupo K", "local": "RD Congo 🇨🇩", "visita": "Uzbekistán 🇺🇿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        # GRUPO L
        {"id": 67, "grupo": "Grupo L", "local": "Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "visita": "Croacia 🇭🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 68, "grupo": "Grupo L", "local": "Ghana 🇬🇭", "visita": "Panamá 🇵🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 69, "grupo": "Grupo L", "local": "Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "visita": "Ghana 🇬🇭", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 70, "grupo": "Grupo L", "local": "Panamá 🇵🇦", "visita": "Croacia 🇭🇷", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 71, "grupo": "Grupo L", "local": "Panamá 🇵🇦", "visita": "Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 72, "grupo": "Grupo L", "local": "Croacia 🇭🇷", "visita": "Ghana 🇬🇭", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
    ]
    pd.DataFrame(partidos_iniciales).to_csv(PARTIDOS_FILE, index=False)

if not os.path.exists(PREDICCONES_FILE):
    pd.DataFrame(columns=["usuario", "partido_id", "goles_l_pred", "goles_v_pred"]).to_csv(PREDICCONES_FILE, index=False)

# Cargar datos actuales y asegurar tratamiento riguroso de dtypes de Pandas
df_partidos = pd.read_csv(PARTIDOS_FILE)
df_partidos["goles_l_real"] = df_partidos["goles_l_real"].astype(str)
df_partidos["goles_v_real"] = df_partidos["goles_v_real"].astype(str)

df_predicciones = pd.read_csv(PREDICCONES_FILE)

# --- FUNCIÓN LÓGICA DE PUNTAJES ---
def calcular_tabla(df_p, df_preds):
    if df_preds.empty:
        return pd.DataFrame(columns=["Participante", "Puntos Totales", "Resultados Exactos (3pts)", "Tendencias (1pt)"])
    
    partidos_jugados = df_p[df_p["jugado"] == True]
    puntajes = {}
    
    for _, pred in df_preds.iterrows():
        user = pred["usuario"]
        p_id = int(pred["partido_id"])
        
        partido_real = list(partidos_jugados[partidos_jugados["id"] == p_id].to_dict(orient="index").values())
        if not partido_real:
            continue
            
        p_real = partido_real[0]
        
        if user not in puntajes:
            puntajes[user] = {"puntos": 0, "exactos": 0, "tendencias": 0}
            
        gl_real = int(float(p_real["goles_l_real"]))
        gv_real = int(float(p_real["goles_v_real"]))
        gl_pred = int(pred["goles_l_pred"])
        gv_pred = int(pred["goles_v_pred"])
        
        # Sistema estándar: 3 pts exacto, 1 pt tendencia
        if gl_real == gl_pred and gv_real == gv_pred:
            puntajes[user]["puntos"] += 3
            puntajes[user]["exactos"] += 1
        elif (gl_real > gv_real and gl_pred > gv_pred) or (gl_real < gv_real and gl_pred < gv_pred) or (gl_real == gv_real and gl_pred == gv_pred):
            puntajes[user]["puntos"] += 1
            puntajes[user]["tendencias"] += 1

    tabla_data = []
    for u, stats in puntajes.items():
        tabla_data.append([u, stats["puntos"], stats["exactos"], stats["tendencias"]])
        
    df_tabla = pd.DataFrame(tabla_data, columns=["Participante", "Puntos Totales", "Resultados Exactos (3pts)", "Tendencias (1pt)"])
    return df_tabla.sort_values(by="Puntos Totales", ascending=False)


# --- INTERFAZ GRÁFICA ---
st.title("🏆 POLLA MUNDIALISTA 2026 - FASE DE GRUPOS ⚽")
st.write("Registra tus pronósticos para los 12 grupos y compite por el liderato de la primera fase.")

tab1, tab2, tab3 = st.tabs(["📊 Tabla de Posiciones", "📝 Mis Predicciones", "🔒 Control Administrador"])

# PESTAÑA 1: RANKING
with tab1:
    st.header("🏆 Ranking Oficial - Fase de Grupos")
    df_ranking = calcular_tabla(df_partidos, df_predicciones)
    if not df_ranking.empty:
        st.dataframe(df_ranking, use_container_width=True, hide_index=True)
    else:
        st.info("La tabla se activará cuando el administrador ingrese el resultado del primer partido jugado.")

# PESTAÑA 2: PREDICCIONES
with tab2:
    st.header("📝 Tus Pronósticos de Grupos")
    usuario = st.text_input("Ingresa tu Nombre o Apodo:", key="user_name", placeholder="Ej. Tesla Jr.")
    
    if usuario:
        st.subheader(f"Formulario de {usuario}:")
        
        grupos = sorted(df_partidos["grupo"].unique())
        
        with st.form("form_grupos_preds"):
            for grupo in grupos:
                # Menús colapsables para no saturar la pantalla
                with st.expander(f"🗂️ Haz clic para abrir el {grupo}"):
                    partidos_grupo = df_partidos[df_partidos["grupo"] == grupo]
                    
                    for _, row in sorted(partidos_grupo.iterrows(), key=lambda r: r[1]['id']):
                        pred_existente = df_predicciones[(df_predicciones["usuario"].str.lower() == usuario.strip().lower()) & (df_predicciones["partido_id"] == row["id"])]
                        val_l = int(pred_existente.iloc[0]["goles_l_pred"]) if not pred_existente.empty else 0
                        val_v = int(pred_existente.iloc[0]["goles_v_pred"]) if not pred_existente.empty else 0
                        
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**{row['local']} vs {row['visita']}**")
                            if row["jugado"]:
                                try:
                                    gl_disp = int(float(row['goles_l_real']))
                                    gv_disp = int(float(row['goles_v_real']))
                                    st.caption(f"Resultado final: {gl_disp} - {gv_disp}")
                                except ValueError:
                                    st.caption(f"Resultado final: {row['goles_l_real']} - {row['goles_v_real']}")
                        with col2:
                            g_l = st.number_input(f"Goles {row['local']}", min_value=0, max_value=15, value=val_l, step=1, key=f"l_{row['id']}")
                        with col3:
                            g_v = st.number_input(f"Goles {row['visita']}", min_value=0, max_value=15, value=val_v, step=1, key=f"v_{row['id']}")
                        st.markdown("---")
            
            if st.form_submit_button("💾 Guardar Todas Mis Predicciones"):
                for _, row in df_partidos.iterrows():
                    p_id = row["id"]
                    g_l_v = st.session_state[f"l_{p_id}"]
                    g_v_v = st.session_state[f"v_{p_id}"]
                    
                    df_predicciones = df_predicciones[~((df_predicciones["usuario"].str.lower() == usuario.strip().lower()) & (df_predicciones["partido_id"] == p_id))]
                    nueva_p = {"usuario": usuario.strip(), "partido_id": p_id, "goles_l_pred": int(g_l_v), "goles_v_pred": int(g_v_v)}
                    df_predicciones = pd.concat([df_predicciones, pd.DataFrame([nueva_p])], ignore_index=True)
                
                df_predicciones.to_csv(PREDICCONES_FILE, index=False)
                st.success("¡Tus pronósticos para los 72 partidos han sido guardados!")
                st.rerun()
    else:
        st.warning("Escribe tu nombre arriba para activar los partidos.")

# PESTAÑA 3: ADMIN
with tab3:
    st.header("🔒 Panel de Resultados Oficiales")
    input_pass = st.text_input("Contraseña del Administrador:", type="password")
    
    if input_pass == PASSWORD_ADMIN:
        st.success("Identidad confirmada.")
        
        with st.form("form_admin_grupos"):
            grupos_admin = sorted(df_partidos["grupo"].unique())
            for grupo in grupos_admin:
                st.markdown(f"### 🏁 Resultados del {grupo}")
                partidos_grupo = df_partidos[df_partidos["grupo"] == grupo]
                
                for idx, row in sorted(partidos_grupo.iterrows(), key=lambda r: r[1]['id']):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        st.write(f"**{row['local']} vs {row['visita']}**")
                    with col2:
                        try:
                            val_l_real = int(float(row["goles_l_real"])) if row["jugado"] else 0
                        except ValueError:
                            val_l_real = 0
                        g_l_r = st.number_input("Goles Local", min_value=0, max_value=15, value=val_l_real, key=f"rl_{row['id']}")
                    with col3:
                        try:
                            val_v_real = int(float(row["goles_v_real"])) if row["jugado"] else 0
                        except ValueError:
                            val_v_real = 0
                        g_v_r = st.number_input("Goles Visita", min_value=0, max_value=15, value=val_v_real, key=f"rv_{row['id']}")
                    with col4:
                        marcar_jugado = st.checkbox("¿Finalizado?", value=row["jugado"], key=f"j_{row['id']}")
                    st.markdown("---")
            
            if st.form_submit_button("🔄 Publicar Resultados Reales"):
                for idx, row in df_partidos.iterrows():
                    p_id = row["id"]
                    df_partidos.at[idx, "goles_l_real"] = str(int(st.session_state[f"rl_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "goles_v_real"] = str(int(st.session_state[f"rv_{p_id}"])) if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "jugado"] = bool(st.session_state[f"j_{p_id}"])
                
                df_partidos.to_csv(PARTIDOS_FILE, index=False)
                st.success("¡Puntajes de la Fase de Grupos recalculados de forma exitosa!")
                st.rerun()
        
        st.subheader("📥 Respaldos de Seguridad")
        st.download_button("Descargar Tabla Partidos (CSV)", df_partidos.to_csv(index=False).encode('utf-8'), "partidos_grupos_completo.csv", "text/csv")
        st.download_button("Descargar Tabla Predicciones (CSV)", df_predicciones.to_csv(index=False).encode('utf-8'), "predicciones_grupos_completo.csv", "text/csv")
