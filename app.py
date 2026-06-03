import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Polla Mundial 2026 - Grupos", page_icon="⚽", layout="wide")

# Archivos de base de datos local
PARTIDOS_FILE = "partidos_grupos.csv"
PREDICCONES_FILE = "predicciones_grupos.csv"
PASSWORD_ADMIN = "grupos2026"  # Contraseña para el administrador

# --- INICIALIZACIÓN DEL FIXTURE DE GRUPOS ---
# Aquí puedes expandir la lista con todos los partidos de la fase de grupos que quieras incluir
if not os.path.exists(PARTIDOS_FILE):
    partidos_iniciales = [
        {"id": 1, "grupo": "Grupo A", "local": "México 🇲🇽", "visita": "Sudáfrica 🇿🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 2, "grupo": "Grupo A", "local": "Nueva Zelanda 🇳🇿", "visita": "Irlanda 🇮🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 3, "grupo": "Grupo B", "local": "Estados Unidos 🇺🇸", "visita": "Paraguay 🇵🇾", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 4, "grupo": "Grupo B", "local": "Canadá 🇨🇦", "visita": "Togo 🇹🇬", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 5, "grupo": "Grupo C", "local": "Brasil 🇧🇷", "visita": "Marruecos 🇲🇦", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
        {"id": 6, "grupo": "Grupo D", "local": "Argentina 🇦🇷", "visita": "Suecia 🇸🇪", "goles_l_real": "-", "goles_v_real": "-", "jugado": False},
    ]
    pd.DataFrame(partidos_iniciales).to_csv(PARTIDOS_FILE, index=False)

if not os.path.exists(PREDICCONES_FILE):
    pd.DataFrame(columns=["usuario", "partido_id", "goles_l_pred", "goles_v_pred"]).to_csv(PREDICCONES_FILE, index=False)

# Cargar datos actuales
df_partidos = pd.read_csv(PARTIDOS_FILE)
df_predicciones = pd.read_csv(PREDICCONES_FILE)

# --- FUNCIÓN LOGICA DE PUNTAJES ---
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
            
        gl_real = int(p_real["goles_l_real"])
        gv_real = int(p_real["goles_v_real"])
        gl_pred = int(pred["goles_l_pred"])
        gv_pred = int(pred["goles_v_pred"])
        
        # Sistema de puntaje: 3 pts exacto, 1 pt tendencia
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
st.write("Registra tus pronósticos para los grupos y conviértete en el campeón de la primera fase.")

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
    usuario = st.text_input("Ingresa tu Nombre o Apodo:", key="user_name", placeholder="Tu nombre para el grupo")
    
    if usuario:
        st.subheader(f"Formulario de {usuario}:")
        grupos = sorted(df_partidos["grupo"].unique())
        
        with st.form("form_grupos_preds"):
            for grupo in grupos:
                st.markdown(f"### 🗂️ {grupo}")
                partidos_grupo = df_partidos[df_partidos["grupo"] == grupo]
                
                for _, row in sorted(partidos_grupo.iterrows(), key=lambda r: r[1]['id']):
                    # Recordar elecciones anteriores si existen
                    pred_existente = df_predicciones[(df_predicciones["usuario"].str.lower() == usuario.strip().lower()) & (df_predicciones["partido_id"] == row["id"])]
                    val_l = int(pred_existente.iloc[0]["goles_l_pred"]) if not pred_existente.empty else 0
                    val_v = int(pred_existente.iloc[0]["goles_v_pred"]) if not pred_existente.empty else 0
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{row['local']} vs {row['visita']}**")
                        if row["jugado"]:
                            st.caption(f"Resultado final: {int(row['goles_l_real'])} - {int(row['goles_v_real'])}")
                    with col2:
                        g_l = st.number_input(f"Goles {row['local']}", min_value=0, max_value=15, value=val_l, step=1, key=f"l_{row['id']}")
                    with col3:
                        g_v = st.number_input(f"Goles {row['visita']}", min_value=0, max_value=15, value=val_v, step=1, key=f"v_{row['id']}")
                    st.markdown("---")
            
            if st.form_submit_button("💾 Guardar / Actualizar Grupo Completo"):
                for _, row in df_partidos.iterrows():
                    p_id = row["id"]
                    g_l_v = st.session_state[f"l_{p_id}"]
                    g_v_v = st.session_state[f"v_{p_id}"]
                    
                    df_predicciones = df_predicciones[~((df_predicciones["usuario"].str.lower() == usuario.strip().lower()) & (df_predicciones["partido_id"] == p_id))]
                    nueva_p = {"usuario": usuario.strip(), "partido_id": p_id, "goles_l_pred": g_l_v, "goles_v_pred": g_v_v}
                    df_predicciones = pd.concat([df_predicciones, pd.DataFrame([nueva_p])], ignore_index=True)
                
                df_predicciones.to_csv(PREDICCONES_FILE, index=False)
                st.success("¡Pronósticos de la Fase de Grupos guardados exitosamente!")
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
            for idx, row in df_partidos.iterrows():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"({row['grupo']}) **{row['local']} vs {row['visita']}**")
                with col2:
                    val_l_real = int(row["goles_l_real"]) if row["jugado"] else 0
                    g_l_r = st.number_input("Goles Local", min_value=0, max_value=15, value=val_l_real, key=f"rl_{row['id']}")
                with col3:
                    val_v_real = int(row["goles_v_real"]) if row["jugado"] else 0
                    g_v_r = st.number_input("Goles Visita", min_value=0, max_value=15, value=val_v_real, key=f"rv_{row['id']}")
                with col4:
                    marcar_jugado = st.checkbox("¿Finalizado?", value=row["jugado"], key=f"j_{row['id']}")
                st.markdown("---")
            
            if st.form_submit_button("🔄 Publicar Resultados Reales"):
                for idx, row in df_partidos.iterrows():
                    p_id = row["id"]
                    df_partidos.at[idx, "goles_l_real"] = st.session_state[f"rl_{p_id}"] if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "goles_v_real"] = st.session_state[f"rv_{p_id}"] if st.session_state[f"j_{p_id}"] else "-"
                    df_partidos.at[idx, "jugado"] = st.session_state[f"j_{p_id}"]
                
                df_partidos.to_csv(PARTIDOS_FILE, index=False)
                st.success("¡Puntajes recalculados con los resultados oficiales de la fecha!")
                st.rerun()
        
        st.subheader("📥 Respaldos locales")
        st.download_button("Descargar Tabla Partidos (CSV)", df_partidos.to_csv(index=False).encode('utf-8'), "partidos_grupos_backup.csv", "text/csv")
        st.download_button("Descargar Tabla Predicciones (CSV)", df_predicciones.to_csv(index=False).encode('utf-8'), "predicciones_grupos_backup.csv", "text/csv")