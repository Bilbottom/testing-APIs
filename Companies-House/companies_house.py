"""
Class to facilitate working with the Companies House API
    * https://developer.company-information.service.gov.uk/
Note that the authentication is controlled by setting up an application in Companies House
"""
import os
import base64

import requests
from dotenv import load_dotenv

load_dotenv('.env')


class CompanyNumberValueError(Exception):
    """
    Custom error class for Company Number value errors. Saves having to copy-and-paste the error text.
    https://www.seanh.cc/2019/06/20/python-custom-exception-classes/
    """
    def __init__(self, company_number):
        super().__init__(
            f'The company number must be exactly 8 characters long and include the leading 0.'
            f' The company number {company_number} is invalid'
        )


class CompaniesHouseConnector(object):
    def __init__(self):
        self.base_url = 'https://api.company-information.service.gov.uk/'
        self.__api_key = os.environ['API-Token']

    @property
    def auth_basic(self) -> str:
        """
        Encode the key following the Companies House documentation (HTTP basic authentication, RFC2617)
            https://developer-specs.company-information.service.gov.uk/guides/authorisation
        """
        return 'Basic ' + base64.b64encode(f'{self.__api_key}:'.encode('UTF-8')).decode()

    @property
    def request_headers(self) -> dict:
        """Set up the default headers into a dictionary"""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.auth_basic
        }

    @staticmethod
    def format_company_number(company_number: str or int) -> str:
        """
        Format a company number into something that the Companies House AIP recognises.
        This is currently a simple implementation, but wrapping it into its own method in case it gets more complicated.
        For example, the Scottish company number start with an SC
        """
        return str(company_number).zfill(8)

    def get_company_profile(self, company_number: str or int, suppress_error: bool = False) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/company-profile/company-profile
        """
        if not suppress_error and len(company_number) != 8:
            raise CompanyNumberValueError(company_number)

        endpoint = f'company/{self.format_company_number(company_number)}'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    def get_company_officers(self, company_number: str or int, suppress_error: bool = False) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/officers/list
        """
        if not suppress_error and len(company_number) != 8:
            raise CompanyNumberValueError(company_number)

        endpoint = f'company/{self.format_company_number(company_number)}/officers'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    def search(self, q: str, items_per_page: int = 20, start_index: int = 0) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/search
        """
        endpoint = f'search?{q=}&{items_per_page=}&{start_index=}'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    def search_company(
        self,
        q: str,
        items_per_page: int = 20,
        start_index: int = 0,
        restrictions: str = ''
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/search/search-companies
        """
        endpoint = f'search/companies?{q=}&{items_per_page=}&{start_index=}&{restrictions=}'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    def search_officers(self, q: str, items_per_page: int = 20, start_index: int = 0) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/search/search-officers
        """
        endpoint = f'search/officers?{q=}&{items_per_page=}&{start_index=}'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )
