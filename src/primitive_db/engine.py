import shlex

import prompt
from prettytable import PrettyTable

from .constants import METADATA_FILE
from .core import create_table, delete, drop_table, insert, select, update
from .parser import parse_clause
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def run():
    print("СУБД запущена")
    print(
        "Напишите help для получения справочной информации"
        )
    while True:
        metadata = load_metadata(METADATA_FILE)
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
                    "<command> insert <имя_таблицы> <значение1> <значение2> <..>"
                    " - вставить запись\n"
                    "<command> select <имя_таблицы> [where <условие>]"
                    " - вывести значения таблицы\n"
                    "<command> update <имя_таблицы> set <условие> where <условие>"
                    " - заменить значение в таблице\n"
                    "<command> delete <имя_таблицы> where <условие>"
                    " - удалить запись\n"
                    "где <условие> вводится через пробел в виде: "
                    "<столбец> = <значение>\n"
                    "условие в [] опционально"
                    )
            case "exit":
                print("База данных завершила свою работу")
                break

            case "create_table":
                result = create_table(metadata, args[1], args[2:])

                if result is not None:
                    save_metadata(METADATA_FILE, result)
                    print(f"Таблица {args[1]} создана")

            case "drop_table":
                result = drop_table(metadata, args[1])

                if result is not None:
                    save_metadata(METADATA_FILE, result)
                    print(f"Таблица {args[1]} удалена")

            case "list_tables":
                if list(metadata.keys()) != []:
                    print("Таблицы:\n", "\n".join(metadata.keys()), sep='')
                else:
                    print("Созданных таблиц не обнаружено")

            case "insert":
                table_name = args[1]
                values = [
                    int(value) if value.isdigit() else value
                    for value in args[2:]
                ]

                data = insert(metadata, table_name, values)

                if data is not None:
                    print("Данные записаны")

            case "select":
                table_name = args[1]
                table_data = load_table_data(table_name)

                if len(args) > 2:
                    if args[2] != "where":
                        print("Ожидалось where")
                        continue

                    where_clause = parse_clause(" ".join(args[3:]))
                    result = select(table_data, where_clause)
                else:
                    result = select(table_data)

                if result is None:
                    continue

                if result:
                    table = PrettyTable()
                    table.field_names = result[0].keys()

                    for row in result:
                        table.add_row(row.values())

                    print(table)
                else:
                    print("Не найдено записей")

            case "update":
                table_name = args[1]
                table_data = load_table_data(table_name)

                if args[2] != "set" or args[6] != "where":
                    print("Ожидались set и where")
                    continue

                set_clause = parse_clause(" ".join(args[3:6]))
                where_clause = parse_clause(" ".join(args[7:]))

                data = update(table_data, set_clause, where_clause)

                if data is not None:
                    save_table_data(table_name, data)
                    print("Данные обновлены")

            case "delete":
                table_name = args[1]
                table_data = load_table_data(table_name)

                if args[2] != "where":
                    print("Ожидалось where")
                    continue

                where_clause = parse_clause(" ".join(args[3:]))
                data = delete(table_data, where_clause)

                if data is not None:
                    save_table_data(table_name, data)
                    print("Записи удалены")

            case _:
                print(
                    f"Команда {command} не является допустимой."
                    f"Введите help для получения справочной информации"
                    )