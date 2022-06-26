import json

from rich import print


def pprint(json_text: str or dict, indent: int = 4):
    """Pretty print JSON/dict objects"""
    if type(json_text) is str:
        json_text = json.loads(json_text)

    try:
        print(
            json.dumps(
                json_text,
                sort_keys=True,
                indent=indent,
                separators=(',', ': ')
            )
        )
    except TypeError:
        print(json_text)


def print_dict_types(dictionary: dict, level: int = 0) -> None:
    """Loop through a dict and print the keys and the value types. List keys will be coloured red"""
    indent = level * '    '
    for key, value in dictionary.items():
        colour = 'red' if isinstance(value, list) else 'blue'
        print(f"{indent}{key} [italic {colour}]{type(value)}[/italic {colour}]")
        if isinstance(value, dict):
            print_dict_types(value, level=level + 1)
