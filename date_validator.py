"""
date_validator.py
Valida e extrai datas com regex e dateutil (opcional).
"""
import re
from dateutil.parser import parse

class DateValidator:

    @staticmethod
    def find_dates(text: str) -> list:
        # Regex simples para capturar datas no formato DD/MM/YYYY, etc.
        pattern = r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b"
        return re.findall(pattern, text)

    @staticmethod
    def validate_date(date_str: str) -> bool:
        try:
            parse(date_str, dayfirst=True)
            return True
        except ValueError:
            return False
