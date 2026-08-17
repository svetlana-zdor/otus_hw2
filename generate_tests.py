import argparse
import sys
import ollama

def generate_scenarios(count: int, model_name: str, output_file: str):
    prompt = f"""
    Сгенерируй ровно {count} сценариев тестирования для формы регистрации пользователя.

    Поля формы:
    1. Поле ввода имени пользователя (Username)
    2. Поле ввода пароля (Password)
    3. Поле ввода подтверждения пароля (Confirm Password)
    4. Кнопка «Зарегистрировать»

    Требования:
    - Обязательно включи как ПОЗИТИВНЫЕ (positive), так и НЕГАТИВНЫЕ (negative) сценарии.
    - Выведи результат строго в формате Markdown.
    - Для каждого сценария укажи: ID, Название, Тип (Позитивный/Негативный), Предварительные условия, Шаги и Ожидаемый результат.
    - Язык ответа: Русский.
    """

    print(f"Отправка запроса в Ollama (модель: {model_name}, количество: {count})...")
    
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response['message']['content']
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Успешно! Сценарии сохранены в файл '{output_file}'.")
        
    except Exception as e:
        print(f"Ошибка при генерации: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="CLI-скрипт генерации тест-кейсов для формы регистрации с помощью Ollama"
    )
    parser.add_argument(
        "count", 
        type=int, 
        help="Количество генерируемых сценариев тестирования"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default="qwen2.5", 
        help="Название модели Ollama (по умолчанию: qwen2.5)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="scenarios.md", 
        help="Имя выходного Markdown-файла (по умолчанию: scenarios.md)"
    )

    args = parser.parse_args()
    generate_scenarios(args.count, args.model, args.output)

if __name__ == "__main__":
    main()