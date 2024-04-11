from django.urls import path
from .views import HomeView, ShowListView, ShowDetailView, WatchingCreateView, WatchingUpdateView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("shows/", ShowListView.as_view(), name="shows"),
    path("show/<slug:abbreviation>", ShowDetailView.as_view(), name="show_detail"),
    path("show/<slug:abbreviation>/log", WatchingCreateView.as_view(), name="log_new"),
    path("show/<slug:abbreviation>/log/<int:pk>", WatchingUpdateView.as_view(), name="log_update")
]
