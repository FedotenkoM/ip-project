# Backend

## Initial setup


#### Virtual environment setup

Открыть **backend** в Pycharm

File -> Settings -> Project: backend -> Python Interpreter -> ⚙ -> Add 
-> New Environment

или через консоль, находясь в ...\ip-project\backend

```bash
python -m venv .venv
```

#### Database setup
(on postgres console)

для активации постгрес консоли нужно прописать в командной строке

```bash
psql -U postgres
```

и ввести пароль от постгреса

```bash
create database "ad_system_dev";
create user "ad_system_dev_user" with encrypted password 'ad_system_dev_user';
grant all privileges on database "ad_system_dev" to "ad_system_dev_user";
```

## Day-to-day setup

Если вы зашли в Pycharm, у вас автоматически в `Terminal` включена виртуальная
среда и вам **не** нужно её включать

```bash
source .venv/bin/activate  # enter environment
```

```bash
deactivate # exit environment
```

## Requirements

Это можно прописать прямо в PyCharm терминале

```bash
pip install -r requirements.txt # after you entered environment
```

## Running

Также прописывается в PyCharm терминале

```bash
make run
```

## Migrations

```bash
# make automatic migration
make db-migrate

# upgrade database to head
make db-upgrade

# downgrade database at one revision
make db-downgrade
```

## Lint

```bash
flake8
```
