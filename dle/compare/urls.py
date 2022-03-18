from django.urls import path

from . import views

app_name = 'compare'
urlpatterns = [
    path('', views.index, name='index'),
    path('compare_all', views.compare_all, name='compare_all'),
    path('compare_diff', views.compare_all, name='compare_diff'),
    path('compare_match', views.compare_all, name='compare_match'),
]