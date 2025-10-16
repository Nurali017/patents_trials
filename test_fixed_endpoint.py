#!/usr/bin/env python3
"""
Тест исправленного endpoint add-participants
"""

import requests
import json

# URL endpoint
url = "http://localhost:8001/api/trial-plans/21/add-participants/"

# Тестовые данные (исправленные)
data = {
    "participants": [
        {
            "participant_number": 1,
            "maturity_group": "D01",
            "statistical_group": 1,
            "seeds_provision": "provided",  # Теперь поддерживается
            "trials": [  # Теперь поддерживается
                {
                    "region_id": 115,
                    "predecessor": "fallow",
                    "seeding_rate": 5,
                    "season": "spring"
                }
            ],
            "patents_sort_id": 2096
        },
        {
            "participant_number": 2,
            "maturity_group": "D01",
            "statistical_group": 1,
            "seeds_provision": "provided",
            "trials": [  # Теперь поддерживается
                {
                    "region_id": 115,
                    "predecessor": "fallow",
                    "seeding_rate": 5,
                    "season": "spring"
                }
            ],
            "application": 23,  # Теперь поддерживается
            "patents_sort_id": 2096
        }
    ]
}

# Отправляем запрос
try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")
