#!/bin/bash

echo "🗄️  Запуск БД для Trials микросервиса"
echo "===================================="
echo ""

# Проверяем, не запущена ли уже БД
if docker ps | grep -q trials_postgres; then
    echo "ℹ️  БД уже запущена!"
    docker ps | grep trials_postgres
    echo ""
    echo "📊 Информация о подключении:"
    echo "   Host: localhost"
    echo "   Port: 5433"
    echo "   Database: trials_db"
    echo "   User: admin"
    echo "   Password: qwe1daSjewspds12"
    echo ""
    echo "🔗 Connection string: postgresql://admin:qwe1daSjewspds12@localhost:5433/trials_db"
    exit 0
fi

echo "🚀 Запускаем PostgreSQL..."
docker-compose up -d trials-db

# Ждем готовности БД
echo "⏳ Ожидание готовности БД..."
for i in {1..30}; do
    if docker exec trials_postgres pg_isready -U admin -d trials_db > /dev/null 2>&1; then
        echo ""
        echo "✅ БД успешно запущена и готова к работе!"
        echo ""
        echo "📊 Информация о подключении:"
        echo "   Host: localhost"
        echo "   Port: 5433"
        echo "   Database: trials_db"
        echo "   User: admin"
        echo "   Password: qwe1daSjewspds12"
        echo ""
        echo "🔗 Connection string: postgresql://admin:qwe1daSjewspds12@localhost:5433/trials_db"
        echo ""
        echo "💡 Для запуска микросервиса используйте: ./start-service.sh"
        exit 0
    fi
    echo -n "."
    sleep 1
done

echo ""
echo "❌ БД не готова после 30 секунд ожидания"
echo "📜 Проверьте логи: docker-compose logs trials-db"
exit 1


















