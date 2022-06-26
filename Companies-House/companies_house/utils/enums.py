"""
Custom enums for working with the Companies House API
"""
from enum import Enum


class OfficerRegisterType(Enum):
    DIRECTORS = 'directors'
    SECRETARIES = 'secretaries'
    LLP_MEMBERS = 'llp-members'


class OfficerOrderBy(Enum):
    APPOINTED_ON = 'appointed_on'
    RESIGNED_ON = 'resigned_on'
    SURNAME = 'surname'
