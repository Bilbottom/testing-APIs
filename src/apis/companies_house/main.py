import contextlib
import json
import pathlib

from src.apis import companies_house

HERE = pathlib.Path(__file__).parent


def _write_json(data: dict, filename: str) -> None:
    (HERE / filename).write_text(json.dumps(data), encoding="utf-8")


def get_company_profile_and_officers():
    """
    Sample method to get an idea of what properties to push into a database.
    """
    disallowed_company_properties = [
        "previous_company_names",
        "sic_codes",
        "foreign_company_details",
    ]
    disallowed_officer_properties = ["former_names"]

    try:
        ch_conn = companies_house.CompaniesHouseConnector()
        company_number = companies_house.CompanyNumber(7706156)
        allica_bank = companies_house.Company(
            companies_house_connector=ch_conn,
            company_number=company_number,
        )
    except ValueError:
        quit(1)

    company_profile_json = allica_bank.get_company_profile()
    company_officers_json = allica_bank.get_company_officers()
    with contextlib.suppress(KeyError):
        [company_profile_json.pop(key) for key in disallowed_company_properties]
        [company_officers_json.pop(key) for key in disallowed_officer_properties]

    _write_json(company_profile_json, f"data/{company_number}-profile.json")
    _write_json(company_officers_json, f"data/{company_number}-officers.json")


if __name__ == "__main__":
    get_company_profile_and_officers()
