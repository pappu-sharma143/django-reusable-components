from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response
from collections import OrderedDict


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class with 20 items per page.
    
    Usage:
        ?page=1
        ?page=2&page_size=50
    """
    
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('results', data)
        ]))


class LargeResultsSetPagination(PageNumberPagination):
    """
    Pagination class for large datasets with 100 items per page.
    
    Usage:
        ?page=1
        ?page=2&page_size=200
    """
    
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('results', data)
        ]))


class SmallResultsSetPagination(PageNumberPagination):
    """
    Pagination class for small datasets with 10 items per page.
    
    Usage:
        ?page=1
        ?page=2&page_size=20
    """
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('results', data)
        ]))


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Limit/Offset pagination for more flexible pagination.
    
    Usage:
        ?limit=20&offset=0
        ?limit=50&offset=100
    """
    
    default_limit = 20
    max_limit = 100
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('limit', self.limit),
            ('offset', self.offset),
            ('results', data)
        ]))


class CustomCursorPagination(CursorPagination):
    """
    Cursor-based pagination for efficient pagination of large datasets.
    Best for real-time data or when you need consistent pagination.
    
    Usage:
        ?cursor=cD0yMDIx...
    """
    
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = '-created_at'  # Default ordering
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class InfinitePagination(PageNumberPagination):
    """
    Pagination for infinite scroll implementations.
    Returns has_more instead of next/previous links.
    
    Usage:
        ?page=1
        ?page=2
    """
    
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('has_more', self.page.has_next()),
            ('current_page', self.page.number),
            ('results', data)
        ]))
