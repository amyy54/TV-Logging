from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse

from django.contrib.auth.models import User
# Create your views here.
class LogListView(ListView):
    model = User
    context_object_name = "users"
    template_name = "home.html"
