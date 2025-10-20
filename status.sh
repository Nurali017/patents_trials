#!/bin/bash

echo "📊 Статус Trials сервисов"
echo "========================="
echo ""

# Проверяем запущенные контейнеры
echo "🐳 Docker контейнеры:"
echo "--------------------"
docker ps --filter "name=trials_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Нет запущенных контейнеров"
echo ""

# Проверяем образы
echo "🖼️  Docker образы:"
echo "-----------------"
docker images --filter "reference=trials*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" 2>/dev/null || echo "Нет образов"
echo ""

# Проверяем volumes
echo "💾 Docker volumes:"
echo "-----------------"
docker volume ls --filter "name=trials" --format "table {{.Name}}\t{{.Driver}}" 2>/dev/null || echo "Нет volumes"
echo ""

# Детальная информация о сервисах
if docker ps | grep -q trials_postgres; then
    echo "✅ БД запущена"
    echo "   📊 PostgreSQL: localhost:5433"
    echo "   🗄️  Database: trials_db"
    
    # Проверяем подключение
    if docker exec trials_postgres pg_isready -U admin -d trials_db > /dev/null 2>&1; then
        echo "   🟢 Статус: Готова к работе"
    else
        echo "   🟡 Статус: Запускается..."
    fi
    echo ""
else
    echo "❌ БД не запущена"
    echo ""
fi

if docker ps | grep -q trials_service; then
    echo "✅ Микросервис запущен"
    echo "   🌐 API: http://localhost:8001/api/"
    echo "   📚 Swagger: http://localhost:8001/swagger/"
    echo "   ⚙️  Admin: http://localhost:8001/admin/"
    
    # Проверяем доступность сервиса
    if curl -s http://localhost:8001/api/ > /dev/null 2>&1; then
        echo "   🟢 Статус: Доступен"
    else
        echo "   🟡 Статус: Запускается..."
    fi
    echo ""
else
    echo "❌ Микросервис не запущен"
    echo ""
fi

# Использование ресурсов
echo "📈 Использование ресурсов:"
echo "-------------------------"
docker stats --no-stream --filter "name=trials_" --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "Нет запущенных контейнеров"
echo ""

# Быстрые команды
echo "💡 Быстрые команды:"
echo "------------------"
echo "   Запустить всё: ./start.sh или docker-compose up -d"
echo "   Запустить БД: ./start-db.sh"
echo "   Запустить сервис: ./start-service.sh"
echo "   Остановить: ./stop.sh"
echo "   Логи: docker-compose logs -f"




















