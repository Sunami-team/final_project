from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10

    def get_page_size(self, request):
        custom_page_size = request.query_params.get("page_size")
        if custom_page_size:
            return min(int(custom_page_size), self.max_page_size)
        return self.page_size
