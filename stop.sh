#!/bin/bash

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose не найден"
    exit 1
fi

echo "🛑 Остановка Trials сервисов"
echo "============================="
echo ""

# Проверяем запущенные контейнеры
RUNNING_CONTAINERS=$(docker ps --filter "name=trials_" --format "{{.Names}}" | wc -l | tr -d ' ')

if [ "$RUNNING_CONTAINERS" = "0" ]; then
    echo "ℹ️  Нет запущенных контейнеров Trials"
    exit 0
fi

echo "📋 Запущенные контейнеры:"
docker ps --filter "name=trials_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

# Спрашиваем что остановить
echo "Что остановить?"
echo "1. Всё (БД + Микросервис)"
echo "2. Только Микросервис"
echo "3. Только БД"
echo "4. Остановить и удалить все данные (включая volumes)"
echo "0. Отмена"
echo ""
read -p "Выбор: " choice

case $choice in
    1)
        echo "🛑 Остановка всех сервисов..."
        $COMPOSE_CMD down
        echo "✅ Все сервисы остановлены!"
        ;;
    2)
        echo "🛑 Остановка микросервиса..."
        $COMPOSE_CMD stop trials_service
        $COMPOSE_CMD rm -f trials_service
        echo "✅ Микросервис остановлен!"
        ;;
    3)
        echo "🛑 Остановка БД..."
        $COMPOSE_CMD stop trials-db
        $COMPOSE_CMD rm -f trials-db
        echo "✅ БД остановлена!"
        echo "⚠️  Внимание: данные сохранены в volume trials_postgres_data"
        ;;
    4)
        echo "⚠️  ВНИМАНИЕ: Это удалит все данные из БД!"
        read -p "Вы уверены? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            echo "🗑️  Остановка и удаление всех данных..."
            $COMPOSE_CMD down -v
            echo "✅ Все сервисы остановлены и данные удалены!"
        else
            echo "❌ Операция отменена"
        fi
        ;;
    0)
        echo "❌ Операция отменена"
        ;;
    *)
        echo "❌ Неверный выбор"
        exit 1
        ;;
esac






































