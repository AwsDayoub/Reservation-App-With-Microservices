from django.urls import path
from . import views

urlpatterns = [
    path('search_for_car_companies/<str:word>/', views.SearchForCarCompanies.as_view()),
    path('show_car_comapnies/', views.ShowCarCompanies.as_view()),
    path('show_car_company_details/<int:car_company_id>/', views.ShowCarCompanyDetails.as_view()),
    path('show_cars/<int:car_company_id>/', views.ShowCars.as_view()),
    path('show_car_details/<int:car_id>/', views.ShowCarDetails.as_view()),
    path('show_car_reservation_details/<int:car_id>/', views.ShowCarReservationDetails.as_view()),
    path('show_car_company_reservations_details/<int:car_company_id>/', views.ShowCarCompanyReservationsDetails.as_view()),
    path('show_car_company_comments/<int:car_company_id>/', views.ShowCarCompanyComments.as_view()),
    path('add_car_company/', views.AddCarCompany.as_view()),
    path('add_car_company_images/', views.AddCarCompanyImage.as_view()),
    path('add_car/', views.AddCar.as_view()),
    path('add_car_images/', views.AddCarImages.as_view()),
   # path('add_car_reservation/<int:car_id>/', views.AddCarReservation.as_view()),
    path('add_car_reservation_id_image/' , views.AddCarReservationIDImage.as_view()),
    path('add_car_company_comment/', views.AddCarCompanyComment.as_view()),
    path('update_car_company/', views.UpdateCarCompany.as_view()),
    path('update_car/', views.UpdateCar.as_view()),
    path('update_car_company_comment/', views.UpdateComment.as_view()),
    path('delete_car_company_image/<int:car_company_image_id>/', views.DeleteCarCompanyImage.as_view()),
    path('delete_car_image/<int:car_image_id>/', views.DeleteCarImage.as_view()),
    path('delete_car_company/<int:car_company_id>/', views.DeleteCarCompany.as_view()),
    path('delete_car/<int:car_id>/', views.DeleteCar.as_view()),
    path('delete_car_company_comment/<int:car_company_comment_id>/', views.DeleteCarCompanyComment.as_view()),
]