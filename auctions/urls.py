from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addTOwatchlist/<int:id>", views.addTOwatchlist, name="addTOwatchlist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("createListing", views.createListing, name="createListing"),
    path("closeBid/<int:id>", views.closeBid, name="closeBid")
]
