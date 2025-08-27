import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Formulario de Trabajo")

# Datos iniciales
cliente = st.text_input("Nombre del cliente:")
supervisor = st.text_input("Supervisor:")
fecha_inicio = st.date_input("Fecha de inicio")
hora_inicio = st.time_input("Hora de inicio")
fecha_parada = st.date_input("Fecha de parada")
hora_parada = st.time_input("Hora de parada")
observacion = st.text_area("Observación:")

# Calcular días de trabajo
if fecha_parada and fecha_inicio:
    dias = (fecha_parada - fecha_inicio).days
    st.write(f"**Días de trabajo:** {dias}")

# Tabla de implementos (ejemplo con Molienda)
st.subheader("MOLIENDA")
implementos_molienda = [
    "Bayetas", "Franela", "Mallas 80", "Mallas 60",
    "Pernos 5/16 X 1 1/4", "Palas Tombo",
    "Platón Grande", "Platón Chico",
    "Horas Alquiler Chancha ($5/hora)",
    "Muestra Análisis de Arena Oro Total",
    "Pruebas de Cianuración", "Mandiles", "Otros EPP-", "Alimentación"
]

valores_molienda = {}
for imp in implementos_molienda:
    valores_molienda[imp] = st.number_input(imp, min_value=0, step=1)

# Exportar
if st.button("Exportar a Excel"):
    df = pd.DataFrame.from_dict(valores_molienda, orient='index', columns=["Cantidad"])
    df.to_excel("implementos.xlsx")
    st.success("Exportado a implementos.xlsx")
