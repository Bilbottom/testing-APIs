
DROP TABLE IF EXISTS company_officers;
CREATE TABLE company_officers(
    officer_id TEXT NOT NULL /*PRIMARY KEY*/,
    company_number TEXT NOT NULL REFERENCES company_profiles(company_number),

    name TEXT,
    occupation TEXT,
    officer_role TEXT,
    responsibilities TEXT,
    nationality TEXT,
    country_of_residence TEXT,
    date_of_birth_year INTEGER,
    date_of_birth_month INTEGER,
    resigned_on TEXT,
    is_pre_1992_appointment TEXT,  /* BOOL */
--     former_names TEXT,  /* LIST */

    name_elements_title TEXT,
    name_elements_forename TEXT,
    name_elements_surname TEXT,
    name_elements_honours TEXT,
    name_elements_other_forenames TEXT,

    contact_details_contact_name TEXT,

    appointed_on TEXT,
    appointed_before TEXT,
    appointed_to_company_name TEXT,
    appointed_to_company_number TEXT,
    appointed_to_company_status TEXT,

    address_address_line_1 TEXT,
    address_address_line_2 TEXT,
    address_care_of TEXT,
    address_country TEXT,
    address_locality TEXT,
    address_po_box TEXT,
    address_postal_code TEXT,
    address_premises TEXT,
    address_region TEXT,

    identification_identification_type TEXT,
    identification_legal_authority TEXT,
    identification_legal_form TEXT,
    identification_place_registered TEXT,
    identification_registration_number TEXT,

    principal_office_address_address_line_1 TEXT,
    principal_office_address_address_line_2 TEXT,
    principal_office_address_care_of TEXT,
    principal_office_address_country TEXT,
    principal_office_address_locality TEXT,
    principal_office_address_po_box TEXT,
    principal_office_address_postal_code TEXT,
    principal_office_address_premises TEXT,
    principal_office_address_region TEXT,

    links_self TEXT,
    links_company TEXT,
    links_officer_appointments TEXT
)
;
