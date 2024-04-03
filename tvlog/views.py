from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.db.models import F
from .models import Show
# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"
    context_object_name = "object_data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            context['current'] = [x for x in user.currentlywatching_set.order_by('-date') if x.episode < x.season.episodes]
        context["last_added_shows"] = Show.objects.order_by('creation_date')[::-1][:3]
        return context

class ShowListView(ListView):
    model = Show
    template_name = "shows.html"
    context_object_name = "shows"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('q', '')

        queryset = queryset.order_by(F('enddate').asc(nulls_last=True), '-startdate')[::-1]

        result = [x for x in queryset if search_query.lower() in x.name.lower()]

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('q', '')

        context['search_query'] = search_query

        return context

class ShowDetailView(DetailView):
    model = Show
    template_name = "show_detail.html"
    context_object_name = "show"
    slug_field = 'abbreviation'
    slug_url_kwarg = 'abbreviation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['seasons'] = context['show'].season_set.order_by('startdate')
        context['seasonplural'] = len(context['seasons']) > 1

        user = self.request.user
        if user.is_authenticated:
            currentlywatching = user.currentlywatching_set.filter(season__in=context['seasons']).order_by('season__startdate')

            context['progress_watching'] = [x for x in currentlywatching if x.episode < x.season.episodes]
            context['progress_watched'] = [x for x in currentlywatching if x.episode >= x.season.episodes]
            context['show_progress'] = len(currentlywatching) > 0

        return context

# class LogListView(ListView):
#     model = User
#     context_object_name = "users"
#     template_name = "home.html"
