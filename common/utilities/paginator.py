from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response


class ClassteacherPagingSerializer(pagination.PageNumberPagination):
    """
    This is a custom paginator for the EMR Project
    It contains metadata that should be accessible at both the API and frontend
    And consequently used to manipulate pagination actions for the all list
    views
    """

    page_size_query_param = 'page_size'
    max_page_size = 15000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_size', self.page.paginator.per_page),
            ('current_page', self.page.number),
            ('total_pages', self.page.paginator.num_pages),
            ('start_index', self.page.start_index()),
            ('end_index', self.page.end_index()),
            ('results', data)
        ]))
