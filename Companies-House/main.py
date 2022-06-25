import json

from companies_house import CompaniesHouseConnector


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


def test_companies_house_connector():
    """Test the Companies House connector class"""
    ch_conn = CompaniesHouseConnector()

    # Test the error message
    pprint(ch_conn.get_company_profile(company_number='7706156').text)

    # Test 2 ways of getting the company profile
    pprint(ch_conn.get_company_profile(company_number='07706156').text)
    pprint(ch_conn.get_company_profile(company_number=7706156, suppress_error=True).text)

    # Test getting the company officers
    pprint(ch_conn.get_company_officers(company_number=7706156, suppress_error=True).text)

    # Test the company search
    pprint(ch_conn.search_company(q='Allica', items_per_page=2).text)

    # Test the officer search
    # pprint(ch_conn.search_officers(q='John', items_per_page=2).text)

    # Test the search
    # pprint(ch_conn.search(q='John', items_per_page=10).text)


def test_get_company_profile_and_officers():
    """Sample method to get an idea of what properties to push into a database"""
    allica_bank = '07706156'
    ch_conn = CompaniesHouseConnector()
    profile = ch_conn.get_company_profile(company_number=allica_bank).text
    officers = ch_conn.get_company_officers(company_number=allica_bank).text

    pprint(profile)
    pprint(officers)


if __name__ == '__main__':
    # test_companies_house_connector()
    test_get_company_profile_and_officers()
