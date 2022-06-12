"""
Testing the ConfluenceConnector class defined in confluence.py
"""
import json

from confluence import ConfluenceConnector


def pprint(json_text: str or dict):
    if type(json_text) is str:
        json_text = json.loads(json_text)

    print(
        json.dumps(
            json_text,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    )


def get_space_details():
    billwallis_id = '5f60829fcc17bd006f03f1fd'
    billwallis_space_id = '977666054'
    analytics_space_id = '1185742862'


def main():
    confluence_connector = ConfluenceConnector()

    pprint(confluence_connector.get_spaces().text)
    pprint(confluence_connector.search_content_by_cql(
        cql='(space=AO AND type=page AND creator.fullname~"Bill")&limit=500'
    ).text)


if __name__ == '__main__':
    main()
