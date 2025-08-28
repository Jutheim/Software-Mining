import streamlit as st
import pandas as pd
from datetime import datetime, time
import io

st.set_page_config(page_title="Formulario de Trabajo", layout="centered")
st.title("📋 Formulario de Trabajo")

# ================== DATOS GENERALES ==================
st.header("Datos Generales")

cliente = st.text_input("Nombre del cliente:")

supervisor_tipo = st.selectbox(
    "Supervisor (tipo):",
    ["Supervisor de Molienda", "Supervisor de Cianuración", "Supervisor de Flotación"]
)

supervisor_nombre = st.text_input("Nombre del Supervisor:")

# Fecha y hora inicio
col_fecha_inicio, col_hora_inicio_h, col_hora_inicio_m = st.columns([2,1,1])
with col_fecha_inicio:
    fecha_inicio = st.date_input("Fecha inicio:", datetime.today())
with col_hora_inicio_h:
    hora_inicio_h = st.selectbox("Hora", list(range(0,24)), index=datetime.now().hour)
with col_hora_inicio_m:
    minuto_inicio_m = st.selectbox("Minuto", list(range(0,60)), index=datetime.now().minute)

hora_inicio = time(hora_inicio_h, minuto_inicio_m)
st.write(f"⏰ Hora inicio seleccionada: {hora_inicio_h:02}:{minuto_inicio_m:02}")

# Fecha y hora parada
col_fecha_parada, col_hora_parada_h, col_hora_parada_m = st.columns([2,1,1])
with col_fecha_parada:
    fecha_parada = st.date_input("Parada:", datetime.today())
with col_hora_parada_h:
    hora_parada_h = st.selectbox("Hora", list(range(0,24)), index=datetime.now().hour, key="hora_parada_h")
with col_hora_parada_m:
    minuto_parada_m = st.selectbox("Minuto", list(range(0,60)), index=datetime.now().minute, key="minuto_parada_m")

hora_parada = time(hora_parada_h, minuto_parada_m)
st.write(f"⏰ Hora parada seleccionada: {hora_parada_h:02}:{minuto_parada_m:02}")

observacion = st.text_area("Observacion:")

# Calcular días de trabajo con decimal
delta_inicio = datetime.combine(fecha_inicio, hora_inicio)
delta_parada = datetime.combine(fecha_parada, hora_parada)
dias_trabajo = (delta_parada - delta_inicio).total_seconds() / 86400
st.write(f"🕒 Días de trabajo: **{dias_trabajo:.1f} días**")

# ================== IMPLEMENTOS ==================
st.header("Implementos")

tabs = st.tabs(["Molienda", "Cianuración", "Flotación"])

molienda_items = [
    "Bayetas","Franela","Mallas 80","Mallas 60","Pernos 5/16 X 1 1/4",
    "Palas Tombo","Platón Grande","Platón Chico","Horas alquiler chancha ($5/hora)",
    "Muestra análisis arena oro total","Pruebas de cianuración","Mandiles","Otros EPP","Alimentación"
]
cianuracion_items = [
    "Cianuro","Cal","Saquillos","Carbon activado","Muestra de solución",
    "Titulación de cianuro","Análisis de arena","Alimentación",
    "24h duración proceso (excedente $45/hora)"
]
flotacion_items = [
    "Big bag","Excedente de sulfato de cobre",
    "Servicio filtrado $15 por bigbag","Alimentación"
]

molienda_data, cianuracion_data, flotacion_data = {}, {}, {}

# Ingreso manual de implementos
with tabs[0]:
    st.subheader("Implementos - Molienda")
    for i, item in enumerate(molienda_items):
        molienda_data[item] = st.text_input(item, key=f"m_{i}")

with tabs[1]:
    st.subheader("Implementos - Cianuración")
    for i, item in enumerate(cianuracion_items):
        cianuracion_data[item] = st.text_input(item, key=f"c_{i}")

with tabs[2]:
    st.subheader("Implementos - Flotación")
    for i, item in enumerate(flotacion_items):
        flotacion_data[item] = st.text_input(item, key=f"f_{i}")

# ================== EXPORTAR A EXCEL ==================
if st.button("📤 Exportar a Excel"):
    export_data = {
        "Cliente": cliente,
        "Supervisor": supervisor_nombre,
        "Fecha inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "Hora inicio": f"{hora_inicio.hour:02}:{hora_inicio.minute:02}",
        "Fecha parada": fecha_parada.strftime("%Y-%m-%d"),
        "Hora parada": f"{hora_parada.hour:02}:{hora_parada.minute:02}",
        "Observacion": observacion,
        "Dias de trabajo": round(dias_trabajo, 1)
    }

    if "Molienda" in supervisor_tipo:
        export_data.update(molienda_data)
    elif "Cianuración" in supervisor_tipo:
        export_data.update(cianuracion_data)
    elif "Flotación" in supervisor_tipo:
        export_data.update(flotacion_data)

    df = pd.DataFrame([export_data])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Formulario")

    st.download_button(
        label="📥 Descargar Excel",
        data=output.getvalue(),
        file_name="formulario_exportado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
