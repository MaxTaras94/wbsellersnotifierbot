## Деплой бота на сервере

Протестировано на Debian 10.

Обновляем систему

```bash
sudo apt update && sudo apt upgrade
```
Устанавливаем докер и докер компоус
```bash
apt-get install docker.io
apt install docker-compose
```
Устанавливаем Python 3.11 сборкой из исходников и sqlite3:

```bash
cd
sudo apt install -y sqlite3 pkg-config
wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz
tar -xzvf Python-3.11.1.tgz
cd Python-3.11.1
./configure --enable-optimizations --prefix=/home/www/.python3.11
sudo make altinstall
```

Устанавливаем Poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Клонируем репозиторий в `~/code/wbsellersnotifierbot`:

```bash
mkdir -p ~/code/
cd ~/code
git clone https://github.com/MaxTaras94/wbsellersnotifierbot.git
cd wbsellersnotifierbot
```

Создаём переменные окружения:

```
cp wbsellersnotifierbot/.env.example wbsellersnotifierbot/.env
vim wbsellersnotifierbot/.env
```

`TELEGRAM_BOT_TOKEN` — токен бота, полученный в BotFather
Заполняем БД начальными данными:

```bash
cat wbsellersnotifierbot/db.sql | sqlite3 wbsellersnotifierbot/db.sqlite3
```

Устанавливаем зависимости Poetry и запускаем бота вручную:

```bash
poetry install
poetry run python -m wbsellersnotifierbot
```

Можно проверить работу бота. Для остановки, жмём `CTRL`+`C`.

Получим текущий адрес до Pytnon-интерпретатора в poetry виртуальном окружении Poetry:

```bash
poetry shell which python
```
Скопируем путь до интерпретатора Python в виртуальном окружении.

Настроим systemd-юнит для автоматического запуска бота, подставив скопированный путь в ExecStart, а также убедившись,
что директория до проекта (в данном случае `/home/www/code/wbsellersnotifierbot`) у вас такая же:

```
[Unit]
Description=Wildberries Notifier Telegram bot
After=network.target

[Service]
User=root
WorkingDirectory=/home/Hohlov/wbsellersnotifierbot
Restart=on-failure
RestartSec=2s
ExecStart=/root/.cache/pypoetry/virtualenvs/wbsellersnotifierbot-niaf6P17-py3.12/bin/python -m wbsellersnotifierbot

[Install]
WantedBy=multi-user.target
END

sudo systemctl daemon-reload
sudo systemctl enable wb.service
sudo systemctl start wb.service
```
