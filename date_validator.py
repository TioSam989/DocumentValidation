import re
from dateutil.parser import parse

class DateValidator:
    """
    Validates and extracts dates from text or images.
    """

    @staticmethod
    def find_dates(text: str) -> list:
        """Finds potential date strings using regex."""
        date_pattern = r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b"
        return re.findall(date_pattern, text)

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validates a date string by attempting to parse it."""
        try:
            parse(date_str, dayfirst=True)  # Day-first format for compatibility with common date formats
            return True
        except ValueError:
            return False
