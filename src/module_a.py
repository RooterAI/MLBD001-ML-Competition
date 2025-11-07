"""
Модуль A: Парсинг и предобработка данных
Простая реализация для работы с CSV файлом
"""
import pandas as pd
import os

def create_sample_data():
    """Создаем пример данных для демонстрации"""
    import numpy as np
    
    # Устанавливаем seed для воспроизводимости
    np.random.seed(42)
    
    # Создаем простой dataset для классификации
    n_samples = 1000
    
    data = {
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.normal(1, 1.5, n_samples),
        'feature3': np.random.uniform(-2, 2, n_samples),
        'feature4': np.random.exponential(1, n_samples),
        'target': np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
    }
    
    # Добавляем немного пропусков и дубликатов
    df = pd.DataFrame(data)
    
    # Добавляем пропуски (5%)
    mask = np.random.choice([True, False], n_samples, p=[0.05, 0.95])
    df.loc[mask, 'feature1'] = None
    
    # Добавляем дубликаты
    duplicates = df.sample(50).copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    return df

def load_data(filepath):
    """Загрузка данных из CSV файла"""
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Данные загружены: {df.shape}")
        return df
    except FileNotFoundError:
        print("⚠️  Файл не найден, создаем демонстрационный dataset...")
        return create_sample_data()

def clean_data(df):
    """Базовая предобработка данных"""
    print(f"Исходные данные: {df.shape}")
    
    # Проверяем пропуски
    missing_before = df.isnull().sum().sum()
    print(f"Пропусков до обработки: {missing_before}")
    
    # Удаляем строки с пропусками
    df_clean = df.dropna()
    print(f"После удаления пропусков: {df_clean.shape}")
    
    # Проверяем дубликаты
    duplicates_before = df_clean.duplicated().sum()
    print(f"Дубликатов до обработки: {duplicates_before}")
    
    # Удаляем дубликаты
    df_clean = df_clean.drop_duplicates()
    print(f"После удаления дубликатов: {df_clean.shape}")
    
    return df_clean

def save_cleaned_data(df, output_path):
    """Сохранение очищенных данных"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Очищенные данные сохранены: {output_path}")

def main():
    """Основная функция модуля A"""
    print("=" * 50)
    print("МОДУЛЬ A: ПРЕДОБРАБОТКА ДАННЫХ")
    print("=" * 50)
    
    # Пути к файлам (относительно корня проекта)
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, 'data', 'raw', 'data.csv')
    output_path = os.path.join(project_root, 'data', 'cleaned', 'cleaned_data.csv')
    
    # 1. Загрузка данных
    df = load_data(input_path)
    
    # 2. Предобработка
    df_clean = clean_data(df)
    
    # 3. Сохранение результата
    save_cleaned_data(df_clean, output_path)
    
    # 4. Финальная статистика
    print("\n" + "=" * 30)
    print("РЕЗУЛЬТАТЫ ПРЕДОБРАБОТКИ:")
    print("=" * 30)
    print(f"Исходных строк: {len(df)}")
    print(f"Очищенных строк: {len(df_clean)}")
    print(f"Удалено строк: {len(df) - len(df_clean)}")
    print(f"Признаков: {len(df_clean.columns) - 1}")  # -1 для target
    print(f"Целевая переменная: target")
    print("\n✅ Модуль A завершен успешно!")

if __name__ == "__main__":
    main()