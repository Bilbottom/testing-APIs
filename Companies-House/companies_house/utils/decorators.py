"""
Custom decorators for working with the Companies House API
"""
from typing import Callable

import requests

from .exceptions import HTTPError


def http_request(func: Callable) -> Callable:
    """
    Decorator for HTTP response handling. Still a POC and not sure if this will stay

    TODO: Consider re-writing the connector class method calls so that the arguments are passed to this decorator
    """
    def http_handler(*args, **kwargs):
        ret: requests.Response = func(*args, **kwargs)
        print(ret.status_code)
        if ret.status_code in {400, 401, 404}:
            raise HTTPError(ret.status_code, ret.reason)
        return ret

    return http_handler
