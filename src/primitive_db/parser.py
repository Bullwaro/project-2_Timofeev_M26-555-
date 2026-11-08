def parse_clause(condition):
    key, value = condition.split("=", 1)
    value = value.strip()

    if value.isdigit():
        value = int(value)
    elif value.lower() in ("true", "false"):
        value = value.lower() == "true"

    return {key.strip(): value}