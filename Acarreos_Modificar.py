import streamlit as st
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, A4, A5, letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import io
import pandas as pd

#st.image("Imagen1.jpg", caption="Sistema de Acarreos")

# Title
st.title("")

boleta1 = st.text_input("Digite la boleta  : ")
    
if boleta1:
    conn = sqlite3.connect("Acarreo_Proyectos.db")
    c = conn.cursor()
    #c.execute(f"select * from datos_acarreo where boleta = '{boleta1}'")
    c = pd.read_sql_query(f"""UPDATE datos_acarreo (fecha, boleta, contratista, maquina, capacidad, lugar_salida, lugar_llegada, distancia, viajes, m3, material, m3_km, precio, monto ) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(fecha, boleta, contratista, maquina, capacidad, lugar_salida, lugar_llegada, distancia, viajes, m3, material, m3_km, precio, monto)) where boleta = '{boleta1}'", conn)
   

if submitted:
    conn = sqlite3.connect("Acarreo_Proyectos.db")
    c = conn.cursor()
    
    c.execute("""UPDATE datos_acarreo (fecha, boleta, contratista, maquina, capacidad, lugar_salida, lugar_llegada, distancia, viajes, m3, material, m3_km, precio, monto) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(fecha, boleta, contratista, maquina, capacidad, lugar_salida, lugar_llegada, distancia, viajes, m3, material, m3_km, precio, monto))

    conn.commit()
    conn.close()

    total_cost = monto
    st.success(f"El monto  de este acarreo es  : Ȼ{total_cost:,.2f}")

else:

    st.info("Complete el formulario y haga clic en el botón para ingresar datos")

