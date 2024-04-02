from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from django.contrib.auth.models import User
from .models import Show
# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"
    context_object_name = "object_data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            context['current'] = [x for x in user.currentlywatching_set.order_by('-date') if x.episode < x.season.episodes][:3]
        else:
            context['current'] = []
        context["last_added_shows"] = Show.objects.order_by('-creation_date')[::-1][:3]
        return context

# class LogListView(ListView):
#     model = User
#     context_object_name = "users"
#     template_name = "home.html"
