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