import streamlit as st
import pandas as pd
from io import BytesIO

# Datos de prueba
data = {"Nombre": ["Juan", "María"], "Edad": [30, 25]}
df = pd.DataFrame(data)

# Generar Excel en memoria
output = BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False)
output.seek(0)

# Botón de descarga
st.download_button(
    label="Descargar Excel",
    data=output,
    file_name="formulario.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
