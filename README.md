# Galera_wsrep_notify
Notification about chaneging Galera cluster status via Telegram

It's easy to use. Just install python3 and install package:
```
pip3 install pyTelegramBotApi
```

Put script someting like /var/lib/mysql/, do chmod +x to the script and add next row to the config:
```
[galera]
wsrep_notify_cmd=/var/lib/mysql/wsrep_status.py
```

And set MariaDB variables to avoid restarting:
```
MariaDB [(none)]> set global wsrep_notify_cmd='/var/lib/mysql/wsrep_status.py'
```