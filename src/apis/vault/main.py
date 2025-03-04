"""
Manual testing for the API clients.
"""

import os

import dotenv

import src.utils
from src.apis import vault

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """
    vault_connector = vault.VaultConnector(
        domain=os.getenv("VAULT__DOMAIN"),
        api_key=os.getenv("VAULT__API_KEY"),
        api_secret=os.getenv("VAULT__API_SECRET"),
    )
    src.utils.pprint(vault_connector.list_roles().text)
    src.utils.pprint(vault_connector.list_connections().text)

    response = vault_connector.read_secret(role_name="dwh_billwallis")
    src.utils.pprint(response.text)


if __name__ == "__main__":
    main()
