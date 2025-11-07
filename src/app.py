"""
Модуль D: Разработка программного продукта
Простое веб-приложение на Streamlit для предсказаний
"""
import streamlit as st
import pandas as pd
import joblib
import os
import sys

# Добавляем корень проекта в sys.path для правильной работы импортов
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)  # Меняем рабочую директорию на корень проекта

def load_model(model_path):
    """Загрузка обученной модели"""
    try:
        full_path = os.path.join(project_root, model_path)
        model = joblib.load(full_path)
        return model
    except FileNotFoundError:
        st.error("❌ Модель не найдена. Сначала запустите модуль C!")
        return None

def load_sample_data():
    """Загрузка данных для определения признаков"""
    try:
        data_path = os.path.join(project_root, 'data', 'cleaned', 'cleaned_data.csv')
        df = pd.read_csv(data_path)
        return df.drop('target', axis=1)
    except FileNotFoundError:
        st.error("❌ Данные не найдены. Сначала запустите модули A и B!")
        return None

def create_input_form(features_df):
    """Создание формы для ввода данных"""
    st.subheader("🔢 Введите значения признаков:")
    
    input_data = {}
    
    # Создаем поля ввода для каждого признака
    for col in features_df.columns:
        col_min = float(features_df[col].min())
        col_max = float(features_df[col].max())
        col_mean = float(features_df[col].mean())
        
        input_data[col] = st.number_input(
            f"{col}",
            min_value=col_min,
            max_value=col_max,
            value=col_mean,
            step=(col_max - col_min) / 100,
            help=f"Диапазон: {col_min:.3f} - {col_max:.3f}"
        )
    
    return input_data

def make_prediction(model, input_data):
    """Выполнение предсказания"""
    # Создаем DataFrame из входных данных
    input_df = pd.DataFrame([input_data])
    
    # Предсказание
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]
    
    return prediction, probability

def display_results(prediction, probability):
    """Отображение результатов предсказания"""
    st.subheader("🎯 Результат предсказания:")
    
    # Основной результат
    if prediction == 1:
        st.success(f"✅ Класс: {prediction} (Положительный)")
    else:
        st.info(f"ℹ️ Класс: {prediction} (Отрицательный)")
    
    # Вероятности
    st.subheader("📊 Вероятности:")
    prob_df = pd.DataFrame({
        'Класс': [0, 1],
        'Вероятность': probability,
        'Процент': probability * 100
    })
    
    st.dataframe(prob_df)
    
    # Визуализация вероятностей
    st.bar_chart(prob_df.set_index('Класс')['Процент'])

def show_model_info():
    """Отображение информации о модели"""
    st.sidebar.subheader("ℹ️ О модели")
    st.sidebar.write("**Алгоритм:** RandomForestClassifier")
    st.sidebar.write("**Параметры:** n_estimators=100")
    
    # Попытка загрузить результаты
    try:
        results_path = os.path.join(project_root, 'reports', 'model_results.txt')
        with open(results_path, 'r', encoding='utf-8') as f:
            results = f.read()
            if 'Точность на тестовой выборке:' in results:
                accuracy_line = [line for line in results.split('\n') 
                               if 'Точность на тестовой выборке:' in line][0]
                accuracy = accuracy_line.split(': ')[1]
                st.sidebar.write(f"**Точность:** {accuracy}")
    except FileNotFoundError:
        st.sidebar.write("**Точность:** Не определена")

def main():
    """Основная функция веб-приложения"""
    # Настройка страницы
    st.set_page_config(
        page_title="ML Предсказание",
        page_icon="🤖",
        layout="wide"
    )
    
    # Заголовок
    st.title("🤖 ML Предсказание")
    st.markdown("Простое веб-приложение для машинного обучения")
    
    # Боковая панель с информацией о модели
    show_model_info()
    
    # Основной интерфейс
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📥 Входные данные")
        
        # Загрузка модели
        model = load_model(os.path.join('models', 'model.pkl'))
        if model is None:
            return
        
        # Загрузка примера данных для определения признаков
        features_df = load_sample_data()
        if features_df is None:
            return
        
        # Форма ввода
        input_data = create_input_form(features_df)
        
        # Кнопка предсказания
        if st.button("🔮 Сделать предсказание", type="primary"):
            prediction, probability = make_prediction(model, input_data)
            
            # Сохранение результатов в сессии
            st.session_state.prediction = prediction
            st.session_state.probability = probability
            st.session_state.input_data = input_data
    
    with col2:
        st.header("📊 Результаты")
        
        # Отображение результатов если они есть
        if hasattr(st.session_state, 'prediction'):
            display_results(st.session_state.prediction, 
                          st.session_state.probability)
            
            # Показываем введенные данные
            st.subheader("📋 Введенные данные:")
            input_df = pd.DataFrame([st.session_state.input_data])
            st.dataframe(input_df.T, width='stretch')
        else:
            st.info("👆 Введите данные и нажмите 'Сделать предсказание'")
    
    # Дополнительная информация
    st.markdown("---")
    st.markdown("**Проект:** Конкурсное задание МОиБД | **Модуль D:** Веб-приложение")

if __name__ == "__main__":
    main()