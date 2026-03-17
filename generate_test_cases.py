"""
Скрипт генерации тест-кейсов из технических требований с помощью GigaChat AI.

Использование:
    python generate_test_cases.py <input.md> [--output <output.md>] --credentials <key>

Пример:
    python generate_test_cases.py requirements.md --credentials MTIzNDU2Nzg5OmFiY2RlZmdo...
    python generate_test_cases.py requirements.md --output test_cases.md --credentials MTIzNDU2Nzg...
"""

import argparse
import sys
from pathlib import Path

from gigachat import GigaChat
from gigachat.exceptions import GigaChatException
from gigachat.models import Chat, Messages, MessagesRole

SYSTEM_PROMPT = (
    "Ты опытный QA-инженер. "
    "Твоя задача — на основе предоставленных технических требований составить полный набор тест-кейсов. "
    "Каждый тест-кейс должен содержать: номер, название, предусловия, шаги, ожидаемый результат. "
    "Отвечай строго в формате Markdown."
)

USER_PROMPT_TEMPLATE = (
    "Ниже приведены технические требования. "
    "Составь исчерпывающий набор тест-кейсов для проверки этих требований.\n\n"
    "---\n\n"
    "{requirements}"
)


def generate_test_cases(credentials: str, requirements: str, model: str, scope: str) -> str:
    """Отправить требования в GigaChat через SDK и получить тест-кейсы."""
    with GigaChat(
        credentials=credentials,
        scope=scope,
        model=model,
        verify_ssl_certs=False,
    ) as client:
        chat = Chat(
            messages=[
                Messages(role=MessagesRole.SYSTEM, content=SYSTEM_PROMPT),
                Messages(
                    role=MessagesRole.USER,
                    content=USER_PROMPT_TEMPLATE.format(requirements=requirements),
                ),
            ],
            temperature=0.3,
            max_tokens=4096,
        )
        response = client.chat(chat)
        return response.choices[0].message.content


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Генерация тест-кейсов из MD-файла с требованиями с помощью GigaChat AI."
    )
    parser.add_argument(
        "input",
        metavar="INPUT",
        help="Путь к входному MD-файлу с техническими требованиями.",
    )
    parser.add_argument(
        "--output", "-o",
        metavar="OUTPUT",
        default=None,
        help=(
            "Путь к выходному MD-файлу с тест-кейсами. "
            "По умолчанию: <имя_входного_файла>_test_cases.md"
        ),
    )
    parser.add_argument(
        "--credentials", "-c",
        metavar="CREDENTIALS",
        required=True,
        help="Base64-ключ авторизации GigaChat (из личного кабинета SberCloud).",
    )
    parser.add_argument(
        "--model",
        metavar="MODEL",
        default="GigaChat",
        help="Модель GigaChat для использования (по умолчанию: GigaChat).",
    )
    parser.add_argument(
        "--scope",
        metavar="SCOPE",
        default="GIGACHAT_API_PERS",
        help="OAuth-scope (по умолчанию: GIGACHAT_API_PERS).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # --- Входной файл ---
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[Ошибка] Входной файл не найден: {input_path}", file=sys.stderr)
        sys.exit(1)

    requirements = input_path.read_text(encoding="utf-8")
    if not requirements.strip():
        print("[Ошибка] Входной файл пуст.", file=sys.stderr)
        sys.exit(1)

    # --- Выходной файл ---
    output_path = Path(args.output) if args.output else input_path.parent / f"{input_path.stem}_test_cases.md"

    # --- Генерация тест-кейсов ---
    print(f"Генерация тест-кейсов для '{input_path.name}' (модель: {args.model})...")
    try:
        test_cases_md = generate_test_cases(
            credentials=args.credentials,
            requirements=requirements,
            model=args.model,
            scope=args.scope,
        )
    except GigaChatException as exc:
        print(f"[Ошибка GigaChat] {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"[Ошибка] {exc}", file=sys.stderr)
        sys.exit(1)

    # --- Сохранение результата ---
    output_path.write_text(test_cases_md, encoding="utf-8")
    print(f"[Готово] Тест-кейсы сохранены в: {output_path}")


if __name__ == "__main__":
    main()
