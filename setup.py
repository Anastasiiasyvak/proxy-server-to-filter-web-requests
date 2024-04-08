import subprocess

# Оновлення та встановлення необхідних пакетів
subprocess.run(['sudo', 'apt', 'update', '-y'])
subprocess.run(['sudo', 'apt', 'install', '-y', 'socat', 'apache2', 'iptables'])

# Зміна прослуховування з 80 на 20000 в файлі ports.conf
subprocess.run(['sudo', 'sed', '-i', 's/Listen 80/Listen 20000/', '/etc/apache2/ports.conf'])

# Зміна Virtual Host з 80 на 20000 в файлі 000-default.conf
subprocess.run(['sudo', 'sed', '-i', 's/<VirtualHost \*:80>/<VirtualHost \*:20000>/', '/etc/apache2/sites-enabled/000-default.conf'])

# Використання iptables для обмеження доступу до порту 20000
subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '20000', '-s', '127.0.0.1', '-j', 'ACCEPT'])
subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '20000', '-j', 'DROP'])

# Створення файлу служби для Socat Proxy Server
with open('/etc/systemd/system/proxy-server.service', 'w') as service_file:
    service_file.write("""
[Unit]
Description=Socat Proxy Server
After=apache2.service
Requires=apache2.service

[Service]
Type=simple
ExecStart=/usr/bin/socat TCP-LISTEN:80,fork,pktinfo exec:/home/ubuntu/proxy_server.py

[Install]
WantedBy=multi-user.target
""")

# Активуємо службу Socat Proxy Server
subprocess.run(['sudo', 'systemctl', 'enable', 'proxy-server'])

# Створення порожніх файлів index.html та error.html
open('/var/www/html/index.html', 'w').close()
open('/var/www/html/error.html', 'w').close()

# Додамо права для файлів index.html та error.html
subprocess.run(['sudo', 'chmod', '+x', '/var/www/html/index.html'])
subprocess.run(['sudo', 'chmod', '+x', '/var/www/html/error.html'])
