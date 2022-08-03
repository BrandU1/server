from rest_framework.pagination import PageNumberPagination


class XSmallResultsSetPagination(PageNumberPagination):
    page_size = 10


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 30
