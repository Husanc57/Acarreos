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




class Imprime_Pdf_Modifica():

    def exportar_a_pdf(data):

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize= landscape(A3))
        styles = getSampleStyleSheet()

        content = []
        title = Paragraph("REPORTE ACARREOS POR BOLETA", styles['Title'])
        content.append(title)
        content.append(Spacer(1, 9))
    
        summary_text = """
        Este reporte nos indica el total de viajes de acarreo de materiales al  proyecto,
        y su logística en las operaciones de transporte.
        Este incluye detalles acerca de las operaciones de transporte, se pueden observar 
        datos del acarreo como:  compañias transportistas,  boletas,  fechas,  maquinaria, 
        capacidad en m3, distancias recorridas,  viajes, volumenes, y precios asociados a 
        cada viaje.
        """
        summary = Paragraph(summary_text, styles['Normal'])
        content.append(summary)
        content.append(Spacer(1, 9))

        table_data = [data[0]] + data[1:]
    
        table_style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.gray),
            ('TEXTCOLOR', (0,0), (-1,0), "#8C0412"),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0),9),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, "#8C0412")
        ])
    
        table = Table(table_data, repeatRows=1)
        table.setStyle(table_style)
        content.append(table)
    
        doc.build(content)
    
        buffer.seek(0)
        return buffer


    def main_pdf_modifica(boleta1):
        #st.title("SISTEMA DE ACARREOS")
    
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Ver Datos", "Exportar a PDF", "Análisis de Datos"])
    
        with tab1:

            st.header("Datos de Acarreo")
            try:
                conn = sqlite3.connect("Acarreo_Proyectos.db")
                df = pd.read_sql_query(f"select * from datos_acarreo where boleta = '{boleta1}'", conn)
                st.data_editor(df)


                with st.form("cost_form"):
                    st.subheader("")


                    # Input fields
                    """fecha1             = st.text("Fecha               : " + df.fecha)
                    boleta1            = st.text("Boleta              : " + df.boleta )
                    contratista1       = st.text("Codigo Empresa      : " + df.contratista)      
                    maquina1           = st.text("Maquina             : " + df.maquina) 
                    capacidad1         = st.text("Capacidad maquina   : " + str(df.capacidad))
                    lugar_salida1      = st.text("Lugar de salida     : " + df.lugar_salida)
                    lugar_llegada1     = st.text("Lugar de llegada    : " + df.lugar_llegada)
                    distancia1         = st.text("Distancia           : " + str(df.distancia))
                    viajes1            = st.text("No. de viajes       : " + str(df.viajes))
                    m31                = st.text("m3                  : " + capacidad1 * viajes1)
                    material1          = st.text("Material            : " + df.material)
                    m3_km1             = st.text("m3_km               : " + str(val(distancia1) * val(viajes1) * val(m31)))
                    precio1            = st.text("Precio unitario     : " + str(df.precio))
                    monto1             = st.text("m3                  : " + str(val(m3_km1) * val(precio1)))"""

                    
                    submitted = st.form_submit_button(label="Modifica datos")

                
                    
                if submitted:
                    conn = sqlite3.connect("Acarreo_Proyectos.db")
                    c = conn.cursor()

                    c.execute("UPDATE datos_acarreo SET fecha = fecha1, boleta = boleta1, contratista = contratista1, maquina= maquina1, capacidad = capacidad1, lugar_salida = lugar_salida1, lugar_llegada = lugar_llegada1, distancia = distancia1, viajes = viajes1, m3 = m31, material = material1, m3_km = m3_km1, precio = precio1, monto = monto1 WHERE boleta = '{boleta1}'")

                    conn.commit()
                    conn.close()

                    total_cost = monto
                    st.success(f"El monto  de este acarreo es  : Ȼ{total_cost:,.2f}")    
                
                       
            except Exception as e:
                st.error(f"Error buscando datos: {e}")

            finally:
                conn.close()
    
        with tab2:

            st.header("PDF Export")
            
            try:
                conn = sqlite3.connect("Acarreo_Proyectos.db")
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT * FROM datos_acarreo WHERE boleta = '{boleta1}'")
                data = [("Fecha", "Boleta", "Contratista", "Maquina", 
                        "Capacidad", "Lugar Salida", "Lugar Llegada", "Distancia", 
                        "Viajes", "Metros", "Material", "m3/km", "Precio", "Monto")] + cursor.fetchall()
                
                pdf_buffer = Imprime_Pdf_Modifica.exportar_a_pdf(data)
                
                st.download_button(
                    label="Descargar Reporte PDF",
                    data=pdf_buffer,
                    file_name="Reporte_Boleta.pdf",
                    mime="app")
            
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if 'conn' in locals():
                    conn.close()
    
        with tab3:
            st.header("")
            try:
                conn = sqlite3.connect("Acarreo_Proyectos.db")
                df = pd.read_sql_query(f"SELECT * FROM datos_acarreo WHERE boleta = '{boleta1}'", conn)
         
                #Check the column names
                #st.write("Nombre de las columnas:", df.columns)
            
                # Basic analytics
                st.subheader("Estadísticas Básicas")
                col1, col2 = st.columns(2)
            
                with col1:
                    st.metric("Total de viajes", df['viajes'].sum())
                    st.metric("Distancia Promedio", f"{df['distancia'].mean():.2f} km")
            
                with col2:
                    st.metric("Total costo", f"Ȼ{df['monto'].sum():.2f}")
                    st.metric("Costo Promedio m3/km", f"Ȼ{df['precio'].mean():.2f}")
            
                # Optional: Visualizations
                st.subheader("Visualización de los contratistas")
                st.bar_chart(df.groupby('contratista')['monto'].sum())
        
            except Exception as e:
                st.error(f"Error en análisis: {e}")
            finally:
                conn.close()


if __name__ == "__main__":
    Imprime_Pdf_Uno.main_pdf_uno()
    