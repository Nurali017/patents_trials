#!/bin/bash

# Test script for creating a Trial via API
# Usage: ./test_trial_create.sh YOUR_AUTH_TOKEN

TOKEN="${1:-}"

if [ -z "$TOKEN" ]; then
    echo "Usage: ./test_trial_create.sh YOUR_AUTH_TOKEN"
    echo "Example: ./test_trial_create.sh eyJ0eXAiOiJKV1QiLCJhbGc..."
    exit 1
fi

BASE_URL="http://localhost:3002/api/v1"

echo "=== Testing Trial Creation ==="
echo ""

# Test 1: Minimal request
echo "1. Creating trial with minimal required fields..."
curl -X POST "${BASE_URL}/trials/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "title": "Test Trial - Minimal",
    "year": 2025,
    "region": 1,
    "start_date": "2025-05-01"
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.' || echo "Failed or jq not installed"

echo ""
echo "---"
echo ""

# Test 2: With optional fields
echo "2. Creating trial with optional fields..."
curl -X POST "${BASE_URL}/trials/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "title": "Test Trial - Full",
    "year": 2025,
    "region": 1,
    "start_date": "2025-05-01",
    "end_date": "2025-09-30",
    "description": "Test description",
    "status": "planned",
    "planting_season": "spring",
    "indicators": [1, 2]
  }' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | jq '.' || echo "Failed or jq not installed"

echo ""
echo "=== Tests Complete ==="




