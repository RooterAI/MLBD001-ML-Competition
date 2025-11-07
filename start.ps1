# Автоматический запуск проекта MLBD001
# Этот скрипт работает на любой машине независимо от путей

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "ЗАПУСК ПРОЕКТА MLBD001" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Определяем корневую директорию проекта
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_ROOT

Write-Host "📂 Рабочая директория: $PROJECT_ROOT" -ForegroundColor Yellow
Write-Host ""

# Проверка наличия виртуального окружения
$VENV_PATH = Join-Path $PROJECT_ROOT ".venv"
if (-not (Test-Path $VENV_PATH)) {
    Write-Host "⚠️  Виртуальное окружение не найдено. Создаём..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Виртуальное окружение создано!" -ForegroundColor Green
}

# Активация виртуального окружения
Write-Host "🔄 Активация виртуального окружения..." -ForegroundColor Cyan
$ACTIVATE_SCRIPT = Join-Path $VENV_PATH "Scripts\Activate.ps1"
& $ACTIVATE_SCRIPT

# Проверка и установка зависимостей
Write-Host "📦 Проверка зависимостей..." -ForegroundColor Cyan
pip install -q -r requirements.txt
Write-Host "✅ Зависимости установлены!" -ForegroundColor Green
Write-Host ""

# Запуск всех модулей
Write-Host "🚀 Запуск модулей обработки данных..." -ForegroundColor Cyan
Write-Host ""

python src/module_a.py
Write-Host ""

python src/module_b.py
Write-Host ""

python src/module_c.py
Write-Host ""

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ ВСЕ МОДУЛИ ВЫПОЛНЕНЫ!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Запуск веб-приложения
Write-Host "🌐 Запуск веб-приложения..." -ForegroundColor Cyan
Write-Host "📌 Откройте браузер: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""

streamlit run src/app.py
