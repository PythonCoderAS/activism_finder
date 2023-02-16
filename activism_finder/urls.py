from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search),
    path("list", views.list_activisms),
    path("tags", views.list_tags),
    path('<str:code>', views.individual),
    path("tag/<str:tag_name>", views.tag)
]
