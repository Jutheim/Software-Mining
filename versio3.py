import streamlit as st
import pandas as pd
from datetime import datetime, date
from io import BytesIO

st.set_page_config(page_title="Formulario de Trabajo", layout="centered")
st.title("📋 Formulario de Trabajo")

# ================== ESTADO INICIAL (para que no se reinicien las horas) ==================
if "hora_inicio" not in st.session_state:
    st.session_state.hora_inicio = datetime.now().time().replace(microsecond=0)
if "hora_parada" not in st.session_state:
    st.session_state.hora_parada = datetime.now().time().replace(microsecond=0)
if "fecha_inicio" not in st.session_state:
    st.session_state.fecha_inicio = date.today()
if "fecha_parada" not in st.session_state:
    st.session_state.fecha_parada = date.today()

# ================== DATOS GENERALES ==================
st.header("Datos Generales")

cliente = st.text_input("Nombre del cliente:")

supervisor_tipo = st.selectbox(
    "Supervisor (tipo):",
    ["Supervisor de Molienda", "Supervisor de Cianuración", "Supervisor de Flotación"],
    key="supervisor_tipo"
)
supervisor_nombre = st.text_input("Nombre del Supervisor:", key="supervisor_nombre")

col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input("Fecha de inicio:", value=st.session_state.fecha_inicio, key="fecha_inicio")
with col2:
    hora_inicio = st.time_input("Hora de inicio:", value=st.session_state.hora_inicio, key="hora_inicio")

col3, col4 = st.columns(2)
with col3:
    fecha_parada = st.date_input("Parada:", value=st.session_state.fecha_parada, key="fecha_parada")
with col4:
    hora_parada = st.time_input("Hora de Parada:", value=st.session_state.hora_parada, key="hora_parada")

observacion = st.text_area("Observación:", key="observacion")

# Calcular días de trabajo (solo por fecha, como pediste)
dias_trabajo = (fecha_parada - fecha_inicio).days
if dias_trabajo < 0:
    dias_trabajo = 0
st.write(f"🕒 Días de trabajo: **{dias_trabajo} días**")

# ================== IMPLEMENTOS ==================
st.header("Implementos")

tabs = st.tabs(["Molienda", "Cianuración", "Flotación"])

implementos = {
    "Molienda": [
        "Bayetas", "Franela", "Mallas 80", "Mallas 60",
        "Pernos para cambiar mallas 5/16 X 1 1/4", "Palas Tombo",
        "Platón Grande", "Platón Chico",
        "HORAS ALQUILER CHANCHA $5 LA HORA",
        "MUESTRA DE ANALISIS DE ARENA ORO TOTAL",
        "PUEBAS DE CIANURACIÓN", "MANDILES", "OTROS EPP-", "ALIMENTACIÓN"
    ],
    "Cianuración": [
        "CIANURO", "CAL", "SAQUILLOS", "CARBON ACTIVADO",
        "MUESTRA DE SOLUCIÓN", "TITULACIÓN DE CIANURO",
        "ANALISIS DE ARENA", "ALIMENTACIÓN",
        "24 HORAS DURACIÓN DEL PROCESO /EXCEDENTE $45 POR HORA"
    ],
    "Flotación": [
        "BIG BAG", "EXCEDENTE DE SULFATO DE COBRE",
        "SERIVICO FILTRADO $15 POR BIGBAG", "ALIMENTACIÓN"
    ]
}

molienda_data = {}
cianuracion_data = {}
flotacion_data = {}

# Pestaña Molienda
with tabs[0]:
    st.subheader("Molienda")
    for item in implementos["Molienda"]:
        key = f"molienda_{item}"
        molienda_data[item] = st.number_input(item, min_value=0, step=1, key=key)

# Pestaña Cianuración
with tabs[1]:
    st.subheader("Cianuración")
    for item in implementos["Cianuración"]:
        key = f"cianuracion_{item}"
        cianuracion_data[item] = st.number_input(item, min_value=0, step=1, key=key)

# Pestaña Flotación
with tabs[2]:
    st.subheader("Flotación")
    for item in implementos["Flotación"]:
        key = f"flotacion_{item}"
        flotacion_data[item] = st.number_input(item, min_value=0, step=1, key=key)

# ================== EXPORTAR A EXCEL ==================
st.header("📤 Exportar")

def build_excel_bytes():
    # Datos generales
    generales = {
        "Cliente": [cliente],
        "Supervisor (tipo)": [supervisor_tipo],
        "Nombre del Supervisor": [supervisor_nombre],
        "Fecha inicio": [fecha_inicio],
        "Hora inicio": [hora_inicio.strftime("%H:%M")],
        "Parada": [fecha_parada],
        "Hora parada": [hora_parada.strftime("%H:%M")],
        "Observación": [observacion],
        "Días de trabajo": [dias_trabajo]
    }
    df_generales = pd.DataFrame(generales)

    # Implementos a dataframes
    df_molienda = pd.DataFrame(list(molienda_data.items()), columns=["Molienda", "Cantidad"])
    df_cianuracion = pd.DataFrame(list(cianuracion_data.items()), columns=["Cianuración", "Cantidad"])
    df_flotacion = pd.DataFrame(list(flotacion_data.items()), columns=["Flotación", "Cantidad"])

    # Escribir a un buffer en memoria
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df_generales.to_excel(writer, sheet_name="Datos Generales", index=False)
        df_molienda.to_excel(writer, sheet_name="Molienda", index=False)
        df_cianuracion.to_excel(writer, sheet_name="Cianuración", index=False)
        df_flotacion.to_excel(writer, sheet_name="Flotación", index=False)
    buffer.seek(0)
    return buffer

# Botón para generar y descargar
excel_buffer = build_excel_bytes()
st.download_button(
    label="💾 Descargar Excel",
    data=excel_buffer,
    file_name="formulario_exportado.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
