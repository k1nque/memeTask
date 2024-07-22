# memeTask
## Запуск и настройка

#### docker-compose.yml:
##### В сервисе postgres укажите поля: 
 - POSTGRES_DB
 - POSTGRES_USER
 - POSTGRES_PASSWORD
 - Также можете изменить порты по умолчанию
---
 ##### В сервисе minio укажите поля:
 - MINIO_ROOT_USER
 - MINIO_ROOT_PASSWORD
 - Также можете изменить порты по умолчанию
##### Настройка PublicAPI и PricateAPI
 - В каталогах PublicAPI и PrivateAPI переименуйте template.env в .env, а также укажите нужные поля, в зависимости от внесенных изменений ранее в docker-compose.yml

## Запуск

```bash
docker compose up
```
