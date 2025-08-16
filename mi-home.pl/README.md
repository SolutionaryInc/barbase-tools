# Тестовый задание на позицию Backend-разработчик (Стажёр) на компанию ИП Solutionary Inc. Парсер товаров с сайта mi-home.pl

## Описание

Скрипт парсит каталог товаров с сайта [mi-home.pl](https://mi-home.pl) и сохраняет данные в **PostgreSQL** или в файлы.

Из каждой карточки товара извлекаются:

- **barcode** — штрихкод (EAN)
- **name** — название товара
- **images** — список ссылок на изображения

---

## Требования

- Node.js
- npm || yarn
- Docker

---

## Структура проекта

```bash
src/
├─ app.module.ts
├─ main.ts
├─ parser/
│  ├─ parser.service.ts      # Основной парсер с Puppeteer
├─ prisma/
│  ├─ prisma.service.ts      # PrismaService для подключения к БД
prisma/
├─ schema.prisma

```

## Настройка переменных окружения

Проект использует файл `.env` для хранения конфиденциальных данных и конфигурации.

### Пример `.env.example`

Создайте файл `.env` на основе `.env.example`:

## Запуск

1. Поднимите контейнеры с PostgreSQL и приложением:

```bash
docker compose up
```

1. Поднимите контейнеры с PostgreSQL и приложением:

```bash
docker compose up
```

2. Prisma автоматически сгенерирует клиент:

```bash
npx prisma generate
```

3. После запуска приложение будет доступно на:

```bash
http://localhost:3000
```

4. Отправлять запрос нужно в

```bash
http://localhost:3000/parser
```
