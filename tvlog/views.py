from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse_lazy
from .models import Show, CurrentlyWatching, Season, UserEx
from .forms import NewLogForm
# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            context['current'] = [x for x in user.currentlywatching_set.order_by('-date') if x.episode < x.season.episodes]
            watched_shows = [x.season.show for x in user.currentlywatching_set.order_by('-date') if x.episode >= x.season.episodes]
            watched_shows = [x for x in watched_shows if x not in [y.season.show for y in context['current']]]

            # https://stackoverflow.com/a/480227
            seen = set()
            seen_add = seen.add
            context['last_watched_shows'] = [x for x in watched_shows if not (x in seen or seen_add(x))][:3]

        context["last_added_shows"] = Show.objects.order_by('creation_date')[::-1][:3]
        return context

class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_count'] = User.objects.all().count()
        context['show_count'] = Show.objects.all().count()
        context['log_count'] = CurrentlyWatching.objects.all().count()

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

            context['is_watchlist'] = context['show'] in user.userex.watchlist.all()

        return context

    def post(self, request, *args, **kwargs):
        show_req = request.POST.get('show')

        show = get_object_or_404(Show, abbreviation=show_req)
        userex = request.user.userex

        if show in userex.watchlist.all():
            userex.watchlist.remove(show)
        else:
            userex.watchlist.add(show)

        userex.save()

        return redirect("watchlist")

class WatchListView(LoginRequiredMixin, TemplateView):
    template_name = "watchlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['watchlist'] = user.userex.watchlist.all()

        return context

class WatchingCreateView(LoginRequiredMixin, CreateView):
    model = CurrentlyWatching
    template_name = "watching_create.html"
    form_class = NewLogForm
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['type'] = "new"

        user = self.request.user
        show = self.kwargs.pop('show', None)
        logged_seasons = user.currentlywatching_set.filter(season__show=show)
        context['logged_seasons'] = [x.season for x in logged_seasons]

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        slug = self.kwargs.pop('abbreviation', None)
        show = get_object_or_404(Show, abbreviation=slug)
        kwargs['show'] = show
        self.kwargs['show'] = show

        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class WatchingUpdateView(LoginRequiredMixin, UpdateView):
    model = CurrentlyWatching
    template_name = "watching_create.html"
    context_object_name = "watching"
    fields = ["date", "episode", "rating", "rewatch"]
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['type'] = "update"

        return context

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def form_valid(self, form, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            raise Http404
        else:
            return super().form_valid(form)

class WatchingDeleteView(LoginRequiredMixin, DeleteView):
    model = CurrentlyWatching
    template_name = "object_delete.html"
    context_object_name = "watching"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['flavor_string'] = f"{self.request.user.username}'s log for {context['watching'].season.show.name} - Season {context['watching'].season.name}"

        return context

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def form_valid(self, form, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            raise Http404
        else:
            return super().form_valid(form)

class SeasonCreateView(LoginRequiredMixin, CreateView):
    model = Season
    template_name = "season_create.html"
    fields = ["name", "episodes", "startdate"]
    success_url = reverse_lazy("shows")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['type'] = "new"

        return context

    def get_form(self):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().get_form()

    def form_valid(self, form, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            slug = self.kwargs.pop('abbreviation', None)
            show = get_object_or_404(Show, abbreviation=slug)
            form.instance.show = show
            return super().form_valid(form)

class SeasonUpdateView(LoginRequiredMixin, UpdateView):
    model = Season
    template_name = "season_create.html"
    fields = ["name", "episodes", "startdate"]
    context_object_name = "season"
    success_url = reverse_lazy("shows")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['type'] = "update"

        return context

    def get_object(self, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().get_object(*args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().form_valid(form)

class SeasonDeleteView(LoginRequiredMixin, DeleteView):
    model = Season
    template_name = "object_delete.html"
    context_object_name = "season"
    success_url = reverse_lazy("shows")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['flavor_string'] = f"{context['season'].show.name} - Season {context['season'].name} ({context['season'].episodes})"

        return context

    def get_object(self, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().get_object(*args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().form_valid(form)

class ShowCreateView(LoginRequiredMixin, CreateView):
    model = Show
    template_name = "show_create.html"
    fields = ["name", "startdate", "enddate", "boxart", "abbreviation"]
    success_url = reverse_lazy("shows")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['type'] = "new"

        return context

    def get_form(self):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().get_form()

    def form_valid(self, form, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().form_valid(form)

class ShowUpdateView(LoginRequiredMixin, UpdateView):
    model = Show
    template_name = "show_create.html"
    fields = ["name", "startdate", "enddate", "boxart", "abbreviation"]
    context_object_name = "show"
    success_url = reverse_lazy("shows")
    slug_field = 'abbreviation'
    slug_url_kwarg = 'abbreviation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['type'] = "update"

        return context

    def get_object(self, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().get_object(*args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().form_valid(form)

class ShowDeleteView(LoginRequiredMixin, DeleteView):
    model = Show
    template_name = "object_delete.html"
    context_object_name = "show"
    success_url = reverse_lazy("shows")
    slug_field = 'abbreviation'
    slug_url_kwarg = 'abbreviation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['flavor_string'] = f"{context['show'].name}"

        return context

    def get_object(self, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().get_object(*args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        if not self.request.user.userex.isEditor:
            raise Http404
        else:
            return super().form_valid(form)
