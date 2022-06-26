"""
Class to facilitate working with the Companies House API
    * https://developer.company-information.service.gov.uk/
Note that the authentication is controlled by setting up an application in Companies House
"""
import os
import re
from base64 import b64encode
from typing import Any

import requests
from dotenv import load_dotenv

from company_house_utils.enums import OfficerRegisterType, OfficerOrderBy
from company_house_utils.exceptions import CompanyNumberValueError
# from company_house_utils.decorators import http_request

load_dotenv('.env')


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
        return 'Basic ' + b64encode(f'{self.__api_key}:'.encode('UTF-8')).decode()

    @property
    def request_headers(self) -> dict:
        """Set up the default headers into a dictionary"""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': self.auth_basic
        }

    # # @http_request
    # def http_request(self, method: str, endpoint: str, data: str or None = None):
    #     return requests.request(
    #         method=method,
    #         url=self.base_url + endpoint,
    #         headers=self.request_headers,
    #         data=data
    #     )

    @staticmethod
    def build_query_parameters(**kwargs):
        """
        Parse the key-word arguments into a parameter string.
        Omits the parameters with a None or null-string value
        """
        def format_parameter(parm: Any) -> str:
            """
            Parse the parameter arguments from Python types into string values for the API.
            This is a simple implementation, but wrapping it into its own method in case it gets more complicated.
            Currently, only boolean types are converted to their string representations and lower-cased
            """
            return str(parm).lower() if isinstance(parm, bool) else parm  # Str conversion will happen in the f'string
        query_parameters = '&'.join(
            [f"{key}={format_parameter(value)}" if value else '' for key, value in kwargs.items()]
        )
        return f'?{query_parameters}' if query_parameters else ''

    @staticmethod
    def is_valid_company_number(company_number: str or int) -> bool:
        """
        Check whether a company number is valid or not.
        This is currently a simple implementation, but wrapping it into its own method in case it gets more complicated.
        For example, the Scottish company number start with an SC
        """
        if isinstance(company_number, str):
            length = len(company_number)
            return length == 8 or (length < 8 and re.match(r'\D', company_number) is None)
        elif isinstance(company_number, int):
            return company_number > 0 and len(str(company_number)) <= 8
        else:
            return False

    @staticmethod
    def format_company_number(company_number: str or int) -> str:
        """
        Format a company number into something that the Companies House AIP recognises.
        This is currently a simple implementation, but wrapping it into its own method in case it gets more complicated.
        For example, the Scottish company number start with an SC
        """
        return str(company_number).zfill(8)

    def get_company_registered_office_address(
        self,
        company_number: str or int,
        suppress_company_error: bool = False
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/registered-office-address/registered-office-address
        """
        if not suppress_company_error and not self.is_valid_company_number(company_number):
            raise CompanyNumberValueError(company_number)

        endpoint = f'company/{self.format_company_number(company_number)}/registered-office-address'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    def get_company_profile(
        self,
        company_number: str or int,
        suppress_company_error: bool = False
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/company-profile/company-profile
        """
        if not suppress_company_error and not self.is_valid_company_number(company_number):
            raise CompanyNumberValueError(company_number)

        endpoint = f'company/{self.format_company_number(company_number)}'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    def get_company_officers(
        self,
        company_number: str or int,
        items_per_page: int = 35,
        register_type: OfficerRegisterType = '',
        register_view: bool = False,
        start_index: int = 0,
        order_by: OfficerOrderBy = '',
        suppress_company_error: bool = False
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/officers/list
        """
        if not suppress_company_error and not self.is_valid_company_number(company_number):
            raise CompanyNumberValueError(company_number)

        parameters = self.build_query_parameters(
            items_per_page=items_per_page,
            register_type=register_type,
            register_view=register_view,
            start_index=start_index,
            order_by=order_by
        )
        endpoint = f'company/{self.format_company_number(company_number)}/officers{parameters}'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    def search(self, q: str, items_per_page: int = 20, start_index: int = 0) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/search
        """
        parameters = self.build_query_parameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index
        )
        endpoint = f'search{parameters}'
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
        parameters = self.build_query_parameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index,
            restrictions=restrictions
        )
        endpoint = f'search/companies{parameters}'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )

    def search_officers(self, q: str, items_per_page: int = 20, start_index: int = 0) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/search/search-officers
        """
        parameters = self.build_query_parameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index
        )
        endpoint = f'search/officers{parameters}'
        return requests.request(
            method='GET',
            url=self.base_url + endpoint,
            headers=self.request_headers
        )
