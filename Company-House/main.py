import json

from company_house import CompanyHouseConnector


def pprint(json_text: str or dict):
    if type(json_text) is str:
        json_text = json.loads(json_text)

    try:
        print(
            json.dumps(
                json_text,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
        )
    except TypeError:
        print(json_text)


def test_company_house_connector():
    ch_conn = CompanyHouseConnector()

    # Test the error message
    # pprint(ch_conn.get_company_profile(company_number='2933452').text)

    # Test 2 ways of getting the company profile
    pprint(ch_conn.get_company_profile(company_number='02933452').text)
    pprint(ch_conn.get_company_profile(company_number=2933452, suppress_error=True).text)

    # Test getting the company officers
    pprint(ch_conn.get_company_officers(company_number=2933452, suppress_error=True).text)

    # Test the company search
    pprint(ch_conn.search_company(q='Allica', items_per_page=2).text)

    # Test the officer search
    pprint(ch_conn.search_officers(q='John', items_per_page=2).text)

    # Test the search
    pprint(ch_conn.search(q='John', items_per_page=10).text)


if __name__ == '__main__':
    test_company_house_connector()
