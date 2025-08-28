import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import io

st.title("📋 Registro de Actividades")

# --- Datos generales ---
cliente = st.text_input("Nombre del cliente:")

# Supervisor
col_sup1, col_sup2 = st.columns([1,2])
with col_sup1:
    supervisor_tipo = st.selectbox(
        "Supervisor (tipo):",
        ["Supervisor de Molienda", "Supervisor de Cianuración", "Supervisor de Flotación"]
    )
with col_sup2:
    supervisor_nombre = st.text_input("Nombre del Supervisor:")

# Fecha y hora de inicio en la misma fila
col1, col2, col3, col4 = st.columns([2,1,1,1])
with col1:
    fecha_inicio = st.date_input("Fecha de inicio", value=date.today())
with col2:
    hora_inicio_h = st.selectbox("Hora", options=list(range(0,24)), key="hora_inicio_h")
with col3:
    minuto_inicio_m = st.selectbox("Minuto", options=list(range(0,60)), key="minuto_inicio_m")
with col4:
    st.write(f"⏰ {hora_inicio_h:02}:{minuto_inicio_m:02}")
hora_inicio = time(hora_inicio_h, minuto_inicio_m)

# Fecha y hora de parada en la misma fila
col5, col6, col7, col8 = st.columns([2,1,1,1])
with col5:
    fecha_parada = st.date_input("Fecha de parada", value=date.today())
with col6:
    hora_parada_h = st.selectbox("Hora", options=list(range(0,24)), key="hora_parada_h")
with col7:
    minuto_parada_m = st.selectbox("Minuto", options=list(range(0,60)), key="minuto_parada_m")
with col8:
    st.write(f"⏰ {hora_parada_h:02}:{minuto_parada_m:02}")
hora_parada = time(hora_parada_h, minuto_parada_m)

# Observacion
observacion = st.text_area("Observación:")

# Calculo de días de trabajo con decimales
dt_inicio = datetime.combine(fecha_inicio, hora_inicio)
dt_parada = datetime.combine(fecha_parada, hora_parada)
dias_trabajo = (dt_parada - dt_inicio).total_seconds() / (24*3600)
st.write(f"📅 Días de trabajo: **{dias_trabajo:.1f} días**")

# --- Implementos ---
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

with tabs[0]:
    st.subheader("Implementos - Molienda")
    for i, item in enumerate(molienda_items):
        molienda_data[item] = st.number_input(item, min_value=0.0, step=0.1, key=f"m_{i}")

with tabs[1]:
    st.subheader("Implementos - Cianuración")
    for i, item in enumerate(cianuracion_items):
        cianuracion_data[item] = st.number_input(item, min_value=0.0, step=0.1, key=f"c_{i}")

with tabs[2]:
    st.subheader("Implementos - Flotación")
    for i, item in enumerate(flotacion_items):
        flotacion_data[item] = st.number_input(item, min_value=0.0, step=0.1, key=f"f_{i}")


# --- Exportación ---
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

