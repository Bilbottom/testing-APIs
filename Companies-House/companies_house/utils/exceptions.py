"""
Custom exception classes for working with the Companies House API
"""


class CompanyNumberValueError(Exception):
    """
    Custom error class for Company Number value errors. Saves having to copy-and-paste the error text.
    https://www.seanh.cc/2019/06/20/python-custom-exception-classes/
    """
    def __init__(self, company_number: str or int):
        super().__init__(
            f'The company number must be exactly 8 characters long and include the leading 0.'
            f' The company number {company_number} is invalid'
        )


class HTTPError(Exception):
    """Custom error class for HTTP errors. Saves having to copy-and-paste the error text"""
    def __init__(self, status_code: int, reason: str):
        super().__init__(f'Bad HTTP request: [{status_code}] {reason}')
