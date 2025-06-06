import logging
from typing import Optional
from transformers import pipeline
import torch

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_local_classifier():
    """Crear y devolver un pipeline de clasificación zero-shot local."""
    try:
        model_id = "facebook/bart-large-mnli"
        logger.info(f"Cargando modelo local: {model_id}")
        classifier = pipeline(
            "zero-shot-classification",
            model=model_id,
            device=0 if torch.cuda.is_available() else -1
        )
        test_result = classifier("Test: hola", candidate_labels=["urgente", "moderado", "normal"])
        logger.info(f"Prueba del modelo {model_id} exitosa: {test_result}")
        return classifier
    except Exception as e:
        logger.error(f"Error al cargar el modelo local: {str(e)}")
        return None

# Inicializar el clasificador globalmente
classifier = create_local_classifier()

def classify_priority(prompt: str) -> str:
    """
    Clasificar la prioridad de una situación usando clasificación zero-shot local.
    
    Args:
        prompt (str): La situación a clasificar
        
    Returns:
        str: La clasificación (urgente, moderado, normal)
    """
    if not prompt or not prompt.strip():
        return "normal"  # Cambiado para devolver "normal" en lugar de error
    
    if classifier is None:
        logger.info("Clasificador no disponible, usando respaldo")
        return classify_priority_fallback(prompt)
    
    try:
        labels = ["urgente", "moderado", "normal"]
        logger.info(f"Clasificando: {prompt[:50]}...")
        result = classifier(prompt.strip(), candidate_labels=labels)
        logger.info(f"Respuesta cruda: {result}")
        max_score_index = result["scores"].index(max(result["scores"]))
        return result["labels"][max_score_index]
    except Exception as e:
        logger.error(f"Error en classify_priority: {str(e)}")
        return classify_priority_fallback(prompt)

def classify_priority_fallback(prompt: str) -> str:
    """
    Clasificación de respaldo usando coincidencia de palabras clave.
    
    Args:
        prompt (str): La situación a clasificar
        
    Returns:
        str: La clasificación
    """
    if not prompt:
        return "normal"
    
    prompt_lower = prompt.lower()
    
    # Palabras clave para urgencias (agregado "incendiando")
    urgent_keywords = [
        "incendio", "incendiando", "fuego", "fire", "emergencia", "emergency",
        "accidente", "accident", "sangre", "blood", 
        "pecho", "respirar", "breathe", "auxilio",
        "help", "urgente", "urgent", "crítico", "critical",
        "peligro", "danger", "muerte", "death", "hospital",
        "quemando", "burning", "humo", "smoke"
    ]
    
    # Palabras clave para prioridades moderadas
    moderate_keywords = [
        "médico", "doctor", "cita", "appointment",
        "importante", "important", "pronto", "soon", 
        "trabajo", "work", "reunión", "meeting",
        "semana", "week", "mañana", "tomorrow"
    ]
    
    # Palabras clave para prioridades normales
    normal_keywords = [
        "compra", "shopping", "película", "movie",
        "ver", "watch", "quiero", "want", "gustaría", "would like"
    ]
    
    if any(keyword in prompt_lower for keyword in urgent_keywords):
        return "urgente"
    if any(keyword in prompt_lower for keyword in normal_keywords):
        return "normal"
    if any(keyword in prompt_lower for keyword in moderate_keywords):
        return "moderado"
    if "necesito" in prompt_lower:
        return "moderado"
    return "normal"

def test_classification():
    """Probar el sistema de clasificación con varios ejemplos."""
    test_cases = [
        ("Mi casa se está incendiando", "urgente"),
        ("Tengo dolor en el pecho y no puedo respirar", "urgente"),
        ("Necesito ir al médico esta semana", "moderado"),
        ("Tengo una reunión importante mañana", "moderado"),
        ("Necesito hacer la compra", "normal"),
        ("Quiero ver una película", "normal"),
        ("", "normal"),
    ]
    
    print("🧪 Probando el Sistema de Clasificación de Prioridades")
    print("=" * 60)
    
    for prompt, expected in test_cases:
        result = classify_priority(prompt)
        status = "✅" if result == expected else "❌"
        print(f"{status} Prompt: '{prompt}'")
        print(f"   Esperado: {expected} | Obtenido: {result}")
        print("-" * 60)
if __name__ == "__main__":
    test_classification()