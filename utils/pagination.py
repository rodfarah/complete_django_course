import math


def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):

    last_page = page_range[-1]

    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset
    elif stop_range > last_page:
        stop_range = last_page
        start_range = last_page - qty_pages

    pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': last_page,
        'start_range': start_range,
        'stop_range': stop_range,
        'page_one_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < last_page
    }
