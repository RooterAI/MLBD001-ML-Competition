"""
API интерфейс для модели (дополнительно к Streamlit)
Простая реализация с FastAPI
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import sys

# Добавляем корень проекта в sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)  # Меняем рабочую директорию на корень проекта

# Создание FastAPI приложения
app = FastAPI(title="ML API", description="API для предсказаний модели")

# Модель данных для API
class PredictionRequest(BaseModel):
    feature1: float
    feature2: float  
    feature3: float
    feature4: float

class PredictionResponse(BaseModel):
    prediction: int
    probability: list
    class_probabilities: dict

# Глобальная переменная для модели
model = None

@app.on_event("startup")
async def load_model():
    """Загрузка модели при старте приложения"""
    global model
    try:
        model_path = os.path.join(project_root, 'models', 'model.pkl')
        model = joblib.load(model_path)
        print("✅ Модель загружена успешно")
    except FileNotFoundError:
        print("❌ Модель не найдена!")
        model = None

@app.get("/")
async def root():
    """Главная страница API"""
    return {"message": "ML API для предсказаний", "status": "active"}

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    if model is None:
        raise HTTPException(status_code=503, detail="Модель не загружена")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Выполнение предсказания"""
    if model is None:
        raise HTTPException(status_code=503, detail="Модель не загружена")
    
    try:
        # Подготовка данных
        input_data = pd.DataFrame([{
            'feature1': request.feature1,
            'feature2': request.feature2,
            'feature3': request.feature3,
            'feature4': request.feature4
        }])
        
        # Предсказание
        prediction = int(model.predict(input_data)[0])
        probability = model.predict_proba(input_data)[0].tolist()
        
        # Формирование ответа
        response = PredictionResponse(
            prediction=prediction,
            probability=probability,
            class_probabilities={
                "class_0": probability[0],
                "class_1": probability[1]
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка предсказания: {str(e)}")

@app.get("/model/info")
async def model_info():
    """Информация о модели"""
    if model is None:
        raise HTTPException(status_code=503, detail="Модель не загружена")
    
    try:
        # Попытка загрузить информацию о модели
        results_path = os.path.join(project_root, 'reports', 'model_results.txt')
        with open(results_path, 'r', encoding='utf-8') as f:
            results = f.read()
            accuracy_line = [line for line in results.split('\n') 
                           if 'Точность на тестовой выборке:' in line]
            accuracy = accuracy_line[0].split(': ')[1] if accuracy_line else "Неизвестно"
    except FileNotFoundError:
        accuracy = "Неизвестно"
    
    return {
        "model_type": "RandomForestClassifier",
        "parameters": {"n_estimators": 100, "random_state": 42},
        "accuracy": accuracy,
        "features": ["feature1", "feature2", "feature3", "feature4"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)