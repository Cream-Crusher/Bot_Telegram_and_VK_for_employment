# Пример бота

![screenshot=10x10](https://dvmn.org/filer/canonical/1569214089/322/)![screenshot](https://dvmn.org/filer/canonical/1569214094/323/)

### Область работы бота

Данный проект показывает работу бота с различными мессенджарами при взаимодействие бота с dialogflow.

### Как запустить

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Затем установите зависимости командой:


```sh
pip install -r requirements.txt
```


Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `vk_bot.py` или `tg_bot.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступна 1 переменная:
- `SECRET_KEY` — секретный ключ проекта

Создайте аналог файла .env с данными параметрами:

TG_TOKEN=Ваши данные - [Инструкция](https://web7.pro/kak-poluchit-token-bota-telegram-api/)

PROJECT_ID=Ваши данные - [Инструкция](https://console.cloud.google.com/projectcreate?previousPage=%2Fcloud-resource-manager%3Fhl%3Dru%26project%3D%26folder%3D%26organizationId%3D&hl=ru)

SESSION_ID=Ваши данные - id пользователя из Telegram.

GOOGLE_APPLICATION_CREDENTIALS= [Инструкция](https://cloud.google.com/docs/authentication/client-libraries)

VK_TOKEN=Ваши данные - Создайте сообщество вк и создайте токен [Инструкция](https://vk.com/@pinttiskad-kak-uznat-token-gruppy)

TG_CHAT_ID=Ваши данные [Инструкция](https://lumpics.ru/how-find-out-chat-id-in-telegram/)


### Возможности

- `Запуск VK бота`:

```sh
$ python3 vk_bot.py
```


- `Запуск TG бота`:

```sh
$ python3 tg_bot.py
```


- `Добавить намерения для бота`(ответы бота на сообщения)
 
  - Создайте файл ```questions.json``` рядом с файлом: `create_intent.py`
  
  - Пример файла:
```sh
{
    "Запись к врачу": {
        "questions": [
            "Как записаться к вам на прием?",
            "Как попасть к вам?",
            "Возможно-ли записаться к вам?",
            "Хочу посетить вас, как это сделать?"
        ],
        "answer": "Если вы хотите посетить нас, запишитесь на сайте ###"
    },
}
```
  - запустите файл и проверьте работаспособность на примере tg бота
  ```sh
  $ python3 create_intent.py
  ```
 
 ### Если возникли ошибки или проблемы с установкой токено, то возможно ответы есть тут:

[Учетные данные для ADC](https://cloud.google.com/docs/authentication/provide-credentials-adc)
[менеджер облачных ресурсов](https://console.cloud.google.com/cloud-resource-manager)
[Аутентификация gcloud](https://googleapis.dev/python/google-api-core/latest/auth.html)
[Создание агентов](https://dialogflow.cloud.google.com/)

#

Проект был создан в учебных уелях
