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
