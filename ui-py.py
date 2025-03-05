"""
UI components for the CV Analyzer Streamlit application.
"""

import base64
import streamlit as st
import logging

from config import LOGO_PATH

def setup_ui():
    """Configure the Streamlit UI components"""
    try:
        # Load and encode logo
        with open(LOGO_PATH, "rb") as file:
            logo_base64 = base64.b64encode(file.read()).decode()
        
        # Set up page title and logo
        st.title('Análisis y Validación de Hojas de Vida para Selección de Candidatos')
        
        # Add logo to bottom right
        st.markdown(
            f"""
            <style>
                .logo {{
                    position: fixed;
                    bottom: 10px;
                    right: 10px;
                    width: 80px;
                    z-index: 100;
                }}
            </style>
            <img class="logo" src="data:image/png;base64,{logo_base64}"/>
            """,
            unsafe_allow_html=True
        )
        
        # Instructions
        st.write("""
            **Instrucciones**
            1. Carga el archivo de la hoja de vida del candidato en formato PDF en el área designada. Asegúrate de que el archivo cumpla con los requisitos de tipo y tamaño permitido.
            2. Ingresa en la caja de texto los requisitos específicos del perfil que se está buscando para la vacante. Esto permitirá al agente realizar una comparación precisa entre los requisitos y la experiencia del candidato.
            3. Una vez cargado el documento, se desplegará una vista previa de la hoja de vida. Presiona el botón debajo de la vista previa para iniciar el análisis. El sistema procesará la información de cada página de la hoja de vida y la comparará con los requisitos del perfil especificado.\n\n
            **Nota:**\n\n
            - Si el proceso es exitoso, el sistema generará un resumen con un análisis detallado sobre la adecuación del candidato al perfil buscado y una decisión final sobre si el candidato cumple o no con los requisitos.
            - Si el proceso no es exitoso, se mostrará un mensaje de error indicando la razón. En ese caso, por favor, revisa los datos ingresados y vuelve a intentarlo."""
        )
        
        logging.info("UI setup completed successfully")
    except Exception as e:
        logging.error(f"Error setting up UI: {e}")
        st.error("Error loading application interface. Please try again later.")
