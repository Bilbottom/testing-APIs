"""
API clients for Companies House.

Note that the authentication is controlled by setting up an application
in Companies House.
"""

import os
from base64 import b64encode
from typing import Any

import requests
import dotenv

from src.apis.companies_house import model

dotenv.load_dotenv()


def _build_query_parameters(**kwargs) -> str:
    """
    Parse the key-value arguments into a parameter string.

    Omits the parameters with a ``None`` or null-string value.
    """

    def format_parameter(parm: Any) -> str:
        return str(parm).lower() if isinstance(parm, bool) else parm

    query_parameters = "&".join(
        [
            f"{key}={format_parameter(value)}" if value else ""
            for key, value in kwargs.items()
        ]
    )
    return f"?{query_parameters}" if query_parameters else ""


class CompaniesHouseConnector:
    def __init__(self):
        self.base_url = "https://api.company-information.service.gov.uk/"
        self.__api_key = os.environ["COMPANIES_HOUSE_API_KEY"]

    @property
    def auth_basic(self) -> str:
        """
        Encode the key using HTTP basic authentication (RFC2617).

        https://developer-specs.company-information.service.gov.uk/guides/authorisation
        """
        return "Basic " + b64encode(f"{self.__api_key}:".encode("UTF-8")).decode()

    @property
    def request_headers(self) -> dict:
        """
        Default request headers.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self.auth_basic,
        }

    def get_company_registered_office_address(
        self,
        company_number: model.CompanyNumber,
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/registered-office-address/registered-office-address
        """
        endpoint = f"company/{company_number}/registered-office-address"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def get_company_profile(
        self,
        company_number: model.CompanyNumber,
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/company-profile/company-profile
        """
        endpoint = f"company/{company_number}"
        return requests.request(
            method="GET", url=self.base_url + endpoint, headers=self.request_headers
        )

    def get_company_officers(
        self,
        company_number: model.CompanyNumber,
        items_per_page: int = 35,
        register_type: model.OfficerRegisterType = "",
        register_view: bool = False,
        start_index: int = 0,
        order_by: model.OfficerOrderBy = "",
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/officers/list
        """
        parameters = _build_query_parameters(
            items_per_page=items_per_page,
            register_type=register_type,
            register_view=register_view,
            start_index=start_index,
            order_by=order_by,
        )
        endpoint = f"company/{company_number}/officers{parameters}"
        return requests.request(
            method="GET", url=self.base_url + endpoint, headers=self.request_headers
        )

    def search(
        self,
        q: str,
        items_per_page: int = 20,
        start_index: int = 0,
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/search
        """
        parameters = _build_query_parameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index,
        )
        endpoint = f"search{parameters}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def search_company(
        self,
        q: str,
        items_per_page: int = 20,
        start_index: int = 0,
        restrictions: str = "",
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/search/search-companies
        """
        parameters = _build_query_parameters(
            q=q,
            items_per_page=items_per_page,
            start_index=start_index,
            restrictions=restrictions,
        )
        endpoint = f"search/companies{parameters}"
        return requests.request(
            method="GET",
            url=self.base_url + endpoint,
            headers=self.request_headers,
        )

    def search_officers(
        self,
        q: str,
        items_per_page: int = 20,
        start_index: int = 0,
    ) -> requests.Response:
        """
        https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/search/search-officers
        """
        parameters = _build_query_parameters(
            q=q, items_per_page=items_per_page, start_index=start_index
        )
        endpoint = f"search/officers{parameters}"
        return requests.request(
            method="GET", url=self.base_url + endpoint, headers=self.request_headers
        )


def main() -> None:
    """
    Manually test the API client.
    """
    conn = CompaniesHouseConnector()
    company_number = model.CompanyNumber("7706156")

    # Check the headers
    # print(os.environ["COMPANIES_HOUSE_API_KEY"])
    # print(conn.request_headers)

    # Test the error message
    # model.CompanyNumber("BROKEN")

    # Test getting the company profile
    print(conn.get_company_profile(company_number).text)

    # Test getting the company officers
    print(conn.get_company_officers(company_number).text)

    # Test the company search
    print(conn.search_company(q="Allica", items_per_page=2).text)

    # Test the officer search
    print(conn.search_officers(q="John", items_per_page=2).text)

    # Test the search
    print(conn.search(q="John", items_per_page=10).text)


if __name__ == "__main__":
    main()
