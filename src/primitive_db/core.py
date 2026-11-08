from .utils import load_table_data, save_table_data

def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError("Таблица с таким именем уже существует")

    valid_types = ("int", "str", "bool")

    for column in columns:
        name, data_type = column.split(":")
        if data_type not in valid_types:
            raise ValueError("Некорректный ввод")

    columns.insert(0, "ID:int")
    metadata[table_name] = {"columns": columns}

    return metadata

def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise ValueError("Таблицы с таким именем не существует")

    del metadata[table_name]

    return metadata

def insert(metadata, table_name, values):
    if table_name not in metadata:
        raise ValueError("Table does not exist")

    columns = metadata[table_name]["columns"][1:]

    if len(values) != len(columns):
        raise ValueError("Invalid number of values")

    row = {}

    for column, value in zip(columns, values):
        name, data_type = column.split(":")

        if data_type == "int" and not isinstance(value, int):
            raise ValueError(f"{name} must be int")
        elif data_type == "str" and not isinstance(value, str):
            raise ValueError(f"{name} must be str")
        elif data_type == "bool" and not isinstance(value, bool):
            raise ValueError(f"{name} must be bool")

        row[name] = value

    data = load_table_data(table_name)
    row["ID"] = max((item["ID"] for item in data), default=0) + 1
    data.append(row)

    save_table_data(table_name, data)

    return data


def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    return [
        row for row in table_data
        if all(row.get(key) == value for key, value in where_clause.items())
    ]


def update(table_data, set_clause, where_clause):
    for row in table_data:
        if all(row.get(key) == value for key, value in where_clause.items()):
            row.update(set_clause)

    return table_data


def delete(table_data, where_clause):
    return [
        row for row in table_data
        if not all(row.get(key) == value for key, value in where_clause.items())
    ]