import json

from .connector import CompaniesHouseConnector


class Company(object):
    def __init__(self, company_number: str or int, validate_company_number_on_init: bool = True):
        self._connector: CompaniesHouseConnector = CompaniesHouseConnector()
        self._company_number = company_number
        self._company_profile: dict or None = None
        self._company_officers: list[dict] or None = None

        if validate_company_number_on_init:
            self.set_company_number()

    def set_company_number(self):
        self._company_number = self.get_company_profile()['company_number']

    @property
    def company_number(self) -> str or int:
        return self._company_number

    def get_company_profile(self, force_update: bool = False, suppress_errors: bool = False) -> dict:
        """Get the profile of the company"""
        if force_update or self._company_profile is None:
            company_profile = self._connector.get_company_profile(
                company_number=self.company_number,
                suppress_company_error=suppress_errors
            )
            if not suppress_errors and company_profile.status_code == 404:
                raise ValueError(f'Company number {self.company_number} not found')
            self._company_profile = json.loads(company_profile.text)
        return self._company_profile

    def get_company_officers(
        self,
        force_update: bool = False,
        page_size: int = 100,
        suppress_errors: bool = False
    ) -> dict:
        """Enumerate through all pages to retrieve the full list of officers"""
        if force_update or self._company_officers is None:
            enumerated_items = 0
            self._company_officers = []
            total_items = json.loads(
                self._connector.get_company_officers(
                    company_number=self.company_number,
                    items_per_page=1,
                    suppress_company_error=suppress_errors
                ).text
            )['total_results']
            while enumerated_items < total_items:
                self._company_officers += json.loads(
                    self._connector.get_company_officers(
                        company_number=self.company_number,
                        items_per_page=page_size,
                        start_index=enumerated_items,
                        suppress_company_error=suppress_errors
                    ).text
                )['items']
                enumerated_items += page_size
            for officer in self._company_officers:
                appointments = officer['links']['officer']['appointments']
                # officer['id'] = appointments[10:-12]  # Not sure if it's always a specific position/length
                officer['officer_id'] = appointments.replace('/officers/', '').replace('/appointments', '')
        return self._company_officers
