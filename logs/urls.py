from django.urls import path

from . import views
from .views import CatListView

app_name = 'logs'
urlpatterns = [
    path('', CatListView.as_view(), name='cat_list'),
]
