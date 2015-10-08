def get_items_status(circulation_data):
    circulation_data = circulation_data or []
    total = 0
    available_now = 0
    restricted = 0
    on_hold = 0
    for_online = 0
    for circulation_data_item in circulation_data:
        total += 1

        restrictions = circulation_data_item.get('restrictions', '')
        if restrictions:
            restricted += 1

        is_available_now = bool(circulation_data_item.get('availableNow', ''))
        if is_available_now:
            available_now += 1

        if is_available_now and not restrictions:
            for_online += 1

        if bool(circulation_data_item.get('onHold', '')):
            on_hold += 1

    return {
        'total': total,
        'available_now': available_now,
        'restricted': restricted,
        'on_hold': on_hold,
        'for_online': for_online
    }


def group_by_locations(holdings):
    group = {}
    holdings = holdings or []
    for holding in holdings:
        nuce_code = holding.get('nucCode', '')
        if not nuce_code:
            continue
        nuce_code_data = {}

        local_location = holding.get('localLocation', '')
        if not local_location:
            continue

        local_location_data = {}
        nuce_code_data[local_location] = local_location_data

        call_number_data = {}
        call_number = holding.get('callNumber', '')

        if not call_number:
            continue

        local_location_data[call_number] = call_number_data

        circulation_data = holding.get('circulationData', [])
        call_number_data['circulation_data'] = circulation_data
        call_number_data['items_status'] = get_items_status(circulation_data)
        call_number_data['shelving_data'] = holding.get('shelvingData', '')

        group[nuce_code] = nuce_code_data
    return group
