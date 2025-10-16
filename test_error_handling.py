#!/usr/bin/env python3
"""
Тест обработки ошибок в endpoint add-participants
"""

import requests
import json

# URL endpoint
url = "http://localhost:8001/api/trial-plans/21/add-participants/"

print("=== Тест 1: Отсутствует region_id ===")
data1 = {
    "participants": [
        {
            "participant_number": 99,
            "maturity_group": "D01",
            "statistical_group": 1,
            "seeds_provision": "provided",
            "trials": [
                {
                    # "region_id": 112,  # ← Отсутствует!
                    "predecessor": "fallow",
                    "seeding_rate": 5,
                    "season": "spring"
                }
            ],
            "patents_sort_id": 2096
        }
    ]
}

try:
    response = requests.post(url, json=data1)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")

print("\n=== Тест 2: Отсутствует predecessor ===")
data2 = {
    "participants": [
        {
            "participant_number": 98,
            "maturity_group": "D01",
            "statistical_group": 1,
            "seeds_provision": "provided",
            "trials": [
                {
                    "region_id": 112,
                    # "predecessor": "fallow",  # ← Отсутствует!
                    "seeding_rate": 5,
                    "season": "spring"
                }
            ],
            "patents_sort_id": 2096
        }
    ]
}

try:
    response = requests.post(url, json=data2)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")

print("\n=== Тест 3: Дублирование participant_number ===")
data3 = {
    "participants": [
        {
            "participant_number": 1,  # ← Уже существует!
            "maturity_group": "D01",
            "statistical_group": 1,
            "seeds_provision": "provided",
            "trials": [
                {
                    "region_id": 112,
                    "predecessor": "fallow",
                    "seeding_rate": 5,
                    "season": "spring"
                }
            ],
            "patents_sort_id": 2096
        }
    ]
}

try:
    response = requests.post(url, json=data3)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")
