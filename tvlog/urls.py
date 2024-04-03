from django.urls import path
from .views import HomeView, ShowListView, ShowDetailView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("shows/", ShowListView.as_view(), name="shows"),
    path("show/<slug:abbreviation>", ShowDetailView.as_view(), name="show_detail")
]
