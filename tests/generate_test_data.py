"""
Скрипт для генерации тестовых данных.
Создаёт вариации вопросов по шаблонам для проверки стабильности агента.
"""

import json

TEMPLATES = [
    {
        "base": "Как сменить пароль",
        "variants": [
            "Как сменить пароль?",
            "Подскажите, как поменять пароль",
            "Хочу изменить свой пароль",
            "Где меняется пароль?",
            "Смена пароля — как это сделать?",
            "пароль сменить",
            "СМЕНИТЬ ПАРОЛЬ!!!",
            "Можно ли как-то обновить пароль?",
            "Забыл пароль, хочу новый",
            "Пароль не подходит, хочу сменить",
        ],
        "expected_source": "knowledge_base",
        "expected_keyword": "пароль",
    },
    {
        "base": "Неизвестный вопрос",
        "variants": [
            "Как полететь на Марс?",
            "Сколько стоит слон?",
            "Вы продаёте рыбу?",
            "Как собрать ядерный реактор?",
            "Где купить билет на поезд?",
            "Когда следующее затмение?",
            "Подскажите рецепт борща",
            "Как вырастить кактус?",
            "Что такое квантовая физика?",
            "Помоги решить уравнение",
        ],
        "expected_source": "ticket_created",
        "expected_keyword": None,
    },
]


def generate():
    test_cases = []
    for template in TEMPLATES:
        for variant in template["variants"]:
            test_cases.append({
                "message": variant,
                "expected_source": template["expected_source"],
                "expected_keyword": template["expected_keyword"],
                "category": template["base"],
            })

    with open("test_data.json", "w", encoding="utf-8") as f:
        json.dump(test_cases, f, ensure_ascii=False, indent=2)

    print(f"Сгенерировано {len(test_cases)} тест-кейсов -> test_data.json")


if __name__ == "__main__":
    generate()
