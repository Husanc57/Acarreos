import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from Insertar import InsertaDatos
from Acarreos_pdf import Imprime_Pdf
from Acarreos_pdf_uno import Imprime_Pdf_Uno
from Acarreos_pdf_fecha import Imprime_Pdf_Fecha
from Acarreos_pdf_empresa import Imprime_Pdf_Empresa
from Acarreos_pdf_material import Imprime_Pdf_Material
from Acarreos_pdf_modifica import Imprime_Pdf_Modifica
from Acarreos_pdf_cia_fecha import Imprime_Pdf_Cia_Fecha
from Acarreos_pdf_cia_material import Imprime_Pdf_Cia_Material
from Acarreos_pdf_material_fecha import Imprime_Pdf_Material_Fecha
import os

with st.sidebar:
    st.image(os.path.join(os.getcwd(), "Logo12.jpg" ))
    selected = option_menu("ACARREO DE AGREGADOS", ["Inicio", "Agregar Datos", 'Consultar Datos I', 'Consultar Datos II', 'Modificar Datos', 'Borrar Datos'])

if selected == "Inicio":
    pass

elif selected == "Agregar Datos":

    selected6 = option_menu(None, ["Agrega un registro a la base"], 
    #icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    
    #with st.form("cost_form"):

    # Title
    #st.title("")


    # Form for inputting costs
    with st.form("cost_form"):
        st.subheader("Inserte los datos")
    
        # Input fields
        fecha             = st.text_input("Fecha           : ")
        boleta            = st.text_input("Boleta          : ")
        contratista       = st.text_input("Codigo Empresa  : ")      
        maquina           = st.text_input("Maquina  : ")
        capacidad         = st.number_input("Capacidad maquina : ", min_value=0.00, value=0.00, format = "%.2f")
        lugar_salida      = st.text_input("Lugar de salida    : ")
        lugar_llegada     = st.text_input("Lugar de llegada    : ")
        distancia         = st.number_input("Distancia : ", min_value=0.0, value=0.0, format = "%.2f")
        viajes            = st.number_input("No. de viajes : ", min_value=0.0, value=0.0, format = "%.2f")
        m3                = round((capacidad * viajes), 2)
        material          = st.text_input("Material    : ")
        m3_km             = round((distancia * viajes * m3), 2)
        precio            = st.number_input("Precio unitario : ", min_value=0.0, value=0.0, format = "%.2f")
        monto             = round((m3_km * precio), 2)

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
        st.info("Complete el formulario y haga clic en el botón para ingresar datos")



elif selected == "Consultar Datos I":
    # 2. horizontal menu
    selected2 = option_menu(None, ["Todo", "Boleta", "Fecha", "Cia", "Material"], 
    #icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    selected2
    if "pv" not in st.session_state:
        st.session_state.pv = True

    if selected2 == "Todo":
        if st.session_state.pv == True:

            st.session_state.pv = False
        else:
            st.subheader("Consulta General")
            Imprime_Pdf.main_pdf() 

    elif selected2 == "Boleta":

        #with st.form("cost_form"):

        # Input fields
        boleta1 = st.text_input("Digite la boleta  : ")      
        #For submit button
        #submitted = st.form_submit_button("Consulta datos")
        print(boleta1)

        if boleta1:
            Imprime_Pdf_Uno.main_pdf_uno(boleta1)

                          
    elif selected2 == "Fecha": 

        #with st.form("cost_form"):

        # Input fields
        fecha1 = st.text_input("Digite la fecha  : ")      
        #For submit button
        #submitted = st.form_submit_button("Consulta fecha")

        if fecha1:
            Imprime_Pdf_Fecha.main_pdf_fecha(fecha1)


    elif selected2 == "Cia": 

        #with st.form("cost_form"):

        # Input fields
        empresa1 = st.text_input("Digite la empresa  : ")      
        #For submit button
        #submitted = st.form_submit_button("Consulta empresa")

        if empresa1:
            Imprime_Pdf_Empresa.main_pdf_empresa(empresa1)

    elif selected2 == "Material":

        #with st.form("cost_form"):

        # Input fields
        material1 = st.text_input("Digite el material  : ")      
        #For submit button
        #submitted = st.form_submit_button("Consulta empresa")

        if material1:
            Imprime_Pdf_Material.main_pdf_material(material1)    

    else:
        pass   


elif selected == "Consultar Datos II":
    # 2. horizontal menu
    selected2 = option_menu(None, ["Consultas II", "Cia/Fecha", "Cia/Material", "Material/Fecha"], 
    #icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    selected2
    if "pv" not in st.session_state:
        st.session_state.pv = True

    if selected2 == "Consultas II":
                   pass 

    elif selected2 == "Cia/Fecha":

        #with st.form("cost_form"):

        # Input fields
        contratista1 = st.text_input("Digite la compañia  : ")
        fecha1       = st.text_input("Digite la fecha     : ")      
        #For submit button
        #submitted = st.form_submit_button("Consulta datos")
        
        if contratista1 and fecha1:
            Imprime_Pdf_Cia_Fecha.main_pdf_cia_fecha(contratista1, fecha1)

                          
    elif selected2 == "Cia/Material": 

        #with st.form("cost_form"):

        # Input fields
        contratista1 = st.text_input("Digite la compañia  : ")
        material1    = st.text_input("Digite el material  : ")      
        #For submit button
        #submitted = st.form_submit_button("Consulta fecha")

        if contratista1 and material1:
            Imprime_Pdf_Cia_Material.main_pdf_cia_material(contratista1, material1)


    elif selected2 == "Material/Fecha": 

       #with st.form("cost_form"):

        # Input fields
        material1    = st.text_input("Digite el material  : ")      
        fecha1       = st.text_input("Digite la fecha     : ")
        #For submit button
        #submitted = st.form_submit_button("Consulta fecha")

        if material1 and fecha1:
            Imprime_Pdf_Material_Fecha.main_pdf_material_fecha(material1, fecha1)
     

    else:
        pass   

elif selected == "Modificar Datos":

    selected5 = option_menu(None, ["Modifica un registro"], 
    #icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    selected5
    #with st.form("cost_form"):

    # Input fields
    boleta1 = st.text_input("Digite la boleta  : ")      
    #For submit button
    #submitted = st.form_submit_button("Consulta datos")
    
    if boleta1:
        #Imprime_Pdf_Modifica.main_pdf_modifica(boleta1)
        
        conn = sqlite3.Connection("Acarreo_Proyectos.db")
        c = conn.cursor()

        resultado = c.execute(f"SELECT * FROM datos_acarreo WHERE boleta = '{boleta1}'")

        st.data_editor(resultado)

        pasar = st.text_input("Desea modificar el registro ?  : ")

        if pasar == "si":
            resultado1 = resultado

            st.dataframe(resultado1)
 
        else:

            print("No entra a resultado")

        


elif selected == "Borrar Datos":
    
    # 4. horizontal menu
    selected4 = option_menu(None, ["Borra un registro"], 
    #icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    selected4
    
    if selected4 == "Borra un registro":

        with st.form("costo_forma"):
            st.subheader("Borra datos")
    
            # Input fields
            boleta1 = st.text_input("Digite la boleta  : ")      
        
            conn = sqlite3.connect("Acarreo_Proyectos.db")
            c = conn.cursor()
 
            # For submit button
            submitted = st.form_submit_button("Borra datos")

            # Display the result if the form is submitted
            if submitted:
  
                c.execute(f"DELETE FROM datos_acarreo WHERE boleta = '{boleta1}';")
                #c.execute(f"DELETE FROM datos_acarreo WHERE boleta = {boleta}") 
                st.success("El registro fue borrado satisfactoriamente")

            else:

                st.info("Complete el formulario y haga clic en el botón para borrar el registro solicitado")
        
            conn.commit()
            conn.close()
      
    
else:
    st.write("No hay nada que borrar")