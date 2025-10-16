#!/bin/bash
# Скрипт для настройки автоматической синхронизации Trials Service

set -e

echo "🔧 Настройка автоматической синхронизации Trials ↔ Patents"
echo "============================================================"

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Проверка что Docker запущен
echo -e "\n${YELLOW}Шаг 1: Проверка Docker...${NC}"
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker не запущен или недоступен${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker работает${NC}"

# 2. Проверка что контейнер trials_service существует
echo -e "\n${YELLOW}Шаг 2: Проверка контейнера trials_service...${NC}"
if ! docker ps -a | grep -q trials_service; then
    echo -e "${RED}❌ Контейнер trials_service не найден${NC}"
    echo "Запустите: docker-compose up -d"
    exit 1
fi

if ! docker ps | grep -q trials_service; then
    echo -e "${YELLOW}⚠️  Контейнер trials_service остановлен${NC}"
    echo "Запускаю контейнер..."
    docker-compose up -d trials-service
    sleep 5
fi
echo -e "${GREEN}✅ Контейнер trials_service запущен${NC}"

# 3. Проверка подключения к Patents Service
echo -e "\n${YELLOW}Шаг 3: Проверка подключения к Patents Service...${NC}"
if docker exec trials_service curl -s -o /dev/null -w "%{http_code}" http://host.docker.internal:8000/api/v2/patents/sorts/all/ | grep -q "200\|401"; then
    echo -e "${GREEN}✅ Patents Service доступен${NC}"
else
    echo -e "${RED}❌ Patents Service недоступен${NC}"
    echo "Убедитесь что Patents Service запущен на порту 8000"
    read -p "Продолжить настройку? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 4. Тестовая синхронизация
echo -e "\n${YELLOW}Шаг 4: Тестовая синхронизация (dry-run)...${NC}"
echo "Проверяем что можно синхронизировать..."
docker exec trials_service python manage.py sync_from_patents --model=sorts --dry-run --verbosity=0 2>&1 | head -20

read -p "Запустить начальную синхронизацию? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${YELLOW}Запуск начальной синхронизации...${NC}"
    echo "Это может занять несколько минут..."
    docker exec trials_service python manage.py sync_from_patents --model=all
    echo -e "${GREEN}✅ Начальная синхронизация завершена${NC}"
fi

# 5. Настройка cron на хосте
echo -e "\n${YELLOW}Шаг 5: Настройка автоматической синхронизации...${NC}"
echo "Добавляем задачи в crontab..."

CRON_SCRIPT="/tmp/trials-sync-cron.sh"
cat > $CRON_SCRIPT << 'EOF'
#!/bin/bash
# Автоматическая синхронизация Trials Service

# Ежедневная синхронизация сортов (2:00)
0 2 * * * docker exec trials_service python manage.py sync_from_patents --model=sorts --outdated-only --days=7 >> /var/log/trials-sync.log 2>&1

# Еженедельная синхронизация культур (воскресенье, 3:00)
0 3 * * 0 docker exec trials_service python manage.py sync_from_patents --model=cultures --outdated-only --days=30 >> /var/log/trials-sync.log 2>&1

# Ежемесячная полная синхронизация (1-го числа, 5:00)
0 5 1 * * docker exec trials_service python manage.py sync_from_patents --model=sorts >> /var/log/trials-sync.log 2>&1

# Проверка здоровья (каждое утро, 9:00)
0 9 * * * docker exec trials_service python manage.py check_sync_health >> /var/log/trials-health.log 2>&1
EOF

echo "Добавить эти задачи в crontab? (y/n)"
echo "--------------------------------------"
cat $CRON_SCRIPT
echo "--------------------------------------"

read -p "Продолжить? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Добавляем в crontab текущего пользователя
    (crontab -l 2>/dev/null; cat $CRON_SCRIPT) | crontab -
    echo -e "${GREEN}✅ Задачи добавлены в crontab${NC}"
    
    # Показываем текущий crontab
    echo -e "\nТекущий crontab:"
    crontab -l | grep -A 4 "Trials Service"
fi

# 6. Проверка состояния
echo -e "\n${YELLOW}Шаг 6: Проверка состояния синхронизации...${NC}"
docker exec trials_service python manage.py check_sync_health

# 7. Финальные инструкции
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Настройка завершена!${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}📋 Полезные команды:${NC}"
echo ""
echo "Проверить состояние:"
echo "  docker exec trials_service python manage.py check_sync_health"
echo ""
echo "Ручная синхронизация:"
echo "  docker exec trials_service python manage.py sync_from_patents --model=sorts --outdated-only --days=7"
echo ""
echo "Просмотр логов:"
echo "  tail -f /var/log/trials-sync.log"
echo "  tail -f /var/log/trials-health.log"
echo ""
echo "Просмотр crontab:"
echo "  crontab -l"
echo ""
echo "Удалить задачи из crontab:"
echo "  crontab -e  # удалить строки с 'trials_service'"
echo ""

echo -e "${YELLOW}📚 Документация:${NC}"
echo "  - SYNC_STRATEGY.md - стратегия синхронизации"
echo "  - SYNC_CHEATSHEET.md - шпаргалка по командам"
echo ""

