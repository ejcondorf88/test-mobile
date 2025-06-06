from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from clasificador import classify_priority

app = FastAPI(title="Priority Classifier API", version="1.0.0")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Modelo del body
class PromptRequest(BaseModel):
    prompt: str

class ClassificationResponse(BaseModel):
    prompt: str
    classification: str
    success: bool

@app.get("/")
async def root():
    return {
        "message": "Priority Classifier API", 
        "status": "running",
        "endpoints": {
            "classify": "/generate/",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "classification_api"}

# Endpoint para clasificar prioridad
@app.post("/generate/", response_model=ClassificationResponse)
async def generate_text(request: PromptRequest):
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="El prompt no puede estar vacío")
        
        # Llamamos a la función de clasificación
        classification = classify_priority(request.prompt)
        
        return ClassificationResponse(
            prompt=request.prompt,
            classification=classification,
            success=True
        )
    
    except Exception as e:
        print(f"Error en el endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error al procesar la clasificación: {str(e)}"
        )

if __name__ == "__main__":
    print("🚀 Iniciando servidor de clasificación de prioridades...")
    print("📝 Endpoints disponibles:")
    print("   GET  / - Información del API")
    print("   POST /generate/ - Clasificar prioridad")
    print("   GET  /health - Estado del servicio")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)