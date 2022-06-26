
DROP TABLE IF EXISTS company_profiles;
CREATE TABLE company_profiles(
    company_number TEXT NOT NULL PRIMARY KEY,
    company_name TEXT,
    etag TEXT,
    type TEXT,
    status TEXT,
    company_status TEXT,
    company_status_detail TEXT,
    jurisdiction TEXT,
    last_full_members_list_date TEXT,
    date_of_creation TEXT,
    date_of_cessation TEXT,
    can_file INTEGER,  /* BOOL */
    has_been_liquidated INTEGER,  /* BOOL */
    has_insolvency_history INTEGER,  /* BOOL */
    has_charges INTEGER,  /* BOOL */
    has_super_secure_pscs INTEGER,  /* BOOL */
    undeliverable_registered_office_address INTEGER,  /* BOOL */
    registered_office_is_in_dispute INTEGER,  /* BOOL */
    is_community_interest_company INTEGER,  /* BOOL */
    -- sic_codes TEXT,  /* LIST */
    -- previous_company_names TEXT,  /* LIST */

    annual_return_overdue INTEGER,  /* BOOL */
    annual_return_next_due TEXT,
    annual_return_last_made_up_to TEXT,
    annual_return_next_made_up_to TEXT,

    accounts_next_due TEXT,
    accounts_next_made_up_to TEXT,
    accounts_overdue INTEGER,  /* BOOL */
    accounts_accounting_reference_date_day TEXT,
    accounts_accounting_reference_date_month TEXT,
    accounts_last_accounts_type TEXT,
    accounts_last_accounts_made_up_to TEXT,
    accounts_last_accounts_period_start_on TEXT,
    accounts_last_accounts_period_end_on TEXT,
    accounts_next_accounts_overdue INTEGER,  /* BOOL */
    accounts_next_accounts_due_on TEXT,
    accounts_next_accounts_period_start_on TEXT,
    accounts_next_accounts_period_end_on TEXT,

    registered_office_address_address_line_1 TEXT,
    registered_office_address_address_line_2 TEXT,
    registered_office_address_care_of TEXT,
    registered_office_address_country TEXT,
    registered_office_address_locality TEXT,
    registered_office_address_po_box TEXT,
    registered_office_address_postal_code TEXT,
    registered_office_address_premises TEXT,
    registered_office_address_region TEXT,

    service_address_address_line_1 TEXT,
    service_address_address_line_2 TEXT,
    service_address_care_of TEXT,
    service_address_country TEXT,
    service_address_locality TEXT,
    service_address_po_box TEXT,
    service_address_postal_code TEXT,
    service_address_premises TEXT,
    service_address_region TEXT,

    confirmation_statement_overdue INTEGER,  /* BOOL */
    confirmation_statement_next_due TEXT,
    confirmation_statement_last_made_up_to TEXT,
    confirmation_statement_next_made_up_to TEXT,

    branch_company_details_business_activity TEXT,
    branch_company_details_parent_company_name TEXT,
    branch_company_details_parent_company_number TEXT,

--     foreign_company_details BLOB,

    links_self TEXT,
    links_officers TEXT,
    links_registers TEXT,
    links_filing_history TEXT,
    links_persons_with_significant_control TEXT,
    links_persons_with_significant_control_statements TEXT
)
;
