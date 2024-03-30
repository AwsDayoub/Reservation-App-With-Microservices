from django.urls import path
from . import views

urlpatterns = [
    path('search_for_hotels/<str:word>', views.SearchForHotels.as_view()),
    path('show_hotels/', views.ShowHotels.as_view())
]