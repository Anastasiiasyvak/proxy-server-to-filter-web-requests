# Створення проксі-сервера для фільтрації веб-запитів

## Короткий опис задачі

У цьому завданні ми створювали проксі-сервер для фільтрації веб-запитів. Спочатку ми налаштували сервер Apache для роботи на порту 20000 замість стандартного порту 80, і обмежили доступ до цього порту лише локально в межах контейнера за допомогою iptables. Потім ми створили два HTML-файли - index.html та error.html, які мають відповідати веб-запитам. Далі був реалізований проксі-сервер, який в залежності від результату обчислень відправляв клієнту один з цих HTML-файлів. Нарешті, ми створили systemd service file для автоматичного запуску проксі-сервера після запуску сервера Apache.

## Файли 
- index.html - HTML-файл, який містить вітання для користувача та посилання на сторінку проксі-сервера. Цей файл створено для відображення коректного веб-запиту.
- error.html - HTML-файл, який містить повідомлення про помилку та посилання на сторінку проксі-сервера. Цей файл створено для відображення у випадку, якщо сталася помилка або неправильний запит.
  наші html файли ми створюємо в  `/var/www/html`
  
  ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/8f1a16f0-4748-49fb-a2df-99551e0e523e)
  
- proxy_server.py - Цей Python-скрипт визначає, який HTML-файл відправити клієнту в залежності від результату обчислень. Він також відповідає за керування відображенням сторінок та інкрементуванням лічильника.
- proxy-server.service - Файл служби systemd, який автоматично запускає проксі-сервер при запуску сервера Apache. Цей файл конфігурації вказує systemd на те, як запустити скрипт проксі-сервера. За допомогою `nano /etc/systemd/system/proxy-server.service` редагуємо файл.
  
## Процес виконання 
   - Створимо чистий контейнер Multipass на основі образу Ubuntu 22.04 за допомогою команди:
     ```
     multipass launch 22.04 --name=second-homework
     ```
   - Встановлення необхідних інструментів
     ```
     sudo apt update && sudo apt install socat && sudo apt install apache2 && sudo apt install iptables
     ```
   - Змінюємо прослуховування з 80 на 20000
     ```
     sudo nano /etc/apache2/ports.conf
     ```
   - Змінюємо Virtual Host з 80 на 20000
     ```
     sudo nano /etc/apache2/sites-enabled/000-default.conf
     ```
   - 
     ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/9c899d09-b20e-4644-99bb-82be6cd50aa4)
   - Створюємо файли index.html та error.html
   - Створюємо proxy_server.py
   - Створюємо proxy-server.service
   - Спочатку ми запускаємо apache2
     ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/a780985c-c36b-4009-8ab5-68fedcd85bed)
   - Потім запускаємо proxy-server
     ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/502c1506-cca0-445b-a16e-cd4e6e89ecbc)

   - ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/d641e8be-1372-4f94-8e5d-568425bd925c)


  
