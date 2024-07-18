from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path('<str:title>', views.entryPage, name="entry"),
    path('search/', views.searchResults, name="searchResults"),
    path('add/', views.newPage, name="newPage"),
    path('edit/<str:title>', views.editPage, name="editPage"),
    path('save/', views.save, name="save"),
    path('random/', views.random, name="random")
]
