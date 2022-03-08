from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import render
from .search_mock_utils import SEARCH_RESULTS


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "search/search.html")
