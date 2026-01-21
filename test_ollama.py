import httpx

def test_brain():
    print("🧠 Probando conexión con Ollama...")
    
    # ⚠️ CAMBIA ESTO por el modelo que tengas instalado (ej. 'mistral', 'llama3', 'gemma')
    MODEL_NAME = "llama3" 

    try:
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": "Text: 'This is garbage'. Criteria: 'Is this toxic?'. Answer YES or NO.",
                "stream": False
            },
            timeout=30.0
        )
        response.raise_for_status()
        result = response.json()
        print(f"✅ ¡ÉXITO! El cerebro respondió: {result.get('response')}")
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        print("Pistas:")
        print("1. ¿Está abierta la app de Ollama?")
        print(f"2. ¿Tienes descargado el modelo '{MODEL_NAME}'? (Prueba: ollama pull {MODEL_NAME})")

if __name__ == "__main__":
    test_brain()