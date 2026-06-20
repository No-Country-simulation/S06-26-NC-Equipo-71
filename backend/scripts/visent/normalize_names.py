from unidecode import unidecode


def normalize_code(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "" or value.lower() == "nan":
        return None

    return unidecode(value).upper()


def normalize_cluster(value):
    return normalize_code(value)


def normalize_municipality(value):
    return normalize_code(value)