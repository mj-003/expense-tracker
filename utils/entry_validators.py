def validate_money(P):
    """
    Validate money input
    :param P:
    :return:
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
    Validate more info input
    :param action:
    :param value_if_allowed:
    :return:
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
