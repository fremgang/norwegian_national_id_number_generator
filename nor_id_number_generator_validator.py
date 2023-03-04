# Jonas Thoresen, 2023
# With some understanding of the id number rules, you can easilly modify to take full id numbers as input and validate.
# You can even with minimal effort generate all possible numbers since 1899.
# This script takes all rules and math into concideration.
# https://github.com/fremgang/norwegian_national_id_number_generator/edit/master/nor_id_number_generator_validator.py
import random
import signal
import datetime


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Time is up!")


signal.signal(signal.SIGALRM, timeout_handler)


def generate_fnr(birthday, gender):
    if not isinstance(birthday, str) or len(birthday) != 6 or not birthday.isdigit():
        raise ValueError("Birthday must be a string of 6 digits (ddmmyy)")
    if gender.lower() not in ["male", "female"]:
        raise ValueError("Gender must be 'male' or 'female'")
    birth_year = int(birthday[4:6])
    if birth_year < 10:
        birth_year += 2000
    else:
        birth_year += 1900
    try:
        datetime.date(birth_year, int(birthday[2:4]), int(birthday[:2]))
    except ValueError:
        raise ValueError("Invalid date of birth")
    if gender.lower() == "male":
        if int(birthday[4:6]) < 40:
            individual_numbers = range(500, 750)
        else:
            individual_numbers = range(0, 500)
    elif gender.lower() == "female":
        if int(birthday[4:6]) < 40:
            individual_numbers = range(500, 1000, 2)
        else:
            individual_numbers = range(0, 500, 2)
    else:
        raise ValueError("Invalid gender provided")
    fnrs = []
    for individual_number in individual_numbers:
        individual_number_str = str(individual_number).zfill(3)
        fnr_without_check_digits = birthday + individual_number_str
        weight_factors_1 = [3, 7, 6, 1, 8, 9, 4, 5, 2, 1]
        weighted_sum = sum(int(digit) * weight_factors_1[i] for i, digit in enumerate(fnr_without_check_digits))
        check_digit_1 = 11 - (weighted_sum % 11)
        if check_digit_1 == 11:
            check_digit_1 = 0
        weight_factors_2 = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2, 1]
        weighted_sum = sum(int(digit) * weight_factors_2[i] for i, digit in enumerate(fnr_without_check_digits + str(check_digit_1)))
        check_digit_2 = 11 - (weighted_sum % 11)
        if check_digit_2 == 11:
            check_digit_2 = 0
        fnr = fnr_without_check_digits + str(check_digit_1) + str(check_digit_2)
        fnrs.append(fnr)
    return fnrs


def is_valid_fnr(fnr):
    """
    Check if the given fødselsnummer (Norwegian national identification number) is valid.

    Args:
        fnr (str): A string representing the fødselsnummer to be checked.

    Returns:
        bool: True if the fødselsnummer is valid, False otherwise.
    """
    if not isinstance(fnr, str) or len(fnr) != 11 or not fnr.isdigit():
        return False
    birth_date = fnr[:6]
    individual_number = fnr[6:9]
    weight_factors_1 = [3, 7, 6, 1, 8, 9, 4, 5, 2, 1]
    weighted_sum = sum(int(digit) * weight_factors_1[i] for i, digit in enumerate(birth_date + individual_number))
    check_digit_1 = 11 - (weighted_sum % 11)
    if check_digit_1 == 11:
        check_digit_1 = 0
    if int(fnr[9]) != check_digit_1:
        return False

    weight_factors_2 = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2, 1]
    weighted_sum = sum(int(digit) * weight_factors_2[i] for i, digit in enumerate(fnr))
    check_digit_2 = 11 - (weighted_sum % 11)
    if check_digit_2 == 11:
        check_digit_2 = 0
    if int(fnr[10]) != check_digit_2:
        return False

    return True


birthday = input("Birthday (ddmmyy): ") 
gender = input("Gender (male/female): ")
# Change the 2 lines above to avoid terminal inputs.
# Change from = input(", to =("ddmmyy"
# Change from input(", to =("male/female
fnrs = generate_fnr(birthday, gender)
for fnr in fnrs:
    if int(fnr[8]) % 2 == 0 and gender.lower() == "male":
        continue
    if int(fnr[8]) % 2 == 1 and gender.lower() == "female":
        continue
    print(fnr)

