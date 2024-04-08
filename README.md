# Створення проксі-сервера для фільтрації веб-запитів

## Короткий опис задачі

У цьому завданні ми створювали проксі-сервер для фільтрації веб-запитів. Спочатку налаштовували сервер Apache для роботи на порту 20000 замість стандартного порту 80 та обмежили доступ до цього порту лише локально в межах контейнера за допомогою iptables. Потім створили два HTML-файли - index.html та error.html, які мають відповідати веб-запитам. Далі був реалізований проксі-сервер, який в залежності від результату обчислень відправляв клієнту один з цих HTML-файлів. Нарешті, ми створили systemd service file для автоматичного запуску проксі-сервера після запуску сервера Apache.

## Файли 
- index.html - HTML-файл, який містить вітання для користувача та посилання на сторінку проксі-сервера. Цей файл створено для відображення коректного веб-запиту.
- error.html - HTML-файл, який містить повідомлення про помилку та посилання на сторінку проксі-сервера. Цей файл створено для відображення у випадку, якщо сталася помилка або неправильний запит.
  наші html файли ми створюємо в  `/var/www/html`
  
  ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/8f1a16f0-4748-49fb-a2df-99551e0e523e)
  
- proxy_server.py - Цей Python-скрипт визначає, який HTML-файл відправити клієнту в залежності від результату обчислень. Він також відповідає за керування відображенням сторінок та інкрементуванням лічильника.
- proxy-server.service - файл служби systemd з назвою proxy-server.service у каталозі /etc/systemd/system/. Цей файл служби повинен автоматично запускати скрипт проксі-сервера (proxy_server.py) при запуску служби Apache2.
Використовуємо команду, подібну до sudo nano /etc/systemd/system/proxy-server.service, щоб створити та редагувати файл служби.
- setup.sh - Цей файл містить команди для автоматичного налаштування сервера та його компонентів. Він виконує такі дії:
1. Оновлення та встановлення необхідних пакетів: socat, apache2, iptables.
2. Зміна прослуховування з порту 80 на порт 20000 у файлі ports.conf Apache.
3. Зміна Virtual Host з порту 80 на порт 20000 у файлі 000-default.conf Apache.
4. Використання iptables для обмеження доступу до порту 20000, дозволяючи лише локальний доступ всередині контейнера.
  
## Процес виконання 
   - Створимо чистий контейнер Multipass на основі образу Ubuntu 22.04 за допомогою команди:
     ```
     multipass launch 22.04 --name=second-homework
     ```
   - За допомогою файла setup.py маємо автоматично встановлені команди
     ```
     nano setup.py
     ```
   - Надаємо право execute file
     ```
     chmod +x setup.py
     ```
   - ```
     sudo python3 setup.py
     ```
   - За допомогою наступної команди, можемо перевірити чи правильно встановлені права для iptables
     ```
     sudo iptables -L
     ```
    
 ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/9c899d09-b20e-4644-99bb-82be6cd50aa4)
 
   - Редагуємо файли index.html та error.html
   - Копіюємо proxy_server.py 
   - Спочатку ми запускаємо apache2
     ```
     sudo systemctl restart apache2
     ```
     та перевіряємо статус, у нашому випадку все добре і все запущено 
     ```
     sudo systemctl status apache2
     ```
     ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/a780985c-c36b-4009-8ab5-68fedcd85bed)
   - Потім запускаємо proxy-server
      ```
      sudo systemctl start proxy-server
      ```
      перевіряємо статус
      ```
      sudo systemctl status proxy-server
      ```
     ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/502c1506-cca0-445b-a16e-cd4e6e89ecbc)

   - перевіряємо чи все працює
   ```
   curl http://localhost:20000
   ```
   - ![image](https://github.com/Anastasiiasyvak/proxy-server-to-filter-web-requests/assets/119412566/d641e8be-1372-4f94-8e5d-568425bd925c)
