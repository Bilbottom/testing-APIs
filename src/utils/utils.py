import json

from rich import print


def pprint(text: str | dict, indent: int = 4) -> None:
    """
    Pretty print JSON/dict objects.
    """

    if isinstance(text, str):
        text = json.loads(text)

    try:
        print(
            json.dumps(
                text,
                sort_keys=True,
                indent=indent,
                separators=(",", ": "),
            )
        )
    except TypeError:
        print(text)


def print_dict_types(dictionary: dict, level: int = 0) -> None:
    """
    Loop through a dict and print the keys and the value types.

    List keys will be coloured red.
    """
    indent = level * "    "
    for key, value in dictionary.items():
        colour = "red" if isinstance(value, list) else "blue"
        print(f"{indent}{key} [italic {colour}]{type(value)}[/italic {colour}]")
        if isinstance(value, dict):
            print_dict_types(value, level=level + 1)


def _json_schema_to_sql() -> None:
    """
    Loop through a dict and convert to SQL column names with types.
    """

    def printer(dictionary: dict, parent: str or None = None) -> None:
        for key, value in dictionary.items():
            if isinstance(value, dict):
                printer(value, parent=key)
            else:
                print(
                    f"{key if parent is None else f'{parent}_{key}'} {sql_type[type(value)]},"
                )

    sql_type = {
        str: "TEXT",
        list: "TEXT",
        dict: "BLOB",
        int: "INTEGER",
        bool: "INTEGER  /* BOOL */",
        float: "REAL",
    }
    with open("temp.json") as f:
        printer(json.loads(f.read()))
