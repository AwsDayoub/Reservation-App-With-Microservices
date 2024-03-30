from django.urls import path
from .views import *

urlpatterns = [
    path('signup/' , Register.as_view() , name='register'),
    path('SendEmailAndReceiveVerificationCodeEmail/<str:email>' , SendEmailAndReceiveVerificationCodeEmail.as_view()),
    path('SendVerificationCode/' , SendVerificationCode.as_view()),
    path('login/', LogIn.as_view(), name='LogIn'),
    path('logout/', LogOut.as_view(), name='LogOut'),
    path('edit_user_info/', EditUserInfo.as_view() , name='edit_user_info'),
    path('password_reset/', ResetPassword.as_view()),
    path('delete_user/<str:username>/', DeleteUser.as_view())
]