#!/usr/bin/env python3
"""
Main application entry point for CV Analyzer.
This script initializes and runs the Streamlit application.
"""

import logging
import streamlit as st
import time
import os

from config import setup_logging, DOCS_FOLDER
from utils import setup_folders, delete_docs, get_pdf_previews
from ui import setup_ui
from agents import create_crew

def main():
    """Main application flow"""
    try:
        # Setup application
        setup_logging()
        setup_folders()
        setup_ui()
        
        # Initialize session state
        if "valid_docs" not in st.session_state:
            st.session_state.valid_docs = [False, False, False]
        
        # Create input fields
        uploaded_file = st.file_uploader("Carga aquí la hoja de vida del candidato", type=["pdf"])
        
        st.write("**Ingresa un texto con los requisitos específicos del perfil para la vacante**")
        descripcion_input = st.text_area(
            "Requisitos del Perfil",
            placeholder="Ejemplo: Programación en Python y R, SQL avanzado, experiencia en Machine Learning con Scikit-Learn y TensorFlow, etc.",
            height=300,
            max_chars=10000
        )
        
        # Process inputs if available
        if uploaded_file and descripcion_input:
            logging.info(f"Document uploaded: {uploaded_file.name}")
            
            # Save the file
            cv_path = os.path.join(DOCS_FOLDER, uploaded_file.name)
            with open(cv_path, "wb") as f:
                f.write(uploaded_file.read())
            
            # Display PDF preview
            st.write("**Vista Previa de la Hoja de Vida del Candidato**")
            images = get_pdf_previews(cv_path, scale=2.0)
            for i, img in enumerate(images):
                st.image(img, caption=f"Página {i+1}", use_column_width=True)
            
            # Analyze CV when button is clicked
            if st.button("Analizar Hoja de Vida"):
                with st.spinner('Procesando Hoja de Vida... Espera un momento por favor.'):
                    logging.info("Processing resume...")
                    
                    # Set up inputs for the crew
                    job_application_inputs = {'descripcion': descripcion_input}
                    
                    # Create and run the crew
                    crew, analysis_task, evaluation_task = create_crew(cv_path)
                    
                    # Track processing time
                    start_time = time.time()
                    crew.kickoff(inputs=job_application_inputs)
                    end_time = time.time()
                    
                    # Display results
                    st.success(f"**Análisis de la Hoja de Vida**:\n\n{analysis_task.output}")
                    st.success(f"**Conclusión Final**:\n\n{evaluation_task.output}")
                    st.write(f"**Tiempo de Procesamiento:** {round(end_time - start_time, 2)} segundos")
                    
                    # Cleanup
                    delete_docs(DOCS_FOLDER)
                    
        # Handle missing inputs
        elif uploaded_file and not descripcion_input:
            st.error("Por favor, ingresa los requisitos del perfil en la caja de texto y presione Ctrl + Enter cuando esté listo.")
            logging.error("Description input is missing.")
            delete_docs(DOCS_FOLDER)
            
        elif descripcion_input and not uploaded_file:
            st.error("Por favor, carga la hoja de vida del candidato en formato PDF teniendo en cuenta los requisitos de tipo y tamaño permitido.")
            logging.error("Document upload is missing.")
            delete_docs(DOCS_FOLDER)
            
        else:
            st.info("Por favor, carga la hoja de vida del candidato y completa los requisitos del perfil para comenzar el análisis.")
            logging.info("Document and description inputs are missing.")
            delete_docs(DOCS_FOLDER)
            
    except Exception as e:
        st.error(f"An error has occurred: {e}")
        logging.error(f"An error has occurred: {e}")
        delete_docs(DOCS_FOLDER)

# Entry point
if __name__ == "__main__":
    main()
