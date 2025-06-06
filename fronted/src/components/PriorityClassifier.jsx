import { useState } from 'react';
import axios from 'axios';

const PriorityClassifier = () => {
    const [prompt, setPrompt] = useState('');
    const [classification, setClassification] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [responseData, setResponseData] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log('🚀 Iniciando envío al backend...');
        console.log('📝 Prompt a enviar:', prompt);
        
        setLoading(true);
        setError(null);
        setResponseData(null);
        
        try {
            console.log('📡 Enviando petición a http://localhost:8000/generate/');
            const response = await axios.post('http://localhost:8000/generate/', {
                prompt: prompt
            });
            
            console.log('✅ Respuesta recibida:', response.data);
            setClassification(response.data.classification);
            setResponseData(response.data);
        } catch (err) {
            console.error('❌ Error en la petición:', err);
            setError(err.response?.data?.detail || 'Error al clasificar la prioridad');
        } finally {
            setLoading(false);
            console.log('🏁 Proceso completado');
        }
    };

    const getPriorityColor = (priority) => {
        switch(priority) {
            case 'urgente':
                return '#dc3545';
            case 'moderado':
                return '#ffc107';
            case 'normal':
                return '#28a745';
            default:
                return '#6c757d';
        }
    };

    return (
        <div className="priority-classifier">
            <h2>Clasificador de Prioridades</h2>
            
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="prompt">Describe la situación:</label>
                    <textarea
                        id="prompt"
                        value={prompt}
                        onChange={(e) => {
                            console.log('📝 Texto actualizado:', e.target.value);
                            setPrompt(e.target.value);
                        }}
                        placeholder="Ejemplo: El servidor principal está caído y no responde"
                        rows="4"
                        required
                    />
                </div>
                
                <button 
                    type="submit" 
                    disabled={loading}
                    className="send-button"
                >
                    {loading ? 'Enviando...' : 'Enviar al Backend'}
                </button>
            </form>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {responseData && (
                <div className="classification-result" style={{ borderColor: getPriorityColor(classification) }}>
                    <h3>Resultado de la Clasificación</h3>
                    <div className="result-details">
                        <p><strong>Situación:</strong> {responseData.prompt}</p>
                        <p className={`priority-${classification}`}>
                            <strong>Clasificación:</strong> {classification.toUpperCase()}
                        </p>
                        <p><strong>Estado:</strong> {responseData.success ? '✅ Exitoso' : '❌ Error'}</p>
                    </div>
                </div>
            )}

            <style jsx>{`
                .priority-classifier {
                    max-width: 600px;
                    margin: 2rem auto;
                    padding: 1rem;
                }

                .form-group {
                    margin-bottom: 1rem;
                }

                label {
                    display: block;
                    margin-bottom: 0.5rem;
                    font-weight: bold;
                }

                textarea {
                    width: 100%;
                    padding: 0.5rem;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-size: 1rem;
                }

                .button-group {
                    display: flex;
                    justify-content: center;
                    margin-top: 1rem;
                }

                .send-button {
                    background-color: #007bff;
                    color: white;
                    padding: 0.75rem 1.5rem;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 1rem;
                    font-weight: bold;
                    transition: all 0.3s ease;
                }

                .send-button:hover {
                    background-color: #0056b3;
                    transform: translateY(-2px);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }

                .send-button:disabled {
                    background-color: #ccc;
                    transform: none;
                    box-shadow: none;
                }

                .error-message {
                    color: #dc3545;
                    margin-top: 1rem;
                    padding: 0.5rem;
                    border: 1px solid #dc3545;
                    border-radius: 4px;
                }

                .classification-result {
                    margin-top: 1rem;
                    padding: 1rem;
                    border-radius: 4px;
                    background-color: #f8f9fa;
                }

                .priority-urgente {
                    color: #dc3545;
                    font-weight: bold;
                }

                .priority-moderado {
                    color: #ffc107;
                    font-weight: bold;
                }

                .priority-normal {
                    color: #28a745;
                    font-weight: bold;
                }
            `}</style>
        </div>
    );
};

export default PriorityClassifier; 