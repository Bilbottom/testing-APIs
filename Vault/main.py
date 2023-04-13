"""
Testing the ``VaultConnector`` class defined in ``vault.py``.
"""
from vault import VaultConnector
from utils import pprint


def main() -> None:
    """
    Test the ``VaultConnector`` class.
    """
    vault_connector = VaultConnector()
    # pprint(vault_connector.list_roles().text)
    # pprint(vault_connector.list_connections().text)
    response = vault_connector.read_secret(role_name="dwh_billwallis")
    print(response)
    pprint(response.text)


if __name__ == "__main__":
    main()
