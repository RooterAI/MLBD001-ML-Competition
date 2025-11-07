"""
Модуль B: Разведочный анализ данных
Простая реализация с базовыми визуализациями
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

def basic_statistics(df):
    """Базовая статистика"""
    print("\n" + "=" * 40)
    print("БАЗОВАЯ СТАТИСТИКА")
    print("=" * 40)
    
    print(f"Размер данных: {df.shape}")
    print(f"\nТипы данных:")
    print(df.dtypes)
    
    print(f"\nОписательная статистика:")
    print(df.describe())
    
    # Распределение целевой переменной
    if 'target' in df.columns:
        print(f"\nРаспределение целевой переменной:")
        print(df['target'].value_counts())

def create_visualizations(df, output_path):
    """Создание базовых визуализаций"""
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Разведочный анализ данных', fontsize=16)
    
    # 1. Гистограммы признаков
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    numeric_cols = [col for col in numeric_cols if col != 'target']
    
    axes[0, 0].set_title('Гистограммы признаков')
    for i, col in enumerate(numeric_cols[:4]):  # первые 4 признака
        axes[0, 0].hist(df[col], alpha=0.6, label=col, bins=20)
    axes[0, 0].legend()
    axes[0, 0].set_xlabel('Значения')
    axes[0, 0].set_ylabel('Частота')
    
    # 2. Корреляционная матрица
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                ax=axes[0, 1], fmt='.2f')
    axes[0, 1].set_title('Корреляционная матрица')
    
    # 3. Boxplot для поиска выбросов
    df[numeric_cols].boxplot(ax=axes[1, 0])
    axes[1, 0].set_title('Boxplot (выбросы)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # 4. Распределение целевой переменной
    if 'target' in df.columns:
        target_counts = df['target'].value_counts()
        axes[1, 1].pie(target_counts.values, labels=target_counts.index, 
                      autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title('Распределение целевой переменной')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Визуализации сохранены: {output_path}")
    plt.show()

def generate_conclusions(df, output_path):
    """Генерация выводов из анализа"""
    conclusions = []
    
    # Основные характеристики
    conclusions.append(f"1. Данные содержат {df.shape[0]} образцов и {df.shape[1]-1} признаков")
    
    # Корреляции
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    numeric_cols = [col for col in numeric_cols if col != 'target']
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        max_corr = corr_matrix.abs().unstack().sort_values(ascending=False)
        # Убираем автокорреляции (корреляция признака с самим собой)
        max_corr = max_corr[max_corr < 1.0]
        if len(max_corr) > 0:
            max_pair = max_corr.index[0]
            max_val = max_corr.iloc[0]
            conclusions.append(f"2. Наибольшая корреляция между {max_pair[0]} и {max_pair[1]}: {max_val:.3f}")
    
    # Выбросы
    outliers_info = []
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
        if len(outliers) > 0:
            outliers_info.append(col)
    
    if outliers_info:
        conclusions.append(f"3. Выбросы обнаружены в признаках: {', '.join(outliers_info)}")
    else:
        conclusions.append("3. Значительных выбросов не обнаружено")
    
    # Целевая переменная
    if 'target' in df.columns:
        target_dist = df['target'].value_counts(normalize=True)
        conclusions.append(f"4. Баланс классов: {target_dist.to_dict()}")
    
    # Сохранение выводов
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("ВЫВОДЫ РАЗВЕДОЧНОГО АНАЛИЗА ДАННЫХ\n")
        f.write("=" * 40 + "\n\n")
        for conclusion in conclusions:
            f.write(conclusion + "\n")
    
    print(f"✅ Выводы сохранены: {output_path}")
    
    return conclusions

def main():
    """Основная функция модуля B"""
    print("=" * 50)
    print("МОДУЛЬ B: РАЗВЕДОЧНЫЙ АНАЛИЗ ДАННЫХ")
    print("=" * 50)
    
    # Пути к файлам (относительно корня проекта)
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, 'data', 'cleaned', 'cleaned_data.csv')
    plots_path = os.path.join(project_root, 'reports', 'eda_plots.png')
    conclusions_path = os.path.join(project_root, 'reports', 'eda_conclusions.txt')
    
    # 1. Загрузка данных
    df = load_data(input_path)
    if df is None:
        return
    
    # 2. Базовая статистика
    basic_statistics(df)
    
    # 3. Визуализации
    create_visualizations(df, plots_path)
    
    # 4. Генерация выводов
    conclusions = generate_conclusions(df, conclusions_path)
    
    # 5. Вывод результатов
    print("\n" + "=" * 30)
    print("ОСНОВНЫЕ ВЫВОДЫ:")
    print("=" * 30)
    for conclusion in conclusions:
        print(conclusion)
    
    print("\n✅ Модуль B завершен успешно!")

if __name__ == "__main__":
    main()