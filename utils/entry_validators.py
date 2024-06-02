def validate_money(P):
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
    if action == '1':  # Insert
        if value_if_allowed.isdigit():
            return True
        else:
            return False
    elif action == '0':  # Delete
        return True
    else:
        return False
