#!/bin/bash
set -e

BASE_URL="${1:-http://localhost:8001}"
COMPOSE_FILE_PATH="${COMPOSE_FILE_PATH:-docker-compose.prod.yml}"
PASS=0
FAIL=0

check() {
    local desc="$1"
    local method="$2"
    local url="$3"
    local data="$4"
    local expected="$5"

    if [ "$method" = "POST" ]; then
        status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$url" \
            -H "Content-Type: application/json" \
            -d "$data" 2>/dev/null)
    else
        status=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    fi

    if [ "$status" = "$expected" ]; then
        echo "[PASS] $desc (HTTP $status)"
        PASS=$((PASS + 1))
    else
        echo "[FAIL] $desc (expected $expected, got $status)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== trials smoke test ==="
echo "Target: $BASE_URL"
echo ""

# 1. Swagger UI (public, AllowAny)
check "Swagger UI available" \
    GET "${BASE_URL}/swagger/" \
    "" \
    "200"

# 2. Redoc (public, AllowAny)
check "Redoc available" \
    GET "${BASE_URL}/redoc/" \
    "" \
    "200"

# 3. Auth login — invalid creds return 401
check "Auth login endpoint (bad creds → 401)" \
    POST "${BASE_URL}/api/auth/login/" \
    '{"username":"admin","password":"test"}' \
    "401"

# 4. Patents Service integration (AllowAny, returns 200 on success, 500 on error)
echo ""
echo "--- Patents Service Integration ---"
check "Patents integration (test-connection → 200)" \
    GET "${BASE_URL}/api/patents/test-connection/" \
    "" \
    "200"

# Show integration details on failure
integration_body=$(curl -s "${BASE_URL}/api/patents/test-connection/" 2>/dev/null)
echo "  Response: ${integration_body}"

echo ""

# 5. Migrations check
echo "--- Migrations ---"
docker compose -f "$COMPOSE_FILE_PATH" exec -T trials_service python manage.py showmigrations 2>&1 | grep -E "\[ \]" && {
    echo "[WARN] Unapplied migrations found"
} || {
    echo "[PASS] All migrations applied"
    PASS=$((PASS + 1))
}

echo ""

# 6. Container logs check
echo "--- Last 20 log lines ---"
docker compose -f "$COMPOSE_FILE_PATH" logs --tail 20 trials_service 2>&1

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
