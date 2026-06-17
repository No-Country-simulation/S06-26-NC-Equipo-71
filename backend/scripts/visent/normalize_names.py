from unidecode import unidecode


def normalize_text(value):
    if value is None:
        return None

    return unidecode(str(value).strip())


def normalize_cluster(value):
    if value is None:
        return None

    return unidecode(str(value).strip().upper())