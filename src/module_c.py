"""
Модуль C: Построение и обучение модели
Простая реализация с RandomForestClassifier
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def load_data(filepath):
    """Загрузка очищенных данных"""
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Данные загружены: {df.shape}")
        return df
    except FileNotFoundError:
        print("❌ Файл не найден. Сначала запустите модуль A!")
        return None

def prepare_features(df):
    """Подготовка признаков и целевой переменной"""
    # Предполагаем, что целевая переменная называется 'target'
    if 'target' not in df.columns:
        print("❌ Целевая переменная 'target' не найдена!")
        return None, None
    
    # Разделение на признаки и целевую переменную
    X = df.drop('target', axis=1)
    y = df['target']
    
    print(f"Признаков: {X.shape[1]}")
    print(f"Образцов: {X.shape[0]}")
    print(f"Классы: {sorted(y.unique())}")
    
    return X, y

def train_model(X, y):
    """Обучение модели"""
    # Разделение на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Обучающая выборка: {X_train.shape}")
    print(f"Тестовая выборка: {X_test.shape}")
    
    # Создание и обучение модели
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    print("🔄 Обучение модели...")
    model.fit(X_train, y_train)
    
    # Предсказания
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Оценка качества
    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    
    print(f"\n📊 Результаты обучения:")
    print(f"Точность на обучении: {train_accuracy:.3f}")
    print(f"Точность на тесте: {test_accuracy:.3f}")
    
    # Подробный отчет
    print(f"\n📋 Подробный отчет (тест):")
    print(classification_report(y_test, y_pred_test))
    
    # Важность признаков
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n🔍 Важность признаков:")
    print(feature_importance)
    
    return model, test_accuracy, feature_importance

def save_model(model, filepath):
    """Сохранение обученной модели"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)
    print(f"✅ Модель сохранена: {filepath}")

def save_results(accuracy, feature_importance, filepath):
    """Сохранение результатов обучения"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    results = f"""РЕЗУЛЬТАТЫ ОБУЧЕНИЯ МОДЕЛИ
{'='*40}

Алгоритм: RandomForestClassifier
Параметры: n_estimators=100, random_state=42
Точность на тестовой выборке: {accuracy:.3f}

ВАЖНОСТЬ ПРИЗНАКОВ:
{'-'*30}
{feature_importance.to_string(index=False)}

ОЦЕНКА КАЧЕСТВА:
{'-'*20}
Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(results)
    
    print(f"✅ Результаты сохранены: {filepath}")

def main():
    """Основная функция модуля C"""
    print("=" * 50)
    print("МОДУЛЬ C: ОБУЧЕНИЕ МОДЕЛИ")
    print("=" * 50)
    
    # Пути к файлам (относительно корня проекта)
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, 'data', 'cleaned', 'cleaned_data.csv')
    model_path = os.path.join(project_root, 'models', 'model.pkl')
    results_path = os.path.join(project_root, 'reports', 'model_results.txt')
    
    # 1. Загрузка данных
    df = load_data(input_path)
    if df is None:
        return
    
    # 2. Подготовка признаков
    X, y = prepare_features(df)
    if X is None:
        return
    
    # 3. Обучение модели
    model, accuracy, feature_importance = train_model(X, y)
    
    # 4. Сохранение модели
    save_model(model, model_path)
    
    # 5. Сохранение результатов
    save_results(accuracy, feature_importance, results_path)
    
    print("\n" + "=" * 30)
    print("ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 30)
    print(f"🎯 Точность модели: {accuracy:.3f} ({accuracy*100:.1f}%)")
    print(f"🔧 Алгоритм: RandomForestClassifier")
    print(f"📊 Признаков использовано: {len(feature_importance)}")
    
    print("\n✅ Модуль C завершен успешно!")

if __name__ == "__main__":
    main()