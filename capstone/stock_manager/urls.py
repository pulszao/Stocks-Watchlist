from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_watchlist/<str:stock>", views.remove_watchlist, name="remove_watchlist"),
    path("portfolio", views.portfolio, name="portfolio"),
    path("transactions", views.transactions, name="transactions"),
    path("remove_transactions/<int:id>", views.remove_transactions, name="remove_transactions"),
    path("chart", views.chart, name="chart"),
]