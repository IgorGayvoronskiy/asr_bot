<h1>Проект по созданию speech recognition телеграм бота</h1>
<img src='https://github.com/IgorGayvoronskiy/asr_bot/blob/main/img/photo_bot.jpg' alter='bot_img'>
<h2>Описание</h2>
<br>Данный телеграм бот разработан на Python при помощи библиотеки telebot.</br> 
<br>Распознавание речи осуществляется за счёт работы asr модели whisper-small от OpenAi, дообученной на русскоязычной части датасета Common voice 17.0. Ссылка на модель на Hugging Face: https://huggingface.co/KnIgor/whisper-small-ru.</br>
<br>Для развёртывания на сервере используется docker файл.</br>
<h2>Примеры:</h2>
<a>Обработка аудиосообщения пользователя и вывод результата</a>
<img src='https://github.com/IgorGayvoronskiy/asr_bot/blob/main/img/work.png' alter='work_img'>
<a>Также данный бот имеет два режима работы: “отдых”, если хочется, чтобы бот не заполнял чат своими сообщениями, и “работа”. Переключение между ними осуществляется при помощи клавиатуры.</a>
<img src='https://github.com/IgorGayvoronskiy/asr_bot/blob/main/img/keyboard.png' alter='keyboard_img'>
<a>Если хочется узнать текущий режим работы бота можно воспользоваться командой /status.</a>
<img src='https://github.com/IgorGayvoronskiy/asr_bot/blob/main/img/status.png' alter='status_img'>
<a>И наконец, все команды, доступные боту, и их описание</a>
<img src='https://github.com/IgorGayvoronskiy/asr_bot/blob/main/img/commands.png' alter='commands_img'>
