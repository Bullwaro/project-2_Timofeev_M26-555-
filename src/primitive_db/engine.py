import shlex
from prettytable import PrettyTable

import prompt

from .parser import parse_clause
from .core import (
                    create_table, 
                    drop_table, 
                    insert, 
                    select, 
                    update, 
                    delete
                   )
from .utils import (
                    load_metadata, 
                    save_metadata, 
                    load_table_data, 
                    save_table_data
                    )


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
                    "Команды для управления таблицами:\n"
                    "<command> create_table <имя_таблицы> "
                    "<столбец1:тип> <столбец2:тип> .. - создать таблицу\n"
                    "<command> list_tables - показать список таблиц\n"
                    "<command> drop_table <имя_таблицы> - удалить таблицу\n"
                    "<command> exit - выйти из программы\n"
                    "<command> help - справочная информация"

                    "\nCRUD-операции"
                    "<command> insert <table> <value>"
                    "<command> select <table> [where <clause>]"
                    "<command> update <table> set <clause> where <clause>"
                    "<command> delete <table> where <clause>"
                    "где clause вводится через пробел в виде <столбец> = <значение>"

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

            case "insert":
                table_name = args[1]
                values = [
                    int(value) if value.isdigit() else value
                    for value in args[2:]
                ]

                try:
                    data = insert(metadata, table_name, values)
                    print("Данные записаны")
                except (ValueError, IndexError) as error:
                    print(error)

            case "select":
                table_name = args[1]
                table_data = load_table_data(table_name)

                try:
                    if len(args) > 2:
                        where_clause = parse_clause(" ".join(args[3:]))
                        result = select(table_data, where_clause)
                    else:
                        result = select(table_data)

                    if result:
                        table = PrettyTable()
                        table.field_names = result[0].keys()

                        for row in result:
                            table.add_row(row.values())

                        print(table)
                    else:
                        print("Не найдено записей")
                except (ValueError, IndexError) as error:
                    print(error)

            case "update":
                table_name = args[1]
                table_data = load_table_data(table_name)

                try:
                    set_clause = parse_clause(" ".join(args[3:6]))
                    where_clause = parse_clause(" ".join(args[7:]))

                    data = update(table_data, set_clause, where_clause)
                    save_table_data(table_name, data)
                    print("Данные обновлены")
                except (ValueError, IndexError) as error:
                    print(error)

            case "delete":
                table_name = args[1]
                table_data = load_table_data(table_name)

                try:
                    where_clause = parse_clause(" ".join(args[3:]))

                    data = delete(table_data, where_clause)
                    save_table_data(table_name, data)
                    print("Записи удалены")
                except (ValueError, IndexError) as error:
                    print(error)

            case _:
                print(
                    f"Команда {command} не является допустимой."
                    f"Введите help для получения справочной информации"
                    )