from decimal import Decimal
import re

# Helper function to convert price string to Decimal


def parse_price(price_str):
    # Remove any non-numeric characters except for the decimal point
    price_num = re.sub(r"[^\d.]", "", price_str)
    try:
        return Decimal(price_num)
    except ValueError:
        return Decimal('0')
