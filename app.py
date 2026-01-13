import streamlit as st
from supabase import create_client
import pandas as pd
import json

# CONFIGURACIÓN
st.set_page_config(page_title="NBA IA Picks", page_icon="🏀", layout="centered")

# CONEXIÓN SUPABASE (Lectura de Secretos)
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except:
    st.error("⚠️ Error de configuración: Faltan secretos.")
    st.stop()

def get_data():
    # Traemos el último registro
    response = supabase.table('predicciones').select("*").order('id', desc=True).limit(1).execute()
    if response.data: return response.data[0]
    return None

# INTERFAZ
st.title("🤖 NBA IA Analyst")
st.caption("Predicciones diarias automatizadas desde Kaggle Cloud")

data = get_data()

if data:
    st.success(f"📅 **Datos del: {data['fecha']}** | 🕒 Actualizado: {data['hora_ejecucion']}")

    # Pestañas para organizar
    tab1, tab2 = st.tabs(["🧠 Análisis & Picks", "📊 Datos Crudos"])

    with tab1:
        st.markdown("### 🎯 Predicciones de Hoy")
        st.markdown(data['analisis_gemini'])

    with tab2:
        st.write("Estadísticas procesadas:")
        st.json(data['datos_brutos'])

else:
    st.info("Esperando la primera ejecución del bot...")

if st.button("Recargar Datos"):
    st.rerun()
