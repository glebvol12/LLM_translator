from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from together import Together
import os
from dotenv import load_dotenv  # Добавьте этот импорт
from fastapi.middleware.cors import CORSMiddleware

# Загружаем переменные окружения из .env
load_dotenv()  





app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    try:
        # Проверяем API ключ
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
        
        # Если языки совпадают, возвращаем исходный текст
        if request.source_language.lower() == request.target_language.lower():
            return {"translated_text": request.text, "model_used": "none (same language)"}
        
        # Создаем клиент Together
        client = Together(api_key=api_key)
        
        # Формируем промпт
        prompt = f"""
        Translate the following text from {request.source_language} to {request.target_language}.
        Return ONLY the translated text without ANY additional text, explanations or comments.

### Rules:
- No introductory phrases
- No explanations
- No notes
- No thinking process
- Just the pure translation
- Keep all punctuation

### Text to translate:
{request.text}
        """
        
        # Отправляем запрос
        response = client.chat.completions.create(
            model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
            messages=[{"role": "user", "content": prompt}]
        )
        
        translated_text = response.choices[0].message.content
        
        return {"translated_text": translated_text, "model_used": "Llama-3-70b"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

