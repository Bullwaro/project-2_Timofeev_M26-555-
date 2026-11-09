import os

from .constants import VALID_TYPES
from .decorators import (
    confirm_action,
    create_cacher,
    handle_db_errors,
    log_time,
)
from .utils import load_table_data, save_table_data

cache_result = create_cacher()


@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError("Таблица с таким именем уже существует")

    for column in columns:
        name, data_type = column.split(":")
        if data_type not in VALID_TYPES:
            raise ValueError(f"Недопустимое значение {data_type}")

    columns.insert(0, "ID:int")
    metadata[table_name] = {"columns": columns}

    return metadata


@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise ValueError("Таблицы с таким именем не существует")

    filepath = f"data/{table_name}.json"

    if os.path.exists(filepath):
        os.remove(filepath)

    del metadata[table_name]

    return metadata


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata:
        raise ValueError("Таблицы с таким именем не существует")

    columns = metadata[table_name]["columns"][1:]

    if len(values) != len(columns):
        raise ValueError("Некорректное количество значений")

    row = {}

    for column, value in zip(columns, values):
        name, data_type = column.split(":")

        if data_type == "int" and (
            not isinstance(value, int) or isinstance(value, bool)
        ):
            raise ValueError(f"Значение {name} должно быть int")
        elif data_type == "str" and not isinstance(value, str):
            raise ValueError(f"Значение {name} должно быть str")
        elif data_type == "bool" and not isinstance(value, bool):
            raise ValueError(f"Значение {name} должно быть bool")

        row[name] = value

    data = load_table_data(table_name)
    row["ID"] = max((item["ID"] for item in data), default=0) + 1
    data.append(row)

    save_table_data(table_name, data)

    return data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    key = (repr(table_data), repr(where_clause))

    return cache_result(
        key,
        lambda: [
            row for row in table_data
            if where_clause is None
            or all(
                row.get(column) == value
                for column, value in where_clause.items()
            )
        ],
    )


@handle_db_errors
def update(table_data, set_clause, where_clause):
    for row in table_data:
        if all(row.get(key) == value for key, value in where_clause.items()):
            row.update(set_clause)

    return table_data


@confirm_action("удаление записей")
@handle_db_errors
def delete(table_data, where_clause):
    return [
        row for row in table_data
        if not all(
            row.get(key) == value
            for key, value in where_clause.items()
        )
    ]