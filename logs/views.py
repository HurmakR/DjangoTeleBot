from django.shortcuts import render
from django.http import HttpResponse
from logs.models import Model
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, UpdateView, CreateView

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class ModelListView(ListView):
    model = Model
    #queryset = Model.objects.order_by('name')