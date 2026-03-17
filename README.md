# generate_test_cases.py

Скрипт читает MD-файл с техническими требованиями, отправляет его в [GigaChat AI](https://developers.sber.ru/portal/products/gigachat) и сохраняет сгенерированные тест-кейсы в MD-файл.

## Установка

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Ключ авторизации (`--credentials`) — **Authorization Key** из [личного кабинета SberCloud](https://developers.sber.ru/studio).

## Запуск

```bash
python generate_test_cases.py <input.md> --credentials <ваш_ключ>
```

Выходной файл по умолчанию: `<имя_входного>_test_cases.md`.

```bash
# Указать выходной файл явно
python generate_test_cases.py requirements.md --output test_cases.md --credentials <ключ>

# Использовать модель GigaChat-Pro
python generate_test_cases.py requirements.md --credentials <ключ> --model GigaChat-Pro

# Корпоративный аккаунт
python generate_test_cases.py requirements.md --credentials <ключ> --scope GIGACHAT_API_CORP
```

## Аргументы

| Аргумент | Обязательный | Описание |
|---|---|---|
| `INPUT` | Да | Входной MD-файл с требованиями |
| `--output` / `-o` | Нет | Выходной MD-файл (по умолчанию `<input>_test_cases.md`) |
| `--credentials` / `-c` | Да | Authorization Key от GigaChat |
| `--model` | Нет | Модель GigaChat (по умолчанию: `GigaChat`) |
| `--scope` | Нет | OAuth-scope (по умолчанию: `GIGACHAT_API_PERS`) |
