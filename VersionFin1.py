import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date, datetime

st.title("📋 Formulario de Control de Procesos")

# --- Datos iniciales ---
cliente = st.text_input("Nombre del cliente")
tipo_supervisor = st.selectbox("Supervisor (tipo)", ["Supervisor de Molienda", "Supervisor de Cianuración", "Supervisor de Flotación"])
nombre_supervisor = st.text_input("Nombre del Supervisor")

# --- Fecha y horas ---
fecha_inicio = st.date_input("Fecha de inicio", value=date.today())
col1, col2 = st.columns(2)
with col1:
    hora_inicio_h = st.number_input("Hora inicio (0-23)", min_value=0, max_value=23, step=1, value=8, key="hora_inicio_h")
with col2:
    hora_inicio_m = st.number_input("Minuto inicio (0-59)", min_value=0, max_value=59, step=1, value=0, key="hora_inicio_m")

parada = st.date_input("Fecha de parada", value=date.today())
col3, col4 = st.columns(2)
with col3:
    hora_parada_h = st.number_input("Hora parada (0-23)", min_value=0, max_value=23, step=1, value=17, key="hora_parada_h")
with col4:
    hora_parada_m = st.number_input("Minuto parada (0-59)", min_value=0, max_value=59, step=1, value=0, key="hora_parada_m")

observacion = st.text_area("Observación")

# Calculo de días con decimales (diferencia total en horas / 24)
inicio_dt = datetime.combine(fecha_inicio, datetime.min.time()).replace(hour=hora_inicio_h, minute=hora_inicio_m)
parada_dt = datetime.combine(parada, datetime.min.time()).replace(hour=hora_parada_h, minute=hora_parada_m)
diff_horas = (parada_dt - inicio_dt).total_seconds() / 3600
dias_trabajo = diff_horas / 24
st.write(f"**🕒 Días de trabajo:** {dias_trabajo:.1f} días")

# --- Implementos ---
st.subheader("Implementos")

implementos = {
    "Molienda": [
        "Bayetas", "Franela", "Mallas 80", "Mallas 60",
        "Pernos 5/16 X 1 1/4", "Palas Tombo", "Platón Grande", "Platón Chico",
        "Horas alquiler chancha ($5/hora)", "Muestra análisis arena oro total",
        "Pruebas de cianuración", "Mandiles", "Otros EPP", "Alimentación"
    ],
    "Cianuración": [
        "Cianuro", "Cal", "Saquillos", "Carbon Activado", "Muestra de solución",
        "Titulación de cianuro", "Análisis de arena", "Alimentación",
        "24h proceso (excedente $45/h)"
    ],
    "Flotación": [
        "Big Bag", "Excedente de sulfato de cobre", "Servicio filtrado ($15/bigbag)",
        "Alimentación"
    ]
}

implementos_data = {}
grupo = tipo_supervisor.split()[-1].capitalize()

for item in implementos[grupo]:
    val = st.text_input(item, value="0", key=f"{tipo_supervisor}_{item}")
    try:
        implementos_data[item] = float(val)
    except ValueError:
        implementos_data[item] = 0.0

# --- Exportación ---
st.subheader("📤 Exportar datos")

if st.button("📤 Exportar a Excel"):
    export_data = {
        "Cliente": cliente,
        "Nombre Supervisor": nombre_supervisor,
        "Fecha Inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "Hora Inicio": f"{hora_inicio_h:02d}:{hora_inicio_m:02d}",
        "Parada": parada.strftime("%Y-%m-%d"),
        "Hora Parada": f"{hora_parada_h:02d}:{hora_parada_m:02d}",
        "Observación": observacion,
        "Días de trabajo": f"{dias_trabajo:.1f}"
    }

    export_data.update(implementos_data)

    df = pd.DataFrame([export_data])

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Formulario")

    st.download_button(
        label="📥 Descargar Excel",
        data=output.getvalue(),
        file_name="formulario_exportado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
