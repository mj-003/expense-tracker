def validate_money(P):
    """

    Validator for money input.
    Money input must be a number with at most 5 digits before the decimal
    point and at most 2 digits after the decimal point.

    :param P: P is the value to validate
    :return: True if the value is valid, False otherwise

    """
    if P == "":
        return True
    try:
        value = float(P)
        if len(P.split('.')[0]) > 5:
            return False
        if '.' in P and len(P.split('.')[1]) > 2:
            return False
        return True
    except ValueError:
        return False


def validate_more_info(action, value_if_allowed):
    """

    Validate the more info input.
    More info input must be a string with at most 100 characters.

    :param action: action is the action to perform
    :param value_if_allowed: value_if_allowed is the value to validate
    :return: True if the value is valid, False otherwise

    """
    if action == '1':  # Insert
        if value_if_allowed.isdigit():
            return True
        else:
            return False
    elif action == '0':  # Delete
        return True
    else:
        return False
