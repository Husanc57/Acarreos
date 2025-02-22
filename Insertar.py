import streamlit as st
import sqlite3


class InsertaDatos:

    def __init__(self, fecha, boleta, contratista, maquina, capacidad, lugar_salida, lugar_llegada, distancia, viajes, m3, material, m3_km, precio, monto):

        self.fecha = fecha
        self.boleta = boleta
        self.contratista = contratista
        self.maquina = maquina
        self.capacidad = capacidad
        self.lugar_salida = lugar_salida
        self.ligar_llegada = lugar_llegada
        self.distancia = distancia
        self.viajes = viajes
        self.m3 = m3
        self.material = material
        self.m3_km = m3_km
        self.precio = precio
        self.monto = monto

    
    def Inserta_datos():
        # Title
        st.title("")


        # Form for inputting costs
        with st.form("cost_form"):
            st.subheader("")
    
            # Input fields
            fecha             = st.text_input("Fecha           : ")
            boleta            = st.text_input("Boleta          : ")
            contratista       = st.text_input("Codigo Empresa  : ")      
            maquina           = st.text_input("Maquina  : ")
            capacidad         = st.number_input("Capacidad maquina : ", min_value=0.0, value=0.0, step=1.0)
            lugar_salida      = st.text_input("Lugar de salida    : ")
            lugar_llegada     = st.text_input("Lugar de llegada    : ")
            distancia         = st.number_input("Distancia : ", min_value=0.0, value=0.0, step=1.0)
            viajes            = st.number_input("No. de viajes : ", min_value=0.0, value=0.0, step=1.0)
            m3                = capacidad * viajes
            material          = st.text_input("Material    : ")
            m3_km             = distancia * viajes * m3
            precio            = st.number_input("Precio unitario : ", min_value=0.0, value=0.0, step=1.0)
            monto             = m3_km * precio

            # For submit button
            submitted = st.form_submit_button("Ingresa datos")

        # Display the result if the form is submitted
        if submitted:
            conn = sqlite3.connect("Acarreo_Proyectos.db")
            c = conn.cursor()
    
            c.execute("""INSERT INTO datos_acarreo (fecha, boleta, contratista, maquina, capacidad, lugar_salida, lugar_llegada, distancia, viajes, m3, material, m3_km, precio, monto) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(fecha, boleta, contratista, maquina, capacidad, lugar_salida, lugar_llegada, distancia, viajes, m3, material, m3_km, precio, monto))

            conn.commit()
            conn.close()

            total_cost = monto
            st.success(f"El monto  de este acarreo es  : Ȼ{total_cost:,.2f}")
        else:
            st.info("")
        return()