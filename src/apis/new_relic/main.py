"""
Manual testing for the API clients.
"""

import os

import dotenv

from src.apis import new_relic

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """
    new_relic_connector = new_relic.NewRelicConnector(
        account_id=os.getenv("NEW_RELIC__ACCOUNT_ID"),
        api_key=os.getenv("NEW_RELIC__API_KEY"),
    )
    print(new_relic_connector)


if __name__ == "__main__":
    main()
