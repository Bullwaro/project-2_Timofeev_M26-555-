import shlex

import prompt

from .core import create_table, drop_table
from .utils import load_metadata, save_metadata


def run():
    print("СУБД запущена")
    print(
        "Напишите help для получения справочной информации"
        )
    while True:
        metadata = load_metadata("db_meta.json")
        args = shlex.split(prompt.string(">> "))

        if not args:
            continue

        command = args[0]
        match command:
            case "help":
                print(
                    "Функции:\n"
                    "<command> create_table <имя_таблицы> "
                    "<столбец1:тип> <столбец2:тип> .. - создать таблицу\n"
                    "<command> list_tables - показать список таблиц\n"
                    "<command> drop_table <имя_таблицы> - удалить таблицу\n"
                    "<command> exit - выйти из программы\n"
                    "<command> help - справочная информация"
                    )
            case "exit":
                print("База данных завершила свою работу")
                break

            case "create_table":
                metadata = create_table(metadata, args[1], args[2:])
                save_metadata("db_meta.json", metadata)
                print(f"Таблица {args[1]} создана")

            case "drop_table":
                metadata = drop_table(metadata, args[1])
                save_metadata("db_meta.json", metadata)
                print(f"Таблица {args[1]} удалена")

            case "list_tables":
                print(list(metadata.keys()))

            case _:
                print(
                    f"Команда {command} не является допустимой."
                    f"Введите help для получения справочной информации"
                    )