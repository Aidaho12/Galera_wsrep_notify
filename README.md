# Galera_wsrep_notify
Notification about chaneging Galera cluster status via Telegram

It's easy to use. Just install python3 and install package:
```
pip3 install pyTelegramBotApi
```
Add your credentials in the script:
```
    token_bot = ""
    channel_name = ""
    #Set proxy server if needs: http://ip:3128   
    proxy = ""
```    
Put the script in someting like /var/lib/mysql/, do 
```
chmod +x /var/lib/mysql/wsrep_status.py
```
to the script and add next row to the mysql config:
```
[galera]
wsrep_notify_cmd=/var/lib/mysql/wsrep_status.py
```

And set MariaDB variables to avoid restarting:
```
MariaDB [(none)]> set global wsrep_notify_cmd='/var/lib/mysql/wsrep_status.py'
```
Fork from: https://github.com/gguillen/galeranotify
