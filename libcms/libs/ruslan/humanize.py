def get_records(sru_response):
    return sru_response.get('records', {}).get('record', [])


def get_record_content(sru_record):
    return sru_record.get('recordData', {}).get('content', [{}])[0]


def get_bib_record_from_opac(opac_record):
    return opac_record.get('record', {}).get('bibliographicRecord', {}).get('record', {})


def get_holdings_data_from_opac(opac_record):
    return opac_record.get('record', {}).get('holdingsData', [])


def grs_to_dict(fields=None):
    fields = fields or []
    grs_dict = {}
    for field in fields:
        value = field.get('value', '')
        if not value: continue
        exist_field = grs_dict.get(value, [])
        if not exist_field:
            grs_dict[value] = exist_field
        exist_field.append(field)
    return grs_dict
