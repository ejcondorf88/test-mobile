# Clasificador de Prioridades

Sistema de clasificación de prioridades usando IA para analizar situaciones y determinar su nivel de urgencia.

## 🚀 Características

- Clasificación automática de situaciones en tres niveles: urgente, moderado, normal
- API REST con FastAPI
- Frontend en React con Vite
- Interfaz intuitiva y responsive
- Logs detallados en consola

## 🛠️ Tecnologías

### Backend
- Python 3.8+
- FastAPI
- HuggingFace Transformers
- Uvicorn

### Frontend
- React
- Vite
- Axios
- CSS Moderno

## 📋 Prerrequisitos

- Python 3.8 o superior
- Node.js 14 o superior
- npm o yarn

## 🔧 Instalación

### Backend

1. Crear y activar entorno virtual:
```bash
cd backend
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Unix o MacOS:
source venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene las siguientes dependencias:
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.4.2
transformers==4.35.2
torch==2.1.1
python-dotenv==1.0.0
langchain==0.0.350
langchain-community==0.0.10
langchain-huggingface==0.0.1
huggingface-hub==0.19.4
```

3. Iniciar el servidor:
```bash
python main.py
```

El servidor estará disponible en `http://localhost:8000`

### Frontend

1. Instalar dependencias:
```bash
cd fronted
npm install
```

2. Iniciar el servidor de desarrollo:
```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

## 📝 Uso

1. Abre la aplicación en tu navegador
2. Escribe una situación en el campo de texto
3. Haz clic en "Enviar al Backend"
4. Verás la clasificación de prioridad con su respectivo color:
   - 🔴 Rojo: Urgente
   - 🟡 Amarillo: Moderado
   - 🟢 Verde: Normal

## 📚 API Endpoints

- `GET /`: Información del API
- `POST /generate/`: Clasificar prioridad
- `GET /health`: Estado del servicio

### Ejemplo de petición POST /generate/

```json
{
    "prompt": "El servidor principal está caído y no responde"
}
```

### Ejemplo de respuesta

```json
{
    "prompt": "El servidor principal está caído y no responde",
    "classification": "urgente",
    "success": true
}
```

## 🤝 Contribuir

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## ✨ Agradecimientos

- [HuggingFace](https://huggingface.co/) por los modelos de IA
- [FastAPI](https://fastapi.tiangolo.com/) por el framework del backend
- [React](https://reactjs.org/) por el framework del frontend 