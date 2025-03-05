"""
CrewAI agents and crew configuration for CV analysis.
"""

import logging
from typing import Tuple

from langchain_openai import ChatOpenAI
from crewai_tools import PDFSearchTool
from crewai import Agent, Crew, Process

from config import OPENAI_API_KEY, OPENAI_MODEL_NAME
from tasks import create_analysis_task, create_translator_task, create_evaluation_task

def create_agents(pdf_tool) -> Tuple[Agent, Agent, Agent]:
    """
    Create and configure the CrewAI agents.
    
    Args:
        pdf_tool: PDFSearchTool instance for document analysis
        
    Returns:
        Tuple of analyst, translator, and evaluator agents
    """
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model_name=OPENAI_MODEL_NAME, 
            temperature=0.7, 
            api_key=OPENAI_API_KEY
        )
        
        # Create Analyst Agent
        analyst = Agent(
            role="Analista de CV",
            goal="""Identificar candidatos con perfiles que se ajusten óptimamente a los requisitos detallados para el puesto {descripcion}, evaluando cada elemento de la hoja de vida proporcionada para determinar si cumple o no con los criterios específicos. Debes usar la tool de búsqueda de texto (pdf_tool) para analizar el contenido de la hoja de vida. Si el contenido de la hoja de vida o los requisitos del perfil están en otro idioma diferente al español, delega al agente traductor para traducirlos antes de proceder con el análisis. """,
            tools=[pdf_tool],
            verbose=True,
            backstory=(
                """Eres un agente especializado en la selección de candidatos con perfiles técnicos. Tu objetivo es analizar en profundidad las habilidades, experiencia y formación presentadas en la hoja de vida y compararlas con los requisitos específicos de la posición {descripcion}. Antes de iniciar el análisis, verifica si la hoja de vida y los requisitos están en español. Si no, delega la tarea al agente traductor para convertir el contenido al español. Debes identificar coincidencias y brechas de manera precisa, resaltando de forma explícita y detallada las áreas donde el candidato cumple o no cumple con las expectativas. Debes usar la tool de búsqueda de texto para analizar el contenido de la hoja de vida."""),
            llm=llm,
            max_iter=30,
            allow_delegation=True,
        )
        
        # Create Translator Agent
        translator = Agent(
            role="Traductor",
            goal="""Traducir cualquier texto de entrada proporcionado al idioma español. La traducción debe ser precisa y mantener el significado del contenido original. Si el texto ya está en español, simplemente devuelve el mismo texto.""",
            backstory=(
            """Eres un agente experto en traducción de idiomas. Tu objetivo es tomar cualquier texto proporcionado en cualquier idioma y traducirlo con precisión al español, asegurándote de mantener el contexto, significado y tono original. Si el texto ya está en español, simplemente devuélvelo sin modificaciones. Eres confiable, eficiente y tienes un conocimiento profundo de diferentes idiomas y matices culturales, lo que te permite realizar traducciones precisas y naturales."""),
            verbose=True,
            llm=llm,
            max_iter=10,
            allow_delegation=False,
        )
        
        # Create Evaluator Agent
        evaluator = Agent(
            role="Evaluador de selección",
            goal="""Determinar si el candidato cumple o no con los requisitos básicos del puesto a partir del análisis realizado de su hoja de vida y los requisitos del perfil. Tu respuesta debe ser "Cumple" o "No cumple" seguido de una justificación clara y concisa de tu decisión. No es necesario realizar un análisis detallado de cada criterio; solo verifica si el perfil del candidato se ajusta de manera general a los requisitos del puesto.""",
            verbose=False,
            backstory=(
                """Eres un agente de selección cuyo único objetivo es verificar si el candidato tiene los requisitos generales para el puesto a partir del análisis obtenido de su hoja de vida y los requisitos del perfil. Debes determinar únicamente si cumple o no cumple como candidato para el perfil solicitado y proporcionar una justificación clara y concisa de tu decisión. No es necesario realizar un análisis detallado de cada criterio; solo verifica si el perfil del candidato se ajusta de manera general a los requisitos del puesto."""),
            llm=llm,
            max_iter=10,
            allow_delegation=False,
        )
        
        logging.info("Created agents successfully")
        return analyst, translator, evaluator
    
    except Exception as e:
        logging.error(f"Error creating agents: {e}")
        raise

def create_crew(cv_path: str) -> Tuple[Crew, any, any]:
    """
    Create a CrewAI crew with agents for CV analysis.
    
    Args:
        cv_path: Path to the CV PDF file
        
    Returns:
        Tuple containing the crew, analysis task, and evaluation task
    """
    try:
        # Initialize PDF tool
        pdf_tool = PDFSearchTool(pdf=cv_path)
        
        # Create agents
        analyst, translator, evaluator = create_agents(pdf_tool)
        
        # Create tasks
        analysis_task = create_analysis_task(analyst, pdf_tool)
        translator_task = create_translator_task(translator, analysis_task)
        evaluation_task = create_evaluation_task(evaluator, analysis_task)
        
        # Create crew
        crew = Crew(
            agents=[analyst, translator, evaluator],
            tasks=[analysis_task, translator_task, evaluation_task],
            process=Process.sequential,
            memory=False,
            verbose=True,
        )
        
        logging.info("Created crew successfully")
        return crew, analysis_task, evaluation_task
    
    except Exception as e:
        logging.error(f"Error creating crew: {e}")
        raise
