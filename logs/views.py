from django.shortcuts import render
from django.http import HttpResponse
from logs.models import Model, Partprice, Cat
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, UpdateView, CreateView



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class  CatListView(ListView):
    model = Cat
    ordering = ['category']
    #queryset = Model.objects.order_by('name')