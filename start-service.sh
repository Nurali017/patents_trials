#!/bin/bash

echo "🔧 Запуск Trials микросервиса"
echo "=============================="
echo ""

# Проверяем, не запущен ли уже сервис
if docker ps | grep -q trials_service; then
    echo "ℹ️  Микросервис уже запущен!"
    docker ps | grep trials_service
    echo ""
    echo "📡 Сервис доступен по адресам:"
    echo "   🌐 API: http://localhost:8001/api/"
    echo "   📚 Swagger: http://localhost:8001/swagger/"
    echo "   ⚙️  Admin: http://localhost:8001/admin/"
    exit 0
fi

# Проверяем, запущена ли БД
echo "🔍 Проверка доступности БД..."
if ! docker ps | grep -q trials_postgres; then
    echo "❌ Ошибка: БД не запущена!"
    echo ""
    echo "💡 Сначала запустите БД:"
    echo "   ./start-db.sh"
    echo ""
    echo "   Или запустите всё вместе:"
    echo "   ./start.sh"
    exit 1
fi

# Проверяем готовность БД
if ! docker exec trials_postgres pg_isready -U admin -d trials_db > /dev/null 2>&1; then
    echo "⚠️  БД запущена, но еще не готова. Ожидание..."
    for i in {1..30}; do
        if docker exec trials_postgres pg_isready -U admin -d trials_db > /dev/null 2>&1; then
            echo "✅ БД готова!"
            break
        fi
        echo -n "."
        sleep 1
    done
    echo ""
fi

echo "✅ БД доступна!"
echo ""
echo "🚀 Запускаем микросервис..."
docker-compose up --build -d trials-service

# Ждем запуска сервиса
echo "⏳ Ожидание запуска сервиса..."
sleep 3

# Показываем логи в реальном времени
echo ""
echo "📜 Логи запуска (Ctrl+C для выхода):"
echo "===================================="
docker-compose logs -f trials-service &
LOGS_PID=$!

# Ждем несколько секунд и показываем информацию
sleep 5
kill $LOGS_PID 2>/dev/null

echo ""
echo "✅ Микросервис запущен!"
echo ""
echo "📡 Сервис доступен по адресам:"
echo "   🌐 API: http://localhost:8001/api/"
echo "   📚 Swagger: http://localhost:8001/swagger/"
echo "   ⚙️  Admin: http://localhost:8001/admin/"
echo ""
echo "💡 Для просмотра логов: docker-compose logs -f trials-service"
echo "💡 Для остановки: docker-compose stop trials-service"


















