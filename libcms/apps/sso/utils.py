# coding=utf-8
def normalize_fio(fio):
    """
    "иванов - петров Иван Иваныч" -> "Иванов-Петров Иван Иваныч"
    :param fio: ФИО
    :return: нормализованное имя
    """
    cleaned_fio = fio.strip().lower()
    fio_parts = []
    for fio_part in cleaned_fio.split(' '):
        if fio_part == ' ' or not fio_part:
            continue
        fio_parts.append(fio_part[0].upper() + fio_part[1:])

    cleaned_fio = u' '.join(fio_parts)
    fio_parts = []

    for fio_part in cleaned_fio.split('-'):
        if fio_part == ' ' or not fio_part:
            continue
        fio_parts.append((fio_part[0].upper() + fio_part[1:]).strip())

    cleaned_fio = u'-'.join(fio_parts)
    return cleaned_fio
