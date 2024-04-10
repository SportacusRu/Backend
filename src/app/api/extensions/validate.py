from re import match
from typing import MutableSet

from src.app.config.config import PLACES_FILTERS, PLACE_CATEGORIES

EMAIL_REGEXP = ("(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:["
                "\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\["
                "\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:["
                "a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|["
                "01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\["
                "\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])")


def validate_password(password: str) -> bool:
    length = len(password)
    return 4 <= length <= 100


def validate_email(email: str) -> bool: 
    return match(EMAIL_REGEXP, email) is not None


def validate_name(name: str) -> bool:
    length = len(name)
    return 4 <= length <= 24


def validate_place_title(text: str) -> bool:
    length = len(text)
    return 4 <= length <= 100


def validate_place_filters(filters: MutableSet[str]) -> bool:
    for currentFilter in filters:
        if not (currentFilter in PLACES_FILTERS):
            return False
    return True


def validate_place_category(category: str) -> bool:
    if not (category in PLACE_CATEGORIES):
        return False
    return True


def validate_review_text(text: str) -> bool:
    length = len(text)
    return 4 <= length <= 100


def validate_complaint_text(text: str) -> bool:
    length = len(text)
    return 4 <= length <= 100