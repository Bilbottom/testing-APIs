"""
Manual testing for the API clients.
"""

import src.utils
from src.apis import vault


def main() -> None:
    """
    Manually test the API client.
    """
    vault_connector = vault.VaultConnector()
    src.utils.pprint(vault_connector.list_roles().text)
    src.utils.pprint(vault_connector.list_connections().text)

    response = vault_connector.read_secret(role_name="dwh_billwallis")
    print(response)
    src.utils.pprint(response.text)


if __name__ == "__main__":
    main()
