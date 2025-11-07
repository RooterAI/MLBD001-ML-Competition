@echo off
REM Автоматический запуск проекта MLBD001 для Windows
REM Работает на любой машине независимо от путей

echo ============================================================
echo ЗАПУСК ПРОЕКТА MLBD001
echo ============================================================
echo.

REM Определяем корневую директорию проекта
cd /d "%~dp0"
set PROJECT_ROOT=%CD%

echo Рабочая директория: %PROJECT_ROOT%
echo.

REM Проверка наличия виртуального окружения
if not exist ".venv\" (
    echo Виртуальное окружение не найдено. Создаём...
    python -m venv .venv
    echo Виртуальное окружение создано!
)

REM Активация виртуального окружения
echo Активация виртуального окружения...
call .venv\Scripts\activate.bat

REM Установка зависимостей
echo Установка зависимостей...
pip install -q -r requirements.txt
echo Зависимости установлены!
echo.

REM Запуск всех модулей
echo Запуск модулей обработки данных...
echo.

python src\module_a.py
echo.

python src\module_b.py
echo.

python src\module_c.py
echo.

echo ============================================================
echo ВСЕ МОДУЛИ ВЫПОЛНЕНЫ!
echo ============================================================
echo.

REM Запуск веб-приложения
echo Запуск веб-приложения...
echo Откройте браузер: http://localhost:8501
echo.

streamlit run src\app.py
