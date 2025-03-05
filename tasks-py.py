"""
CrewAI tasks for CV analysis.
"""

import logging
from crewai import Task

def create_analysis_task(analyst, pdf_tool):
    """
    Create the CV analysis task.
    
    Args:
        analyst: The analyst agent
        pdf_tool: The PDF tool for document analysis
        
    Returns:
        The analysis task
    """
    try:
        analysis_task = Task(
            description=(
                """Evaluar si el perfil del candidato cumple con los requisitos mínimos detallados en la descripción del trabajo {descripcion}, basándose en la información proporcionada en su hoja de vida. Realizar un análisis exhaustivo de cada criterio especificado en la descripción y compararlo con la experiencia, habilidades y formación presentes en el CV. Debes usar la tool de búsqueda de texto para analizar el contenido de la hoja de vida y proporcionar el análisis solamente en español. Si el contenido de la hoja de vida o los requisitos del perfil están en otro idioma diferente al español, delega al agente traductor para traducirlos antes de proceder con el análisis."""),
            expected_output=(
                """Un análisis detallado solamente en español indicando, para cada requisito, si el candidato cumple o no con el criterio específico, junto con una breve justificación de cada caso. El resultado debe resaltar claramente las áreas en las que el candidato cumple los requisitos, así como las áreas donde no los cumple, en base a la comparación de los requisitos del perfil: {descripcion} y la hoja de vida. Debes usar la tool de búsqueda de texto para analizar el contenido de la hoja de vida. Si el contenido de la hoja de vida o los requisitos del perfil están en otro idioma diferente al español, delega al agente traductor para traducirlos antes de proceder con el análisis."""),
            agent=analyst,
            tools=[pdf_tool],
        )
        logging.info("Created analysis task")
        return analysis_task
    except Exception as e:
        logging.error(f"Error creating analysis task: {e}")
        raise

def create_translator_task(translator, analysis_task):
    """
    Create the translator task.
    
    Args:
        translator: The translator agent
        analysis_task: The analysis task for context
        
    Returns:
        The translator task
    """
    try:
        translator_task = Task(
            description=(
                """Traduce el contenido proporcionado al idioma español. Si el texto ya está en español, devuelve el mismo texto sin cambios."""
            ),
            expected_output=(
                """El texto traducido al español manteniendo el significado del contenido original. Si el texto ya está en español, devuelve el mismo texto."""
            ),
            agent=translator,
            context=[analysis_task]
        )
        logging.info("Created translator task")
        return translator_task
    except Exception as e:
        logging.error(f"Error creating translator task: {e}")
        raise

def create_evaluation_task(evaluator, analysis_task):
    """
    Create the evaluation task.
    
    Args:
        evaluator: The evaluator agent
        analysis_task: The analysis task for context
        
    Returns:
        The evaluation task
    """
    try:
        evaluation_task = Task(
            description=(
                """Determinar si el candidato cumple en términos generales con los requisitos mínimos establecidos en la descripción del puesto en relación con su joha de vida, utilizando únicamente el análisis ya obtenido en la tarea de "analysis task". No es necesario realizar un análisis detallado de cada criterio; solo verifica si el perfil del candidato se ajusta de manera general a los requisitos del puesto. La respuesta debe ser "Cumple" o "No cumple" seguido de una justificación clara y concisa de tu decisión en español."""),
            expected_output=(
                """Una evaluación en español indicando únicamente si el candidato cumple o no con los requisitos mínimos del puesto en relación con su hoja de vida, basado en el análisis ya obtenido. La respuesta debe ser "Cumple" o "No cumple" seguido de una justificación clara y concisa de tu decisión. No es necesario realizar un análisis detallado de cada criterio; solo verifica si el perfil del candidato se ajusta de manera general a los requisitos del puesto."""),
            agent=evaluator,
            context=[analysis_task]
        )
        logging.info("Created evaluation task")
        return evaluation_task
    except Exception as e:
        logging.error(f"Error creating evaluation task: {e}")
        raise
