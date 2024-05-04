from django.urls import path
from .views import HomeView, ShowListView, ShowDetailView, WatchingCreateView, WatchingUpdateView, WatchingDeleteView, AboutView, SeasonCreateView, SeasonUpdateView, SeasonDeleteView, ShowCreateView, ShowUpdateView, ShowDeleteView, WatchListView, InviteCreateView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("shows", ShowListView.as_view(), name="shows"),
    path("about", AboutView.as_view(), name="about"),
    path("show/new", ShowCreateView.as_view(), name="show_new"),
    path("show/<slug:abbreviation>", ShowDetailView.as_view(), name="show_detail"),
    path("show/<slug:abbreviation>/log", WatchingCreateView.as_view(), name="log_new"),
    path("show/<slug:abbreviation>/log/<int:pk>", WatchingUpdateView.as_view(), name="log_update"),
    path("show/<slug:abbreviation>/log/<int:pk>/delete", WatchingDeleteView.as_view(), name="log_delete"),
    path("show/<slug:abbreviation>/season/new", SeasonCreateView.as_view(), name="season_new"),
    path("show/<slug:abbreviation>/season/<int:pk>", SeasonUpdateView.as_view(), name="season_update"),
    path("show/<slug:abbreviation>/season/<int:pk>/delete", SeasonDeleteView.as_view(), name="season_delete"),
    path("show/<slug:abbreviation>/edit", ShowUpdateView.as_view(), name="show_update"),
    path("show/<slug:abbreviation>/delete", ShowDeleteView.as_view(), name="show_delete"),
    path("watchlist", WatchListView.as_view(), name="watchlist"),
    path("createinvite", InviteCreateView.as_view(), name="create_invite")
]
