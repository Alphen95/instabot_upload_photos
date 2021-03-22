# Космический Инстаграм

- так, а что сюда написать?... а, понятно.

Проект для загрузки фотографий космоса с телескопа Хаббл и SpaceX и выгрузки этих фотографий в социальную сеть Instagram.

### Как установить

Записываем ключ и имя пользователя
1. откройте Блокнот/WordPad/TextEdit/Gedit (а лучше Notepad++)
2. запишите туда:
```
USERNAME_INSTABOT=ваше имя пользователя от аккаунта Instagram
PASSWORD_INSTABOT=ваш пароль от аккаунта Instagram
```
3. сохраните в папку со скачанными файлами под именем ".env" (если файл не показывается в Проводнике - ничего страшного! ваша система просто тихо мигргировала на ядро Linux.)

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Загружаем картинки
1. откройте:
в Windows NT - cmd.exe
в Windows 9x - файла нет, найдите в меню Пуск
в MacOS X 10.0 - 11.1 - Terminal (Терминал)
в Ubuntu/Kubuntu/Xubuntu/Lubuntu/Mint/Bolgen OS - тоже Терминал
в BSD - вы уже в терминале!
в MacOS 9.x - откуда у вас там Python 3?
2. сначала запустите скрипт load_images.py и дождитесь до его полного завершения.
пример:
```
python3 load_images.py
```
3. после этого запустите auto_load.py и наслаждайтесь работой.
```
python3 auto_load.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

### Для пользователей BSD

Как создать файл:
1. Зайдите в редактор ViM - vim имя_файла
2. нажмите SHIFT+A (режим редактирования)
3. для выхода - [esc] :q!
   для сохранения - [esc] :w!
   для выхода и сохранения - [esc] :wq!
   
### Дополнительная настройка

если хотите изменить задержку между загрузкой картинок:
1. откройте auto_load.py своим любимым редактором текстовых файлов
2. измените цифры на строках 21-23 как вам требуется
3. сохраните файл.