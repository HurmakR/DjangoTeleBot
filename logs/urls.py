from django.urls import path

from . import views
from .views import ModelListView

app_name = 'logs'
urlpatterns = [
    path('', ModelListView.as_view(), name='model_list'),
]
