# websocket-messenger

Сервис для обмена моментальными сообщениями.

## Основные сущности

### Чат (`Chat`)

Объединение пользователей в группу, обменивающуюся сообщениями.
Чат имеет следующие параметры:

1. Идентификатор (`chat_id`)
2. Название (`name`)
3. Идентификатор инициатора (`initiator`)
4. Список участников (`participants`)
5. Историю сообщений (`history`)
6. Идентификатор последнего сообщения (`last_message`)
7. Время последней активности в чате (`last_activity_timestamp`)
8. Признак удаления (`deleted`)

### Сообщение (`Message`)

Текстовое сообщение, привязанное к чату, отправленное пользователем.
Все сообщения в рамках чата являются широковещательными. Все участники чата получают уведомления о новом сообщении.
Сообщение имеет следующие параметры:

1. Идентификатор (`message_id`)
2. Идентификатор чата (`chat_id`)
3. Идентификатор отправителя (`sender`)
4. Идентификатор сообщение, ответом на которое было сформировано текущее сообщение (`reply_to`)
5. Текст сообщения (`content`)
6. Вложения (`attachments`)
7. Статус (`status`): `sent`, `received`, `read`
8. Время создания (`created`)
9. Время обновления (`updated`)

### Вложение (`Attachment`)

Вложение, привязанное к чату. Вложение представляет из себя ссылку на медиафайл, указанного типа.
Вложение имеет следующие параметры:

1. Идентификатор (`attachment_id`)
2. Идентификатор чата (`chat_id`)
3. Идентификатор отправителя (`uploader`)
4. Время загрузки (`uploaded`)
5. Ссылка на вложение (`url`)
6. Название загруженного файла (`filename`)
7. Тип вложения (`content_type`): `image`, `audio`, `video`, `file`

### Реакция (`Reaction`)

Реакция на сообщение. Реакция представляет из себя emoji, оставленное под сообщением участником чата.
Реакция имеет следующие параметры:

1. Идентификатор (`reaction_id`)
2. Идентификатор отреагировавшего пользователя (`reactor`)
3. Идентификатор сообщения (`message_id`)
4. Emoji (`emoji`)
5. Время создания (`created`)

## Основные методы

### Чаты:
1. Создание чата: `POST /chats`
2. Получение списка чатов, доступных для пользователя: `GET /chats`
3. Загрузка нового вложения в чат: `POST /chats/{chat_id}/attachments`
4. Получение списка вложений в чате: `GET /chats/{chat_id}/attachments`
5. Отправка сообщения в чат: `POST /chats/{chat_id}/messages`
6. Получение списка сообщений в чате: `GET /chats/{chat_id}/messages`

### Сообщения:
1. Подтверждение получения сообщения: `PUT /messages/{message_id}/receive`
2. Подтверждение прочтения сообщения: `PUT /messages/{message_id}/read`
3. Удаление сообщения: `DELETE /messages/{message_id}`
4. Добавление реакции: `POST /messages/{message_id}/reactions`
5. Удаление реакции: `DELETE /messages/{message_id}/reactions/{reaction_id}`

### Подписки:
1. Подписка на моментальное получение новых сообщений: (`websocket`): `/subscriptions`

## Установка

```bash
python3.12 -m venv venv
make install
```

## Запуск

### Локальный запуск

```bash
make run
```

### Запуск в docker-compose

```bash
make docker-up
make docker-down
```

## Настройка среды разработки

### Установка зависимостей

```bash
make dev
```

### Настройка `pre-commit`

```bash
make pre-commit
```
