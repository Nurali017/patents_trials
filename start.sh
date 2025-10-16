#!/bin/bash

echo "🚀 Управление Trials сервисом"
echo "================================"
echo ""

show_menu() {
    echo "📋 Выберите вариант запуска:"
    echo ""
    echo "1. Запустить всё (БД + Микросервис)"
    echo "2. Запустить только БД"
    echo "3. Запустить только Микросервис (требует запущенную БД)"
    echo "4. Остановить всё"
    echo "5. Перезапустить всё"
    echo "6. Показать статус"
    echo "7. Показать логи"
    echo "0. Выход"
    echo ""
}

start_all() {
    echo "🚀 Запуск БД и Микросервиса..."
    docker-compose up --build -d
    echo ""
    echo "✅ Сервисы запущены!"
    show_info
}

start_db_only() {
    echo "🗄️  Запуск только БД..."
    docker-compose up -d trials-db
    echo ""
    echo "✅ БД запущена!"
    echo "📊 PostgreSQL доступен на порту: 5433"
    echo "🔗 Connection: postgresql://admin:qwe1daSjewspds12@localhost:5433/trials_db"
}

start_service_only() {
    echo "🔍 Проверка доступности БД..."
    if ! docker ps | grep -q trials_postgres; then
        echo "❌ Ошибка: БД не запущена!"
        echo "   Сначала запустите БД (опция 2) или запустите всё вместе (опция 1)"
        return 1
    fi
    
    echo "🔧 Запуск Микросервиса..."
    docker-compose up --build -d trials-service
    echo ""
    echo "✅ Микросервис запущен!"
    show_info
}

stop_all() {
    echo "🛑 Остановка всех сервисов..."
    docker-compose down
    echo "✅ Все сервисы остановлены!"
}

restart_all() {
    echo "🔄 Перезапуск всех сервисов..."
    docker-compose restart
    echo "✅ Сервисы перезапущены!"
    show_info
}

show_status() {
    echo "📊 Статус сервисов:"
    echo ""
    docker-compose ps
}

show_logs() {
    echo "📜 Показать логи какого сервиса?"
    echo "1. Микросервис"
    echo "2. БД"
    echo "3. Все"
    read -p "Выбор: " log_choice
    
    case $log_choice in
        1)
            docker-compose logs -f trials-service
            ;;
        2)
            docker-compose logs -f trials-db
            ;;
        3)
            docker-compose logs -f
            ;;
        *)
            echo "❌ Неверный выбор"
            ;;
    esac
}

show_info() {
    echo ""
    echo "📡 Информация о сервисах:"
    echo "=========================="
    echo "🌐 API: http://localhost:8001/api/"
    echo "📚 Swagger: http://localhost:8001/swagger/"
    echo "⚙️  Admin: http://localhost:8001/admin/"
    echo "🗄️  PostgreSQL: localhost:5433"
    echo ""
}

# Основной цикл меню
while true; do
    show_menu
    read -p "Введите номер: " choice
    echo ""
    
    case $choice in
        1)
            start_all
            ;;
        2)
            start_db_only
            ;;
        3)
            start_service_only
            ;;
        4)
            stop_all
            ;;
        5)
            restart_all
            ;;
        6)
            show_status
            ;;
        7)
            show_logs
            ;;
        0)
            echo "👋 Выход..."
            exit 0
            ;;
        *)
            echo "❌ Неверный выбор. Попробуйте снова."
            ;;
    esac
    
    echo ""
    read -p "Нажмите Enter для продолжения..."
    clear
done
