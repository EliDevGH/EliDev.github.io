import re

def validate_credit_card_number(card_number):
    pattern = r'^([4-6]\d{3})(-?\d{4}){3}$'
    if re.match(pattern, card_number):
        card_number = card_number.replace('-', '')
        for i in range(0, len(card_number) - 3):
            if card_number[i] == card_number[i + 1] == card_number[i + 2] == card_number[i + 3]:
                return False
        return True
    return False

# Test cases
card_numbers = [
    '4123456789123456',
    '5123-4567-8912-3456',
    '61234-567-8912-3456',
    '4123356789123456',
    '5133-3367-8912-3456',
    '5123 - 3567 - 8912 - 3456'
]

for card_number in card_numbers:
    if validate_credit_card_number(card_number):
        print(f"{card_number} is a valid credit card number.")
    else:
        print(f"{card_number} is not a valid credit card number.")
#  Credit Card Validator
# This implementation uses 
# regular expressions to match the pattern of a valid credit card number. 
# It checks for the following conditions:


# The number starts with 4, 5, or 6.
# It consists of groups of four digits separated by a hyphen (-) or no separator.
# It does not have four or more consecutive repeated digits.
# The validate_credit_card_number function returns True if the card number is valid and False otherwise.