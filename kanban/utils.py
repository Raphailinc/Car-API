import random
import re
import string


VIN_TEMPLATE = "WDDUJ76X09A000000"


def generate_vin(template: str = VIN_TEMPLATE) -> str:
    def replace_char(match):
        char = match.group(0)
        if char.isalpha():
            return random.choice(string.ascii_uppercase)
        if char.isdigit():
            return str(random.randint(0, 9))
        return char

    vin = re.sub(r"[A-Z0-9]", replace_char, template)
    return vin[:17]
