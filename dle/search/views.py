from django.http import (
    HttpRequest,
    HttpResponse
)
from django.shortcuts import render
from .search_mock_utils import SEARCH_RESULTS


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "search/search.html")

def list_search_results(request: HttpRequest) -> HttpResponse:
    print(request.method)
    print(request.body)
    context = {
        'search_results': SEARCH_RESULTS
    }
    return render(request, "search/search_results.html", context=context)