import math


def make_pagination_range(
    page_range,  # 1 - 20
    qty_pages,  # 4
    current_page,  # 19
):

    last_page = page_range[-1]  # 20

    middle_range = math.ceil(qty_pages / 2)  # 2
    start_range = current_page - middle_range  # 17
    stop_range = current_page + middle_range  # 21

    start_range_offset = abs(start_range) if start_range < 0 else 0  # 0

    if start_range < 0:  # False
        start_range = 0
        stop_range += start_range_offset
    elif stop_range > last_page:  # True
        stop_range = last_page
        start_range = last_page - qty_pages
    return page_range[start_range:stop_range]
