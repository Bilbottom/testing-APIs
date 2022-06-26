import json

import pandas as pd

from utils import pprint, print_dict_types
from companies_house import CompaniesHouseConnector


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


class Company(object):
    def __init__(self, company_number: str or int):
        self._connector: CompaniesHouseConnector = CompaniesHouseConnector()
        self._company_number = company_number
        self._company_profile: dict or None = None
        self._company_officers: dict or None = None

    @property
    def company_number(self) -> str or int:
        return self._company_number

    @property
    def company_profile(self, force_update: bool = False) -> dict:
        if force_update or self._company_profile is None:
            self._company_profile = json.loads(
                self._connector.get_company_profile(company_number=self.company_number).text
            )
        return self._company_profile

    @property
    def company_officers(self, force_update: bool = False) -> dict:
        if force_update or self._company_officers is None:
            self._company_officers = json.loads(
                self._connector.get_company_officers(company_number=self.company_number).text
            )
        return self._company_officers


def test_get_company_profile_and_officers():
    """Sample method to get an idea of what properties to push into a database"""
    allica_bank = Company(company_number='07706156')
    company_profile = allica_bank.company_profile
    pprint(company_profile)
    # pprint(allica_bank.company_officers)

    print_dict_types(dictionary=company_profile)


if __name__ == '__main__':
    # test_companies_house_connector()
    test_get_company_profile_and_officers()
