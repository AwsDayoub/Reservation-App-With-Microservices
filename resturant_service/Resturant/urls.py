from django.urls import path
from . import views

urlpatterns = [
    path('search_for_resturants/<str:word>', views.SearchForResturants.as_view()),
    path('show_resturants/', views.ShowResturants.as_view())
]