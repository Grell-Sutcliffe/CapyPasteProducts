# Сравниватель цен

**Сравниватель цен** — это Python-приложение, разработанное на Flask, которое позволяет сравнивать цены на товары с различных платформ. Проект предоставляет удобный веб-интерфейс для поиска и анализа цен, а также поддерживает несколько методов парсинга данных.

## Структура проекта

### Основные файлы и папки:
- **`app.py`**  
  Главный файл приложения, запускающий Flask-сервер и связывающий функциональность парсеров и веб-интерфейса.
  
- **`parsers/`**  
  Содержит модули для парсинга данных:
  - **`vasko.py`** — парсер, который собирает данные с сайта в момент запроса.
  - **`parser_techno.py`** — парсер, который предварительно собирает данные и сохраняет их в JSON-файл.

- **`parsed_data/`**  
  Содержит предобработанные данные в формате JSON, собранные парсером `parser_techno.py`.

- **`templates/`**  
  Шаблоны HTML для веб-интерфейса:
  - **Начальный экран** — главная страница приложения.
  - **Поиск** — страница для ввода и отображения результатов поиска.
  - **Авторизация** — страница входа для пользователей.
  - **История** — страница с историей запросов пользователя.
  - **Профиль** — личный кабинет пользователя.
  - **Ошибка 404** — страница, отображаемая при некорректных URL.


