from django.urls import path

from . import views

app_name = 'compare'
urlpatterns = [
    path('', views.index, name='index'),
    path('list_labels', views.list_labels, name='list_labels'),
    path('compare_labels', views.compare_labels, name='compare_labels'),
    path('compare_versions', views.compare_versions, name='compare_versions'),
    path('compare_result', views.compare_result, name='compare_result'),
]