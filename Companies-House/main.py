import contextlib
import sqlite3  # https://stackoverflow.com/a/14432914/8213085

import pandas as pd

from companies_house import Company


def test_get_company_profile_and_officers():
    """Sample method to get an idea of what properties to push into a database"""
    disallowed_company_properties = ['previous_company_names', 'sic_codes', 'foreign_company_details']
    disallowed_officer_properties = ['former_names']
    db_conn = sqlite3.connect('companies-house.db')
    allica_bank = None

    try:
        allica_bank = Company(company_number=7706156, validate_company_number_on_init=True)
    except ValueError:
        print('Exiting...')
        exit()  # When wrapping this into a for-loop, this should just be the loop exit

    # pprint(allica_bank.get_company_profile())
    # pprint(allica_bank.get_company_officers()[0])

    company_profile_json = allica_bank.get_company_profile(suppress_errors=True)
    company_officers_json = allica_bank.get_company_officers(suppress_errors=True)
    with contextlib.suppress(KeyError):
        [company_profile_json.pop(key) for key in disallowed_company_properties]
        [company_officers_json.pop(key) for key in disallowed_officer_properties]

    company_profile = pd.json_normalize(company_profile_json).rename(columns=lambda c: c.replace('.', '_'))
    company_officers = pd.json_normalize(company_officers_json).rename(columns=lambda c: c.replace('.', '_'))
    company_officers.loc[:, 'company_number'] = allica_bank.company_number

    # print(company_profile.transpose())
    # print(company_officers.transpose())

    with contextlib.suppress(sqlite3.IntegrityError):
        company_profile.to_sql(name='company_profiles', con=db_conn, index=False, if_exists='append')
        company_officers.to_sql(name='company_officers', con=db_conn, index=False, if_exists='append')


if __name__ == '__main__':
    test_get_company_profile_and_officers()
