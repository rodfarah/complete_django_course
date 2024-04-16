from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        # Current page = 1
        # Qty Page = 4
        # Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

        # Current page = 2
        # Qty Page = 4
        # Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

        # Current page = 3
        # Qty Page = 4
        # Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )
        self.assertEqual([2, 3, 4, 5], pagination['pagination'])

        # Current page = 4
        # Qty Page = 4
        # Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )
        self.assertEqual([3, 4, 5, 6], pagination['pagination'])

    def test_make_sure_middle_ranges_are_correct(self):
        # Current page = 10
        # Qty Page = 4
        # Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )
        self.assertEqual([9, 10, 11, 12], pagination['pagination'])

        # Current page = 12
        # Qty Page = 4
        # Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )
        self.assertEqual([11, 12, 13, 14], pagination['pagination'])

    def test_high_ranges_stop_list_spinning(self):
        # Current page = 18
        # Qty Page = 4
        # Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])

        # Current page = 19
        # Qty Page = 4
        # Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])

        # Current page = 20
        # Qty Page = 4
        # Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])

    def test_higher_qty_pages_vs_lower_and_higher_current_page(self):
        # Current page = 1
        # Qty Page = 8
        # Middle Page = 4
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=8,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], pagination['pagination'])

        # Current page = 5
        # Qty Page = 8
        # Middle Page = 4
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=8,
            current_page=5,
        )
        self.assertEqual([2, 3, 4, 5, 6, 7, 8, 9], pagination['pagination'])

        # Current page = 19
        # Qty Page = 8
        # Middle Page = 4
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=8,
            current_page=19,
        )
        self.assertEqual(
            [13, 14, 15, 16, 17, 18, 19, 20],
            pagination['pagination'])
