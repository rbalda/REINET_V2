from rest_framework.pagination import PageNumberPagination

__author__ = 'rbalda'
class PaginacionPorDefecto(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pagina_tamanio'
    max_page_size = 100